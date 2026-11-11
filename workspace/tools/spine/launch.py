#!/usr/bin/env python3
"""launch.py: the read order for a launch, by batch type.

  python3 tools/spine/launch.py <content|patch|site|tools|plan> [--plan FILE] [--batch ID]

Prints every document the batch type reads, with the line range and size of each section (read them with
sed -n A,Bp), the total against the old ten-document order read whole, and the doc and state checks
(doc_lint). With --batch ID it first refuses a batch that is already open (the handoff State shows the id OPEN, or the
branch wip/<id> exists on the remote of either repo): a second chat continues an open batch through RESUME path A and
never launches it again. With --plan FILE it checks the plan file (doc_lint.plan_errors); with --batch ID as well, a
passing plan is copied to docs/batches/<batch>/PLAN.md in the private repo, the batch record from then on. The table in the runbook ("Read order by batch
type") names the same documents; ORDER below is what a launch follows.

A document outside a type's list is grepped for the topic of the edit in hand. DECISIONS_DIGEST is never read whole.
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(WS, 'tools'))
import doc_lint  # noqa: E402
import docs_path  # noqa: E402

R, S, H = '@BATCH_RUNBOOK.md', '@STANDING_DIRECTIONS.md', '@STEP2HAKI_HANDOFF.md'
EFF = 'repair/efficiency/'
RUN_HEAD = 'top'          # the runbook's text before section 1 (read order, token rules)
# (document, None for whole, or a list of heading prefixes). '@' = private docs/, '^' = private repo root, else workspace.
ORDER = {
    'content': [(H, None), (R, [RUN_HEAD, '1.', '2.', '3.', '4.', '5.', '6.', '7.', '9.']), (S, None), (EFF + 'TEXTBOOK_STYLE.md', None),
                (EFF + 'SPINE_SCALE_PLAN.md', ['0', '2', '4', '5', '8']), ('^claude/SPINE_SPEC.md', None), (EFF + 'WORKUP_5A_SPEC.md', None)],
    'patch': [(H, None), (R, [RUN_HEAD, '3.', '7.', '8b.', '9.']), (S, None), (EFF + 'TEXTBOOK_STYLE.md', None)],
    'site': [(H, None), (R, [RUN_HEAD, '7.', '8.', '9.']), (S, ['Core rules', 'Display', 'Process and approvals', 'UI architecture']),
             ('@ui/UI_ARCHITECTURE.md', None), ('@ui/UI_MAP.md', None)],
    'tools': [(H, None), (R, [RUN_HEAD, '7.', '8.', '9.']), (S, ['Core rules', 'Process and approvals', 'Repo and files'])],
    'plan': [('@RESUME.md', ['C.', 'Reading rules']), ('@PLAN_TEMPLATE.md', None), (R, ['11.'])],
}
ALSO = {
    'content': ['the batch section of the plan file (claude/pending/, or private docs/batches/<batch>/PLAN.md)',
                'BRIEF_AMEND_LIST rows of the batch briefs (grep, private claude/pending/BRIEF_AMEND_LIST.md)',
                'conditional PASS: claude/pending/POST_SHIP_R3.md section 2 (project)'],
    'patch': ['the intake proposals named in the launch prompt', 'BRIEF_AMEND_LIST rows of the batch briefs (grep)'],
    'site': ['the batch plan file'], 'tools': ['the batch plan file'], 'plan': [],
}
OLD = [H, R, S, EFF + 'TEXTBOOK_STYLE.md', '@DECISIONS_DIGEST.md', EFF + 'SPINE_SCALE_PLAN.md', '^claude/pending/BRIEF_AMEND_LIST.md',
       '^claude/SPINE_SPEC.md', EFF + 'WORKUP_5A_SPEC.md']


def path(ref):
    if ref.startswith('@'):
        return docs_path.doc(ref[1:])
    if ref.startswith('^'):
        return os.path.join(docs_path.private_root(), ref[1:])
    return os.path.join(WS, ref)


def sections(text):
    """[(title, first line, last line, bytes)] for the text before the first "## " ('top') and each "## " section."""
    lines = text.split('\n')
    starts = [(0, RUN_HEAD)] + [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith('## ')]
    out = []
    for k, (i, t) in enumerate(starts):
        j = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        out.append((t, i + 1, j, len('\n'.join(lines[i:j]).encode('utf-8'))))
    return out


def remote_heads(repo, batch):
    """names of the remote branches wip/<batch> of one clone (empty when there is none or the remote cannot be read)"""
    try:
        r = subprocess.run(['git', '-C', repo, 'ls-remote', '--heads', 'origin', 'wip/' + batch],
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return []
    return [l.split('\t')[-1] for l in r.stdout.splitlines() if l.strip()]


def open_reasons(batch, handoff_text, heads=remote_heads, repos=None):
    """why a launch of batch must stop: one line per sign that the batch is already open"""
    why = []
    for head, _ in doc_lint.state_entries(handoff_text):
        if re.match(r'%s OPEN\b' % re.escape(batch), head):
            why.append('the handoff State shows "%s"' % head)
    if repos is None:
        repos = [('public', os.path.dirname(WS)), ('private', docs_path.private_root())]
    for name, repo in repos:
        if heads(repo, batch):
            why.append('the %s repo has the remote branch wip/%s' % (name, batch))
    return why


def main(a):
    if not a or a[0] not in ORDER:
        print(__doc__); return 2
    if '--batch' in a:
        b = a[a.index('--batch') + 1]
        why = open_reasons(b, open(path(H), encoding='utf-8').read())
        if why:
            print('LAUNCH REFUSED: batch %s is already open (%s). Continue it in this chat through RESUME path A '
                  '("Step2Haki: continue the current batch per claude/RESUME.md"); a new batch needs a new id.' % (b, '; '.join(why)))
            return 1
    kind = a[0]; total = 0; missing = 0
    print('Core rules (STANDING_DIRECTIONS):')
    for l in doc_lint.core_rules(open(path(S), encoding='utf-8').read()):
        print('  ' + l)
    print('Read order for a %s launch (sed -n A,Bp FILE for a range):' % kind)
    for ref, want in ORDER[kind]:
        p = path(ref)
        if not os.path.exists(p):
            print('  MISSING %s' % p); missing += 1; continue
        text = open(p, encoding='utf-8').read()
        if want is None:
            n = len(text.encode('utf-8')); total += n
            print('  %-78s whole  %6.1f KB' % (p, n / 1024))
            continue
        print('  %s' % p)
        secs = sections(text)
        for w in want:
            hit = [s for s in secs if s[0] == w or s[0].startswith(w + ' ') or s[0].startswith(w)]
            hit = hit[:1]
            if not hit:
                print('      MISSING section "%s"' % w); missing += 1; continue
            t, x, y, n = hit[0]; total += n
            print('      %5d,%-5d %6.1f KB  %s' % (x, y, n / 1024, t[:70]))
    for line in ALSO[kind]:
        print('  also: ' + line)
    print('  DECISIONS_DIGEST: grep the batch id and its briefs; tail the last 20 dated lines; doc_lint.py --topic <tag> per topic')
    old = sum(os.path.getsize(path(r)) for r in OLD if os.path.exists(path(r)))
    print('Total listed: %.1f KB. The ten-document order read whole: %.1f KB (%d%% of it).' % (total / 1024, old / 1024, round(100.0 * total / old)))
    print('Record in the batch file: this total, and the context at the first edit (python3 tools/hooks/usage_ledger.py --context).')
    docs = docs_path.docs_dir()
    dg, st = os.path.join(docs, 'DECISIONS_DIGEST.md'), os.path.join(docs, 'STANDING_DIRECTIONS.md')
    errs = doc_lint.stable_errors(dg, st, WS) + doc_lint.state_errors(docs, WS)
    rc = 1 if (errs or missing) else 0
    if '--plan' in a:
        plan = a[a.index('--plan') + 1]
        perr = doc_lint.plan_errors(plan)
        errs += perr
        if perr:
            rc = 1
        elif '--batch' in a:
            dest = os.path.join(docs_path.batch_dir(a[a.index('--batch') + 1]), 'PLAN.md')
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if os.path.abspath(plan) != dest:
                shutil.copyfile(plan, dest)
            print('Plan file passes; batch record (private repo): %s' % os.path.relpath(dest, docs_path.private_root()))
    for e in errs:
        print('  DOC-LINT', e)
    print('DOC-LINT %s' % ('FAIL (%d)' % len(errs) if errs else 'PASS'))
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
