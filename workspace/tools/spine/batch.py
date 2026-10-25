#!/usr/bin/env python3
"""batch: the mechanical S8 and S9 steps of a numbered batch in three commands (s152 close, 2026-10-25; BATCH_RUNBOOK
section 2 S8 and S9). The lead reads the one-line outputs and the facts file; logs go to local/<batch>/.

  python3 tools/spine/batch.py s8 <batch> <brief id> [...] [--no-present]
      changelog entry check; batch page build (local/<batch>/index.html); verify_all three at a time; gate, render,
      preflight, vendor scan, squeeze_check and pointer_check on the batch page; word counts; spend by role and lead
      total; then approval.py present (only when every brief is READY and every check passes). Writes
      local/<batch>/s8_facts.md, the facts the section 5 report needs.
  python3 tools/spine/batch.py ship <batch> "<message>"
      after Jonathan's "ship": ship.sh with AX_SESSION, then pushes HEAD to main by hand when ship.sh had no token
      (fast-forward only). Prints the commit and page sha.
  python3 tools/spine/batch.py post <batch> "<commit message>" <brief id> [...]
      after the lead has written OPEN_WORK, the batch file's S9 section, the DIGEST line and the handoff State: closes
      WAVE.json, records the lead row, syncs the folders, local/<batch>, packets and reviews into the private clone
      (patch.py sync: commits and pushes both repos), then fast-forwards public and private main.
"""
import collections
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
REPO = os.path.dirname(WS)
PRIV = os.environ.get('AX_PRIVATE', '/home/claude/step2haki-private')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WS, 'tools'))


def sh(cmd, cwd=WS, timeout=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)


def py(*a, timeout=None):
    return sh([sys.executable] + list(a), timeout=timeout)


def last(r, n=1, pat=None):
    lines = (r.stdout + r.stderr).strip().splitlines()
    if pat:
        lines = [l for l in lines if re.search(pat, l)]
    return ' | '.join(l.strip() for l in lines[-n:])


def folders(ids):
    r = py(os.path.join(HERE, 'folder_of.py'), *ids)
    out = {}
    for l in r.stdout.splitlines():
        p = l.split('\t')
        if len(p) == 2 and p[1] != 'no folder':
            out[p[0]] = p[1]
    return out


def changelog_has(batch):
    s = open(os.path.join(WS, 'repair', 'changelog', 'axlog.py'), encoding='utf-8').read()
    return "('%s'," % batch[1:] in s


def spend(batch):
    rows = [x for x in csv.DictReader(open(os.path.join(WS, 'repair', 'efficiency', 'ledger_spine.csv'), encoding='utf-8'))
            if x['wave'] == batch]
    by = collections.defaultdict(lambda: [0, 0, 0])
    for x in rows:
        k = '%s %s' % (x['role'], x['model_requested'])
        by[k][0] += 1
        by[k][1] += int(x['calls'] or 0)
        by[k][2] += int(x['tokens'] or 0)
    lead = [x for x in csv.DictReader(open(os.path.join(WS, 'repair', 'efficiency', 'ledger_lead.csv'), encoding='utf-8'))
            if x['wave'] == batch]
    w = json.load(open(os.path.join(WS, 'repair', 'efficiency', 'WAVE.json'), encoding='utf-8'))
    return by, lead, w


def words(page, ids):
    import inventory as I
    import pagelib as P
    pg = P.read_page(page)
    out = {}
    for i in ids:
        b = P.brief_by_id(pg, i)
        if b:
            m = re.search(r'<h4[^>]*>(.*?)</h4>', b.inner, re.S)
            out[i] = (re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else i, I.words_above(b.inner))
    return out


