"""render_v2: draws format v2 brief records into the page.

  python3 tools/render_v2.py PAGE RECORDS_DIR [--ids A,B] [--host ID=RID,...] [--out FILE] [--check]

RECORDS_DIR holds one RECORD_ID.json per brief (workspace/local/records_v2/). For each record whose id names a brief on
the page, the brief's inner markup (inside its <template class="axl">) is replaced by the drawing and its root takes the
class v2. Every other brief is left byte for byte. --check: each drawn brief's visible strings equal its record's
strings, and the page outside the drawn briefs equals PAGE; exit 1 on any difference. --host ID=RID draws record RID
in place of brief ID, for a record with no brief of its own on the page; test pages only, refused when the output is
index.html.
"""
import html as H
import copy, json, os, re, sys
from collections import Counter

E = lambda s: H.escape(str(s), quote=False)
A = lambda s: H.escape(str(s), quote=True)

# ---------- record strings ----------
STRUCT = {'c', 'under', 'assembled', 'empty', 'chrome', 'mark', 'ref', 'xdom', 'kind', 'align', 'x', 'lv', 'row', 'once', 'warn', 'format', 'id', 'entry', 'source', 'attrs', 'tone', 'form', 'task', 'to', 'src', 'version', 'status', 'urgent', 'correct', 'key', 'b', 'i', 'nbme', 'op', 'type', 'nl'}
CHROME = {'Dotted line', 'hover or tap for the reason', 'If', '→', 'Avoid', 'Chain and insights', 'Stack', 'List', 'Review', 'Related topics',
          'Illness script', 'Presentation', 'Workup', 'Treatment', 'When the answer changes', 'Diagnosis', 'Differential',
          'Practice questions'}
STEPS = {'disease': ['Illness script', 'Workup', 'Treatment', 'Differential', 'Practice'],
         'hub': ['Presentation', 'Workup', 'Differential', 'Practice'],
         'drug': ['Illness script', 'Workup', 'Treatment', 'Differential', 'Practice']}

def norm(s):
    return re.sub(r'^: ', '', ' '.join(str(s).split()))

def strings(o, key=None):
    if isinstance(o, str):
        if key not in STRUCT:
            yield norm(o)
    elif isinstance(o, list):
        for x in o:
            yield from strings(x, key)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in STRUCT:
                yield from strings(v, k)

# source names in any case; authoring marks in capitals only ("conflict" is also a clinical word)

def tip_html(tip):
    if isinstance(tip, str):
        return '<span class="yp">%s</span>' % E(tip)
    src = ' data-src="%s"' % A(tip['src']) if tip.get('src') else ''
    out = []
    if tip.get('title'):
        out.append('<b class="yt">%s</b>' % E(tip['title']))
    if tip.get('head'):
        h = '<i class="yh">%s</i>' % text(tip['head'])
        out.insert(0, h) if tip.get('head_first') else out.append(h)     # head_first: the head line above the title
    for ln in tip.get('lines', []):
        out.append('<span class="yl">%s</span>' % text(ln))
    return '<span class="yp"%s>%s</span>' % (src, ''.join(out))

def run(r, cls=''):
    pre = '<br>' if r.get('nl') else ''
    if 'op' in r:
        return pre + '<span class="op %s" role="img" aria-label="%s"></span>' % ('op-a' if r['op'] == 'leads to' else 'op-p', r['op'])
    t = text(r['rich']) if 'rich' in r else E(r['t'])
    src = ' data-src="%s"' % A(r['src']) if r.get('src') else ''
    if r.get('tip') is not None:
        return pre + '<span class="it ti%s"%s><span class="y" role="button" tabindex="0">%s</span>%s</span>' % (cls, src, t, tip_html(r['tip']))
    if r.get('to'):
        t = '<a class="lk%s" data-to="%s">%s</a>' % (' sm' if r.get('c') == 'sm' else '', A(r['to']), t)   # sm: a small link after a name
    if r.get('ref'):
        t = '<a class="lk" href="#%s">%s</a>' % (A(r['ref']), t)
    if r.get('b'):
        t = '<b>%s</b>' % t
    if r.get('i'):
        t = '<i>%s</i>' % t
    if r.get('c') in ('fr', 'ul0'):                # the stem phrase line; the muted lead of a list
        return pre + '<span class="%s">%s</span>' % (r['c'], t)
    if src:
        t = '<span%s>%s</span>' % (src, t)
    elif not (r.get('to') or r.get('ref') or r.get('b') or r.get('i')):
        t = '<span>%s</span>' % t                # one node per run, so the string check sees the record's runs
    return pre + t

def text(x):
    if x is None:
        return ''
    if isinstance(x, str):
        return E(x)
    return ''.join(run(r) for r in x)

def piece(rs):
    """a stretch of runs with its outer spaces trimmed; one plain run is bare text"""
    rs = copy.deepcopy(rs)
    for r in rs:
        r.pop('nl', None)
    if rs and 't' in rs[0]: rs[0]['t'] = rs[0]['t'].lstrip()
    if rs and 't' in rs[-1]: rs[-1]['t'] = rs[-1]['t'].rstrip()
    return E(rs[0]['t']) if len(rs) == 1 and set(rs[0]) == {'t'} else text(rs)

def split_runs(x, at):
    """a text as stretches of runs, a new stretch at each run that at() marks; the mark itself is kept only for 'nl'"""
    if isinstance(x, str):
        return [[{'t': x}]]
    out = [[]]
    for r in x:
        if at(r) and out[-1]:
            out.append([])
        if 'op' not in r or not at(r):
            out[-1].append(r)
    return out

