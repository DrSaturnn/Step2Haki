#!/usr/bin/env python3
"""vendor_scan.py: find vendor (source) text outside the local-only sources.

  python3 tools/vendor_scan.py [--repo DIR] [--sources DIR] [--stock DIR] [--history] [--min N] [--show PATH] [--json]

Builds 10-word shingles (tags stripped, entities decoded, lowercase [a-z0-9] words) from every
file under the sources dir on disk (default <repo>/repair/sources, including aq/) plus, with
--history, every blob ever committed under a local-only path of tools/local_only.txt. Then scans
every tracked file (default) or every blob in all history (--history), skipping local-only paths,
and prints per path: shared shingles, share of the path's shingles, and the source file that
contributes most. Paths with >= --min shared shingles (default 1) are listed; index.html is
reported separately with its count. --show PATH prints the shared passages for one path.
"""
import fnmatch
import html as H
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

K = 10


def words(txt):
    t = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', txt, flags=re.S | re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = H.unescape(t).lower()
    return re.findall(r'[a-z0-9]+', t)


def shingles(ws):
    return {' '.join(ws[i:i + K]) for i in range(len(ws) - K + 1)}


STOCK_DEFAULT = '/root/.claude/skills/synced'


def is_vendor(rel):
    b = os.path.basename(rel)
    return bool(re.match(r'^s\d+[a-z]?_questions\.md$', b)) or '/aq/' in '/' + rel.replace(os.sep, '/')


def git(repo, *a, inp=None):
    return subprocess.run(['git', '-C', repo] + list(a), input=inp, capture_output=True, check=True).stdout


def local_only(repo):
    p = os.path.join(repo, 'tools', 'local_only.txt')
    out = ['repair/sources/']
    if os.path.exists(p):
        for l in open(p, encoding='utf-8'):
            l = l.split('#', 1)[0].strip()
            if l and l not in out:
                out.append(l)
    return out


def is_local(path, lo):
    for x in lo:
        if any(c in x for c in '*?['):
            if fnmatch.fnmatch(path, x):
                return True
        elif path == x.rstrip('/') or path.startswith(x if x.endswith('/') else x + '/'):
            return True
    return False


def blobs(repo, history):
    """[(sha, path)] for all blobs at HEAD or in all history."""
    if history:
        raw = git(repo, 'rev-list', '--all', '--objects').decode()
        cand = [l.split(' ', 1) for l in raw.splitlines() if ' ' in l]
        shas = '\n'.join(c[0] for c in cand).encode()
        types = git(repo, 'cat-file', '--batch-check=%(objectname) %(objecttype)', inp=shas).decode().split('\n')
        typ = dict(t.split() for t in types if t)
        # a blob can live at several paths; collect every path per blob
        paths = defaultdict(set)
        for c in cand:
            if typ.get(c[0]) == 'blob':
                paths[c[0]].add(c[1])
        # rev-list names a blob by one path only; add all paths from every commit's tree
        for line in git(repo, 'log', '--all', '--format=', '--raw', '--no-abbrev', '--no-renames', '-m').decode().splitlines():
            m = re.match(r'^:\d+ \d+ [0-9a-f]+ ([0-9a-f]+) \w+\t(.+)$', line)
            if m and m.group(1) != '0' * 40:
                paths[m.group(1)].add(m.group(2))
        return [(s, p) for s, ps in paths.items() for p in ps]
    raw = git(repo, 'ls-files', '-s').decode()
    return [(l.split()[1], l.split('\t', 1)[1]) for l in raw.splitlines()]


def read_blobs(repo, shas):
    out = {}
    if not shas:
        return out
    data = git(repo, 'cat-file', '--batch', inp='\n'.join(shas).encode())
    i = 0
    while i < len(data):
        nl = data.index(b'\n', i)
        sha, _, size = data[i:nl].decode().split()
        size = int(size)
        out[sha] = data[nl + 1:nl + 1 + size].decode('utf-8', 'replace')
        i = nl + 1 + size + 1
    return out


