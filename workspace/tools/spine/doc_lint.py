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
  python3 doc_lint.py DIGEST.md STANDING.md --docs WORKSPACE --state   # also the state checks (resume.py, launch.py, docstate.py)
  python3 doc_lint.py --plan PLAN.md                          # a plan file before launch (launch.py runs this)

Path, state and plan checks:
- path_errors (gate, launch gate): the runbook and STANDING_DIRECTIONS name no path that does not exist: a document
  that lives in the private docs/ cited as claude/<doc> or repair/efficiency/<doc>, or a tools/, repair/efficiency/,
  repair/ui/, docs/ or claude/ path missing from the clones. Placeholders (<batch>, sNN, *) and claude/pending/ (plan
  files, kept in the project until launch) are skipped; claude/RESUME.md, claude/STEP2HAKI_HANDOFF.md and
  claude/PLAN_TEMPLATE.md are the project mirrors.
- state_errors (gate; resume.py and launch.py print them at chat start): the same path check on RESUME and the handoff;
  RESUME's "**Batch state: ...**" line equals the head of the first handoff State entry; the State holds at most
  STATE_CAP entries (the open batch, the last ship, one in transit). tools/spine/docstate.py sync writes the line and
  moves older entries to docs/SHIPLOG.md.
- unfiled_errors (gate, launch gate): a live digest line whose topic is not "process" is cited by a rule document
  (STANDING_DIRECTIONS, the runbook, RULE_DOCS, docs/ui/) or ends "(one-time)"; a decision that sets a standing rule
  and reaches no rule document fails.
- allow_errors (gate, launch gate): an allow list holds no more entries than tools/spine/allow_baseline.json records,
  and the baseline row names a digest id; a list may shrink freely.
- core_rules: the numbered core rules of STANDING_DIRECTIONS, printed by resume.py and launch.py at chat start.
- plan_errors: in a plan file (PLAN_TEMPLATE.md), every Evidence list line is marked TESTED or ASSUMED (on the line or
  on its heading) and every open call carries "Recommendation:".
