#!/usr/bin/env python3
"""Offline tests for the s148f tool changes (runbook section 3, G-DIFF):
  1. outline_render.w5a renders an outline's "By presentation" zone as "Targeted tests";
  2. gen_site_r2.py renames every zone label on the live page and nothing else (one brief-scoped replace per label);
  3. lint.py's prose check (the cases live in tools/spine/test_lint.py; run here too).
  python3 repair/s148f/test_s148f.py
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools', 'spine')); sys.path.insert(0, os.path.join(WS, 'tools'))
import outline_render as O  # noqa: E402
from pagelib import read_page  # noqa: E402
ok = bad = 0
def expect(n, c):
    global ok, bad
    if c: ok += 1
    else: bad += 1; print('FAIL', n)
h = O.w5a({'zones': [['First step', [['Any clue', ['CBC'], []]]], ['By presentation', [['Suspected', ['ECG'], []]]]]}, lambda x: x)
expect('renderer: old zone name renders as Targeted tests', '<p class="w5z">Targeted tests</p>' in h and 'By presentation' not in h)
h2 = O.w5a({'zones': [['Next step', [['c', ['MRI'], []]]]]}, lambda x: x)
expect('renderer: other zone names unchanged', '<p class="w5z">Next step</p>' in h2)
spec = json.load(open(os.path.join(HERE, '30_targeted.json')))['edits']
live = read_page(os.path.join(WS, 'index.html'))
expect('rename: one op per zone label on the live page', len(spec) == live.count('<p class="w5z">By presentation</p>'))
expect('rename: each op only swaps the label', all(e['op'] == 'replace' and e['find'].replace('By presentation', 'Targeted tests') == e['with'] for e in spec))
r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'spine', 'test_lint.py')], capture_output=True, text=True)
expect('lint tests pass', r.returncode == 0)
print('test_s148f: %d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
