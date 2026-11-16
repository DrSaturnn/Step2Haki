#!/usr/bin/env python3
"""style_surface.py: what a theme or legibility audit can see, so an audit runs only on what changed (the owner
2026-11-08, s170: "yes lets enforce it. Absolutely, ensure theme audits are optimized").

A page's style surface is (1) every CSS rule of the built page, flattened with its @media/@layer context, and (2) every
element signature (tag, classes, inline style) in the body. Brief text is not part of it: a text-only edit changes no
surface, so it never triggers an audit. The last audited surface per tool is kept in the tracked record
repair/efficiency/style_audits.json (it survives a fresh container; local/ does not).

  python3 tools/style_surface.py plan PAGE --tool legib|theme [--css EXTRA.css] [--views desk,phone]
        print what the tool must audit against its record (exit 0); "nothing" when no change can show
  python3 tools/style_surface.py seed PAGE --tool legib|theme --reason "..." [--sigs-from PAGE2] [--label L]
        write the record without an audit, when an audit of this surface already happened (the reason names it)
  python3 tools/style_surface.py show [--tool T]     print the record's header lines

legib plan: each changed rule (added, or removed since the record) maps to the views its @media allows (phone 390 px,
desk 1180 px), the themes its selector scopes ([data-theme=dark] dark and tinted, [data-glass=tinted] tinted), the modes
(.axm-flat flat, .axm-study/body.study study), Two-pane ([data-layout=two], desk) and accent ([data-axa=X]); a rule that
sets only size, spacing or layout properties is measured in light and sculpted alone (a theme changes color only,
D-20261105-10). The rule's selector, with states, pseudo-elements and theme or mode tokens removed, is matched against
the page: a rule that matches no element inside a brief is chrome and needs no brief audit (legib measures only briefs);
an unparseable selector falls back to the sample briefs. For each view, theme and mode the fewest briefs that cover
every changed rule are chosen (greedy cover). New element signatures (a class combination or inline style the record
has not seen) put the briefs holding them in every view, theme and mode.
theme plan: theme_gate.js reloads the whole page per view, so it either runs or not: it runs when a changed rule is
theme- or mode-scoped or sets a paint property, when a new element signature appears, when the views or theme_gate.js
changed, or when no record exists.
"""
import base64, datetime, hashlib, json, os, re, sys, zlib
from itertools import product

import tinycss2

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORD = os.path.join(WS, 'repair', 'efficiency', 'style_audits.json')
VIEWS = {'phone': 390, 'desk': 1180}
THEMES = ('light', 'dark', 'tinted')
MODES = ('sculpted', 'flat', 'study')
THEME_TOOLS = ['tools/theme_gate.js']
# properties that move no color, shadow, border or fill: a theme never changes them (D-20261105-10), so a rule setting
# only these is measured in one theme and one look; any property not listed (custom properties included) counts as paint
NONPAINT = set('''font-size line-height letter-spacing word-spacing font-family font-weight font-style font-variant
font-stretch font-feature-settings font-variation-settings text-transform text-align text-indent white-space
word-break overflow-wrap hyphens tab-size width min-width max-width height min-height max-height inline-size
block-size margin margin-top margin-right margin-bottom margin-left margin-inline margin-block margin-inline-start
margin-inline-end margin-block-start margin-block-end padding padding-top padding-right padding-bottom padding-left
padding-inline padding-block padding-inline-start padding-inline-end padding-block-start padding-block-end gap
row-gap column-gap display grid grid-template grid-template-columns grid-template-rows grid-template-areas
grid-column grid-row grid-area grid-auto-flow grid-auto-columns grid-auto-rows flex flex-direction flex-wrap
flex-flow flex-grow flex-shrink flex-basis justify-content justify-items justify-self align-content align-items
align-self place-content place-items place-self order position top right bottom left inset inset-inline
inset-block z-index overflow overflow-x overflow-y vertical-align float clear columns column-count column-width
box-sizing transition transition-property transition-duration transition-timing-function transition-delay
animation animation-name animation-duration animation-delay animation-timing-function animation-iteration-count
animation-fill-mode cursor content-visibility contain contain-intrinsic-size will-change pointer-events
user-select list-style list-style-type list-style-position aspect-ratio scroll-margin scroll-margin-top
scroll-padding scroll-padding-top scroll-behavior touch-action resize table-layout border-collapse
border-spacing caption-side empty-cells counter-reset counter-increment quotes object-fit object-position'''.split())
STATE = re.compile(r':(?:hover|focus-visible|focus-within|focus|active|visited|target|checked|disabled|enabled|link|'
                   r'any-link|open|popover-open|modal|fullscreen|placeholder-shown|indeterminate|default|'
                   r'-webkit-[\w-]+|-moz-[\w-]+)(?![\w-])')
