"""Welcome card pilot. Builds the live page with this branch's site/ sources (tools/site_build.py) and adds one
pilot-only button that opens the card again (the card shows by itself once per browser).
Usage: python3 make_pilot.py <live index.html> <out dir>"""
import os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
page = os.path.join(out, 'index.html')
subprocess.run([sys.executable, os.path.join(WS, 'tools', 'site_build.py'), src, '--out', page], check=True)
s = open(page, encoding='utf-8').read()
tail = ('<style id="tour-pilot-css">#tourpilot{position:fixed;z-index:9000;left:50%;top:6px;transform:translateX(-50%);'
        'padding:7px 14px;border-radius:999px;border:0;background:#15151B;color:#fff;font:600 12.5px/1 system-ui,sans-serif;'
        'cursor:pointer;opacity:.86}</style>'
        '<script id="tour-pilot-js">(function(){var b=document.createElement("button");b.id="tourpilot";b.type="button";'
        'b.textContent="Pilot: show the welcome card";b.addEventListener("click",function(){AX.emit("tour:open");});'
        'document.body.appendChild(b);})();</script>')
j = s.rindex('</body>')
s = s[:j] + tail + s[j:]
s = re.sub(r'<title>[^<]*</title>', '<title>Step2Haki Welcome Card Pilot</title>', s, count=1)
open(page, 'w', encoding='utf-8').write(s)
site = os.path.join(os.path.dirname(WS), 'discriminator-briefs-site', 'version.json')
if os.path.exists(site):
    shutil.copy(site, os.path.join(out, 'version.json'))
print('pilot', page, len(s))
