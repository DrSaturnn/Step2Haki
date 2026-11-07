#!/usr/bin/env python3
"""ui_gate.py: the standing UI tests run before a ship (UI_REFACTOR_PLAN 6b).

  python3 tools/ui_gate.py PAGE BASE [--allow ALLOW.json] [--views desk,phone] [--skip parity,theme,a11y,perf]

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
Exit 1 when any test fails; every test runs and prints its verdict line. About 25 minutes in a two-core container.
"""
import os, subprocess, sys, tempfile, time

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


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    page, base = argv[0], argv[1]
    allow = argv[argv.index('--allow') + 1] if '--allow' in argv else None
    views = argv[argv.index('--views') + 1] if '--views' in argv else 'desk,phone'
    skip = set(argv[argv.index('--skip') + 1].split(',')) if '--skip' in argv else set()
    ok = True
    with tempfile.TemporaryDirectory() as d:
        if 'parity' not in skip:
            checks = os.path.join(d, 'checks.json')
            r = subprocess.run(['node', 'tools/ui_check.js', 'css', base, page, checks], cwd=WS, capture_output=True, text=True)
            if r.returncode:
                print('parity FAIL ui_check css: ' + (r.stderr or r.stdout)[-400:])
                ok = False
            else:
                os.makedirs(os.path.join(WS, 'local', 'ui_gate'), exist_ok=True)
                cmd = ['node', 'tools/ui_check.js', 'run', base, page, checks, '--views', views, '--max-els', '300',
                       '--out', os.path.join(WS, 'local', 'ui_gate', 'parity.json')] + (['--allow', allow] if allow else [])
                ok &= run('parity', cmd, 'UI-CHECK SAME')
        if 'theme' not in skip:
            ok &= run('theme', ['node', 'tools/theme_gate.js', page, '--views', views], 'PASS')
        if 'a11y' not in skip:
            ok &= run('a11y', ['node', 'tools/a11y_scan.js', page, '--views', views,
                               '--baseline', 'tools/spine/a11y_baseline.json'], 'A11Y PASS')
        if 'perf' not in skip:
            ok &= run('perf', [sys.executable, 'tools/perf_budget.py', page], 'PERF PASS')
    print('UI-GATE ' + ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
