#!/usr/bin/env python3
"""ui_gate.py: the standing UI tests run before a ship (UI_REFACTOR_PLAN 6b).

  python3 tools/ui_gate.py PAGE BASE [--allow ALLOW.json] [--views desk,phone] [--skip parity,theme,a11y,perf,twopane]
                                     [--fresh]

PAGE is the candidate build, BASE the live page (../discriminator-briefs-site/index.html). Four tests, in order, one
browser job at a time:
  parity  tools/ui_check.js css BASE PAGE, then run on desk and phone in every setting (300 elements a check): every
          computed-style difference between the live page and the candidate fails unless ALLOW.json lists it (the batch's
          intended changes: {sel, prop, setting}; each one is named in the batch report). Verdict line UI-CHECK SAME.
          The result is kept in local/ui_gate/parity.json. An intended change that moves boxes below it is better carried
          by BASE: a page built from the live commit plus that change only (ship.sh: UI_GATE_BASE), named in the report.
  theme   tools/theme_gate.js PAGE: themes move no box and leave no light color in dark or tinted.
  a11y    tools/a11y_scan.js PAGE --baseline tools/spine/a11y_baseline.json: no serious or critical axe count above the
          baseline in any view and setting.
  perf    tools/perf_budget.py PAGE: size and elements at load not above the baseline, load times within 15%.
  twopane tools/two_pane_check.js PAGE: every brief keeps its text in the Two-pane layout and after returning to
          Scrolling (about 4 minutes).
Exit 1 when any test fails; every test runs and prints its verdict line.

Faster runs (s169, D-20261107-14; measured on the live page in a two-core container, 18.6 min before):
- a passed test is recorded in local/ui_gate/passed.json under a key made from the page (its change log block and build
  stamp emptied, as perf_budget measures size), BASE, ALLOW, the views and the test's own tool and baseline files; the
  same test on the same key is not run again and prints "PASS (recorded ...)". So ship.sh's run on the approved
  candidate takes seconds when the candidate already passed. --fresh runs every test.
- parity loads no page when no style rule differs between BASE and PAGE (zero checks measure nothing; was 296 s);
  otherwise both pages of a view load at the same time (ui_check.js).
- a11y: two pages per view, each loading once and taking every other setting (543 s to about 320 s).
- twopane: two pages at once (212 s to about 103 s).
"""
import hashlib, json, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)


def run(name, cmd, ok_word):
    t = time.time()
    env = dict(os.environ, NODE_OPTIONS='--max-old-space-size=4096')
    r = subprocess.run(cmd, cwd=WS, capture_output=True, text=True, env=env)
    out = (r.stdout or '') + (r.stderr or '')
    lines = [l for l in out.splitlines() if l.strip()]
    verdict = next((l for l in reversed(lines) if ok_word in l or 'WORSE' in l or 'DIFFER' in l or 'FAIL' in l), lines[-1] if lines else '')
    ok = r.returncode == 0 and ok_word in out
    print('%-6s %s %s (%d s)' % (name, 'PASS' if ok else 'FAIL', verdict.strip()[:300], time.time() - t))
    if not ok:
        print('\n'.join('       ' + l for l in lines[-25:]))
    return ok


TOOLS = {'parity': ['tools/ui_check.js'], 'theme': ['tools/theme_gate.js'],
         'a11y': ['tools/a11y_scan.js', 'tools/spine/a11y_baseline.json'],
         'perf': ['tools/perf_budget.py', 'tools/perf_load.js', 'tools/spine/perf_baseline.json'],
         'twopane': ['tools/two_pane_check.js', 'tools/serve_page.js']}
RECORD = os.path.join(WS, 'local', 'ui_gate', 'passed.json')


def digest(path, page=False):
    if not path or not os.path.exists(path):
        return '-'
    b = open(path, 'rb').read()
    if page:
        b = re.sub(rb'(<script type="application/json" id="axlog">).*?(</script>)', rb'\1\2', b, count=1, flags=re.S)
        b = re.sub(rb'(<meta name="ax-build" content=")[^"]*(">)', rb'\1\2', b, count=1)
    return hashlib.sha256(b).hexdigest()[:16]


def key(test, page, base, allow, views):
    parts = [test, digest(page, True), digest(base, True), digest(allow), views] + [digest(os.path.join(WS, t)) for t in TOOLS[test]]
    return '|'.join(parts)


def recorded():
    try:
        return json.load(open(RECORD))
    except (OSError, ValueError):
        return {}


def remember(k):
    r = recorded(); r[k] = time.strftime('%Y-%m-%d %H:%M')
    os.makedirs(os.path.dirname(RECORD), exist_ok=True)
    json.dump(r, open(RECORD, 'w'), indent=1)


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    page, base = argv[0], argv[1]
    allow = argv[argv.index('--allow') + 1] if '--allow' in argv else None
    views = argv[argv.index('--views') + 1] if '--views' in argv else 'desk,phone'
    skip = set(argv[argv.index('--skip') + 1].split(',')) if '--skip' in argv else set()
    fresh = '--fresh' in argv
    ok = True
    keys = {t: key(t, page, base, allow, views) for t in TOOLS}
    rec = {} if fresh else recorded()
    for t in list(TOOLS):
        if t not in skip and keys[t] in rec:
            print('%-6s PASS (recorded %s: same page, base, allow list, views and tools)' % (t, rec[keys[t]]))
            skip.add(t)
    passed = []

    def run_t(t, cmd, word):
        r = run(t, cmd, word)
        if r:
            passed.append(t)
        return r
    with tempfile.TemporaryDirectory() as d:
        if 'parity' not in skip:
            checks = os.path.join(d, 'checks.json')
            r = subprocess.run(['node', 'tools/ui_check.js', 'css', base, page, checks], cwd=WS, capture_output=True, text=True)
            if r.returncode:
                print('parity FAIL ui_check css: ' + (r.stderr or r.stdout)[-400:])
                ok = False
            elif not json.load(open(checks)).get('checks'):
                print('parity PASS no style rule differs between the live page and the candidate (0 checks; no page loaded)')
                passed.append('parity')
            else:
                os.makedirs(os.path.join(WS, 'local', 'ui_gate'), exist_ok=True)
                cmd = ['node', 'tools/ui_check.js', 'run', base, page, checks, '--views', views, '--max-els', '300',
                       '--out', os.path.join(WS, 'local', 'ui_gate', 'parity.json')] + (['--allow', allow] if allow else [])
                ok &= run_t('parity', cmd, 'UI-CHECK SAME')
        if 'theme' not in skip:
            ok &= run_t('theme', ['node', 'tools/theme_gate.js', page, '--views', views], 'PASS')
        if 'a11y' not in skip:
            ok &= run_t('a11y', ['node', 'tools/a11y_scan.js', page, '--views', views,
                               '--baseline', 'tools/spine/a11y_baseline.json'], 'A11Y PASS')
        if 'perf' not in skip:
            ok &= run_t('perf', [sys.executable, 'tools/perf_budget.py', page], 'PERF PASS')
        if 'twopane' not in skip:
            ok &= run_t('twopane', ['node', 'tools/two_pane_check.js', page], 'TWO-PANE PASS')
    for t in passed:
        remember(keys[t])
    print('UI-GATE ' + ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