def stack(x):
    """a text with line breaks, one span per line"""
    return ''.join('<span>%s</span>' % piece(g) for g in split_runs(x, lambda r: r.get('nl')))

def line(x, cls='ln'):
    if isinstance(x, dict) and 'classic' in x:          # the classic presentation: one tinted chip
        c = x['classic']
        return '<div class="%s"><div class="pc"><b class="pct">%s</b>%s</div></div>' % (cls, E(c['title']), ''.join('<span>%s</span>' % text(i) for i in c['items']))
    if isinstance(x, dict) and 'chip' in x:
        mn = x.get('mnemonic')                     # a mnemonic card inside the line
        card_ = ('<div class="pc" style="margin-top:8px"><b class="pct">%s</b>%s</div>' % (E(mn['title']), ''.join(
            '<span><b>%s</b><span>%s</span></span>' % (E(l['l']), text(l['text'])) for l in mn['letters']))) if mn else ''
        return '<div class="%s urg"><b class="ul">%s</b>%s%s</div>' % (cls, E(x['chip']), text(x['text']), card_)
    return '<div class="%s">%s</div>' % (cls, text(x))

LIST_ROWS = ('Culprits', 'Used for')

def chain_line(x):
    """a Mechanism line: the runs before its first "leads to" are the lead, drawn bold"""
    if isinstance(x, str) or not any(r.get('op') == 'leads to' for r in x):
        return text(x)
    i = next(n for n, r in enumerate(x) if r.get('op') == 'leads to')
    lead = ''.join(r.get('t', '') for r in x[:i]).strip()
    if any(set(r) - {'t', 'b'} for r in x[:i]):
        return text(x)                              # a lead with a hover, link or mark keeps its runs
    return '<b>%s</b>%s' % (E(lead), text(x[i:]))

def bare(x):
    """a text whose plain runs are bare text nodes (the list rows and the stem phrase line of the target page)"""
    if isinstance(x, str):
        return E(x)
    return ''.join(E(r['t']) if set(r) == {'t'} else run(r) for r in x)

def kv(row, drug=False):
    if drug and row['k'] == 'Mechanism':
        body = '<div class="mech">%s</div>' % ''.join('<div>%s</div>' % chain_line(v) for v in row['v'])
    elif drug and row['k'] in LIST_ROWS:
        body = '<div class="uses">%s</div>' % ''.join(
            ('<span class="ul0">%s</span>' % E(v[0]['t'])) if isinstance(v, list) and len(v) == 1 and v[0].get('c') == 'ul0' else '<div>%s</div>' % bare(v)
            for v in row['v'])
    else:
        body = '<div>%s</div>' % '<br>'.join(text(v) for v in row['v'])
    return '<div class="kv"><div class="lb">%s</div>%s</div>' % (E(row['k']), body)

def sub(label):
    return '<div class="sub"><b>%s</b></div>' % E(label)

def card(inner, cls='bx card'):
    return '<div class="%s">%s</div>' % (cls, inner)

def blk(title, inner, k=None, cls='blk'):
    dk = ' data-k="%s"' % k if k else ''
    return '<div class="%s"%s><h2 class="st">%s</h2>%s</div>' % (cls, dk, E(title), inner)

def two(a, b, cls='two', k=None):
    dk = ' data-k="%s"' % k if k else ''
    return '<div class="%s"%s>%s%s</div>' % (cls, dk, a, b)

def table(t, caption=True, cls=''):
    head = '<thead><tr>%s</tr></thead>' % ''.join('<th>%s</th>' % E(h) for h in t['head'])
    rows = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % text(c) for c in r) for r in t['rows'])
    cap = sub(t['caption']) if caption and t.get('caption') else ''
    return '%s<table class="c3 tb%s">%s<tbody>%s</tbody></table>' % (cap, cls, head, rows)

def drawer(d, extra=''):
    body = []
    tl = d.get('timeline')
    if tl and any(x.get('why') for x in tl):
        body.append('<ol class="tlv mon">%s</ol>' % ''.join('<li><b>%s</b><span>%s</span>%s</li>' % (
            E(x['when']), text(x['text']), '<em>%s</em>' % text(x['why']) if x.get('why') else '') for x in tl))
    elif tl:
        body.append('<ol class="tlv">%s</ol>' % ''.join('<li><b>%s</b>%s</li>' % (E(x['when']), text(x['text'])) for x in tl))
    if d.get('table'):
        body.append(table(d['table']))
    for it in d.get('items', []):
        if it.get('avoid') or it.get('why'):
            body.append('<div class="mg"><b>%s</b>%s%s%s</div>' % (
                text(it['label']), stack(it['text']),
                '<div class="avr"><i>Avoid</i><span>%s</span></div>' % text(it['avoid']) if it.get('avoid') else '',
                '<em>%s</em>' % text(it['why']) if it.get('why') else ''))
        else:
            body.append('<div class="ln"><b>%s</b><br>%s</div>' % (text(it['label']), text(it['text'])))
    for ln in d.get('lines', []):
        body.append(line(ln))
    return '<div class="dz"><button type="button">%s</button><div class="body">%s%s</div></div>' % (E(d['title']), extra, ''.join(body))

