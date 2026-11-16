#!/usr/bin/env python3
"""s174 round 1 pairs, third pass: the pairs r1_apply2 left (inline tags or entities inside the old text). The old and
new texts are split into a common prefix, a changed middle and a common suffix; the prefix and suffix match with tags
allowed between characters, and only the middle is replaced, so tags in the prefix and suffix stay."""
import html, json, re, subprocess
WS = '/home/claude/Step2Haki/workspace'
TAG = r'(?:<[^>]+>)*'
def rx(s):
    return TAG.join(re.escape(c) for c in s)
left = [l for l in open(WS + '/local/s174/r1_pairs2.md').read().split('## Left')[1].splitlines() if l.startswith('- ')]
out = []
for l in left:
    m = re.match(r'- (\S+) (\S+): LEFT \{\{(.*)\}\} -> \{\{(.*)\}\}$', l)
    bid, part, old, new = m.groups()
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]: i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]: j += 1
    pre, mid_o, suf, mid_n = old[:i], old[i:len(old) - j], old[len(old) - j:], new[i:len(new) - j]
    fo = subprocess.run(['python3', WS + '/tools/spine/folder_of.py', bid], capture_output=True, text=True).stdout.split()[-1]
    p = '%s/%s/rewrite_s174/rewrite_s174.json' % (WS, fo)
    rw = json.load(open(p)); done = False
    pat = re.compile('(' + rx(pre) + ')(' + rx(mid_o) + ')(' + rx(suf) + ')')
    for e in rw.get('units', []) + rw.get('raw', []):
        s = html.unescape(e.get('new', ''))
        ms = list(pat.finditer(s))
        if len(ms) == 1:
            m2 = ms[0]
            e['new'] = s[:m2.start(2)] + mid_n + s[m2.end(2):]
            done = True; break
    json.dump(rw, open(p, 'w'), ensure_ascii=False, indent=1)
    out.append('%s %s %s: %r -> %r' % ('applied' if done else 'LEFT', bid, part, mid_o, mid_n))
print('\n'.join(out))
