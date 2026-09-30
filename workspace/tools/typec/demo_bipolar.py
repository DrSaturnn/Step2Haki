#!/usr/bin/env python3
"""demo_bipolar.py: the chart builder's other two uses, as a preview fragment (not a brief; no claim map).

  python3 tools/typec/demo_bipolar.py > /tmp/bipolar_demo.html
  python3 tools/typec/preview.py /tmp/bipolar_demo.html /tmp/bipolar_preview.html

The clock ruler carries every minimum duration NBME plays against another, including the two the psychosis brief turns on
(delusional disorder at 1 month, schizoaffective disorder's 2 weeks of psychosis alone). The cyclothymic threshold for
children is not on the ruler: it is unverified (the sources were unreachable from the build container on 2026-09-30)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lifechart import threshold_ruler, mood_multiples, Mark, Panel, Mood, Psy

RULER = threshold_ruler('The clocks NBME mixes up', [
    Mark('1 day', 'Brief psychotic disorder', 'recovered by 1 month', 'ps'),
    Mark('4 days', 'Hypomanic episode', 'no psychosis or admission', 'hi'),
    Mark('1 week', 'Manic episode', 'or any length if admitted', 'hi', danger=True),
    Mark('2 weeks', 'Major depressive episode', '5 symptoms', 'lo'),
    Mark('2 weeks', 'Schizoaffective disorder', 'psychosis alone, then mood most of the illness', 'ps'),
    Mark('1 month', 'Delusional disorder', 'one delusion; Criterion A never met', 'ps'),
    Mark('1 month', 'Schizophreniform disorder', 'under 6 months', 'ps'),
    Mark('6 months', 'Schizophrenia', '1 month active', 'ps'),
    Mark('2 years', 'Persistent depressive disorder', '1 year in children', 'lo'),
    Mark('2 years', 'Cyclothymic disorder', 'below episode criteria', 'mix')],
    step=1, fid='bp-clocks', keys=('lo', 'hi', 'ps', 'dng'))

EPISODES = mood_multiples('Read the episodes', [
    Panel('bp1', 'Bipolar I disorder', 'none', 'One manic episode is enough; depression not required',
          mood=[Mood(4, 32, 'hi'), Mood(58, 34, 'lo', opt=True)], psy=[Psy(10, 18)], danger=(4,)),
    Panel('bp2', 'Bipolar II disorder', 'none', 'Hypomania plus major depression; never mania',
          mood=[Mood(6, 20, 'hi', mild=True), Mood(44, 44, 'lo')]),
    Panel('cyc', 'Cyclothymic disorder', 'none', 'Swings below episode criteria, 2 years or more',
          mood=[Mood(t, 9 if t < 90 else 8, 'hi' if i % 2 == 0 else 'lo', sub=True) for i, t in enumerate((2, 15, 28, 41, 54, 67, 80, 90))])],
    step=2, fid='bp-episodes', height=210, keys=('lo', 'hi', 'ps', 'dng', 'opt', 'mild', 'sub'))

print(f'<div class="brief" id="bipolar-mania" data-shelf="psych" data-bp="behav"><h4>Bipolar and the Clocks (preview)</h4>'
      f'<div class="lc-row">{RULER}{EPISODES}</div></div>')