PSEUDO_EL = re.compile(r'::?(?:before|after|marker|placeholder|selection|first-line|first-letter|backdrop|'
                       r'file-selector-button|-webkit-[\w-]+|-moz-[\w-]+)(?:\([^)]*\))?')
SCOPE_ATTR = re.compile(r'\[data-(?:theme|glass|layout|axa)(?:[~|^$*]?=[^\]]*)?\]')
SCOPE_CLASS = re.compile(r'\.axm-(?:flat|study)(?![\w-])')
ROOTISH = re.compile(r'(^|[\s>+~(,])(html|body|:root)((?:[.#\[:][^\s>+~,()]*)+)')


def h12(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:12]


def fdigest(rel):
    p = os.path.join(WS, rel)
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16] if os.path.exists(p) else '-'


# ---------------------------------------------------------------- surface
def page_css(html):
    return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))


def flat_rules(css):
    """[(context, selector, [property names], content)] for every style rule, nested @media/@layer/@supports flattened"""
    out = []

    def walk(rules, ctx):
        for r in rules:
            if r.type == 'qualified-rule':
                props = [d.lower_name for d in tinycss2.parse_declaration_list(r.content, skip_comments=True, skip_whitespace=True)
                         if d.type == 'declaration']
                out.append((list(ctx), ' '.join(tinycss2.serialize(r.prelude).split()), props,
                            ' '.join(tinycss2.serialize(r.content).split())))
            elif r.type == 'at-rule' and r.content is not None:
                pre = ' '.join(tinycss2.serialize(r.prelude).split())
                if r.lower_at_keyword in ('media', 'layer', 'supports', 'container', 'scope'):
                    walk(tinycss2.parse_rule_list(r.content, skip_comments=True, skip_whitespace=True),
                         ctx + ['@%s %s' % (r.lower_at_keyword, pre)])
                else:                                       # @keyframes, @font-face: one opaque paint rule
                    out.append((list(ctx), '@%s %s' % (r.lower_at_keyword, pre), ['@' + r.lower_at_keyword],
                                ' '.join(tinycss2.serialize(r.content).split())))
    walk(tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True), [])
    return out


def soup_of(html):
    from bs4 import BeautifulSoup
    return BeautifulSoup(html, 'lxml')


def sig_of(e):
    return '%s|%s|%s' % (e.name, ' '.join(sorted(e.get('class', []))), ' '.join((e.get('style') or '').split()))


def surface(page, extra_css=''):
    html = open(page, encoding='utf-8').read()
    soup = soup_of(html)
    rules = {}
    for ctx, sel, props, content in flat_rules(page_css(html) + '\n' + extra_css):
        rules[h12(json.dumps([ctx, sel, content]))] = [ctx, sel, props]
    sigs = sorted({sig_of(e) for e in soup.body.find_all(True)}) if soup.body else []
    return {'rules': rules, 'sigs': sigs}, soup


def pack(sf):
    return base64.b64encode(zlib.compress(json.dumps(sf, separators=(',', ':')).encode('utf-8'), 9)).decode('ascii')


def unpack(blob):
    return json.loads(zlib.decompress(base64.b64decode(blob)).decode('utf-8'))


def fingerprint(sf):
    return h12(json.dumps([sorted(sf['rules']), sf['sigs']]))


