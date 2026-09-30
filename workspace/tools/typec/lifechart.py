#!/usr/bin/env python3
"""lifechart.py v4: the psych chart builder for the AxBx study page (styles: tools/typec/typec.css, "Psych charts v4").

Three chart types, one visual language on every brief:
  time runs down, marked by a labeled arrow or a gated ruler;
  periwinkle = low mood, apricot = high mood;
  teal hatch = psychosis (Criterion A met); solid pale teal with a dotted border = one delusion only;
  an ink outline around a psychosis segment = psychosis with no mood episode;
  red = danger (hospitalization) and nothing else;
  a filled dark circle = a step of the method; an outlined tag "Q1" = an NBME patient placed on the chart.

  duration_bands()  A gated ruler. Lane 1 holds the diagnoses that need Criterion A, one band per window between gates.
                    An optional second lane holds a diagnosis that owns a window in the same time axis without Criterion A
                    (delusional disorder), named and maskable like every band. Gate notes, an inset (what the 6 months of
                    schizophrenia contain), NBME pins and case lines are optional.
  mood_multiples()  Small multiples on one time axis (up to 3). The builder COMPUTES from the drawn geometry which psychosis
                    falls outside mood episodes (outlined automatically) and the mood share of the illness, writes both in
                    one verdict strip under every panel, and refuses a panel whose picture contradicts its rule.
  threshold_ruler() Minimum-duration clocks on a log time ruler, cards pushed apart so none overlap, a leader to each mark.

Every label is real HTML text: study mode masks the diagnosis names (class "mask") and only the names, screen readers read
the figure (no role="img"; the bars and rails are aria-hidden, the words carry the meaning), phones wrap it.
Text is escaped by default; wrap a string in Html() to pass markup through.
Self-test: python3 tools/typec/lifechart.py
"""
import math
from dataclasses import dataclass, field
from html import escape
from typing import List, Optional, Sequence, Tuple


class ChartError(ValueError):
    pass


class Html(str):
    """A string that is already HTML; the builder inserts it unescaped."""


def esc(x):
    return x if isinstance(x, Html) else escape(str(x), quote=True)


# ---------------------------------------------------------------- the visual language
KEYS = {'lo': ('k-lo', 'Low mood'), 'hi': ('k-hi', 'High mood'), 'ps': ('k-ps', 'Psychosis'),
        'free': ('k-free', 'Psychosis with no mood episode'), 'lane': ('k-lane', 'One delusion only'),
        'dng': ('k-dng', 'Hospitalized'), 'pin': ('k-pin', 'NBME question, numbered as in Practice'),
        'sub': ('k-sub', 'Below episode criteria'), 'opt': ('k-opt', 'Common, not required'),
        'mild': ('k-mild', 'Hypomania: milder')}


def key(*names):
    out = []
    for n in names:
        if n not in KEYS:
            raise ChartError(f'unknown key {n!r}')
        k, t = KEYS[n]
        swatch = '<i class="k-pin">NBME</i>' if n == 'pin' else f'<i class="{k}"></i>'
        out.append(f'<span>{swatch}{esc(t)}</span>')
    return '<div class="lc-key">' + ''.join(out) + '</div>'


def _caption(title, step, small=''):
    st = f'<b class="step">{esc(step)}</b>' if step else ''
    return (f'<figcaption>{st}<span class="t">{esc(title)}</span>'
            + (f'<small>{esc(small)}</small>' if small else '') + '</figcaption>')


def _fig(cls, fid, inner):
    return f'<figure class="{cls}"' + (f' id="{esc(fid)}"' if fid else '') + f'>{inner}</figure>'


# ---------------------------------------------------------------- duration bands
@dataclass
class Gate:
    label: str                  # written on the gate line, top to bottom
    note: str = ''              # e.g. "still ill: move down"


@dataclass
class Inset:
    segments: Sequence[Tuple[str, float, str]]   # (label, weight, 'soft'|'act')
    caption: str = ''


@dataclass
class Band:
    name: str                   # diagnosis (masked in study mode)
    rule: str                   # the non-time discriminator, not the window (the gates show the window)
    depth: int = 1              # 1..3, teal deepens the longer the illness
    open: bool = False          # last band runs "and longer"
    inset: Optional[Inset] = None