"""
import os, re, sys

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

RULE_DOCS = ['@BATCH_RUNBOOK.md', 'repair/efficiency/CARD_SPEC.md', 'repair/efficiency/TEXTBOOK_STYLE.md',
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
        path = os.path.join(os.path.dirname(digest), rel[1:]) if rel.startswith('@') else os.path.join(ws, rel)
        if not os.path.exists(path):
            continue
        for cited in sorted(set(re.findall(r'\[(D-\d{8}-\d+)\]', open(path, encoding='utf-8').read()))):
            if cited not in d:
                errs.append(f'{rel} cites {cited}, which is not in the digest')
            elif d[cited]['superseded_by']:
                errs.append(f'{rel} cites {cited}, superseded by {d[cited]["superseded_by"][0]}: update the line')
    return errs


DOCS_HOME = {'BATCH_RUNBOOK.md', 'STANDING_DIRECTIONS.md', 'DECISIONS_DIGEST.md', 'OPEN_WORK.md', 'OPEN_WORK_CLOSED.md',
             'STEP2HAKI_HANDOFF.md', 'RESUME.md', 'SHIPLOG.md', 'PLAN_TEMPLATE.md'}
PROJECT_MIRRORS = {'claude/RESUME.md', 'claude/STEP2HAKI_HANDOFF.md', 'claude/PLAN_TEMPLATE.md'}
PROJECT_MIRRORS.add('claude/design/Workup_5a.html')   # a design file kept in the project only
PATH_DOCS = ['BATCH_RUNBOOK.md', 'STANDING_DIRECTIONS.md']       # stable rule documents: checked in the gate
STATE_DOCS = ['RESUME.md', 'STEP2HAKI_HANDOFF.md']               # rewritten every step: checked with the state checks
STATE_CAP = 3
PATH = re.compile(r'(?<![\w/.~<-])((?:workspace/)?(?:repair/efficiency|repair/ui|tools|claude|docs)/[\w./<>*-]*[\w>*])')
PLACEHOLDER = re.compile(r'[<>*]|sNN|NNN|\.\.\.')


def path_errors(docs_dir, ws, names=None):
    """A named path must exist (see the module docstring). docs_dir is the private docs/ folder, ws the public
    workspace/."""
    priv = os.path.dirname(os.path.abspath(docs_dir)); errs = []
    for name in names or PATH_DOCS:
        f = os.path.join(docs_dir, name)
        if not os.path.exists(f):
            continue
        seen = set()
        for n, line in enumerate(open(f, encoding='utf-8').read().splitlines(), 1):
            for m in PATH.finditer(line):
                tok = m.group(1); p = tok[len('workspace/'):] if tok.startswith('workspace/') else tok
                if PLACEHOLDER.search(p) or p.startswith('claude/pending/') or p in PROJECT_MIRRORS or (name, tok) in seen:
                    continue
                base = os.path.basename(p); why = None
                if p.startswith('docs/'):
                    if not os.path.exists(os.path.join(priv, p)): why = 'is not in the private repo'
                elif base in DOCS_HOME:
                    why = 'names a document that lives in the private docs/ (write docs/%s)' % base
                elif p.startswith('claude/'):
                    if not os.path.exists(os.path.join(priv, p)): why = 'is not in the private repo'
                elif not os.path.exists(os.path.join(ws, p)):
                    why = 'is not in the workspace'
                if why:
                    seen.add((name, tok)); errs.append('%s line %d: path %s %s' % (name, n, tok, why))
    return errs


ONE_TIME = '(one-time)'


def unfiled_errors(digest, ws):
    """Live rule-topic digest ids cited by no rule document and not marked one-time."""
    import glob
    d = parse(digest); docs = os.path.dirname(os.path.abspath(digest))
    paths = [os.path.join(docs, 'STANDING_DIRECTIONS.md'), os.path.join(docs, 'BATCH_RUNBOOK.md'), os.path.join(docs, 'PLAN_TEMPLATE.md')]
    paths += sorted(glob.glob(os.path.join(docs, 'ui', '*.md'))) + [os.path.join(ws, r) for r in RULE_DOCS if not r.startswith('@')]
    cited = set()
    for p in paths:
        if os.path.exists(p):
            cited |= set(re.findall(r'D-\d{8}-\d+', open(p, encoding='utf-8').read()))
    return ['%s {%s} sets a rule cited by no rule document: write the rule into one with its id, or end the digest line "%s"'
            % (k, e['topic'], ONE_TIME) for k, e in d.items()
            if e['topic'] != 'process' and not e['superseded_by'] and k not in cited and not e['text'].rstrip().endswith(ONE_TIME)]


def allow_count(path):
    """Entries in an allow list: the longest list in a JSON file, or the non-comment lines of a text file."""
    if path.endswith('.json'):
        import json
        j = json.load(open(path, encoding='utf-8'))
        return max([len(v) for v in (j.values() if isinstance(j, dict) else [j]) if isinstance(v, list)] or [0])
    return sum(1 for l in open(path, encoding='utf-8') if l.strip() and not l.lstrip().startswith('#'))


def allow_errors(digest, ws):
    """Each allow list in tools/spine/allow_baseline.json holds at most its recorded count, under a known digest id."""
    import json
    bp = os.path.join(ws, 'tools', 'spine', 'allow_baseline.json')
    if not os.path.exists(bp):
        return ['tools/spine/allow_baseline.json is missing; restore it from git']
    d = parse(digest); errs = []
    for rel, row in json.load(open(bp, encoding='utf-8')).items():
        p = os.path.join(ws, rel)
        if not os.path.exists(p):
            continue
        n = allow_count(p)
        if n > row['count']:
            errs.append('%s holds %d entries, baseline %d: a new entry needs a digest id (raise the count and name the id in allow_baseline.json)' % (rel, n, row['count']))
        if row.get('id') not in d:
            errs.append('allow_baseline.json: %s names %s, which is not in the digest' % (rel, row.get('id')))
    return errs


def core_rules(standing_text):
    """The numbered lines under the "Core rules" heading of STANDING_DIRECTIONS."""
    m = re.search(r'^## Core rules[^\n]*\n(.*?)(?=^\S(?!\d*\.)|\Z)', standing_text, re.S | re.M)
    return [l for l in (m.group(1) if m else '').split('\n') if re.match(r'\d+\. ', l)]


def stable_errors(digest, standing, ws):
    """Every check on the documents that change only by decision: the gate and the launch gate run this."""
    return (errors(digest, standing) + rule_doc_errors(digest, ws) + path_errors(os.path.dirname(os.path.abspath(digest)), ws)
            + unfiled_errors(digest, ws) + allow_errors(digest, ws))


def state_entries(handoff_text):
    """[(head, body)] for each "- **head** ..." entry of the handoff's State section, in file order; "Previous: " is
    dropped from the head. An entry runs to the next entry or the first line that is neither indented nor blank."""
    m = re.search(r'^## State\b.*?\n(.*?)(?=^## |\Z)', handoff_text, re.S | re.M)
    out = []; cur = None
    for line in (m.group(1) if m else '').split('\n'):
        h = re.match(r'- \*\*(.+?)\*\*', line)
        if h:
            cur = [re.sub(r'^Previous: ', '', h.group(1)), [line]]; out.append(cur)
        elif cur is not None and (line.startswith(' ') or not line.strip()):
            cur[1].append(line)
        else:
            cur = None
    return [(h, '\n'.join(b).rstrip()) for h, b in out]


RESUME_LINE = re.compile(r'^\*\*Batch state: (.+?)\*\*', re.M)


def state_errors(docs_dir, ws):
    """Checks on the files rewritten every step: paths in RESUME and the handoff, RESUME's batch line, the State cap."""
    errs = path_errors(docs_dir, ws, STATE_DOCS)
    hp, rp = os.path.join(docs_dir, 'STEP2HAKI_HANDOFF.md'), os.path.join(docs_dir, 'RESUME.md')
    if not (os.path.exists(hp) and os.path.exists(rp)):
        return errs + ['STEP2HAKI_HANDOFF.md or RESUME.md is missing from ' + docs_dir]
    ents = state_entries(open(hp, encoding='utf-8').read())
    if not ents:
        return errs + ['the handoff State has no "- **<batch> <STATUS> <date>**" entry']
    m = RESUME_LINE.search(open(rp, encoding='utf-8').read())
    if not m:
        errs.append('RESUME has no "**Batch state: ...**" line (python3 tools/spine/docstate.py sync writes it)')
    elif m.group(1) != ents[0][0]:
        errs.append('RESUME batch line reads "%s"; the handoff State reads "%s" (python3 tools/spine/docstate.py sync)' % (m.group(1), ents[0][0]))
    if len(ents) > STATE_CAP:
        errs.append('the handoff State holds %d entries, cap %d: python3 tools/spine/docstate.py sync moves the older ones to docs/SHIPLOG.md' % (len(ents), STATE_CAP))
    return errs


