#!/usr/bin/env python3
"""reps: apply approved receipt replacements to a brief folder's sources, exactly once each (s148 efficiency fix 5;
replaces the s148 scratch reps.py). Sources: build.py, tail_fix.json and head_fix.json, whichever exist.

  python3 tools/spine/reps.py <brief dir> <receipt.md> [--only 1,3] [--dry]
  python3 tools/spine/reps.py <brief dir> <pairs.json> [--dry]          pairs.json: [[old, new], ...]

Each old text must occur exactly once across the sources, in one of its written forms (as is, JSON-escaped, or
Python-escaped). Zero hits or more than one is a miss and changes nothing for that replacement. A miss whose words do
occur in tail_fix.json or head_fix.json with markup between them is reported as "crosses markup" and never forced
(tail text with markup is edited by hand). Prints one line per replacement; exit 1 when any missed. --dry writes nothing.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import condpass as CP  # noqa: E402

SOURCES = ('build.py', 'tail_fix.json', 'head_fix.json')


def forms(t):
    out = [t, json.dumps(t, ensure_ascii=False)[1:-1], t.replace('\\', '\\\\').replace("'", "\\'"),
           t.replace('\\', '\\\\').replace('"', '\\"')]
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def crosses_markup(old, text):
    """the old text's words occur in order with tags between them (so it spans markup)"""
    ws = re.findall(r'\w+', old)
    if len(ws) < 2:
        return False
    pat = r'(?:<[^>]*>|\s|[^\w<])*'.join(re.escape(w) for w in ws)
    m = re.search(pat, text)
    return bool(m and '<' in m.group(0))


def apply(folder, pairs, dry=False):
    """pairs [(label, old, new)]; returns (results [(label, status, detail)], ok)"""
    files = [os.path.join(folder, f) for f in SOURCES if os.path.exists(os.path.join(folder, f))]
    txt = {f: open(f, encoding='utf-8').read() for f in files}
    res, ok = [], True
    for label, old, new in pairs:
        hits = []
        for f in files:
            for fo_old, fo_new in zip(forms(old), forms(new)):
                c = txt[f].count(fo_old)
                if c:
                    hits.append((f, fo_old, fo_new, c))
                    break
        n = sum(h[3] for h in hits)
        if n == 1:
            f, fo_old, fo_new, _ = hits[0]
            txt[f] = txt[f].replace(fo_old, fo_new, 1)
            res.append((label, 'ok', os.path.basename(f)))
            continue
        ok = False
        if n == 0:
            mk = [os.path.basename(f) for f in files if f.endswith('.json') and crosses_markup(old, txt[f])]
            res.append((label, 'crosses markup' if mk else 'not found', ', '.join(mk)))
        else:
            res.append((label, 'ambiguous', '%d hits in %s' % (n, ', '.join(os.path.basename(h[0]) for h in hits))))
    if not dry:
        for f in files:
            if txt[f] != open(f, encoding='utf-8').read():
                open(f, 'w', encoding='utf-8').write(txt[f])
    return res, ok


def load(path, only=None):
    if path.endswith('.json'):
        return [(str(i + 1), o, n) for i, (o, n) in enumerate(json.load(open(path, encoding='utf-8')))]
    _, reps = CP.parse(open(path, encoding='utf-8').read())
    return [(str(n), o, w) for n, o, w in reps if not only or n in only]


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    only = {int(x) for x in argv[argv.index('--only') + 1].split(',')} if '--only' in argv else None
    pairs = load(argv[1], only)
    res, ok = apply(argv[0], pairs, '--dry' in argv)
    for label, st, det in res:
        print('%-3s %-15s %s  %s' % (label, st, det, dict((p[0], p[1]) for p in pairs)[label][:70]))
    print('reps: %d applied, %d missed%s' % (sum(1 for r in res if r[1] == 'ok'), sum(1 for r in res if r[1] != 'ok'),
                                             ' (dry run: nothing written)' if '--dry' in argv else ''))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