@dataclass
class Lane:
    name: str                   # diagnosis owning the second lane (masked)
    rule: str
    start: int                  # index of the gate/band it hangs from
    header: str = 'One delusion only'
    band_header: str = 'Criterion A met'


@dataclass
class Pin:
    label: str                  # "Q1"
    band: int                   # band index the pin sits beside
    where: str = 'mid'          # 'top'|'mid'|'end'
    lane: bool = False          # True: in the second lane


@dataclass
class Case:
    pin: str
    text: str
    answer: str = ''            # masked in study mode


def duration_bands(title, gates: Sequence[Gate], bands: Sequence[Band], *, step=None, fid=None, lane: Optional[Lane] = None,
                   pins: Sequence[Pin] = (), cases: Sequence[Case] = (), keys=('pin',), scale_note='not to scale'):
    if len(gates) != len(bands):
        raise ChartError('one gate per band')
    for b in bands:
        if b.depth not in (1, 2, 3):
            raise ChartError(f'{b.name}: depth must be 1, 2 or 3')
    if lane and not 0 <= lane.start < len(bands):
        raise ChartError(f'lane {lane.name}: no band {lane.start}')
    for p in pins:
        if not 0 <= p.band < len(bands):
            raise ChartError(f'pin {p.label}: no band {p.band}')
        if p.where not in ('top', 'mid', 'end'):
            raise ChartError(f'pin {p.label}: where must be top, mid or end')
        if p.lane and not lane:
            raise ChartError(f'pin {p.label}: no lane to sit in')
    rows, r, brow = [], 1, []
    pinned = {p.band for p in pins if not p.lane}          # a band with a pin keeps its text clear of the tag
    for i, (g, b) in enumerate(zip(gates, bands)):
        rows.append(f'<b class="tk" style="grid-row:{r}">{esc(g.label)}</b><i class="gate" aria-hidden="true" style="grid-row:{r}"></i>'
                    + (f'<em class="gnote" style="grid-row:{r}">{esc(g.note)}</em>' if g.note else ''))
        r += 1
        ins = ''
        if b.inset:
            segs = ''.join(f'<span class="{k}" style="flex:{f}">{esc(lab)}</span>' for lab, f, k in b.inset.segments)
            ins = f'<span class="inset">{segs}</span>' + (f'<span class="icap">{esc(b.inset.caption)}</span>' if b.inset.caption else '')
        cls = 'band' + (' deep' if b.depth == 3 else '') + (' open' if b.open else '') + (' pinned' if i in pinned else '')
        rows.append(f'<i class="spine{" brk" if i else ""}" aria-hidden="true" style="grid-row:{r}"></i>'
                    f'<div class="{cls}" style="grid-row:{r};--c:var(--psy{b.depth})"><span class="nm mask">{esc(b.name)}</span>'
                    f'<span class="rl">{esc(b.rule)}</span>{ins}</div>')
        brow.append(r)
        r += 1
    if lane:
        rows.append(f'<div class="lane" style="grid-row:{brow[lane.start]} / {brow[-1] + 1}"><span class="nm mask">{esc(lane.name)}</span>'
                    f'<span class="rl">{esc(lane.rule)}</span></div>')
    for p in pins:
        al = {'top': 'start', 'mid': 'center', 'end': 'end'}[p.where]
        rows.append(f'<b class="pin" style="grid-row:{brow[p.band]};grid-column:{3 if p.lane else 2};align-self:{al}">{esc(p.label)}</b>')
    head = ''
    if lane:
        head = f'<div class="lanes-h" aria-hidden="true"><span></span><span>{esc(lane.band_header)}</span><span>{esc(lane.header)}</span></div>'
    cs = ''.join(f'<li><b class="pin inl">{esc(c.pin)}</b><span>{esc(c.text)}' + (f' <span class="mask">{esc(c.answer)}</span>' if c.answer else '') + '</span></li>'
                 for c in cases)
    inner = (_caption(title, step, scale_note) + head + f'<div class="grid{" two" if lane else ""}">{"".join(rows)}</div>'
             + (key(*keys) if keys else '') + (f'<ul class="cases">{cs}</ul>' if cs else ''))
    return _fig('lcb', fid, inner)


