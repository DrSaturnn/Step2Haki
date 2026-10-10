"""Mutation tests for outline_check.py (and the renderer's guards): each mutation of a golden outline must raise its
rule, and the unmutated goldens must pass. Needs the local-only goldens under repair/migration.

  python3 tools/spine/test_outline_check.py
"""
import copy
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import outline_check as OC  # noqa: E402

GOLD = {'nephrotic-child': 'repair/migration/peds/NEPH/spine', 'scfe': 'repair/migration/peds/SCFE/spine',
        'copd': 'repair/migration/fm/COPD/spine'}
BASE = GOLD['nephrotic-child']


def blocks(o, t):
    return [b for b in o['body'] if isinstance(b, dict) and b.get('type') == t]


def dx_table(o):
    return [b for b in blocks(o, 'table') if b['heads'][-1] == 'Decides it'][0]


def ladder(o):
    return blocks(o, 'ladder')[0]


def m_label(o, d):
    o['steps'][2][1] = 'Look-alikes'


def m_no_h(o, d):
    o['body'].remove(blocks(o, 'h')[1])


def m_unknown(o, d):
    o['body'].append({'type': 'carousel'})


def m_plain(o, d):
    o['body'].append('<p>Steroids work in most children here</p>')


def m_bad_id(o, d):
    o['body'].append({'t': 'Steroids work in most children', 'ids': ['zz99']})


def m_drawer(o, d):
    o['body'].append({'drawer': 'no-such-brief', 'label': 'Nowhere'})


def m_cap(o, d):
    o['entry'] = 'presentation'


def m_bottom(o, d):
    b = blocks(o, 'bottom')[0]
    b['lines'] = b['lines'] + b['lines'][:2]


def m_insights(o, d):
    s = blocks(o, 'script2')[0]
    for row in s['rows']:
        if row[0] == 'Insights':
            row[1] = row[1] + row[1][:1]


def m_tempting(o, d):
    o.pop('golden', None)


def m_decides_action(o, d):
    dx_table(o)['rows'][1][-1] = {'t': 'Give prednisone now', 'ids': ['m02']}


def m_decides_dup(o, d):
    t = dx_table(o)
    t['rows'][1][-1] = copy.deepcopy(t['rows'][0][-1])


def m_g2(o, d):
    lad = ladder(o)
    for r in lad['rungs']:
        if '2nd' in r[1]:
            r[2] = {'t': 'some children', 'ids': ['m15']}


def m_g3(o, d):
    lad = ladder(o)
    lad['rungs'].insert(0, lad['rungs'].pop())


def m_currency(o, d):
    o['body'].append({'t': 'Relapse within 30 days in most', 'ids': ['N001']})


def m_population(o, d):
    o['body'].append({'t': 'Search for occult cancer by age', 'ids': ['mn7']})


def m_combined(o, d):
    pass                                            # the goldens already combine; X1 must list them


def m_label_undefined(o, d):
    for _ in range(3):
        o['body'].append({'t': 'atypical features need a biopsy', 'ids': ['n17']})


def m_old(o, d):
    o['old_claims'][0][1] = 'kept'


def m_card_missing(o, d):
    p = os.path.join(d, 'cards_disposition.json')
    c = json.load(open(p))
    c.pop(sorted(k for k in c if '.' not in k)[0])
    json.dump(c, open(p, 'w'))


def m_card_covered(o, d):
    p = os.path.join(d, 'cards_disposition.json')
    c = json.load(open(p))
    c['999'] = 'covered:step 1'
    json.dump(c, open(p, 'w'))
    open(os.path.join(d, 'cards.md'), 'a').write('\n## card 999 (test)\n- anchor (cloze): zebra stripe sign\n')


def m_card_owner(o, d):
    p = os.path.join(d, 'cards_disposition.json')
    c = json.load(open(p))
    c[sorted(c)[0]] = 'owner:no-such-brief'
    json.dump(c, open(p, 'w'))


CASES = [('S1', m_label), ('S1', m_no_h), ('S2', m_unknown), ('S2', m_plain), ('S2', m_bad_id), ('S2', m_drawer),
         ('C1', m_cap), ('C2', m_bottom), ('C2', m_insights), ('D1', m_tempting), ('D2', m_decides_action),
         ('D3', m_decides_dup), ('L1', m_g2), ('L2', m_g3), ('N1', m_currency), ('P1', m_population),
         ('X1', m_combined), ('U1', m_label_undefined), ('O1', m_old), ('K1', m_card_missing),
         ('K1', m_card_covered), ('K1', m_card_owner)]


def run(src_dir, mutate=None):
    tmp = tempfile.mkdtemp(prefix='ocheck-')
    try:
        for f in os.listdir(os.path.join(WS, src_dir)):
            if f.endswith('.json'):
                shutil.copy(os.path.join(WS, src_dir, f), tmp)
        bid = json.load(open(os.path.join(tmp, 'outline.json')))['brief']
        shutil.copy(os.path.join(WS, 'repair/migration/spine/packets', bid, 'cards.md'), os.path.join(tmp, 'cards.md'))
        o = json.load(open(os.path.join(tmp, 'outline.json')))
        if mutate:
            mutate(o, tmp)
        json.dump(o, open(os.path.join(tmp, 'outline.json'), 'w'))
        c = OC.Check(os.path.join(tmp, 'outline.json'), os.path.join(WS, 'index.html'), os.path.join(tmp, 'cards.md')).run()
        return c.errors, c.flags
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    bad = 0
    for bid, d in GOLD.items():
        e, f = run(d)
        print('%-5s golden %s: %d error(s)' % ('ok' if not e else 'FAIL', bid, len(e)))
        bad += bool(e)
        for x in e[:3]:
            print('     ', x)
    for rule, m in CASES:
        e, f = run(BASE, m)
        hit = [x for x in e + f if x.split()[1] == rule]
        print('%-5s %s %s%s' % ('ok' if hit else 'FAIL', rule, m.__name__, '' if hit else ' (not raised)'))
        bad += not hit
    print('test_outline_check: %d failure(s)' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
