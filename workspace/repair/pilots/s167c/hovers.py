"""s167c N7 (D-20261107-9): hover triggers A+F, by offset splicing (no DOM re-serialization).

A. An appended label trigger (a capitalized label after the line's text, e.g. "In practice", "Why", "Maneuvers") moves
   onto the term in the line: the label's own words where the line contains them, else the line's lead term. The old
   label moves, unchanged, to the start of its card as a kicker (span.sp-k), so the brief's text order is unchanged
   (prose_lint.text_key equal; markup-only change). A kicker equal to the anchor or the card title is kept hidden.
F. A hover whose body (title excluded) is under 8 words becomes a visible line: the button becomes span.sp-k (or plain
   text for an in-sentence trigger) and the card becomes span.sp-vl, shown.
Untouched: NBME phrasing hovers (.nbd), in-sentence triggers (lowercase label) and standalone triggers (no text before
them in the line), apart from F.
"""
import re

VOID = {'br', 'img', 'input', 'hr', 'meta', 'wbr', 'link', 'col', 'source'}
TOK = re.compile(r'<!--.*?-->|<[^>]+>|[^<]+', re.S)
STOP = {'a', 'an', 'the', 'if', 'when', 'choose', 'then', 'and', 'or', 'give', 'start', 'with', 'in', 'on', 'for', 'to'}
SEP = re.compile(r'[;:,.]\s|\s\(|\s&rarr;|\s→|\s-\s')
SHORT = 8
WEAK = {'such', 'where', 'that', 'which', 'who', 'when', 'before', 'after', 'at', 'in', 'on', 'for', 'to', 'from',
        'with', 'by', 'into', 'once', 'if', 'and', 'or', 'but', 'is', 'are', 'was', 'can', 'may', 'until', 'than', 'as',
        'about', 'over', 'under', 'within', 'without', 'during', 'because', 'so', 'the', 'a', 'an', 'not', 'no'}


class N:
    __slots__ = ('tag', 's', 'e', 'os', 'oe', 'cs', 'kids', 'par', 'attrs', 'text')

    def __init__(self, tag, s, oe, par, attrs='', text=None):
        self.tag, self.s, self.oe, self.par, self.attrs, self.text = tag, s, oe, par, attrs, text
        self.e = oe; self.cs = None; self.kids = []

    def cls(self):
        m = re.search(r'\bclass="([^"]*)"', self.attrs or '')
        return m.group(1).split() if m else []


def tree(html):
    root = N('#root', 0, 0, None)
    cur = root
    for m in TOK.finditer(html):
        t, s, e = m.group(0), m.start(), m.end()
        if t.startswith('<!--'):
            continue
        if t.startswith('</'):
            name = t[2:-1].strip().lower()
            n = cur
            while n is not root and n.tag != name:
                n = n.par
            if n is root:
                continue
            n.cs, n.e = s, e
            cur = n.par
        elif t.startswith('<'):
            name = re.match(r'<\s*([a-zA-Z0-9]+)', t).group(1).lower()
            n = N(name, s, e, cur, t)
            cur.kids.append(n)
            if name not in VOID and not t.endswith('/>'):
                cur = n
            else:
                n.cs = n.e = e
        else:
            cur.kids.append(N('#text', s, e, cur, text=t))
    return root


def walk(n):
    for k in n.kids:
        yield k
        yield from walk(k)


def txt(n, html):
    if n.tag == '#text':
        return n.text
    return re.sub(r'<[^>]+>', '', html[n.oe:n.cs]) if n.cs is not None else ''


def words(s):
    return re.sub(r'&[a-z#0-9]+;', ' ', s).split()


def lead_span(t, base):
    """(start, end) offsets of the lead term inside text node t (offset base), or None."""
    m = re.match(r'\s*', t)
    i = m.end()
    rest = t[i:]
    stop = SEP.search(rest)
    seg = rest[:stop.start()] if stop else rest.rstrip()
    ws = list(re.finditer(r'\S+', seg))
    while ws and ws[0].group(0).lower().strip('(') in STOP:
        ws.pop(0)
    if not ws:
        return None
    cut = next((k for k, w in enumerate(ws) if k >= 1 and w.group(0).lower() in WEAK), len(ws))
    ws = ws[:min(cut, 4)]
    s, e = ws[0].start(), ws[-1].end()
    # keep trailing punctuation inside the anchor when the next char is not a space (text_key stays equal)
    while e < len(seg) and not seg[e].isspace():
        e += 1
    if not re.search(r'[A-Za-z0-9]', seg[s:e]):
        return None
    return base + i + s, base + i + e


