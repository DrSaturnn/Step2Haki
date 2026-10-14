"""make: build repair/s136/10_glance.json from src/glance.css, src/glance.js and tools/glance_accent.py.

  python3 repair/s136/make.py [page.html]     (default: the working page, workspace/index.html)

Run it again on the page after main (with s135) is merged in: the accent rewrites anchor on whole rules, so a rule
s135 changed gets a fresh anchor instead of a stale one.
"""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
page = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WS, 'index.html')
tmp = os.path.join(tempfile.mkdtemp(), 'acc.json')
subprocess.run([sys.executable, os.path.join(WS, 'tools', 'glance_accent.py'), page, tmp], check=True)
acc = json.load(open(tmp))
css = open(os.path.join(HERE, 'src', 'glance.css')).read().replace('/*@TOKENS@*/', acc['tokens_css'])
js = open(os.path.join(HERE, 'src', 'glance.js')).read()
note = 's136 site layout Phase 1 (claude/pending/S136.md; Jonathan 2026-10-13 and 14)'
edits = acc['edits'] + [
    {'op': 'replace_global', 'find': '</head>', 'with': '<style id="ax-s136">\n' + css + '</style>\n</head>', 'note': note + ': the glance style block'},
    {'op': 'replace_global', 'find': '</script>\n</body>', 'with': '</script>\n<script>\n' + js + '</script>\n</body>', 'note': note + ': the glance script block'},
]
json.dump({'edits': edits}, open(os.path.join(HERE, '10_glance.json'), 'w'), indent=1)
print('10_glance.json: %d edits (%d accent rule rewrites, style %d bytes, script %d bytes)' % (len(edits), len(acc['edits']), len(css), len(js)))
