#!/usr/bin/env python3
"""H5, usage ledger (run by the lead after each wave; not a hook). Reads every subagent transcript and writes measured
calls and tokens per agent, with its role, wave, requested model (agent-<id>.meta.json) and the models that served it
(T5, T6), to repair/efficiency/ledger_spine.csv (one row per agent, rewritten in place).

  python3 tools/hooks/usage_ledger.py [--wave ID]     print the table (and the wave total) and update the CSV
  python3 tools/hooks/usage_ledger.py --lead           the lead's own calls and tokens per session transcript (item 3)
  python3 tools/hooks/usage_ledger.py --context        start-up context of the lead and of each agent, against
                                                       repair/efficiency/context_baseline.json (item 9; run at batch start)
"""
import csv
import glob
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

OUT = os.path.join(C.WS, 'repair', 'efficiency', 'ledger_spine.csv')
COLS = ['agent_id', 'wave', 'role', 'plan_step', 'lane', 'model_requested', 'models_served', 'calls', 'input',
        'cache_write', 'cache_read', 'output', 'output_est', 'tokens', 'transcript']


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
                    'cache_read': u['cache_read'], 'output': u['output'], 'output_est': u['output_est'], 'tokens': u['tokens'], 'transcript': p})
    return out


BASE = os.path.join(C.WS, 'repair', 'efficiency', 'context_baseline.json')


def lead(argv):
    for p in C.lead_transcripts():
        u, f = C.usage(p), C.first_context(p) or {}
        print('lead %s calls=%d tokens=%d (input %d, cache write %d, cache read %d, output est %d); start-up context %d'
              % (os.path.basename(p)[:8], u['calls'], u['tokens'], u['input'], u['cache_write'], u['cache_read'],
                 u['output_est'], sum(f.values())))
    return 0


def context(argv):
    """warn when a start-up context has grown more than 10% past its baseline (a grown tool list shows here first)"""
    base = json.load(open(BASE, encoding='utf-8')) if os.path.exists(BASE) else {}
    now = {}
    ls = C.lead_transcripts()
    if ls:
        now['lead'] = sum((C.first_context(ls[-1]) or {}).values())
    by_sha = {l['prompt_sha']: l for l in C.launches()}
    for p in glob.glob(os.path.join(C.PROJECTS, '*', '*', 'subagents', 'agent-*.jsonl')):
        l = by_sha.get(C.sha(C.first_user_text(p)))
        f = C.first_context(p)
        if l and f:
            k = 'agent:%s:%s' % (l.get('agent_type') or 'general-purpose', l.get('model'))
            now[k] = min(now.get(k, 10 ** 9), sum(f.values()))
    warn = 0
    for k in sorted(now):
        b = (base.get(k) or {}).get('tokens')
        flag = ''
        if b and now[k] > 1.10 * b:
            flag, warn = '  WARNING: %.0f%% above baseline %d' % (100.0 * now[k] / b - 100, b), warn + 1
        print('%-40s %8d%s' % (k, now[k], flag if b else '  (no baseline)'))
    if '--set' in argv:
        for k, v in now.items():
            base[k] = {'tokens': v, 'set': time.strftime('%Y-%m-%d')}
        json.dump(base, open(BASE, 'w', encoding='utf-8'), indent=1, sort_keys=True)
        print('baseline written: %s' % os.path.relpath(BASE, C.WS))
    return 1 if warn else 0


def main(argv):
    if '--lead' in argv:
        return lead(argv)
    if '--context' in argv:
        return context(argv)
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
