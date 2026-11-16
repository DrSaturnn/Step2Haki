#!/usr/bin/env python3
"""size_check.py: the page size the ship's perf check will measure, from a workspace build, in seconds.

  python3 tools/spine/size_check.py PAGE [--baseline tools/spine/perf_baseline.json]

Copies PAGE to a scratch folder, runs tools/site_build.py on the copy (the styles and scripts the ship adds), and
measures it as tools/perf_budget.py does (change log body and build stamp emptied). Prints the size against the
baseline; exit 1 when it is larger. A batch that adds content on purpose raises the baseline with perf_budget.py
--write or by setting "size" to the printed figure, and says so in its report."""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def measure(page):
    spec = importlib.util.spec_from_file_location('perf_budget', os.path.join(WS, 'tools', 'perf_budget.py'))
    pb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pb)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'index.html')
        shutil.copy(page, p)
        r = subprocess.run([sys.executable, os.path.join(WS, 'tools', 'site_build.py'), p], capture_output=True, text=True,
                           cwd=WS)
        if r.returncode:
            sys.exit('size_check: site_build failed: ' + (r.stderr or r.stdout)[-400:])
        return pb.page_size(p)


def main(a):
    if not a:
        sys.exit(__doc__)
    base = a[a.index('--baseline') + 1] if '--baseline' in a else os.path.join(WS, 'tools', 'spine', 'perf_baseline.json')
    limit = json.load(open(base))['size']
    size = measure(a[0])
    if size > limit:
        print('size: %d over the baseline %d by %d bytes (perf would fail at S8)' % (size, limit, size - limit))
        return 1
    print('size: %d within the baseline %d' % (size, limit))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
