#!/usr/bin/env python3
"""css_inventory: every style rule of the page's site-level style blocks (SVG-internal blocks skipped), in source order,
with its block, its at-rule context, selectors and declarations. Writes local/s164b/css_rules.json and prints counts.

  python3 repair/s164b/css_inventory.py [PAGE]
"""
import json, os, re, sys
from collections import Counter
import tinycss2

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def blocks(html):
    out = []
    for m in re.finditer(r'<style([^>]*)>(.*?)</style>', html, re.S):
        before = html[max(0, m.start() - 400):m.start()]
        if before.rfind('<svg') > before.rfind('</svg>'):
            continue  # inside an inline SVG: brief content
        bid = re.search(r'id="([^"]+)"', m.group(1))
        out.append({'id': bid.group(1) if bid else 'anon@%d' % m.start(), 'start': m.start(), 'css': m.group(2)})
    return out


def walk(nodes, ctx, blk, rules, src):
    for n in nodes:
        if n.type == 'qualified-rule':
            sel = tinycss2.serialize(n.prelude).strip()
            decls = [d for d in tinycss2.parse_declaration_list(n.content, skip_comments=True, skip_whitespace=True)
                     if d.type == 'declaration']
            rules.append({'i': len(rules), 'block': blk, 'ctx': ctx, 'sel': sel,
                          'decl': [[d.name if d.name.startswith('--') else d.lower_name, tinycss2.serialize(d.value).strip(), bool(d.important)] for d in decls],
                          'off': n.source_line})
        elif n.type == 'at-rule':
            pre = tinycss2.serialize(n.prelude).strip()
            name = '@' + n.lower_at_keyword
            if n.content is not None and name in ('@media', '@supports', '@layer', '@container'):
                walk(tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True),
                     ctx + [name + ' ' + pre], blk, rules, src)
            else:
                rules.append({'i': len(rules), 'block': blk, 'ctx': ctx, 'at': name + ' ' + pre,
                              'raw': tinycss2.serialize([n])[:20000]})


def main(argv):
    page = argv[0] if argv else os.path.join(WS, 'index.html')
    html = open(page, encoding='utf-8').read()
    rules = []
    bl = blocks(html)
    for b in bl:
        walk(tinycss2.parse_stylesheet(b['css'], skip_comments=True, skip_whitespace=True), [], b['id'], rules, b['css'])
    os.makedirs(os.path.join(WS, 'local', 's164b'), exist_ok=True)
    json.dump({'blocks': [{k: v for k, v in b.items() if k != 'css'} | {'len': len(b['css'])} for b in bl], 'rules': rules},
              open(os.path.join(WS, 'local', 's164b', 'css_rules.json'), 'w'), indent=0)
    q = [r for r in rules if 'sel' in r]
    print('blocks', len(bl), 'rules', len(q), 'at-rules', len(rules) - len(q),
          'decls', sum(len(r['decl']) for r in q), 'important', sum(d[2] for r in q for d in r['decl']))
    th = Counter()
    for r in q:
        s = r['sel']
        for k in ('data-theme', 'data-axa', 'data-glass', 'body.flat', '.flat', 'body.study', '.study', 'html:is('):
            if k in s:
                th[k] += 1
    print('selector markers', dict(th))
    print('at-rule kinds', Counter(r['at'].split()[0] for r in rules if 'at' in r))
    print('ctx', Counter(' > '.join(r['ctx']) for r in q).most_common(15))
    print('per block', Counter(r['block'] for r in q).most_common(30))


if __name__ == '__main__':
    main(sys.argv[1:])
