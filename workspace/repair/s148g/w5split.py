#!/usr/bin/env python3
"""s148g First step split on the page (Jonathan 2026-10-20; SITE_BODY_GLANCE item 2): rewrite one 5a First step band
of a brief into one row group per order, each spanning only its own results, from a pairing (one order number per
finding). The markup is exactly what tools/spine/outline_render.w5a writes for a band with "pair", so later builds from
an outline give the same bytes. Text, masks and hovers are carried byte for byte; only the grouping changes.

  split(brief_html, band, pair) -> (old_fragment, new_fragment)
      band: 0-based index of the .w5b inside the brief's .w5t.first; pair: [order number per finding]
"""
import re

TAG = re.compile(r'<(/?)(div|span)\b[^>]*>')


def element(h, i):
    """End offset of the div or span element that opens at h[i] (balanced on its own tag name)."""
    m = TAG.match(h, i)
    assert m and not m.group(1), h[i:i + 40]
    name, depth = m.group(2), 0
    for t in TAG.finditer(h, i):
        if t.group(2) != name:
            continue
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return t.end()
    raise ValueError('unbalanced <%s> at %d' % (name, i))


def children(h, a, b):
    """Top-level elements between a and b: [(start, end)]; text between them must be empty."""
    out, i = [], a
    while i < b:
        assert h[i] == '<', 'text between elements: %r' % h[i:i + 40]
        e = element(h, i)
        out.append((i, e)); i = e
    return out


def inner(h, a, b):
    return h[h.index('>', a) + 1:h.rindex('<', a, b)]


def parse(h, at):
    """Parse the .w5b at offset `at` and its .w5f: (end, clue, orders, findings) with raw inner html."""
    e = element(h, at)
    kids = children(h, h.index('>', at) + 1, h.rindex('<', at, e))
    assert len(kids) == 3 and h.startswith('<div class="w5c">', kids[0][0]) and h.startswith('<span class="w5ar"', kids[1][0]) \
        and h.startswith('<div class="w5o">', kids[2][0]), 'unexpected .w5b layout'
    clue = inner(h, *kids[0])
    om = children(h, h.index('>', kids[2][0]) + 1, h.rindex('<', kids[2][0], kids[2][1]))
    assert len(om) == 1 and h.startswith('<span class="mask w5om">', om[0][0])
    orders = [inner(h, a, b) for a, b in children(h, h.index('>', om[0][0]) + 1, h.rindex('<', om[0][0], om[0][1]))]
    findings, end = [], e
    if h.startswith('<div class="w5f">', e):
        end = element(h, e)
        rows = children(h, h.index('>', e) + 1, h.rindex('<', e, end))
        assert len(rows) % 3 == 0
        for k in range(0, len(rows), 3):
            fd, an, mn = rows[k:k + 3]
            assert h.startswith('<div class="w5fd', fd[0]) and h.startswith('<span class="w5an', an[0]) and h.startswith('<div class="w5m', mn[0])
            t = children(h, h.index('>', fd[0]) + 1, h.rindex('<', fd[0], fd[1]))
            assert h.startswith('<span class="t" lang="en">', t[0][0]) and h[t[1][0]:t[1][1]] == '<span class="ld" aria-hidden="true"></span>'
            m = inner(h, *mn)
            mean = None
            if m:
                mm = children(h, h.index('>', mn[0]) + 1, h.rindex('<', mn[0], mn[1]))
                assert len(mm) == 1 and h.startswith('<span class="mask">', mm[0][0])
                mean = inner(h, *mm[0])
            findings.append((inner(h, *t[0]), mean))
    return end, clue, orders, findings


def render(clue, orders, findings, pair=None):
    """The band as tools/spine/outline_render.w5a writes it (r = identity)."""
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'spine'))
    from outline_render import split_band
    band = [clue, orders, findings] + ([pair] if pair else [])
    out = []
    for c, os_, fs in split_band(band):
        head = '<div class="w5c">%s</div>' % c if c is not None else ''
        out.append('<div class="w5b%s">%s<span class="w5ar" aria-hidden="true">&rarr;</span>'
                   '<div class="w5o"><span class="mask w5om">%s</span></div></div>'
                   % ('' if c is not None else ' w5k', head, ''.join('<span class="w5ol">%s</span>' % o for o in os_)))
        if fs:
            out.append('<div class="w5f">')
            n = len(fs)
            for k, (fd, mean) in enumerate(fs):
                cls = (' f1' if k == 0 else '') + (' fl' if k == n - 1 else '') + ('' if mean else ' nom')
                out.append('<div class="w5fd%s"><span class="t" lang="en">%s</span><span class="ld" aria-hidden="true"></span></div>'
                           '<span class="w5an%s" aria-hidden="true"></span><div class="w5m%s">%s</div>'
                           % (cls, fd, cls, cls, ('<span class="mask">%s</span>' % mean) if mean else ''))
            out.append('</div>')
    return ''.join(out)


def split(h, band, pair):
    i = h.index('<div class="w5t first">')
    end_t = element(h, i)
    starts = [m.start() for m in re.finditer(r'<div class="w5b[ "]', h[:end_t])]
    starts = [s for s in starts if s > i]
    at = starts[band]
    end, clue, orders, findings = parse(h, at)
    old = h[at:end]
    assert render(clue, orders, findings) == old, 'round trip differs: the band is not in the outline_render format'
    new = render(clue, orders, findings, pair)
    # the same text runs, apart from the decorative arrow each new row group carries (aria-hidden)
    ar = '<span class="w5ar" aria-hidden="true">&rarr;</span>'
    runs = lambda x: sorted(re.findall(r'>([^<]+)<', x.replace(ar, '')))  # noqa: E731
    assert runs(old) == runs(new), 'text changed in the split'
    return old, new
