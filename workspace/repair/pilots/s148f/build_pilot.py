#!/usr/bin/env python3
"""s148f pilot (runbook section 8): the live page plus the s148f batch, plus a pilot-only switch for the muted tints
(proposal, Jonathan judges). The switch never ships: ship builds come from repair/s148f/*.json only.

  python3 repair/pilots/s148f/build_pilot.py <out.html>
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
out = sys.argv[1]
subprocess.check_call([sys.executable, os.path.join(WS, 'repair', 's148f', 'gen_site_r2.py')])
subprocess.check_call([sys.executable, os.path.join(WS, 'repair', 'build.py'), 's148f', '--out', out])
s = open(out, encoding='utf-8').read()
panel = '''<div id="qx-pilot" style="position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:90;display:flex;align-items:center;gap:10px;padding:6px 8px 6px 14px;border-radius:999px;background:var(--glass-2);box-shadow:var(--glass-edge-2);-webkit-backdrop-filter:blur(30px);backdrop-filter:blur(30px);font:650 13px/1 var(--sans);color:var(--ink)">
<span>s148f pilot</span><button type="button" id="qx-tint" aria-pressed="true" style="all:unset;cursor:pointer;padding:8px 12px;border-radius:999px;background:var(--confirm-bg);color:var(--confirm)">Muted tints: on</button><button type="button" id="qx-grow" aria-pressed="false" style="all:unset;cursor:pointer;padding:8px 12px;border-radius:999px;background:var(--principle-bg);color:var(--principle)">Stack: answer space kept</button></div>
<script>(function(){var b=document.getElementById('qx-tint');b.addEventListener('click',function(){var off=document.body.classList.toggle('qx-notint');b.setAttribute('aria-pressed',off?'false':'true');b.textContent='Muted tints: '+(off?'off':'on');});var g=document.getElementById('qx-grow');g.addEventListener('click',function(){var on=document.body.classList.toggle('qx-grow');g.setAttribute('aria-pressed',on?'true':'false');g.textContent=on?'Stack: card grows on answer':'Stack: answer space kept';});})();</script>
</body>'''
assert s.count('</body>') == 1
s = s.replace('</body>', panel)
s = s.replace('<title>Step2Haki &ndash; Clinical Board Briefs</title>', '<title>Step2Haki s148f Pilot</title>', 1)
open(out, 'w', encoding='utf-8').write(s)
print('pilot', out, len(s))
