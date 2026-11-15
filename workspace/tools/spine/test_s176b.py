#!/usr/bin/env python3
"""Offline tests for the pair tool, the outline guard, the stale-delta check, the lost-claim-id report, the size check
and condpass undo across inline tags.

  python3 tools/spine/test_s176b.py
"""
import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_pairs as AP  # noqa: E402
import condpass as CP  # noqa: E402
import patch as PT  # noqa: E402
import rewrite_lanes as RL  # noqa: E402
import size_check as SC  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


# pair extraction: a finding number before PAIR, several PAIRs in one line, backticks, a Replacements block
txt = ('2. MED, a note. PAIR b1 | OLD: so normal rules it out | NEW: and this child has no episodes\n'
       'PAIR b1 | OLD: Born early: any infant | NEW: Born early: regardless. PAIR b1 | OLD: Mostly NREM | NEW: Mostly in NREM sleep\n'
       '`PAIR b1 | OLD: x one | NEW: x two`\n'
       'Replacements:\n1. old: {{a high residual means overflow}}\n   new: {{a high residual points to overflow}}\n')
got = AP.dedupe(AP.from_text(txt, 'b1'))
expect('numbered line read', ('b1', 'so normal rules it out', 'and this child has no episodes') in got)
expect('two pairs in one line split', ('b1', 'Born early: any infant', 'Born early: regardless') in got
       and ('b1', 'Mostly NREM', 'Mostly in NREM sleep') in got)
expect('backticks stripped', ('b1', 'x one', 'x two') in got)
expect('replacements read', ('b1', 'a high residual means overflow', 'a high residual points to overflow') in got)
expect('no PAIR text leaks into a NEW', not any('PAIR' in n for _, _, n in got))
expect('duplicates count once', len(AP.dedupe(got + got)) == len(got))

# entities: a pause answer keeps &rarr;, markup-safe entities stay
d, back = AP.decode('<span class="pp-a">&rarr; <span class="mask">Name the tempo</span></span> &lt;200 &amp; more')
r = AP.sub(d, 'Name the tempo', 'CSF RT-QuIC')
out = AP.encode(r, back)
expect('entity kept after a pair', out.startswith('<span class="pp-a">&rarr; ') and 'CSF RT-QuIC' in out)
expect('lt and amp untouched', '&lt;200 &amp; more' in out)
d2, back2 = AP.decode('a → b &rarr; c')
expect('a literal arrow keeps the field as it was', AP.encode(d2, back2) == 'a → b → c')

# apply end to end on a lane folder
with tempfile.TemporaryDirectory() as t:
    f = os.path.join(t, 'brief')
    os.makedirs(os.path.join(f, 'rewrite_sX'))
    json.dump({'brief': 'b1', 'units': [{'uid': 'U001', 'new': '<p>Offered &middot; <b>A</b>: one fact here</p>'}], 'raw': [],
               'new_claims': [{'text': 'A: one fact here', 'ids': ['x']}]},
              open(os.path.join(f, 'rewrite_sX', 'rewrite_sX.json'), 'w'))
    json.dump({'units': [{'uid': 'U001', 'html': '<p>old</p>'}, {'uid': 'U002', 'html': '<li>Two &rarr; three</li>'}]},
              open(os.path.join(f, 'rewrite_sX', 'units.json'), 'w'))
    res = AP.apply('sX', [('b1', 'one fact here', 'one fact stated'), ('b1', 'Two → three', 'Two → four')],
                   fold=lambda b: f)
    rw = json.load(open(os.path.join(f, 'rewrite_sX', 'rewrite_sX.json')))
    expect('changed unit applied with its entity kept', rw['units'][0]['new'] == '<p>Offered &middot; <b>A</b>: one fact stated</p>')
    expect('new claim text follows', rw['new_claims'][0]['text'] == 'A: one fact stated')
    expect('unchanged unit added with its entity kept',
           any(u['uid'] == 'U002' and u['new'] == '<li>Two &rarr; four</li>' for u in rw['units']))
    expect('both reported applied', all(r.startswith('applied') for r in res))

