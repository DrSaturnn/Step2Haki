#!/usr/bin/env python3
"""Compact AnKing lookup (lead tool, s146): cards.py [-n N] [--s2] term [term...]  (all terms must match, case-insensitive,
in text+extra). Prints nid, Step 2 UWorld ids, cloze-filled text and high-yield lines, each cut to 220 chars."""
import json, sys
args = sys.argv[1:]; n = 12; s2 = False
if args and args[0] == '-n': n = int(args[1]); args = args[2:]
if args and args[0] == '--s2': s2 = True; args = args[1:]
terms = [a.lower() for a in args]
out = 0
for l in open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'repair', 'sources', 'anki', 'anki_index.jsonl'), encoding='utf-8'):
    d = json.loads(l)
    blob = (d.get('text', '') + ' ' + d.get('extra', '')).lower()
    if not all(t in blob for t in terms): continue
    tags = ' '.join(d.get('tags', []))
    step2 = 'AK_Step2' in tags
    if s2 and not step2: continue
    uw = d.get('uworld', {}).get('step2', [])
    hy = ' / '.join(h['text'] for h in d.get('hy', []))
    print('%s%s uw%s | %s | HY: %s' % (d['nid'], ' S2' if step2 else '', uw or '', d.get('text', '').replace('\n', ' ')[:220], hy[:220]))
    out += 1
    if out >= n: break
