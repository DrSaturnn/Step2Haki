#!/usr/bin/env python3
"""tokenize: D-20261105-10, themes are color tokens only. Used by split_css.py --tokens; standalone it prints counts.

  python3 repair/s164b/tokenize.py [--report]
  python3 repair/s164b/tokenize.py --candidates   (local/s164b/extra_candidates.json for subset_check.js)

For every declaration of a theme rule (a selector naming [data-theme], [data-glass] or [data-axa]; light-only rules that
only negate the theme are not theme rules):
- dead (split_css DEAD, or repair/s164b/dead_theme.json from dead_decls.js): deleted;
- shape (radius, border width or style, outline width, style or offset): deleted, light's shape applies in every theme;
- custom property on a pure theme selector: kept as is;
- anything else (color, background, shadow, a custom property on a component selector): a token. The light rules with the
  same selector (theme prefix removed) and property that the theme rule outranked before get `prop:var(--t-...)`, one
  token per light rule holding that rule's own value (tokens.css; a value holding var() stays in the rule as the
  fallback, `prop:var(--t-...,var(--x))`, because a token on the root would resolve var(--x) there), so light is unchanged; the theme rule becomes
  `<theme prefix>{--t-...:<theme value>}` for each of those tokens, in its own place and media. A light rule that
  outranked the theme rule keeps its literal value (the theme value never showed there).
- a theme background-color or background-image whose light rule sets the `background` shorthand: the light rule gains
  that longhand right after the shorthand, as a token holding the shorthand's own component (light unchanged);
- a theme value using a custom property that is redefined below the root (the Flat look's --e2, --inner on .axm-flat):
  the token is also defined on `<theme prefix> <that selector>`, so var() is resolved where the variable is set
  (`scoped_tokens`; a call for Jonathan's approval, the alternative being the Flat-look variables moved to the root);
- a theme declaration with no light rule to carry it: listed (`no_light_rule`), kept in the theme file for now;
- an important theme declaration: kept on its rule (`important_kept`); the rule routes to its component's file;
- an in-between light rule B (same subject compound and property as the theme key K, a different selector the theme rule
  outranked; scaphoid `figure.w5a .w5skip` under `[dark] .w5a .w5skip`): gets its own token that the theme rule also
  sets, when repair/s164b/token_extra.json lists it (subset_check.js: every element B matches also matches K).
Returns the new rule list plus the token rules for tokens.css, and a report (local/s164b/tokens_report.json).
"""
import json, os, re, sys
from collections import OrderedDict, defaultdict

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
THEME = re.compile(r'\[data-(?:theme|axa|glass)[^\]]*\]')
HACK = 'html:is([data-theme],:not([data-theme]))'
NEG_THEME = re.compile(r':not\(\[data-theme[^\]]*\]\)')
SHAPE = re.compile(r'^(border(-(top|right|bottom|left|block|inline)(-(start|end))?)?-(width|style)|border-radius|'
                   r'border-[a-z-]*-radius|outline-(width|style|offset))$')
# a theme prefix: leading compounds made only of html, :root and theme attributes
PREFIX = re.compile(r'^\s*((?:(?:html|:root)?(?:\[data-(?:theme|axa|glass)[^\]]*\])+\s+)+)(.*)$', re.S)


def top_split(sel, chars):
    out, depth, cur = [], 0, ''
    for ch in sel:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if depth == 0 and ch in chars:
            out.append(cur); cur = ''; continue
        cur += ch
    out.append(cur)
    return out


