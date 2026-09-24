#!/usr/bin/env python3
"""verify_edits.py: the one check a worker runs before finishing.

  python3 tools/verify_edits.py <edits.json> [page] [--no-render]

1. schema-checks every op; 2. applies the edits to a scratch copy (every anchor must be
unique in its brief); 3. runs tools/gate.py on the copy with the original page as base
(never delete, ids immutable, version bumped on key/distractor change); 4. runs
tools/render.js on the copy (0 malformed MCQs, no dead anchors, no JS errors) and checks
the MCQ count equals the static item count; 5. flags new or edited items that
near-duplicate an existing item. Prints each failure with its fix. Exit 0 = clean.
The original page is never written.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from pagelib import items, read_page, text, write_page  # noqa: E402
import apply_edits  # noqa: E402

STOPW = set('a an the and or of to in on for with at by from is are was with no not this that'.split())


def words(s):
    return {w for w in re.findall(r'[a-z0-9]+', text(s).lower()) if w not in STOPW}


def jacc(a, b):
    return len(a & b) / float(len(a | b)) if a and b else 0.0


def near_dups(before_html, after_html):
    """Items added or whose stem/key changed, compared against every other item."""
    old = {i.id: (i.stem, i.key) for i in items(before_html)}
    now = items(after_html)
    touched = [i for i in now if old.get(i.id) != (i.stem, i.key)]
    out = []
    for t in touched:
        ts, tk = words(t.stem), re.sub(r'\s+', ' ', t.key.lower()).strip()
        for o in now:
            if o.id == t.id:
                continue
            j = jacc(ts, words(o.stem))
            same_key = re.sub(r'\s+', ' ', o.key.lower()).strip() == tk
            if (same_key and j >= 0.6) or j >= 0.85:
                out.append((t, o, j, same_key))
    return out


def main(argv):
    render = '--no-render' not in argv
    pos = [a for a in argv if not a.startswith('--')]
    if not pos:
        print(__doc__)
        return 2
    page = os.path.abspath(pos[1] if len(pos) > 1 else os.path.join(REPO, 'index.html'))
    fails = []
    try:
        spec = json.load(open(pos[0], encoding='utf-8'))
    except Exception as ex:
        print('verify_edits: FAIL cannot read %s as JSON: %s\n      fix: write valid JSON (double quotes, no trailing commas)' % (pos[0], ex))
        return 1
    errs = apply_edits.validate(spec)
    if errs:
        print('verify_edits: FAIL %d schema error(s)' % len(errs))
        for n, op, msg, fix in errs:
            print('  [schema] edit %d (%s): %s\n      fix: %s' % (n, op, msg, fix))
        return 1
    before = read_page(page)
    try:
        after, log = apply_edits.apply(before, spec)
    except apply_edits.EditError as ex:
        print('verify_edits: FAIL edits do not apply\n  [apply] %s' % ex)
        return 1
    tmp = tempfile.mkdtemp(prefix='axbx-verify-')
    try:
        scratch = os.path.join(tmp, 'index.html')
        base = os.path.join(tmp, 'base.html')
        write_page(scratch, after)
        shutil.copyfile(page, base)
        # coverage.csv resolves beside the page: mirror the repo's repair/nbme into the scratch dir
        cov = os.path.join(os.path.dirname(page), 'repair', 'nbme')
        if not os.path.isdir(cov):
            cov = os.path.join(REPO, 'repair', 'nbme')
        if os.path.isdir(cov):
            shutil.copytree(cov, os.path.join(tmp, 'repair', 'nbme'))
        g = subprocess.run([sys.executable, os.path.join(HERE, 'gate.py'), scratch, '--base', base], capture_output=True, text=True)
        gate_line = g.stdout.splitlines()[0] if g.stdout else 'gate: no output ' + g.stderr[-200:]
        if g.returncode != 0:
            fails.append(('gate', g.stdout.strip() or g.stderr.strip()))
        render_line = 'render: skipped'
        if render:
            r = subprocess.run(['node', os.path.join(HERE, 'render.js'), scratch], capture_output=True, text=True, timeout=180)
            render_line = r.stdout.splitlines()[0] if r.stdout else 'render: no output ' + r.stderr[-200:]
            if r.returncode != 0:
                fails.append(('render', r.stdout.strip() or r.stderr.strip()))
            m = re.search(r'\| mcq (\d+)', render_line)
            n_items = len(items(after, with_briefs=False))
            if m and int(m.group(1)) != n_items:
                fails.append(('mcq-count', 'rendered %s MCQs for %d items\n      fix: every item needs a direct-child arrow and both data-d1/data-d2'
                              % (m.group(1), n_items)))
        dups = near_dups(before, after)
        for t, o, j, same in dups:
            fails.append(('near-dup', '%s (%s) resembles %s (%s): stem overlap %.2f%s\n      new: %s -> %s\n      old: %s -> %s\n'
                          '      fix: do not duplicate a question; change the deciding variable, or drop the item and link the existing one'
                          % (t.id, t.brief_id, o.id, o.brief_id, j, ', same key' if same else '', t.stem[:90], t.key[:50], o.stem[:90], o.key[:50])))
        delta = len(items(after, with_briefs=False)) - len(items(before, with_briefs=False))
        status = 'FAIL' if fails else 'PASS'
        print('verify_edits: %s %d op(s), items %+d, near-dups %d' % (status, len(log), delta, len(dups)))
        print('  ' + gate_line)
        print('  ' + render_line)
        for code, msg in fails:
            if code in ('gate', 'render'):
                body = [l for l in msg.splitlines()[1:]]
                if body:
                    print('\n'.join('  ' + l for l in body))
            else:
                print('  [%s] %s' % (code, msg))
        return 1 if fails else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
