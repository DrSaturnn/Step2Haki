#!/usr/bin/env python3
"""lifechart.py: the psych chart builder for the AxBx study page (styles: tools/typec/typec.css, section "Psych charts v3").

Chart types, one visual language (time runs down in v3 charts, left to right in the v4 rows; periwinkle = low mood, apricot = high mood, teal = psychosis and
deepens as the illness lasts longer, hatched teal = a delusion only, an outlined psychosis segment = psychosis with no mood
episode, red = danger):

  duration_bands()  Step "time it": a ruler with gates; each band is the diagnosis that owns that window; optional
                    gate notes ("still ill: moves down"), a hatched delusion-only strip, case pins (the NBME patients
                    placed on the ruler) and an inset (e.g. what the 6 months of schizophrenia may include).
  mood_multiples()  Step "check it against mood": small multiples on one time axis. The builder COMPUTES from the drawn
                    geometry which psychosis falls outside mood episodes (outlined automatically) and the mood share of
                    the illness (the meter), and refuses a panel whose picture contradicts its rule.
  window_rows()     v4, horizontal: one row per diagnosis on one shared axis; the bar is the window the diagnosis owns,
                    with its requirements beside it (needs, mood episodes, cues). Bars must end on a tick.
  mood_tracks()     v4, horizontal: a Mood lane over a Psychosis lane per diagnosis; same geometry checks as mood_multiples().
  workup_path()     v4: an ordered workup on a vertical line with dots; tests done together sit in one shaded tile.
  threshold_ruler() Minimum-duration clocks on a log time ruler (4 days ... 2 years), labels de-collided with leaders.

Every label is HTML text: study mode masks the names (class "mask"), screen readers read it, and phones wrap it.
Run this file to self-test (python3 tools/typec/lifechart.py)."""
import math
from html import escape as E

KEYS = {'lo': ('k-lo', 'Low mood'), 'hi': ('k-hi', 'High mood'), 'ps': ('k-ps', 'Psychosis'), 'free': ('k-free', 'Psychosis with no mood episode'),
        'only': ('k-only', 'A delusion only'), 'dng': ('k-dng', 'Hospitalized'), 'pin': ('k-pin', 'NBME question'),
        'w': ('k-w', 'Wider bar: more severe'), 'sub': ('k-sub', 'Below episode criteria'),
        'opt': ('k-opt', 'Common, not required'), 'mild': ('k-mild', 'Hypomania: milder')}


class ChartError(ValueError):
    pass


def key(*names, extra=()):
    items = [KEYS[n] for n in names] + list(extra)
    return '<div class="lc-key">' + ''.join(f'<span><i class="{k}"></i>{t}</span>' for k, t in items) + '</div>'


def _title(title, step, small=''):
    st = f'<b class="step">{E(str(step))}</b>' if step else ''
    return f'<div class="ttl"><span>{st}{title}</span>' + (f'<small>{E(small)}</small>' if small else '') + '</div>'


