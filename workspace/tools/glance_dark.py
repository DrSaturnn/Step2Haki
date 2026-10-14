"""glance_dark: the s136 dark theme (Jonathan 2026-10-14: "throw in a dark mode as well that mimics apples darker
tinted liquid glass") as CSS, written into the s136 style block by repair/s136/make.py.

  python3 tools/glance_dark.py --test

How it works: every rule in the page's head style blocks that sets a color (color, background, border, shadow,
outline, fill, stroke) is repeated once under [data-theme="dark"], in the same order and the same @media, with its
literal colors mapped to a dark equivalent. Repeating every color rule with the same prefix keeps both which rule
wins (each gains the same specificity) and the order among them, so the dark page follows the light page's cascade.
Tokens (var(--x)) are left as they are and redefined for dark in tokens_css(). The theme attribute sits on the page's
regions and then the root (glance.js), like the accent, so a switch does not restyle every brief in one frame.

Mapping, in HLS: lightness is inverted (light surfaces become dark ones, dark ink becomes light ink); the darkest
results are lifted to a near-black canvas and their saturation softened, so tints read as tinted dark glass. Shadows:
a blurred layer stays a shadow (white highlights fade to a faint sheen, grey shadows become black), a hard ring
inverts. Colors inside url(...) (inline SVG icons) are left alone.
"""
import colorsys
import re
import sys

PROPS = re.compile(r'^(color|background(-color|-image)?|border(-[a-z]+)*|box-shadow|text-shadow|outline(-color)?|fill|stroke|'
                   r'text-decoration(-color)?|caret-color|column-rule(-color)?|-webkit-text-fill-color)$')
SHADOW = ('box-shadow', 'text-shadow')
COLOR = re.compile(r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+\s*(,\s*[\d.]+\s*)?\)|\b(white|black)\b', re.I)
PREFIX = '[data-theme="dark"]'


def parse(c):
    c = c.strip().lower()
    if c == 'white':
        return [255, 255, 255], 1.0
    if c == 'black':
        return [0, 0, 0], 1.0
    if c.startswith('#'):
        h = c[1:]
        if len(h) == 3:
            h = ''.join(x * 2 for x in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)], a
    n = [float(x) for x in re.findall(r'[\d.]+', c)]
    return n[:3], (n[3] if len(n) > 3 else 1.0)


def fmt(rgb, a):
    rgb = [max(0, min(255, round(v))) for v in rgb]
    if a >= 0.999:
        return '#%02X%02X%02X' % tuple(rgb)
    return 'rgba(%d,%d,%d,%s)' % (rgb[0], rgb[1], rgb[2], ('%.3f' % a).rstrip('0').rstrip('.'))


def invert(rgb):
    h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in rgb])
    l2 = 1 - l
    if l2 < 0.30:                      # light surfaces: a near-black canvas, tints kept but softened
        l2 = 0.075 + l2 * 0.75
        s *= 0.55
    elif l2 > 0.90:                    # the darkest ink: bright, not glaring white
        l2 = 0.90 + (l2 - 0.90) * 0.6
    else:                              # mid colors (accents, status colors): lighter so they read on dark
        l2 = min(0.86, l2 + 0.06)
    return [v * 255 for v in colorsys.hls_to_rgb(h, l2, s)]


