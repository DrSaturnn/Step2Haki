"""card_checklist: the AnKing items a brief must account for (plan 0.6b), as a packet file.

  python3 tools/spine/card_checklist.py <brief-id> [--terms "copd,chronic obstructive"] [--cap 15]
                                        [--out repair/migration/spine/packets/<id>/cards.md]

Must items: cards linked to the brief by note id (data-nid on the brief or its items). For each card: the anchor
(its cloze answers: the fact the card tests) and its Extra statements (the deck's high-yield notes), each with a
stable id <nid>.<key>. Statements already listed under another card are merged (one id, both cards named).
Candidate items (--terms): Step 2 tagged cards not linked by note id whose Text names one of the terms (word
match, case-insensitive), ranked by how many terms the Text and Extra name, capped (default 15) with the cut
logged. A provisional score until the frozen test set in the plan defines it; candidates may be marked not-topic.
The output holds card text, so it lives under repair/migration (local-only) and is never committed. Every item
needs a disposition in the author's report: covered:<line or row>, owner:<brief id>, scope:<reason>, or
conflict:<fact id>. Cards are leads, never citations.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.dirname(HERE))
import pagelib as P  # noqa: E402


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    bid = argv[0]
    out = argv[argv.index('--out') + 1] if '--out' in argv else os.path.join(WS, 'repair', 'migration', 'spine', 'packets', bid, 'cards.md')
    b = P.brief_by_id(P.read_page(os.path.join(WS, 'index.html')), bid)
    toks = set(b.attrs.get('data-nid', '').split())
    for g in re.findall(r'data-nid="([^"]*)"', b.inner):
        toks |= set(g.split())
    nids = {int(t) for t in toks if re.fullmatch(r'1\d{12}', t)}
    cards = {}
    for line in open(os.path.join(WS, 'repair', 'sources', 'anki', 'anki_index.jsonl'), encoding='utf-8'):
        r = json.loads(line)
        if r.get('nid') in nids:
            cards[r['nid']] = r
    seen = {}
    lines = ['# Card checklist: %s (%s)' % (b.title, bid), '',
             'Must items from %d linked cards (%d note ids on the brief; %d not in the deck index). Cards are leads, never citations: '
             'give every item a disposition (covered:<line or row id>, owner:<brief id>, scope:<reason>, conflict:<fact id>).' % (
                 len(cards), len(nids), len(nids - set(cards))), '']
    n = 0
    for nid, r in sorted(cards.items()):
        lines.append('## card %s (%s)' % (nid, r.get('deck', '')))
        lines.append('- anchor (cloze): %s' % ('; '.join(r.get('cloze') or []) or '(none)'))
        lines.append('- card text: %s' % r['text'][:300].replace('\n', ' '))
        for h in r.get('hy', []):
            if h['key'] in seen:
                lines.append('- [%s] same as %s' % (h['id'], seen[h['key']]))
                continue
            seen[h['key']] = h['id']
            n += 1
            lines.append('- [%s] %s' % (h['id'], h['text']))
        lines.append('')
    terms = [t.strip() for t in (argv[argv.index('--terms') + 1].split(',') if '--terms' in argv else []) if t.strip()]
    cap = int(argv[argv.index('--cap') + 1]) if '--cap' in argv else 15
    if terms:
        pats = [re.compile(r'\b%s\b' % re.escape(t), re.I) for t in terms]
        cand = []
        for line in open(os.path.join(WS, 'repair', 'sources', 'anki', 'anki_index.jsonl'), encoding='utf-8'):
            r = json.loads(line)
            if r.get('nid') in cards or not any(t.startswith('#AK_Step2') for t in r.get('tags', [])):
                continue
            if any(p.search(r['text']) for p in pats):
                score = sum(bool(p.search(r['text'])) * 2 + bool(p.search(r.get('extra', ''))) for p in pats)
                cand.append((-score, r.get('nid') or 0, r))
        cand.sort(key=lambda x: (x[0], x[1]))
        lines.append('# Candidates (terms: %s): %d matched, showing %d%s' % (', '.join(terms), len(cand), min(cap, len(cand)),
                     '; %d cut by the cap' % (len(cand) - cap) if len(cand) > cap else ''))
        lines.append('Disposition each: covered, owner, scope, not-topic, conflict.')
        lines.append('')
        for _, _, r in cand[:cap]:
            lines.append('## candidate %s (%s)' % (r.get('nid') or r['guid'], r.get('deck', '')))
            lines.append('- anchor (cloze): %s' % ('; '.join(r.get('cloze') or []) or '(none)'))
            lines.append('- card text: %s' % r['text'][:300].replace('\n', ' '))
            for h in r.get('hy', [])[:6]:
                if h['key'] not in seen:
                    seen[h['key']] = h['id']
                    lines.append('- [%s] %s' % (h['id'], h['text']))
            lines.append('')
        print('candidates: %d matched, %d kept (cap %d)' % (len(cand), min(cap, len(cand)), cap))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('card_checklist: %s: %d cards, %d anchors, %d distinct statements -> %s' % (
        bid, len(cards), sum(1 for r in cards.values() if r.get('cloze')), n, os.path.relpath(out, WS)))


if __name__ == '__main__':
    main(sys.argv[1:])
