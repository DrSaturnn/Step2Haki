#!/usr/bin/env python3
"""block_inventory: one row per site style block and script block of the page: size, rule count, the batch ids and
decisions its comments name, its opening comment, and which later style blocks override its rules (same selector, same
property, same at-rule context). Writes local/s164b/blocks.md and local/s164b/blocks.json.

  python3 repair/s164b/block_inventory.py [PAGE]
"""
import json, os, re, sys
from collections import Counter, defaultdict

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import css_inventory  # noqa: E402

BATCH = re.compile(r'\bs(\d{2,3}[a-z]?)\b')


def norm(sel):
    s = re.sub(r'html:is\(\[data-theme\],:not\(\[data-theme\]\)\)\s*', '', sel)
    s = re.sub(r'\s+', ' ', s).strip()
    return ','.join(sorted(p.strip() for p in s.split(',')))


def head_comment(text):
    m = re.match(r'\s*/\*(.*?)\*/', text, re.S)
    if m:
        return re.sub(r'\s+', ' ', m.group(1)).strip()[:420]
    m = re.match(r'\s*((?://[^\n]*\n\s*)+)', text)
    return re.sub(r'\s+', ' ', m.group(1)).strip()[:420] if m else re.sub(r'\s+', ' ', text.strip()[:160])


def main(argv):
    page = argv[0] if argv else os.path.join(WS, 'index.html')
    html = open(page, encoding='utf-8').read()
    css = json.load(open(os.path.join(WS, 'local', 's164b', 'css_rules.json')))
    rules = [r for r in css['rules'] if 'sel' in r]
    # override edges: for each (ctx, selector, property) the blocks that set it, in order
    setters = defaultdict(list)
    for r in rules:
        for p, v, imp in r['decl']:
            setters[(' > '.join(r['ctx']), norm(r['sel']), p)].append((r['block'], r['i'], imp))
    over = defaultdict(Counter)
    for k, lst in setters.items():
        for j in range(1, len(lst)):
            for i in range(j):
                if lst[i][0] != lst[j][0]:
                    over[lst[i][0]][lst[j][0]] += 1
    rows = []
    for b in css_inventory.blocks(html):
        text = b['css']
        rows.append({'kind': 'style', 'id': b['id'], 'start': b['start'], 'len': len(text),
                     'rules': sum(1 for r in rules if r['block'] == b['id']),
                     'batches': sorted(set(BATCH.findall(text)), key=lambda x: (int(re.match(r'\d+', x).group()), x)),
                     'jonathan': len(re.findall(r'Jonathan', text)), 'head': head_comment(text),
                     'overridden_by': dict(over[b['id']].most_common(8))})
    for m in re.finditer(r'<script([^>]*)>(.*?)</script>', html, re.S):
        attrs, text = m.group(1), m.group(2)
        if 'application/json' in attrs:
            kind = 'data'
        else:
            kind = 'script'
        bid = re.search(r'id="([^"]+)"', attrs)
        rows.append({'kind': kind, 'id': bid.group(1) if bid else 'anon@%d' % m.start(), 'start': m.start(), 'len': len(text),
                     'batches': sorted(set(BATCH.findall(text)), key=lambda x: (int(re.match(r'\d+', x).group()), x)),
                     'jonathan': len(re.findall(r'Jonathan', text)), 'head': head_comment(text),
                     'storage': sorted(set(re.findall(r"localStorage\.(?:get|set|remove)Item\('([^']+)'", text))),
                     'iife': text.count('(function')})
    json.dump(rows, open(os.path.join(WS, 'local', 's164b', 'blocks.json'), 'w'), indent=1)
    with open(os.path.join(WS, 'local', 's164b', 'blocks.md'), 'w') as f:
        for r in rows:
            f.write('## %s %s @%d, %d chars%s\n' % (r['kind'], r['id'], r['start'], r['len'],
                    (', %d rules' % r['rules']) if r['kind'] == 'style' else ''))
            f.write('batches: %s; Jonathan x%d%s\n' % (' '.join(r['batches'][:30]), r['jonathan'],
                    ('; storage ' + ' '.join(r['storage'])) if r.get('storage') else ''))
            if r.get('overridden_by'):
                f.write('overridden by: %s\n' % ', '.join('%s %d' % kv for kv in r['overridden_by'].items()))
            f.write('head: %s\n\n' % r['head'])
    print(len(rows), 'blocks;', Counter(r['kind'] for r in rows))


if __name__ == '__main__':
    main(sys.argv[1:])