def s8(argv):
    present = '--no-present' not in argv
    a = [x for x in argv if not x.startswith('--')]
    batch, ids = a[0], a[1:]
    L = os.path.join(WS, 'local', batch)
    os.makedirs(L, exist_ok=True)
    facts, ok = [], True
    if not changelog_has(batch):
        print('s8 %s: no changelog entry %s in repair/changelog/axlog.py; write it first' % (batch, batch[1:]))
        return 1
    fd = folders(ids)
    miss = [i for i in ids if i not in fd]
    if miss:
        print('s8 %s: no spine folder for %s' % (batch, ', '.join(miss)))
        return 1
    page = os.path.join(L, 'index.html')
    r = py('repair/build.py', batch, '--out', page)
    facts.append('build: ' + last(r))
    ok &= r.returncode == 0
    ready, notready = [], []
    for i in range(0, len(ids), 3):
        grp = ids[i:i + 3]
        r = py(os.path.join(HERE, 'verify_all.py'), *[fd[x] for x in grp], timeout=3000)
        open(os.path.join(L, 's8_verify_all.log'), 'a', encoding='utf-8').write(r.stdout + r.stderr)
        for l in r.stdout.splitlines():
            if l.startswith('READY '):
                ready.append(l.split()[1])
            elif l.startswith('NOT READY') or l.startswith('NOT-READY'):
                notready.append(l)
        if r.returncode:
            ok = False
    facts.append('verify_all: %d of %d READY%s' % (len(ready), len(ids), '; ' + ' | '.join(notready) if notready else ''))
    ok &= len(ready) == len(ids)
    comma = ','.join(ids)
    checks = [('gate', py('tools/gate.py', page, '--base', 'HEAD'), 'gate:'),
              ('render', sh(['node', 'tools/render.js', page]), 'render:'),
              ('preflight', py('tools/preflight.py', page, '--base', 'HEAD'), '^preflight'),
              ('vendor', py('tools/vendor_scan.py', '--page', page), 'shared'),
              ('squeeze', py(os.path.join(HERE, 'squeeze_check.py'), page, comma, timeout=600), 'squeeze_check'),
              ('pointer', py(os.path.join(HERE, 'pointer_check.py'), page, comma, timeout=600), 'pointer_check')]
    with open(os.path.join(L, 's8_page_checks.log'), 'w', encoding='utf-8') as fh:
        for name, r, pat in checks:
            fh.write('== %s\n%s\n' % (name, r.stdout + r.stderr))
            line = last(r, 2 if name == 'vendor' else 1, pat)
            facts.append('%s: %s' % (name, line))
            if name in ('gate', 'render') and ('PASS' not in line or r.returncode):
                ok = False
            if name in ('squeeze', 'pointer') and r.returncode:
                ok = False
    wc = words(page, ids)
    facts.append('words above the bank (hover text included): ' +
                 '; '.join('%s %d%s' % (i, w, ' (over 1300)' if w > 1300 else '') for i, (t, w) in wc.items()))
    by, lead, w = spend(batch)
    tot = [sum(v[k] for v in by.values()) for k in range(3)]
    facts.append('reviewers: %d agents, %d calls, %.2fM tokens (of %s, %s, %.1fM)' % (
        tot[0], tot[1], tot[2] / 1e6, w.get('max_agents'), w.get('max_calls'), (w.get('max_tokens') or 0) / 1e6))
    for k, v in sorted(by.items()):
        facts.append('  %s: %d agents, %d calls, %.2fM' % (k, v[0], v[1], v[2] / 1e6))
    lt = sum(int(x['tokens']) for x in lead)
    facts.append('lead: %d chat row(s), %.1fM tokens (figure %s)' % (len(lead), lt / 1e6,
                 '%.0fM' % (w['max_lead_tokens'] / 1e6) if w.get('max_lead_tokens') else 'none in WAVE.json'))
    if present and ok:
        r = py('tools/hooks/approval.py', 'present', batch)
        facts.append('present: ' + last(r))
        ok &= r.returncode == 0
    elif present:
        facts.append('present: NOT RUN (a brief is not READY or a check failed)')
    with open(os.path.join(L, 's8_facts.md'), 'w', encoding='utf-8') as fh:
        fh.write('# %s S8 facts (tools/spine/batch.py s8)\n\n' % batch)
        fh.write('\n'.join('- ' + f if not f.startswith('  ') else '  - ' + f.strip() for f in facts) + '\n')
        fh.write('\n## Titles\n' + ''.join('- %s: %s\n' % (i, t) for i, (t, _) in wc.items()))
    for f in facts:
        print(f)
    print('s8 %s: %s; facts in local/%s/s8_facts.md' % (batch, 'OK' if ok else 'STOP', batch))
    return 0 if ok else 1


