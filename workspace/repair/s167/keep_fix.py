#!/usr/bin/env python3
"""keep_fix.py: s167 chunk 13, puts back the dehack workarounds that parity (ui_check c4 vs base_fix) showed are load-bearing.

Each entry is also in dehack.py KEEP with its reason. A '(hack)' entry restores the html:is prefix on the rule; a property
entry restores that declaration's !important. Idempotent.

  python3 repair/s167/keep_fix.py
"""
import os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WS, 'repair', 's167'))
from dehack import KEEP, HACK, CSS, split_decls  # noqa: E402

CHUNK13 = [k for k in KEEP if len(k) > 4 and k[4] == 13]


def main():
    done = 0
    for rel, sel, prop, _why, _c in CHUNK13:
        p = os.path.join(CSS, rel)
        lines = open(p, encoding='utf-8').read().splitlines(True)
        hit = 0
        for i, ln in enumerate(lines):
            m = re.match(r'^([^{}@]*)\{(.*)\}(\s*)$', ln)
            if not m or m.group(1).replace(HACK, '') != sel:
                continue
            s, body, tail = m.groups()
            if prop.startswith('(hack'):
                need = prop[6:-1] if prop.startswith('(hack:') else None
                if need and not any(':' in d and d.split(':', 1)[0].strip() == need for d in split_decls(body)):
                    if HACK in s:
                        s = s.replace(HACK, '')
                    lines[i] = s + '{' + body + '}' + tail
                    continue
                if HACK not in s:
                    s = HACK + s
                hit += 1
            else:
                decls = split_decls(body)
                for j, d in enumerate(decls):
                    if ':' in d and d.split(':', 1)[0].strip() == prop:
                        hit += 1
                        if '!important' not in d:
                            decls[j] = d.rstrip() + '!important'
                body = ';'.join(decls)
            lines[i] = s + '{' + body + '}' + tail
        if not hit:
            sys.exit('keep_fix: not found: %s %s %s' % (rel, sel, prop))
        done += hit
        open(p, 'w', encoding='utf-8').write(''.join(lines))
    print('keep_fix: %d entries, %d rules' % (len(CHUNK13), done))


if __name__ == '__main__':
    main()
