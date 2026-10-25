#!/usr/bin/env python3
"""Offline tests for the s152-close tools: batch.py (pure parts), mentions.py, build_lanes.py placeholders, author_lib."""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WS, 'tools'))
ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


import batch as B  # noqa: E402
import mentions as M  # noqa: E402
import author_lib as A  # noqa: E402

expect('author_lib WS is the workspace', A.WS == WS)
expect('changelog: a shipped entry is found', B.changelog_has('s151'))
expect('changelog: a missing entry is not', not B.changelog_has('s999'))
by, lead, w = B.spend('s151')
expect('spend: reads both ledgers and the wave', isinstance(by, dict) and isinstance(lead, list) and 'id' in w)

H = '''<div><h4>T</h4><table><tr><td>Venous hum</td><td>above the right clavicle</td></tr>
<tr><td>Still murmur</td><td>lower left sternal border</td></tr></table><p>A venous hum fades with head flexion.</p>
<h5 class="authored-hdr">Practice</h5><ol class="bank"><li data-type="dx" data-d1="Patent ductus arteriosus" data-d2="Still murmur"
data-item-id="q_abc" data-key-why="A hum below the clavicle that goes with rotation is a venous hum." data-d1-why="x"
data-d2-why="y">4 yo, hum below the clavicle &rarr; <b>Venous hum</b> &rarr; reassure</li></ol></div>'''
g = M.sheet(H, 2)
expect('mentions: the venous hum group holds body and bank lines', 'venous hum' in g and len(g['venous hum']) == 4)
expect('mentions: a subject named once is left out', 'patent ductus arteriosus' not in g)
expect('mentions: a parenthetical other name is dropped', M.norm('Conversion disorder (FND)') == 'conversion disorder')

t = open(os.path.join(HERE, 'BUILD_CONTRACT.md'), encoding='utf-8').read()
import re  # noqa: E402
keys = set(re.findall(r'\{([a-z_]+)\}', t))
expect('contract: only known placeholders', keys <= {'batch', 'bid', 'title', 'entry', 'folder', 'budget', 'live',
                                                     'live_txt', 'model', 'golden', 'spine_spec'})
import build_lanes as BL  # noqa: E402
p = BL.prompt({'plan_step': 's999', 'budget': 90}, {'id': 'x'}, '/w/repair/migration/x/spine')
expect('build prompt: gate lines first', p.splitlines()[:4] == ['Role: brief-build', 'Plan step: s999',
                                                                 'Lane: /w/repair/migration/x/spine', 'Budget: 90'])
roles = json.load(open(os.path.join(WS, 'tools', 'hooks', 'roles.json')))['roles']
expect('roles: brief-build is opus, 90 calls, lean-builder', roles.get('brief-build') == {
    'model': 'opus', 'budget': 90, 'agent': 'lean-builder'})
print('test_batch_tools: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