# ---------- slots ----------
def script(s, drug=False):
    c1 = card(sub('Presentation') + ''.join(line(x) for x in s['presentation'])) if s.get('presentation') else ''
    c2 = ''.join(kv(r, drug) for r in s['rows'])
    if drug and s.get('insights'):                  # a drug script holds its insights as a row
        ins = ''.join(insight(i) for i in s['insights']).replace('<div class="ins">', '<div class="ins" style="margin-top:0">', 1)
        c2 += '<div class="kv"><div class="lb">Insights</div><div>%s</div></div>' % ins
    elif s.get('chain'):
        c2 += drawer({'title': 'Chain and insights'}, chain(s['chain']) + ''.join(insight(i) for i in s.get('insights', [])))
    elif s.get('insights'):
        c2 += drawer({'title': 'Insights'}, ''.join(insight(i) for i in s['insights']))
    for d in s.get('drawers', []):
        c2 += drawer(d)
    return c1 + card(c2)

def chain(phases):
    out = []
    for p in phases:
        if p.get('label'):
            out.append('<div class="ph">%s</div>' % E(p['label']))
        out += ['<div class="ar">%s</div>' % text(x) for x in p['steps']]
    return '<div class="ch">%s</div>' % ''.join(out)

def insight(i):
    """a line whose runs are joined by "leads to" marks is drawn one step per line"""
    out = []
    for x in i['lines']:
        st = split_runs(x, lambda r: r.get('op') == 'leads to')
        if len(st) > 1:
            out.append('<span>%s</span>' % piece(st[0]))
            out += ['<span class="ia">%s</span>' % piece(g) for g in st[1:]]
        else:
            out.append('<span>%s</span>' % text(x))
    return '<div class="ins"><b>%s</b>%s</div>' % (E(i['claim']), ''.join(out))

def score(sc):
    """a scoring rule: its items with points, then one line per cutoff range with the step it leads to"""
    arrow = ' <i>→</i> '
    rows = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (text(x['item']), E(x['points'])) for x in sc['items'])
    out = ['<table class="wl"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>\n%s\n</tbody></table>' % (E(sc['name']), E(sc['points_head']), rows)]
    for t in sc['cutoffs']:
        sub_ = '<em>%s</em>' % arrow.join(text(x) for x in t['sub']) if t.get('sub') else ''
        out.append('<div class="tot"><b>%s</b><span>%s%s</span></div>' % (E(t['range']), arrow.join(text(x) for x in t['chain']), sub_))
    return '\n'.join(out)

def criteria(c, drug=False):
    if c.get('score'):
        return blk(c['title'], card(score(c['score'])))
    if drug and c.get('mnemonic') and 'letters' in c['mnemonic']:
        m = c['mnemonic']                            # an open tinted card, never in a drawer
        cardh = '<div class="pc"%s style="margin-top:8px"><b class="pct">%s</b>%s</div>' % (
            ' id="%s"' % A(m['ref']) if m.get('ref') else '', E(m['title']), ''.join(('<span>%s</span>' % text(x['text'])) if x.get('inside') else '<span><b>%s</b><span>%s</span></span>' % (E(x['l']), text(x['text'])) for x in m['letters']))
        rows = []
        for r in c['rows']:
            h = kv(r, True)
            if r['k'] == m.get('under'):
                h = h[:-len('</div></div>')] + cardh + '</div></div>'
            rows.append(h)
        inner = ''.join(rows) + ('' if m.get('under') in [r['k'] for r in c['rows']] else '<div class="ln">%s</div>' % cardh.replace(' style="margin-top:8px"', ''))
        return blk(c['title'], card(inner))
    inner = (sub(c['label']) if c.get('label') else '') + ''.join(kv(r) for r in c['rows'])
    if c.get('mnemonic'):
        m = c['mnemonic']
        inner += drawer({'title': m['title']}, '<div class="mn"%s>%s</div>' % (' id="%s"' % A(m['ref']) if m.get('ref') else '', ''.join('<b>%s</b><span>%s</span>' % (E(x['l']), text(x['text'])) for x in m['letters'])))
    more = ''
    for x in c.get('cards', []):                    # further cards of the panel: a short table, or labeled rows
        if 'table' in x:
            more += card(wl_table(x['table']))
        else:
            more += card((sub(x['label']) if x.get('label') else '') + ''.join(kv(r) for r in x['rows']))
    return blk(c['title'], card(inner) + more)

def wl_table(t):
    """a two-column lookup in the criteria panel; last_px fixes the last column's width with no wrap"""
    fix = ' style="width:%dpx;white-space:nowrap"' % t['last_px'] if t.get('last_px') else ''
    cell = lambda tag, v, last: '<%s%s>%s</%s>' % (tag, fix if last else '', v, tag)
    head = ''.join(cell('th', E(h), k == len(t['head']) - 1) for k, h in enumerate(t['head']))
    rows = ''.join('<tr>%s</tr>' % ''.join(cell('td', text(v), k == len(r) - 1) for k, v in enumerate(r)) for r in t['rows'])
    return '<table class="wl"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (head, rows)

