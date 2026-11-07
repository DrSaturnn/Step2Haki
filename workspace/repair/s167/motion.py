#!/usr/bin/env python3
"""motion.py: s167 step 4, every transition and animation timed with a spring token (D-20261105-3; ui_lint
motion_not_spring to 0).

Per transition or animation item in site/css (the prefers-reduced-motion block and `none` values are left alone):
- a timing function with overshoot (cubic-bezier y above 1) or var(--axn-bnc) -> var(--bnc) (bouncy);
- var(--axn-spr) -> var(--spr) (the sidebar copies are the same curves; their definitions are removed when unused);
- the shake keyframes (axrvShake) and items of .2s or less -> var(--snp) (snappy, added to tokens.css);
- every other timed item (ease, ease-in, ease-out, ease-in-out, linear, cubic-bezier, or none named) -> var(--spr);
- a 0s item (a visibility switch) keeps no timing function; when it is the only item it takes var(--spr).
Durations and delays are kept. Writes the files and prints one line per change to local/s167/motion_changes.txt.

  python3 repair/s167/motion.py [--dry]
"""
import glob, math, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = os.path.join(WS, 'site', 'css')
TF = r'(?:ease-in-out|ease-in|ease-out|ease|linear|step-start|step-end|cubic-bezier\([^)]*\)|steps\([^)]*\)|var\(--axn-(?:spr|bnc)\))'
DECL = re.compile(r'(?<![\w-])(transition|animation)(-timing-function)?\s*:\s*([^;}]*)')


def snp_curve():
    """SwiftUI snappy: a spring with bounce 0.15 (damping ratio 0.85), settled to 0.1% at the end of the duration."""
    z = 0.85
    w = 6.9 / z
    wd = w * math.sqrt(1 - z * z)
    pts = []
    for i in range(31):
        t = i / 30
        x = 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z * w / wd * math.sin(wd * t))
        pts.append(x)
    pts[-1] = 1
    return 'linear(' + ','.join(('%.3f' % p).rstrip('0').rstrip('.').replace('0.', '.', 1) if p < 1 else ('%.3f' % p).rstrip('0').rstrip('.') for p in pts) + ')'


def split_items(v):
    out, d, cur = [], 0, ''
    for ch in v:
        d += ch == '('
        d -= ch == ')'
        if ch == ',' and d == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def secs(tok):
    m = re.fullmatch(r'([\d.]+)(m?s)', tok)
    return None if not m else float(m.group(1)) / (1000 if m.group(2) == 'ms' else 1)


def convert_item(item, kind):
    s = item.strip()
    imp = ''
    if s.endswith('!important'):
        s, imp = s[:-10].strip(), '!important'
    if s in ('none', 'unset', 'initial', 'inherit', '') or re.search(r'var\(--(?:spr|bnc|snp)\b', s):
        return item
    tf = re.search(TF, s)
    toks = re.sub(TF, ' ', s).split()
    durs = [secs(t) for t in toks if secs(t) is not None]
    dur = durs[0] if durs else 0.0
    old = tf.group(0) if tf else ''
    bouncy = 'axn-bnc' in old or (old.startswith('cubic-bezier') and any(float(x) > 1 for x in re.findall(r'[\d.]+', old)[1::2]))
    if kind == 'animation' and 'axrvShake' in s:
        new = 'var(--snp)'
    elif bouncy:
        new = 'var(--bnc)'
    elif 'axn-spr' in old:
        new = 'var(--spr)'
    elif dur == 0:
        if not tf:
            return item
        lead = item[:len(item) - len(item.lstrip())]
        return lead + re.sub(r'\s+', ' ', s[:tf.start()] + s[tf.end():]).strip() + imp
    elif dur <= 0.2:
        new = 'var(--snp)'
    else:
        new = 'var(--spr)'
    if tf:
        s = s[:tf.start()] + new + s[tf.end():]
    else:
        # the timing function goes after the first time value (the duration)
        s = re.sub(r'(?<![\w.-])([\d.]+m?s)\b', lambda m: m.group(1) + ' ' + new, s, count=1)
    lead = item[:len(item) - len(item.lstrip())]
    return lead + s + imp


def convert_value(prop, sub, val):
    kind = prop
    if sub:   # transition-timing-function / animation-timing-function
        items = split_items(val)
        return ','.join(re.sub(TF, 'var(--spr)', x) if re.search(TF, x) else x for x in items)
    items = split_items(val)
    new = [convert_item(x, kind) for x in items]
    joined = ','.join(new)
    timed = [x for x in new if x.strip() not in ('none', 'none!important', 'unset', 'initial', 'inherit')]
    if timed and not re.search(r'var\(--(?:spr|bnc|snp)\b', joined):
        # only 0s switches (visibility): the first takes a spring so the declaration is timed by a token
        new[0] = re.sub(r'(?<![\w.-])(0m?s)\b', r'\1 var(--spr)', new[0], count=1)
    return ','.join(new)


def main(a):
    changes, files = [], {}
    for f in sorted(glob.glob(os.path.join(CSS, '**', '*.css'), recursive=True)):
        src = open(f, encoding='utf-8').read()
        out = []
        for ln in src.splitlines(True):
            if 'prefers-reduced-motion' in ln:
                out.append(ln); continue
            def rep(m):
                val = m.group(3)
                new = convert_value(m.group(1), m.group(2), val)
                if new != val:
                    changes.append('%s: %s%s: %s  ->  %s' % (os.path.relpath(f, CSS), m.group(1), m.group(2) or '', val.strip(), new.strip()))
                return m.group(1) + (m.group(2) or '') + ':' + new
            out.append(DECL.sub(rep, ln))
        new = ''.join(out)
        if new != src:
            files[f] = new
    # --axn-spr / --axn-bnc: same curves as --spr / --bnc; the definitions go when nothing reads them
    tf = os.path.join(CSS, 'tokens.css')
    tok = files.get(tf, open(tf, encoding='utf-8').read())
    if '--snp:' not in tok:
        tok = re.sub(r'(--spr:linear\([^)]*\);)', r'\1--snp:' + snp_curve() + ';', tok, count=1)
        files[tf] = tok
        changes.append('tokens.css: --snp added ' + snp_curve())
    allsrc = '\n'.join(files.get(f, open(f, encoding='utf-8').read()) for f in glob.glob(os.path.join(CSS, '**', '*.css'), recursive=True))
    for t in ('axn-spr', 'axn-bnc'):
        if 'var(--%s)' % t not in allsrc:
            for f in glob.glob(os.path.join(CSS, '**', '*.css'), recursive=True):
                s = files.get(f, open(f, encoding='utf-8').read())
                s2 = re.sub(r'--%s:linear\([^)]*\);?' % t, '', s)
                if s2 != s:
                    files[f] = s2; changes.append('%s: --%s definition removed (unused)' % (os.path.relpath(f, CSS), t))
    os.makedirs(os.path.join(WS, 'local', 's167'), exist_ok=True)
    open(os.path.join(WS, 'local', 's167', 'motion_changes.txt'), 'w').write('\n'.join(changes) + '\n')
    print('motion:', len(changes), 'changes in', len(files), 'files')
    if '--dry' not in a:
        for f, s in files.items():
            open(f, 'w', encoding='utf-8').write(s)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
