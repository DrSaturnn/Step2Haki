#!/usr/bin/env python3
"""Receipts to decisions: python3 repair/s172e/decide.py LANES_DIR OUT_DIR

Reads judge_1/receipt.md, judge_2/receipt.md and second/receipt.md (pipe lines: pop | KEEP/MOVE/LABEL | where | text |
reason), checks every hover of rows.json has one verdict, prints the counts and the agreement of the second read on
KEEP against not-KEEP, and writes OUT_DIR/verdicts.json, decisions_move.json (anchors.py apply format) and
labels_pending.json.
"""
import json
import os
import sys


def parse(path):
    out, bad = {}, []
    for ln in open(path, encoding='utf-8'):
        ln = ln.strip().strip('`')
        if '|' not in ln:
            continue
        f = [x.strip().strip('`') for x in ln.split('|')]
        if len(f) < 5 or f[1] not in ('KEEP', 'MOVE', 'LABEL'):
            bad.append(ln[:120])
            continue
        if f[0] in out:
            bad.append('duplicate ' + f[0])
        out[f[0]] = {'verdict': f[1], 'where': f[2], 'text': f[3], 'reason': ' | '.join(f[4:])}
    return out, bad


def main():
    lanes, outd = sys.argv[1], sys.argv[2]
    rows = json.load(open(os.path.join(lanes, 'rows.json')))
    v, bad = {}, []
    for n in ('judge_1', 'judge_2'):
        a, b = parse(os.path.join(lanes, n, 'receipt.md'))
        v.update(a)
        bad += b
    ids = [r['pop'] for r in rows]
    missing = [i for i in ids if i not in v]
    extra = [i for i in v if i not in ids]
    cnt = {k: sum(1 for i in ids if i in v and v[i]['verdict'] == k) for k in ('KEEP', 'MOVE', 'LABEL')}
    print('verdicts: %s; missing %d; unknown ids %d; bad lines %d' % (cnt, len(missing), len(extra), len(bad)))
    for x in (missing + extra + bad)[:20]:
        print('  ! ' + x)
    s, sb = parse(os.path.join(lanes, 'second', 'receipt.md'))
    both = [i for i in s if i in v]
    agree = [i for i in both if (s[i]['verdict'] == 'KEEP') == (v[i]['verdict'] == 'KEEP')]
    print('second read: %d rows, agree on KEEP against not-KEEP %d of %d' % (len(s), len(agree), len(both)))
    os.makedirs(outd, exist_ok=True)
    json.dump({i: v[i] for i in ids if i in v}, open(os.path.join(outd, 'verdicts.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(s, open(os.path.join(outd, 'second.json'), 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(outd, 'disagree.md'), 'w') as f:
        by = {r['pop']: r for r in rows}
        for i in both:
            if i not in agree:
                r = by[i]
                f.write('- %s (%s) trigger "%s" | title "%s" | judge %s %s (%s) | second %s %s (%s)\n' % (
                    i, r['brief'], r['trigger'], r['title'], v[i]['verdict'], v[i]['text'], v[i]['reason'],
                    s[i]['verdict'], s[i]['text'], s[i]['reason']))
    mv = {}
    for i in ids:
        d = v.get(i)
        if d and d['verdict'] == 'MOVE':
            mv[i] = {'verdict': 'move', 'term': d['text']}
            if d['where'].lower().startswith('row'):
                mv[i]['cell'] = 'row'
    json.dump(mv, open(os.path.join(outd, 'decisions_move.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump({i: {'verdict': 'own', 'label': v[i]['text'], 'reason': v[i]['reason']} for i in ids
               if i in v and v[i]['verdict'] == 'LABEL'}, open(os.path.join(outd, 'labels_pending.json'), 'w'),
              indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
