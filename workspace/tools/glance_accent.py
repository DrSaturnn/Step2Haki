"""glance_accent: s136 accent setting (Jonathan 2026-10-14) as edits for repair/build.py.

  python3 tools/glance_accent.py <page.html> <out.json>      write the edits (replace_global ops)
  python3 tools/glance_accent.py --test                      offline checks

The accent used to be a literal purple in many rules (rgba(84,74,196,a), #544AC4 and its tints such as #F2F1FA). A
token changes only where a rule reads the token, and an override block cannot replace a literal without also
changing which rule wins, so each such rule is rewritten in place with the same selector and the colors swapped for
accent tokens:
  rgba(84,74,196,a)    -> rgba(var(--acc-rgb),a)
  #544AC4              -> var(--accent)
  a purple tint #RRGGBB -> var(--axh-RRGGBB), defined per accent as the same mix of the accent with white (lighter
                          tints) or black (darker shades) that the tint was of the original purple
and, separately, text set in the faint grey (color:var(--faint)) reads the muted grey (s136 scope 4).

Left alone: principle indigo (#3A3E70 family, hue under 238), the dark sidebar tile colors (lightness under 30%), and
everything outside the head's style blocks (inline SVG charts). Each rule's find text must occur once in the page;
the tool widens it with the text before it until it does, and fails if it cannot.
"""
import colorsys
import json
import re
import sys

ACCENTS = [  # (key, name, hex): Jonathan 2026-10-14; Slate is the default
    ('slate', 'Slate', '#3B5B8C'), ('indigo', 'Indigo', '#5856D6'), ('purple', 'Purple', '#544AC4'),
    ('navy', 'Navy', '#1E3A8A'), ('ocean', 'Ocean', '#1D6A8C'), ('plum', 'Plum', '#7A3B8F'),
    ('rose', 'Rose', '#B0306A'), ('graphite', 'Graphite', '#4A5060')]
PURPLE = '#544AC4'
PURPLE_RGB = '84,74,196'


def rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def hexs(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(rgb(a)), lum(rgb(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def is_tint(h):
    """a purple-family color that follows the accent (hue 238 to 262, not grey, not the dark sidebar tiles)"""
    r, g, b = (v / 255 for v in rgb(h))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return 238 <= hh * 360 <= 262 and s > 0.12 and (max(r, g, b) - min(r, g, b)) > 0.03 and l >= 0.30


def mix_of(h):
    """(base, t): h is about base*(1-t) + PURPLE*t, base white for a lighter color and black for a darker one"""
    c, p = rgb(h), rgb(PURPLE)
    if lum(c) >= lum(p):
        base = [255, 255, 255]
    else:
        base = [0, 0, 0]
    num = sum((ci - bi) * (pi - bi) for ci, pi, bi in zip(c, p, base))
    den = sum((pi - bi) ** 2 for pi, bi in zip(p, base))
    t = max(0.0, min(1.0, num / den))
    return base, t


def follow(h, acc):
    base, t = mix_of(h)
    return hexs([b * (1 - t) + a * t for b, a in zip(base, rgb(acc))])


def style_blocks(page):
    head = page[:page.index('</head>')]
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', head, re.S):
        yield m.start(1), m.group(1)


def rules(css):
    """(start, end) of each innermost rule 'selector{declarations}' in a style block (comments skipped)"""
    out, i, n = [], 0, len(css)
    seg = [0]          # where the current statement starts, per nesting level
    open_ = []         # (statement start, has a nested block) per open brace
    while i < n:
        if css.startswith('/*', i):
            j = css.find('*/', i + 2)
            if not css[seg[-1]:i].strip():
                seg[-1] = n if j < 0 else j + 2   # a comment before a selector is not part of the rule
            i = n if j < 0 else j + 2
            continue
        c = css[i]
        if c == '{':
            if open_:
                open_[-1][1] = True
            open_.append([seg[-1], False])
            seg.append(i + 1)
        elif c == '}' and open_:
            st, nested = open_.pop()
            seg.pop()
            if not nested:
                out.append((st, i + 1))
            seg[-1] = i + 1
        elif c == ';' and not open_:
            seg[-1] = i + 1   # a top-level at-rule statement such as @import
        i += 1
    return out


HEX = re.compile(r'#[0-9A-Fa-f]{6}\b')


def subst(rule_text, used):
    sel, _, decls = rule_text.partition('{')

    def hx(m):
        h = m.group(0).upper()
        if h == PURPLE:
            return 'var(--accent)'
        if is_tint(h):
            used.add(h)
            return 'var(--axh-%s)' % h[1:]
        return m.group(0)
    d = re.sub(r'rgba\(\s*84\s*,\s*74\s*,\s*196\s*,', 'rgba(var(--acc-rgb),', decls)
    d = HEX.sub(hx, d)
    d = re.sub(r'(?<![-\w])color\s*:\s*var\(--faint\)', 'color:var(--muted)', d)
    # the original :root holds the token definitions themselves; leave them as they are
    if sel.strip() == ':root':
        return rule_text
    return sel + '{' + d


def build(page):
    used, ops = set(), []
    for off, css in style_blocks(page):
        for a, b in rules(css):
            raw = css[a:b].lstrip()
            a2 = b - len(raw)
            new = subst(raw, used)
            if new == raw:
                continue
            find, w = raw, new
            ga = off + a2
            while page.count(find) != 1:
                if ga <= 0:
                    raise SystemExit('cannot make a unique anchor for: ' + raw[:120])
                ga -= 1
                find, w = page[ga] + find, page[ga] + w
            ops.append({'op': 'replace_global', 'find': find, 'with': w,
                        'note': 's136 accent setting (Jonathan 2026-10-14): accent literals read the accent tokens'})
    return ops, sorted(used)


def tokens_css(used):
    """the accent tokens: :root holds Slate (the default); each other choice redefines them under [data-axa]"""
    lines = []
    for key, name, h in ACCENTS:
        r, g, b = rgb(h)
        decl = ['--accent:%s' % h, '--acc-rgb:%d,%d,%d' % (r, g, b), '--accent-bg:%s' % follow('#E7E7F1', h)]
        decl += ['--axh-%s:%s' % (t[1:], follow(t, h)) for t in used]
        sel = ':root,[data-axa="slate"]' if key == 'slate' else '[data-axa="%s"]' % key
        lines.append(sel + '{' + ';'.join(decl) + '}')
    return '\n'.join(lines)


def test():
    ok = True

    def chk(name, cond):
        nonlocal ok
        print(('ok   ' if cond else 'FAIL ') + name)
        ok &= bool(cond)
    chk('purple maps to itself', all(follow(t, PURPLE).upper() == t or
                                     max(abs(x - y) for x, y in zip(rgb(follow(t, PURPLE)), rgb(t))) <= 12
                                     for t in ['#F2F1FA', '#EDECF7', '#E9E8F4', '#DEDEEB', '#E7E7F1', '#9A93E8']))
    chk('principle indigo untouched', not is_tint('#3A3E70') and not is_tint('#E5E7EF'))
    chk('dark sidebar tiles untouched', not is_tint('#1B1830') and not is_tint('#2C2656'))
    u = set()
    r = subst('.x .y{color:var(--faint);border-left:2px solid rgba(84, 74,196,.28);background:#F2F1FA}', u)
    chk('rule substitution', r == '.x .y{color:var(--muted);border-left:2px solid rgba(var(--acc-rgb),.28);background:var(--axh-F2F1FA)}')
    chk('faint as a background is not text', subst('.z{background:var(--faint)}', set()) == '.z{background:var(--faint)}')
    chk('a property ending in color is not text', 'border-color:var(--faint)' in subst('.z{border-color:var(--faint)}', set()))
    chk(':root left alone', subst(':root{--accent:#544AC4}', set()) == ':root{--accent:#544AC4}')
    css = '/* a {b} */\n.a{color:#544AC4}\n@media (max-width:640px){\n  .b{background:#F2F1FA}\n}\n'
    rs = [css[a:b].strip() for a, b in rules(css)]
    chk('rules inside media, comments skipped', rs == ['.a{color:#544AC4}', '.b{background:#F2F1FA}'])
    page = '<html><head><style>.a{color:#544AC4}\n.c .a{color:#544AC4}</style></head><body></body></html>'
    ops, _ = build(page)
    chk('anchors are unique', all(page.count(o['find']) == 1 for o in ops) and len(ops) == 2)
    for key, name, h in ACCENTS:
        chk('%s passes 4.5:1 on #EFF0F0 and #E6E7E8' % name, contrast(h, '#EFF0F0') >= 4.5 and contrast(h, '#E6E7E8') >= 4.5)
    return 0 if ok else 1


def main(argv):
    if argv[:1] == ['--test']:
        return test()
    page = open(argv[0], encoding='utf-8').read()
    ops, used = build(page)
    json.dump({'edits': ops, 'tokens_css': tokens_css(used)}, open(argv[1], 'w'), indent=1)
    print('%d rules rewritten; %d tints follow the accent' % (len(ops), len(used)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
