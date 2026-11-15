#!/usr/bin/env python3
"""Apply review fixes to the rewrite lanes of a batch.

  python3 tools/spine/apply_pairs.py <batch> <pairs file> [--dry]       a file of PAIR lines
  python3 tools/spine/apply_pairs.py <batch> --round N [--dry]          every fix in the round's receipts
  python3 tools/spine/apply_pairs.py <batch> --round N --print          list the round's fixes as PAIR lines, apply none

A fix is `PAIR <brief> | OLD: <text> | NEW: <text>` anywhere in a line (several in one line are split apart; a finding
number or label before them is ignored), or, in a receipt, an `old: {{...}}` / `new: {{...}}` pair under
"Replacements:" (the brief is the receipt section's). Duplicates count once. The old text is found in the plain text of
exactly one changed unit or raw change of the brief's rewrite_<batch>.json (or, failing that, one unchanged unit, which
then becomes a changed unit). Only the differing middle is replaced, tags between characters allowed, so markup around
it stays; HTML entities in the field (&rarr;, &middot;, &nbsp;) are kept as entities. new_claims texts holding the old
text are updated too. Prints applied / LEFT per fix; LEFT fixes are done by hand. Run from workspace/."""
import glob, html, json, os, re, subprocess, sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
KEEP = {'amp', 'lt', 'gt', 'quot', 'apos', '#38', '#60', '#62', '#34', '#39', '#x26', '#x3c', '#x3e', '#x22', '#x27'}
ENT = re.compile(r'&(#x?[0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);')
PAIR = re.compile(r'PAIR (\S+) \| OLD: (.*?) \| NEW: (.*?)(?=\.? PAIR \S+ \| OLD: |\s*$)')
REPL = re.compile(r'old: \{\{(.*?)\}\}\s*\n\s*new: \{\{(.*?)\}\}', re.S)


def decode(s):
    """s with entities other than the markup-safe ones (amp, lt, gt, quotes) turned into characters, and the map of each
    such character back to its entity when the character never occurs literally in s"""
    back, lit = {}, ENT.sub('', s)

    def one(m):
        if m.group(1).lower() in KEEP:
            return m.group(0)
        ch = html.unescape(m.group(0))
        if ch == m.group(0):
            return ch
        if ch not in lit:
            back.setdefault(ch, m.group(0))
        return ch
    return ENT.sub(one, s), back


def encode(s, back):
    """characters back to the entities the field held them as; only outside tags"""
    if not back:
        return s
    parts = re.split(r'(<[^>]+>)', s)
    return ''.join(p if p.startswith('<') else ''.join(back.get(c, c) for c in p) for p in parts)


def clean(t):
    return t.strip().strip('`').strip()


def from_text(text, brief=None):
    """[(brief, old, new)] from PAIR lines anywhere in text, then from Replacements blocks when brief is given"""
    out = []
    for ln in text.split('\n'):
        for m in PAIR.finditer(ln):
            out.append((m.group(1), clean(m.group(2)), clean(m.group(3))))
    if brief:
        out += [(brief, o.strip(), n.strip()) for o, n in REPL.findall(text)]
    return out


def from_round(batch, rnd):
    out = []
    for r in sorted(glob.glob(os.path.join(WS, 'repair/efficiency/lanes/%s/r%s/lane_*/receipt.md' % (batch, rnd)))):
        for sec in re.split(r'\n(?==== )', open(r, encoding='utf-8').read()):
            m = re.match(r'=== (\S+) (?:acc|read|flags|display)', sec)
            out += from_text(sec, m.group(1) if m else None)
    return out


def dedupe(pairs):
    seen, out = set(), []
    for b, o, n in pairs:
        if (b, o) not in seen and o != n:
            seen.add((b, o))
            out.append((b, o, n))
    return out


def folder(b):
    return subprocess.run([sys.executable, os.path.join(WS, 'tools/spine/folder_of.py'), b], capture_output=True,
                          text=True, cwd=WS).stdout.split('\t')[1].strip()


TAG = r'(?:<[^>]+>|\s)*'
def rx(s):
    return TAG.join(re.escape(c) for c in s if not c.isspace()) if s.strip() else ''
def split(old, new):
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]: i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]: j += 1
    while i and not old[i - 1].isspace() and old[i - 1].isalnum() and i < len(old) and old[i:i + 1].isalnum(): i -= 1   # whole words
    return old[:i], old[i:len(old) - j], old[len(old) - j:], new[i:len(new) - j]