# ---------------------------------------------------------------- small multiples against mood
@dataclass
class Mood:
    t: float                    # start, percent of the panel height
    h: float                    # length, percent
    kind: str = 'lo'            # 'lo'|'hi'
    opt: bool = False           # dashed: common, not required
    mild: bool = False          # hypomania
    sub: bool = False           # below episode criteria

    def css(self):
        return self.kind + (' opt' if self.opt else '') + (' mild' if self.mild else '') + (' sub' if self.sub else '')


@dataclass
class Psy:
    t: float
    h: float


@dataclass
class Panel:
    id: str
    name: str                   # masked
    rule: str                   # 'inside'|'schizoaffective'|'minority'|'none'
    decider: str
    mood: List[Mood] = field(default_factory=list)
    psy: List[Psy] = field(default_factory=list)
    free_label: str = ''        # written beside the longest psychosis-alone stretch, and used as its verdict word
    danger: Sequence[float] = ()
    min_free: float = 8         # percent of the panel a psychosis-alone stretch needs to read as "2 weeks or more"


RULES = ('inside', 'schizoaffective', 'minority', 'none')


def _union(spans):
    out = []
    for s, e in sorted(spans):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


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


def _overlap(a, b):
    return sum(max(0, min(e, be) - max(s, bs)) for s, e in a for bs, be in b)


def analyse(p: Panel):
    """Geometry -> teaching facts: (psychosis-alone segments, share of psychosis that is alone, mood share of the illness).
    The illness is the psychotic illness (its drawn psychosis) for schizoaffective and schizophrenia; for a mood disorder
    with psychotic features the illness is the mood episodes themselves."""
    mood = _union([(m.t, m.t + m.h) for m in p.mood if not m.opt])
    psy = _union([(x.t, x.t + x.h) for x in p.psy])
    free = [seg for s in psy for seg in _minus(s, mood)]
    psy_len = sum(e - s for s, e in psy)
    alone = sum(e - s for s, e in free) / psy_len if psy_len else 0
    ref = mood if p.rule == 'inside' or not psy else psy
    ref_len = sum(e - s for s, e in ref)
    share = _overlap(mood, ref) / ref_len if ref_len else 0
    return free, alone, share


def _check(p: Panel, free, share):
    if p.rule not in RULES:
        raise ChartError(f'{p.id}: unknown rule {p.rule!r}')
    if p.rule == 'none':
        return
    if not p.psy:
        raise ChartError(f'{p.id}: rule {p.rule!r} needs psychosis drawn')
    longest = max((e - s for s, e in free), default=0)
    if p.rule == 'inside' and free:
        raise ChartError(f'{p.id}: rule "inside" but psychosis is drawn outside a mood episode')
    if p.rule == 'schizoaffective':
        if not free:
            raise ChartError(f'{p.id}: schizoaffective needs psychosis with no mood episode')
        if longest < p.min_free:
            raise ChartError(f'{p.id}: the psychosis-alone stretch is too short to read as 2 weeks or more')
        if share <= .5:
            raise ChartError(f'{p.id}: schizoaffective needs mood episodes for most of the illness (drawn {share:.0%})')
        if not any(x.t < m.t + m.h and m.t < x.t + x.h for x in p.psy for m in p.mood if not m.opt):
            raise ChartError(f'{p.id}: schizoaffective needs a mood episode concurrent with the psychosis')
    if p.rule == 'minority' and share >= .5:
        raise ChartError(f'{p.id}: rule "minority" but mood episodes cover {share:.0%} of the illness')


def _words(alone, share, free_label):
    a = 'none' if alone == 0 else 'most' if alone >= .5 else (free_label or 'some')
    s = 'all' if share > .97 else 'most' if share > .5 else 'minority' if share > 0 else 'none'
    return a, s


