#!/usr/bin/env python3
"""test_move_brief.py (s146c): apply_edits' move_brief moves a brief byte for byte, keeps every other brief and the page
chrome unchanged, and refuses an unknown brief or a move after itself.  python3 tools/test_move_brief.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import apply_edits as A
from pagelib import read_page, briefs
page = read_page(os.path.join(os.path.dirname(HERE), 'index.html'))
bl = briefs(page); ids = [b.id for b in bl]; old = {b.id: page[b.start:b.end] for b in bl}
ok = bad = 0
def check(name, cond):
    global ok, bad
    ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
    print(('ok  ' if cond else 'BAD ') + name)
x, y = ids[5], ids[40]
new, log = A.apply(page, {'edits': [{'op': 'move_brief', 'brief': x, 'after': y}]})
nb = briefs(new); nids = [b.id for b in nb]
check('the brief now follows its target', nids.index(x) == nids.index(y) + 1)
check('every brief is byte-identical', all(new[b.start:b.end] == old[b.id] for b in nb) and len(nb) == len(bl))
check('the order of the others is unchanged', [i for i in nids if i != x] == [i for i in ids if i != x])
check('nothing else changed (length within the moved whitespace)', abs(len(new) - len(page)) <= 4)
for spec, name in (({'op': 'move_brief', 'brief': x, 'after': x}, 'a move after itself is refused'),
                   ({'op': 'move_brief', 'brief': 'no-such-brief', 'after': y}, 'an unknown brief is refused')):
    try:
        A.apply(page, {'edits': [spec]}); check(name, False)
    except A.EditError:
        check(name, True)
print('test_move_brief: %d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
