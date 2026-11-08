#!/usr/bin/env python3
"""Tests for ui_retired.py (gate check ui-retired): each item kind is caught when it comes back and left alone when only a
live neighbour is present."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ui_retired as U

MD = """# UI map

## Retired (selectors and ids removed; none may come back)

| Selector or id | Retired in | Replaced by |
|---|---|---|
| #modes .flatt (Flat theme switch), body .axm-flat #modes .flatt .knob | s168 | Surface |
| --t-old-token | s168 | none |
| #mkrail, .mk-* (mockups) | never shipped | #ax2rail |
| a.aq | s167c | none |
| "BOARD-STYLE ONLY" switch | s167c | none |

## Next section
| .live | x | y |
"""


def page(css='', js='', body=''):
    return ('<html><head><style id="ax-css">' + css + '</style></head><body>' + body +
            '<script type="application/json" id="axlog">{"x":"BOARD-STYLE ONLY removed"}</script>'
            '<script id="ax-js">' + js + '</script></body></html>')


CLEAN = page('@layer components{#modes .surf{color:red}#modes .knob{top:0}.track{x:1}}', 'var a="ax2rail";', '<nav id="nav"><a class="axn-b">x</a></nav>')
CASES = [
    ('selector in a layer', page('@layer layout{@media (min-width:1px){#modes .flatt{color:red}}}'), '#modes .flatt'),
    ('selector as a compound tail', page('body .axm-flat #modes .flatt .knob,.x{a:b}'), 'body .axm-flat #modes .flatt .knob'),
    ('custom property', page(':root{--t-old-token:1px}'), '--t-old-token'),
    ('custom property in a script', page('', 'el.style.setProperty("--t-old-token","1")'), '--t-old-token'),
    ('id in markup', page('', '', '<div id="mkrail"></div>'), '#mkrail'),
    ('id in a script', page('', 'd.id="mkrail";'), '#mkrail'),
    ('prefix class in markup', page('', '', '<i class="mk-row"></i>'), '.mk-*'),
    ('prefix class in a script', page('', 'b.className="x mk-tip";'), '.mk-*'),
    ('tag and class in markup', page('', '', '<a class="aq" href="#x">x</a>'), 'a.aq'),
    ('label in page text', page('', '', '<button>Board-style only</button>'), '"BOARD-STYLE ONLY" switch'),
]


def main():
    fails = 0
    got = U.check(CLEAN, MD)
    if got:
        fails += 1; print('FAIL clean page reported', got)
    if len(U.table_items(MD)) != 7:
        fails += 1; print('FAIL table items', U.table_items(MD))
    for name, html, item in CASES:
        hits = [h for h in U.check(html, MD) if h[1] == item]
        if not hits:
            fails += 1; print('FAIL', name, 'not caught:', item)
    bad = U.check(CLEAN, MD.replace('| a.aq |', '| Some Words |'))
    if not any(h[2] == 'unreadable' for h in bad):
        fails += 1; print('FAIL an unreadable entry passed')
    print('ui_retired tests: %d of %d passed' % (len(CASES) + 3 - fails, len(CASES) + 3))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
