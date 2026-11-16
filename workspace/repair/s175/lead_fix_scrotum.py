#!/usr/bin/env python3
"""Lead fix after the pilot (scrotum): the two differential captions keep their settings as sp-note lines (the s174
bone-tumors form), and the rule label takes the header list's name. Run from workspace/."""
import json
F = 'repair/migration/peds/scrotum/spine/rewrite_s175/'
d = json.load(open(F + 'rewrite_s175.json')); base = {u['uid']: u for u in json.load(open(F + 'units.json'))['units']}
pre = '<div class="sp-dx"><table class="dense">'
for uid, setting in (('U023', 'acute scrotum'), ('U030', 'painless scrotal mass')):
    old = base[uid]['html']; u = next(x for x in d['units'] if x['uid'] == uid)
    d['units'].remove(u)
    d['raw'].append({'old': pre + old, 'new': '<p class="sp-note">Setting: %s</p>%s<caption>Differential diagnosis</caption>' % (setting, pre),
                     'claims': base[uid].get('claims', []), 'lock_ok': ['most tempting first', 'most', 'tempting', 'first', 'The', 'the'],
                     'lock_reason': 'header rename H2; setting moved to the sp-note line', 'note': 'caption rename, setting note (lead)'})
for r in d['raw']:
    if 'Transferable rules' in r['new']:
        r['new'] = r['new'].replace('<span class="lbl">Transferable rules</span>', '<span class="lbl">General rule</span>')
        r.setdefault('lock_ok', []).extend(['Transferable', 'rules']); r['lock_reason'] = 'header rename H23'
json.dump(d, open(F + 'rewrite_s175.json', 'w'), indent=1, ensure_ascii=False)
