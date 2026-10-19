#!/usr/bin/env python3
"""s148b offline test for the legib_audit change: text inside a closed <details> is skipped, its summary and open
panels are still measured. Runs legib_audit on a tiny page and checks which texts it reports."""
import json, os, subprocess, sys, tempfile
WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PAGE = """<!doctype html><html><head><style>body{font:16px sans-serif;background:#fff;color:#111}</style></head><body>
<div class="brief" id="tb"><p>Visible line</p>
<details><summary>Closed summary</summary><div><span class="k">Hidden text</span></div></details>
<details open><summary>Open summary</summary><div><span class="k">Open panel text</span>
<details><summary>Inner closed</summary><p>Inner hidden</p></details></div></details></div></body></html>"""
d = tempfile.mkdtemp()
page = os.path.join(d, 'p.html')
open(page, 'w').write(PAGE)
subprocess.run([sys.executable, os.path.join(WS, 'tools', 'legib_audit.py'), page, '--briefs', 'tb', '--views', 'desk',
                '--modes', 'sculpted', '--out', d], check=True, capture_output=True)
texts = {r['text'] for r in json.load(open(os.path.join(d, 'run.json')))}
want = {'Visible line', 'Closed summary', 'Open summary', 'Open panel text', 'Inner closed'}
bad = {'Hidden text', 'Inner hidden'}
ok = want <= texts and not (bad & texts)
print('test_legib_details:', 'PASS' if ok else 'FAIL', sorted(texts))
sys.exit(0 if ok else 1)