def workup(w):
    rows = []
    for g in w['groups']:
        if g.get('label'):
            q = '<span class="hq">%s</span>' % text(g['qualifier']) if g.get('qualifier') else ''
            rows.append('<tr class="grp"><td colspan="3"><b>%s</b>%s</td></tr>' % (E(g['label']), q))
        for r in g['rows']:
            cond = '<span class="cond2"><i>If</i> %s</span>' % text(r['if']) if r.get('if') else ''
            if not r['results']:                                  # a test with no result line on the page: empty cells
                rows.append('<tr><td>%s%s</td><td></td><td></td></tr>' % (text(r['test']), cond)); continue
            first, rest = r['results'][0], r['results'][1:]
            span = ' rowspan="%d"' % len(r['results']) if rest else ''   # the test cell spans its result rows
            rows.append('<tr><td%s>%s%s</td><td>%s</td><td>%s</td></tr>' % (span, text(r['test']), cond, text(first['result']), text(first['means'])))
            rows += ['<tr class="cont rs"><td>%s</td><td>%s</td></tr>' % (text(x['result']), text(x['means'])) for x in rest]
    head = '<thead><tr>%s</tr></thead>' % ''.join('<th>%s</th>' % E(h) for h in w['head'])
    also = ''.join('<div class="ln"><span class="cond2"><i>If</i> %s</span>%s</div>' % (text(a['if']), '<br>'.join('<b>%s</b>' % text(x) for x in a['tests']))
                   for a in w.get('also', []))          # tests the source gives no result for
    skip = ('<div class="lad avd"><div>%s</div><div>%s</div></div>' % (E(w['skip']['label']), ''.join('<span>%s</span>' % text(x) for x in w['skip']['lines']))
            if w.get('skip') else '')
    return '<table class="c3">%s<tbody>%s</tbody></table>%s%s%s' % (head, ''.join(rows), also, ''.join(line(x) for x in w.get('notes', [])), skip)

def treatment(t):
    out = []
    for s in t.get('ladder', []):
        if s.get('group'):                         # a titled group of rungs (ssri-effects): a header band, as a Workup group
            out.append('<div class="lgp"><b>%s</b></div>' % E(s['group']))
        do = s['do']
        do = '<div class="it">%s</div>' % text(do) if not isinstance(do, str) else '<b class="act">%s</b>' % E(do)
        out.append('<div class="lad"><div><span class="ck%s">%s</span></div><div><span class="wh">%s</span>%s</div></div>'
                   % ((' g' if s.get('tone') == 'confirm' else '') + (' wr' if len(s['chip']) > 12 else ''), E(s['chip']), text(s['when']), do))   # a long chip wraps in its column
    if t.get('avoid'):
        out.append('<div class="lad avd"><div>Avoid</div><div>%s</div></div>' % ''.join('<span>%s</span>' % text(x) for x in t['avoid']))
    out += [drawer(d) for d in t.get('drawers', [])]
    if t.get('followup'):
        out.append(drawer(t['followup']))
    return ''.join(out)

def answer_changes(ac):
    out = []
    for key, rows in ac.items():
        out.append(sub(key[:1].upper() + key[1:]))
        for r in rows:
            chip = '<b class="ul">Urgent</b>' if r.get('urgent') else ''
            src = ' data-src="%s"' % A(r['src']) if r.get('src') else ''
            out.append('<div class="wc%s"%s>%s<span><i>If</i> %s</span><b>%s</b>%s</div>'
                       % (' urg' if chip else '', src, chip, bare(r['if']) if any(x.get('c') == 'fr' for x in (r['if'] if isinstance(r['if'], list) else [])) else text(r['if']), text(r['then']), '<em>%s</em>' % text(r['why']) if r.get('why') else ''))
    return ''.join(out)

def dx_name(x):
    """a name followed by a hover phrase: the phrase sits under the name in regular weight"""
    if isinstance(x, list) and len(x) == 2 and set(x[0]) == {'t'} and x[1].get('tip') is not None:
        return '<span>%s</span>%s' % (E(x[0]['t'].rstrip()), run(x[1], ' stm'))
    return text(x)

def dxtable(d, zebra=False):
    head = '<thead><tr>%s</tr></thead>' % ''.join('<th>%s</th>' % E(h) for h in d['head'])
    rows, n = [], 0
    for g in d['groups']:
        if g.get('label'):
            rows.append('<tr class="grp"><td colspan="3">%s</td></tr>' % E(g['label']))
        for r in g['rows']:
            z = ' class="z"' if zebra and n % 2 == 0 else ''
            name = dx_name(r['dx']) if zebra else text(r['dx'])
            rows.append('<tr%s><td>%s</td><td>%s</td><td>%s</td></tr>' % (z, name, text(r['features']), text(r['decides'])))
            n += 1
    return '<table class="c3%s">%s<tbody>%s</tbody></table>' % (' zb' if zebra else '', head, ''.join(rows))

CURVE = '<svg preserveAspectRatio="none" viewBox="0 0 100 60"><path class="a" d="M0,54 L6,54 C12,54 16,10 24,10 C32,10 36,40 46,40 L100,40 L100,60 L0,60 Z"></path><path class="l" d="M0,54 L6,54 C12,54 16,10 24,10 C32,10 36,40 46,40 L100,40"></path></svg>'

