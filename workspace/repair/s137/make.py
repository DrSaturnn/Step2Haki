"""make: build repair/s137/50_phase2.json from src/phase2.css and src/phase2.js (site layout Phase 2, display layer).

  python3 repair/s137/make.py
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(HERE, 'src', 'phase2.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'src', 'phase2.js'), encoding='utf-8').read()
note = 's137 site layout Phase 2, display layer (claude/pending/S137.md; Jonathan 2026-10-14 "Display layer")'
edits = [
    {'op': 'replace_global', 'find': "var a = b.querySelector('.bb-rl a.cur');", 'with': "var a = b.querySelector('.bb-rl a.cur') || (window.axRailOf && window.axRailOf(b) ? window.axRailOf(b).querySelector('.bb-rl a.cur') : null);   /* s137: the rail may sit in the sidebar */", 'note': note + ': the toolbar finds the current section in a nested rail'},
    {'op': 'replace_global', 'find': '</head>', 'with': '<style id="ax-s137">\n' + css + '</style>\n</head>', 'note': note + ': the style block'},
    {'op': 'replace_global', 'find': '</script>\n</body>', 'with': '</script>\n<script>\n' + js + '</script>\n</body>', 'note': note + ': the script block'},
]
json.dump({'edits': edits}, open(os.path.join(HERE, '50_phase2.json'), 'w'), indent=1)
print('50_phase2.json: %d edits (style %d bytes, script %d bytes)' % (len(edits), len(css), len(js)))
