#!/usr/bin/env python3
"""H5, usage ledger (run by the lead after each wave; not a hook). Reads every subagent transcript and writes measured
calls and tokens per agent, with its role, wave, requested model (agent-<id>.meta.json) and the models that served it
(T5, T6), to repair/efficiency/ledger_spine.csv (one row per agent, rewritten in place).

  python3 tools/hooks/usage_ledger.py [--wave ID]     print the table (and the wave total) and update the CSV
"""
import csv
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

OUT = os.path.join(C.WS, 'repair', 'efficiency', 'ledger_spine.csv')
COLS = ['agent_id', 'wave', 'role', 'plan_step', 'lane', 'model_requested', 'models_served', 'calls', 'input',
        'cache_write', 'cache_read', 'output', 'tokens', 'transcript']


def rows():
    by_sha = {l['prompt_sha']: l for l in C.launches()}
    out = []
    for p in sorted(glob.glob(os.path.join(C.PROJECTS, '*', '*', 'subagents', 'agent-*.jsonl'))):
        aid = os.path.basename(p)[len('agent-'):-len('.jsonl')]
        text = C.first_user_text(p)
        h = C.header(text)
        l = by_sha.get(C.sha(text), {})
        meta = p[:-len('.jsonl')] + '.meta.json'
        req = ''
        if os.path.exists(meta):
            try:
                req = json.load(open(meta, encoding='utf-8')).get('model', '')
            except ValueError:
                pass
        u = C.usage(p)
        out.append({'agent_id': aid, 'wave': l.get('wave', ''), 'role': h.get('role', ''), 'plan_step': h.get('plan_step', ''),
                    'lane': h.get('lane', ''), 'model_requested': req, 'models_served': ' '.join(u['models']),
                    'calls': u['calls'], 'input': u['input'], 'cache_write': u['cache_write'],
                    'cache_read': u['cache_read'], 'output': u['output'], 'tokens': u['tokens'], 'transcript': p})
    return out


def main(argv):
    wave = argv[argv.index('--wave') + 1] if '--wave' in argv else None
    rs = rows()
    old = {}
    if os.path.exists(OUT):
        for r in csv.DictReader(open(OUT, encoding='utf-8')):
            old[r['agent_id']] = r
    for r in rs:
        old[r['agent_id']] = r
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        for k in sorted(old):
            w.writerow({c: old[k].get(c, '') for c in COLS})
    shown = [r for r in rs if wave is None or r['wave'] == wave]
    for r in shown:
        print('%-18s %-8s %-14s req=%-7s served=%-22s calls=%-4s tokens=%s' % (
            r['agent_id'], r['wave'] or '-', r['role'] or '-', r['model_requested'] or '-', r['models_served'] or '-',
            r['calls'], r['tokens']))
    print('ledger: %d agent(s) shown, %d calls, %d tokens; %s' % (
        len(shown), sum(int(r['calls']) for r in shown), sum(int(r['tokens']) for r in shown), os.path.relpath(OUT, C.WS)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
