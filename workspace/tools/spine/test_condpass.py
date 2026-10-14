#!/usr/bin/env python3
"""Offline tests for conditional PASS (tools/spine/condpass.py and verify.py's replay).

  python3 tools/spine/test_condpass.py
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import condpass as CP  # noqa: E402
import verify as V  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


# ---- receipt format
R = '''part: read
deps: brief=aaaaaaaaaa live=bbbbbbbbbb siblings=cccccccccc specs=dddddddddd
brief-sha: aaaaaaaaaa
Verdict: PASS-IF
Findings
1. LOW ...
Replacements:
1. old: {{loop diuretic as in rung 1}}
   new: {{loop diuretic as in card 1 above}}
2. old: {{Clot prevention: considered at high risk}}
   new: {{Clot prevention is considered when risk is high}}
Checked and fine:
- everything else
'''
v, reps = CP.parse(R)
expect('verdict PASS-IF parsed', v == 'PASS-IF')
expect('two replacements parsed', len(reps) == 2 and reps[0][1] == 'loop diuretic as in rung 1')
expect('section after the block is not swallowed', 'everything' not in reps[-1][2])
expect('plain PASS parsed', CP.parse('Verdict: PASS\n')[0] == 'PASS')
# s138: a receipt without {{ }} (one line each) still parses; braces win when both appear; a broken pair does not parse
_nb = CP.parse('Verdict: PASS-IF\nReplacements:\n1. old: salt restriction, which would\n   new: salt restriction, since a diet would\n2. old: x y\n   new: x z\n\nChecked and fine:\nok\n')
expect('brace-less replacements parsed', _nb == ('PASS-IF', [(1, 'salt restriction, which would', 'salt restriction, since a diet would'), (2, 'x y', 'x z')]))
expect('brace-less: new on a later line only', CP.parse('Verdict: PASS-IF\nReplacements:\n1. old: a b\n\n   new: a c\n')[1] == [])
expect('braces still win', CP.parse('Verdict: PASS-IF\nReplacements:\n1. old: {{a b}}\n   new: {{a c}}\n')[1] == [(1, 'a b', 'a c')])
# s138: an ambiguous replacement with a string id (verify's pool ids are 'part.n') reports instead of crashing
expect('ambiguous with a string id', 'ambiguous' in str(CP.undo('x y x y', [('read.1', 'a', 'x y')], 'html')[2]))

# ---- hard rules: text only, numbers, length
expect('markup refused', CP.hard_problems('a <b>b</b>', 'a b'))
expect('mask refused', CP.hard_problems('x', '<span class="mask">x</span>'))
expect('entity refused', CP.hard_problems('a &amp; b', 'a and b'))
expect('changed number refused', CP.hard_problems('ratio above 0.2', 'ratio above 0.5'))
expect('dropped number refused', CP.hard_problems('as in rung 1', 'as in the first card'))
expect('long new text refused', CP.hard_problems('a', ' '.join(['w'] * 41)))
expect('plain rewording allowed', not CP.hard_problems('urinalysis mean minimal change', 'urinalysis point to minimal change'))

# ---- wording-only test (hedge words are meaning, Jonathan 2026-10-12)
T = {'Minimal change disease', 'membranous nephropathy', 'CT'}
expect('rewording is wording-only', CP.wording_only('mean minimal change disease', 'point to minimal change disease', T))
expect('dropping a hedge is not', not CP.wording_only('usually Streptococcus pneumoniae', 'Streptococcus pneumoniae', T))
expect('usually to usual is not', not CP.wording_only('usually pneumococcus', 'the usual organism is pneumococcus', T))
expect('considered keeps consider', CP.wording_only('considered at high risk', 'is considered when risk is high', T))
expect('adding may is not', not CP.wording_only('gives clots', 'may give clots', T))
expect('about is a hedge', not CP.wording_only('about 1 to 3 weeks', '1 to 3 weeks', T))
expect('a negation change is not', not CP.wording_only('with hematuria', 'without hematuria', T))
expect('a name change is not', not CP.wording_only('membranous in a child', 'membranous nephropathy in a child', T))
expect('a test name change is not', not CP.wording_only('imaging first', 'CT first', T))
# s133 flags replacements 6 and 7: meaning changes the test must catch
R6O = 'hepatitis B first; also lupus, autoimmune thyroid disease'
expect('s133 rep 6 is not', not CP.wording_only(R6O, 'usually hepatitis B, lupus or autoimmune thyroid disease', T))
expect('dropping first is not, even with no hedge', not CP.wording_only(R6O, 'hepatitis B, lupus or autoimmune thyroid disease', T))
expect('s133 rep 7 adds an exception', not CP.wording_only('Long-term anticoagulation',
                                                          'Long-term anticoagulation unless an invasive intervention is planned', T))
expect('adding only is not', not CP.wording_only('in membranous', 'only in membranous', T))
expect('keeping first is still wording-only', CP.wording_only('hepatitis B first', 'hepatitis B comes first', T))

# ---- undo: backwards replay, forms, ambiguity
html = '<p>In nephrotic syndrome&rsquo;s course, the organism is usually pneumococcus.</p><p>card 1 above</p>'
t, ap, pr = CP.undo(html, [(1, 'card A', 'card 1 above')], 'html')
expect('undo applies a present replacement', ap == [1] and 'card A' in t and pr is None)
t, ap, pr = CP.undo(html, [(2, 'gone', 'not here')], 'html')
expect('an absent replacement is simply not applied', ap == [] and t == html)
t, ap, pr = CP.undo(html, [(3, 'syndrome’s', 'syndrome’s course')], 'html')
expect('named-entity form is found (’ as &rsquo;)', ap == [3])
t, ap, pr = CP.undo('<p>x y</p><p>x y</p>', [(4, 'x z', 'x y')], 'html')
expect('ambiguous new text is a problem', pr is not None)
js = json.dumps({'t': 'He said "card 1 above" twice'})
t, ap, pr = CP.undo(js, [(5, 'card A', 'card 1 above')], 'json')
expect('json form is found', ap == [5])

# ---- pool: own replacements always; others only when wording-only
rec = {'read': ('PASS-IF', [(1, 'mean minimal change disease', 'point to minimal change disease'),
                            (2, 'usually pneumococcus', 'the usual organism is pneumococcus')]),
       'acc': ('PASS', []), 'display': ('PASS', []), 'flags': ('PASS-IF', [(1, 'a <b>x</b>', 'a x')])}
pl = CP.pool(rec, T)
expect('read keeps both its own', len(pl['read']) == 2)
expect('acc takes only the wording-only one', [o for _, o, _ in pl['acc']] == ['mean minimal change disease'])
expect('a markup replacement counts for nobody', all('<b>' not in o for p in pl for _, o, _ in pl[p]))

# ---- verify.replay end to end on a toy folder
d = tempfile.mkdtemp()
try:
    H0 = '<div class="brief" id="toy"><p>a pure 4+ protein urinalysis mean minimal change disease</p>' \
         '<h5 class="authored-hdr">Practice</h5><p>bank</p></div>'
    C0 = json.dumps({'claims': [{'text': 'a pure 4+ protein urinalysis mean minimal change disease'}]})
    O0 = json.dumps({'t': 'a pure 4+ protein urinalysis mean minimal change disease'})

    class F:
        pass
    f = F()
    f.d, f.bid, f.PAGE, f.SPECS = d, 'nephrotic-child', V.Verify.PAGE, V.Verify.SPECS
    f.deps = lambda **kw: V.Verify.deps(f, **kw)

    def state(h, c, o):
        f.brief_html = h
        open(os.path.join(d, 'claim_map.json'), 'w').write(c)
        open(os.path.join(d, 'outline.json'), 'w').write(o)
    state(H0, C0, O0)
    got = f.deps()
    keys = ('brief', 'bank', 'claims', 'outline')
    rep = [('read.1', 'urinalysis mean minimal change', 'urinalysis point to minimal change')]
    sw = lambda x: x.replace('urinalysis mean minimal change', 'urinalysis point to minimal change')
    state(sw(H0), sw(C0), sw(O0))
    expect('replay accepts exactly the approved replacement', V.Verify.replay(f, 'read', keys, got, rep) == ['read.1'])
    state(sw(H0).replace('4+ protein', '4+ protein only'), sw(C0), sw(O0))
    expect('replay refuses one extra edit', V.Verify.replay(f, 'read', keys, got, rep) is None)
    state(sw(H0), sw(C0), O0.replace('pure', 'clean'))
    expect('replay refuses an extra edit in the outline alone', V.Verify.replay(f, 'read', keys, got, rep) is None)
    state(H0, C0, O0)
    expect('nothing applied and nothing changed: replay has nothing to accept',
           V.Verify.replay(f, 'read', keys, got, []) is None)
finally:
    shutil.rmtree(d, ignore_errors=True)

print('test_condpass: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
