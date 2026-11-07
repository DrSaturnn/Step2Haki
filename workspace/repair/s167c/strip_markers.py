"""s167c N13: drop the Board-style and Aquifer marker rules and their tokens from site/css (rule-level, brace-matched)."""
import re, sys, glob
SEL = re.compile(r'#nav a\.bs|#nav a\.aq|\.bsband|\.aqband|\.bsonly|\.navsub\.aq|\.brief\.bs\s*>\s*h4::after|data-src="aquifer"\]\s*>\s*h4::after')
TOK = re.compile(r'--t-[\w-]*(?:bsband|aqband|bsonly|navsub-aq|bs-h4-after)[\w-]*')

def blocks(s):
    """yield (prelude, body, start, end) for each top-level block in s."""
    i = 0
    while True:
        j = s.find('{', i)
        if j < 0: return
        k, d = j, 0
        while True:
            c = s[k]
            if c == '{': d += 1
            elif c == '}':
                d -= 1
                if d == 0: break
            k += 1
        p0 = max(s.rfind('}', 0, j), s.rfind(';', 0, j) if s[:j].rstrip().endswith(';') else -1) + 1
        yield s[i:j], s[j + 1:k], i, k + 1
        i = k + 1

def clean(s, stat):
    out, pos = [], 0
    for pre, body, a, b in blocks(s):
        head = pre.strip()
        if head.startswith('@media') or head.startswith('@layer') or head.startswith('@supports'):
            inner = clean(body, stat)
            if inner.strip():
                out.append(pre + '{' + inner + '}')
            else:
                stat['empty_at'] += 1; out.append(pre[:len(pre) - len(pre.lstrip())] if False else re.match(r'\s*', pre).group(0))
            continue
        if head.startswith('@'):
            out.append(pre + '{' + body + '}'); continue
        sels = [x for x in head.split(',')]
        keep = [x for x in sels if not SEL.search(x)]
        if not keep:
            stat['rules'] += 1; out.append(re.match(r'\s*', pre).group(0)); continue
        if len(keep) != len(sels):
            stat['selectors'] += 1
        decls = [d for d in body.split(';')]
        kd = [d for d in decls if not TOK.match(d.strip())]
        if len(kd) != len(decls): stat['tokens'] += len(decls) - len(kd)
        nb = ';'.join(kd)
        if not nb.strip():
            stat['rules'] += 1; out.append(re.match(r'\s*', pre).group(0)); continue
        out.append(re.match(r'\s*', pre).group(0) + ','.join(keep).strip() + '{' + nb + '}')
    tail = s[s.rfind('}') + 1:] if '}' in s else s
    return ''.join(out) + tail

stat = {'rules': 0, 'selectors': 0, 'tokens': 0, 'empty_at': 0}
for f in sorted(glob.glob('site/css/**/*.css', recursive=True)):
    s = open(f).read()
    n = clean(s, stat)
    n = re.sub(r'\n{2,}', '\n', n)
    if n != s:
        open(f, 'w').write(n); print('changed', f)
print(stat)
left = [f for f in glob.glob('site/css/**/*.css', recursive=True) if SEL.search(open(f).read()) or TOK.search(open(f).read())]
print('left', left)