def lum(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def split_top(s, sep=','):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def map_colors(val):
    return COLOR.sub(lambda m: fmt(invert(parse(m.group(0))[0]), parse(m.group(0))[1]), val)


def map_shadow(val):
    layers = []
    for layer in split_top(val):
        cols = list(COLOR.finditer(layer))
        if not cols:
            layers.append(layer)
            continue
        rest = COLOR.sub(' ', layer)
        lens = re.findall(r'-?[\d.]+(?:px|em|rem)?', rest.replace('inset', ''))
        blur = float(re.sub(r'[a-z]', '', lens[2])) if len(lens) > 2 else 0.0

        def one(m):
            rgb, a = parse(m.group(0))
            if blur > 0:
                if lum(rgb) > 0.6:
                    return fmt([255, 255, 255], round(a * 0.05, 3))     # a highlight becomes a faint sheen
                return fmt([0, 0, 0], min(0.7, round(a * 1.5, 3)))       # a shadow stays a shadow
            if lum(rgb) > 0.6:
                return fmt([255, 255, 255], round(a * 0.09, 3))         # a hard light edge: a thin glass edge
            return fmt(invert(rgb), a)
        layers.append(COLOR.sub(one, layer))
    return ','.join(layers)


def map_decl(prop, val):
    if 'url(' in val:                       # inline SVG icons: keep their colors, swap only the rest
        parts = re.split(r'(url\([^)]*\))', val)
        return ''.join(p if p.startswith('url(') else map_decl(prop, p) for p in parts)
    return map_shadow(val) if prop in SHADOW else map_colors(val)


def blocks(css):
    """(context preludes, selector, body) for each innermost rule; @keyframes and @font-face are skipped"""
    out, i, n, stack, seg = [], 0, len(css), [], 0
    while i < n:
        if css.startswith('/*', i):
            j = css.find('*/', i + 2)
            if not css[seg:i].strip():
                seg = n if j < 0 else j + 2
            i = n if j < 0 else j + 2
            continue
        c = css[i]
        if c == '{':
            stack.append([css[seg:i].strip(), i + 1, False])
            if len(stack) > 1:
                stack[-2][2] = True
            seg = i + 1
        elif c == '}' and stack:
            pre, st, nested = stack.pop()
            if not nested and not any(p.startswith(('@keyframes', '@-webkit-keyframes', '@font-face')) for p, _, _ in stack) \
                    and not pre.startswith('@'):
                out.append(([p for p, _, _ in stack], pre, css[st:i]))
            seg = i + 1
        elif c == ';' and not stack:
            seg = i + 1
        i += 1
    return out


def prefix(sel):
    out = []
    for s in split_top(sel):
        s = s.strip()
        if not s:
            continue
        m = re.match(r'^(html|:root)(?![-\w])', s)
        if m:
            out.append(m.group(1) + PREFIX + s[m.end():])
        else:
            out.append(PREFIX + ' ' + s)
    return ','.join(out)


def dark_css(css):
    lines, last = [], None
    for ctx, sel, body in blocks(css):
        if sel.strip() == ':root' or sel.startswith('@'):
            continue
        decls = []
        for d in split_top(body, ';'):
            if ':' not in d:
                continue
            p, _, v = d.partition(':')
            p = p.strip().lower()
            if p.startswith('--') or not PROPS.match(p):
                continue
            v = v.strip()
            nv = map_decl(p, v)
            if p == 'background' and 'url(' not in v:
                # repeat only the color part, so the shorthand does not reset an image, repeat or size set elsewhere
                bare = re.sub(r'\s*!important\s*$', '', v)
                imp = ' !important' if bare != v else ''
                if COLOR.fullmatch(bare.strip()):
                    p, nv = 'background-color', map_decl(p, bare.strip()) + imp
                elif re.fullmatch(r'\s*((repeating-)?(linear|radial|conic)-gradient\(.*\)\s*,?\s*)+', bare, re.S):
                    p, nv = 'background-image', map_decl(p, bare) + imp
            decls.append('%s:%s' % (p, nv))
        if not decls:
            continue
        rule = prefix(sel) + '{' + ';'.join(decls) + '}'
        for pre in reversed(ctx):
            rule = pre + '{' + rule + '}'
        lines.append(rule)
    return '\n'.join(lines)


def test():
    ok = True

    def chk(name, cond):
        nonlocal ok
        print(('ok   ' if cond else 'FAIL ') + name)
        ok &= bool(cond)
    canvas = invert([239, 240, 240])
    chk('canvas becomes near black', lum(canvas) < 0.02)
    chk('ink becomes light', lum(invert([21, 21, 27])) > 0.7)
    muted = invert([94, 94, 107])
    chk('muted grey reads on the dark canvas (4.5:1)', (lum(muted) + 0.05) / (lum(canvas) + 0.05) >= 4.5)
    green = invert([42, 98, 87])
    chk('confirm green reads on the dark canvas', (lum(green) + 0.05) / (lum(canvas) + 0.05) >= 4.5)
    chk('blurred white highlight fades', map_shadow('-3px -3px 6px rgba(255,255,255,.94)') == '-3px -3px 6px rgba(255,255,255,0.047)')
    chk('blurred grey shadow turns black', 'rgba(0,0,0,' in map_shadow('3px 3px 7px rgba(146,154,157,.27)'))
    chk('hard light edge becomes a thin glass edge', map_shadow('inset 0 1px 0 #FFFFFF') == 'inset 0 1px 0 rgba(255,255,255,0.09)')
    chk('url icons untouched', "stroke='%23ffffff'" in map_decl('background-image', "url(\"data:image/svg+xml,%3Csvg stroke='%23ffffff'/%3E\")"))
    chk('vars untouched', map_decl('color', 'var(--ink)') == 'var(--ink)')
    css = '/* x {y} */\n.a,.b:not(.c,.d){color:#15151B;padding:2px}\n@media (max-width:640px){html .e{background:#fff}}\n@keyframes k{from{color:#fff}}\n:root{--x:#fff}\n.f{margin:0}'
    chk('background shorthand: color only', 'background-color:' in dark_css('.g{background:#fff}') and 'background-image:linear' in dark_css('.g{background:linear-gradient(#fff,#eee)}'))
    out = dark_css(css)
    chk('prefix, media, keyframes and tokens', out.splitlines()[0].startswith('[data-theme="dark"] .a,[data-theme="dark"] .b:not(.c,.d){color:')
        and 'padding' not in out and '@media (max-width:640px){html[data-theme="dark"] .e{background-color:' in out
        and '@keyframes' not in out and '--x' not in out and '.f' not in out)
    return 0 if ok else 1


if __name__ == '__main__':
    if sys.argv[1:2] == ['--test']:
        sys.exit(test())
    sys.exit(__doc__.strip().splitlines()[2].strip())