def main(argv):
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
    repo = os.path.abspath(opt('--repo', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    history = '--history' in argv
    src_dir = opt('--sources', os.path.join(repo, 'repair', 'sources'))
    mn = int(opt('--min', '1'))
    # the workspace may be a subfolder of the git repo (Step2Haki/workspace): git paths are
    # root-relative, local-only patterns are workspace-relative, so prefix them
    top = git(repo, 'rev-parse', '--show-toplevel').decode().strip()
    pre = os.path.relpath(repo, top)
    lo = [x if pre == '.' else pre + '/' + x for x in local_only(repo)]
    repo = top
    # source shingles -> contributing source file. Vendor sources are question files (sNN_questions.md)
    # and Aquifer case text (aq/); other files under sources (skill copy, audits, inventories) are
    # local-only but not vendor text. Stock phrases are subtracted: shingles found in skill text
    # (the skill copy under sources, or --stock DIR) and shingles shared by >= 3 vendor files
    # (NBME lead-ins and other boilerplate).
    src = defaultdict(set)
    stock = set()
    if os.path.isdir(src_dir):
        for root, _, fs in os.walk(src_dir):
            for f in fs:
                p = os.path.join(root, f)
                rel = os.path.relpath(p, src_dir)
                sh = shingles(words(open(p, encoding='utf-8', errors='replace').read()))
                if is_vendor(rel):
                    for s in sh:
                        src[s].add(rel)
                elif 'skill' in f.lower():
                    stock |= sh
    for d in [opt('--stock', STOCK_DEFAULT)]:
        if d and os.path.isdir(d):
            for root, _, fs in os.walk(d):
                for f in fs:
                    if f.endswith('.md'):
                        stock |= shingles(words(open(os.path.join(root, f), encoding='utf-8', errors='replace').read()))
    bl = blobs(repo, history)
    if history:
        # sources as committed in history also count as source text
        srcblobs = read_blobs(repo, sorted({s for s, p in bl if is_local(p, lo)}))
        for s, p in bl:
            if s in srcblobs and is_local(p, lo) and is_vendor(p):
                for sh in shingles(words(srcblobs[s])):
                    src[sh].add(p)
    common = {h for h, fs in src.items() if len({os.path.basename(f) for f in fs}) >= 3}
    for h in stock | common:
        src.pop(h, None)
    scan = [(s, p) for s, p in bl if not is_local(p, lo)]
    texts = read_blobs(repo, sorted({s for s, _ in scan}))
    res = {}
    for s, p in scan:
        t = texts.get(s, '')
        if '\x00' in t[:2000]:
            continue
        sh = shingles(words(t))
        hit = sh & src.keys()
        key = p
        prev = res.get(key)
        if prev is None or len(hit) > prev['shared']:
            top = Counter(f for h in hit for f in src[h]).most_common(1)
            res[key] = {'shared': len(hit), 'of': len(sh), 'blob': s, 'top': top[0][0] if top else '', 'hits': hit}
    if opt('--show'):
        r = res.get(opt('--show'))
        if not r:
            print('no such path in scan')
            return 1
        # merge consecutive shingles into passages
        t = words(texts[r['blob']])
        spans = []
        for i in range(len(t) - K + 1):
            if ' '.join(t[i:i + K]) in r['hits']:
                if spans and i <= spans[-1][1]:
                    spans[-1][1] = i + K
                else:
                    spans.append([i, i + K])
        for a, b in spans[:40]:
            print('  [%d words] %s' % (b - a, ' '.join(t[a:b])[:300]))
        return 0
    flagged = {p: r for p, r in res.items() if r['shared'] >= mn and os.path.basename(p) != 'index.html'}
    idx = {p: r for p, r in res.items() if os.path.basename(p) == 'index.html'}
    if '--json' in argv:
        print(json.dumps({p: {k: v for k, v in r.items() if k != 'hits'} for p, r in list(flagged.items()) + list(idx.items())}, indent=1))
        return 0
    print('vendor_scan: %s | %d source shingles | %d paths scanned | %d flagged (>= %d shared) | local-only: %s'
          % ('all history' if history else 'tracked files', len(src), len(res), len(flagged), mn, ' '.join(lo)))
    for p, r in sorted(flagged.items(), key=lambda x: -x[1]['shared']):
        print('  %6d shared (%5.1f%% of %d)  %-50s top source: %s' % (r['shared'], 100.0 * r['shared'] / max(1, r['of']), r['of'], p, r['top']))
    for p, r in idx.items():
        print('  index.html (%s): %d shared of %d (%.3f%%)' % (p, r['shared'], r['of'], 100.0 * r['shared'] / max(1, r['of'])))
    return 1 if flagged else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
