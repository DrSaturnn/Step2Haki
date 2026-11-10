#!/usr/bin/env python3
"""Tests for the s172c doc_lint checks: (a) stale paths in rule documents, (b) RESUME batch line against the handoff
State, (c) the State cap, (d) plan files. Run: python3 tools/spine/test_doc_lint.py"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_lint

bad = 0


def ok(cond, name):
    global bad
    print(('ok  ' if cond else 'BAD ') + name)
    bad += not cond


def tree(files):
    d = tempfile.mkdtemp()
    for rel, text in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(text)
    return d


HAND = '''# Handoff

## State (rewrite after every step)

- **s200 OPEN 2026-11-10** (step S3).
  second line of the entry.
- **Previous: s199 SHIPPED 2026-11-09** (commit abc).

Older entries: docs/SHIPLOG.md.

## Next
'''
ws = tree({'tools/gate.py': '', 'repair/efficiency/TEXTBOOK_STYLE.md': ''})

# (a) paths
priv = tree({'docs/BATCH_RUNBOOK.md': 'Read claude/STANDING_DIRECTIONS.md and repair/efficiency/DECISIONS_DIGEST.md.\n'
                                      'Then tools/gate.py, repair/efficiency/TEXTBOOK_STYLE.md, tools/nope.py,\n'
                                      'repair/<batch>/ui_allow.json, repair/sNN/x.json, claude/pending/S1.md, claude/RESUME.md.\n',
             'docs/STANDING_DIRECTIONS.md': 'ok\n', 'docs/DECISIONS_DIGEST.md': '', 'claude/SPINE_SPEC.md': ''})
e = doc_lint.path_errors(os.path.join(priv, 'docs'), ws, ['BATCH_RUNBOOK.md', 'STANDING_DIRECTIONS.md'])
ok(any('claude/STANDING_DIRECTIONS.md' in x for x in e), '(a) claude/<doc> for a document in docs/ fails')
ok(any('repair/efficiency/DECISIONS_DIGEST.md' in x for x in e), '(a) repair/efficiency/<doc> for a document in docs/ fails')
ok(any('tools/nope.py' in x for x in e), '(a) a tool path that does not exist fails')
ok(len(e) == 3, '(a) existing paths, placeholders, claude/pending/ and the project mirrors pass (%d errors)' % len(e))

# (b) RESUME batch line
d = tree({'docs/STEP2HAKI_HANDOFF.md': HAND, 'docs/RESUME.md': '# r\n\n**Batch state: s199 SHIPPED 2026-11-09** x\n'})
e = doc_lint.state_errors(os.path.join(d, 'docs'), ws)
ok(any('RESUME' in x and 's200 OPEN 2026-11-10' in x for x in e), '(b) RESUME batch line that disagrees with the State fails')
d = tree({'docs/STEP2HAKI_HANDOFF.md': HAND, 'docs/SHIPLOG.md': '', 'docs/RESUME.md': '# r\n\n**Batch state: s200 OPEN 2026-11-10** x\n'})
ok(doc_lint.state_errors(os.path.join(d, 'docs'), ws) == [], '(b) matching line passes')
d = tree({'docs/STEP2HAKI_HANDOFF.md': HAND, 'docs/RESUME.md': '# r\nno line\n'})
ok(any('no "**Batch state:' in x for x in doc_lint.state_errors(os.path.join(d, 'docs'), ws)), '(b) RESUME with no batch line fails')

# (c) State cap
many = HAND.replace('\nOlder entries', '- **Previous: s198 SHIPPED 2026-11-08** (x).\n- **Previous: s197 SHIPPED 2026-11-07** (x).\n\nOlder entries')
d = tree({'docs/STEP2HAKI_HANDOFF.md': many, 'docs/RESUME.md': '**Batch state: s200 OPEN 2026-11-10**\n'})
ok(any('4 entries' in x for x in doc_lint.state_errors(os.path.join(d, 'docs'), ws)), '(c) a State with four entries fails')
ok([h for h, _ in doc_lint.state_entries(HAND)] == ['s200 OPEN 2026-11-10', 's199 SHIPPED 2026-11-09'], '(c) entries parsed, "Previous:" dropped')

# (d) plan files
PLAN = '''# s200: x

## Open calls
1. Which one? A or B. Recommendation: A, because it is smaller.
2. Width? 300 or 320.

## Evidence
Method line: page abc.
### Sidebar overlap  TESTED (measure.js)
- Reproduction at 1280.
### Rail
- Width is 320. TESTED (rail.js)
- The saving is large.
- Probably fine. ASSUMED

## Steps
'''
p = os.path.join(tree({'PLAN.md': PLAN}), 'PLAN.md')
e = doc_lint.plan_errors(p)
ok(len(e) == 2 and any('open call 2' in x for x in e) and any('The saving is large' in x for x in e),
   '(d) an open call with no recommendation and an unmarked Evidence line fail; marked lines and headings pass (%d)' % len(e))

print('%d failures' % bad)
sys.exit(1 if bad else 0)
