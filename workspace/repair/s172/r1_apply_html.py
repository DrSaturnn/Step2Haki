#!/usr/bin/env python3
"""s172 chat 2: the 9 round 1 pairs r1_apply.py left (receipt quoted display text; the rewrite holds HTML).
Exact HTML replacements; each old must occur once across the brief's entries."""
import json, subprocess
WS = '/home/claude/Step2Haki/workspace'
P = [
 ('ssri-effects', 'Relapse: typically <b>2 to 3 weeks or more</b> after a stop or taper', 'Depressive relapse: typically <b>2 to 3 weeks or more</b> after a stop'),
 ('ssri-effects', '<i>Bipolar Disorder</i>: mood rises after the SSRI starts (antidepressant-induced mania is rare).', '<i>Bipolar Disorder</i>: antidepressant-induced mania after the SSRI starts (rare).'),
 ('lithium-effects', '<b>Amiloride</b> blocks that entry, so it can treat the diabetes insipidus when lithium must continue', '<b>Amiloride</b> blocks lithium entry through the epithelial sodium channel, so it can treat nephrogenic diabetes insipidus when lithium must continue'),
 ('lithium-effects', '&uarr; TSH, normal free thyroxine', '&uarr; TSH (thyroid-stimulating hormone), normal free thyroxine'),
 ('lithium-effects', ': the TSH of 5.5 is mildly high', ': the TSH (thyroid-stimulating hormone) of 5.5 is mildly high'),
 ('lithium-effects', '<i>Thyroid Disease in an Adult</i>: reading the TSH.', '<i>Thyroid Disease in an Adult</i>: reading the TSH (thyroid-stimulating hormone).'),
 ('ipv', 'Abuse unnamed in the history', 'Abuse not disclosed'),
 ('disruptive-behavior', '<tr><th>When</th><th>Management</th></tr>', '<tr><th>When</th><th>Prognosis</th></tr>'),
 ('suicide-risk', 'Not recommended: a safety plan replaces it', 'Not recommended'),
]
for bid, old, new in P:
    fo = subprocess.run(['python3', WS + '/tools/spine/folder_of.py', bid], capture_output=True, text=True).stdout.split()[-1]
    p = '%s/%s/rewrite_s172/rewrite_s172.json' % (WS, fo)
    rw = json.load(open(p))
    hits = [e for e in rw.get('units', []) + rw.get('raw', []) if old in e.get('new', '')]
    if len(hits) == 1 and hits[0]['new'].count(old) == 1:
        hits[0]['new'] = hits[0]['new'].replace(old, new)
        json.dump(rw, open(p, 'w'), ensure_ascii=False, indent=1)
        print('applied', bid, hits[0].get('uid', 'raw'))
    else:
        print('MISS', bid, len(hits), old[:60])
