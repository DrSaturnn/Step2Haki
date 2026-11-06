#!/usr/bin/env python3
"""split_css: writes the page's site CSS (local/s164b/css_rules.json, from css_inventory.py) into site/css/ as layer
files, rules in their original order within each file, comments dropped, breakpoints named.

  python3 repair/s164b/split_css.py [--report] [--dehack] [--tokens]

--tokens converts theme rules to color tokens (D-20261105-10; repair/s164b/tokenize.py).

--dehack drops the html:is([data-theme],:not([data-theme])) specificity workaround from every selector.

The file a rule goes to is decided by FILES below, first match on the rule's selector. Writes site/css/<file>.css and
local/s164b/split_map.json (rule index -> file), and prints rules per file.
"""
import json, os, re, sys
from collections import Counter, OrderedDict

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(WS, 'site', 'css')

# named breakpoints (expanded by the build); every other width keeps a name of its own
MEDIA = OrderedDict([
    ('(max-width:640px)', '--phone'), ('(min-width:641px)', '--not-phone'), ('(max-width:1100px)', '--narrow'),
    ('(min-width:1101px)', '--desktop'), ('(max-width:980px)', '--w980'), ('(max-width:900px)', '--w900'),
    ('(min-width:900px)', '--min900'), ('(max-width:560px)', '--w560'), ('(min-width:700px)', '--min700'),
    ('(max-width:420px)', '--w420'), ('(max-width:1240px)', '--w1240'), ('(prefers-reduced-motion:reduce)', '--reduced-motion'),
    ('(prefers-reduced-motion: reduce)', '--reduced-motion'), ('print', '--print'),
])

THEME = re.compile(r'\[data-(?:theme|axa|glass)[^\]]*\]')
HACK = 'html:is([data-theme],:not([data-theme]))'
# a theme attribute that is only negated (light-only rules) does not make a rule a theme rule
NEG_THEME = re.compile(r':not\(\[data-theme[^\]]*\]\)')

# (file, layer, pattern on the selector with the specificity hack removed); first match wins
FILES = [
    ('themes/tinted', 'themes', r'\[data-glass'),
    ('themes/accents', 'themes', r'\[data-axa'),
    ('themes/dark', 'themes', r'\[data-theme'),
    ('layout/print', 'layout', r'^@print'),
    ('layout/sidebar', 'layout', r'body\.navopen|#nav\b|#navlinks|#navtop|#navscroll|#navscrim|\.axn\b|#axn\b|\.axn-|\.bb-rl\b|\.bb-rail|\.navsub|\.navclose|\.shelfsel|\.shelfpick|\.fmdrop'),
    ('layout/phone', 'layout', r'\.bb-menu|#mbar|#navtab|\.bb-bar\b|\.bb-idx|\.bb-t\b|\.bb-sec|\.bb-prog|\.bb-l\b|\.bb-c\b'),
    ('layout/rail', 'layout', r'\.bb-rail|\.bb-end|\.bb-cap|\.bb-nx|\.bb-top'),
    ('layout/toolbar', 'layout', r'#axbar|#modes|#axdisp|\.axsw|#axtopfade|#axedge|\.axrvb|\.axacc|\.flatt'),
    ('layout/drawer', 'layout', r'\.sp-drawer|\.lbp|\.axdrw|#spd|\.drw'),
    ('components/review', 'components', r'#rvpanel|#axrv|#rvsession|#rvlaunch|#rvbar|\.rv[a-z]*\b|\.due\b'),
    ('components/search', 'components', r'#search|#sxres|\.sx[a-z]+|\.noresults'),
    ('components/changelog', 'components', r'\.axlog|#axlog'),
    ('components/nbme', 'components', r'nbme|\.nbd\b|\.nbv'),
    ('components/cards', 'components', r'\.pc-|\[data-entry="card"\]'),
    ('components/links', 'components', r'\.sp-drw'),
    ('components/hovercard', 'components', r'\.sp-pop|\.sp-why|\[popover\]|\.flowpop|\.pop\b'),
    ('components/bank', 'components', r'\.mcq|\.bank\b|\.bankwrap|\.bk[a-z]*\b|\.qx-|\.opts\b|\.stack\b|\.sp-prac|\.qp\b|ol\.bank'),
    ('components/workup', 'components', r'\.w5|\.wk\b|\.cluet|\.sp-wk|\.figcap|\.figbody|figure'),
    ('components/ladder', 'components', r'\.sp-rung|\.sp-node|\.sp-ladder|\.ladder|\.sp-scale|\.sp-thr'),
    ('components/pause', 'components', r'\.sp-pause|\.pp\b'),
    ('components/timeline', 'components', r'\.lc[a-z-]*\b|\.rax\b|\.sw-|\.sp-tl|\.sp-on|\.track\b|\.tk\b|\.axis\b|\.wr2?\b|\.wrows|\.sp-trk|\.sp-when|\.ons\b|\.tl\b|\.night'),
    ('components/mnemonic', 'components', r'\.mn\b|\.mnem|\.mn-'),
    ('components/table', 'components', r'\btable\b|\.tw\b|\btd\b|\bth\b|\btr\b|\.tierT|\.rows\b|\.crit\b'),
    ('base', 'base', r'^[\s,]*(?:[a-z0-9*]+|html|body|:root)(?::{1,2}[\w-]+(?:\([^)]*\))?)*(?:\s*[>+~ ]\s*(?:[a-z0-9*]+)(?::{1,2}[\w-]+(?:\([^)]*\))?)*)*(?:\s*,\s*(?:[a-z0-9*]+|html|body|:root)(?::{1,2}[\w-]+(?:\([^)]*\))?)*(?:\s*[>+~ ]\s*[a-z0-9*]+(?::{1,2}[\w-]+(?:\([^)]*\))?)*)*)*[\s,]*$'),
    ('components/brief', 'components', r'.'),
]
# dead declarations: (rule index, property) -> why it never applied. Each lost before the layers and would win after
# them; every entry goes to the batch report's Retired table with its owner decision.
DEAD = {
    (1653, '--sidebar'): 's136 dark theme copied the 286px default; s141 set the desktop sidebar to 344px (won on '
                         'specificity), and below 1101px the copy equals the default',
}
FILE_ORDER = ['tokens'] + [f for f, _, _ in FILES]
LAYER_OF = dict([('tokens', 'tokens'), ('base', 'base')] + [(f, l) for f, l, _ in FILES])


