"""ui_lint.py (draft, 2026-11-05): structure checks for the Step2Haki page, so UI rules hold even when a chat or agent skips
a section of the docs. Proposed home: tools/spine/ui_lint.py, run by gate.py and ship.sh.

Ratchet design: the current page has debt (layered override blocks, theme rules that move layout). The check records today's
counts in a baseline file and fails any build that makes a count WORSE; a refactor batch lowers the baseline. So nothing new
can be added the old way, and the debt can only shrink.

Usage:
  python3 ui_lint.py PAGE.html                      # report
  python3 ui_lint.py PAGE.html --baseline B.json    # fail (exit 1) if any count rose above the baseline
  python3 ui_lint.py PAGE.html --write-baseline B.json
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
        for part in sel.split(','):
            p = part.strip()
            if p and not p.startswith('@') and p not in ('from', 'to') and not re.match(r'^\d+%$', p):
                counts[p] = counts.get(p, 0) + 1
    dup = sorted([(n, s) for s, n in counts.items() if n >= 4], reverse=True)
    # motion: every transition or animation timing should be a spring token (var(--spr) smooth, var(--bnc) bouncy, var(--snp)
    # snappy), SwiftUI style; plain ease/linear/cubic-bezier timings are counted
    motion = re.findall(r'(?:transition|animation)(?:-timing-function)?\s*:([^;}]*)', css_nc)
    non_spring = [m.strip()[:80] for m in motion if m.strip() not in ('none', 'unset', 'initial', 'inherit')
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

def main(a):
    if not a: print(__doc__); return 2
    m = measure(open(a[0], encoding='utf-8').read())
    nums = {k: v for k, v in m.items() if not k.startswith('_')}
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
