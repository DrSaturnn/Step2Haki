#!/usr/bin/env python3
"""s161b (site layer, Jonathan 2026-11-03): writes repair/s161b/40_nav_home.json from the live page.
One home per brief in the sidebar (the step rail always under the system tile; the Presentations tile marked with a dot;
groups the sidebar opened close behind the reader); browsing Presentations keeps the sidebar on Presentations; the
shelf picker becomes a card under the search; the flat theme is the default. Pilot: repair/pilots/nav-home/make_pilot.py
(this script runs it and turns its replacements into replace_global edits, so batch and pilot cannot drift)."""
import json, os, runpy, sys, tempfile
WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
pilot = os.path.join(WS, 'repair', 'pilots', 'nav-home', 'make_pilot.py')
out = os.path.join(tempfile.mkdtemp(), 'pilot.html')
argv = sys.argv; sys.argv = [pilot, os.path.join(WS, 'index.html'), out]
ns = runpy.run_path(pilot); sys.argv = argv
E = [{'op': 'replace_global', 'find': a, 'with': b} for a, b in ns['PAIRS']]
json.dump({'edits': E}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '40_nav_home.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(E), 'edits; pilot page', out)
