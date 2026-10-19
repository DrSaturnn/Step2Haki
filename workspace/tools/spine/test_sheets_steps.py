#!/usr/bin/env python3
"""Offline tests for sheets.py --page (s148c packet error): spine step numbers map to shots.py segment positions through a
brief's h5 headers, so a brief with absent steps gets the steps asked for, and an absent step is an error.

  python3 tools/spine/test_sheets_steps.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sheets as S  # noqa: E402

H = '<h5 class="sp-h">%s</h5>'
PAGE = ('<html><body><div class="brief" id="x"><h4>X</h4>' + ''.join(
    H % t for t in ('<span>1</span>Drug script', '2Urgent risks', '3Differential', '7Treatment', '8Follow-up')) +
    '<h5 class="authored-hdr sp-h">Practice</h5></div>'
    '<div class="brief" id="y"><h4>Y</h4>' + ''.join(
        H % t for t in ('1Illness script', '2Urgent risks', '3Differential', '4Workup', '5Diagnostic criteria',
                        '6Severity', '7Treatment', '8Follow-up')) + '<h5 class="sp-h">Practice</h5></div>'
    '<script>var a=1;</script></body></html>')

fails = []


def check(name, got, want):
    if got != want:
        fails.append('%s: got %r, want %r' % (name, got, want))


px = S.positions(PAGE, 'x')
check('absent steps shift positions', S.map_steps(['header', '2', '3', '7', '8', 'practice'], px), ['0', '2', '3', '4', '5', '6'])
check('no Workup header', px.get('4'), None)
py = S.positions(PAGE, 'y')
check('full brief is identity', S.map_steps(['1', '4', '7', '8', 'practice'], py), ['1', '4', '7', '8', '9'])
try:
    S.map_steps(['4'], px)
    fails.append('absent step 4 did not raise')
except SystemExit:
    pass
files = ['a_phone_step%d.png' % k for k in range(7)] + ['a_phone_step4a.png']
check('pick on mapped positions', S.pick(sorted(files, key=S.stepkey), S.map_steps(['7', '8'], px)),
      ['a_phone_step4.png', 'a_phone_step4a.png', 'a_phone_step5.png'])
print('test_sheets_steps: %d failed' % len(fails) + ''.join('\n  ' + f for f in fails))
sys.exit(1 if fails else 0)
