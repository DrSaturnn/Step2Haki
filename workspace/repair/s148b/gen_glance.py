#!/usr/bin/env python3
"""s148b (site layer, Jonathan 2026-10-18): writes repair/s148b/40_glance_body.json from the live page.
The brief body in the Lithium Glance mockup's type and tiles (claude/pending/SITE_BODY_GLANCE.md, Decided A to D, work
plan items 1 and 4): src/glance_body.css as <style id="ax-s148b"> and src/onset.js as <script id="ax-s148b-on">, both
appended at the end of the body so they follow every earlier layer. No brief text or markup changes."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import read_page
s = read_page(os.path.join(WS, 'index.html'))
assert s.count('</body>') == 1 and 'id="ax-s148b"' not in s
css = open(os.path.join(HERE, 'src', 'glance_body.css'), encoding='utf-8').read().strip()
js = open(os.path.join(HERE, 'src', 'onset.js'), encoding='utf-8').read().strip()
block = '<style id="ax-s148b">\n%s\n</style>\n<script id="ax-s148b-on">\n%s\n</script>\n</body>' % (css, js)
E = [{'op': 'replace_global', 'find': '</body>', 'with': block,
      'note': 's148b: brief body restyle to the Lithium Glance mockup and onset timeline placement (site layer)'}]
json.dump({'edits': E}, open(os.path.join(HERE, '40_glance_body.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(E), 'edit;', len(css), 'bytes CSS,', len(js), 'bytes JS')
