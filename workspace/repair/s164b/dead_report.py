#!/usr/bin/env python3
"""dead_report: reads dead_decls.js output; a declaration is dead when, in every view/config, it is live on no element it
matches (rules outside their media or matching nothing in a run count as no evidence there).
  python3 repair/s164b/dead_report.py DEAD.json [--list]"""
import json, sys, collections
d = json.load(open(sys.argv[1])); runs = list(d)
css = {r['i']: r for r in json.load(open('local/s164b/css_rules.json'))['rules']}
agg = collections.defaultdict(lambda: [0, 0, 0])   # (i, prop) -> matched, live, runs with evidence
unk = collections.Counter()
for run in runs:
    for i, v in d[run].items():
        if isinstance(v, str):
            unk[v] += 1; continue
        for p, (n, l) in v.items():
            a = agg[(int(i), p)]; a[0] += n; a[1] += l; a[2] += 1
dead = [k for k, a in agg.items() if a[1] == 0 and a[0] > 0]
part = [k for k, a in agg.items() if 0 < a[1] < a[0]]
print('runs', len(runs), 'decls with evidence', len(agg), 'dead', len(dead), 'partly live', len(part), 'no evidence', dict(unk))
if '--list' in sys.argv:
    for k in sorted(dead):
        print('DEAD', k[0], k[1], css[k[0]]['sel'][:90])
json.dump({'dead': sorted(dead), 'part': sorted(part)}, open(sys.argv[1].replace('.json', '_sum.json'), 'w'))
