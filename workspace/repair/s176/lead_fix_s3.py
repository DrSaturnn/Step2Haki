#!/usr/bin/env python3
"""Lead fixes after S3 r0: the Beckwith-Wiedemann bait joins the one pause point block of bs-abdominal-mass (gate
pause-format: one block, one div.pp-b per bait); the bs-distal-rta worked example keeps the arithmetic form of its
anion gap line (preflight P1 read the old qualifier).  python3 repair/s176/lead_fix_s3.py"""
import json
A = 'repair/migration/peds/bs-abdominal-mass/spine/rewrite_s176/rewrite_s176.json'
j = json.load(open(A, encoding='utf-8'))
r = j['raw'][1]
seam = '</div>\n</div>\n<div class="sp-pause"><b class="pp-t">Pause point</b>\n<div class="pp-b">'
if seam in r['new']:
    r['new'] = r['new'].replace(seam, '</div>\n<div class="pp-b">')
json.dump(j, open(A, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
D = 'repair/migration/peds/bs-distal-rta/spine/rewrite_s176/rewrite_s176.json'
s = open(D, encoding='utf-8').read()
old = 'Worked example: sodium 138, chloride 112, bicarbonate 16 → gap 10, normal'
s = s.replace(old, 'Worked example: 138 minus (112 plus 16) gives 10, a normal gap')
open(D, 'w', encoding='utf-8').write(s)
print('ok')

# bs-fever-rash-arthralgia U061: the newborn VariZIG line shared a 12-word run with a cited quote (shingle_check)
B = 'repair/migration/id/bs-fever-rash-arthralgia/spine/rewrite_s176/rewrite_s176.json'
s = open(B, encoding='utf-8').read()
o = '2 days after delivery: VariZIG within 10 days'
if o in s:
    assert s.count(o) == 1
    s = s.replace(o, '2 days after delivery: give VariZIG within 10 days')
    open(B, 'w', encoding='utf-8').write(s)
print('ok fever-rash')

# bs-abdominal-mass: data-nbme sits on the bait's div.pp-b (lint pause-format), not on its setup span
j = json.load(open(A, encoding='utf-8'))
r = j['raw'][1]
o = '<div class="pp-b">\n<span class="sl" data-nbme="peds-cms-f627e3">'
if o in r['new']:
    r['new'] = r['new'].replace(o, '<div class="pp-b" data-nbme="peds-cms-f627e3">\n<span class="sl">')
    json.dump(j, open(A, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('ok pp-b')
