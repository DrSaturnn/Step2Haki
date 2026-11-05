#!/usr/bin/env python3
"""s161d (site layer, Jonathan 2026-11-04: "theres also an issue being able to scroll to the bottom of the side bar when
opened, it should be able to scroll all the way down with all items open"): on windows 1500 px and wider the page is
zoomed to 110% (s146c), and the desktop sidebar's height, calc(100vh - 32px), is zoomed with it, so the panel ran about
10% past the bottom of the window (72 px at 1600 x 900) and its last rows could not be reached. The panel is now held
16 px from the top and the bottom of the window (top and bottom insets, no height from vh), so it fits at any zoom.
Writes repair/s161d/40_sidebar_fit.json."""
import json, os
E = [{'op': 'replace_global', 'find': '</head>', 'note': 'desktop sidebar held by insets, not 100vh',
      'with': '<style id="ax-s161d">\n/* s161d: the desktop sidebar fits the window at the 110% zoom of wide windows (Jonathan 2026-11-04) */\n'
              '@media (min-width:1101px){#nav.axn{top:16px;bottom:16px;height:auto}}\n</style>\n</head>'}]
json.dump({'edits': E}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '40_sidebar_fit.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(E), 'edit')