def specificity(sel):
    """(ids, classes+attrs+pseudo-classes, types+pseudo-elements) of one complex selector; :is/:not/:has take their
    most specific argument, :where counts 0."""
    a = b = c = 0
    i, s = 0, sel
    while i < len(s):
        ch = s[i]
        if ch == '#':
            a += 1; i += 1
            while i < len(s) and re.match(r'[\w-]', s[i]): i += 1
        elif ch == '.':
            b += 1; i += 1
            while i < len(s) and re.match(r'[\w-]', s[i]): i += 1
        elif ch == '[':
            b += 1; d = 1; i += 1
            while i < len(s) and d:
                d += {'[': 1, ']': -1}.get(s[i], 0); i += 1
        elif ch == ':':
            pe = s[i:i + 2] == '::'
            j = i + (2 if pe else 1)
            m = re.match(r'[\w-]+', s[j:]); name = m.group(0) if m else ''
            j += len(name)
            if j < len(s) and s[j] == '(':
                d, k = 1, j + 1
                while k < len(s) and d:
                    d += {'(': 1, ')': -1}.get(s[k], 0); k += 1
                arg = s[j + 1:k - 1]
                if name in ('is', 'not', 'has', 'matches'):
                    best = max((specificity(x) for x in top_split(arg, ',')), default=(0, 0, 0))
                    a, b, c = a + best[0], b + best[1], c + best[2]
                elif name == 'where':
                    pass
                elif pe:
                    c += 1
                else:
                    b += 1
                i = k
            else:
                if pe or name in ('before', 'after', 'first-line', 'first-letter', 'marker', 'placeholder', 'selection'):
                    c += 1
                else:
                    b += 1
                i = j
        elif re.match(r'[a-zA-Z*]', ch):
            m = re.match(r'[\w*-]+', s[i:]); tok = m.group(0)
            if tok != '*': c += 1
            i += len(tok)
        else:
            i += 1
    return (a, b, c)


IMAGE = re.compile(r'^(?:none|(?:repeating-)?(?:linear|radial|conic)-gradient\(|url\(|image-set\(|-webkit-[\w-]*gradient\()', re.I)
COLORW = re.compile(r'^(?:#[0-9a-fA-F]{3,8}|(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\(.*|transparent|currentcolor|'
                    r'white|black|red|green|blue|gray|grey|silver|orange|yellow|purple|pink|navy|teal|maroon)$', re.I)


def bg_component(value, prop):
    """the background-color or background-image a `background` shorthand sets, or None when it cannot be told (a bare
    var() could be either)."""
    layers = [l.strip() for l in top_split(value, ',')]
    images, color = [], 'transparent'
    for n, layer in enumerate(layers):
        words = [w for w in top_split(layer, ' ') if w.strip()]
        img = [w for w in words if IMAGE.match(w)]
        col = [w for w in words if COLORW.match(w)]
        if any(w.startswith('var(') for w in words if w not in img and w not in col):
            return None
        if len(img) > 1 or (col and n < len(layers) - 1):
            return None
        images.append(img[0] if img else 'none')
        if n == len(layers) - 1 and col:
            color = col[-1]
    return color if prop == 'background-color' else ','.join(images)


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def split_theme(part):
    """(theme prefix, key) of one theme selector part, or (None, None) when the theme attribute is not a leading root
    compound."""
    p = norm(NEG_THEME.sub('', part.replace(HACK, '')))
    m = PREFIX.match(p + ' ') if THEME.search(p) else None
    if not m:
        return None, None
    prefix, key = norm(m.group(1)), norm(m.group(2))
    if THEME.search(key):
        return None, None
    return prefix, key


def light_key(part):
    return norm(part.replace(HACK, ''))


def is_theme_rule(r):
    return 'sel' in r and bool(THEME.search(NEG_THEME.sub('', r['sel'].replace(HACK, ''))))


def slug(key, prop):
    k = re.sub(r'[^a-zA-Z0-9]+', '-', key).strip('-').lower()
    k = re.sub(r'-(axm-flat|flat|brief)\b', '', k)[:34].strip('-') or 'root'
    p = {'background': 'bg', 'background-color': 'bgc', 'background-image': 'bgi', 'color': 'fg', 'box-shadow': 'sh',
         'border-color': 'bc', 'text-shadow': 'tsh', 'outline-color': 'oc', 'text-decoration': 'td'}.get(prop, re.sub(r'^-+', '', prop))
    return '--t-%s-%s' % (k, p)