def plan_errors(plan_path):
    """A plan file is ready to launch when every Evidence list line is marked TESTED or ASSUMED (itself or its
    heading) and every open call carries a recommendation (PLAN_TEMPLATE.md)."""
    errs = []; sec = ''; head_marked = False; call = None
    mark = re.compile(r'\b(TESTED|ASSUMED)\b')

    def close_call():
        if call and 'Recommendation:' not in call[1]:
            errs.append('%s: open call %s has no "Recommendation:"' % (os.path.basename(plan_path), call[0]))
    for line in open(plan_path, encoding='utf-8').read().splitlines() + ['## end']:
        if line.startswith('## '):
            close_call(); call = None
            sec = line[3:].strip(); head_marked = bool(mark.search(line)); continue
        if sec.startswith('Evidence'):
            if line.startswith('#'):
                head_marked = bool(mark.search(line))
            elif re.match(r'(- |\d+\. )', line) and not head_marked and not mark.search(line):
                errs.append('%s: Evidence line is neither TESTED nor ASSUMED: %s' % (os.path.basename(plan_path), line[:70]))
        elif sec.startswith('Open calls'):
            n = re.match(r'(\d+)\. ', line)
            if n:
                close_call(); call = [n.group(1), line]
            elif call:
                call[1] += '\n' + line
    return errs


def main(a):
    if '--plan' in a:
        errs = plan_errors(a[a.index('--plan') + 1])
        if errs: print('PLAN-LINT FAIL'); [print(' ', x) for x in errs]; return 1
        print('PLAN-LINT PASS'); return 0
    if len(a) < 2: print(__doc__); return 2
    d = parse(a[0]); standing = open(a[1], encoding='utf-8').read(); errs = errors(a[0], a[1])
    if '--docs' in a:
        ws = a[a.index('--docs') + 1]
        errs = stable_errors(a[0], a[1], ws)
        if '--state' in a:
            errs += state_errors(os.path.dirname(os.path.abspath(a[0])), ws)
    if '--topic' in a:
        t = a[a.index('--topic') + 1]
        live = sorted([(e['date'], k, e['text']) for k, e in d.items() if e['topic'] == t and not e['superseded_by']], reverse=True)
        print(f'live decisions on {{{t}}}, newest first:'); [print(' ', x[0], x[1], x[2][:160]) for x in live]
    if errs: print('DOC-LINT FAIL'); [print(' ', x) for x in errs]; return 1
    print(f'DOC-LINT PASS ({len(d)} ids checked)'); return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
