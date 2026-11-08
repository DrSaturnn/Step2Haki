"""ui_lint.py (2026-11-05; wired into tools/gate.py as checks ui-lint and ui-site, D-20261106-11): structure checks for the
Step2Haki page, so UI rules hold even when a chat or agent skips a section of the docs.

Ratchet design: the current page has debt (layered override blocks, theme rules that move layout). The check records today's
counts in a baseline file and fails any build that makes a count WORSE; a refactor batch lowers the baseline. So nothing new
can be added the old way, and the debt can only shrink.

Usage:
  python3 ui_lint.py PAGE.html                      # report
  python3 ui_lint.py PAGE.html --baseline B.json    # fail (exit 1) if any count rose above the baseline
  python3 ui_lint.py PAGE.html --write-baseline B.json
  python3 ui_lint.py PAGE.html --tighten B.json     # lower each baseline count to the page's count (never raises); ship.sh
                                                    # runs it before the commit, with the site/ raw-color count
  python3 ui_lint.py --site [site] [--examples] [--hard]   # D-20261105-10 checks over site/css; --hard exits 1 on any
"""
import json, re, sys

LAYOUT = re.compile(r'(?:^|;)\s*(display|position|float|width|height|min-width|max-width|min-height|max-height|margin[\w-]*|'
                    r'padding[\w-]*|top|left|right|bottom|inset|grid[\w-]*|flex[\w-]*|gap|column[\w-]*|transform|zoom|order)\s*:', re.I)

def measure(html):
    styles = re.findall(r'<style([^>]*)>(.*?)</style>', html, re.S)
    css = '\n'.join(body for _, body in styles)
    css_nc = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    rules = re.findall(r'([^{}]+)\{([^{}]*)\}', css_nc)
    theme = [(sel.strip(), body) for sel, body in rules if 'data-theme' in sel]
    theme_layout = sorted({sel[:140] for sel, body in theme if LAYOUT.search(body)})
    counts = {}
    for sel, _ in rules:
        for part in re.split(r',(?![^()]*\))', sel):
            p = part.strip()
            if p and not p.startswith('@') and p not in ('from', 'to') and not re.match(r'^\d+%$', p):
                counts[p] = counts.get(p, 0) + 1
    dup = sorted([(n, s) for s, n in counts.items() if n >= 4], reverse=True)
    # motion: every transition or animation timing should be a spring token (var(--spr) smooth, var(--bnc) bouncy, var(--snp)
    # snappy), SwiftUI style; plain ease/linear/cubic-bezier timings are counted
    motion = re.findall(r'(?:transition|animation)(?:-timing-function)?\s*:([^;}]*)', css_nc)
    non_spring = [m.strip()[:80] for m in motion if re.sub(r'\s*!important$', '', m.strip()) not in ('none', 'unset', 'initial', 'inherit')
                  and 'var(--spr' not in m and 'var(--bnc' not in m and 'var(--snp' not in m]
    # comments in the shipped page (D-20261105-6): the build should strip them all
    js = '\n'.join(re.findall(r'<script(?![^>]*application/(?:ld\+)?json)[^>]*>(.*?)</script>', html, re.S))
    comments = (re.findall(r'/\*.*?\*/', css, re.S) + re.findall(r'/\*.*?\*/', js, re.S)
                + re.findall(r'(?<![:\'"\\/])//[^\n]*', js) + re.findall(r'<!--.*?-->', html, re.S))
    narration = [c for c in comments if re.search(r'Jonathan|\bs1\d\d[a-z]?\b|DIGEST|STANDING|handoff|Decided', c)]
    return {
        'style_blocks': len(styles),
        'script_blocks': len(re.findall(r'<script\b', html)),
        'important': css_nc.count('!important'),
        'specificity_hacks': css_nc.count('html:is([data-theme],:not([data-theme]))'),
        'theme_rules_setting_layout': len(theme_layout),
        'selectors_defined_4plus': len(dup),
        'motion_not_spring': len(non_spring),
        'comments_shipped': len(comments),
        'comments_with_decision_narration': len(narration),
        '_examples': {'theme_rules_setting_layout': theme_layout[:15], 'selectors_defined_4plus': [s for _, s in dup[:15]], 'motion_not_spring': non_spring[:15], 'comments_with_decision_narration': [c[:100] for c in narration[:10]]},
    }