def mood_multiples(title, panels: Sequence[Panel], *, step=None, fid=None, axis='Time', height=200,
                   keys=('lo', 'hi', 'ps', 'free'), note=''):
    if not 1 <= len(panels) <= 3:
        raise ChartError('1 to 3 panels')
    names, plots, verdicts, deciders = [], [], [], []
    for p in panels:
        free, alone, share = analyse(p)
        _check(p, free, share)
        split = len({m.kind for m in p.mood}) > 1          # both polarities: low left, high right in the lane
        mood_html = ''.join(f'<i class="mb {m.css()}{" split" if split else ""}" style="--t:{m.t}%;--h:{m.h}%"></i>' for m in p.mood)
        mood_html += ''.join(f'<i class="pdg" style="--t:{t}%"></i>' for t in p.danger)
        mood = _union([(m.t, m.t + m.h) for m in p.mood if not m.opt])
        psy_html = ''
        for x in p.psy:
            s, e = x.t, x.t + x.h
            cuts = sorted({s, e} | {v for a, b in mood for v in (a, b) if s < v < e})
            for a, b in zip(cuts, cuts[1:]):
                covered = any(ma <= a and b <= mb for ma, mb in mood)
                psy_html += f'<i class="pb{"" if covered else " free"}" style="--t:{a}%;--h:{b - a}%"></i>'
        guides = '' if len(mood) > 3 else ''.join(f'<i class="gd" style="--t:{v}%"></i>' for v in sorted({v for a, b in mood for v in (a, b)}))
        fl = ''
        if free and p.free_label:
            s, e = max(free, key=lambda z: z[1] - z[0])
            fl = f'<em class="fl" style="--t:{s}%;--h:{e - s}%">{esc(p.free_label)}</em>'
        names.append(f'<div class="ph"><b class="pn mask">{esc(p.name)}</b></div>')
        plots.append(f'<div class="pp" aria-hidden="true">{guides}{mood_html}{psy_html}{fl}</div>')
        if p.rule == 'none':
            verdicts.append('<div class="vd none"></div>')
        else:
            a, s = _words(alone, share, p.free_label)
            verdicts.append(f'<dl class="vd"><dt>Psychosis alone</dt><dd>{esc(a)}</dd>'
                            f'<dt>Mood share</dt><dd><i style="--s:{share * 100:.0f}%"></i>{esc(s)}</dd></dl>')
        deciders.append(f'<p class="dc">{esc(p.decider)}</p>')
    n = len(panels)
    grid = (f'<div class="lcs" style="--n:{n};--ph:{height}px">'
            f'<i class="sp"></i>{"".join(names)}'
            f'<i class="axis" aria-hidden="true"><span>{esc(axis)}</span></i>{"".join(plots)}'
            f'<i class="sp"></i>{"".join(verdicts)}'
            f'<i class="sp"></i>{"".join(deciders)}</div>')
    inner = _caption(title, step) + grid + key(*keys) + (f'<p class="note">{esc(note)}</p>' if note else '')
    return _fig('lc', fid, inner)


# ---------------------------------------------------------------- threshold ruler
UNIT = {'day': 1, 'days': 1, 'week': 7, 'weeks': 7, 'month': 30.4, 'months': 30.4, 'year': 365, 'years': 365}


@dataclass
class Mark:
    at: str                     # '4 days', '2 weeks', '6 months'
    name: str                   # masked
    rule: str = ''
    kind: str = 'ps'            # 'lo'|'hi'|'ps'|'mix'
    danger: bool = False


def _days(s):
    try:
        n, u = s.split()
        return float(n) * UNIT[u]
    except (ValueError, KeyError):
        raise ChartError(f'cannot read the duration {s!r}: use "<number> <day|week|month|year>[s]"')


