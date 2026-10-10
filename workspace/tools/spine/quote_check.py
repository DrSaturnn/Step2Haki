"""quote_check: every quote a brief cites must be one verbatim fragment of a cached source (plan 0.7).

  python3 tools/spine/quote_check.py <facts.json>

facts.json: {"facts": [{"id": "f1", "sha": "<cache sha>" | "url": "<url>" | "local": "<path under repair/sources>",
              "quote": "...", "via": "fetch" | "relayed" | "local", "section": "...", "population": "...",
              "setting": "...", "kind": "fact" | "mnemonic"}]}
Rules: a quote is a single fragment (no "...", no editorial brackets); it must appear in the cached text
(whitespace, curly quotes and dashes normalized; case-insensitive). via=relayed (a WebFetch reading of a site that
blocks scripts) cannot be checked here: it is listed for the auditor, never counted as verified. An AnKing card
(local: repair/sources/anki/anki_cards.txt) or a local question explanation (repair/sources/sNN_questions.md) is
accepted on kind=board rows: evidence of what Step 2 rewards, used where the literature or practice differs from the
exam or no fetched source covers the exam answer (Jonathan 2026-10-10: follow NBME, then UWorld, then AnKing on such
disagreements); and on kind=mnemonic rows. Its words never go on the page (shingle_check).
Exit 1 on any failure.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import load_index  # noqa: E402

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CACHE = os.path.join(WS, 'repair', 'sources', 'web')
TRANS = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-',
                       '−': '-', ' ': ' ', '≥': '>=', '≤': '<='})


def norm(s):
    return ' '.join(s.translate(TRANS).lower().split())


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    facts = json.load(open(argv[0], encoding='utf-8'))['facts']
    ix = load_index()
    by_url = {e['url']: sha for sha, e in ix.items()}
    texts, fails, relayed, ok = {}, [], [], 0
    for f in facts:
        fid, q, via = f.get('id', '?'), f.get('quote', ''), f.get('via', 'fetch')
        if '...' in q or '…' in q:
            fails.append('%s: joins fragments with "..."; split it into one fact per fragment' % fid)
            continue
        if re.search(r'\[[^\]]*\]', q):
            fails.append('%s: editorial brackets inside the quote; quote the source exactly' % fid)
            continue
        if via == 'relayed':
            relayed.append('%s: %s (relayed reading; auditor checks it against the page)' % (fid, f.get('url', '')))
            continue
        if f.get('local'):
            path = os.path.join(WS, 'repair', 'sources', f['local'].split('repair/sources/')[-1])
            if '/anki/' in path.replace(os.sep, '/') and f.get('kind') not in ('mnemonic', 'board'):
                fails.append('%s: an AnKing card cited as a fact source; cite it only as kind "board" (what the exam '
                             'rewards, where the literature or practice differs or no fetched source covers the exam '
                             'answer) or kind "mnemonic"' % fid)
                continue
        else:
            sha = f.get('sha') or by_url.get(f.get('url', ''))
            if not sha or not os.path.exists(os.path.join(CACHE, sha + '.txt')):
                fails.append('%s: source not in the cache; run tools/spine/fetch.py <url> first' % fid)
                continue
            path = os.path.join(CACHE, sha + '.txt')
        if path not in texts:
            texts[path] = norm(open(path, encoding='utf-8', errors='replace').read())
        if norm(q) in texts[path]:
            ok += 1
        else:
            fails.append('%s: quote not found verbatim in %s' % (fid, os.path.relpath(path, WS)))
    print('quote_check: %d verified, %d relayed (unverified), %d failed' % (ok, len(relayed), len(fails)))
    for x in relayed:
        print('  RELAYED ' + x)
    for x in fails:
        print('  FAIL ' + x)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
