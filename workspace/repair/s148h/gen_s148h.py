#!/usr/bin/env python3
"""s148h (psych per-choice reasons and First step pairing; DECISIONS_DIGEST 2026-10-20; claude/pending/SITE_S148G.md):
writes repair/s148h/*.json from the live page.

  10_reasons.json    three set_attr ops per practice item (data-key-why, data-d1-why, data-d2-why) for the 23 briefs,
                     from data/src/<brief>.txt (one line per item: id prefix | key | d1 | d2), merged into data/reasons.json
  30_prose.json      the two prose-rule warnings (lint.py) left in these briefs, both in re-rendered First step bands
  20_firststep.json  First step split for the bands in data/pairs.json, via repair/s148g/w5split.py (one row group per
                     order, each spanning only its own results; text, masks and hovers carried byte for byte)

Checks (the run fails on any): every item of every brief has exactly three reasons and no reason names an unknown item;
each reason is 3 to 14 words, one line, with no em or en dash, arrow or HTML; the set_attr ops leave every brief
byte-identical apart from the three new attributes. Reports (data/checks.json, counts printed): the row-reuse check (a
distractor that names a differential row: the reason's content words must come from that row) and the wording check
(every reason's content words found in the brief's own text: its tables, hovers, items and explanations).

  python3 repair/s148h/gen_s148h.py [--page index.html]
"""
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
sys.path.insert(0, os.path.join(WS, 'repair', 's148g'))
sys.path.insert(0, HERE)
from pagelib import read_page, brief_by_id  # noqa: E402
import w5split  # noqa: E402
import extract as X  # noqa: E402

NOTE = 's148h (Jonathan 2026-10-20: per-choice reasons; First step split)'
ORDER = ('psychosis-duration voices sz-psychosocial bipolar-mania mdd cluster-b panic somatic gppd delirium toxidrome '
         'substance psych-medical disruptive-behavior ssri-effects antipsych-effects lithium-effects tca-tox suicide-risk '
         'ipv tics peds-sleep bs-learning').split()
PROSE = [('psychosis-duration', '>Chase the medical cause<', '>Treat the medical cause<'),
         ('mdd', '>Abnormal TSH or a culprit exposure<', '>Abnormal TSH or a causative drug or substance<')]
ATTRS = ('data-key-why', 'data-d1-why', 'data-d2-why')
STOP = set('''a an the and or of to in on for with by at as from is are be not no only than then this that it its his her
their he she they them him we you here there now any each per via into out over under more most less least very
needs need requires one is was has have none also when without these those'''.split())
ERRS = []
FRAME = set('needs need requires here not no only now yet first instead'.split())


def words(s):
    return [w for w in re.findall(r"[a-z0-9]+(?:'[a-z]+)?", s.lower().replace('-', ' ')) if w not in STOP]


def stem_word(w):
    for suf in ('ing', 'es', 's', 'ed'):
        if len(w) > 4 and w.endswith(suf):
            return w[:-len(suf)]
    return w


def bag(s):
    return {stem_word(w) for w in words(s)}


def load_src(bid):
    rows = {}
    for n, line in enumerate(open(os.path.join(HERE, 'data', 'src', bid + '.txt'), encoding='utf-8'), 1):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(' | ')]
        assert len(parts) == 4, '%s line %d: want "id | key | d1 | d2", got %d parts' % (bid, n, len(parts))
        assert parts[0] not in rows, '%s line %d: %s twice' % (bid, n, parts[0])
        rows[parts[0]] = parts[1:]
    return rows


def check_reason(bid, iid, k, r):
    bad = []
    n = len(r.split())
    if not 3 <= n <= 14:
        bad.append('%d words' % n)
    if re.search('[—–→<>\n]', r) or '&' in r:
        bad.append('dash, arrow, markup or ampersand')
    if r != r.strip() or '  ' in r:
        bad.append('spacing')
    if r.endswith('.'):
        bad.append('trailing period')
    if bad:
        ERRS.append('%s %s %s: %r: %s' % (bid, iid, ATTRS[k], r, ', '.join(bad)))


def diff_rows(t):
    """the brief's differential table (the first table whose header names Fingerprint): {normalized name: row text}"""
    for rows in X.tables(t):
        if rows and 'Fingerprint' in rows[0] or (rows and 'Illness script' in rows[0]):
            out = {}
            for r in rows[1:]:
                cells = r.split(' | ')
                out[norm(cells[0])] = ' '.join(cells)
            return out
    return {}


def norm(name):
    return re.sub(r'\s+', ' ', re.sub(r'\(.*?\)', '', name.lower())).strip(' ,.')


def row_for(choice, rows):
    c = norm(choice)
    if c in rows:
        return c
    for k in rows:   # a choice may carry a qualifier the row name lacks ("Schizoaffective disorder, bipolar type")
        if k and (c.startswith(k + ',') or c == k.split(',')[0]):
            return k
    return None