def threshold_ruler(title, marks: Sequence[Mark], *, step=None, fid=None,
                    ticks=('1 day', '1 week', '1 month', '6 months', '1 year', '2 years'), height=420, card=46, keys=()):
    """Log time ruler from the first to the last tick; cards sit at their mark when there is room, else are pushed down
    under the card above, and the ruler grows rather than letting cards overlap or leave the frame."""
    for m in marks:
        if m.kind not in ('lo', 'hi', 'ps', 'mix'):
            raise ChartError(f'{m.name}: kind must be lo, hi, ps or mix')
    lo_d, hi_d = _days(ticks[0]), _days(ticks[-1])
    h0, pad = height, 14
    y = lambda d: pad + (math.log10(d) - math.log10(lo_d)) / (math.log10(hi_d) - math.log10(lo_d)) * (height - 2 * pad)
    tk = ''.join(f'<b class="rt" style="top:{y(_days(t)):.1f}px">{esc(t)}</b><i class="rtick" aria-hidden="true" style="top:{y(_days(t)):.1f}px"></i>' for t in ticks)
    ms = sorted(marks, key=lambda m: _days(m.at))

    def est(m):                                   # card height from text length (13px name ~24 chars, 11.5px rule ~30 chars a line)
        rule = f'{m.at} or more' + (' . ' + m.rule if m.rule else '')
        return 16 + 18 * math.ceil(len(m.name) / 24) + 16 * math.ceil(len(rule) / 30)
    hs = [max(card, est(m)) for m in ms]
    want = [y(_days(m.at)) for m in ms]
    pos, prev_end = [], 0
    for w, h in zip(want, hs):
        p = max(w - h / 2, prev_end + 6, 0)
        pos.append(p)
        prev_end = p + h
    height = max(height, prev_end + 4)
    lines, cards, dots = [], [], []
    for m, w, p, h in zip(ms, want, pos, hs):
        cy = p + h / 2
        lines.append(f'<path d="M70 {w:.1f} C 86 {w:.1f}, 84 {cy:.1f}, 100 {cy:.1f}"/>')
        dots.append(f'<i class="rd {m.kind}" aria-hidden="true" style="top:{w:.1f}px"></i>'
                    + (f'<i class="rdg" aria-hidden="true" style="top:{w:.1f}px"></i>' if m.danger else ''))
        cards.append(f'<div class="rc {m.kind}" style="top:{p:.1f}px;min-height:{h}px"><span class="nm mask">{esc(m.name)}</span>'
                     f'<span class="rl"><b>{esc(m.at)} or more</b>{(" &middot; " + esc(m.rule)) if m.rule else ""}</span></div>')
    svg = f'<svg class="rl-svg" width="100%" height="{height}" aria-hidden="true">{"".join(lines)}</svg>'
    inner = (_caption(title, step, 'log time scale')
             + f'<div class="rul" style="height:{height}px"><i class="ax" aria-hidden="true" style="height:{h0 - 28}px"></i>{tk}{svg}{"".join(dots)}{"".join(cards)}</div>'
             + (key(*keys) if keys else ''))
    return _fig('lct', fid, inner)


