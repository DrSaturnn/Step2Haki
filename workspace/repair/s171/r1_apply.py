#!/usr/bin/env python3
"""s171 chat 2: apply round 1 PASS-IF replacement pairs ({{old}} -> {{new}}) from the lane receipts to each brief's
rewrite_s171/rewrite_s171.json (unit or raw "new" html), where the old text occurs exactly once across the changed
entries. Writes local/s171/r1_pairs.md (applied / left for the fix lanes)."""
import glob, json, re, subprocess, sys
WS = '/home/claude/Step2Haki/workspace'
rows, left = [], []
pairs = {}
for rp in sorted(glob.glob(WS + '/repair/efficiency/lanes/s171/r1/lane_*/receipt.md')):
    txt = open(rp).read()
    for sec in re.split(r'^=== ', txt, flags=re.M)[1:]:
        head = sec.split('\n', 1)[0].split()
        bid, part = head[0], head[1] if len(head) > 1 else '?'
        for m in re.finditer(r'(\d+)\. old: \{\{(.*?)\}\}\s*\n\s*new: \{\{(.*?)\}\}', sec, flags=re.S):
            pairs.setdefault(bid, []).append((part, m.group(1), m.group(2), m.group(3)))
for bid, ps in pairs.items():
    fo = subprocess.run(['python3', WS + '/tools/spine/folder_of.py', bid], capture_output=True, text=True).stdout.split()[-1]
    p = '%s/%s/rewrite_s171/rewrite_s171.json' % (WS, fo)
    rw = json.load(open(p))
    ents = rw.get('units', []) + rw.get('raw', [])
    for part, n, old, new in ps:
        hits = [e for e in ents if old in e.get('new', '')]
        if len(hits) == 1 and hits[0]['new'].count(old) == 1:
            hits[0]['new'] = hits[0]['new'].replace(old, new)
            rows.append('- %s %s %s: applied (%s)' % (bid, part, n, hits[0].get('uid', 'raw')))
        else:
            left.append('- %s %s %s: %d hit(s). old: {{%s}} new: {{%s}}' % (bid, part, n, len(hits), old, new))
    json.dump(rw, open(p, 'w'), ensure_ascii=False, indent=1)
open(WS + '/local/s171/r1_pairs.md', 'w').write('# r1 pairs\n\n## Applied\n' + '\n'.join(rows) + '\n\n## Left for the fix lanes\n' + '\n'.join(left) + '\n')
print('applied %d, left %d' % (len(rows), len(left)))