def figure(f):
    """Lane geometry is not in the record: labels, ticks and the curve are spaced evenly."""
    out = []
    for sec in f['sections']:
        if sec.get('label'):
            out.append(sub(sec['label']))
        for ln in sec['lanes']:
            n = max(len(ln['ticks']) - 1, 1)
            pos = [round(4 + 88 * k / n) for k in range(len(ln['ticks']))]
            ticks = ''.join('<s style="left:%d%%"><b>%s</b></s>' % (p, E(t)) for p, t in zip(pos, ln['ticks']))
            u = '<u style="left:%d%%"></u>' % pos[-1]
            if ln['form'] == 'requirement':
                body = '<i class="pre" style="width:%d%%"></i><i class="fl" style="left:%d%%"></i>' % (pos[-1], pos[-1])
            else:
                sits = ln.get('situations', [])
                body = ''.join('<div class="sit" style="left:%d%%;width:24%%">%s</div>' % (14 + 44 * k, E(s)) for k, s in enumerate(sits)) + CURVE
                body += ''.join('<em%s style="left:%d%%;top:%dpx">%s</em>' % (' class="k"' if l.get('key') else '', 27 + 12 * k, 14 + 30 * (k % 2), E(l['text']))
                                for k, l in enumerate(ln.get('labels', [])))
            out.append('<div class="swl"><div class="nm"><b>%s</b><span>%s</span></div><div class="tl%s">%s%s%s</div></div>'
                       % (E(ln['name']), text(ln['sub']), ' rq' if ln['form'] == 'requirement' else '', body, ticks, u))
    if f.get('legend'):
        out.append('<p class="swk"><span class="k mk"></span>%s</p>' % text(f['legend']))
    return '<div class="sw">%s</div>' % ''.join(out)

def related(rel):
    if not rel:
        return ''
    items = '<br>'.join('<i%s>%s</i>: %s' % (' data-to="%s"' % A(r['to']) if r.get('to') else '', E(r['title']), E(r['text'])) for r in rel)
    return '<div class="qrel card"><b>Related topics</b>%s</div>' % items

def practice(rec):
    return ('<div class="blk v-stack" data-k="prac"><h2 class="st">Practice questions</h2><div class="qtools"><div class="qv">'
            '<button type="button" data-v="stack" class="on">Stack</button><button type="button" data-v="list">List</button>'
            '<button type="button" data-v="review">Review</button></div><div class="qfl"></div></div><div class="qhost"></div>'
            '<div class="qn"></div><div class="qrev"></div>%s</div>' % related(rec['related']))

