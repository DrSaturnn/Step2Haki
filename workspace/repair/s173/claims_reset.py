#!/usr/bin/env python3
"""Rebuild every explicit "claims" list of a card's rewrite file from collect's own default assignment plus the
deliberate moves, so a claim that a unit merely contains is not pinned to that unit's text.

  python3 repair/s173/claims_reset.py            (all cards in MOVES)
"""
import json, re, subprocess, sys

MOVES = {
 'mood-anticonv': {'S316': 'U053', 'S318': 'U053', 'S320': 'U053', 'S324': 'U060', 'S326': 'U060', 'S328': 'U060',
                   'S332': 'U017', 'S336': 'U017', 'S338': 'U017', 'S340': 'U030', 'S342': 'U030', 'S344': 'U030'},
 'pc-benzo': {'S003': 'U004', 'S006': 'U004', 'S023': 'U007', 'S029': 'U007', 'S033': 'U009', 'S035': 'U009',
              'S040': 'U010', 'S034': 'U028'},
 'adhd-meds': {'S024': 'U051', 'S051': 'U016', 'S058': 'U017', 'S067': 'U019', 'S074': 'U035', 'S102': 'U029',
               'S126': 'U034', 'S174': 'U056'},
 'sud-meds': {'S115': 'U032', 'S125': 'U034', 'S176': 'U054', 'S194': 'U006'},
 'pc-other': {'S120': 'U005', 'S121': 'U005', 'S122': 'U005', 'S132': 'U042'},
 'pc-atypical': {'S176': 'U033', 'S178': 'U033', 'S184': 'U053', 'S186': 'U053', 'S188': 'U053', 'S190': 'U053'},
 'pc-antichol': {'S127': 'U031', 'S129': 'U031', 'S131': 'U031', 'S133': 'U031', 'S135': 'U027', 'S137': 'U027',
                 'S139': 'U027'},
 'pc-sleep': {'S102': 'U026'},
 'pc-anxiety': {'S087': 'U020', 'S103': 'U023'},
 'pc-cog': {},
}

AUTO = json.load(open('local/s173/auto_moves.json'))
for b in ('pc-typical', 'pc-td', 'pc-orexin'):
    MOVES.setdefault(b, {})

MOVES['pc-atypical'].update({'S108': 'U035', 'S183': 'U053', 'S185': 'U053', 'S187': 'U053'})
MOVES['pc-antichol'].update({'S126': 'U031', 'S128': 'U031', 'S130': 'U031'})
MOVES['mood-anticonv'].update({'S315': 'U053', 'S317': 'U053', 'S319': 'U053', 'S323': 'U060', 'S325': 'U060', 'S327': 'U060',
                               'S339': 'U030', 'S343': 'U030', 'S292': 'U098', 'S267': 'U089'})

def sh(*a):
    return subprocess.run(list(a), capture_output=True, text=True)

def folder(b):
    return sh('python3', 'tools/spine/folder_of.py', b).stdout.split('\t')[1].strip()

def check(b):
    out = sh('python3', 'tools/spine/rewrite_lanes.py', 'check', 's173', b).stdout
    return out, re.findall(r'FIX claim (S\d+) text is not in the rebuilt brief', out)

for b in (sys.argv[1:] or list(MOVES)):
    f = folder(b); p = f + '/rewrite_s173/rewrite_s173.json'
    j = json.load(open(p, encoding='utf-8'))
    mv = dict(MOVES[b]); mv.update(AUTO.get(b, {}))
    have = {u['uid'] for u in j['units']}
    for uid in sorted(set(mv.values()) - have):
        base = [u for u in json.load(open(f + '/rewrite_s173/units.json'))['units'] if u['uid'] == uid][0]
        j['units'].append({'uid': uid, 'new': base['html'], 'note': 'unchanged line; holds a claim moved to it'})
    for e in j['units'] + j['raw']:
        e.pop('claims', None)
    for r in j['raw']:
        r['claims'] = []
    json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    out, missing = check(b)
    d = json.load(open(f + '/delta_s173.json', encoding='utf-8'))
    default = {c['uid']: [u['id'] for u in c.get('claim_updates', [])] for c in d['changes']}
    U = {u['uid']: u for u in j['units']}
    for uid, ids in default.items():
        stray = [c for c in ids if c in mv and mv[c] != uid]
        if stray and uid in U:
            U[uid]['claims'] = [c for c in ids if c not in stray]
    for cid, uid in mv.items():
        if uid not in U:
            print('%s: %s target %s is not a changed unit' % (b, cid, uid)); continue
        U[uid]['claims'] = sorted(set(U[uid].get('claims') or default.get(uid, [])) | {cid})
    byold = {x['old']: x for x in j['raw']}
    gone = [c for c in d['changes'] if c['new'] == '' and c['old'] in byold]
    for c in gone:
        byold[c['old']]['claims'] = sorted((set(default.get(c['uid'], [])) | (set(missing) if c is gone[0] else set())) - set(mv))
    if missing and not gone:
        print('%s: missing claims with no removed raw: %s' % (b, missing))
    json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    out, missing = check(b)
    print(b, out.strip().split('\n')[-1], '| still missing', missing[:8])