def ship(argv):
    batch, msg = argv[0], argv[1]
    env = dict(os.environ)
    env.setdefault('AX_SESSION', os.environ.get('AX_SESSION', ''))
    log = os.path.join(WS, 'local', batch, 's9_ship.log')
    os.makedirs(os.path.dirname(log), exist_ok=True)
    r = subprocess.run([os.path.join(WS, 'tools', 'ship.sh'), batch, msg], capture_output=True, text=True, cwd=WS, env=env)
    open(log, 'w', encoding='utf-8').write(r.stdout + r.stderr)
    out = r.stdout + r.stderr
    if r.returncode:
        print('ship %s: ship.sh FAIL (exit %d): %s' % (batch, r.returncode, last(r, 3)))
        return 1
    commit = (re.findall(r'commit: (\w+)', out) or ['?'])[-1]
    page = (re.findall(r'index\.html sha256 (\w+)', out) or ['?'])[-1]
    pushed = 'pushed by ship.sh'
    if 'push skipped' in out:
        sh(['git', 'fetch', '-q', '--depth', '50', 'origin', 'main'], cwd=REPO)
        anc = sh(['git', 'merge-base', '--is-ancestor', 'FETCH_HEAD', 'HEAD'], cwd=REPO).returncode == 0
        if not anc:
            print('ship %s: committed %s but main has moved; merge main and push by hand' % (batch, commit))
            return 1
        p = sh(['git', 'push', '-q', 'origin', 'HEAD:main'], cwd=REPO)
        pushed = 'pushed to main by hand' if p.returncode == 0 else 'PUSH FAILED: ' + p.stderr.strip()[-200:]
    print('ship %s: commit %s, page %s, %s (log local/%s/s9_ship.log)' % (batch, commit, page, pushed, batch))
    return 0


def post(argv):
    batch, msg, ids = argv[0], argv[1], argv[2:]
    p = os.path.join(WS, 'repair', 'efficiency', 'WAVE.json')
    s = open(p, encoding='utf-8').read()
    if json.loads(s).get('id') == batch:
        s2 = re.sub(r'"open":\s*true', '"open": false', s, count=1)
        open(p, 'w', encoding='utf-8').write(s2)
        print('wave %s closed' % batch)
    r = py('tools/hooks/usage_ledger.py', '--lead', '--record', batch)
    print('lead: ' + last(r, 1, 'lead'))
    import patch
    patch.sync(batch, msg, ids)
    for repo, name in ((REPO, 'public'), (PRIV, 'private')):
        br = sh(['git', 'branch', '--show-current'], cwd=repo).stdout.strip()
        sh(['git', 'fetch', '-q', '--depth', '80', 'origin', br], cwd=repo)      # deepen, so ancestry is visible
        sh(['git', 'fetch', '-q', '--depth', '80', 'origin', 'main'], cwd=repo)  # FETCH_HEAD = main
        anc = sh(['git', 'merge-base', '--is-ancestor', 'FETCH_HEAD', 'HEAD'], cwd=repo).returncode == 0
        if anc:
            q = sh(['git', 'push', '-q', 'origin', 'HEAD:main'], cwd=repo)
            head = sh(['git', 'rev-parse', '--short', 'HEAD'], cwd=repo).stdout.strip()
            print('%s main: %s' % (name, head if q.returncode == 0 else 'PUSH FAILED ' + q.stderr.strip()[-150:]))
        else:
            print('%s main: not a fast-forward from %s; merge by hand' % (name, br))
    return 0


def main(argv):
    if not argv or argv[0] not in ('s8', 'ship', 'post'):
        sys.exit(__doc__.strip().splitlines()[3].strip())
    return {'s8': s8, 'ship': ship, 'post': post}[argv[0]](argv[1:])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
