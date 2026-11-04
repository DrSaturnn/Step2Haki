#!/usr/bin/env python3
"""s161c (site layer, Jonathan 2026-11-03/04): writes repair/s161c/40_presentations.json from the live page.
Presentations becomes its own section: each of its briefs leaves its system and is listed once, on the page in a new
Presentations section after "How to Use This" and in the sidebar's Presentations group, under a sub-header per system
in page order. Pilot: repair/pilots/presentations/make_pilot.py (this script runs it for the sidebar, styles and script,
and moves the briefs with move_brief after_anchor, so nothing in a brief changes)."""
import json, os, re, runpy, sys, tempfile
WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import read_page, briefs
live = read_page(os.path.join(WS, 'index.html'))
pilot = os.path.join(WS, 'repair', 'pilots', 'presentations', 'make_pilot.py')
out = os.path.join(tempfile.mkdtemp(), 'pilot.html')
argv = sys.argv; sys.argv = [pilot, os.path.join(WS, 'index.html'), out]; runpy.run_path(pilot); sys.argv = argv
pp = read_page(out)
E = []
# 1. the section header and its sub-headers, before the MSK section (the live page carries the MSK comment twice)
anchor = '<!-- =================== MSK =================== -->\n\n<!-- =================== MSK =================== -->'
assert live.count(anchor) == 1
a = pp.index('<!-- =================== PRESENTATIONS'); z = pp.index(anchor[:56], a)
section = pp[a:z]
heads = re.findall(r'<div class="psub" id="pres-[\w-]+">.*?</div>', section)
skeleton = section[:section.index('<div class="psub"')] + '\n\n'.join(heads) + '\n\n'
E.append({'op': 'replace_global', 'find': anchor, 'with': skeleton + anchor, 'note': 'Presentations section and its system sub-headers'})
# 2. each brief, in reverse order within its sub-header, just after the sub-header
groups = []
for m in re.finditer(r'(<div class="psub" id="pres-[\w-]+">.*?</div>)|<div class="brief[^"]*" id="([\w-]+)"', section):
    if m.group(1): groups.append((m.group(1), []))
    else: groups[-1][1].append(m.group(2))
for head, ids in groups:
    for i in reversed(ids):
        E.append({'op': 'move_brief', 'brief': i, 'after_anchor': head, 'note': 'to Presentations'})
# 3. the sidebar, the section tab, the sub-header style and script, as the pilot has them
def block(s):
    i = s.index('<div id="navlinks">'); d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group(0) == '<div' else -1
        if d == 0: return s[i:i + m.end()]
E.append({'op': 'replace_global', 'find': block(live), 'with': block(pp), 'note': 'sidebar: Presentations once, under system sub-labels; counts'})
E.append({'op': 'replace_global', 'find': "var SHORT={msk:'MSK',", 'with': "var SHORT={presentations:'CC',msk:'MSK',"})
st = pp[pp.index('<style id="ax-pres">'):pp.index('</style>', pp.index('<style id="ax-pres">')) + 9]
E.append({'op': 'replace_global', 'find': '</head>', 'with': st + '\n</head>'})
sc0 = pp.index('/* s161c Presentations sub-headers'); sc = pp[pp.rindex('<script>', 0, sc0):pp.index('</script>', sc0) + 9]
E.append({'op': 'replace_global', 'find': '</body>', 'with': sc + '\n</body>'})
json.dump({'edits': E}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '40_presentations.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(E), 'edits;', sum(len(i) for _, i in groups), 'briefs moved; pilot page', out)
