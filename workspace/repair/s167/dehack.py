#!/usr/bin/env python3
"""dehack.py: s167 step 3, the specificity workarounds and !important that the layers make unnecessary.

1. `html:is([data-theme],:not([data-theme])) ` is removed from every selector in site/css (it outranked the old theme
   rules, which are now custom-property tokens in the last layer).
2. `!important` is removed from every declaration in site/css, except: layout/print.css (print overrides the inline
   styles of the screen view), the prefers-reduced-motion block, and the declarations kept in KEEP below with a reason.
A rule whose removal changed a computed style (tools/ui_check.js run) or that beats an inline style a script writes is
listed in KEEP as (file, selector text as it stands after step 1, property, reason); it keeps its !important or, with
property '(hack)', its workaround prefix.

  python3 repair/s167/dehack.py [--dry]     writes site/css and local/s167/dehack_changes.txt
"""
import glob, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = os.path.join(WS, 'site', 'css')
HACK = 'html:is([data-theme],:not([data-theme])) '
SKIP_FILES = {'layout/print.css'}

# (file, selector after step 1, property or '(hack)', reason)
KEEP = [
]


def keep(rel, sel, prop):
    return any(k[0] == rel and k[1] == sel and k[2] == prop for k in KEEP)


def split_decls(body):
    out, depth, cur = [], 0, ''
    for ch in body:
        depth += ch == '('
        depth -= ch == ')'
        if ch == ';' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def main(a):
    changes, n_hack, n_imp, kept = [], 0, 0, 0
    for f in sorted(glob.glob(os.path.join(CSS, '**', '*.css'), recursive=True)):
        rel = os.path.relpath(f, CSS)
        src = open(f, encoding='utf-8').read()
        out, in_rm = [], False
        for ln in src.splitlines(True):
            if 'reduced-motion' in ln and ln.lstrip().startswith('@media'):
                in_rm = True
            m = re.match(r'^([^{}@]*)\{(.*)\}(\s*)$', ln)
            if in_rm and ln.strip() == '}':
                in_rm = False
            if not m or rel in SKIP_FILES:
                out.append(ln); continue
            sel, body, tail = m.groups()
            new_sel = sel
            if HACK in sel:
                stripped = sel.replace(HACK, '')
                if keep(rel, stripped, '(hack)'):
                    kept += 1
                else:
                    new_sel = stripped; n_hack += sel.count(HACK)
                    changes.append('%s: hack  %s' % (rel, stripped[:150]))
            decls = split_decls(body)
            for i, d in enumerate(decls):
                if '!important' not in d or ':' not in d or in_rm:
                    continue
                prop = d.split(':', 1)[0].strip()
                if keep(rel, new_sel if new_sel == sel.replace(HACK, '') else sel.replace(HACK, ''), prop):
                    kept += 1; continue
                decls[i] = re.sub(r'\s*!important', '', d); n_imp += 1
                changes.append('%s: important  %s { %s }' % (rel, sel.replace(HACK, '')[:120], prop))
            out.append(new_sel + '{' + ';'.join(decls) + '}' + tail)
        new = ''.join(out)
        if new != src and '--dry' not in a:
            open(f, 'w', encoding='utf-8').write(new)
    os.makedirs(os.path.join(WS, 'local', 's167'), exist_ok=True)
    open(os.path.join(WS, 'local', 's167', 'dehack_changes.txt'), 'w').write('\n'.join(changes) + '\n')
    print('dehack: hack prefixes removed', n_hack, '; !important removed', n_imp, '; kept', kept, '(KEEP %d)' % len(KEEP))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
