#!/usr/bin/env python3
"""s148f (site layer, Jonathan 2026-10-19/20): writes repair/s148f/*.json from the live page.

  40_site_r2.json   src/site_r2.css as <style id="ax-s148f"> and src/site_r2.js as <script id="ax-s148f-js">, appended at
                    the end of the body so they follow every earlier layer (as s148b).
  30_targeted.json  workup 5a zone "By presentation" renamed "Targeted tests" (digest 2026-10-19), one brief-scoped
                    replace per brief; nothing else in any brief changes.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import read_page, briefs  # noqa: E402

s = read_page(os.path.join(WS, 'index.html'))
assert s.count('</body>') == 1 and 'id="ax-s148f"' not in s
OLD, NEW = '<p class="w5z">By presentation</p>', '<p class="w5z">Targeted tests</p>'
E = []
for b in briefs(s):
    n = s[b.start:b.end].count(OLD)
    if n == 1:
        E.append({'op': 'replace', 'brief': b.id, 'find': OLD, 'with': NEW,
                  'note': 's148f: workup zone 2 renamed Targeted tests (digest 2026-10-19)'})
    elif n > 1:                     # two workups in one brief: lengthen each anchor backwards until it is unique
        body, at = s[b.start:b.end], 0
        for _ in range(n):
            i = body.find(OLD, at); k = 40
            while body.count(body[i - k:i + len(OLD)]) > 1:
                k += 40
            E.append({'op': 'replace', 'brief': b.id, 'find': body[i - k:i + len(OLD)], 'with': body[i - k:i] + NEW,
                      'note': 's148f: workup zone 2 renamed Targeted tests (digest 2026-10-19)'})
            at = i + len(OLD)
assert len(E) == s.count(OLD), (len(E), s.count(OLD))
json.dump({'edits': E}, open(os.path.join(HERE, '30_targeted.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

css = open(os.path.join(HERE, 'src', 'site_r2.css'), encoding='utf-8').read().strip()
js = open(os.path.join(HERE, 'src', 'site_r2.js'), encoding='utf-8').read().strip()
assert '</script' not in js and '</style' not in css
block = '<style id="ax-s148f">\n%s\n</style>\n<script id="ax-s148f-js">\n%s\n</script>\n</body>' % (css, js)
G = [{'op': 'replace_global', 'find': '</body>', 'with': block,
      'note': 's148f: question tiles, hover motion, linked briefs, muted tints, one shading rule, carried phone fixes (site layer)'}]
json.dump({'edits': G}, open(os.path.join(HERE, '40_site_r2.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('%d zone renames; 1 layer edit (%d bytes CSS, %d bytes JS)' % (len(E), len(css), len(js)))