# outline guard and stale delta
with tempfile.TemporaryDirectory() as f:
    a, b = os.path.join(f, 'outline.json'), os.path.join(f, 'outline_before_sX.json')
    open(a, 'w').write('{"x": 1}')
    open(b, 'w').write('{"x": 1}')
    g = PT.outline_guard(f, 'sX')
    expect('identical restored outline removed', g and not g.startswith('STOP') and not os.path.exists(a))
    expect('nothing to do after removal', PT.outline_guard(f, 'sX') is None)
    open(a, 'w').write('{"x": 2}')
    expect('differing outline stops', (PT.outline_guard(f, 'sX') or '').startswith('STOP') and os.path.exists(a))
    os.makedirs(os.path.join(f, 'rewrite_sX'))
    rw, dl = os.path.join(f, 'rewrite_sX', 'rewrite_sX.json'), os.path.join(f, 'delta_sX.json')
    open(dl, 'w').write('{}')
    open(rw, 'w').write('{}')
    now = time.time()
    os.utime(dl, (now - 60, now - 60))
    expect('lane file newer than delta is stale', PT.stale_delta(f, 'sX'))
    os.utime(dl, (now + 60, now + 60))
    expect('fresh delta is not stale', not PT.stale_delta(f, 'sX'))

# lost claim ids
with tempfile.TemporaryDirectory() as f:
    cm = os.path.join(f, 'claim_map.json')
    json.dump({'claims': [{'id': 'S012', 'new_text': 'a', 'derived_from': ['x', 'y']},
                          {'id': 'S902', 'new_text': 'b line', 'derived_from': ['p', 'q']}]}, open(cm, 'w'))
    before = RL.claim_ids(f)
    json.dump({'claims': [{'id': 'S012', 'new_text': 'a', 'derived_from': ['x']},
                          {'id': 'S903', 'new_text': 'b line', 'derived_from': ['p', 'q']}]}, open(cm, 'w'))
    lost = RL.lost_ids(before, RL.claim_ids(f), 'sX')
    expect('lost id on an old claim reported', len(lost) == 1 and 'S012' in lost[0] and 'y' in lost[0])
    expect('a renumbered new claim with its ids is not reported', not any('b line' in x for x in lost))

# condpass undo across inline tags
orig = '<li><b>Azithromycin</b>: treats cat-scratch disease, whose node develops 1 to 2 weeks after the scratch; a node</li>'
done = '<li><b>Azithromycin</b>: may be given for cat-scratch disease, whose node develops 1 to 2 weeks after the scratch papule; a node</li>'
o = 'Azithromycin: treats cat-scratch disease, whose node develops 1 to 2 weeks after the scratch;'
n = 'Azithromycin: may be given for cat-scratch disease, whose node develops 1 to 2 weeks after the scratch papule;'
t, ap, pr = CP.undo(done, [(1, o, n)], 'html')
expect('undo across a bold term restores the html byte for byte', ap == [1] and pr is None and t == orig)
t, ap, pr = CP.undo(done + done, [(1, o, n)], 'html')
expect('two matches across tags are ambiguous', ap == [] and pr and 'ambiguous' in pr)
t, ap, pr = CP.undo('<p>A <b>X</b>Y b</p>', [(1, 'A Z b', 'A XY b')], 'html')
expect('a middle that holds a tag is not undone', ap == [] and pr is None)
t, ap, pr = CP.undo('<p>plain new text</p>', [(1, 'plain old text', 'plain new text')], 'html')
expect('plain undo unchanged', ap == [1] and t == '<p>plain old text</p>')

# size check against a baseline
with tempfile.TemporaryDirectory() as t:
    b = os.path.join(t, 'base.json')
    json.dump({'size': 100}, open(b, 'w'))
    real = SC.measure
    SC.measure = lambda page: 101
    expect('over the baseline fails', SC.main(['x.html', '--baseline', b]) == 1)
    SC.measure = lambda page: 100
    expect('at the baseline passes', SC.main(['x.html', '--baseline', b]) == 0)
    SC.measure = real

print('test_s176b: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
