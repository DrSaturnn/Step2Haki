#!/usr/bin/env python3
"""s170 anchor pass (D-20261108-5, A1): every hover sits on the term its card explains.

  python3 repair/s170/anchors/anchors.py survey PAGE OUT.md OUT.json   # every hover trigger with its line, kicker, title, body
  python3 repair/s170/anchors/anchors.py apply PAGE DECISIONS.json OUT  # applies the sorted decisions by offset splicing

Survey rows: brief, pop id, trigger class, trigger text, the line the trigger sits in (its nearest block: li, td, th,
p, dd, dt, div), kicker (.sp-k), title (.sp-ct) and the body text (title and kicker removed), plus `overlap`: the
content words the trigger shares with the title, kicker and the body's first line (0 marks a row to judge first).

Decisions JSON: {"<pop id>": {"verdict": "fits"} | {"verdict": "move", "term": "<exact text in the line>"} |
{"verdict": "own", "label": "<short trigger label>"} | {"verdict": "icon"}}.
- move: the trigger button moves onto the first occurrence of `term` in the same line's text, outside any other tag
  (the old trigger text stays as plain text where it was). Visible text is unchanged.
  With "cell": "row" the trigger and its card move onto the first occurrence of `term` in the first cell of the same
  table row (the row head); the old trigger text stays as plain text where it was.
- own: the trigger button is emptied of the line text (that text stays in the line as plain text) and a new button with
  `label` is placed right after the line's last text, before the card body. The label is the only new visible text.
- icon: the trigger text stays in the line as plain text and an empty marker button (class "sp-pop sp-i", drawn as a
  circled i by the style sheet) is placed right before the card body. No visible text is added.
Untouched: hovers not named in the decisions file, and hovers marked fits.
"""
import json
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
import pagelib as P  # noqa: E402
import site_build  # noqa: E402

STOP = set('a an the of and or to in on for with by at as is are be from that this its it into than then when if not no '
           'after before over under per vs versus also only more most less first second'.split())
BTN = re.compile(r'<button\b[^>]*\bclass="(sp-pop\b[^"]*)"[^>]*\baria-controls="([^"]+)"[^>]*>(.*?)</button>', re.S)
BLOCK_OPEN = re.compile(r'<(li|td|th|p|dd|dt|div)\b[^>]*>')


def txt(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).replace('&amp;', '&').replace('&nbsp;', ' ').strip()


def words(s):
    return {w for w in re.findall(r'[a-z0-9][a-z0-9-]+', s.lower()) if w not in STOP and len(w) > 2}


def stem(ws):
    return {w[:5] for w in ws}


def body_span(inner, pid):
    m = re.search(r'<span class="sp-pop-b"[^>]*\bid="%s"[^>]*>' % re.escape(pid), inner)
    if not m:
        return None
    depth, k = 1, m.end()
    for t in re.finditer(r'<span\b|</span>', inner[m.end():]):
        depth += 1 if t.group(0) == '<span' else -1
        if depth == 0:
            k = m.end() + t.start()
            break
    return m.start(), m.end(), k, k + 7


def enclosing(inner, pos):
    """start, end of the nearest block element around pos (balanced by tag name)."""
    best = None
    for m in BLOCK_OPEN.finditer(inner, max(0, pos - 6000), pos):
        tag = m.group(1)
        depth, j = 1, m.end()
        for t in re.finditer(r'<%s\b[^>]*>|</%s>' % (tag, tag), inner[m.end():]):
            depth += 1 if not t.group(0).startswith('</') else -1
            if depth == 0:
                j = m.end() + t.end()
                break
        if j > pos:
            best = (m.start(), j)
    return best


def trigger_kind(inner, m, bs, enc, cls, ttext):
    """nbd (NBME phrasing, untouched); term (the button text is line text); label (an appended label after the line's
    text); standalone (no line text before the button)."""
    if 'nbd' in cls.split():
        return 'nbd'
    if 'sp-a' in cls.split():
        return 'term'
    pre = txt(inner[enc[0]:m.start()]) if enc else ''
    post = txt(inner[m.end():bs[0]]) if bs[0] >= m.end() else ''
    if not post and enc and bs[3] <= enc[1]:
        post = txt(re.sub(r'<button\b[^>]*class="sp-pop[^"]*"[^>]*>.*?</button>|<span class="sp-pop-b".*?</span>', '',
                          inner[bs[3]:enc[1]], flags=re.S))
    if not pre and not post:
        return 'standalone'
    if pre and not post and ttext[:1].isupper():
        return 'label'
    return 'term'


