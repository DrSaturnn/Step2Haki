#!/usr/bin/env python3
"""Offline tests for verify.p1_residual (s134): hedge words lost with whole lines cut for the soft cap are accounted for
only by cuts listed in cuts.json whose text is gone from the brief; a hedge dropped from a kept line still counts.

  python3 tools/spine/test_p1_cuts.py
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import verify as V  # noqa: E402


def page(body):
    return ('<html><body><div class="brief" id="zz-test" data-title="T"><h3>T</h3>%s</div>'
            '<div class="brief" id="zz-next" data-title="N"><h3>N</h3><p>x</p></div></body></html>' % body)


OLD = page('<p>Kept line: the level may rise within 10 days.</p>'
           '<p>Cut line one: stopping lithium may be enough; it can often settle.</p>'
           '<p>Cut line two: about 20% of users may develop polyuria.</p>')
ok = bad = 0


def case(name, new_body, cuts, want):
    global ok, bad
    d = tempfile.mkdtemp()
    if cuts is not None:
        json.dump({'cuts': [{'text': c} for c in cuts]}, open(os.path.join(d, 'cuts.json'), 'w'))
    got = V.p1_residual(d, 'zz-test', OLD, page(new_body))
    if (got < 2) == want:
        ok += 1
    else:
        bad += 1
        print('FAIL', name, 'residual', got)


KEPT = '<p>Kept line: the level may rise within 10 days.</p>'
# 1. both lines cut and listed: every lost hedge is held by a cut
case('cuts listed', KEPT, ['Cut line one: stopping lithium may be enough; it can often settle.',
                           'Cut line two: about 20% of users may develop polyuria.'], True)
# 2. the same cuts, not listed: P1 stands
case('cuts not listed', KEPT, None, False)
# 3. cuts listed, but the kept line also lost its hedge: residual 1 + nothing else... make it 2 by a second kept hedge
OLD2 = OLD
case('kept line lost a hedge, one cut unlisted', '<p>Kept line: the level rises within 10 days.</p>',
     ['Cut line one: stopping lithium may be enough; it can often settle.'], False)
# 4. a listed cut whose text is still on the page does not count
case('listed cut still present', KEPT + '<p>Cut line two: about 20% of users may develop polyuria.</p>',
     ['Cut line one: stopping lithium may be enough; it can often settle.',
      'Cut line two: about 20% of users may develop polyuria.'], True)
case('listed cut still present, other unlisted', KEPT + '<p>Cut line two: about 20% of users may develop polyuria.</p>',
     ['Cut line two: about 20% of users may develop polyuria.'], False)
# 5. a kept line that drops "may" while all cuts are listed: residual 1, below the preflight threshold of 2 (as P1)
case('one kept hedge lost, cuts listed', '<p>Kept line: the level rises within 10 days.</p>',
     ['Cut line one: stopping lithium may be enough; it can often settle.',
      'Cut line two: about 20% of users may develop polyuria.'], True)
# tail_fix.json (s134): exact, single-match replacements only
def tcase(name, t, fixes, want_t, want_err):
    global ok, bad
    got, err = V.apply_tail_fix(t, fixes)
    if (got == want_t or want_t is None) and bool(err) == want_err:
        ok += 1
    else:
        bad += 1
        print('FAIL', name, repr(got)[:60], err)


tcase('one fix', 'a give mesna b', [['give mesna', 'mesna prevents']], 'a mesna prevents b', False)
tcase('missing anchor', 'a b', [['give mesna', 'x']], None, True)
tcase('double anchor', 'mesna mesna', [['mesna', 'x']], None, True)
tcase('chained', 'abc', [['a', 'x'], ['xb', 'y']], 'yc', False)

# s148: qualified_held: a qualified number cut with its line (listed, text gone) is held; bare stems elsewhere do not matter
def qcase(name, new_body, cuts, tok, want):
    global ok, bad
    d = tempfile.mkdtemp()
    if cuts is not None:
        json.dump({'cuts': [{'text': c} for c in cuts]}, open(os.path.join(d, 'cuts.json'), 'w'))
    got = V.qualified_held(d, 'zz-test', page(new_body), tok)
    if got == want:
        ok += 1
    else:
        bad += 1
        print('FAIL', name, got)


STEM = '<p>A man has 2 days of knee swelling.</p>'
qcase('qualified cut listed, gone', STEM, ['drainage if not improving after about 2 days'], '2 days', True)
qcase('qualified cut not listed', STEM, None, '2 days', False)
qcase('listed cut still on the page', STEM + '<p>drainage if not improving after about 2 days</p>',
      ['drainage if not improving after about 2 days'], '2 days', False)
qcase('listed cut holds another number', STEM, ['about 20% of users'], '2 days', False)
print('test_p1_cuts: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