# ---------------------------------------------------------------- self-test
def _selftest():
    import re
    ok = 0

    def refuses(fn, what):
        nonlocal ok
        try:
            fn()
        except ChartError:
            ok += 1
            print('ok  refused:', what)
            return
        raise SystemExit('BAD accepted: ' + what)

    def passes(cond, what):
        nonlocal ok
        if not cond:
            raise SystemExit('BAD: ' + what)
        ok += 1
        print('ok ', what)

    P = lambda **k: Panel(id='x', name='x', decider='x', **k)
    # mood multiples: the four contradictions
    refuses(lambda: mood_multiples('t', [P(rule='inside', mood=[Mood(0, 40)], psy=[Psy(30, 20)])]), 'psychosis drawn past a mood episode under "inside"')
    refuses(lambda: mood_multiples('t', [P(rule='schizoaffective', mood=[Mood(0, 20)], psy=[Psy(0, 90)])]), 'schizoaffective with mood a minority')
    refuses(lambda: mood_multiples('t', [P(rule='schizoaffective', mood=[Mood(0, 50), Mood(50, 50)], psy=[Psy(0, 100)])]), 'schizoaffective with no psychosis alone')
    refuses(lambda: mood_multiples('t', [P(rule='minority', mood=[Mood(0, 60)], psy=[Psy(0, 100)])]), 'schizophrenia with mood the majority')
    refuses(lambda: mood_multiples('t', [P(rule='inside', mood=[Mood(0, 40)])]), 'a psychosis rule with no psychosis drawn')
    refuses(lambda: mood_multiples('t', [P(rule='sometimes', mood=[Mood(0, 40)], psy=[Psy(0, 10)])]), 'an unknown rule')
    # geometry -> words, one verdict strip per panel
    h = mood_multiples('t', [P(rule='schizoaffective', mood=[Mood(0, 40), Mood(55, 40)], psy=[Psy(5, 90)], free_label='2 wk+')])
    passes('pb free' in h and 'class="fl"' in h, 'free psychosis outlined and labeled from geometry')
    passes('<dd>2 wk+</dd>' in h and '<dd><i style="--s:83%"></i>most</dd>' in h, 'schizoaffective verdict: psychosis alone "2 wk+", mood share most')
    h = mood_multiples('t', [P(rule='inside', mood=[Mood(4, 38), Mood(58, 36)], psy=[Psy(12, 22), Psy(64, 20)])])
    passes('<dd>none</dd>' in h and '--s:100%' in h and '</i>all</dd>' in h, 'mood disorder with psychotic features: psychosis alone none, mood share all')
    h = mood_multiples('t', [P(rule='minority', mood=[Mood(44, 16)], psy=[Psy(4, 92)])])
    passes('<dd>most</dd>' in h and '</i>minority</dd>' in h, 'schizophrenia: psychosis alone most, mood share minority')
    h = mood_multiples('t', [P(rule='none', mood=[Mood(4, 30, 'hi'), Mood(50, 30, 'lo', opt=True)], danger=(4,))])
    passes('vd none' in h and 'mb hi split' in h and 'mb lo opt split' in h and 'pdg' in h, 'bipolar panel: no verdict strip, both polarities split, danger dot')
    # duration bands
    G = [Gate('Day 1'), Gate('1 month', 'still ill: move down'), Gate('6 months')]
    B = [Band('Brief psychotic disorder', 'clears', 1), Band('Schizophreniform disorder', 'provisional', 2), Band('Schizophrenia', 'decline', 3, open=True)]
    refuses(lambda: duration_bands('t', G[:2], B), 'gates and bands that do not pair')
    refuses(lambda: duration_bands('t', G, B, pins=[Pin('Q1', 7)]), 'a pin on a band that does not exist')
    refuses(lambda: duration_bands('t', G, B, pins=[Pin('Q1', 0, lane=True)]), 'a lane pin with no lane')
    refuses(lambda: duration_bands('t', G, [Band('x', 'y', 4)] + B[1:]), 'a band depth outside 1..3')
    h = duration_bands('t', G, B, step=2, fid='pd-time', lane=Lane('Delusional disorder', '1 month or more', 1),
                       pins=[Pin('NBME 2', 0), Pin('NBME 1', 2, 'top', lane=True)], cases=[Case('NBME 1', 'the healer:', 'delusional disorder')])
    passes(h.count('class="nm mask"') == 4 and 'class="lane"' in h and 'grid-row:4 / 7' in h, 'the delusion lane is a named, masked element spanning from its gate to the end')
    passes('<figcaption><b class="step">2</b>' in h and 'role=' not in h and 'id="pd-time"' in h, 'figure with a figcaption and an id, no role="img"')
    passes('>still ill: move down</em>' in h and 'grid-row:2;grid-column:2;align-self:center">NBME 2' in h and 'grid-row:6;grid-column:3;align-self:start">NBME 1' in h and h.count('band pinned') == 1, 'gate note written; pins sit beside their band, in the band column or the lane; a pinned band clears its text')
    passes('<span class="mask">delusional disorder</span>' in h, 'the case answer masks')
    h = duration_bands('t', G, [Band('<b>x</b>', 'a & b', 1)] + B[1:])
    passes('&lt;b&gt;x&lt;/b&gt;' in h and 'a &amp; b' in h, 'labels are escaped by default')
    h = duration_bands('t', G, [Band(Html('<i>x</i>'), 'y', 1)] + B[1:])
    passes('<i>x</i>' in h, 'Html() passes markup through')
    # threshold ruler
    r = threshold_ruler('t', [Mark('4 days', 'a', kind='hi'), Mark('1 week', 'b', kind='hi'), Mark('2 weeks', 'c', kind='lo')])
    tops = [float(x) for x in re.findall(r'class="rc [a-z]+" style="top:([\d.]+)px', r)]
    passes(all(b - a >= 46 for a, b in zip(tops, tops[1:])), f'ruler cards never overlap {[round(t) for t in tops]}')
    refuses(lambda: threshold_ruler('t', [Mark('4 fortnights', 'a')]), 'a duration in an unknown unit')
    refuses(lambda: threshold_ruler('t', [Mark('4 days', 'a', kind='red')]), 'a mark kind outside the language')
    print(f'{ok}/{ok} passed')


if __name__ == '__main__':
    _selftest()
