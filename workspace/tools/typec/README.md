# Psych chart builder (tools/typec/lifechart.py, v4)

One Python module draws every psych chart from named fields, plus its styles (`typec.css`, section "Psych charts v4").
Every label is real HTML text: study mode masks the diagnosis names and only the names, screen readers read the figure
(a `figure` with a `figcaption`, no `role="img"`; bars and rails are `aria-hidden`), phones wrap it.

    python3 tools/typec/lifechart.py          # self-test, 24 cases
    python3 tools/typec/demo_bipolar.py > /tmp/bp.html && python3 tools/typec/preview.py /tmp/bp.html /tmp/bp_preview.html
    node tools/typec/shoot.js /tmp/bp_preview.html bipolar-mania /tmp/shots   # 390 and 1280 px, reading and study mode

## The visual language (the same on every brief)

- Time runs down, on a gated ruler or a labeled arrow.
- Periwinkle = low mood; apricot = high mood (blue against orange survives red-green color blindness).
- Teal hatch = psychosis with Criterion A met, deeper the longer it lasts. Solid pale teal with a dotted border = one
  delusion only. An ink outline around a psychosis segment = psychosis with no mood episode.
- Red = danger (hospitalization) and nothing else.
- A filled dark circle = a step of the method (1 rule out a cause, 2 time it, 3 check it against mood). The same badge
  goes on a table caption (`<caption><b class="step">1</b>Rule out a cause</caption>`) so the method reads in order.
- An outlined tag "NBME 1" = an NBME patient placed on a chart, numbered as in the brief's Practice section. Never a
  filled circle, so a pin is never mistaken for a step.

## One recall direction

Study mode masks diagnosis names everywhere (chart bands, the lane, panel names, case answers) and the comparison table
masks its first column (`data-mask="1"`). Facts stay visible. That is the exam's direction (stem to diagnosis), and it
means no element on the page is the answer key for another.

## The three chart types

```python
from lifechart import duration_bands, mood_multiples, threshold_ruler, Gate, Band, Inset, Lane, Pin, Case, Panel, Mood, Psy, Mark
```

1. `duration_bands(title, gates, bands, *, step, fid, lane, pins, cases, keys)`: a gated ruler. `Gate(label, note)` per
   band; `Band(name, rule, depth 1..3, open, inset=Inset([(label, weight, 'soft'|'act')], caption))`. Band `rule` is the
   non-time discriminator (the gates show the window). `Lane(name, rule, start)` adds a second, named lane for a diagnosis
   that owns a window without Criterion A (delusional disorder from the 1-month gate). `Pin('NBME 2', band, 'top', lane)`
   and `Case(pin, text, answer)` place the NBME patients; the case answer masks.
2. `mood_multiples(title, panels, *, step, fid, height, keys, note)`: up to 3 `Panel(id, name, rule, decider, mood=[Mood(t, h,
   'lo'|'hi', opt, mild, sub)], psy=[Psy(t, h)], free_label, danger)` on one time axis; t and h are percent of the panel.
   The builder computes from the geometry which psychosis falls outside mood episodes (outlined) and writes one verdict
   strip under every panel: "Psychosis alone: none / <free_label> / most" and "Mood share: all / most / minority". It
   refuses a panel whose drawing contradicts its rule: `inside` (no psychosis outside a mood episode), `schizoaffective`
   (psychosis alone long enough to read as 2 weeks, a concurrent mood episode, mood more than half the illness),
   `minority` (mood less than half), `none` (bipolar charts, no verdict strip). The share is of the drawn psychotic illness
   (of the mood episodes themselves for `inside`), so it checks the picture against the rule, not the clinic against time.
3. `threshold_ruler(title, marks, *, step, fid, ticks, height)`: `Mark(at='4 days', name, rule, kind lo|hi|ps|mix, danger)`
   on a log time ruler; cards are pushed apart so none overlap, with a leader to each mark.

Text is escaped by default; wrap a string in `Html()` to pass markup through. In a brief, pass every label through the
build script's `T()` so it gets a traced claim row (see the psychosis v6 build).

## Layout

Figures cap at 480 px alone; inside `<div class="lc-row">` two figures sit side by side from 900 px. Under 480 px the
two-lane ruler narrows its tick column and lane and steps its type down one size.

## Known limits

- The charts are diagrams, not to scale; real durations are in the labels and the comparison table's Time course column.
- The cyclothymic threshold for children is left off the ruler: unverified (the sources were unreachable from the build
  container on 2026-09-30).
- Styles assume the page's tokens (`--raised`, `--hair`, `--muted`, `--ink`, `--recess`); `preview.py` renders a brief
  inside a copy of the page.
