#!/usr/bin/env python3
"""s148g pilot (runbook section 8; SITE_S148G.md item 9): the live page plus the s148g batch, plus pilot-only content that
never ships in s148g: drafted per-choice reasons for the five sample banks (pilot_reasons.json; reviewed reasons ship in
s148h), First step pairings for psychosis-duration and toxidrome (s148h), and a switch bar (linked brief panel anchored
to its link, or the old right-hand panel, to compare).

  python3 repair/pilots/s148g/build_pilot.py <out.html>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, os.path.join(WS, 'repair', 's148g'))
import apply_edits  # noqa: E402
from pagelib import read_page, write_page, briefs  # noqa: E402
import w5split  # noqa: E402

out = sys.argv[1]
subprocess.check_call([sys.executable, os.path.join(WS, 'repair', 's148g', 'gen_s148g.py')])
subprocess.check_call([sys.executable, os.path.join(WS, 'repair', 'build.py'), 's148g', '--out', out])
s = read_page(out)

R = json.load(open(os.path.join(HERE, 'pilot_reasons.json'), encoding='utf-8'))
E = []
for iid, (k, d1, d2) in ((k, v) for k, v in R.items() if not k.startswith('_')):
    for attr, val in (('data-key-why', k), ('data-d1-why', d1), ('data-d2-why', d2)):
        E.append({'op': 'set_attr', 'target': iid, 'attr': attr, 'value': val})
B = {b.id: b for b in briefs(s)}
for bid, bands in (('psychosis-duration', [(0, [1, 1, 2, 3])]), ('toxidrome', [(1, [1, 3]), (0, [1, 2])])):
    for band, pair in bands:
        h = s[B[bid].start:B[bid].end]
        old, new = w5split.split(h, band, pair)
        E.append({'op': 'replace', 'brief': bid, 'find': old, 'with': new})
        s, _ = apply_edits.apply(s, {'edits': [E.pop()]})
        B = {b.id: b for b in briefs(s)}
s, log = apply_edits.apply(s, {'edits': E})
print('pilot: %d reason attributes on %d items; pairings for psychosis-duration and toxidrome' % (len(E), len(E) // 3))

bar = '''<div id="qx-pilot" style="position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:90;display:flex;align-items:center;gap:8px;padding:6px 6px 6px 14px;border-radius:999px;background:var(--glass-2);box-shadow:var(--glass-edge-2);-webkit-backdrop-filter:blur(30px);backdrop-filter:blur(30px);font:650 13px/1 var(--sans);color:var(--ink);white-space:nowrap">
<span>s148g pilot</span><button type="button" id="qx-rhpb" aria-pressed="false" style="all:unset;cursor:pointer;padding:8px 12px;border-radius:999px;background:var(--principle-bg);color:var(--principle)">Linked brief: anchored panel</button></div>
<script>(function(){var b=document.getElementById('qx-rhpb');b.addEventListener('click',function(){var on=document.body.classList.toggle('qx-rhp');b.setAttribute('aria-pressed',on?'true':'false');b.textContent='Linked brief: '+(on?'right-hand panel (old)':'anchored panel');});})();</script>
</body>'''
assert s.count('</body>') == 1
s = s.replace('</body>', bar)
s = s.replace('<title>Step2Haki &ndash; Clinical Board Briefs</title>', '<title>Step2Haki s148g Pilot</title>', 1)
write_page(out, s)
print('pilot', out, len(s))
