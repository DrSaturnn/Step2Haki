#!/usr/bin/env python3
"""root_fixes: the 3 ui_lint theme_noncustom_decl findings on the token split (D-20261105-10 rule 1), all canvas paint on
the root element. Run once on site/css after it is committed from `split_css.py --tokens`.

  python3 repair/s164b/root_fixes.py [--check]

1. color-scheme: tokens.css `:root{color-scheme:light}` reads `var(--t-color-scheme,light)`; dark.css sets the token.
2. dark.css `html[data-theme="dark"]{background:var(--canvas-b)}` is deleted: base.css `html{background:var(--canvas-b)}`
   gives the same value, since dark sets --canvas-b on the same element.
3. tinted.css html background gradient becomes `--t-html-bg` on the same selector; base.css html background reads
   `var(--t-html-bg,var(--canvas-b))`.
--check prints what would change and writes nothing.
"""
import os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = os.path.join(WS, 'site', 'css')


def edit(rel, fn):
    p = os.path.join(CSS, rel)
    t = open(p, encoding='utf-8').read()
    n = fn(t)
    if n == t:
        sys.exit('root_fixes: no change in ' + rel)
    return p, n


def one(t, old, new):
    if t.count(old) != 1:
        sys.exit('root_fixes: expected one %r, found %d' % (old[:80], t.count(old)))
    return t.replace(old, new)


def main(argv):
    out = []
    out.append(edit('tokens.css', lambda t: one(t, ':root{color-scheme:light;', ':root{color-scheme:var(--t-color-scheme,light);')))

    def dark(t):
        t = one(t, '[data-theme="dark"]{color-scheme:dark;', '[data-theme="dark"]{--t-color-scheme:dark;')
        return one(t, 'html[data-theme="dark"]{background:var(--canvas-b)}\n', '')
    out.append(edit('themes/dark.css', dark))

    def tinted(t):
        m = re.search(r'html\[data-theme="dark"\]\[data-glass="tinted"\]\{background:([^;}]*)([;}])', t)
        if not m or t.count(m.group(0)) != 1:
            sys.exit('root_fixes: tinted html background rule not found once')
        return t.replace(m.group(0), 'html[data-theme="dark"][data-glass="tinted"]{--t-html-bg:%s%s' % (m.group(1), m.group(2)))
    out.append(edit('themes/tinted.css', tinted))
    out.append(edit('base.css', lambda t: one(t, 'html{background:var(--canvas-b);', 'html{background:var(--t-html-bg,var(--canvas-b));')))
    for p, n in out:
        print('root_fixes:', os.path.relpath(p, WS))
        if '--check' not in argv:
            open(p, 'w', encoding='utf-8').write(n)


if __name__ == '__main__':
    main(sys.argv[1:])
