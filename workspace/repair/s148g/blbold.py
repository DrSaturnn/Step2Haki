#!/usr/bin/env python3
"""s148g bold key words in bottom lines (Jonathan 2026-10-20: "still bolding the key words/criteria"; bold only, no
wording change). Library plus a dump tool.

  python3 repair/s148g/blbold.py dump [brief ...]     print each bottom line's text, one block per line, hovers removed

Spec per brief (repair/s148g/data/bold_bl.json): a list of phrases. A phrase is plain text as it stands in the page source (entities as
written, e.g. &uarr;), lying inside one text run of the bottom line (no tag inside it), outside hover cards and hover
labels, and not already bold; it must occur exactly once there. "[[...]]" marks the part to bold when more context is
needed to make the phrase unique; with no marks the whole phrase is bolded.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import read_page, briefs  # noqa: E402

OPEN = '<div class="dp"><span class="lbl">Bottom line</span>'
TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>')
VOID = {'br', 'img', 'hr', 'wbr', 'input'}


def region(html):
    """(start, end) of the bottom line block inside one brief's html (the .dp div, balanced), or None."""
    i = html.find(OPEN)
    if i < 0:
        return None
    if html.find(OPEN, i + 1) >= 0:
        raise ValueError('two bottom lines')
    depth = 0
    for m in TAG.finditer(html, i):
        name = m.group(2).lower()
        if name != 'div':
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return i, m.end()
    raise ValueError('unbalanced bottom line')


def runs(h):
    """Text runs of h that may take bold: [(start, end)] outside tags, hover bodies, hover labels and existing bold."""
    out, stack, pos = [], [], 0
    for m in TAG.finditer(h):
        if m.start() > pos and not any(blocked for _, blocked in stack):
            out.append((pos, m.start()))
        pos = m.end()
        name, closing, selfc = m.group(2).lower(), m.group(1), m.group(3)
        if name in VOID or selfc:
            continue
        if closing:
            while stack:
                n, _ = stack.pop()
                if n == name:
                    break
        else:
            t = m.group(0)
            blocked = ('sp-pop-b' in t or 'class="sp-pop' in t or name in ('b', 'strong', 'button', 'script', 'style')
                       or 'aria-hidden="true"' in t or 'class="op ' in t)
            stack.append((name, blocked))
    if pos < len(h) and not any(b for _, b in stack):
        out.append((pos, len(h)))
    return out


def apply(h, phrases):
    """Return h with each phrase's marked part wrapped in <b>; raises on a phrase not found exactly once."""
    spans = []
    for p in phrases:
        if '[[' in p:
            pre, rest = p.split('[[', 1)
            mid, post = rest.split(']]', 1)
        else:
            pre, mid, post = '', p, ''
        whole = pre + mid + post
        hits = []
        for a, b in runs(h):
            k = h.find(whole, a)
            while 0 <= k and k + len(whole) <= b:
                hits.append(k)
                k = h.find(whole, k + 1)
        if len(hits) != 1:
            raise ValueError('phrase %r found %d times in a boldable run' % (p, len(hits)))
        s = hits[0] + len(pre)
        spans.append((s, s + len(mid)))
    spans.sort()
    for (a, b), (c, d) in zip(spans, spans[1:]):
        if c < b:
            raise ValueError('overlapping bold phrases at %d' % c)
    for a, b in reversed(spans):
        h = h[:a] + '<b>' + h[a:b] + '</b>' + h[b:]
    return h


def unbold_equal(old, new):
    """The bold-only check: removing the added <b> tags gives back the old text exactly."""
    return new.replace('<b>', '').replace('</b>', '') == old.replace('<b>', '').replace('</b>', '') and \
        len(re.findall(r'<b>', new)) - len(re.findall(r'<b>', old)) == len(re.findall(r'</b>', new)) - len(re.findall(r'</b>', old))


def plain(h):
    """Readable view: boldable runs as text, existing bold as **x**, hover labels as {x}, hover bodies dropped."""
    out, stack, pos = [], [], 0
    def kind():
        for n, k in reversed(stack):
            if k:
                return k
        return ''
    for m in TAG.finditer(h):
        txt = h[pos:m.start()]
        k = kind()
        if txt and k != 'hide':
            out.append({'': txt, 'b': '**%s**' % txt, 'lab': '{%s}' % txt}.get(k, txt))
        pos = m.end()
        name, closing, selfc, t = m.group(2).lower(), m.group(1), m.group(3), m.group(0)
        if name in VOID or selfc:
            continue
        if closing:
            if name in ('li', 'p'):
                out.append('\n')
            while stack:
                n, _ = stack.pop()
                if n == name:
                    break
            continue
        if 'class="op op-p"' in t:
            out.append(' + ')
        elif 'class="op op-a"' in t:
            out.append(' -> ')
        k = 'hide' if 'sp-pop-b' in t else ('lab' if 'class="sp-pop' in t or name == 'button' else ('b' if name in ('b', 'strong') else ''))
        stack.append((name, k))
    out.append(h[pos:])
    return re.sub(r'[ \t]+', ' ', ''.join(out))


def main(argv):
    if not argv or argv[0] != 'dump':
        sys.exit(__doc__)
    s = read_page(os.path.join(WS, 'index.html'))
    want = set(argv[1:])
    for b in briefs(s):
        if want and b.id not in want:
            continue
        h = s[b.start:b.end]
        r = region(h)
        if not r:
            continue
        print('== %s' % b.id)
        print(plain(h[r[0] + len(OPEN):r[1]]).strip())


if __name__ == '__main__':
    main(sys.argv[1:])