# ---------------------------------------------------------------- duration bands
def duration_bands(title, ticks, bands, step=None, only=None, pins=(), gate_notes=None, inset=None, keys=('only',), cases=()):
    """ticks: gate labels top to bottom, one per band. bands: {name, rule, c: 1|2|3, open}. only: index of the first band the
    delusion-only strip covers. pins: (label, band index, where 'top'|'mid'|'end'|'gate-after', lane 'band'|'only').
    gate_notes: {gate index: text} written on that gate line. inset: (band index, [(label, flex, kind)]).
    cases: [(pin label, text)] explained under the key."""
    if len(ticks) != len(bands):
        raise ChartError('one gate label per band')
    rows, r, brow = [], 1, []
    for i, b in enumerate(bands):
        note = (gate_notes or {}).get(i)
        rows.append(f'<b class="tk" style="grid-row:{r}">{E(ticks[i])}</b><i class="gate" style="grid-row:{r}"></i>'
                    + (f'<em class="gnote" style="grid-row:{r}">{note}</em>' if note else ''))
        r += 1
        cls = 'band' + (' deep' if b['c'] == 3 else '') + (' open' if b.get('open') else '')
        ins = ''
        if inset and inset[0] == i:
            segs = ''.join(f'<span class="{k}" style="flex:{f}">{lab}</span>' for lab, f, k in inset[1])
            ins = f'<span class="inset">{segs}</span>' + (f'<span class="icap">{inset[2]}</span>' if len(inset) > 2 else '')
        rows.append(f'<i class="spine{" brk" if i else ""}" style="grid-row:{r}"></i>'
                    f'<div class="{cls}" style="grid-row:{r};--c:var(--psy{b["c"]})"><span class="nm mask">{b["name"]}</span>'
                    f'<span class="rl">{b["rule"]}</span>{ins}</div>')
        brow.append(r)
        r += 1
    if only is not None:
        rows.append(f'<i class="only" style="grid-row:{brow[only]} / {brow[-1] + 1}"></i>')
    for lab, bi, where, lane in pins:
        if not 0 <= bi < len(bands):
            raise ChartError(f'pin {lab}: no band {bi}')
        row = brow[bi] + 1 if where == 'gate-after' else brow[bi]
        col = '3 / 4'                                   # pins ride the right rail, never over band text
        al = {'top': 'start', 'mid': 'center', 'end': 'end', 'gate-after': 'center'}[where]
        rows.append(f'<b class="pin" style="grid-row:{row};grid-column:{col};align-self:{al}">{E(lab)}</b>')
    legend = key(*keys) if keys else ''
    legend = legend.replace('<i class="k-pin"></i>', '<i class="k-pin">1</i>')
    cs = ''.join(f'<li><b class="pin inl">{E(c[0])}</b><span>{c[1]}' + (f' <span class="mask">{c[2]}</span>' if len(c) > 2 else '') + '</span></li>'
                 for c in cases)                        # the diagnosis in a case line masks in study mode
    return (f'<figure class="lcb" role="img" aria-label="{E(title)}">{_title(title, step, "not to scale")}'
            f'<div class="grid">{"".join(rows)}</div>{legend}' + (f'<ul class="cases">{cs}</ul>' if cs else '') + '</figure>')


# ---------------------------------------------------------------- small multiples against mood
def _union(spans):
    out = []
    for s, e in sorted(spans):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def _minus(span, cover):
    s, e = span
    out, cur = [], s
    for cs, ce in cover:
        if ce <= cur or cs >= e:
            continue
        if cs > cur:
            out.append((cur, cs))
        cur = max(cur, ce)
    if cur < e:
        out.append((cur, e))
    return out


def analyse(panel):
    """Geometry -> teaching facts. Returns (free psychosis segments, mood share of the illness, verdict word)."""
    mood = _union([(t, t + h) for t, h, k in panel['mood'] if 'opt' not in k])
    psy = [(t, t + h) for t, h in panel['psy']]
    free = [seg for p in psy for seg in _minus(p, mood)]
    ref = psy if panel.get('rule') in ('schizoaffective', 'minority') and psy else mood + psy   # DSM: share of the psychotic illness
    span = (min(s for s, _ in ref), max(e for _, e in ref))
    mood_len = sum(max(0, min(e, span[1]) - max(s, span[0])) for s, e in mood)
    share = mood_len / (span[1] - span[0])
    return free, share


def _check(panel, free, share):
    rule = panel['rule']
    longest = max((e - s for s, e in free), default=0)
    if rule == 'inside' and free:
        raise ChartError(f'{panel["id"]}: rule "inside" but psychosis is drawn outside a mood episode')
    if rule == 'schizoaffective':
        if not free:
            raise ChartError(f'{panel["id"]}: schizoaffective needs psychosis with no mood episode')
        if longest < panel.get('min_free', 8):
            raise ChartError(f'{panel["id"]}: the psychosis-alone stretch is too short to read as 2 weeks or more')
        if share <= .5:
            raise ChartError(f'{panel["id"]}: schizoaffective needs mood episodes for most of the illness (drawn {share:.0%})')
        if not any(ps < me and ms < pe for ps, pe in [(t, t + h) for t, h in panel['psy']] for ms, me in [(t, t + h) for t, h, _ in panel['mood']]):
            raise ChartError(f'{panel["id"]}: schizoaffective needs a mood episode concurrent with the psychosis')
    if rule not in ('inside', 'schizoaffective', 'minority', 'none'):
        raise ChartError(f'{panel["id"]}: unknown rule {rule!r}')
    if rule == 'minority' and share >= .5:
        raise ChartError(f'{panel["id"]}: rule "minority" but mood episodes cover {share:.0%} of the illness')


