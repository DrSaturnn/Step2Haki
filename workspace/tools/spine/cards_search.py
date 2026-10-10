"""cards_search: find AnKing cards by words, to learn what the exam rewards (Jonathan 2026-10-10: on a literature vs
board disagreement, follow NBME, then UWorld, then AnKing).

  python3 tools/spine/cards_search.py "lithium" "dialysis" [--any] [--max 12] [--step2]

All terms must appear (case-insensitive) in the card's Text or Extra unless --any. --step2 keeps cards tagged for
Step 2. Prints nid, deck, UWorld Step 2 QIDs, the card text and its Extra. Card words are evidence, never page text:
cite a card in facts.json as {"id", "local": "repair/sources/anki/anki_cards.txt", "quote": <a verbatim fragment of
the card as it appears in that file>, "kind": "board", "nid": <nid>} and write the page line in your own words.
"""
import json
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
IX = os.path.join(WS, 'repair', 'sources', 'anki', 'anki_index.jsonl')


def main(argv):
    terms = [a for i, a in enumerate(argv) if not a.startswith('--') and not (i and argv[i - 1] == '--max')]
    if not terms:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    mx = int(argv[argv.index('--max') + 1]) if '--max' in argv else 12
    anyw, step2 = '--any' in argv, '--step2' in argv
    pats = [re.compile(r'\b' + re.escape(t), re.I) for t in terms]
    n = 0
    for line in open(IX, encoding='utf-8'):
        r = json.loads(line)
        hay = (r.get('text') or '') + ' ' + (r.get('extra') or '')
        hits = [bool(p.search(hay)) for p in pats]
        if not (any(hits) if anyw else all(hits)):
            continue
        uw = (r.get('uworld') or {}).get('step2') or []
        if step2 and not uw and not any('step2' in t.lower().replace('_', '') for t in r.get('tags', [])):
            continue
        n += 1
        print('--- nid %s | %s | UWorld Step 2 QIDs: %s' % (r['nid'], r.get('deck', ''), ', '.join(map(str, uw[:8])) or '-'))
        print('  text : ' + re.sub(r'\s+', ' ', r.get('text') or '')[:400])
        if r.get('extra'):
            print('  extra: ' + re.sub(r'\s+', ' ', r['extra'])[:400])
        if n >= mx:
            break
    print('cards_search: %d shown%s' % (n, ' (capped)' if n >= mx else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