def _ws(g, want, closing_side):
    """gap g (tags and whitespace only) with exactly one space when want, none otherwise; tags kept."""
    bare = re.sub(r'(<[^>]+>)|\s+', lambda x: x.group(1) or '', g)
    if not want: return bare
    if bare != g: return re.sub(r'(<[^>]+>)|\s+', lambda x: x.group(1) or ' ', g)
    return bare + ' ' if (closing_side or bare.startswith('</')) else ' ' + bare
def sub(s, old, new):
    """s with old -> new, or None (LEFT); s is html (entities unescaped by the caller). The space at each edge of the
    replaced middle follows the new text; a middle whose html holds a tag is LEFT, since replacing it would drop the tag."""
    pre, mo, suf, mn = split(old, new)
    parts = [p for p in (rx(pre), rx(mo), rx(suf))]
    pat = re.compile('(' + parts[0] + ')(' + TAG + ')(' + parts[1] + ')(' + TAG + ')(' + parts[2] + ')')
    ms = list(pat.finditer(s))
    if len(ms) != 1: return None
    m = ms[0]
    if re.search(r'<[^>]+>', m.group(3)): return None
    lw = (pre[-1:].isspace() or mn[:1].isspace()) if pre else None
    rw = (mn[-1:].isspace() or suf[:1].isspace()) if suf else None
    if not mo.strip():      # pure insertion: one gap
        g = m.group(2) + m.group(4)
        tags = re.sub(r'(<[^>]+>)|\s+', lambda x: x.group(1) or '', g)
        body = (' ' if lw else '') + mn.strip() + (' ' if rw else '') if mn.strip() else (' ' if (lw or rw) else '')
        return s[:m.end(1)] + (body + tags if tags.startswith('<') and not tags.startswith('</') else tags + body) + s[m.start(5):]
    L = m.group(2) if lw is None else _ws(m.group(2), lw, True)
    R = m.group(4) if rw is None else _ws(m.group(4), rw, False)
    return s[:m.start(2)] + L + mn.strip() + R + s[m.end(4):]

def apply(batch, pairs, dry=False, fold=folder):
    out, cache = [], {}
    for b, old, new in pairs:
        if b not in cache:
            f = fold(b)
            if not os.path.isabs(f):
                f = os.path.join(WS, f)
            cache[b] = (f, json.load(open('%s/rewrite_%s/rewrite_%s.json' % (f, batch, batch), encoding='utf-8')),
                        {u['uid']: u for u in json.load(open('%s/rewrite_%s/units.json' % (f, batch), encoding='utf-8'))['units']})
        f, rw, base = cache[b]
        done, hits = None, []
        for e in rw.get('units', []) + rw.get('raw', []):
            d, back = decode(e.get('new', ''))
            r = sub(d, old, new)
            if r is not None:
                hits.append((e, encode(r, back)))
        if len(hits) == 1:
            hits[0][0]['new'] = hits[0][1]
            done = 'applied'
        elif not hits:
            changed = {e['uid'] for e in rw.get('units', [])}
            h2 = []
            for k, u in base.items():
                if k in changed:
                    continue
                d, back = decode(u['html'])
                r = sub(d, old, new)
                if r is not None:
                    h2.append((u, encode(r, back)))
            if len(h2) == 1:
                rw['units'].append({'uid': h2[0][0]['uid'], 'new': h2[0][1], 'note': 'review pair (lead)'})
                done = 'applied (unit added %s)' % h2[0][0]['uid']
        if done:
            for c in rw.get('new_claims', []):
                if old in c.get('text', ''):
                    c['text'] = c['text'].replace(old, new)
        out.append('%s %s: %s -> %s' % (done or 'LEFT (%d matches)' % len(hits), b, old[:70], new[:70]))
    if not dry:
        for b, (f, rw, base) in cache.items():
            json.dump(rw, open('%s/rewrite_%s/rewrite_%s.json' % (f, batch, batch), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
    return out


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    batch = a[0]
    pairs = from_round(batch, a[a.index('--round') + 1]) if '--round' in a else from_text(open(a[1], encoding='utf-8').read())
    pairs = dedupe(pairs)
    if '--print' in a:
        print('\n'.join('PAIR %s | OLD: %s | NEW: %s' % p for p in pairs))
        return 0
    out = apply(batch, pairs, '--dry' in a)
    print('\n'.join(out))
    print('pairs %d, applied %d, left %d' % (len(out), sum(o.startswith('applied') for o in out),
                                             sum(o.startswith('LEFT') for o in out)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