def rows(page):
    out = []
    for b in P.briefs(page):
        inner = site_build.unwrap(page[b.start:b.end])
        for m in BTN.finditer(inner):
            cls, pid, ttext = m.group(1), m.group(2), txt(m.group(3))
            bs = body_span(inner, pid)
            if not bs:
                continue
            body = inner[bs[1]:bs[2]]
            kick = txt(''.join(re.findall(r'<span class="sp-k[^"]*">(.*?)</span>', body, re.S)))
            title = txt(''.join(re.findall(r'<span class="sp-ct">(.*?)</span>', body, re.S)))
            rest = re.sub(r'<span class="sp-k[^"]*">.*?</span>|<span class="sp-ct">.*?</span>', '', body, flags=re.S)
            lines = [txt(x) for x in re.findall(r'<span class="sp-l[^"]*">(.*?)</span>', rest, re.S)] or [txt(rest)]
            enc = enclosing(inner, m.start())
            line = ''
            if enc:
                seg = inner[enc[0]:bs[0]] + inner[bs[3]:enc[1]] if enc[0] <= bs[0] and bs[3] <= enc[1] else inner[enc[0]:enc[1]]
                seg = re.sub(r'<span class="sp-pop-b".*?</span>\s*(?=</(?:li|td|th|p|dd|dt|div)>)', '', seg, flags=re.S)
                line = txt(seg)[:1200]
            tw = stem(words(ttext))
            cw = stem(words(title + ' ' + kick + ' ' + (lines[0] if lines else '')))
            kind = trigger_kind(inner, m, bs, enc, cls, ttext)
            out.append({'brief': b.id, 'pop': pid, 'cls': cls, 'kind': kind, 'trigger': ttext, 'line': line, 'kicker': kick,
                        'title': title, 'body': ' | '.join(l for l in lines if l)[:400], 'overlap': len(tw & cw)})
    return out


def survey(page_path, md, js):
    page = P.read_page(page_path)
    rs = rows(page)
    json.dump(rs, open(js, 'w'), indent=1)
    with open(md, 'w') as f:
        f.write('# s170 anchor survey: %d hovers, %d with no shared word\n\n' % (len(rs), sum(1 for r in rs if not r['overlap'])))
        cur = None
        for r in rs:
            if r['brief'] != cur:
                cur = r['brief']
                f.write('\n## %s\n\n' % cur)
            f.write('- `%s` %s ov %d | trigger **%s** | line: %s | kicker: %s | title: %s | body: %s\n' % (
                r['pop'], r['kind'], r['overlap'], r['trigger'], r['line'], r['kicker'],
                r['title'], r['body'][:200]))
    print('survey: %d hovers in %d briefs; overlap 0: %d' % (len(rs), len({r['brief'] for r in rs}),
                                                             sum(1 for r in rs if not r['overlap'])))


def text_positions(seg):
    """map of visible-text index -> raw offset, for text outside tags (button text included)."""
    pos, raw = [], []
    i = 0
    for m in re.finditer(r'<[^>]+>|[^<]+', seg):
        if m.group(0).startswith('<'):
            continue
        for k, ch in enumerate(m.group(0)):
            pos.append(m.start() + k)
            raw.append(ch)
    return ''.join(raw), pos


def row_head_term(whole, pos, term):
    """start, end of the first occurrence of term in the plain text of the first cell of the table row around pos
    (outside buttons, card bodies and masks); None when the row, the cell or the term is missing."""
    rs = whole.rfind('<tr', 0, pos)
    re_ = whole.find('</tr>', pos)
    if rs < 0 or re_ < 0 or whole.find('</tr>', rs, pos) >= 0:
        return None
    c = re.compile(r'<(td|th)\b[^>]*>').search(whole, rs, re_)
    if not c:
        return None
    ce = whole.find('</%s>' % c.group(1), c.end(), re_)
    if ce < 0 or c.end() <= pos < ce:
        return None
    cell = whole[c.end():ce]
    skip = [(x.start(), x.end()) for x in re.finditer(
        r'<button\b.*?</button>|<span class="sp-pop-b".*?</span>(?=\s*(?:<|$))|<span class="mask">.*?</span>', cell, re.S)]
    for t in re.finditer(r'(?<=>)[^<]+|^[^<]+', cell):
        k = t.group(0).find(term)
        if k >= 0 and not any(s0 <= t.start() + k < e0 for s0, e0 in skip):
            return c.end() + t.start() + k, c.end() + t.start() + k + len(term)
    return None


