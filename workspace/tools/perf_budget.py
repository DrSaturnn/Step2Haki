#!/usr/bin/env python3
"""perf_budget.py: the page's performance budget (shipped size, element count at load, load time).

  python3 tools/perf_budget.py PAGE [--baseline tools/spine/perf_baseline.json] [--write] [--runs 3]

Runs tools/perf_load.js (local HTTP server, Chromium, desk and phone with the phone CPU slowed 4x; median of the runs)
and compares with the baseline:
  size (bytes of the shipped page without the changelog block and the build stamp, which every ship rewrites) and
  el_load (elements at the load event): any rise fails;
  load and ready (ms): a rise of more than TIME_TOL, and of more than TIME_FLOOR ms, fails (headless timing varies).
--write records the measured figures as the new baseline (a batch that adds content raises size and elements on
purpose: it writes the baseline and lists the change in its report). Exit 1 when a figure is worse.
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BL = os.path.join(HERE, 'spine', 'perf_baseline.json')
TIME_TOL = 0.15
TIME_FLOOR = 150  # ms: a desk load near 400 ms varies by more than 15% between headless runs
COUNT_KEYS = ('el_load',)
TIME_KEYS = ('load', 'ready')


AXLOG = re.compile(rb'(<script type="application/json" id="axlog">).*?(</script>)', re.S)
STAMP = re.compile(rb'(<meta name="ax-build" content=")[^"]*(">)')


def page_size(page):
    """Bytes of the page with the axlog body and the ax-build stamp emptied: ship.sh fills both after the build, so the
    figure is the same for a candidate and its shipped page (s167 follow-on, folded into s166)."""
    b = open(page, 'rb').read()
    b = AXLOG.sub(rb'\1\2', b, count=1)
    b = STAMP.sub(rb'\1\2', b, count=1)
    return len(b)


def measure(page, runs):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, 'perf.json')
        r = subprocess.run(['node', os.path.join(HERE, 'perf_load.js'), page, '--runs', str(runs), '--views', 'desk,phone',
                            '--json', out], capture_output=True, text=True)
        if r.returncode:
            sys.exit('perf_load failed: ' + (r.stderr or r.stdout)[-800:])
        j = json.load(open(out))
    fig = {'size': page_size(page)}
    for view, v in j['views'].items():
        for k in COUNT_KEYS + TIME_KEYS:
            fig[view + '.' + k] = v['median'].get(k)
    return fig


def main(argv):
    if not argv or argv[0].startswith('-'):
        sys.exit(__doc__)
    page = argv[0]
    bl = argv[argv.index('--baseline') + 1] if '--baseline' in argv else DEFAULT_BL
    runs = int(argv[argv.index('--runs') + 1]) if '--runs' in argv else 3
    fig = measure(page, runs)
    print('perf: ' + ' '.join('%s=%s' % kv for kv in sorted(fig.items())))
    if '--write' in argv:
        json.dump(fig, open(bl, 'w'), indent=1)
        open(bl, 'a').write('\n')
        print('perf baseline written: ' + bl)
        return 0
    base = json.load(open(bl))
    worse = []
    for k, v in fig.items():
        b = base.get(k)
        if v is None or b is None:
            continue
        lim = max(b * (1 + TIME_TOL), b + TIME_FLOOR) if k.split('.')[-1] in TIME_KEYS else b
        if v > lim:
            worse.append('%s %s > %s (limit %d)' % (k, b, v, lim))
    if worse:
        print('PERF WORSE: ' + '; '.join(worse))
        return 1
    print('PERF PASS (size and elements at or below the baseline, times within %d%% or %d ms)' % (TIME_TOL * 100, TIME_FLOOR))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