def strip_comments(s):
    return re.sub(r'/\*.*?\*/', '', s, flags=re.S)


def top_split(sel, chars):
    out, depth, cur = [], 0, ''
    for ch in sel:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if depth == 0 and ch in chars:
            out.append(cur)
            cur = ''
            continue
        cur += ch
    out.append(cur)
    return out


def subject(part):
    comps = [c for c in top_split(part.strip(), ' >+~') if c.strip()]
    return comps[-1] if comps else part


def classify_one(part, r):
    plain = NEG_THEME.sub('', part.replace(HACK, ''))
    if THEME.search(plain):
        for f, _, pat in FILES[:3]:
            if re.search(pat, plain):
                return f
    if '@media print' in r['ctx']:
        return 'layout/print'
    subj = subject(plain)
    for f, _, pat in FILES[3:]:
        if f in ('base', 'components/brief'):
            continue
        if re.search(pat, subj):
            return f
    for f, _, pat in FILES[3:]:
        if f in ('base', 'components/brief'):
            continue
        if re.search(pat, plain):
            return f
    if re.fullmatch(FILES[-2][2], plain) or re.fullmatch(r'body(?:\.[\w-]+)+', subj.strip()):
        return 'base'
    return 'components/brief'


def classify(r):
    """the file for each selector of the rule: {file: [selector parts]}"""
    if 'at' in r:
        return {'layout/print' if r['at'].startswith('@page') else 'base': None}
    sel = strip_comments(r['sel'])
    plain = sel.replace(HACK, '')
    if not THEME.search(plain) and re.fullmatch(r'\s*(:root|html)\s*', plain) and all(d[0].startswith('--') or d[0] == 'color-scheme' for d in r['decl']):
        return {'tokens': None}
    out = OrderedDict()
    for part in top_split(sel, ','):
        out.setdefault(classify_one(part, r), []).append(part.strip())
    return out


def media_name(ctx):
    out = []
    for c in ctx:
        m = re.match(r'@media\s+(.*)$', c)
        if m:
            q = re.sub(r'\s+', ' ', m.group(1).strip())
            key = q.replace(': ', ':') if q not in MEDIA else q
            name = MEDIA.get(q) or MEDIA.get(key)
            out.append('@media (%s)' % name if name else c)
        else:
            out.append(c)
    return out


def decl_text(d):
    return '%s:%s%s' % (d[0], strip_comments(d[1]).strip(), '!important' if d[2] else '')


def main(argv):
    css = json.load(open(os.path.join(WS, 'local', 's164b', 'css_rules.json')))
    per = OrderedDict((f, []) for f in FILE_ORDER)
    where = {}
    rules = css['rules']
    if '--tokens' in argv:
        import importlib.util
        spec = importlib.util.spec_from_file_location('tokenize_s164b', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tokenize.py'))
        tk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)
        rules, toks, rep = tk.run(rules, set(DEAD) | tk.load_dead())
        rules = rules + [{'i': 10 ** 6, 'block': 'tokens', 'ctx': [], 'sel': ':root', 'decl': [[k, v, False] for k, v in toks.items()]}]
        json.dump(rep, open(os.path.join(WS, 'local', 's164b', 'tokens_report.json'), 'w'), indent=1)
        print('tokens', rep['counts'])
    for r in rules:
        if any((r['i'], d[0]) in DEAD for d in r.get('decl', [])):
            r = dict(r, decl=[d for d in r['decl'] if (r['i'], d[0]) not in DEAD])
            if not r['decl']:
                continue
        groups = classify(r)
        where[r['i']] = list(groups)
        for f, parts in groups.items():
            rr = dict(r)
            if parts is not None:
                if '--dehack' in argv:
                    parts = [q.replace(HACK, '').strip() for q in parts]
                rr['sel'] = ','.join(parts)
            per[f].append(rr)
    for f, rules in per.items():
        path = os.path.join(OUT, f + '.css')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        lines, cur = [], None
        for r in rules:
            ctx = media_name(r['ctx'])
            if ctx != cur:
                if cur:
                    lines.append('}' * len(cur))
                for c in ctx:
                    lines.append(c + '{')
                cur = ctx
            if 'at' in r:
                lines.append(strip_comments(r['raw']).strip())
            else:
                sel = re.sub(r'\s+', ' ', strip_comments(r['sel'])).strip()
                lines.append('%s{%s}' % (sel, ';'.join(decl_text(d) for d in r['decl'])))
        if cur:
            lines.append('}' * len(cur))
        open(path, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    json.dump({'where': where, 'order': FILE_ORDER, 'layer': LAYER_OF},
              open(os.path.join(WS, 'local', 's164b', 'split_map.json'), 'w'), indent=0)
    for f, rules in per.items():
        print('%-24s %5d' % (f, len(rules)))


if __name__ == '__main__':
    main(sys.argv[1:])
