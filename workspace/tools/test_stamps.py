#!/usr/bin/env python3
"""test_stamps.py: the stamp groups hold what each check reads, and no more (ship step rules-stamps).

  python3 tools/test_stamps.py [--no-trace] [--only CHECK[,CHECK]] [--folder SPINE_FOLDER]

Unit cases (always): a decision line added to DECISIONS_DIGEST keeps every verify stamp and reruns the gate; a State
rewrite keeps both; STANDING_DIRECTIONS and the code a check runs still void its stamp; a lead tool no check reads
voids none.
Trace cases (need strace; --no-trace skips them): each check runs once under `strace -f` and every file it opens for
reading inside the workspace or the private docs must be in the check's groups (stamps.covered) or in stamps.EXEMPT
with a reason. A miss prints the file: add it to the check's groups in tools/stamps.py (or to EXEMPT with the reason
it cannot change the result), never to this test. verify is traced on one spine folder (--folder, or the first local
folder of a brief on the page); with no local folder that case is skipped and named.
"""
import fnmatch
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import docs_path  # noqa: E402
import stamps as S  # noqa: E402

DOCS = os.path.realpath(docs_path.docs_dir())
PASS, BAD = [], []


def expect(name, ok, detail=''):
    (PASS if ok else BAD).append(name)
    print('%s %s%s' % ('ok ' if ok else 'BAD', name, '' if ok else ': ' + str(detail)[:1500]))


# ---- unit cases
def groups(check, private=None, folder=None, page=None):
    """the check's groups, computed in a fresh process (docs_path reads S2H_PRIVATE at import)"""
    code = ('import json, sys; sys.path.insert(0, %r); import stamps as S; '
            'print(json.dumps(S.hashed(S.spec(%r, page=%r, folder=%r))))' % (HERE, check, page, folder))
    env = dict(os.environ, **({'S2H_PRIVATE': private} if private else {}))
    return json.loads(subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, env=env, cwd=WS).stdout)


def changed(a, b):
    return sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))


def unit():
    t = tempfile.mkdtemp(prefix='stamps-test-')
    priv = os.path.join(t, 'private')
    shutil.copytree(DOCS, os.path.join(priv, 'docs'), ignore=shutil.ignore_patterns('batches'))
    folder = os.path.join(WS, 'repair', 'migration', '_s0stamptest', 'groups', 'spine')   # an ignored path
    os.makedirs(folder, exist_ok=True)
    json.dump({'edits': [{'op': 'replace_brief', 'brief': 's0-stamp-groups', 'html': '<div></div>'}]},
              open(os.path.join(folder, '10_s0_stamp_groups_spine.json'), 'w'))
    page = os.path.join(WS, 'index.html')
    try:
        v0, g0 = groups('verify', priv, folder), groups('gate', priv, page=page)
        expect('groups computed (verify %d, gate %d)' % (len(v0), len(g0)), len(v0) >= 9 and len(g0) >= 8, (v0, g0))

        def edit(name, text='\n- 2099-01-01 [D-20990101-1] {process} test line. (one-time)\n'):
            with open(os.path.join(priv, 'docs', name), 'a', encoding='utf-8') as f:
                f.write(text)
        edit('DECISIONS_DIGEST.md')
        v1, g1 = groups('verify', priv, folder), groups('gate', priv, page=page)
        expect('a digest line keeps the verify stamp (same key)', v1 == v0, changed(v0, v1))
        expect('a digest line reruns the gate (it reads the digest): docs', changed(g0, g1) == ['docs'], changed(g0, g1))
        for name in ('STEP2HAKI_HANDOFF.md', 'RESUME.md', 'OPEN_WORK.md'):
            edit(name, '\nstate test line\n')
        v2, g2 = groups('verify', priv, folder), groups('gate', priv, page=page)
        expect('a State, RESUME or OPEN_WORK rewrite keeps the verify and gate stamps', v2 == v1 and g2 == g1,
               changed(v1, v2) + changed(g1, g2))
        edit('STANDING_DIRECTIONS.md', '\n- test rule line\n')
        v3 = groups('verify', priv, folder)
        expect('a STANDING_DIRECTIONS change voids the verify stamp: docs', changed(v2, v3) == ['docs'], changed(v2, v3))
        open(os.path.join(folder, 'facts.json'), 'w').write('{}')
        v4 = groups('verify', priv, folder)
        expect('a folder change voids the verify stamp: folder', changed(v3, v4) == ['folder'], changed(v3, v4))
    finally:
        shutil.rmtree(t, ignore_errors=True)
        shutil.rmtree(os.path.dirname(os.path.dirname(folder)), ignore_errors=True)
    vc, gc = set(S.closure(S.ENTRY['verify'])), set(S.closure(S.ENTRY['gate']))
    need = ['tools/spine/verify.py', 'tools/gate.py', 'tools/render.js', 'tools/preflight.py', 'tools/vendor_scan.py',
            'tools/spine/numbers.py', 'tools/pagelib.py', 'tools/apply_edits.py', 'repair/build.py']
    expect('verify code closure holds the scripts verify runs', all(n in vc for n in need), [n for n in need if n not in vc])
    lead = ['tools/spine/patch.py', 'tools/spine/batch.py', 'tools/spine/docstate.py', 'tools/spine/review_packet.py',
            'tools/spine/launch.py', 'tools/hooks/approval.py', 'tools/hooks/callgate.py', 'tools/test_stamps.py']
    expect('lead tools no check reads are in no verify or gate key', not [n for n in lead if n in vc | gc],
           [n for n in lead if n in vc | gc])
    for c, ex in S.EXEMPT.items():
        expect('EXEMPT %s: every entry carries a reason' % c, all(len(r) > 20 for _, r in ex))


