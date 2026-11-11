#!/usr/bin/env python3
"""docstate.py: keeps the three state files in
step after the lead rewrites the handoff State by hand.

  python3 tools/spine/docstate.py sync      # run after every State rewrite, before the commit
  python3 tools/spine/docstate.py check     # the state checks only (doc_lint.state_errors)
  python3 tools/spine/docstate.py copies    # the files a ship copies out, with sizes (project and Mac copies)

sync does three things in the private docs/ (tools/docs_path.py):
1. moves State entries beyond KEEP (the first two: the open batch or last ship, and the one before it) to the end of
   docs/SHIPLOG.md, oldest first, with "Previous: " dropped; SHIPLOG is append-only and is read by grep on the batch id;
2. writes RESUME.md's "**Batch state: <head>**" line from the head of the first State entry (the State is the
   authority; RESUME's line is never hand-edited);
3. sets the handoff's "Last updated:" date when --date YYYY-MM-DD is given;
then runs the state checks and exits 1 when any fails. It does not commit: the lead commits and pushes the private clone.

State entry form (resume.py and doc_lint read it): "- **<batch> OPEN <date>** (...)" or "- **<batch> SHIPPED <date>**
(...)"; older entries may start "- **Previous: ...**".
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(WS, 'tools'))
import doc_lint  # noqa: E402
import docs_path  # noqa: E402

KEEP = 2
SHIPLOG_HEAD = ('# Step2Haki ship log (append only)\n\n'
                'State entries moved out of STEP2HAKI_HANDOFF.md by tools/spine/docstate.py sync, oldest first. Read by grep on\n'
                'the batch id (grep -n "^- \\*\\*s172 " docs/SHIPLOG.md), never whole. Entries older than s160 are in\n'
                'docs/archive_public/STATE_ARCHIVE.md. Open follow-ups live in docs/OPEN_WORK.md.\n')


def sync(docs, date=None):
    hp, rp, sp = (os.path.join(docs, n) for n in ('STEP2HAKI_HANDOFF.md', 'RESUME.md', 'SHIPLOG.md'))
    hand = open(hp, encoding='utf-8').read()
    ents = doc_lint.state_entries(hand)
    if not ents:
        print('docstate: the handoff State has no entry'); return 1
    moved = ents[KEEP:]
    if moved:
        for _, body in moved:
            if hand.count(body) != 1:
                print('docstate: a State entry is not unique in the handoff; move it by hand: ' + body[:60]); return 1
            hand = hand.replace(body, '', 1)
        hand = re.sub(r'\n{3,}', '\n\n', hand)
        log = open(sp, encoding='utf-8').read() if os.path.exists(sp) else SHIPLOG_HEAD
        for _, body in reversed(moved):
            log = log.rstrip('\n') + '\n\n' + re.sub(r'^- \*\*Previous: ', '- **', body) + '\n'
        open(sp, 'w', encoding='utf-8').write(log)
    if date:
        hand = re.sub(r'^Last updated: \d{4}-\d{2}-\d{2}', 'Last updated: ' + date, hand, count=1, flags=re.M)
    open(hp, 'w', encoding='utf-8').write(hand)
    res = open(rp, encoding='utf-8').read()
    line = '**Batch state: %s**' % ents[0][0]
    if doc_lint.RESUME_LINE.search(res):
        res = doc_lint.RESUME_LINE.sub(lambda m: line, res, count=1)
    else:
        print('docstate: RESUME.md has no "**Batch state: ...**" line; add one under the title and rerun'); return 1
    open(rp, 'w', encoding='utf-8').write(res)
    print('docstate: State %d entries (%d moved to SHIPLOG.md); RESUME batch line "%s"' % (len(ents) - len(moved), len(moved), ents[0][0]))
    return check(docs)


def check(docs):
    errs = doc_lint.state_errors(docs, WS)
    for e in errs:
        print('  STATE-LINT', e)
    print('STATE-LINT %s' % ('FAIL (%d)' % len(errs) if errs else 'PASS'))
    return 1 if errs else 0


def copies(docs):
    print('After a ship, the same bytes go to three places (runbook section 9):')
    for name, dests in (('STEP2HAKI_HANDOFF.md', ['project claude/STEP2HAKI_HANDOFF.md', 'Mac ~/Documents/Step2Haki/STEP2HAKI_HANDOFF.md']),
                        ('RESUME.md', ['project claude/RESUME.md']), ('PLAN_TEMPLATE.md', ['project claude/PLAN_TEMPLATE.md (only when it changed)'])):
        p = os.path.join(docs, name)
        print('  %s (%d bytes) -> %s' % (p, os.path.getsize(p) if os.path.exists(p) else 0, '; '.join(dests)))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    d = docs_path.docs_dir()
    cmd = a[0] if a else ''
    if cmd == 'sync':
        sys.exit(sync(d, a[a.index('--date') + 1] if '--date' in a else None))
    if cmd == 'check':
        sys.exit(check(d))
    if cmd == 'copies':
        sys.exit(copies(d))
    print(__doc__); sys.exit(2)
