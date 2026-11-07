"""s167c N16 (D-20261107-9): one shared axis per window timeline (figure.lcw), bars stacked per row.

A figure whose rows all carry the same axis (div.rax) keeps one copy, in div.wax before the rows; the per-row copies go.
Rails (bars and ticks) stay per row, so the ticks run down every row as gridlines. Figures whose rows differ, or where a
row has no axis, are left as they are.
"""
import re
RAX = re.compile(r'<div class="rax"[^>]*>.*?</div>', re.S)


def transform(inner):
    edits, st = [], {'shared': 0, 'skipped': 0, 'rows_axis_removed': 0}
    for f in re.finditer(r'<figure class="([^"]*)"', inner):
        if 'lcw' not in f.group(1).split():
            continue
        end = inner.find('</figure>', f.start())
        fig = inner[f.start():end]
        rax = list(RAX.finditer(fig))
        rows = len(re.findall(r'<li class="wr\b', fig))
        if not rax or rows < 2 or len(rax) != rows or len({m.group(0) for m in rax}) != 1:
            st['skipped'] += 1
            continue
        ol = fig.find('<ol class="wrows"')
        if ol < 0:
            st['skipped'] += 1
            continue
        base = f.start()
        edits.append((base + ol, base + ol, '<div class="wax" aria-hidden="true">' + rax[0].group(0) + '</div>'))
        edits += [(base + m.start(), base + m.end(), '') for m in rax]
        st['shared'] += 1
        st['rows_axis_removed'] += rows
    edits.sort(key=lambda x: (x[0], x[1]))
    out, pos = [], 0
    for s, e, new in edits:
        out.append(inner[pos:s]); out.append(new); pos = e
    out.append(inner[pos:])
    return ''.join(out), st
