#!/usr/bin/env python3
"""Record the meaning-lock holds for the lead wording fixes."""
import json
L = [('SLEEPAG', 'U025', '2 of 3', 'verification note "No board question on it found yet" leaves visible text for the batch report'),
     ('SLEEPAG', 'U026', '0 of 1', 'verification note "No board question on it found yet" leaves visible text for the batch report'),
     ('ADHD', 'U033', '1 of 2', 'hover title is a noun phrase; the body line keeps "do not make a stimulant use disorder"')]
for f, uid, tok, why in L:
    p = 'repair/migration/pharm/%s/spine/rewrite_s173/rewrite_s173.json' % f
    j = json.load(open(p, encoding='utf-8'))
    for u in j['units']:
        if u['uid'] == uid:
            u['lock_ok'] = sorted(set(u.get('lock_ok', [])) | {tok})
            u['lock_reason'] = (u.get('lock_reason', '') + '; ' + why).strip('; ')
    json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
