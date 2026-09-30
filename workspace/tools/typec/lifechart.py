#!/usr/bin/env python3
"""lifechart.py: HTML builders for the psych charts styled by tools/typec/typec.css (.lcb duration bands, .lc life chart).

Every label is HTML text (maskable in study mode, readable by screen readers); geometry is inline CSS variables in percent
of the plot, so charts scale with the phone width. Colors carry one meaning on every brief (see typec.css)."""
from html import escape as E


def duration_bands(title, ticks, bands, only=None, scale_note='not to scale', key=None):
    """ticks: labels for the gates, top to bottom (len(bands) of them); bands: dicts {name, rule, c: 1|2|3, open: bool}.
    only: (start band index, key text) draws the hatched 'a delusion only' strip from that band down."""
    rows, r, band_rows = [], 1, []
    for i, b in enumerate(bands):
        rows.append(f'<b class="tk" style="grid-row:{r}">{E(ticks[i])}</b><i class="gate" style="grid-row:{r}"></i>')
        r += 1
        cls = 'band' + (' deep' if b['c'] == 3 else '') + (' open' if b.get('open') else '')
        rows.append(f'<i class="spine" style="grid-row:{r}"></i><div class="{cls}" style="grid-row:{r};--c:var(--psy{b["c"]})">'
                    f'<span class="nm mask">{b["name"]}</span><span class="rl">{b["rule"]}</span></div>')
        band_rows.append(r)
        r += 1
    if only:
        s = band_rows[only[0]]
        rows.append(f'<i class="only" style="grid-row:{s} / {band_rows[-1] + 1}"></i>')
    keys = ''.join(f'<span><i class="{k}"></i>{t}</span>' for k, t in (key or []))
    return (f'<figure class="lcb" role="img" aria-label="{E(title)}"><div class="ttl"><span>{title}</span><small>{E(scale_note)}</small></div>'
            f'<div class="grid">{"".join(rows)}</div>' + (f'<div class="lc-key">{keys}</div>' if keys else '') + '</figure>')


def life_chart(title, eps, axis='Time', height=220, note='', guides=(), brackets=(), dangers=(), key=None, tag=''):
    """eps: dicts {kind: lo|hi|ps, t, h (percent), f (width fraction of the half, lo/hi), label, alone, opt}."""
    parts = [f'<i class="axis"><span>{E(axis)}</span></i><i class="base"></i>']
    parts += [f'<i class="guide" style="--t:{g}%"></i>' for g in guides]
    for e in eps:
        st = f'--t:{e["t"]}%;--h:{e["h"]}%' + (f';--f:{e["f"]}' if 'f' in e else '')
        if e['kind'] == 'ps':
            parts.append(f'<i class="ps{" alone" if e.get("alone") else ""}" style="{st}"></i>')
        else:
            parts.append(f'<div class="ep {e["kind"]}{" opt" if e.get("opt") else ""}" style="{st}">{e.get("label", "")}</div>')
    parts += [f'<div class="brk" style="--t:{t}%;--h:{h}%">{txt}</div>' for t, h, txt in brackets]
    parts += [f'<i class="dng" style="{pos}"></i>' for pos in dangers]
    keys = ''.join(f'<span><i class="{k}"></i>{t}</span>' for k, t in (key or []))
    return (f'<figure class="lc" role="img" aria-label="{E(title)}"><div class="ttl"><span>{title}</span>'
            + (f'<small>{E(tag)}</small>' if tag else '') + '</div>'
            '<div class="heads"><span>Low mood</span><span>Psychosis</span><span>High mood</span></div>'
            f'<div class="plot" style="--ph:{height}px">{"".join(parts)}</div>'
            + (f'<div class="lc-key">{keys}</div>' if keys else '') + (f'<p class="note">{note}</p>' if note else '') + '</figure>')
