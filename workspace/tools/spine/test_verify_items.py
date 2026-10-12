#!/usr/bin/env python3
"""Offline tests for verify.py's item version rule (item_meaning): which item changes need a version bump.

  python3 tools/spine/test_verify_items.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify import item_meaning  # noqa: E402

BASE = ('<li data-type="next" data-d1="Renal biopsy" data-d2="Repeat dipstick" data-item-id="q_x" data-item-version="1" '
        'data-lead-in="Which of the following is the most appropriate next step?">'
        '<span class="sl">6-year-old boy has puffy eyes</span>\n<span class="si">urine: 4+ protein</span>'
        ' &rarr; <b>Oral prednisone</b> &rarr; a typical child has presumed minimal change disease</li>')
ok = bad = 0


def expect(name, same, want_same):
    global ok, bad
    if same == want_same:
        ok += 1
    else:
        bad += 1
        print('FAIL %s: meaning %s, expected %s' % (name, 'same' if same else 'changed', 'same' if want_same else 'changed'))


m0 = item_meaning(BASE)
expect('explanation-only edit needs no bump',
       item_meaning(BASE.replace('a typical child has presumed', 'a typical young child has presumed')) == m0, True)
expect('lead-in change is a meaning change',
       item_meaning(BASE.replace('most appropriate next step?', 'should be avoided?')) == m0, False)
expect('item type change is a meaning change',
       item_meaning(BASE.replace('data-type="next"', 'data-type="avoid"')) == m0, False)
expect('key change is a meaning change', item_meaning(BASE.replace('Oral prednisone', 'Renal biopsy now')) == m0, False)
expect('distractor label change is a meaning change',
       item_meaning(BASE.replace('data-d2="Repeat dipstick"', 'data-d2="Renal ultrasound"')) == m0, False)
expect('stem change is a meaning change', item_meaning(BASE.replace('4+ protein', '2+ protein')) == m0, False)
arrow = BASE.replace('urine: 4+ protein', 'urine: 4+ protein &rarr; repeat 3+')
ma = item_meaning(arrow)
expect('an arrow inside the stem keeps the key', ma[-1] == 'Oral prednisone', True)
expect('an arrow inside the stem stays part of the stem', 'repeat 3+' in ma[-2], True)
expect('explanation edit with an arrow in the stem still needs no bump',
       item_meaning(arrow.replace('a typical child', 'a typical young child')) == ma, True)
expect('formatting-only stem edit (extra spaces) needs no bump',
       item_meaning(BASE.replace('puffy eyes</span>', 'puffy  eyes</span>')) == m0, True)
print('test_verify_items: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