def qbank(rec):
    out = []
    for it in rec['practice']['items']:
        q = {'t': it['task'], 'c': it['label'], 'l': it['stem']['lead'], 'f': it['stem']['findings']}
        if it['stem'].get('exam'):
            q['x'] = it['stem']['exam']
        q['q'] = it['question']
        q['o'] = [[1 if o['correct'] else 0, o['text'], o['why']] for o in it['options']]
        q['w'] = [it['answer']['text'], it['answer']['why']]
        out.append(q)
    return json.dumps(out, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

# ---------- legacy ----------
def lg_html(h):
    h = re.sub(r'\bclass="([^"]*)"', lambda m: 'class="%s"' % ' '.join('lg-' + c for c in m.group(1).split()), h)
    h = re.sub(r'\s(hidden|aria-hidden)(="[^"]*")?(?=[\s>/])', '', h)
    return re.sub(r'\sid="[^"]*"', '', h)

SEC_NAME = {'(before first section)': 'Head, above the question line'}

def not_placed(section, blocks):
    items = ''.join('<div class="np-i"><p class="np-r">%s</p><div class="np-x">%s</div></div>' % (E(b['reason']), lg_html(b['html'])) for b in blocks)
    return '<div class="np card"><div class="np-h"><b>Not placed</b><span>Old section: %s</span></div>%s</div>' % (E(SEC_NAME.get(section, section)), items)

# ---------- layouts ----------
def layout_disease(rec):
    S = rec['slots']
    tables = S.get('differential', {}).get('tables', [])
    out = [two(blk('Illness script', script(S['script'])), criteria(S['criteria']) if S.get('criteria') else '', 'two', 'script')]
    if S.get('workup'):
        out.append(blk('Workup', card(workup(S['workup'])), 'work'))
    out.append(two(blk('Treatment', card(treatment(S['treatment'])), 'tx'),
                   blk('When the answer changes', card(answer_changes(S['answer_changes']))) if S.get('answer_changes') else '', 'two eq'))
    d = S.get('differential')
    if d:
        inner = (figure(d['figure']) if d.get('figure') else '') + dxtable(tables[0]) + ''.join(line(x) for x in d.get('notes', []))
        out.append(blk('Differential', card(inner), 'ddx'))
    extra = ''.join(blk(t['title'], card(dxtable(t))) for t in tables[1:])
    out.append(two(extra, practice(rec), 'two pq'))
    rail = [('script', '1', 'Illness script'), ('work', '2', 'Workup'), ('tx', '3', 'Treatment'), ('ddx', '4', 'Differential'), ('prac', '', 'Practice')]
    return out, rail, {}

AXIS = [3, 26, 50, 74, 90]     # where the shared time axis draws its grid lines (the .trk rule in site/css/components/v2.css)

def onset(f):
    """the shared time axis, one lane per `lane` number (one per event where none is given), a dot at each onset;
    a delayed lane draws a line from the start of the axis to its dot. Positions come from the record."""
    xs = [t['x'] for t in f['ticks']]
    a4 = xs == AXIS[:4]                              # no Years tick (ssri-effects): the 90% grid line is not drawn
    if xs != AXIS and not a4:
        raise NotImplementedError('onset: ticks %s are not on the shared axis %s' % ([t['x'] for t in f['ticks']], AXIS))
    al = {'l': '0', 'c': '-50%', 'r': '-100%'}
    ticks = ''.join('<s style="left:%d%%;transform:translateX(%s)">%s</s>' % (t['x'], al[t.get('align', 'c')], E(t['t'])) for t in f['ticks'])
    lanes = {}
    for k, e in enumerate(sorted(f['events'], key=lambda e: e['x'])):
        lanes.setdefault(e.get('lane', 'e%d' % k), []).append(e)
    out = ['<div class="sw tm%s"><div class="swl hd">' % (' a4' if a4 else '') + '<div class="nm"></div><div class="trk hdx">%s</div></div>' % ticks]
    x0 = f['ticks'][0]['x']
    for evs in lanes.values():
        x = evs[0]['x']
        assert all(e['x'] == x for e in evs), 'onset: one lane, two positions'
        late = any(e.get('delayed') for e in evs)
        nm = ''.join('<b>%s</b>' % E(e['label']) for e in evs) + ''.join('<span>%s</span>' % E(e['text']) for e in evs if e['text'])
        mark = ('<i class="lead" style="left:%d%%;width:%d%%"></i><span class="cap" style="left:calc(%d%% + 8px)">Delayed onset</span>'
                % (x0, x - x0, x0)) if late else ''
        out.append('<div class="swl"><div class="nm">%s</div><div class="trk%s">%s%s<u style="left:%d%%"></u></div></div>'
                   % (nm, ' dl' if late else '', ticks, mark, x))
    return (sub(f['caption']) if f.get('caption') else '') + ''.join(out) + '</div>'

def layout_drug(rec):
    """the Panic and PE template rows, with the Adverse effects panel in the criteria place and a side table in row 5"""
    S = rec['slots']
    out = [two(blk('Illness script', script(S['script'], True)), criteria(S['panel'], True), 'two', 'script')]   # step 1 name
    if S.get('workup'):
        out.append(blk('Workup', card(workup(S['workup'])), 'work'))
    out.append(two(blk('Treatment', card(treatment(S['treatment'])), 'tx'),
                   blk('When the answer changes', card(answer_changes(S['answer_changes']))) if S.get('answer_changes') else '', 'two eq'))
    d = S['differential']
    notes = d.get('notes', [])
    rule = (sub('General rule').replace('"sub"', '"sub gr"') + line(notes[0]).replace('<div class="ln">', '<div class="ln" style="border-top:0;padding-top:6px">', 1)
            + ''.join(line(x) for x in notes[1:])) if notes else ''
    inner = (onset(d['onset']) if d.get('onset') else '') + dxtable(d['tables'][0], zebra=True) + rule
    out.append(blk('Differential', card(inner), 'ddx'))
    side = blk(S['side']['caption'], card(table(S['side'], caption=False, cls=' di'))) if S.get('side') else ''
    out.append(two(side, practice(rec), 'two pq'))
    for sec in dict.fromkeys(b['section'] for b in rec['legacy']):      # a kept line waiting on a call, drawn for review
        out.append(not_placed(sec, [b for b in rec['legacy'] if b['section'] == sec]))
    rail = [('script', '1', 'Illness script'), ('work', '2', 'Workup'), ('tx', '3', 'Treatment'), ('ddx', '4', 'Differential'), ('prac', '', 'Practice')]
    if not S.get('workup'):                         # no Workup row (ssri-effects): no step for it; the other numbers keep their place
        rail = [x for x in rail if x[0] != 'work']
    return out, rail, {'css': DRUG_CSS}

DRUG_CSS = ''     # drug styles live in site/css/components/v2.css

def rule_out(r):
    out = []
    for x in r['rows']:
        cond = '<span><i>If</i> %s</span>' % bare(x['if']) if x.get('if') else ''
        then = '<b>%s</b>' % bare(x['then']) if x.get('then') else ''
        out.append('<div class="wc ur"><strong>%s</strong><span>%s</span>%s%s<em><a class="lk" data-to="%s">%s</a></em></div>'
                   % (bare(x['name']), bare(x['finding']), cond, then, A(x['to']), E(x['brief'])))
    return ''.join(out)

def hub_treatment(t):
    return ''.join('<div class="mg"><b>%s</b>%s</div>' % (E(c['name']), ''.join('<span>%s</span>' % bare(x) for x in c['lines'])) for c in t['causes'])

def hub_changes(groups):
    out = []
    for g in groups:
        out.append(sub(g['label']))
        for r in g['rows']:
            offer = '<span>%s</span>' % bare(r['offer']) if r.get('offer') else ''
            out.append('<div class="wc"><span><i>If</i> %s</span>%s<b>%s</b>%s</div>'
                       % (bare(r['if']), offer, bare(r['then']), '<em>%s</em>' % bare(r['why']) if r.get('why') else ''))
    return ''.join(out)

def num(v):
    return '%g' % v

def ranges(f):
    """lanes on one axis per section, each bar or line at its record position (percent of the track)"""
    al = {'l': '0', 'c': '-50%', 'r': '-100%'}
    out = []
    for n, sec in enumerate(f['sections']):
        ticks = ''.join('<s style="left:%s%%;transform:translateX(%s)">%s</s>' % (num(t['x']), al[t['align']], E(t['t'])) for t in sec['ticks'])
        grid = ''.join('<q style="left:%s%%"></q>' % num(t['x']) for t in sec['ticks'])
        h = ['<div class="sw tm">%s<div class="swl hd"><div class="nm"></div><div class="trk hdx">%s</div></div>' % (sub(sec['label']), ticks)]
        for ln in sec['lanes']:
            nm = '<b>%s</b><span>%s</span>%s' % (E(ln['name']), bare(ln['sub']), ''.join('<span class="nt"><b>%s</b>%s</span>' % (E(x['k']), bare(x['v'])) for x in ln.get('notes', [])))
            marks = []
            for m in ln['marks']:
                if 'bar' in m:
                    marks.append('<i class="%s" style="left:%s%%;width:%s%%"></i>' % (' '.join(['rb'] + m.get('tone', [])), num(m['bar'][0]), num(m['bar'][1])))
                elif 'line' in m:
                    marks.append('<i class="lead" style="left:0;width:%s%%"></i>' % num(m['line']))
                elif 'dot' in m:
                    marks.append('<u class="dot" style="left:%s"></u>' % ('0' if m['dot'] == 0 else num(m['dot']) + '%'))
                elif 'cap' in m:
                    marks.append('<span class="cap">%s</span>' % E(m['cap']))
            h.append('<div class="swl"><div class="nm">%s</div><div class="trk%s">%s%s</div></div>'
                     % (nm, ' dl' if ln.get('delayed') else '', grid + ticks if ln.get('grid') else '', ''.join(marks)))
        if n == len(f['sections']) - 1 and f.get('legend'):
            h.append('<p class="swk"><span class="k k-%s"></span>%s</p>' % (f['legend']['tone'], bare(f['legend']['text'])))
        out.append(''.join(h) + '</div>')
    return ''.join(out)

def members(ms):
    return '<div class="qrel card mbs"><b>Member briefs</b>%s</div>' % ''.join('<a class="lk" data-to="%s">%s</a>' % (A(m['to']), E(m['title'])) for m in ms)

def hub_table(d):
    """the differential table form of a complaint overview: zebra rows, plain runs as bare text"""
    head = '<thead><tr>%s</tr></thead>' % ''.join('<th>%s</th>' % E(h) for h in d['head'])
    rows = [r for g in d['groups'] for r in g['rows']]
    body = ''.join('<tr%s><td>%s</td><td>%s</td><td>%s</td></tr>' % (' class="z"' if n % 2 == 0 else '', bare(r['dx']), bare(r['features']), bare(r['decides']))
                   for n, r in enumerate(rows))
    return '<table class="c3 zb">%s<tbody>%s</tbody></table>' % (head, body)

def layout_hub(rec):
    """the complaint overview: the five rows of every brief type, with Overview beside Rule out first"""
    S = rec['slots']
    out = [two(blk(S['overview']['title'], card(''.join(kv(r) for r in S['overview']['rows']))),
               blk(S['rule_out']['title'], card(rule_out(S['rule_out']))), 'two', 'script')]
    out.append(blk('Workup', card(workup(S['workup'])), 'work'))
    t = S.get('treatment')
    if t:
        hint = '<p class="hint">%s</p>' % bare(t['hint']) if t.get('hint') else ''
        out.append(two('<div class="blk" data-k="tx"><h2 class="st">Treatment</h2>%s%s</div>' % (card(hub_treatment(t)), hint),
                       blk('When the answer changes', card(hub_changes(S['answer_changes']))) if S.get('answer_changes') else '', 'two eq'))
    d = S['differential']
    notes = d.get('notes', [])
    rule = (sub('General rule').replace('"sub"', '"sub gr"') + line(notes[0]).replace('<div class="ln">', '<div class="ln" style="border-top:0;padding-top:6px">', 1)
            + ''.join(line(x) for x in notes[1:])) if notes else ''
    fig = ranges(d['ranges']) if d.get('ranges') else ''
    out.append(blk('Differential', card(fig + hub_table(d['tables'][0]) + rule, 'bx card" style="padding-top:18px' if fig else 'bx card'), 'ddx'))
    side = blk(S['side']['title'], card(hub_table(S['side']))) if S.get('side') else ''
    prac = practice(rec)
    if S.get('members'):
        prac = prac[:-len('</div>')] + members(S['members']) + '</div>'
    out.append(two(side, prac, 'two pq'))
    rail = [('script', '1', 'Overview'), ('work', '2', 'Workup'), ('tx', '3', 'Treatment'), ('ddx', '4', 'Differential'), ('prac', '', 'Practice')]
    if not t:
        rail = [x for x in rail if x[0] != 'tx']
    return out, rail, {}
LAYOUTS = {'disease': layout_disease, 'drug': layout_drug, 'hub': layout_hub}

# ---------- page ----------
def div_span(h, start):
    """index range of the <div ...> that opens at start, through its matching </div>"""
    depth, k = 0, start
    for m in re.compile(r'<div\b|</div>').finditer(h, start):
        depth += 1 if m.group() == '<div' else -1
        if depth == 0:
            return start, m.end()
    raise ValueError('unbalanced div at %d' % start)



# ---------- page ----------
BANK = re.compile(r'<ol class="bank\b[^"]*">.*?</ol>', re.S)

def render(rec, bank=''):
    """the brief's inner markup: title line, then the layout's rows; returns (html, rail, css). bank is the brief's own
    practice list from the page (ol.bank), kept byte for byte so question ids and progress carry over; the live bank
    code builds the questions from it inside .qhost"""
    body, rail, extra = LAYOUTS[rec['entry']](rec)
    if bank:
        body = [x.replace('<div class="qhost"></div>', '<div class="qhost">%s</div>' % bank, 1) for x in body]
    head = ('<div class="head"><div><h1>%s</h1>\n<p>%s</p></div>\n<div class="legend"><span>Dotted line</span>: hover or tap for the reason</div></div>'
            % (E(rec['title']), E(rec['lead'])))
    rl = ''.join('<button type="button" data-k="%s"><i>%s</i>%s</button>' % (k, n, E(lbl)) for k, n, lbl in rail)
    inner = '<div class="v2r"><nav class="v2rail" hidden>%s</nav>%s%s</div>' % (rl, head, '\n'.join(body))
    return inner, rail, extra.get('css', '')

BRIEF = re.compile(r'<div class="(brief\b[^"]*)" id="([^"]+)"([^>]*)><template class="axl">')

def brief_span(h, m):
    """index range of a brief's template content"""
    a = m.end()
    return a, h.index('</template>', a)

def write(page, recs, host=None):
    """host maps a page brief id to the record id drawn in its place; returns the page and {brief id: (record id, inner)}"""
    host = host or {}
    out, last, drawn = [], 0, {}
    for m in BRIEF.finditer(page):
        rid = m.group(2)
        key = host.get(rid, rid if rid not in host.values() else None)
        if key not in recs:
            continue
        a, b = brief_span(page, m)
        own = BANK.search(page, a, b) if key == rid else None      # a record drawn in another brief's place keeps no bank
        inner, rail, css = render(recs[key], own.group() if own else '')
        cls = m.group(1) if ' v2' in ' ' + m.group(1) else m.group(1) + ' v2'
        out.append(page[last:m.start()])
        out.append('<div class="%s" id="%s"%s><template class="axl">' % (cls, rid, m.group(3)))
        out.append(inner)
        last = b
        drawn[rid] = (key, inner)
    out.append(page[last:])
    return ''.join(out), drawn

def visible(inner):
    from bs4 import BeautifulSoup
    sc = BeautifulSoup(inner, 'lxml')
    for x in sc.find_all(['svg', 'script', 'style', 'nav']):
        x.decompose()
    for x in sc.select('.qhost'):                   # the practice list is checked by item id (bank_ids)
        x.decompose()
    for x in sc.select('div.trk:not(.hdx) > s'):
        x.decompose()
    return Counter(norm(n) for n in sc.find_all(string=True) if norm(n))

def check(rec, inner):
    pg = visible(inner)
    mine = Counter(s for s in strings({k: v for k, v in rec.items() if k not in ('legacy', 'practice')}) if s)
    chrome = CHROME | {'Drug script', 'Illness script', 'Adverse effects', 'Toxicity', 'Monitoring', 'Used for', 'Practice questions',
                       'Related topics', 'Insights', 'Urgent', 'Means', 'Test', 'Result', 'When the answer changes', 'Delayed onset', 'General rule', 'Member briefs'}
    for c in chrome:
        pg.pop(c, None); mine.pop(c, None)
    return mine - pg, pg - mine

def bank_ids(rec, inner):
    """the record's practice item ids against the ids of the page list kept in the drawing"""
    want = [it['id'] for it in rec['practice']['items'] if it.get('id')]
    got = re.findall(r'data-item-id="([^"]+)"', inner)
    return want, got

def outside(h, ids):
    """the page with every named brief's template content removed and v2 classes undone"""
    for m in reversed(list(BRIEF.finditer(h))):
        if m.group(2) in ids:
            a, b = brief_span(h, m)
            h = h[:m.start()] + h[m.start():m.end()].replace(' v2"', '"') + h[b:]
    return h

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
    for k in ('--ids', '--out', '--host'):
        if opt(k) in args:
            args.remove(opt(k))
    page_path, rdir = args[:2]
    page = open(page_path, encoding='utf-8').read()
    want = set(opt('--ids').split(',')) if opt('--ids') else None
    host = dict(x.split('=', 1) for x in opt('--host').split(',')) if opt('--host') else {}
    out = opt('--out') or page_path
    if host and os.path.basename(out) == 'index.html':
        sys.exit('--host draws a record in place of another brief: test pages only, never index.html')
    recs = {}
    for f in sorted(os.listdir(rdir)):
        if f.endswith('.json') and f.count('.') == 1:
            rid = f[:-5]
            if want is None or rid in want:
                recs[rid] = json.load(open(os.path.join(rdir, f), encoding='utf-8'))
    new, drawn = write(page, recs, host)
    bad = 0
    for bid, (rid, inner) in drawn.items():
        lost, added = check(recs[rid], inner)
        print('%s%s: %d strings drawn, %d not drawn, %d drawn that the record lacks' % (rid, ' (in %s)' % bid if bid != rid else '', sum(visible(inner).values()), sum(lost.values()), sum(added.values())))
        for s in list(lost)[:8]:
            print('  not drawn:', repr(s[:90]))
        for s in list(added)[:8]:
            print('  drawn, not in record:', repr(s[:90]))
        bad += bool(lost or added)
        want, got = bank_ids(recs[rid], inner)
        if bid == rid:
            ok = want == got
            print('  practice: %d page items kept, %s' % (len(got), 'ids equal to the record in order' if ok else 'IDS DIFFER from the record (%d)' % len(want)))
            bad += not ok
    same = outside(new, set(drawn)) == outside(page, set(drawn))
    print('briefs drawn: %d of %d records; page outside them %s' % (len(drawn), len(recs), 'unchanged' if same else 'CHANGED'))
    missing = sorted(set(recs) - {r for r, _ in drawn.values()})
    if missing:
        print('  no brief on the page for:', ', '.join(missing))
    open(out, 'w', encoding='utf-8').write(new)
    print('wrote', out)
    sys.exit(1 if '--check' in sys.argv and (bad or not same) else 0)

if __name__ == '__main__':
    main()
