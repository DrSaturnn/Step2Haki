#!/usr/bin/env python3
"""make_gate_page.py: the small page the rule self-test (tools/test_gate_rules.py) runs its cases on.

  python3 tools/fixtures/make_gate_page.py [PAGE]      PAGE defaults to workspace/index.html

One gate run on the full page takes about a minute and the self-test makes about forty, so the cases run on a page
that keeps only the briefs they read. This script cuts that page from PAGE and writes, under tools/fixtures/gate_page/:

  index.html                 the page chrome (styles, scripts, navigation) and the kept briefs, bytes unchanged
  search.json                its search index (tools/search_index.js)
  repair/nbme/coverage.csv   the NBME coverage rows of the kept briefs
  KEPT.txt                   the kept brief ids and why each is kept

Kept: the first brief of each kind (topic, Part II, Aquifer); the first three briefs in page order (the merge and
item-move cases); the first brief with a step rail; two hubs, one brief placed in Presentations and one plain topic
brief (the navigation cases). Three things are rewritten so the cut page passes the gate on its own: navigation
links to removed briefs are dropped, each section count is set to its number of links, and a "Pairs with" partner
that was removed is marked <i> (the gate's form for a partner that does not exist); a link to a removed brief
elsewhere on the page keeps its text and loses its <a>.

Rerun it when a gate rule changes what a clean page must hold and the first self-test case ("passes the gate") fails
on the fixture; commit the result with the rule change. The self-test compares counts with the fixture's own counts,
so a ship that lowers a baseline does not make the fixture stale.
"""
import csv
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
WS = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
from pagelib import briefs, read_page  # noqa: E402

OUT = os.path.join(HERE, 'gate_page')


def pick(page, bl):
    why = {}

    def keep(b, reason):
        why.setdefault(b.id, []).append(reason)

    for kind in ('brief', 'bs', 'aq'):
        keep(next(x for x in bl if x.kind == kind), 'first %s brief' % kind)
    for b in bl[:3]:
        keep(b, 'one of the first three briefs')
    keep(next(x for x in bl if '<nav class="sp-step"' in page[x.start:x.end]), 'first brief with a step rail')
    hubs = [b for b in bl if b.attrs.get('data-entry') == 'hub']
    placed = [b for b in bl if b.attrs.get('data-sys') == 'presentations' and b.attrs.get('data-entry') != 'hub']
    for b in hubs[:2]:
        keep(b, 'hub')
    for b in placed[:1]:
        keep(b, 'placed in Presentations')
    keep(next(b for b in bl if b.kind == 'brief' and b.attrs.get('data-entry') != 'hub' and b not in placed), 'plain topic brief')
    return why


def cut(page, bl, kept):
    out, pos = [], 0
    for b in bl:
        if b.id not in kept:
            out.append(page[pos:b.start]); pos = b.end
    out.append(page[pos:])
    html = ''.join(out)
    gone = {b.id for b in bl} - set(kept)
    a, z = html.find('<div id="navlinks">'), html.find('</aside>', html.find('<div id="navlinks">'))
    nav = re.sub(r'[ \t]*<a href="#([^"]+)"[^>]*>.*?</a>\n?', lambda m: '' if m.group(1) in gone else m.group(0),
                 html[a:z], flags=re.S)
    parts = re.split(r'(<div class="sect(?: [a-z0-9 -]+)?">.*?</div>)', nav, flags=re.S)
    for i in range(1, len(parts), 2):
        n = len(re.findall(r'<a\b[^>]*>', parts[i + 1])) if i + 1 < len(parts) else 0
        parts[i] = re.sub(r'(<span class="count">)\d+(</span>)', lambda m: m.group(1) + str(n) + m.group(2), parts[i])
    rest = re.sub(r'<a\b[^>]*\bhref="#([^"]+)"[^>]*>(.*?)</a>', lambda m: m.group(2) if m.group(1) in gone else m.group(0),
                  html[z:], flags=re.S)
    html = html[:a] + ''.join(parts) + rest
    titles = {re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t)).strip().lower()
              for t in re.findall(r'<h4[^>]*>(.*?)</h4>', html, flags=re.S)}

    def pairs(m):
        def one(b):
            t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', b.group(1))).strip().lower()
            return b.group(0) if t in titles else '<i>%s</i>' % b.group(1)
        return m.group(1) + re.sub(r'<b>(.*?)</b>', one, m.group(2), flags=re.S) + m.group(3)
    html = re.sub(r'(<div class="pearls"[^>]*>\s*<span class="lbl">Pairs with</span>)(.*?)(</div>)', pairs, html, flags=re.S)
    return html


def main(a):
    src = a[0] if a else os.path.join(WS, 'index.html')
    page = read_page(src)
    bl = briefs(page)
    why = pick(page, bl)
    html = cut(page, bl, why)
    os.makedirs(os.path.join(OUT, 'repair', 'nbme'), exist_ok=True)
    p = os.path.join(OUT, 'index.html')
    open(p, 'w', encoding='utf-8').write(html)
    ids = set()
    for v in re.findall(r'data-nbme="([^"]*)"', html):
        ids.update(v.split())
    rows = list(csv.reader(open(os.path.join(WS, 'repair', 'nbme', 'coverage.csv'), encoding='utf-8', newline='')))
    with open(os.path.join(OUT, 'repair', 'nbme', 'coverage.csv'), 'w', encoding='utf-8', newline='') as fh:
        csv.writer(fh, lineterminator='\n').writerows([rows[0]] + [r for r in rows[1:] if r and r[0] in ids])
    with open(os.path.join(OUT, 'KEPT.txt'), 'w', encoding='utf-8') as fh:
        fh.write(''.join('%s\t%s\n' % (b.id, '; '.join(why[b.id])) for b in bl if b.id in why))
    r = subprocess.run(['node', os.path.join(TOOLS, 'search_index.js'), p, os.path.join(OUT, 'search.json')],
                       capture_output=True, text=True, cwd=WS)
    if r.returncode:
        print('make_gate_page: search index FAILED: ' + (r.stdout + r.stderr).strip()[-300:])
        return 1
    print('make_gate_page: %d of %d briefs kept, %d KB of %d KB, %d coverage rows (tools/fixtures/gate_page/)'
          % (len(why), len(bl), len(html.encode('utf-8')) // 1024, len(page.encode('utf-8')) // 1024, len(ids)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
