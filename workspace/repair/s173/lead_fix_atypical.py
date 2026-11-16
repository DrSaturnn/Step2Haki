#!/usr/bin/env python3
"""Finish the pc-atypical rewrite file: one raw removes the NBME wrapper, and the QT hover lines are restated."""
import json

D = 'repair/migration/pharm/ATYP/spine/'
P = D + 'rewrite_s173/rewrite_s173.json'
j = json.load(open(P, encoding='utf-8'))
units = {u['uid']: u for u in json.load(open(D + 'rewrite_s173/units.json', encoding='utf-8'))['units']} \
    if isinstance(json.load(open(D + 'rewrite_s173/units.json', encoding='utf-8')), dict) else \
    {u['uid']: u for u in json.load(open(D + 'rewrite_s173/units.json', encoding='utf-8'))}
gone = ['U0%d' % n for n in range(72, 81)]
claims = sorted({c for g in gone for c in (units[g].get('claims_in') or []) + (units[g].get('claims_part') or [])})
j['units'] = [u for u in j['units'] if u['uid'] not in gone]
base = open(D + 'baseline_s173.html', encoding='utf-8').read()
i = base.index('<div class="pc-nbq">')
e = base.index('</div></div>', i) + len('</div></div>')
j['raw'] = [r for r in j['raw'] if 'pc-nbq' not in r['old']]
j['raw'].append({'old': base[i:e], 'new': '', 'claims': claims, 'carried_by': ['U033', 'U053'],
                 'lock_ok': ['Setup', 'Offered', 'Deciding', 'Answer', 'clue', 'NBME', 'question', 'Effects', 'a', 'means',
                             'Antipsychotic', 'Adverse'],
                 'lock_reason': 'NBME blocks removed: labels dropped, stem details carried in U033 and U053',
                 'note': 'N5: neither block is a fence case; facts carried, wrapper removed'})
for u in j['units']:
    if u['uid'] == 'U035':
        u['new'] = u['new'].replace('<span class="sp-l">Quetiapine or risperidone: also paired with ziprasidone for QT</span>',
                                    '<span class="sp-l">Risperidone: also listed with ziprasidone for QT prolongation</span>')
        u['lock_ok'] = sorted(set(u['lock_ok']) | {'0 of 1'})
        u['lock_reason'] = ('source name moved to data-src (N4); the note that one card omits quetiapine is a source '
                            'difference and goes to the batch report')
    if u['uid'] in ('U033', 'U053'):
        u['new'] = u['new'].replace('Other answer options for that picture:', 'Common wrong answers:') \
                           .replace('Other answer options:', 'Common wrong answers:')
json.dump(j, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('raw', len(j['raw']), 'units', len(j['units']), 'claims', len(claims))
