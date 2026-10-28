#!/usr/bin/env python3
"""facts_from_spec (lead tool, s146): build a brief folder's facts.json from a short spec, checking every quote.
  python3 tools/spine/facts_from_spec.py <spec.json> [--append]
spec: {"out": "<facts.json path>", "population": "...", "cards": [[id, nid, quote], ...],
       "web": [[id, sha, section, quote, population?], ...],
       "local": [[id, file under repair/sources, title, quote], ...],   (s147: a local UWorld question file)
       "relayed": [{id, url, title, quote, section, population?, setting?, kind?, fetched?}, ...]}   (s155: a WebFetch
       reading of a site that refuses fetch.py; stored via=relayed, so quote_check lists it and the auditor checks it)
Card quotes must appear in the card's text or extra (whitespace-normalized, as quote_check reads them); the title
carries "high-yield line" when the quote is (part of) a pink line, and the card's Step 2 UWorld ids. Web quotes must
appear in repair/sources/web/<sha>.txt; local quotes in their file (kind board). --append keeps the facts already in the file (ids must not repeat)."""
import json, os, sys
WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
norm = lambda s: ' '.join(s.split())
spec = json.load(open(sys.argv[1], encoding='utf-8'))
out = os.path.join(WS, spec['out'])
facts = json.load(open(out, encoding='utf-8'))['facts'] if '--append' in sys.argv and os.path.exists(out) else []
seen = {f['id'] for f in facts}
want = {c[1] for c in spec.get('cards', [])}
ix = {}
for l in open(os.path.join(WS, 'repair', 'sources', 'anki', 'anki_index.jsonl'), encoding='utf-8'):
    d = json.loads(l)
    if d.get('nid') in want: ix[d['nid']] = d
    elif d.get('guid') in want: ix[d['guid']] = d      # s146b: a card with no note id is named by its guid
bad = []
for fid, nid, q in spec.get('cards', []):
    d = ix.get(nid)
    if not d or norm(q) not in norm(d.get('text', '')) and norm(q) not in norm(d.get('extra', '')):
        bad.append((fid, q[:60])); continue
    uw = d.get('uworld', {}).get('step2', [])
    hy = any(norm(q) in norm(h['text']) or norm(h['text']) in norm(q) for h in d.get('hy', []))
    parts = (['high-yield line'] if hy else []) + (['UWorld Step ' + ', '.join(map(str, uw))] if uw else [])
    assert fid not in seen, fid; seen.add(fid)
    facts.append(dict(id=fid, local='repair/sources/anki/anki_cards.txt', quote=q, kind='board', nid=nid,
                      title='AnKing card %s' % nid + (' (%s)' % '; '.join(parts) if parts else ''),
                      population=spec['population'], setting='Step 2 CK board teaching'))
for w in spec.get('web', []):
    fid, sha, sec, q = w[:4]
    t = open(os.path.join(WS, 'repair', 'sources', 'web', sha + '.txt'), encoding='utf-8').read()
    if norm(q) not in norm(t):
        bad.append((fid, q[:60])); continue
    assert fid not in seen, fid; seen.add(fid)
    facts.append(dict(id=fid, sha=sha, quote=q, section=sec, population=w[4] if len(w) > 4 else spec['population'],
                      setting='clinical reference', via='fetch'))
for fid, f, title, q in spec.get('local', []):      # s147: UWorld question files, as the AIR and COPD facts cite them
    assert f.startswith('repair/sources/'), f
    if norm(q) not in norm(open(os.path.join(WS, f), encoding='utf-8').read()):
        bad.append((fid, q[:60])); continue
    assert fid not in seen, fid; seen.add(fid)
    facts.append(dict(id=fid, local=f, quote=q, kind='board', title=title, population=spec['population'],
                      setting='Step 2 CK board teaching'))
for f in spec.get('relayed', []):              # s155: relayed readings go into facts.json, not a side file
    f = dict(f)
    assert f.get('id') and f.get('url', '').startswith('http') and f.get('quote'), f
    assert f['id'] not in seen, f['id']; seen.add(f['id'])
    f['via'] = 'relayed'
    f.setdefault('population', spec['population']); f.setdefault('setting', 'clinical reference')
    facts.append(f)
if bad:
    sys.exit('not found: %s' % bad)
json.dump({'facts': facts}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('%d facts -> %s' % (len(facts), spec['out']))