def mood_multiples(title, panels, step=None, axis='Time', height=210, keys=('lo', 'hi', 'ps', 'free'), note=''):
    """panels: {id, name, mood: [(t, h, 'lo'|'hi')], psy: [(t, h)], rule: inside|schizoaffective|minority|none,
    decider, free_label (written in the mood lane beside the first free stretch), min_free}. t and h are percent."""
    if not 1 <= len(panels) <= 3:
        raise ChartError('1 to 3 panels')
    names, plots, meters, deciders = [], [], [], []
    for p in panels:
        free, share = analyse(p)
        _check(p, free, share)
        split = len({k.split()[0] for _, _, k in p['mood']}) > 1        # both polarities: low left, high right in the lane
        mood_html = ''.join(f'<i class="mb {k}{" split" if split else ""}" style="--t:{t}%;--h:{h}%"></i>' for t, h, k in p['mood'])
        mood_html += ''.join(f'<i class="pdg" style="--t:{t}%"></i>' for t in p.get('danger', ()))
        mood = _union([(t, t + h) for t, h, _ in p['mood']])
        psy_html = ''
        for t, h in p['psy']:
            for s, e in [(t, t + h)]:
                cuts = sorted({s, e} | {x for a, b in mood for x in (a, b) if s < x < e})
                for a, b in zip(cuts, cuts[1:]):
                    covered = any(ma <= a and b <= mb for ma, mb in mood)
                    psy_html += f'<i class="pb{"" if covered else " free"}" style="--t:{a}%;--h:{b - a}%"></i>'
        guides = '' if len(mood) > 3 else ''.join(f'<i class="gd" style="--t:{x}%"></i>' for x in sorted({v for a, b in mood for v in (a, b)}))
        fl = ''
        if free and p.get('free_label'):
            s, e = max(free, key=lambda z: z[1] - z[0])
            fl = f'<em class="fl" style="--t:{s}%;--h:{e - s}%">{p["free_label"]}</em>'
        word = 'All' if share > .97 else 'Most' if share > .5 else 'Minority' if share > 0 else 'None'
        names.append(f'<div class="ph"><b class="pn mask">{p["name"]}</b></div>')
        plots.append(f'<div class="pp">{guides}{mood_html}{psy_html}{fl}</div>')
        if p['rule'] == 'none':
            meters.append('<div class="mt none"></div>')
        elif p['rule'] == 'inside':
            meters.append('<div class="mt chip"><span>Outside mood: none</span></div>')
        else:
            meters.append(f'<div class="mt"><i style="--s:{share * 100:.0f}%"></i><span>Mood: {word.lower()}</span></div>')
        deciders.append(f'<p class="dc">{p["decider"]}</p>')
    n = len(panels)
    grid = (f'<div class="lcs" style="--n:{n};--ph:{height}px">'
            f'<i class="sp"></i>{"".join(names)}'
            f'<i class="axis"><span>{E(axis)}</span></i>{"".join(plots)}'
            f'<i class="sp"></i>{"".join(meters)}'
            f'<i class="sp"></i>{"".join(deciders)}</div>')
    return (f'<figure class="lc" role="img" aria-label="{E(title)}">{_title(title, step)}'
            f'{grid}{key(*keys)}' + (f'<p class="note">{note}</p>' if note else '') + '</figure>')


# ---------------------------------------------------------------- threshold ruler
UNIT = {'day': 1, 'days': 1, 'week': 7, 'weeks': 7, 'month': 30.4, 'months': 30.4, 'year': 365, 'years': 365}


def _days(s):
    n, u = s.split()
    return float(n) * UNIT[u]