# ---------------------------------------------------------------- record
def load_record():
    try:
        return json.load(open(RECORD, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def write_record(tool, sf, label, note, extra=None):
    rec = load_record()
    rec['_doc'] = ('Last audited style surface per tool (tools/style_surface.py); a tool plans its next audit against '
                   'this entry. Written by legib_audit.py and ui_gate.py after a run, or by style_surface.py seed.')
    e = {'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'label': label, 'note': note,
         'fingerprint': fingerprint(sf), 'rules': len(sf['rules']), 'sigs': len(sf['sigs'])}
    e.update(extra or {})
    e['surface'] = pack(sf)
    rec[tool] = e
    os.makedirs(os.path.dirname(RECORD), exist_ok=True)
    json.dump(rec, open(RECORD, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    open(RECORD, 'a').write('\n')
    return e


# ---------------------------------------------------------------- classify one rule
def media_views(ctx):
    """views a rule's @media context allows; None when a query cannot be read (both views)"""
    ok = set(VIEWS)
    for c in ctx:
        if not c.startswith('@media'):
            continue
        q = c[6:].strip().lower()
        if re.search(r'\bprint\b', q) or 'prefers-reduced-motion:reduce' in q.replace(' ', ''):
            return set()
        if re.search(r'\bnot\b|\bor\b|,', q):
            continue                                   # unread query: keep both views (conservative)
        for kind, n in re.findall(r'(max|min)-width\s*:\s*([\d.]+)px', q):
            n = float(n)
            ok = {v for v in ok if (VIEWS[v] <= n if kind == 'max' else VIEWS[v] >= n)}
    return ok


def classify(ctx, sel, props):
    """the view, theme, mode, accent and layout combinations in which a rule can change what legib measures"""
    paint = any(p not in NONPAINT for p in props)
    views = media_views(ctx)
    s = sel.replace('"', '').replace("'", '')
    if ':not([data-theme' in s or ':not([data-glass' in s:
        themes = set(THEMES)
    elif 'data-glass=tinted' in s:
        themes = {'tinted'}
    elif '[data-theme' in s:
        themes = {'dark', 'tinted'}
    else:
        themes = set(THEMES) if paint else {'light'}
    if re.search(r'\.axm-study(?![\w-])|body\.study(?![\w-])', s):
        modes = {'study'}
    elif re.search(r'\.axm-flat(?![\w-])', s):
        modes = {'flat'}
    else:
        modes = {'sculpted', 'flat'} if paint else {'sculpted'}
    layout = 'two' if 'data-layout=two' in s else ''
    if layout:
        views &= {'desk'}
    m = re.search(r'\[data-axa=([\w-]+)\]', s)
    accent = m.group(1) if m else ''
    return {(v, t, md, accent, layout) for v, t, md in product(sorted(views), sorted(themes), sorted(modes))}, paint


def split_list(sel):
    out, depth, cur = [], 0, ''
    for ch in sel:
        depth += ch in '([' and 1 or (ch in ')]' and -1 or 0)
        if ch == ',' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    return out + [cur]


def normalize(one):
    s = PSEUDO_EL.sub('', one)
    s = STATE.sub('', s)
    s = SCOPE_ATTR.sub('', s)
    s = SCOPE_CLASS.sub('', s)
    s = ROOTISH.sub(lambda m: m.group(1) + m.group(2).replace(':root', 'html'), s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'^[>+~]\s*', '', s)
    s = re.sub(r'([>+~])\s*$', '', s).strip()
    return s or '*'


def brief_ids_of(soup):
    return [b['id'] for b in soup.select('.brief[id]')]


def match_briefs(sel, soup):
    """brief ids holding an element the selector matches; None when the selector cannot be matched (unknown)"""
    if sel.startswith('@'):
        return None
    found = set()
    for one in split_list(sel):
        try:
            els = soup.select(normalize(one))
        except Exception:
            return None
        for e in els:
            b = e if (e.get('id') and 'brief' in e.get('class', [])) else e.find_parent(
                lambda t: t.get('id') and 'brief' in t.get('class', []))
            if b is not None:
                found.add(b['id'])
    return found


def sample_briefs(soup, cap=6):
    """fewest briefs (up to cap) covering the most element signatures found inside briefs: the full-audit sample"""
    sets = {b['id']: {sig_of(e) for e in b.find_all(True)} | {sig_of(b)} for b in soup.select('.brief[id]')}
    left, pick = set().union(*sets.values()) if sets else set(), []
    while left and len(pick) < cap:
        bid = max(sets, key=lambda k: (len(sets[k] & left), k))
        if not sets[bid] & left:
            break
        pick.append(bid); left -= sets[bid]
    return pick


def cover(need):
    """need: {item: set(brief ids)} -> fewest briefs touching every item (greedy, stable by brief id)"""
    left, pick = {k: v for k, v in need.items() if v}, []
    while left:
        counts = {}
        for v in left.values():
            for b in v:
                counts[b] = counts.get(b, 0) + 1
        b = min(counts, key=lambda k: (-counts[k], k))
        pick.append(b)
        left = {k: v for k, v in left.items() if b not in v}
    return sorted(pick)


# ---------------------------------------------------------------- diff and plans
def diff(old, new):
    added = {k: v for k, v in new['rules'].items() if k not in old['rules']}
    removed = {k: v for k, v in old['rules'].items() if k not in new['rules']}
    sigs = sorted(set(new['sigs']) - set(old['sigs']))
    return added, removed, sigs


def plan_legib(sf, soup, rec_entry):
    """{'runs': [{'view','theme','mode','accent','layout','briefs'}], 'why': [...]}; no runs means nothing to audit"""
    why, need = [], {}
    if not rec_entry:
        sample = sample_briefs(soup)
        why.append('no legib record: full audit of the sample briefs %s' % ','.join(sample))
        for c in product(sorted(VIEWS), THEMES, MODES, [''], ['']):
            need.setdefault(c, {})['sample'] = set(sample)
        return finish(need, why)
    added, removed, sigs = diff(unpack(rec_entry['surface']), sf)
    chrome = unknown = 0
    sample = None
    for k, (ctx, sel, props) in list(added.items()) + list(removed.items()):
        combos, _ = classify(ctx, sel, props)
        if not combos:
            continue
        b = match_briefs(sel, soup)
        if b is None:
            unknown += 1
            sample = sample if sample is not None else set(sample_briefs(soup))
            b = sample
        if not b:
            chrome += 1
            continue
        for c in combos:
            need.setdefault(c, {})['rule ' + k] = b
    holders = {}
    if sigs:
        want = set(sigs)
        for br in soup.select('.brief[id]'):
            for e in [br] + br.find_all(True):
                s = sig_of(e)
                if s in want:
                    holders.setdefault(s, set()).add(br['id'])
        for s, b in holders.items():
            for c in product(sorted(VIEWS), THEMES, MODES, [''], ['']):
                need.setdefault(c, {})['sig ' + s] = b
    why.append('against %s (%s): %d rule(s) added, %d removed (%d chrome only, %d unreadable selector(s)); '
               '%d new element signature(s), %d inside briefs' % (rec_entry.get('label'), rec_entry.get('date'),
                                                                  len(added), len(removed), chrome, unknown, len(sigs), len(holders)))
    return finish(need, why)


def finish(need, why):
    runs = []
    for (v, t, m, acc, lay), items in sorted(need.items()):
        b = cover(items)
        if b:
            runs.append({'view': v, 'theme': t, 'mode': m, 'accent': acc, 'layout': lay, 'briefs': b})
    return {'runs': runs, 'why': why}


def theme_reasons(sf, rec_entry, views):
    """reasons theme_gate must run; empty means the record's pass still holds"""
    if not rec_entry:
        return ['no theme record']
    r = []
    if rec_entry.get('views') != views:
        r.append('views %s, record %s' % (views, rec_entry.get('views')))
    tools = {t: fdigest(t) for t in THEME_TOOLS}
    if rec_entry.get('tools') != tools:
        r.append('theme_gate.js changed')
    added, removed, sigs = diff(unpack(rec_entry['surface']), sf)
    themed = [v[1] for v in list(added.values()) + list(removed.values())
              if classify(*v)[1] or SCOPE_ATTR.search(v[1]) or SCOPE_CLASS.search(v[1])]
    if themed:
        r.append('%d changed rule(s) set paint or are theme or mode scoped (first: %s)' % (len(themed), themed[0][:80]))
    if sigs:
        r.append('%d new element signature(s) (first: %s)' % (len(sigs), sigs[0][:80]))
    return r


def main(argv):
    if not argv or argv[0] not in ('plan', 'seed', 'show'):
        sys.exit(__doc__.strip())
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
    if argv[0] == 'show':
        rec = load_record()
        for t, e in rec.items():
            if t.startswith('_') or (opt('--tool') and t != opt('--tool')):
                continue
            print('%s: %s %s fingerprint %s, %d rules, %d signatures; %s' % (t, e['date'], e['label'], e['fingerprint'],
                                                                           e['rules'], e['sigs'], e.get('note', '')))
        return 0
    page, tool = argv[1], opt('--tool')
    if tool not in ('legib', 'theme'):
        sys.exit('style_surface: --tool legib or theme')
    extra = open(opt('--css'), encoding='utf-8').read() if opt('--css') else ''
    sf, soup = surface(page, extra)
    if argv[0] == 'seed':
        if not opt('--reason'):
            sys.exit('style_surface seed: --reason names the audit that already covered this surface')
        if opt('--sigs-from'):
            sf['sigs'] = surface(opt('--sigs-from'))[0]['sigs']
        extra_e = {'views': opt('--views', 'desk,phone'), 'tools': {t: fdigest(t) for t in THEME_TOOLS}} if tool == 'theme' else {}
        e = write_record(tool, sf, opt('--label', 'seed'), 'seeded without an audit: ' + opt('--reason'), extra_e)
        print('style_surface: %s record seeded, fingerprint %s (%d rules, %d signatures)' % (tool, e['fingerprint'], e['rules'], e['sigs']))
        return 0
    rec = load_record().get(tool)
    if tool == 'theme':
        r = theme_reasons(sf, rec, opt('--views', 'desk,phone'))
        print('theme: ' + ('run: ' + '; '.join(r) if r else 'nothing: no change a theme can show since %s (%s)' % (rec['label'], rec['date'])))
        return 0
    p = plan_legib(sf, soup, rec)
    print('legib: ' + '; '.join(p['why']))
    if not p['runs']:
        print('legib: nothing to audit')
    for r in p['runs']:
        print('  %s %s %s%s%s: %s' % (r['view'], r['theme'], r['mode'], ' accent ' + r['accent'] if r['accent'] else '',
                                      ' layout ' + r['layout'] if r['layout'] else '', ','.join(r['briefs'])))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
