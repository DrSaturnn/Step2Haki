#!/usr/bin/env python3
"""r2_apply.py: apply review-receipt old/new pairs to each brief's rewrite_s170.json (s170 chat 5).

  python3 repair/s170/r2_apply.py RECEIPT... [--apply] [--skip brief:part:n,...] [--out local/s170/r2_pairs.md]

Parses '=== <brief> <part>' sections and 'N. old: {{...}}' / 'new: {{...}}' pairs. Each old text must occur exactly
once in the brief's rewrite_s170.json unit 'new' fields (tried raw, then with HTML entities); dry run by default.
"""
import html, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
args = sys.argv[1:]
apply = '--apply' in args
skip = set()
out = ROOT / 'local/s170/r2_pairs.md'
recs = []
i = 0
while i < len(args):
    a = args[i]
    if a == '--apply': pass
    elif a == '--skip': skip = set(args[i + 1].split(',')); i += 1
    elif a == '--out': out = ROOT / args[i + 1]; i += 1
    else: recs.append(Path(a))
    i += 1

pairs = []
for r in recs:
    brief = part = None
    lines = r.read_text().splitlines()
    for j, l in enumerate(lines):
        m = re.match(r'=== (\S+) (\S+)', l)
        if m: brief, part = m.groups(); continue
        m = re.match(r'\s*(\d+)\. old: \{\{(.*)\}\}\s*$', l)
        if m and j + 1 < len(lines):
            n = re.match(r'\s*new: \{\{(.*)\}\}\s*$', lines[j + 1])
            if n: pairs.append(dict(brief=brief, part=part, n=m.group(1), old=m.group(2), new=n.group(1)))


def folder(b):
    return ROOT / subprocess.run([sys.executable, 'tools/spine/folder_of.py', b], cwd=ROOT, capture_output=True,
                                 text=True).stdout.split('\t')[1].strip()


def variants(s):
    v = [s]
    e = html.escape(s, quote=False)
    if e != s: v.append(e)
    named = {'·': '&middot;', '↑': '&uarr;', '↓': '&darr;', '→': '&rarr;', '≥': '&ge;', '≤': '&le;', '–': '&ndash;'}
    t = e
    for k, w in named.items(): t = t.replace(k, w)
    if t not in v: v.append(t)
    return v


docs, report = {}, []
counts = dict(applied=0, skipped=0, missing=0, multiple=0)
for p in pairs:
    key = f"{p['brief']}:{p['part']}:{p['n']}"
    if p['brief'] not in docs:
        f = folder(p['brief']) / 'rewrite_s170' / 'rewrite_s170.json'
        docs[p['brief']] = (f, json.loads(f.read_text()))
    f, d = docs[p['brief']]
    status = ''
    if key in skip:
        status = 'SKIPPED'; counts['skipped'] += 1
    else:
        hits = []
        for u in d['units']:
            for o, nw in zip(variants(p['old']), variants(p['new'])):
                c = u['new'].count(o)
                if c: hits.append((u, o, nw, c)); break
        total = sum(h[3] for h in hits)
        if total == 0:
            status = 'MISSING'; counts['missing'] += 1
        elif total > 1:
            status = f'MULTIPLE {total} ({",".join(h[0]["uid"] for h in hits)})'; counts['multiple'] += 1
        else:
            u, o, nw, _ = hits[0]
            u['new'] = u['new'].replace(o, nw)
            status = f"applied {u['uid']}"; counts['applied'] += 1
    report.append(f"### {key} {status}\nOLD: {p['old']}\nNEW: {p['new']}\n")

out.write_text('\n'.join(report))
if apply:
    for f, d in docs.values():
        f.write_text(json.dumps(d, indent=1, ensure_ascii=False) + '\n')
print(f"r2_apply: {len(pairs)} pairs; " + ', '.join(f'{k} {v}' for k, v in counts.items()) +
      f"; {'written' if apply else 'dry run'}; report {out.relative_to(ROOT)}")
