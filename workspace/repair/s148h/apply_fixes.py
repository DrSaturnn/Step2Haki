#!/usr/bin/env python3
"""s148h S5: apply a fix list (data/r1_fixes.tsv: brief, item prefix or *, slot key|d1|d2 or *, old, new, finding) to the
reason sources data/src/<brief>.txt (one line per item: id prefix | key | d1 | d2). Each fix must match exactly one
reason (the old text in that slot of that item; * searches every item or slot) or the run fails and writes nothing.
Then run gen_s148h.py to rebuild 10_reasons.json and data/reasons.json.

  python3 repair/s148h/apply_fixes.py data/r1_fixes.tsv [--dry]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLOT = {'key': 1, 'd1': 2, 'd2': 3}


def main(argv):
    fx = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, argv[0]), encoding='utf-8') if l.strip() and not l.startswith('#')]
    src, errs, n = {}, [], 0
    for f in fx:
        if len(f) != 6:
            errs.append('bad row: %r' % f)
            continue
        b, item, slot, old, new, why = f
        if b not in src:
            src[b] = [l.split(' | ') for l in open(os.path.join(HERE, 'data', 'src', b + '.txt'), encoding='utf-8').read().splitlines()]
        hits = [(r, s) for r in src[b] if item == '*' or r[0].startswith(item)
                for s in ([SLOT[slot]] if slot != '*' else [1, 2, 3]) if r[s] == old]
        if len(hits) != 1:
            errs.append('%s %s %s: %d match(es) for "%s"' % (b, item, slot, len(hits), old))
            continue
        r, s = hits[0]
        r[s] = new
        n += 1
    if errs:
        sys.exit('apply_fixes: nothing written\n' + '\n'.join(errs))
    if '--dry' not in argv:
        for b, rows in src.items():
            open(os.path.join(HERE, 'data', 'src', b + '.txt'), 'w', encoding='utf-8').write('\n'.join(' | '.join(r) for r in rows) + '\n')
    print('apply_fixes: %d fix(es) in %d brief(s)%s' % (n, len(src), ' (dry run)' if '--dry' in argv else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