def theme_wants(rules, dead):
    """live theme declarations by (key, prop): [(rule index, part, prefix, value, important, ctx)]"""
    want = defaultdict(list)
    for r in rules:
        if not is_theme_rule(r):
            continue
        for prop, val, imp in r['decl']:
            if (r['i'], prop) in dead or SHAPE.match(prop) or imp:
                continue                       # important: kept on its rule (step 3), routed to its component file
            for part in top_split(r['sel'], ','):
                prefix, key = split_theme(part)
                if prefix is None:
                    continue
                if prop.startswith('--') and not key:
                    continue
                want[(key, prop)].append((r['i'], part, prefix, val, imp, tuple(r['ctx'])))
    return want


def theme_group(prefix):
    return tuple(sorted(re.sub(r'["\'\s]', '', m) for m in THEME.findall(prefix)))


def subj(part):
    comps = [c for c in top_split(norm(part), ' >+~') if c.strip()]
    return comps[-1].strip() if comps else ''


def outranks(t, part, imp, pos, i):
    """theme declaration t outranks the light declaration on selector part (rule i)"""
    if bool(t[4]) != bool(imp):
        return bool(t[4])
    ts_, ls = specificity(norm(t[1])), specificity(norm(part))
    return ts_ > ls or (ts_ == ls and pos[t[0]] > pos[i])


def candidates(rules, dead):
    """in-between light rules: a light selector B setting a property P that a theme declaration on key K (a different
    selector) outranked. B gets a token only when every element B matches also matches K (repair/s164b/subset_check.js),
    because the theme value showed on those elements before (scaphoid `figure.w5a .w5skip` under `[dark] .w5a .w5skip`;
    `#navlinks .pc-sect` under `[dark] #nav .sect`). Returns {B: {K: [P, ...]}}."""
    want = theme_wants(rules, dead)
    pos = {r['i']: n for n, r in enumerate(rules)}
    by_prop = defaultdict(list)
    for (k, prop), ts in want.items():
        if k:
            by_prop[prop].append((k, ts))
    out = OrderedDict()
    for r in rules:
        if 'sel' not in r or is_theme_rule(r):
            continue
        for part in top_split(r['sel'], ','):
            b = light_key(part)
            for prop, val, imp in r['decl']:
                for k, ts in by_prop.get(prop, []):
                    if k != b and any(outranks(t, part, imp, pos, r['i']) for t in ts):
                        ps = out.setdefault(b, OrderedDict()).setdefault(k, [])
                        if prop not in ps:
                            ps.append(prop)
    return out


def load_extra():
    p = os.path.join(WS, 'repair', 's164b', 'token_extra.json')
    ex = defaultdict(list)
    if os.path.exists(p):
        for kp, bs in json.load(open(p))['extra'].items():
            k, prop = kp.rsplit('|', 1)
            for b in bs:
                ex[(b, prop)].append(k)
    return ex


