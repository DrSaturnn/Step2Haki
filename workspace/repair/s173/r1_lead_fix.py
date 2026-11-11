#!/usr/bin/env python3
"""After the lane B fix script: a unit that names "claims" keeps its own claims too; record the lock holds."""
import json
MOVED = {'SUD': {'S115', 'S125', 'S176', 'S194'}, 'OTHER': {'S120', 'S121', 'S122', 'S132'}}
for f, moved in MOVED.items():
    d = 'repair/migration/pharm/%s/spine/rewrite_s173/' % f
    base = {u['uid']: u for u in json.load(open(d + 'units.json'))['units']}
    j = json.load(open(d + 'rewrite_s173.json'))
    for u in j['units']:
        if u.get('claims'):
            own = [c for c in base[u['uid']].get('claims_in', []) if c not in moved or c in u['claims']]
            u['claims'] = sorted(set(u['claims']) | set(own))
    json.dump(j, open(d + 'rewrite_s173.json', 'w'), ensure_ascii=False, indent=1)
LOCK = [('ANXIO', 'U017', '1 of 2'), ('ANXIO', 'U020', '0 of 1'), ('ANXIO', 'U023', '0 of 1'), ('COG', 'U042', '0 of 1')]
for f, uid, tok in LOCK:
    p = 'repair/migration/pharm/%s/spine/rewrite_s173/rewrite_s173.json' % f
    j = json.load(open(p))
    for u in j['units']:
        if u['uid'] == uid:
            u['lock_ok'] = sorted(set(u.get('lock_ok', [])) | {tok})
            u['lock_reason'] = (u.get('lock_reason', '') + '; the note "no board source found yet" leaves visible text, the unverified mark stays').strip('; ')
    json.dump(j, open(p, 'w'), ensure_ascii=False, indent=1)
