#!/usr/bin/env python3
"""Dump a live brief's text above the practice bank as numbered lines L02.. (lead tool, s146; run from workspace/).
usage: dump_lines.py <brief id> <out live_lines.json>  (prints the lines; writes the json)"""
import json, re, sys
from bs4 import BeautifulSoup, NavigableString
bid, out = sys.argv[1], sys.argv[2]
soup = BeautifulSoup(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'index.html'), encoding='utf-8').read(), 'lxml')
b = soup.find('div', id=bid, class_='brief')
lines = []
BLOCK = {'p', 'li', 'tr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dt', 'dd', 'figcaption', 'caption', 'summary'}
stop = False
def leafish(el):
    return not any(getattr(c, 'name', None) in BLOCK | {'div', 'table', 'ul', 'ol'} for c in el.descendants)
def walk(el):
    global stop
    for c in el.children:
        if stop: return
        if isinstance(c, NavigableString) or c.name is None: continue
        cls = ' '.join(c.get('class', []))
        if c.name == 'ol' and 'bank' in cls: stop = True; return
        if c.name == 'h5' and 'authored-hdr' in cls and 'Practice' in c.get_text(): stop = True; return
        if c.name in ('script', 'style', 'button') and not c.get_text(strip=True): continue
        if c.name in BLOCK or (c.name == 'div' and leafish(c)):
            if c.name == 'tr':
                t = ' | '.join(td.get_text(' ', strip=True) for td in c.find_all(['td', 'th']))
            else:
                t = c.get_text(' ', strip=True)
            t = re.sub(r'\s+', ' ', t)
            if t: lines.append(t)
            if c.name in BLOCK and c.name != 'li': continue
            if c.name == 'li' and not c.find(['ul', 'ol']): continue
            if c.name == 'div': continue
        walk(c)
walk(b)
d = {'L%02d' % (i + 2): t for i, t in enumerate(lines)}
json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in d.items(): print(k, v)
