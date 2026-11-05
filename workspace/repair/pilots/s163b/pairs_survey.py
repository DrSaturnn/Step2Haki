"""s163b I7 survey: how each Pairs with block parses under the live renderer (old) and the s163b renderer (new).
python3 repair/pilots/s163b/pairs_survey.py <page> <out.md>; prints counts."""
import re, sys
from bs4 import BeautifulSoup, NavigableString
sys.path.insert(0, 'tools')
import pagelib as P
page, out = sys.argv[1], sys.argv[2]
h = P.read_page(page)
norm = lambda s: re.sub(r'\s+', ' ', s or '').strip()
key = lambda s: re.sub(r'[^a-z0-9 ]', '', norm(s).lower())
B = P.briefs(h)
T = {key(b.title): b.id for b in B if b.title}
LBL = re.compile(r'(^|[\s.;,])(?:Part I{1,2}|Aquifer)\s*$')
def parse(div, new):
    items, cur, bad = [], None, False
    lbl = div.find('span', class_='lbl', recursive=False)
    for n in div.children:
        if n is lbl:
            continue
        if not isinstance(n, NavigableString) and n.name in ('i', 'b', 'em', 'a'):
            if new and cur is not None and n.name != 'a' and key(n.get_text()) not in T:
                cur['why'] += n.get_text(); continue
            if new:
                if cur is not None: cur['why'] = LBL.sub(r'\1', cur['why'])
                elif norm(LBL.sub('', lead)) == '': lead = ''
            if not new or cur is not None or not norm(lead): pass
            cur = {'name': norm(n.get_text()), 'why': '', 'a': n.get('href', '') if n.name == 'a' else ''}
            items.append(cur); continue
        t = n.get_text() if not isinstance(n, NavigableString) else str(n)
        if cur is not None: cur['why'] += t
        else:
            lead = (locals().get('lead') or '') + t
    if not new and norm(locals().get('lead') or ''): bad = True
    if new and norm(LBL.sub('', locals().get('lead') or '')): bad = True
    if not items or bad: return None
    return [(it['name'], (it['a'][1:] if it['a'].startswith('#') else T.get(key(it['name'])))) for it in items]
rows, c = [], {'old_list': 0, 'new_list': 0, 'became_list': 0, 'nolink_old': 0, 'nolink_new': 0, 'blocks': 0}
for b in B:
    soup = BeautifulSoup(b.inner, 'html.parser')
    for d in soup.find_all('div', class_='pearls'):
        l = d.find('span', class_='lbl', recursive=False)
        if not l or norm(l.get_text()).lower() != 'pairs with': continue
        c['blocks'] += 1
        lead = None
        o, n = parse(d, False), parse(d, True)
        c['old_list'] += bool(o); c['new_list'] += bool(n); c['became_list'] += (not o and bool(n))
        no_o = [x for x, i in (o or []) if not i]; no_n = [x for x, i in (n or []) if not i]
        c['nolink_old'] += bool(no_o); c['nolink_new'] += bool(no_n)
        rows.append('- %s: old %s%s; new %s%s' % (b.id, 'list' if o else 'sentence', ' nolink ' + repr(no_o) if no_o else '',
                    'list' if n else 'sentence', ' nolink ' + repr(no_n) if no_n else ''))
open(out, 'w').write('# Pairs with, live and s163b renderer\n\n%s\n\n' % c + '\n'.join(rows) + '\n')
print(c)