def anchor(btn, label, html):
    """Find (start, end) to wrap: the label's words inside the line, else the line's lead term."""
    levels = [btn]
    p = btn.par
    if p is not None and p.tag in ('span', 'b', 's', 'em', 'strong') and 'sp-pop-b' not in p.cls():
        levels.append(p)
    lab = re.escape(label.strip())
    for lv in levels:
        sibs = lv.par.kids[:lv.par.kids.index(lv)]
        # 1. the label's own words in a text node of the line
        for n in sibs:
            for t in ([n] if n.tag == '#text' else [x for x in walk(n) if x.tag == '#text']):
                if any(a.tag in ('button',) or 'sp-pop-b' in a.cls() for a in ancestors(t, lv.par)):
                    continue
                m = re.search(r'(?<![\w-])' + lab + r'(?![\w-])', t.text, re.I)
                if m:
                    return t.s + m.start(), t.s + m.end(), 'label'
        # 2. the line's lead term: the first usable text in document order
        for n in sibs:
            if n.tag == '#text':
                sp = lead_span(n.text, n.s)
                if sp:
                    return sp[0], sp[1], 'lead'
                continue
            if n.tag in ('button', 'br') or 'sp-pop-b' in n.cls() or 'aka' in n.cls():
                continue
            for t in [x for x in walk(n) if x.tag == '#text']:
                if any(a.tag == 'button' or 'sp-pop-b' in a.cls() for a in ancestors(t, n.par)):
                    continue
                sp = lead_span(t.text, t.s)
                if sp:
                    return sp[0], sp[1], 'lead'
                break
    return None


def ancestors(n, stop):
    a = n.par
    while a is not None and a is not stop:
        yield a
        a = a.par


def transform(inner):
    """-> (new_inner, stats, notes)."""
    root = tree(inner)
    edits, st, notes = [], {'A_label': 0, 'A_lead': 0, 'A_none': 0, 'F_block': 0, 'F_inline': 0, 'kept': 0, 'nbd': 0}, []
    byid = {}
    for n in walk(root):
        m = re.search(r'\bid="([^"]+)"', n.attrs or '')
        if m and n.tag != '#text':
            byid[m.group(1)] = n
    for b in [n for n in walk(root) if n.tag == 'button' and 'sp-pop' in n.cls()]:
        if 'nbd' in b.cls():
            st['nbd'] += 1
            continue
        cid = re.search(r'aria-controls="([^"]+)"', b.attrs).group(1)
        card = byid.get(cid)
        if card is None or card.cs is None:
            st['kept'] += 1
            continue
        label = txt(b, inner).strip()
        body = txt(card, inner)
        ct = next((k for k in card.kids if 'sp-ct' in k.cls()), None)
        title = txt(ct, inner).strip() if ct else ''
        bw = len(words(body)) - len(words(title))
        sibs = b.par.kids[:b.par.kids.index(b)]
        has_prev = any((n.tag == '#text' and n.text.strip()) or (n.tag != '#text' and 'sp-pop-b' not in n.cls() and txt(n, inner).strip()) for n in sibs)
        appended = has_prev and bool(re.match(r'[\(A-Z0-9]', label))
        nxt = card.par.kids.index(card) if card.par is b.par else -1
        adjacent = nxt == b.par.kids.index(b) + 1
        if bw < SHORT and adjacent:
            open_t = inner[card.s:card.oe]
            new_open = re.sub(r'\s+hidden\b', '', open_t)
            new_open = re.sub(r'\s+id="[^"]*"', '', new_open)
            if appended or not has_prev:
                edits += [(b.s, b.oe, '<span class="sp-k">'), (b.cs, b.e, '</span>'),
                          (card.s, card.oe, new_open.replace('class="sp-pop-b"', 'class="sp-vl"'))]
                st['F_block'] += 1
            else:
                edits += [(b.s, b.oe, '<span class="sp-t">'), (b.cs, b.e, '</span>'),
                          (card.s, card.oe, new_open.replace('class="sp-pop-b"', 'class="sp-vl sp-in"'))]
                st['F_inline'] += 1
            notes.append(('F', label, title, body.strip()[:90]))
            continue
        if not appended or not adjacent:
            st['kept'] += 1
            continue
        a = anchor(b, label, inner)
        if a is None:
            st['A_none'] += 1
            notes.append(('A-none', label, title, ''))
            continue
        s, e, how = a
        st['A_' + how] += 1
        term = re.sub(r'<[^>]+>', '', inner[s:e])
        dup = label.lower() in (term.lower(), title.lower())
        kick = '<span class="sp-k%s">' % (' dup' if dup else '')
        new_btn_open = inner[b.s:b.oe].replace('class="sp-pop', 'class="sp-pop sp-a', 1)
        edits += [(s, s, new_btn_open), (e, e, '</button>'), (b.s, b.e, ''),
                  (card.oe, card.oe, kick + inner[b.oe:b.cs] + '</span>')]
        notes.append(('A-' + how, label, term, title))
    edits.sort(key=lambda x: (x[0], x[1]))
    out, pos = [], 0
    for s, e, new in edits:
        if s < pos:
            raise ValueError('overlapping edits at %d' % s)
        out.append(inner[pos:s]); out.append(new); pos = e
    out.append(inner[pos:])
    return ''.join(out), st, notes
