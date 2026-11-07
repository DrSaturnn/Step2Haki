#!/usr/bin/env python3
"""rawcolor.py: s167 step 2, the raw-color pass (ui_lint component_raw_color to 0).

Every literal color in a site/css/components/*.css declaration becomes a palette token defined once in
site/css/tokens.css (`:root{--p-...}`), named by its value: hex `#FBFBFB` -> `--p-FBFBFB`, `white` -> `--p-white`,
`rgba(24,28,30,.05)` -> `--p-181C1E-a05`. A token holds the literal as written, so every computed value is unchanged.
`rgba(var(--x),.12)` (a token color with an alpha) is left as it is: ui_lint treats it as a token color.
Custom-property declarations, content, font-family and quotes are skipped, as in ui_lint.

  python3 repair/s167/rawcolor.py [--dry]
"""
import glob, os, re, sys

SITE = os.path.join(os.path.dirname(__file__), '..', '..', 'site', 'css')
RAW = re.compile(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\((?!\s*var\()[^()]*\)|\b(?:white|black)\b', re.I)
NAMED = {'white': 'white', 'black': 'black'}


def name(v):
    s = v.strip()
    low = s.lower()
    if low in NAMED:
        return 'p-' + low
    if s.startswith('#'):
        h = s[1:].upper()
        if len(h) in (3, 4):
            h = ''.join(c * 2 for c in h)
        return 'p-' + h
    m = re.match(r'(rgba?|hsla?)\(\s*([\d.]+)%?\s*[, ]\s*([\d.]+)%?\s*[, ]\s*([\d.]+)%?\s*(?:[,/]\s*([\d.]+%?))?\s*\)', s, re.I)
    if not m:
        raise SystemExit('rawcolor: cannot name ' + s)
    fn, a, b, c, al = m.groups()
    if fn.lower().startswith('rgb'):
        base = '%02X%02X%02X' % (round(float(a)), round(float(b)), round(float(c)))
    else:
        base = 'h%s-%s-%s' % (a.replace('.', '_'), b.replace('.', '_'), c.replace('.', '_'))
    if al is None:
        return 'p-' + base
    al = al.strip()
    if al.endswith('%'):
        al = '%g' % (float(al[:-1]) / 100)
    frac = ('%g' % float(al))
    frac = frac[2:] if frac.startswith('0.') else frac.replace('.', '_')
    return 'p-' + base + '-a' + frac


def split_decls(body):
    out, depth, cur = [], 0, ''
    for ch in body:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ';' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def convert_value(val, tokens):
    urls = []
    def keep(m):
        urls.append(m.group(0)); return '\x00%d\x00' % (len(urls) - 1)
    val = re.sub(r'url\([^)]*\)', keep, val)
    def rep(m):
        lit = m.group(0)
        t = name(lit)
        prev = tokens.get(t)
        if prev and prev.replace(' ', '').lower() != lit.replace(' ', '').lower():
            t = t + '-' + str(len([k for k in tokens if k.startswith(t)]) + 1)
        tokens.setdefault(t, lit)
        return 'var(--%s)' % t
    out = RAW.sub(rep, val)
    return re.sub(r'\x00(\d+)\x00', lambda m: urls[int(m.group(1))], out)


def convert_rule_line(line, tokens):
    # one rule per line: "selector{decls}" or an at-rule opener / closer
    m = re.match(r'^([^{}]*)\{(.*)\}\s*$', line)
    if not m or m.group(1).lstrip().startswith('@'):
        return line, 0
    sel, body = m.groups()
    n = 0
    decls = split_decls(body)
    for i, d in enumerate(decls):
        if ':' not in d:
            continue
        prop, val = d.split(':', 1)
        p = prop.strip().lower()
        if p.startswith('--') or p in ('content', 'font-family', 'quotes'):
            continue
        new = convert_value(val, tokens)
        if new != val:
            n += len(RAW.findall(val)); decls[i] = prop + ':' + new
    return sel + '{' + ';'.join(decls) + '}' + ('\n' if line.endswith('\n') else ''), n


def main(a):
    tokens, total, per = {}, 0, {}
    files = sorted(glob.glob(os.path.join(SITE, 'components', '*.css')))
    outs = {}
    for f in files:
        lines = open(f, encoding='utf-8').read().splitlines(True)
        new, n = [], 0
        for ln in lines:
            x, k = convert_rule_line(ln, tokens)
            new.append(x); n += k
        outs[f] = ''.join(new); per[os.path.basename(f)] = n; total += n
    print('rawcolor:', total, 'literals,', len(tokens), 'palette tokens', per)
    if '--dry' in a:
        for k, v in sorted(tokens.items()):
            print(' ', k, v)
        return 0
    for f, s in outs.items():
        open(f, 'w', encoding='utf-8').write(s)
    tf = os.path.join(SITE, 'tokens.css')
    t = open(tf, encoding='utf-8').read()
    block = ':root{' + ';'.join('--%s:%s' % (k, v) for k, v in sorted(tokens.items())) + '}\n'
    t = re.sub(r'(?m)^:root\{--p-[^\n]*\n', '', t)
    open(tf, 'w', encoding='utf-8').write(t.rstrip('\n') + '\n' + block)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