def main(argv):
    page = argv[argv.index('--page') + 1] if '--page' in argv else os.path.join(WS, 'index.html')
    pg = read_page(page)
    reasons, ops, checks = {}, [], {'row_reuse': [], 'wording': [], 'counts': {}}
    for bid in ORDER:
        b = brief_by_id(pg, bid)
        t = pg[b.start:b.end]
        items = X.items(t)
        src = load_src(bid)
        full = {}
        for pre in src:
            hit = [it for it in items if it['id'].startswith(pre)]
            assert len(hit) == 1, '%s: prefix %s matches %d items' % (bid, pre, len(hit))
            full[hit[0]['id']] = src[pre]
        missing = [it['id'] for it in items if it['id'] not in full]
        assert not missing, '%s: no reasons for %s' % (bid, ', '.join(missing))
        rows = diff_rows(t)
        text_bag = bag(X.plain(re.sub(r'<span class="sp-pop-b"', '<span class="x"', t)) + ' ' +
                       ' '.join(' '.join([it['stem'], it['key'], it['d1'], it['d2'], it['expl'], it['lead']]) for it in items))
        reasons[bid] = {}
        nrow = nword = 0
        for it in items:
            rs = full[it['id']]
            for k, r in enumerate(rs):
                check_reason(bid, it['id'], k, r)
            reasons[bid][it['id']] = rs
            for k, choice in enumerate((it['key'], it['d1'], it['d2'])):
                rk = row_for(choice, rows)
                if rk and k:   # distractors only: the one-owner rule
                    nrow += 1
                    extra = sorted(bag(rs[k]) - bag(rows[rk]) - {stem_word(w) for w in FRAME} - bag(it['stem']))
                    if extra:
                        checks['row_reuse'].append({'brief': bid, 'item': it['id'], 'attr': ATTRS[k], 'choice': choice,
                                                    'reason': rs[k], 'row': rows[rk], 'words_not_in_row': extra})
                miss = sorted(bag(rs[k]) - text_bag - {stem_word(w) for w in FRAME})
                if miss:
                    nword += 1
                    checks['wording'].append({'brief': bid, 'item': it['id'], 'attr': ATTRS[k], 'reason': rs[k],
                                              'words_not_in_brief': miss})
                ops.append({'op': 'set_attr', 'target': it['id'], 'attr': ATTRS[k], 'value': rs[k], 'note': NOTE})
        checks['counts'][bid] = {'items': len(items), 'distractor_rows': nrow}
    assert not ERRS, 'reason format:\n' + '\n'.join(ERRS)
    json.dump({'_doc': 's148h per-choice reasons [key, d1, d2] per item, by brief in sidebar order (written by '
                       'gen_s148h.py from data/src/*.txt)', **reasons},
              open(os.path.join(HERE, 'data', 'reasons.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    json.dump({'edits': ops}, open(os.path.join(HERE, '10_reasons.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)

    pairs = json.load(open(os.path.join(HERE, 'data', 'pairs.json'), encoding='utf-8'))
    fops = []
    for bid in [k for k in ORDER if k in pairs]:
        b = brief_by_id(pg, bid)
        h = pg[b.start:b.end]
        for band, pair in sorted(pairs[bid], reverse=True):   # later bands first: a split adds .w5b groups
            old, new = w5split.split(h, band, pair)
            assert h.count(old) == 1
            h = h.replace(old, new, 1)
            fops.append({'op': 'replace', 'brief': bid, 'find': old, 'with': new, 'note': NOTE})
    json.dump({'edits': fops}, open(os.path.join(HERE, '20_firststep.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)
    # s148f prose sweep (repair/s148f/prose_sweep.md: "content fixes go to each brief's next batch"): the two lint prose
    # warnings left in these 23 briefs, both in First step bands this batch re-renders; applied after the split
    pops = []
    for bid, old, new in PROSE:
        h = pg[brief_by_id(pg, bid).start:brief_by_id(pg, bid).end]
        assert h.count(old) == 1, (bid, old)
        pops.append({'op': 'replace', 'brief': bid, 'find': old, 'with': new, 'note': NOTE + '; prose rule 2026-10-19'})
    json.dump({'edits': pops}, open(os.path.join(HERE, '30_prose.json'), 'w', encoding='utf-8'), indent=1,
              ensure_ascii=False)
    json.dump(checks, open(os.path.join(HERE, 'data', 'checks.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    n = sum(len(v) for v in reasons.values())
    print('gen_s148h: %d briefs, %d items, %d reasons (10_reasons.json %d ops); First step %d band(s) in %d brief(s)'
          % (len(reasons), n, 3 * n, len(ops), len(fops), len({o['brief'] for o in fops})))
    print('checks: row reuse %d of %d distractor-row reasons carry words not in the row; wording %d reasons carry words '
          'not in the brief (data/checks.json)' % (len(checks['row_reuse']),
                                                  sum(c['distractor_rows'] for c in checks['counts'].values()),
                                                  len(checks['wording'])))


if __name__ == '__main__':
    main(sys.argv)
