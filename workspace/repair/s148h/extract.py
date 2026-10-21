#!/usr/bin/env python3
"""s148h lead tool: one brief's practice items and tables as compact text, for writing the per-choice reasons without
reading the brief whole (runbook section 7).

  python3 repair/s148h/extract.py <brief id> [--page index.html]

Prints every table (one row per line, cells joined by ' | ', hover text left out) and every bank item:
id, type, lead-in, stem, key, d1, d2, explanation, and any reasons the item already carries.
"""
import html
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
import pagelib as P  # noqa: E402

HOV = re.compile(r'<span class="(?:hv|hov|hover)[^"]*"[^>]*>.*?</span>', re.S)


def drop_pops(x):
    """remove each hover body (span.sp-pop-b, balanced on span)"""
    while True:
        m = re.search(r'<span class="sp-pop-b"', x)
        if not m:
            return x
        depth = 0
        for t in re.finditer(r'<(/?)span\b[^>]*>', x[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                x = x[:m.start()] + ' ' + x[m.start() + t.end():]
                break
        else:
            return x


def plain(x):
    x = drop_pops(x)
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', x))).strip()


def attr(a, k):
    m = re.search(r'\b' + k + r'="([^"]*)"', a)
    return html.unescape(m.group(1)) if m else ''


def items(t):
    i = t.find('<ol class="bank')
    out = []
    for m in re.finditer(r'<li([^>]*data-item-id[^>]*)>(.*?)</li>', t[i:], re.S):
        a, body = m.group(1), m.group(2)
        parts = re.split(r'\s*(?:&rarr;|\u2192)\s*', body, maxsplit=2)
        stem = plain(parts[0]); key = plain(parts[1]) if len(parts) > 1 else '?'
        expl = plain(parts[2]) if len(parts) > 2 else ''
        out.append(dict(id=attr(a, 'data-item-id'), type=attr(a, 'data-type'), lead=attr(a, 'data-lead-in'),
                        stem=stem, key=key, d1=attr(a, 'data-d1'), d2=attr(a, 'data-d2'), expl=expl,
                        why=[attr(a, 'data-key-why'), attr(a, 'data-d1-why'), attr(a, 'data-d2-why')]))
    return out


def tables(t):
    out = []
    for m in re.finditer(r'<table[^>]*>.*?</table>', t, re.S):
        rows = []
        for r in re.findall(r'<tr[^>]*>(.*?)</tr>', m.group(0), re.S):
            cells = [plain(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)]
            if any(cells):
                rows.append(' | '.join(cells))
        out.append(rows)
    return out


def main(argv):
    bid = argv[1]
    page = argv[argv.index('--page') + 1] if '--page' in argv else os.path.join(WS, 'index.html')
    pg = P.read_page(page)
    b = P.brief_by_id(pg, bid)
    t = pg[b.start:b.end]
    print('# %s' % bid)
    for n, rows in enumerate(tables(t), 1):
        print('## T%d' % n)
        for r in rows:
            print('  ' + r)
    print('## items')
    for k, it in enumerate(items(t), 1):
        print('%d %s %s [%s]' % (k, it['id'][:10], it['type'], it['lead']))
        print('  S: ' + it['stem'])
        print('  K: %s | D1: %s | D2: %s' % (it['key'], it['d1'], it['d2']))
        print('  E: ' + it['expl'])
        if any(it['why']):
            print('  W: ' + ' || '.join(it['why']))


if __name__ == '__main__':
    main(sys.argv)
