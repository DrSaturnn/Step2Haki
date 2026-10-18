#!/usr/bin/env python3
"""Offline test for verify.presentations_link (s147): a one-brief preview of a new hub gets its Presentations link."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify import presentations_link

NAV = ('<div id="navlinks">\n\n    <div class="sect">Presentations <span class="count">2</span></div>\n'
       '    <a href="#cough">Chronic Cough</a>\n    <a href="#voices">Hears Voices</a>\n\n'
       '    <div class="sect">Renal <span class="count">1</span></div>\n    <a href="#scrotum">Scrotal Pain and Masses</a>\n</div>\n')
HUB = '<div class="brief sp" id="scrotum" data-entry="hub"><h4>Scrotal Pain and Masses</h4></div>'
DIS = '<div class="brief sp" id="scrotum" data-entry="disease"><h4>Scrotal Pain and Masses</h4></div>'
ok = 0
# 1. a hub not yet listed: link added after the group's last link, count 2 -> 3
out = presentations_link(NAV + HUB, 'scrotum')
assert '<span class="count">3</span>' in out and '    <a href="#voices">Hears Voices</a>\n    <a href="#scrotum">Scrotal Pain and Masses</a>\n\n' in out, out
assert out.count('href="#scrotum"') == 2; ok += 1
# 2. a disease brief: unchanged
assert presentations_link(NAV + DIS, 'scrotum') == NAV + DIS; ok += 1
# 3. already listed: unchanged (idempotent)
assert presentations_link(out, 'scrotum') == out; ok += 1
# 4. no Presentations group: unchanged
plain = NAV.replace('Presentations', 'Pulmonary') + HUB
assert presentations_link(plain, 'scrotum') == plain; ok += 1
print('test_verify_presentations: %d/4 passed' % ok)
