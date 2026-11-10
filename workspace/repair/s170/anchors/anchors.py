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
  With "cell": "row" the trigger moves onto the first occurrence of `term` in the first cell of the same
  table row (the row head); the old trigger text stays as plain text where it was, and the card body stays in place
  (the page finds it by id).
  For a term trigger the term is found in the visible text of the whole line, whole words only, with the trigger's own
  text counted as line text (an occurrence inside the old trigger wins, then the first in reading order), so a move may
  trim or extend the present trigger and may hold whole inline tags; a term inside a mask is refused unless the old
  trigger sat in a mask.
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


def card_ranges(seg):
    """start, end of every hover card body in seg (balanced spans)."""
    out = []
    for m in re.finditer(r'<span class="sp-pop-b"', seg):
        if out and m.start() < out[-1][1]:
            continue
        depth, k = 0, len(seg)
        for t in re.finditer(r'<span\b|</span>', seg[m.start():]):
            depth += 1 if t.group(0) == '<span' else -1
            if depth == 0:
                k = m.start() + t.end()
                break
        out.append((m.start(), k))
    return out


def balance(raw):
    """(unmatched closing tags, unmatched opening tags) of raw, by tag name order."""
    stack, closes = [], []
    for t in re.finditer(r'<(/?)([a-zA-Z0-9]+)\b[^>]*?(/?)>', raw):
        if t.group(3) or t.group(2) in ('br', 'img', 'hr'):
            continue
        if not t.group(1):
            stack.append(t.group(2))
        elif stack and stack[-1] == t.group(2):
            stack.pop()
        else:
            closes.append(t.group(2))
    return closes, stack


def masked_at(block, p):
    """True when offset p of block lies inside a study-mode mask element."""
    for m in re.finditer(r'<(span|b)\b[^>]*\bclass="(?:nm )?mask(?: w5om)?"[^>]*>', block[:p]):
        tag, depth = m.group(1), 1
        for t in re.finditer(r'<%s\b|</%s>' % (tag, tag), block[m.end():p]):
            depth += 1 if not t.group(0).startswith('</') else -1
            if depth == 0:
                break
        if depth > 0:
            return True
    return False



def span_move(whole, pid, term):
    """whole with the trigger of pid re-placed on `term`, found in the visible text of the trigger's own block with the
    trigger's text counted as line text; the term may overlap the old trigger and may hold whole inline tags. Returns
    (new whole, None) or (whole, reason)."""
    m = next((x for x in BTN.finditer(whole) if x.group(2) == pid), None)
    if not m:
        return whole, 'no trigger'
    enc = enclosing(whole, m.start())
    if not enc:
        return whole, 'no line'
    open_tag = whole[m.start():m.start() + whole[m.start():].index('>') + 1]
    block = whole[enc[0]:m.start()] + m.group(3) + whole[m.end():enc[1]]
    skip = card_ranges(block) + [(x.start(), x.end()) for x in re.finditer(r'<button\b.*?</button>', block, re.S)]
    chars, pos = [], []
    for t in re.finditer(r'<[^>]+>|[^<]+', block):
        if t.group(0).startswith('<') or any(a <= t.start() < z for a, z in skip):
            continue
        if chars:
            chars.append('\x00')
            pos.append(-1)
        for k, ch in enumerate(t.group(0)):
            chars.append(ch)
            pos.append(t.start() + k)
    text = ''.join(chars)
    pat = r'(?<![A-Za-z0-9])' + r'[\s\x00]*'.join(re.escape(w) for w in re.split(r'\s+', term.strip())) + r'(?![A-Za-z0-9])'
    t0 = m.start() - enc[0]
    t1 = t0 + len(m.group(3))
    hits = sorted(re.finditer(pat, text), key=lambda h: not (pos[h.start()] < t1 and pos[h.end() - 1] >= t0))
    if not hits:
        return whole, 'term "%s" not in the visible text of its line' % term
    was_masked = masked_at(block, t0)
    why = None
    for hit in hits:
        a, z = pos[hit.start()], pos[hit.end() - 1] + 1
        if masked_at(block, a) and not was_masked:
            why = 'term "%s" sits inside a mask' % term
            continue
        ok = True
        for _ in range(4):
            closes, opens = balance(block[a:z])
            if not closes and not opens:
                break
            pre = re.search(r'<([a-zA-Z0-9]+)\b[^>]*>$', block[:a])
            post = re.match(r'</([a-zA-Z0-9]+)>', block[z:])
            if closes and pre and pre.group(1) == closes[0] and 'mask' not in pre.group(0):
                a = pre.start()
            elif opens and post and post.group(1) == opens[-1]:
                z += post.end()
            else:
                ok = False
                break
        inner = block[a:z]
        if not ok or balance(inner) != ([], []):
            why = 'term "%s" cuts through a tag' % term
            continue
        if any(a < e and s0 < z for s0, e in skip) or 'mask"' in inner or 'class="mask' in inner:
            why = 'term "%s" crosses a card, a button or a mask' % term
            continue
        break
    else:
        return whole, why
    block = block[:a] + open_tag + inner + '</button>' + block[z:]
    return whole[:enc[0]] + block + whole[enc[1]:], None


def apply(page_path, dec_path, out_path):
    page = site_build.unwrap(P.read_page(page_path))
    dec = json.load(open(dec_path))
    sp_a = {x.group(2) for x in BTN.finditer(page) if 'sp-a' in x.group(1).split()}
    spans, span_miss = {k: v for k, v in dec.items() if v.get('verdict') == 'move' and not v.get('cell') and k in sp_a}, []
    dec = {k: v for k, v in dec.items() if k not in spans}
    for b in reversed(list(P.briefs(page))):
        whole = page[b.start:b.end]
        for pid, d in spans.items():
            if 'aria-controls="%s"' % pid in whole:
                whole, why = span_move(whole, pid, d['term'])
                if why:
                    span_miss.append('%s: %s' % (pid, why))
        page = page[:b.start] + whole + page[b.end:]
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
                if kind != 'term':
                    miss.append(pid + ': a row move applies to a term trigger only')
                    continue
                ed = [(m.start(), m.end(), btext), (a, z, open_tag + whole[a:z] + '</button>')]
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
    done += len(spans) - len(span_miss)
    miss += span_miss
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
