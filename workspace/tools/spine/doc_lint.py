"""doc_lint.py (2026-11-05; wired into tools/gate.py as check doc-lint, D-20261106-11): keeps DECISIONS_DIGEST and STANDING_DIRECTIONS from holding two live answers to one question.
Runs in tools/gate.py on every gate run (ship, launch gate) and from the command line before any doc commit.

Conventions it enforces, for every digest line written from 2026-11-05 on (older lines get ids in the refactor's audit):
- the line starts "- YYYY-MM-DD [D-YYYYMMDD-n] {topic}" ; topic is a short tag (workup, sidebar, fit, motion, theme ...);
- a line that changes an earlier decision says "supersedes D-..." ; the earlier line must then end "(superseded by D-...)";
- STANDING_DIRECTIONS cites digest ids as [D-...] ; citing a superseded id fails.

Usage:
  python3 doc_lint.py DIGEST.md STANDING.md            # fail (exit 1) on broken supersession or stale citations
  python3 doc_lint.py DIGEST.md STANDING.md --topic workup   # every live decision on one topic, newest first
  python3 doc_lint.py DIGEST.md STANDING.md --docs WORKSPACE  # also every rule document in RULE_DOCS (the gate runs this)
"""
import re, sys

LINE = re.compile(r'^- (\d{4}-\d{2}-\d{2}) \[(D-\d{8}-\d+)\] \{([\w-]+)\}(.*)$')

def parse(digest):
    out = {}
    for raw in open(digest, encoding='utf-8').read().splitlines():
        m = LINE.match(raw)
        if m:
            date, did, topic, rest = m.groups()
            out[did] = {'date': date, 'topic': topic, 'text': rest.strip(),
                        'supersedes': re.findall(r'supersedes (D-\d{8}-\d+)', rest),
                        'superseded_by': re.findall(r'\(superseded by (D-\d{8}-\d+)\)', rest)}
    return out

def errors(digest, standing_path):
    d = parse(digest); standing = open(standing_path, encoding='utf-8').read(); errs = []
    for did, e in d.items():
        for t in e['supersedes']:
            if t not in d: errs.append(f'{did} supersedes {t}, which is not in the digest')
            elif did not in d[t]['superseded_by']: errs.append(f'{t} is superseded by {did} but not marked "(superseded by {did})"')
    for cited in sorted(set(re.findall(r'\[(D-\d{8}-\d+)\]', standing))):
        if cited in d and d[cited]['superseded_by']:
            errs.append(f'STANDING_DIRECTIONS cites {cited}, superseded by {d[cited]["superseded_by"][0]}: update the line')
        if cited not in d: errs.append(f'STANDING_DIRECTIONS cites {cited}, which is not in the digest')
    return errs

RULE_DOCS = ['repair/efficiency/BATCH_RUNBOOK.md', 'repair/efficiency/CARD_SPEC.md', 'repair/efficiency/TEXTBOOK_STYLE.md',
             'repair/efficiency/RULES_voice.md', 'repair/efficiency/RULES_worker.md', 'repair/efficiency/RULES_coverage.md',
             'repair/efficiency/RUBRIC.md', 'repair/efficiency/RUBRIC_migration.md', 'repair/efficiency/WORKUP_5A_SPEC.md',
             'repair/efficiency/SPINE_SCALE_PLAN.md', 'repair/efficiency/CODEX_LEAD.md', 'tools/MIGRATION_CONTRACT.md',
             'tools/spine/BUILD_CONTRACT.md', 'tools/spine/BUILD_CONTRACT_CARD.md', 'tools/hooks/agents/lean-builder.md',
             'tools/hooks/agents/lean-reviewer.md', 'tools/plugin/step2haki-tools/agents/lean-builder.md',
             'tools/plugin/step2haki-tools/agents/lean-reviewer.md']


def rule_doc_errors(digest, ws):
    """Every rule document (RULE_DOCS, paths relative to the workspace) cites live digest ids only: a bracketed [D-...]
    citation of a superseded or unknown id fails (D-20261106-10)."""
    import os
    d = parse(digest); errs = []
    for rel in RULE_DOCS:
        path = os.path.join(ws, rel)
        if not os.path.exists(path):
            continue
        for cited in sorted(set(re.findall(r'\[(D-\d{8}-\d+)\]', open(path, encoding='utf-8').read()))):
            if cited not in d:
                errs.append(f'{rel} cites {cited}, which is not in the digest')
            elif d[cited]['superseded_by']:
                errs.append(f'{rel} cites {cited}, superseded by {d[cited]["superseded_by"][0]}: update the line')
    return errs


def main(a):
    if len(a) < 2: print(__doc__); return 2
    d = parse(a[0]); standing = open(a[1], encoding='utf-8').read(); errs = errors(a[0], a[1])
    if '--docs' in a:
        errs += rule_doc_errors(a[0], a[a.index('--docs') + 1])
    if '--topic' in a:
        t = a[a.index('--topic') + 1]
        live = sorted([(e['date'], k, e['text']) for k, e in d.items() if e['topic'] == t and not e['superseded_by']], reverse=True)
        print(f'live decisions on {{{t}}}, newest first:'); [print(' ', x[0], x[1], x[2][:160]) for x in live]
    if errs: print('DOC-LINT FAIL'); [print(' ', x) for x in errs]; return 1
    print(f'DOC-LINT PASS ({len(d)} ids checked)'); return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
