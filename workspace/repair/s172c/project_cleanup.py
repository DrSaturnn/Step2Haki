#!/usr/bin/env python3
"""project_cleanup.py (s172c step 7, picks 1 and 2): classify every project document by whether a repo holds a record
of it. Input: project_docs.txt (the project's doc list, 2026-11-10). A record is (a) the same relative path in the
private repo, (b) the same file name anywhere in either clone (git ls-files; generic names such as lean.py excluded), or (c) for a file named for a shipped
batch, that batch's file workspace/repair/<batch>/<BATCH>.md (the folder alone is not a record). Names only: the project copies were not compared byte for byte.
Output: project_cleanup.md with DELETE (record found) and KEEP (live, or no record) lists."""
import os, re, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
PUB, PRIV = '/home/claude/Step2Haki', '/home/claude/step2haki-private'
ls = lambda r: subprocess.run(['git', '-C', r, 'ls-files'], capture_output=True, text=True).stdout.split('\n')
pub, priv = ls(PUB), ls(PRIV)
privset = set(priv)
byname = collections.defaultdict(list)
for repo, files in (('public', pub), ('private', priv)):
    for f in files:
        byname[os.path.basename(f)].append(repo + ':' + f)
LIVE = {  # kept on purpose
    'claude/RESUME.md': 'mirror of docs/RESUME.md', 'claude/STEP2HAKI_HANDOFF.md': 'the project instruction\'s copy',
    'claude/PLAN_TEMPLATE.md': 'mirror of docs/PLAN_TEMPLATE.md', 'claude/pending/DOCS_REFACTOR.md': 's172c plan, open until its ship',
    'claude/pending/S172B.md': 'picked, not launched', 'claude/pending/CONTENT_BATCHES_S170.md': 'launch prompts s173 to s181',
    'claude/pending/S166_PHONE_PILOT.md': 's166 paused, not shipped', 'claude/pending/POST_SHIP_R3.md': 'read order, conditional PASS',
    'claude/pending/BRIEF_AMEND_LIST.md': 'work queue', 'claude/design/Workup_5a.html': 'design file named by STANDING_DIRECTIONS',
    'claude/pending/POST_REFACTOR_LEDGER.md': 'ledger N1 to N20, items open', 'claude/pending/NEW_BRIEFS_2026-10-26.md': 'open proposals',
    'claude/pending/NEW_BRIEFS_2026-10-30.md': 'open proposals', 'claude/pending/NBME_PRESENTATION_SPEC.md': 'mockup not built',
}
LIVE_PREFIX = {'claude/pending/two_pane_r2/': 's172b scripts', 'claude/pending/mobilenav/': 's166 paused', 'claude/pending/nbme_mockup/': 'mockup not built'}
RULE = {'claude/TEXTBOOK_STYLE.md', 'claude/CARD_SPEC.md', 'claude/SPINE_SCALE_PLAN.md', 'claude/SPINE_SPEC.md', 'claude/design/WORKUP_5A_SPEC.md', 'claude/PHASE0_SCRIPTS.md'}
GENERIC = {'make_batch.py', 'lean.py', 'setup.py', 'build.py', 'packet.py', 'lib.js'}   # a shared file name is not a record
delete, keep = [], []
for p in [l.strip() for l in open(os.path.join(HERE, 'project_docs.txt')) if l.strip()]:
    why = LIVE.get(p) or next((v for k, v in LIVE_PREFIX.items() if p.startswith(k)), None)
    if why:
        keep.append((p, 'live: ' + why)); continue
    base = os.path.basename(p); rec = None
    if p in privset:
        rec = 'private:' + p
    elif byname.get(base) and base not in GENERIC:
        rec = byname[base][0] + (' (+%d)' % (len(byname[base]) - 1) if len(byname[base]) > 1 else '')
    else:
        m = re.search(r'(?:^|/)[Ss](\d{3}[a-zA-Z]?)(?:[_./]|$)', p[len('claude/pending/'):] if p.startswith('claude/pending/') else '')
        b = 's' + m.group(1).lower() if m else ''
        if m and os.path.exists(os.path.join(PUB, 'workspace', 'repair', b, b.upper() + '.md')):
            rec = 'public:workspace/repair/%s/%s.md' % (b, b.upper())
    if rec:
        delete.append((p, ('pick 1, rule document; ' if p in RULE else 'pick 2; ') + 'record ' + rec))
    else:
        keep.append((p, 'no record found in either repo'))
out = ['# s172c step 7: project documents (made by project_cleanup.py, 2026-11-10)', '',
       'Record test: names only (same path in the private repo, same file name in either clone, or the batch folder).',
       '', '## DELETE from the project (%d)' % len(delete), ''] + ['- %s: %s' % x for x in delete] + \
      ['', '## KEEP (%d)' % len(keep), ''] + ['- %s: %s' % x for x in keep]
open(os.path.join(HERE, 'project_cleanup.md'), 'w').write('\n'.join(out) + '\n')
print(len(delete), 'delete;', len(keep), 'keep;', sum(1 for _, w in keep if w.startswith('no record')), 'kept for no record')
