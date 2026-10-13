#!/usr/bin/env python3
"""board_index: the board-evidence topic index, built once (s135 efficiency item 5), so runbook step S1 looks a brief's
board sources up instead of searching the local UWorld and NBME question files, the AnKing deck and the page's NBME
items again for every brief.

  python3 tools/spine/board_index.py build                 one pass over every source, every brief (about a minute)
  python3 tools/spine/board_index.py show <brief> [--cards N] [--all]
                                                           the brief's hits: question items (file, header, ids, key),
                                                           page NBME items, coverage rows, AnKing cards (Step 2 first)
  python3 tools/spine/board_index.py terms <brief> "term" ...   add search terms for a brief, then rebuild

Terms per brief: its page title split into names, its other names from repair/efficiency/ALIASES.json, and any terms
added in repair/efficiency/board_terms.json (committed: terms are not vendor text). A term matches on a word boundary,
case-insensitive. The index itself holds pointers and short card text, so it is local-only:
repair/sources/board_index.json (tools/local_only.txt covers repair/sources/). Card and question words stay evidence,
never page text (cards_search.py rules).
"""
import csv
import glob
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.dirname(HERE))
import pagelib as P  # noqa: E402

SRC = os.path.join(WS, 'repair', 'sources')
OUT = os.path.join(SRC, 'board_index.json')
TERMS = os.path.join(WS, 'repair', 'efficiency', 'board_terms.json')
ALIASES = os.path.join(WS, 'repair', 'efficiency', 'ALIASES.json')
COVERAGE = os.path.join(WS, 'repair', 'nbme', 'coverage.csv')
STOP = {'and', 'or', 'the', 'of', 'in', 'a', 'an', 'vs', 'versus', 'with', 'to', 'for', 'on', 'by', 'its', 'child',
        'children', 'adult', 'adults', 'disorder', 'disorders', 'problems', 'effects', 'therapy', 'syndrome'}


def title_terms(title):
    parts = re.split(r'\s*(?:/|:|;|,|\(|\)|\bvs\.?\b|\band\b|\bor\b|&|\+)\s*', title)
    out = []
    for p in parts:
        p = re.sub(r'\s+', ' ', p).strip(' .-')
        if len(p) < 4 or p.lower() in STOP:
            continue
        out.append(p)
    return out


def alias_terms(bid, title):
    try:
        a = json.load(open(ALIASES, encoding='utf-8'))
    except (OSError, ValueError):
        return []
    out, tl = [], title.lower()
    for e in a.get('entries', []) if isinstance(a, dict) else []:
        names = [e.get('name', '')] + list(e.get('aliases') or [])
        if bid in (e.get('briefs') or []) or any(n and n.lower() in tl for n in names):
            out += [n for n in names if n]
    return out


def brief_terms(bid, title, extra):
    seen, out = set(), []
    for t in title_terms(title) + alias_terms(bid, title) + list(extra.get(bid, [])):
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out


def question_items():
    out = []
    for p in sorted(glob.glob(os.path.join(SRC, 's*_questions.md'))):
        cur = None
        for line in open(p, encoding='utf-8'):
            if line.startswith('## '):
                if cur:
                    out.append(cur)
                cur = {'file': os.path.relpath(p, WS), 'header': line[3:].strip(), 'ids': [], 'key': '', 'text': ''}
                continue
            if cur is None:
                continue
            s = line.strip()
            m = re.match(r'-\s*(nbme_id|qid|uworld[_ ]?(?:qid|id)?|id)\s*:\s*(.+)', s, re.I)
            if m:
                cur['ids'].append('%s %s' % (m.group(1).lower(), m.group(2).split()[0]))
            m = re.match(r'-\s*key\s*:\s*(.+)', s, re.I)
            if m:
                cur['key'] = m.group(1)[:120]
            cur['text'] += ' ' + s
        if cur:
            out.append(cur)
    return out


def rx(terms):
    return [(t, re.compile(r'\b' + re.escape(t), re.I)) for t in terms]


