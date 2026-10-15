"""conv.py: build repair/s143/40_glance_nav.json from src/axnav.css and src/axnav.js.

  python3 repair/s143/src/conv.py
The old sidebar scripts (s137 nest, s141 movement, the phone index) keep running on the hidden list; four guards stop
them scrolling the list or the page now that the s143 component (window.AXN) owns both.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(HERE, 'axnav.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'axnav.js'), encoding='utf-8').read()
edits = [
    {'op': 'replace_global', 'find': "    if(!WIDE.matches) return;\n    var rl = list.querySelector('.bb-rail.ax-nr .bb-rl'); if(!rl) return;",
     'with': "    if(!WIDE.matches || window.AXN) return;   // s143: the axnav component draws the rail\n    var rl = list.querySelector('.bb-rail.ax-nr .bb-rl'); if(!rl) return;"},
    {'op': 'replace_global', 'find': '    if(box){\n      var br = box.getBoundingClientRect()',
     'with': '    if(box && !window.AXN){   // s143: the axnav component keeps its own list in view\n      var br = box.getBoundingClientRect()'},
    {'op': 'replace_global', 'find': "if(sc && act && act.style.display!=='none' && !sxQuery()){",
     'with': "if(sc && act && act.style.display!=='none' && !sxQuery() && !window.AXN){"},
    {'op': 'replace_global', 'find': '  function seat(){\n    if(moved) return;',
     'with': '  function seat(){\n    if(moved || window.AXN) return;   // s143: axnav seats the landing'},
    {'op': 'replace_global', 'find': '    applyShelf(shelf);   /* re-pins for the new hash, un-pins the old one */\n    gotoHash(true);',
     'with': '    applyShelf(shelf);   /* re-pins for the new hash, un-pins the old one */\n    gotoHash(!window.AXN);   // s143: an instant jump; axnav then seats the target while lazy briefs above it render'},
    {'op': 'replace_global', 'find': '</body>', 'with': '<style>\n' + css + '</style>\n<script>\n' + js + '</script>\n</body>'},
]
out = os.path.join(os.path.dirname(HERE), '40_glance_nav.json')
json.dump({'edits': edits}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', os.path.relpath(out), len(edits), 'edits')
