#!/usr/bin/env python3
"""Lead wording fixes on the rewrite files before review round 1; each pair must occur once in its unit."""
import json, subprocess

FIX = {
 'pc-orexin': [('U008', 'the class agent with the most board questions', 'the orexin antagonist tested on boards'),
               ('U029', 'In practice: use is not recommended', 'In practice: not recommended; not a listed contraindication')],
 'pc-sleep': [('U025', '<span class="sp-l">No board question on it found yet.</span>', ''),
              ('U026', '<span class="sp-l">No board question on it found yet.</span>', '')],
 'pc-antichol': [('U027', 'Anorectal manometry, colon transit study, fiber, abdominal X-ray: not the first step; testing waits',
                  'Common wrong answers: anorectal manometry, colon transit study, fiber, abdominal X-ray</p><p>Reversible drug cause: testing waits')],
 'pc-benzo': [('U028', 'Effects offered that are not benzodiazepine effects:', 'Common wrong answers (not benzodiazepine effects):'),
              ('U045', 'In one item: as early as 24 hours', 'Also reported: onset as early as 24 hours')],
 'adhd-meds': [('U056', 'Prescribed use is not a use disorder', None),
               ('U033', 'Prescribed use is not a use disorder', 'Prescribed stimulant use')],
}
for b, pairs in FIX.items():
    f = subprocess.run(['python3', 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip()
    p = f + '/rewrite_s173/rewrite_s173.json'
    j = json.load(open(p, encoding='utf-8'))
    U = {u['uid']: u for u in j['units']}
    for uid, old, new in pairs:
        if new is None:
            continue
        n = U[uid]['new'].count(old) if uid in U else -1
        if n != 1:
            print('MISS %s %s (%d): %s' % (b, uid, n, old[:50])); continue
        U[uid]['new'] = U[uid]['new'].replace(old, new)
    json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done')