def build(argv):
    t0 = time.time()
    html = P.read_page(os.path.join(WS, 'index.html'))
    extra = json.load(open(TERMS, encoding='utf-8')) if os.path.exists(TERMS) else {}
    bl = [b for b in P.briefs(html) if b.id]
    idx = {b.id: {'title': b.title, 'terms': brief_terms(b.id, b.title, extra), 'questions': [], 'nbme_items': [],
                  'coverage': [], 'anki': []} for b in bl}
    pats = {bid: rx(v['terms']) for bid, v in idx.items()}
    for q in question_items():
        for bid, ps in pats.items():
            hit = [t for t, r in ps if r.search(q['header'] + ' ' + q['text'])]
            if hit:
                idx[bid]['questions'].append({'file': q['file'], 'header': q['header'], 'ids': q['ids'],
                                              'key': q['key'], 'terms': hit})
    for it in P.items(html):
        if it.brief_id in idx and 'How NBME framed it' in it.inner:
            idx[it.brief_id]['nbme_items'].append(it.id)
    if os.path.exists(COVERAGE):
        for r in csv.DictReader(open(COVERAGE, encoding='utf-8')):
            if r.get('brief') in idx:
                idx[r['brief']]['coverage'].append({k: r.get(k, '') for k in ('nbme_id', 'sort', 'item_id', 'task',
                                                                               'result', 'note')})
    # one pass over the deck: a cheap lowercase substring screen per brief, then the word-boundary test
    low = {bid: [(t.lower(), r) for t, r in ps] for bid, ps in pats.items()}
    ncards = 0
    for line in open(os.path.join(SRC, 'anki', 'anki_index.jsonl'), encoding='utf-8'):
        c = json.loads(line)
        hay = (c.get('text') or '') + ' ' + (c.get('extra') or '')
        hl = hay.lower()
        ncards += 1
        uw = (c.get('uworld') or {}).get('step2') or []
        step2 = bool(uw) or any('step2' in t.lower().replace('_', '') for t in c.get('tags', []))
        for bid, ps in low.items():
            hit = [t for t, r in ps if t in hl and r.search(hay)]
            if hit:
                idx[bid]['anki'].append({'nid': c['nid'], 'step2': step2, 'uworld': uw[:6], 'terms': hit,
                                         'text': re.sub(r'\s+', ' ', c.get('text') or '')[:240],
                                         'extra': re.sub(r'\s+', ' ', c.get('extra') or '')[:240]})
    for v in idx.values():
        v['anki'].sort(key=lambda c: (not c['step2'], -len(c['terms'])))
    meta = {'built': time.strftime('%Y-%m-%d %H:%M'), 'briefs': len(idx), 'cards': ncards,
            'question_items': len(question_items()), 'seconds': round(time.time() - t0, 1)}
    json.dump({'_meta': meta, 'briefs': idx}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('board_index: %(briefs)d briefs, %(question_items)d question items, %(cards)d cards, %(seconds)ss' % meta,
          '->', os.path.relpath(OUT, WS))
    return 0


def show(argv):
    bid = argv[0]
    n = int(argv[argv.index('--cards') + 1]) if '--cards' in argv else 25
    d = json.load(open(OUT, encoding='utf-8'))
    v = d['briefs'].get(bid)
    if not v:
        sys.exit('board_index: no brief %r (built %s)' % (bid, d['_meta']['built']))
    print('%s: %s (index built %s)' % (bid, v['title'], d['_meta']['built']))
    print('terms: ' + ' | '.join(v['terms']))
    print('question items: %d' % len(v['questions']))
    for q in v['questions']:
        print('  %s :: %s | %s | key %s | on %s' % (q['file'], q['header'], ', '.join(q['ids']) or '-', q['key'] or '-',
                                                  ', '.join(q['terms'])))
    print('page NBME items: %s' % (', '.join(v['nbme_items']) or '-'))
    for c in v['coverage']:
        print('  coverage %(nbme_id)s %(sort)s %(item_id)s %(task)s %(result)s: %(note)s' % c)
    s2 = sum(1 for c in v['anki'] if c['step2'])
    print('AnKing cards: %d (%d Step 2); showing %d' % (len(v['anki']), s2, min(n, len(v['anki']))))
    for c in v['anki'][:n] if '--all' not in argv else v['anki']:
        print('--- nid %s%s | UWorld %s | on %s' % (c['nid'], ' [Step 2]' if c['step2'] else '',
                                                   ', '.join(map(str, c['uworld'])) or '-', ', '.join(c['terms'])))
        print('  text : ' + c['text'])
        if c['extra']:
            print('  extra: ' + c['extra'])
    return 0


def terms(argv):
    bid, add = argv[0], argv[1:]
    t = json.load(open(TERMS, encoding='utf-8')) if os.path.exists(TERMS) else {
        '_doc': 'Extra board_index search terms per brief id (tools/spine/board_index.py terms).'}
    t[bid] = sorted(set(t.get(bid, [])) | set(add), key=str.lower)
    json.dump(t, open(TERMS, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, sort_keys=True)
    print('board_terms: %s now %s; run build' % (bid, t[bid]))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('build', 'show', 'terms'):
        sys.exit(__doc__.strip().splitlines()[4].strip())
    sys.exit({'build': build, 'show': show, 'terms': terms}[a[0]](a[1:]))
