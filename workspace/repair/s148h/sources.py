#!/usr/bin/env python3
"""s148h: where each per-choice reason comes from, for the acc and flags reviewers (SITE_S148G.md source rule: a distractor
that is a differential row reuses that row's wording; any other reason cites claim-map facts like any claim).

For every reason: the brief line whose words cover it best (a table row, or the item's own explanation or stem), and the
claim ids (claim_map.json new_text) that teach those words, with the covered share. Page text and claim ids only; no
quotes (the quotes stay in each folder's claim_map.json, local-only).

  python3 repair/s148h/sources.py [--page index.html]     writes repair/s148h/data/sources/<brief>.md and a summary line
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, os.path.join(WS, 'tools', 'hooks'))
sys.path.insert(0, HERE)
from pagelib import read_page, brief_by_id  # noqa: E402
import extract as X  # noqa: E402
import gen_s148h as G  # noqa: E402
import ready_gate  # noqa: E402

ATTR = ('key', 'd1', 'd2')


def cover(r, seg):
    a = G.bag(r) - {G.stem_word(w) for w in G.FRAME}
    return (len(a & G.bag(seg)) / len(a)) if a else 1.0


def main(argv):
    page = argv[argv.index('--page') + 1] if '--page' in argv else os.path.join(WS, 'index.html')
    pg = read_page(page)
    reasons = json.load(open(os.path.join(HERE, 'data', 'reasons.json'), encoding='utf-8'))
    folders = ready_gate.folders()
    os.makedirs(os.path.join(HERE, 'data', 'sources'), exist_ok=True)
    low = tot = 0
    for bid in G.ORDER:
        t = pg[brief_by_id(pg, bid).start:brief_by_id(pg, bid).end]
        items = {it['id']: it for it in X.items(t)}
        rows = [('table T%d' % n, r) for n, rs in enumerate(X.tables(t), 1) for r in rs[1:]]
        claims = []
        if bid in folders:
            cm = json.load(open(os.path.join(folders[bid], 'claim_map.json'), encoding='utf-8'))
            claims = [(c['id'], c.get('new_text') or '') for c in cm.get('claims', []) if c.get('new_text')]
        out = ['# %s: sources of the per-choice reasons (s148h)' % bid, '',
               'Folder: %s' % (os.path.relpath(folders[bid], WS) if bid in folders else 'none (non-spine brief; page text only)'),
               'Each reason: its best brief line (share of its content words found there) and up to 3 claim ids.', '']
        for iid, rs in reasons[bid].items():
            it = items[iid]
            out.append('## %s  key: %s | d1: %s | d2: %s' % (iid[:10], it['key'], it['d1'], it['d2']))
            segs = rows + [('item explanation', it['expl']), ('item stem', it['stem'])]
            for k, r in enumerate(rs):
                best = max(segs, key=lambda s: cover(r, s[1]))
                sc = cover(r, best[1])
                cl = sorted(claims, key=lambda c: -cover(r, c[1]))[:3]
                cl = [c for c in cl if cover(r, c[1]) >= 0.34]
                tot += 1
                low += sc < 0.6
                out.append('- %s why: "%s"' % (ATTR[k], r))
                out.append('  - best line (%d%%, %s): %s' % (round(100 * sc), best[0], best[1][:220]))
                if cl:
                    out.append('  - claims: ' + '; '.join('%s "%s"' % (c[0], c[1][:90]) for c in cl))
            out.append('')
        open(os.path.join(HERE, 'data', 'sources', bid + '.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('sources: %d reasons; %d with under 60%% of their content words on one brief line (data/sources/*.md)' % (tot, low))


if __name__ == '__main__':
    main(sys.argv)