def threshold_ruler(title, marks, step=None, ticks=('1 day', '1 week', '1 month', '6 months', '1 year', '2 years'),
                    height=420, card=46, keys=()):
    """marks: {at: '4 days', name, rule, kind: lo|hi|ps|mix, danger}. Log time ruler from the first to the last tick;
    cards are placed at their mark and pushed apart so none overlap; a leader joins each card to its mark."""
    lo_d, hi_d = _days(ticks[0]), _days(ticks[-1])
    h0 = height
    pad = 14
    y = lambda d: pad + (math.log10(d) - math.log10(lo_d)) / (math.log10(hi_d) - math.log10(lo_d)) * (height - 2 * pad)
    tk = ''.join(f'<b class="rt" style="top:{y(_days(t)):.1f}px">{E(t)}</b><i class="rtick" style="top:{y(_days(t)):.1f}px"></i>' for t in ticks)
    ms = sorted(marks, key=lambda m: _days(m['at']))
    def est(m):                                   # card height from text length (13px name ~30 chars, 11.5px rule ~38 chars a line)
        rule = f"{m['at']} or more" + (' . ' + m['rule'] if m.get('rule') else '')
        return 16 + 18 * math.ceil(len(m['name']) / 24) + 16 * math.ceil(len(rule) / 30)
    hs = [max(card, est(m)) for m in ms]
    want = [y(_days(m['at'])) for m in ms]
    pos, prev_end = [], 0
    for w, h in zip(want, hs):                    # centered on its mark when there is room, else pushed down below the card above
        p = max(w - h / 2, prev_end + 6, 0)
        pos.append(p)
        prev_end = p + h
    height = max(height, prev_end + 4)            # the ruler grows rather than letting cards overlap or leave the frame
    lines, cards, dots = [], [], []
    for m, w, p, h in zip(ms, want, pos, hs):
        cy = p + h / 2
        lines.append(f'<path d="M70 {w:.1f} C 86 {w:.1f}, 84 {cy:.1f}, 100 {cy:.1f}"/>')
        dots.append(f'<i class="rd {m["kind"]}" style="top:{w:.1f}px"></i>' + (f'<i class="rdg" style="top:{w:.1f}px"></i>' if m.get('danger') else ''))
        cards.append(f'<div class="rc {m["kind"]}" style="top:{p:.1f}px;min-height:{h}px"><span class="nm mask">{m["name"]}</span>'
                     f'<span class="rl"><b>{E(m["at"])} or more</b>{(" &middot; " + m["rule"]) if m.get("rule") else ""}</span></div>')
    svg = f'<svg class="rl-svg" width="100%" height="{height}" aria-hidden="true">{"".join(lines)}</svg>'
    return (f'<figure class="lct" role="img" aria-label="{E(title)}">{_title(title, step, "log time scale")}'
            f'<div class="rul" style="height:{height}px"><i class="ax" style="height:{h0 - 28}px"></i>{tk}{svg}{"".join(dots)}{"".join(cards)}</div>'
            + (key(*keys) if keys else '') + '</figure>')


# ---------------------------------------------------------------- v4: horizontal rows (time runs left to right)
def _pct(x):
    return f'{x:g}%'