def run(rules, dead):
    """rules: css_rules.json rules (in order); dead: {(i, prop)}. Returns (new_rules, token_decls, report)."""
    rep = defaultdict(list)
    # custom properties set below the root (on body, .axm-flat, a brief...): a token holding var() of one of them would be
    # resolved at the root and miss the redefinition
    below = defaultdict(list)          # variable -> selectors (theme prefix removed) that set it below the root
    for r in rules:
        if 'sel' not in r:
            continue
        for part in top_split(r['sel'], ','):
            p = norm(NEG_THEME.sub('', part.replace(HACK, '')))
            key = split_theme(part)[1] if THEME.search(p) else p
            if key and key not in (':root', 'html'):
                for d in r['decl']:
                    if d[0].startswith('--') and key not in below[d[0]]:
                        below[d[0]].append(key)
    def scopes(v):
        out = []
        for m in re.findall(r'var\((--[\w-]+)', v):
            out.extend(k for k in below.get(m, []) if k not in out)
        return out
    def uses_below(v):
        return bool(scopes(v))
    want = theme_wants(rules, dead)
    extra = load_extra()             # (light key B, prop) -> [theme key K]: B's elements are a subset of K's
    # 2. light rules the theme declarations outranked get a token per rule
    tokens = OrderedDict()             # token -> literal light value (tokens.css)
    fallback = {}                      # token -> light value holding var(), kept in the rule as the fallback
    tok_of = {}                        # (light rule i, part, prop) -> token
    toks_for = defaultdict(list)       # (key, prop) -> tokens the theme sets
    used = set()
    pos = {r['i']: n for n, r in enumerate(rules)}
    add_of = defaultdict(list)         # (light rule i, part) -> [(longhand, token)] appended after a shorthand
    tok_ctx = {}                       # token -> media context of the light rule holding it
    skip = defaultdict(set)            # (theme rule i, part, prop) -> tokens it does not set (another theme rule won)
    for r in rules:
        if 'sel' not in r or is_theme_rule(r):
            continue
        for part in top_split(r['sel'], ','):
            key = light_key(part)
            own = {d[0] for d in r['decl']}
            todo = [(prop, val, imp, prop) for prop, val, imp in r['decl']]
            for prop, val, imp in r['decl']:
                if prop == 'background':
                    for lh in ('background-color', 'background-image'):
                        if lh not in own and want.get((key, lh)):
                            comp = bg_component(val, lh)
                            if comp is None:
                                rep['shorthand_unparsed'].append('%s { background:%s } vs %s' % (part.strip()[:80], val[:60], lh))
                            else:
                                todo.append((lh, comp, imp, 'background'))
            for prop, val, imp, src in todo:
                keys = [key] + [k for k in extra.get((key, prop), []) if k != key]
                entries = [(kk, t) for kk in keys for t in want.get((kk, prop), []) if outranks(t, part, imp, pos, r['i'])]
                if not entries:
                    if want.get((key, prop)):
                        rep['light_kept_literal'].append('%s { %s } outranks the theme rule' % (part.strip()[:90], prop))
                    continue
                name = base = slug(key, prop); n = 2
                while name in used:
                    name = '%s-%d' % (base, n); n += 1
                used.add(name)
                if 'var(' in val:
                    fallback[name] = val
                else:
                    tokens[name] = val
                tok_ctx[name] = tuple(r['ctx'])
                if src == prop:
                    tok_of[(r['i'], part.strip(), prop)] = name
                else:
                    add_of[(r['i'], part.strip())].append((prop, name, imp))
                for kk in OrderedDict.fromkeys(kk for kk, _ in entries):
                    toks_for[(kk, prop)].append(name)
                    if kk != key:
                        rep['extra_tokens'].append('%s { %s } carries %s' % (part.strip()[:80], prop, kk[:60]))
                # per theme, only the theme declaration that won on this rule's elements sets its token: the most
                # specific (then latest); a lower one is kept only where every higher one sits in another media
                groups = defaultdict(list)
                for kk, t in entries:
                    groups[theme_group(t[2])].append(t)
                for g, ts in groups.items():
                    ts.sort(key=lambda t: (specificity(norm(t[1])), pos[t[0]]), reverse=True)
                    emitted = []
                    for j, t in enumerate(ts):
                        if any(not f[5] or f[5] == t[5] for f in ts[:j]):
                            skip[(t[0], t[1].strip(), prop)].add(name)
                        else:
                            emitted.append(t)
                    if len(emitted) > 1 and sorted(emitted, key=lambda t: pos[t[0]]) != emitted[::-1]:
                        rep['order_risk'].append('%s { %s } %s' % (part.strip()[:80], prop, ' / '.join(norm(t[1])[:50] for t in emitted)))
    # a light rule's `background` token and the longhand tokens appended after it: a theme `background` shorthand resets
    # both longhands, so the theme rule sets the longhand tokens too (phone sculpted dark: `[dark] .tw{background:none}`
    # under 640px over the global `[dark] .tw{background-image:...}`)
    root_val = {}
    for r in rules:
        if r.get('sel', '').strip() == ':root' and not r['ctx']:
            for d in r['decl']:
                root_val[d[0]] = d[1].strip()
    bg_sib = {}
    for (li, lp), lhs in add_of.items():
        bn = tok_of.get((li, lp, 'background'))
        if bn:
            bg_sib[bn] = [(lh, nm) for lh, nm, _ in lhs]
    def ref(nm):
        return 'var(%s,%s)' % (nm, fallback[nm]) if nm in fallback else 'var(%s)' % nm
    # a token defined below the root on a scope (scoped_tokens) shadows the root for everything inside that scope, so
    # every theme rule that sets the token sets it on the same scopes too, in its own place and media (phone .tw
    # box-shadow none lost to the scoped global var(--e2) on .axm-flat)
    name_scopes = defaultdict(list)
    for r in rules:
        if not is_theme_rule(r):
            continue
        for prop, val, imp in r['decl']:
            sc = scopes(val)
            if not sc or imp or (r['i'], prop) in dead or SHAPE.match(prop):
                continue
            for part in top_split(r['sel'], ','):
                prefix, key = split_theme(part)
                for nm in (toks_for.get((key, prop)) or []) if prefix is not None else []:
                    if nm not in skip.get((r['i'], part.strip(), prop), ()):
                        name_scopes[nm].extend(k for k in sc if k not in name_scopes[nm])
    # 3. rewrite
    out = []
    shapes, dropped_dead = [], []
    for r in rules:
        if 'sel' not in r:
            out.append(r); continue
        if is_theme_rule(r):
            keep, theme_rules = [], []
            for prop, val, imp in r['decl']:
                if (r['i'], prop) in dead:
                    dropped_dead.append((r['i'], prop)); continue
                if SHAPE.match(prop):
                    shapes.append('%s { %s:%s }' % (norm(r['sel'])[:100], prop, val)); continue
                parts = top_split(r['sel'], ',')
                pure = all(split_theme(p)[0] is not None and split_theme(p)[1] == '' for p in parts)
                if pure:
                    keep.append([prop, val, imp]); continue
                if imp:
                    # an important theme value beats every normal rule (the tinted .tw tbody tr background over the
                    # zebra rule): it stays a declaration and competes in its component's layer
                    rep['important_kept'].append('%s { %s:%s !important }' % (norm(r['sel'])[:100], prop, val[:60]))
                    keep.append([prop, val, imp]); continue
                carried = True
                by_prefix = OrderedDict()
                for part in parts:
                    prefix, key = split_theme(part)
                    names = toks_for.get((key, prop)) if prefix is not None else None
                    if not names:
                        carried = False; continue
                    if not any(tok_ctx[nm] in ((), tuple(r['ctx'])) for nm in names):
                        # every light rule holding the token sits in a narrower media (#axtopfade{display:none} on the
                        # phone only): outside it the theme value has no rule to land on, so the declaration stays too
                        rep['ctx_uncovered'].append('%s { %s:%s } light only in %s' % (norm(part)[:90], prop, val[:40], sorted({tok_ctx[nm] for nm in names})))
                        carried = False
                    by_prefix.setdefault(prefix, []).extend(nm for nm in names if nm not in skip.get((r['i'], part.strip(), prop), ()))
                sc = scopes(val)
                if sc:
                    rep['scoped_tokens'].append('%s { %s:%s } also on %s' % (norm(r['sel'])[:90], prop, val[:60], ', '.join(sc)[:80]))
                for prefix, names in by_prefix.items():
                    if not names:
                        continue
                    decl = [[nm, val, False] for nm in OrderedDict.fromkeys(names)]
                    if prop == 'background':
                        for nm in OrderedDict.fromkeys(names):
                            for lh, ln in bg_sib.get(nm, []):
                                comp = bg_component(val, lh)
                                mv = re.fullmatch(r'\s*var\((--[\w-]+)\)\s*', val)
                                if comp is None and mv and COLORW.match(root_val.get(mv.group(1), '')):
                                    # a bare var() holding a color on the root (--dk, --glass, --ink): a color layer
                                    comp = val.strip() if lh == 'background-color' else 'none'
                                if comp is None:
                                    rep['bg_sibling_unparsed'].append('%s { background:%s } -> %s' % (norm(r['sel'])[:80], val[:50], ln))
                                else:
                                    decl.append([ln, comp, False])
                                    rep['bg_sibling_set'].append('%s { background } sets %s' % (norm(r['sel'])[:80], ln))
                    theme_rules.append(dict(r, sel=prefix, decl=decl, i=r['i'], tok=True))
                    # the value uses a variable redefined below the root: define the token there too, so var() is
                    # resolved where that variable is set
                    for k in OrderedDict.fromkeys(k for nm in names for k in name_scopes.get(nm, [])):
                        theme_rules.append(dict(r, sel=prefix + ' ' + k, decl=decl, i=r['i'], tok=True))
                if not carried:
                    rep['no_light_rule'].append('%s { %s:%s }' % (norm(r['sel'])[:110], prop, val))
                    keep.append([prop, val, imp])
            if keep:
                out.append(dict(r, decl=keep))
            out.extend(theme_rules)
            continue
        parts = top_split(r['sel'], ',')
        hit = [p for p in parts if any((r['i'], p.strip(), d[0]) in tok_of for d in r['decl']) or (r['i'], p.strip()) in add_of]
        if not hit:
            out.append(r); continue
        rest = [p for p in parts if p not in hit]
        if rest:
            out.append(dict(r, sel=','.join(rest)))
        for p in hit:
            decl = []
            for d in r['decl']:
                k = (r['i'], p.strip(), d[0])
                decl.append([d[0], ref(tok_of[k]), d[2]] if k in tok_of else d)
                if d[0] == 'background':
                    decl.extend([lh, ref(nm), im] for lh, nm, im in add_of.get((r['i'], p.strip()), []))
            out.append(dict(r, sel=p.strip(), decl=decl))
    rep['shapes_dropped'] = shapes
    rep['dead_dropped'] = ['%d %s' % k for k in dropped_dead]
    rep['counts'] = {'tokens': len(tokens) + len(fallback), 'fallback_in_rule': len(fallback), 'scoped_tokens': len(rep['scoped_tokens']), 'keys': len(toks_for), 'shapes_dropped': len(shapes), 'dead_dropped': len(dropped_dead),
                     'no_light_rule': len(rep['no_light_rule']), 'important_kept': len(rep['important_kept']), 'extra_tokens': len(rep['extra_tokens']), 'skipped': sum(len(v) for v in skip.values()), 'order_risk': len(rep['order_risk']), 'ctx_uncovered': len(rep['ctx_uncovered']), 'bg_sibling_set': len(rep['bg_sibling_set']), 'bg_sibling_unparsed': len(rep['bg_sibling_unparsed']), 'light_kept_literal': len(rep['light_kept_literal']),
                     'shorthand_unparsed': len(rep['shorthand_unparsed']), 'longhands_added': sum(len(v) for v in add_of.values())}
    return out, tokens, rep


def load_dead():
    dead = set()
    p = os.path.join(WS, 'repair', 's164b', 'dead_theme.json')
    if os.path.exists(p):
        for e in json.load(open(p))['dead']:
            dead.add((e['i'], e['prop']))
    return dead


if __name__ == '__main__':
    css = json.load(open(os.path.join(WS, 'local', 's164b', 'css_rules.json')))
    if '--candidates' in sys.argv:
        c = candidates(css['rules'], load_dead())
        json.dump(c, open(os.path.join(WS, 'local', 's164b', 'extra_candidates.json'), 'w'), indent=1)
        print('candidates: %d light selectors, %d (B, K) pairs' % (len(c), sum(len(v) for v in c.values())))
        sys.exit(0)
    out, tokens, rep = run(css['rules'], load_dead())
    json.dump(rep, open(os.path.join(WS, 'local', 's164b', 'tokens_report.json'), 'w'), indent=1)
    print(rep['counts'])
