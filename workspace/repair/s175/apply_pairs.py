#!/usr/bin/env python3
"""Apply reviewer pairs to the rewrite lanes of a batch.
  python3 repair/s175/apply_pairs.py <batch> <pairs file> [--dry]      (run from workspace/)
Pairs file: one pair per line, `PAIR <brief> | OLD: <text> | NEW: <text>` (other lines are ignored; a line starting
with '#' after PAIR lines is a comment). The old text is found in the plain text of exactly one changed unit or raw
change of the brief's rewrite_<batch>.json (or, failing that, one unchanged unit, which then becomes a changed unit).
Only the differing middle is replaced, tags between characters allowed, so markup around it stays. new_claims texts
holding the old text are updated too. Prints applied / LEFT per pair; LEFT pairs are done by hand."""
import html, json, re, subprocess, sys
batch, src = sys.argv[1], sys.argv[2]; dry = '--dry' in sys.argv
TAG = r'(?:<[^>]+>|\s)*'
def rx(s):
    return TAG.join(re.escape(c) for c in s if not c.isspace()) if s.strip() else ''
def folder(b):
    return subprocess.run(['python3', 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip()
def split(old, new):
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]: i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]: j += 1
    while i and not old[i - 1].isspace() and old[i - 1].isalnum() and i < len(old) and old[i:i + 1].isalnum(): i -= 1   # whole words
    return old[:i], old[i:len(old) - j], old[len(old) - j:], new[i:len(new) - j]
def sub(s, old, new):
    """s with old -> new, or None; s is html (entities unescaped by the caller)."""
    pre, mo, suf, mn = split(old, new)
    parts = [p for p in (rx(pre), rx(mo), rx(suf))]
    pat = re.compile('(' + parts[0] + ')' + TAG + '(' + parts[1] + ')' + TAG + '(' + parts[2] + ')')
    ms = list(pat.finditer(s))
    if len(ms) != 1: return None
    m = ms[0]
    if not mo.strip():      # pure insertion: put the new middle right after the prefix
        return s[:m.end(1)] + mn + s[m.end(1):]
    lead = ' ' if (mn[:1] != ' ' and mo[:1] == ' ') else ''
    return s[:m.start(2)] + lead + mn.strip() + (' ' if mo.endswith(' ') or (mn.endswith(' ')) else '') + s[m.end(2):]
out, cache = [], {}
for line in open(src, encoding='utf-8'):
    m = re.match(r'\s*[-*]?\s*`?PAIR (\S+) \| OLD: (.*?) \| NEW: (.*?)`?\s*$', line)
    if not m: continue
    b, old, new = m.group(1), m.group(2).strip(), m.group(3).strip()
    if b not in cache:
        f = folder(b)
        cache[b] = (f, json.load(open('%s/rewrite_%s/rewrite_%s.json' % (f, batch, batch))),
                    {u['uid']: u for u in json.load(open('%s/rewrite_%s/units.json' % (f, batch)))['units']})
    f, rw, base = cache[b]; done = None
    hits = []
    for e in rw.get('units', []) + rw.get('raw', []):
        r = sub(html.unescape(e.get('new', '')), old, new)
        if r is not None: hits.append((e, r))
    if len(hits) == 1:
        hits[0][0]['new'] = hits[0][1]; done = 'applied'
    elif not hits:
        changed = {e['uid'] for e in rw.get('units', [])}
        h2 = [(u, sub(html.unescape(u['html']), old, new)) for k, u in base.items() if k not in changed]
        h2 = [(u, r) for u, r in h2 if r is not None]
        if len(h2) == 1:
            rw['units'].append({'uid': h2[0][0]['uid'], 'new': h2[0][1], 'note': 'review pair (lead)'}); done = 'applied (unit added %s)' % h2[0][0]['uid']
    if done:
        for c in rw.get('new_claims', []):
            if old in c.get('text', ''): c['text'] = c['text'].replace(old, new)
    out.append('%s %s: %s -> %s' % (done or 'LEFT (%d matches)' % len(hits), b, old[:70], new[:70]))
if not dry:
    for b, (f, rw, base) in cache.items():
        json.dump(rw, open('%s/rewrite_%s/rewrite_%s.json' % (f, batch, batch), 'w'), ensure_ascii=False, indent=1)
print('\n'.join(out)); print('pairs %d, applied %d, left %d' % (len(out), sum(o.startswith('applied') for o in out), sum(o.startswith('LEFT') for o in out)))