def window_rows(title, ticks, rows, step=None, keys=('ps', 'only'), note='', small='not to scale'):
    """Horizontal duration windows, one row per diagnosis, all on one shared schematic axis.
    ticks: [(label, x%)] left to right. rows: {name, window, span: (a, b|None), kind: c1|c2|c3|only|exp, needs, mood,
    cues, segs: [(label, a, b, soft|act)], segcap, group}. A span end must sit on a tick (the picture must agree with the
    stated window); b=None means open-ended ("and longer"). 'group' starts a labelled group above that row."""
    xs = {x for _, x in ticks}
    head = ''.join(f'<span style="--x:{_pct(x)}">{E(l)}</span>' for l, x in ticks)
    grid = ''.join(f'<i class="tk" style="--x:{_pct(x)}"></i>' for _, x in ticks)
    out = []
    for r in rows:
        a, b = r['span']
        if r['kind'] != 'exp' and (a not in xs or (b is not None and b not in xs)):
            raise ChartError(f'{r["name"]}: span {r["span"]} does not sit on the ticks {sorted(xs)}')
        if r.get('group'):
            out.append(f'<li class="wg">{r["group"]}</li>')
        end = 100 if b is None else b
        bar = f'<i class="bar {r["kind"]}{" open" if b is None else ""}" style="--a:{_pct(a)};--b:{_pct(end)}"></i>'
        segs = ''
        if r.get('segs'):
            for lab, sa, sb, k in r['segs']:
                segs += f'<span class="sg {k}" style="--a:{_pct(sa)};--b:{_pct(sb)}">{lab}</span>'
            segs = f'<div class="rail segs" aria-hidden="true">{grid}{segs}</div>'
            if r.get('segcap'):
                segs += f'<p class="segcap">{r["segcap"]}</p>'
        lines = ''.join(f'<p class="wl"><b>{lab}</b>{r[k]}</p>' for k, lab in (('needs', 'Needs'), ('mood', 'Mood episodes')) if r.get(k))
        cues = f'<p class="cue">{r["cues"]}</p>' if r.get('cues') else ''
        out.append(f'<li class="wr"><div class="wh"><b class="nm mask">{r["name"]}</b><span class="win">{r["window"]}</span></div>'
                   f'<div class="wb"><div class="rail" aria-hidden="true">{grid}{bar}</div>{segs}{lines}{cues}</div></li>')
    return (f'<figure class="lcw">{_title(title, step, small)}'
            f'<div class="wax" aria-hidden="true"><div class="wsp"></div><div class="wt">{head}<em>Time</em></div></div>'
            f'<ol class="wrows">{"".join(out)}</ol>' + (key(*keys) if keys else '') + (f'<p class="note">{note}</p>' if note else '') + '</figure>')


def mood_tracks(title, panels, step=None, keys=('lo', 'ps', 'free'), note=''):
    """Horizontal paired tracks: per diagnosis a Mood lane over a Psychosis lane on one time axis (t, h in percent, left
    to right). Same rules and geometry checks as mood_multiples(): free psychosis is outlined automatically and a picture
    that contradicts its rule is refused."""
    out = []
    for p in panels:
        free, share = analyse(p)
        _check(p, free, share)
        mood = _union([(t, t + h) for t, h, _ in p['mood']])
        mb = ''.join(f'<i class="mb {k}" style="--a:{_pct(t)};--b:{_pct(t + h)}"></i>' for t, h, k in p['mood'])
        pb = ''
        for t, h in p['psy']:
            cuts = sorted({t, t + h} | {x for a, b in mood for x in (a, b) if t < x < t + h})
            for a, b in zip(cuts, cuts[1:]):
                covered = any(ma <= a and b <= mbb for ma, mbb in mood)
                pb += f'<i class="pb{"" if covered else " free"}" style="--a:{_pct(a)};--b:{_pct(b)}"></i>'
        fl = ''
        if free and p.get('free_label'):
            s, e = max(free, key=lambda z: z[1] - z[0])
            fl = f'<em class="fl" style="--a:{_pct(s)};--b:{_pct(e)}">{p["free_label"]}</em>'
        out.append(f'<li class="tr"><div class="wh"><b class="nm mask">{p["name"]}</b><span class="win">{p["decider"]}</span></div>'
                   f'<div class="wb"><div class="lanes" aria-hidden="true"><span class="ln">Mood</span><div class="lane">{mb}</div>'
                   f'<span class="ln">Psychosis</span><div class="lane">{pb}</div>' + (f'<span></span><div class="fls">{fl}</div>' if fl else '') + '</div>'
                   f'</div></li>')
    return (f'<figure class="lcw lcm">{_title(title, step, "")}'
            f'<div class="wax" aria-hidden="true"><div class="wsp"></div><div class="wt"><em>Time</em></div></div>'
            f'<ol class="wrows">{"".join(out)}</ol>{key(*keys)}' + (f'<p class="note">{note}</p>' if note else '') + '</figure>')


