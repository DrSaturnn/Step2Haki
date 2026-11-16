"""Phone redesign pilot (s166). Builds the live page with this branch's site/ sources (tools/site_build.py), then adds the
pilot-only options (pilot_head.js in the head; pilot.css and pilot.js before </body>): Layout, Bars while reading,
Side rail, Differential, under Settings. The site/ changes are the batch itself; the pilot files are not shipped.
Usage: python3 make_pilot.py <live index.html> <out.html>"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
src, out = sys.argv[1], sys.argv[2]
subprocess.run([sys.executable, os.path.join(WS, 'tools', 'site_build.py'), src, '--out', out], check=True)
s = open(out, encoding='utf-8').read()
rd = lambda n: open(os.path.join(HERE, n), encoding='utf-8').read()
head = '<script id="ph-pilot-head">' + rd('pilot_head.js') + '</script>'
i = s.index('<head>') + len('<head>')
s = s[:i] + head + s[i:]
tail = '<style id="ph-pilot-css">' + rd('pilot.css') + '</style><script id="ph-pilot-js">' + rd('pilot.js') + '</script>'
j = s.rindex('</body>')
s = s[:j] + tail + s[j:]
import re
s = re.sub(r'<title>[^<]*</title>', '<title>Step2Haki Phone Pilot</title>', s, count=1)
open(out, 'w', encoding='utf-8').write(s)
print('pilot', out, len(s))