def apply(page_path, dec_path, out_path):
    page = site_build.unwrap(P.read_page(page_path))
    dec = json.load(open(dec_path))
    edits, done, miss = [], 0, []
    for b in P.briefs(page):
        whole = page[b.start:b.end]
        for m in BTN.finditer(whole):
            pid = m.group(2)
            d = dec.get(pid)
            if not d or d.get('verdict') == 'fits':
                continue
            open_tag = whole[m.start():m.start() + whole[m.start():].index('>') + 1]
            btext = m.group(3)
            bs = body_span(whole, pid)
            enc = enclosing(whole, m.start())
            if not bs or not enc:
                miss.append(pid + ': no body or line')
                continue
            kind = trigger_kind(whole, m, bs, enc, m.group(1), txt(btext))
            if d.get('label') is True and kind == 'term':
                kind = 'label'
            if kind == 'nbd':
                miss.append(pid + ': NBME phrasing hover, left as is')
                continue
            if kind in ('label', 'standalone') and d['verdict'] == 'own':
                ed = [(m.start(), m.end(), open_tag + d['label'] + '</button>')]
            elif kind == 'standalone' and d['verdict'] == 'move':
                miss.append(pid + ': standalone trigger has no line text to move onto')
                continue
            elif d['verdict'] == 'move' and d.get('cell') == 'row':
                found = row_head_term(whole, m.start(), d['term'])
                if not found:
                    miss.append('%s: term "%s" not in plain text of the first cell of its row' % (pid, d['term']))
                    continue
                a, z = found
                gap = re.match(r'\s*', whole[m.end():bs[0]]).end() if bs[0] >= m.end() and not txt(whole[m.end():bs[0]]) else 0
                keep = btext if kind == 'term' else ''
                ed = [(m.start(), m.end() + gap, keep), (bs[0], bs[3], ''),
                      (a, z, open_tag + whole[a:z] + '</button>' + whole[bs[0]:bs[3]])]
            elif d['verdict'] == 'move':
                seg_s, seg_e = enc[0], m.start()
                after_s, after_e = m.end(), bs[0]
                term = d['term']
                found = None
                for (s0, e0) in ((after_s, after_e), (seg_s, seg_e)):
                    seg = whole[s0:e0]
                    for t in re.finditer(r'(?<=>)[^<]+|^[^<]+', seg):
                        k = t.group(0).find(term)
                        if k >= 0:
                            found = (s0 + t.start() + k, s0 + t.start() + k + len(term))
                            break
                    if found:
                        break
                if not found:
                    miss.append('%s: term "%s" not in plain text of its line' % (pid, term))
                    continue
                a, z = found
                if kind == 'label':
                    body = whole[bs[1]:bs[2]]
                    kick = '' if 'class="sp-k' in body else '<span class="sp-k">' + btext + '</span>'
                    pre_ws = re.search(r'\s*$', whole[:m.start()]).group(0)
                    ed = [(m.start() - len(pre_ws), m.end(), ''), (bs[1], bs[1], kick),
                          (a, z, open_tag + whole[a:z] + '</button>')]
                else:
                    ed = [(m.start(), m.end(), btext), (a, z, open_tag + whole[a:z] + '</button>')]
            elif d['verdict'] == 'icon':
                if kind != 'term':
                    miss.append(pid + ': marker applies to a term trigger only')
                    continue
                tag = re.sub(r'class="[^"]*"', 'class="sp-pop sp-i"', open_tag, count=1)[:-1] + ' aria-label="More information">'
                ed = [(m.start(), m.end(), btext), (bs[0], bs[0], tag + '</button>')]
            elif d['verdict'] == 'own':
                label = d['label']
                ed = [(m.start(), m.end(), btext), (bs[0], bs[0], ' ' + open_tag + label + '</button>')]
            else:
                miss.append(pid + ': unknown verdict')
                continue
            for s, e, r in ed:
                edits.append((b.start + s, b.start + e, r))
            done += 1
    edits.sort(key=lambda x: (x[0], x[1]), reverse=True)
    for s, e, r in edits:
        page = page[:s] + r + page[e:]
    open(out_path, 'w', encoding='utf-8').write(site_build.wrap(page))
    print('apply: %d hovers changed; %d not applied' % (done, len(miss)))
    for x in miss:
        print('  MISS ' + x)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['survey']:
        survey(*a[1:4])
    elif a[:1] == ['apply']:
        apply(*a[1:4])
    else:
        print(__doc__)