# ---------------------------------------------------------------- v4: workup path (an ordered workup on a vertical line with dots)
def workup_path(title, steps, step=None):
    """An ordered workup: a vertical line with one dot per stage, read top to bottom.
    steps: {when, tests: [(name, [(result, meaning)])], kind: 'first'|'' , text}. A 'first' stage is the shaded tile of
    tests done together, in either order, joined by '+'. Meanings carry class "mask" so study mode hides them."""
    out = []
    for st in steps:
        body = ''
        if st.get('tests'):
            ts = []
            for name, res in st['tests']:
                rs = ''.join(f'<p class="wr2"><b>{r}</b><span class="mask">{m}</span></p>' for r, m in res)
                ts.append(f'<div class="wt2"><p class="tn">{name}</p>{rs}</div>')
            body = f'<div class="tile{" first" if st.get("kind") == "first" else ""}">' + '<i class="plus" aria-label="and"></i>'.join(ts) + '</div>'
        if st.get('text'):
            body += f'<p class="pt-tx">{st["text"]}</p>'
        out.append(f'<li class="pt{" end" if st.get("kind") == "end" else ""}"><span class="when">{st["when"]}</span>{body}</li>')
    return f'<figure class="lcp">{_title(title, step)}<ol class="path">{"".join(out)}</ol></figure>'


# ---------------------------------------------------------------- self-test
if __name__ == '__main__':
    ok = 0
    def expect_error(fn, what):
        global ok
        try:
            fn()
        except ChartError:
            ok += 1
            print('ok  refused:', what)
            return
        raise SystemExit('BAD accepted: ' + what)
    base = {'id': 'x', 'name': 'x', 'decider': 'x'}
    expect_error(lambda: mood_multiples('t', [dict(base, rule='inside', mood=[(0, 40, 'lo')], psy=[(30, 20)])]), 'psychosis drawn past a mood episode under "inside"')
    expect_error(lambda: mood_multiples('t', [dict(base, rule='schizoaffective', mood=[(0, 20, 'lo')], psy=[(0, 90)])]), 'schizoaffective with mood a minority')
    expect_error(lambda: mood_multiples('t', [dict(base, rule='schizoaffective', mood=[(0, 50, 'lo'), (50, 50, 'lo')], psy=[(0, 100)])]), 'schizoaffective with no psychosis alone')
    expect_error(lambda: mood_multiples('t', [dict(base, rule='minority', mood=[(0, 60, 'lo')], psy=[(0, 100)])]), 'schizophrenia with mood the majority')
    html = mood_multiples('t', [dict(base, rule='schizoaffective', mood=[(0, 40, 'lo'), (55, 40, 'lo')], psy=[(5, 90)], free_label='2 wk')])
    assert 'pb free' in html and 'class="fl"' in html and '—' not in html
    ok += 1; print('ok  free psychosis outlined and labeled from geometry')
    r = threshold_ruler('t', [{'at': '4 days', 'name': 'a', 'kind': 'hi'}, {'at': '1 week', 'name': 'b', 'kind': 'hi'}, {'at': '2 weeks', 'name': 'c', 'kind': 'lo'}])
    tops = [float(x) for x in __import__('re').findall(r'class="rc [a-z]+" style="top:([\d.]+)px', r)]
    assert all(b - a >= 46 for a, b in zip(tops, tops[1:])), tops
    ok += 1; print('ok  ruler cards never overlap', [round(t) for t in tops])
    expect_error(lambda: window_rows('t', [('a', 0), ('b', 30)], [{'name': 'x', 'window': 'x', 'span': (0, 40), 'kind': 'c1'}]), 'a window that ends off its tick')
    expect_error(lambda: mood_tracks('t', [dict(base, verdict='v', rule='inside', mood=[(0, 40, 'lo')], psy=[(30, 20)])]), 'horizontal: psychosis past a mood episode under "inside"')
    h = mood_tracks('t', [dict(base, verdict='v', rule='schizoaffective', mood=[(0, 40, 'lo'), (55, 40, 'lo')], psy=[(5, 90)], free_label='2 wk')])
    assert 'pb free' in h and 'class="fl"' in h
    ok += 1; print('ok  horizontal tracks outline free psychosis')
    print(f'{ok}/9 passed')