THEME_SEL = re.compile(r'^(?:(?:html|:root)?(?:\[data-(?:theme|axa|glass)[^\]]*\])+\s*)+$')
# a scoped token (Jonathan 2026-11-05, s164b): '<theme prefix> <scope>' holding only --t- custom properties, where the
# theme value uses a variable that the scope element sets below the root (.axm-flat, figure.sw, .lcc)
THEME_SCOPED = re.compile(r'^(?:(?:html|:root)?(?:\[data-(?:theme|axa|glass)[^\]]*\])+\s+)+\S.*$')
RAW_COLOR = re.compile(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(|'
                       r'\b(?:white|black|red|green|blue|gray|grey|silver|orange|yellow|purple|pink|navy|teal|maroon)\b', re.I)


def site_checks(site):
    """D-20261105-10 hard fails over the site/ sources: (1) a themes/ file holds only custom properties on a theme
    selector; (2) a components/ file names no raw color (colors come from var() tokens). Returns (counts, examples)."""
    import glob, os, tinycss2
    out = {'theme_noncustom_decl': [], 'theme_component_selector': [], 'component_raw_color': []}

    def rules(nodes, ctx):
        for n in nodes:
            if n.type == 'qualified-rule':
                yield ctx, tinycss2.serialize(n.prelude).strip(), n.content
            elif n.type == 'at-rule' and n.content is not None and n.lower_at_keyword in ('media', 'supports', 'layer', 'container'):
                yield from rules(tinycss2.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True), ctx + [n.lower_at_keyword])

    for f in sorted(glob.glob(os.path.join(site, 'css', '**', '*.css'), recursive=True)):
        rel = os.path.relpath(f, os.path.join(site, 'css'))
        kind = rel.split(os.sep)[0]
        if kind not in ('themes', 'components'):
            continue
        sheet = tinycss2.parse_stylesheet(open(f, encoding='utf-8').read(), skip_comments=True, skip_whitespace=True)
        for ctx, sel, content in rules(sheet, []):
            decls = [d for d in tinycss2.parse_declaration_list(content, skip_comments=True, skip_whitespace=True) if d.type == 'declaration']
            if kind == 'themes':
                scoped_ok = bool(decls) and all(d.name.startswith('--t-') for d in decls)
                bad_sel = [s.strip() for s in sel.split(',') if not (THEME_SEL.match(s.strip()) or
                           (scoped_ok and THEME_SCOPED.match(s.strip())))]
                if bad_sel:
                    out['theme_component_selector'].append(rel + ': ' + sel[:120])
                for d in decls:
                    if not d.name.startswith('--'):
                        out['theme_noncustom_decl'].append(rel + ': ' + sel[:80] + ' { ' + d.name + ' }')
            else:
                for d in decls:
                    if d.name.startswith('--') or d.lower_name in ('content', 'font-family', 'quotes'):
                        continue
                    val = tinycss2.serialize(d.value)
                    # a token color with an alpha, rgba(var(--acc-rgb),.12), takes its color from a token (s167)
                    val = re.sub(r'\b(?:rgba?|hsla?)\(\s*var\(--[\w-]+\)\s*,\s*[\d.]+%?\s*\)', '', val)
                    val = re.sub(r'var\(--[\w-]+\)', '', val)          # bare token references
                    val = re.sub(r'url\([^)]*\)', '', val)
                    if RAW_COLOR.search(val):
                        out['component_raw_color'].append(rel + ': ' + sel[:80] + ' { ' + d.name + ': ' + val.strip()[:60] + ' }')
    return {k: len(v) for k, v in out.items()}, {k: v[:15] for k, v in out.items()}


def main(a):
    if not a: print(__doc__); return 2
    if a[0] == '--site':
        counts, ex = site_checks(a[1] if len(a) > 1 and not a[1].startswith('--') else 'site')
        if '--examples' in a:
            print(json.dumps(ex, indent=2))
        bad = {k: v for k, v in counts.items() if v}
        if bad and '--hard' in a:
            print('UI-LINT FAIL (D-20261105-10): themes hold only custom properties on theme selectors; components take colors from var() tokens:', bad)
            return 1
        print('UI-LINT SITE', 'PASS' if not bad else 'REPORT', counts); return 0
    m = measure(open(a[0], encoding='utf-8').read())
    nums = {k: v for k, v in m.items() if not k.startswith('_')}
    if '--tighten' in a:
        path = a[a.index('--tighten') + 1]
        base = json.load(open(path))
        try:
            nums['component_raw_color'] = site_checks('site')[0]['component_raw_color']
        except Exception:
            pass
        tight = {k: (min(v, nums[k]) if k in nums else v) for k, v in base.items()}
        lowered = {k: (base[k], tight[k]) for k in base if tight[k] != base[k]}
        json.dump(tight, open(path, 'w'), indent=2); open(path, 'a').write('\n')
        print('UI-LINT baseline tightened', lowered if lowered else '(no change)'); return 0
    if '--write-baseline' in a:
        json.dump(nums, open(a[a.index('--write-baseline') + 1], 'w'), indent=2); print('baseline written', nums); return 0
    if '--baseline' in a:
        base = json.load(open(a[a.index('--baseline') + 1]))
        worse = {k: (base.get(k), v) for k, v in nums.items() if base.get(k) is not None and v > base[k]}
        if worse:
            print('UI-LINT FAIL: counts rose above the baseline (was, now):', worse)
            print('Fix: replace the old rule instead of adding an override; put colors in theme tokens, not layout in themes;')
            print('     time every transition and animation with a spring token (var(--spr), var(--bnc), var(--snp));')
            print('     no decision history in code comments (it belongs in git, the digest and UI_MAP.md).')
            return 1
        print('UI-LINT PASS', nums); return 0
    print(json.dumps(m, indent=2)); return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