# ---- trace cases
LINE = re.compile(r'^\d+\s+(?:openat\(AT_FDCWD, |open\()"((?:[^"\\]|\\.)*)", ([A-Z_|0-9]+)[^)]*\)\s+=\s+(\d+)')
PYC = re.compile(r'/__pycache__/([^/]+?)\.[\w-]+\.pyc$')


def traced(cmd, env=None):
    """(returncode, output, files opened for reading under the workspace or the private docs)"""
    fd, log = tempfile.mkstemp(prefix='stamps-trace-')
    os.close(fd)
    try:
        r = subprocess.run(['strace', '-f', '-qq', '-e', 'trace=openat,open', '-o', log] + cmd, cwd=WS,
                           capture_output=True, text=True, env=env)
        seen = set()
        for l in open(log, errors='replace'):
            m = LINE.match(l)
            if not m or re.search(r'O_DIRECTORY|O_WRONLY|O_CREAT', m.group(2)):
                continue
            p = m.group(1) if os.path.isabs(m.group(1)) else os.path.join(WS, m.group(1))
            p = PYC.sub(r'/\1.py', p)                 # a cached module stands for its source
            p = os.path.realpath(p)
            if os.path.isfile(p):
                seen.add(p)
    finally:
        os.remove(log)
    return r.returncode, (r.stdout + r.stderr).strip(), seen


def label(p):
    if p.startswith(DOCS + os.sep):
        return 'docs:' + os.path.relpath(p, DOCS).replace(os.sep, '/')
    return os.path.relpath(p, WS).replace(os.sep, '/')


SKIP_DIRS = ('.git/', 'node_modules/', 'local/')    # git's own files; packages (package-lock is hashed); logs and stamps


def outside(check, seen, sp, tmp_ok=()):
    cov = S.covered(check, sp)
    out = []
    if any(pat == 'tree:changed' for pat, _ in S.EXEMPT.get(check, [])):
        top, tree, _ = S._repo()
        cov |= {os.path.realpath(os.path.join(top, r)) for r in tree}
    for p in sorted(seen):
        if p in cov or not (p.startswith(os.path.realpath(WS) + os.sep) or p.startswith(DOCS + os.sep)):
            continue
        lb = label(p)
        if lb.startswith(SKIP_DIRS) or '/node_modules/' in lb or '__pycache__' in lb or lb.endswith('.log'):
            continue
        if any(fnmatch.fnmatch(lb, pat) for pat, _ in S.EXEMPT.get(check, [])):
            continue
        out.append(lb)
    return out


def spine_folder():
    try:
        page = open(os.path.join(WS, 'index.html'), encoding='utf-8').read()
    except OSError:
        return None
    for e in sorted(glob.glob(os.path.join(WS, 'repair', 'migration', '*', '*', 'spine', '10_*_spine.json'))):
        d = os.path.dirname(e)
        try:
            bid = json.load(open(e, encoding='utf-8'))['edits'][0]['brief']
        except (OSError, ValueError, KeyError, IndexError):
            continue
        if 'id="%s"' % bid in page and os.path.exists(os.path.join(d, 'facts.json')) and \
                os.path.exists(os.path.join(d, 'build.py')):
            return d
    return None


def trace(only, folder):
    if not shutil.which('strace'):
        expect('trace cases: strace is installed', False, 'install strace, or run with --no-trace and say so')
        return
    page = os.path.join(WS, 'index.html')
    py = sys.executable
    cases = [('rules-migrate', [py, 'tools/test_migrate_check.py'], {}, 'passed'),
             ('rules-gate', [py, 'tools/test_gate_rules.py'], {}, 'passed'),
             ('gate', [py, 'tools/gate.py', page, '--base', 'HEAD'], {'page': page}, 'gate:'),
             ('render', ['node', 'tools/render.js', page], {'page': page}, 'render:')]
    if os.path.isdir(os.path.join(WS, 'repair', 'sources')):
        cases += [('vendor-scan', [py, 'tools/vendor_scan.py'], {}, 'vendor_scan'),
                  ('vendor-orphan', [py, 'tools/vendor_scan.py', '--page', page], {'page': page}, 'vendor_scan')]
    else:
        print('skip vendor-scan, vendor-orphan: repair/sources is not restored (local-only)')
    folder = folder or spine_folder()
    if folder:
        cases.append(('verify', [py, 'tools/spine/verify.py', folder, '--no-stamp'], {'folder': folder}, 'preview'))
    else:
        print('skip verify: no local spine folder of a brief on the page (restore local-only)')
    for check, cmd, kw, word in cases:
        if only and check not in only:
            continue
        sp0 = S.spec(check, **kw)
        rc, out, seen = traced(cmd)
        ran = word in out            # the run reached the check's own work (a verdict of FAIL still reads its inputs)
        expect('%s ran under the trace (%d files opened)' % (check, len(seen)), ran and len(seen) > 0, out[-600:])
        miss = outside(check, seen, sp0)
        expect('%s: every file it opened is in its groups%s' % (check, ' (%s)' % os.path.relpath(folder, WS) if check == 'verify' else ''),
               not miss, '%d outside: %s' % (len(miss), ', '.join(miss[:60])))


def main(argv):
    only = set(argv[argv.index('--only') + 1].split(',')) if '--only' in argv else None
    folder = os.path.abspath(argv[argv.index('--folder') + 1]) if '--folder' in argv else None
    if not only:
        unit()
    if '--no-trace' in argv:
        print('trace cases skipped (--no-trace)')
    else:
        trace(only, folder)
    print('%d/%d passed' % (len(PASS), len(PASS) + len(BAD)))
    return 1 if BAD else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
