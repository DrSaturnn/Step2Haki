#!/usr/bin/env python3
"""s148h build check: every brief outside the batch is byte-identical to the live page; a batch brief differs only by the
three reason attributes, plus, for a brief in data/pairs.json, the First step regrouping (same text runs) and the two
prose fixes of gen_s148h.PROSE.

  python3 repair/s148h/identity_check.py <built index.html>
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, HERE)
from pagelib import read_page, briefs  # noqa: E402
import gen_s148h as G  # noqa: E402

live, new = read_page(os.path.join(WS, 'index.html')), read_page(sys.argv[1])
L = {b.id: live[b.start:b.end] for b in briefs(live)}
N = {b.id: new[b.start:b.end] for b in briefs(new)}
pairs = json.load(open(os.path.join(HERE, 'data', 'pairs.json')))
assert set(L) == set(N), 'brief set changed'
why = re.compile(r' data-(?:key|d1|d2)-why="[^"]*"')
ar = '<span class="w5ar" aria-hidden="true">&rarr;</span>'
runs = lambda x: sorted(re.findall(r'>([^<]+)<', x.replace(ar, '')))  # noqa: E731
same = attr_only = split = 0
for bid in L:
    a, b = L[bid], N[bid]
    if a == b:
        assert bid not in G.ORDER, '%s unchanged' % bid
        same += 1
        continue
    assert bid in G.ORDER, '%s changed but is not in the batch' % bid
    b0 = why.sub('', b)
    for pb, old, rep in G.PROSE:
        if pb == bid:
            b0 = b0.replace(rep, old)
    if b0 == a:
        attr_only += 1
        assert bid not in pairs, '%s: pairing not applied' % bid
        continue
    assert bid in pairs, '%s differs beyond the reasons' % bid
    assert runs(a) == runs(b0), '%s: text runs differ after the split' % bid
    split += 1
print('identity_check: %d briefs byte-identical, %d differ by the reason attributes only, %d also by the First step '
      'split (text runs equal)%s' % (same, attr_only, split, ', prose fixes undone before comparing' if G.PROSE else ''))
