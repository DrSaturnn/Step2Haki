#!/usr/bin/env python3
"""Round 1 lead fix (s175): meaning-lock waivers for three approved review replacements that restate a negation. Run once from workspace/."""
import json, subprocess
def F(b): return subprocess.run(['python3', 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip() + '/rewrite_s175/rewrite_s175.json'
for b, kind, key, toks in (('cough', 'units', 'U033', ['negation', 'negation 1 of 2', '1 of 2', 'no']),
                           ('feeding-refusal', 'raw', 1, ['negation', 'negation 1 of 2', '1 of 2', 'no', 'decoy']),
                           ('cyclic-vomiting', 'raw', 1, ['negation', 'negation 0 of 1', '0 of 1', 'no'])):
    d = json.load(open(F(b)))
    e = next(x for x in d['units'] if x['uid'] == key) if kind == 'units' else d['raw'][key]
    e['lock_ok'] = sorted(set(e.get('lock_ok', []) + toks))
    e['lock_reason'] = (e.get('lock_reason', '') + '; round 1 review replacement restates the negation (lead)').strip('; ')
    json.dump(d, open(F(b), 'w'), indent=1, ensure_ascii=False)
