#!/usr/bin/env python3
"""stamps.py: input-hash stamps for the ship checks (s171b; D-20261109-4, Jonathan 2026-11-09: "no reason to run things
unnecessarily unless there was a rationale").

A check that passed writes a stamp: one sha256 per group of the files it reads, and the combined key. The next run of
the same check on the same inputs is skipped and prints the stamp's date; a run whose inputs changed names the groups
that changed and runs the check. So ship.sh rerun after a late fail repeats only the failed check and the checks whose
inputs changed, and ready_gate.py accepts the READY stamp verify.py wrote at S8.

Stamps live in local/stamps/<check>/<name>.json (untracked, in the container that ran the check, like the approval
record; AX_STAMPS_DIR overrides it in test_hooks.py only). A stamp keeps the last 5 passing keys. AX_STAMPS=off makes every check
miss (a deliberate cold run); passes still write stamps. callgate refuses hand writes to the store (G-STAMP).

  python3 tools/stamps.py check CHECK PENDING [--page P] [--attr-only REF]
        exit 0 and print the stored summary line when CHECK's stamp matches; exit 1 and print the changed groups
        otherwise. Either way PENDING gets the key, for commit after the check passes.
  python3 tools/stamps.py commit PENDING [SUMMARY]   write the stamp from PENDING (ship.sh, after the check passed)
  python3 tools/stamps.py show [CHECK]               list the stamps

Checks (ship.sh): rules-migrate, rules-gate, gate, render, vendor-scan, vendor-orphan; verify (one stamp per spine
folder, written by verify.py on READY); ui_gate tests (parity, a11y, perf, twopane; theme keeps style_surface's record).
Groups are deliberately wide (every Python and JS tool, every tool data file): a check reruns when any tool it could
load changed. The perf and a11y baselines belong only to ui_gate, so fixing one (the s171 abort) reruns only perf or a11y.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
# AX_STAMPS_DIR is honored only beside AX_HOOK_STATE (test_hooks.py), a variable callgate refuses in the lead's commands
STORE = (os.environ.get('AX_STAMPS_DIR') if os.environ.get('AX_HOOK_STATE') else None) or os.path.join(WS, 'local', 'stamps')
KEEP = 5
UI_ONLY = {'tools/spine/perf_baseline.json', 'tools/spine/a11y_baseline.json'}

_cache = {}


def off():
    return os.environ.get('AX_STAMPS', '').lower() in ('off', '0', 'no', 'false')


def fhash(p):
    """sha256 of a file's bytes ('-' when missing); cached on (size, mtime) within one process"""
    try:
        st = os.stat(p)
    except OSError:
        return '-'
    if not os.path.isfile(p):   # a directory or a symlink to one (git lists an untracked symlink as a file)
        return 'dir:' + (os.readlink(p) if os.path.islink(p) else '')
    k = (p, st.st_size, st.st_mtime_ns)
    if k not in _cache:
        h = hashlib.sha256()
        with open(p, 'rb') as f:
            for b in iter(lambda: f.read(1 << 20), b''):
                h.update(b)
        _cache[k] = h.hexdigest()
    return _cache[k]


def files(root, patterns, exclude=()):
    out = set()
    for pat in patterns:
        for p in glob.glob(os.path.join(root, pat), recursive=True):
            if os.path.isfile(p):
                rel = os.path.relpath(p, root).replace(os.sep, '/')
                if rel not in exclude and '__pycache__' not in rel and not rel.endswith('.pyc'):
                    out.add(rel)
    return sorted(out)


def ghash(root, rels, extra=''):
    """one hash for a group: each file's path and content hash, in path order, plus any extra text"""
    h = hashlib.sha256(extra.encode())
    for r in rels:
        h.update(('%s\0%s\n' % (r, fhash(os.path.join(root, r)))).encode())
    return h.hexdigest()[:16]


def _run(args):
    try:
        return subprocess.run(args, capture_output=True, text=True, cwd=WS).stdout.strip()
    except OSError:
        return '-'


def _docs():
    try:
        sys.path.insert(0, HERE)
        import docs_path
        return docs_path.docs_dir()
    except Exception:  # noqa: BLE001
        return None


# ---- the groups
def g_tools_code():
    rel = files(WS, ['tools/**/*.py', 'tools/**/*.js', 'tools/**/*.sh', 'repair/build.py'], exclude=())
    rel = [r for r in rel if not r.startswith(('tools/plugin/', 'tools/hooks/'))]
    rel.append('package-lock.json')
    return ghash(WS, rel, 'node %s | python %s' % (_run(['node', '--version']), sys.version.split()[0]))


def g_tools_data():
    rel = files(WS, ['tools/**/*.json', 'tools/**/*.txt', 'tools/**/*.csv', 'tools/**/*.md', 'tools/tests/**/*'],
                exclude=UI_ONLY)
    return ghash(WS, [r for r in rel if not r.startswith(('tools/plugin/', 'tools/hooks/'))])


DOCS = ['DECISIONS_DIGEST.md', 'STANDING_DIRECTIONS.md', 'BATCH_RUNBOOK.md', 'ui/UI_MAP.md']


def g_docs():
    """the private docs the tools read (gate doc-lint, verify specs, ui-retired); the handoff, RESUME and OPEN_WORK
    change at every step; the gate's state checks read the handoff and RESUME (s172c), and they stay out of the
    stamp on purpose: a State rewrite must not void every stamp, and resume.py, launch.py and docstate.py rerun those
    checks at every chat start and State rewrite"""
    d = _docs()
    return ghash(d, DOCS) if d else 'none'


# records the tools write as they run (budgets, audit and context records, the State archive); no check reads them as
# rules, and counting them would void every stamp at the next theme pass or State move
RECORDS = ('WAVE.json', 'style_audits.json', 'context_baseline.json', 'STATE_ARCHIVE.md', 'RESULTS.md')


def g_rules():
    """TEXTBOOK_STYLE, ABBREV, ALIASES, HEADERS and the other top-level rule files; the rules sheets"""
    rel = files(WS, ['repair/efficiency/*.json', 'repair/efficiency/*.md', 'repair/migration/spine/rules/*.md'],
                exclude={'repair/efficiency/' + f for f in RECORDS})
    return ghash(WS, rel)


def g_site():
    return ghash(WS, files(WS, ['site/**/*']))


def g_sources():
    return ghash(WS, files(WS, ['repair/sources/**/*']))


def g_gate_repo():
    """repo files the gate reads beside the page: retirements, archived items, the NBME coverage table"""
    return ghash(WS, files(WS, ['repair/migration/**/spine/06_*_retire.json', 'repair/archive/**/*', 'repair/nbme/coverage.csv']))


def g_base_page():
    """what tools/spine/basepage.py adds to the working page: pending shells, retirements, the wave's site files (the
    wave id from WAVE.json; its spend fields change as agents run)"""
    rel = files(WS, ['repair/migration/**/spine/05_*_new.json', 'repair/migration/**/spine/06_*_retire.json'])
    try:
        w = json.load(open(os.path.join(WS, 'repair', 'efficiency', 'WAVE.json'), encoding='utf-8')).get('wave') or ''
    except (OSError, ValueError, AttributeError):
        w = ''
    if w:
        rel += files(WS, ['repair/%s/0[0-4]_*.json' % w])
    return ghash(WS, rel, 'wave %s | HEAD:index.html %s' % (w, head_page()))


def head_page():
    return _run(['git', 'rev-parse', 'HEAD:./index.html']) or '-'


def g_repo():
    """everything vendor_scan reads: the tracked files (index blobs and working-tree changes) and untracked files git
    does not ignore"""
    idx = _run(['git', 'ls-files', '-s'])
    top = _run(['git', 'rev-parse', '--show-toplevel'])
    changed = _run(['git', 'ls-files', '-m', '--full-name']).splitlines() + \
        _run(['git', 'ls-files', '--others', '--exclude-standard', '--full-name']).splitlines()
    return ghash(top, sorted(set(changed)), idx)


def page_hash(p):
    return fhash(os.path.abspath(p))[:16] if p else '-'


def beside(p, name):
    return page_hash(os.path.join(os.path.dirname(os.path.abspath(p)), name)) if p else '-'


# ---- keys per check
def verify_groups(folder):
    """verify.py on one spine folder: the folder, its receipts, the page it builds on, the rules, the tools, the
    sources (logs written into the folder, such as verify_all.log, are left out). Left out on purpose: the tracked tree its preview vendor_scan also reads; ship.sh runs vendor-scan and
    vendor-orphan on that tree at every ship whose tree changed."""
    folder = os.path.abspath(folder)
    bid = brief_id(folder)
    rec = files(WS, ['repair/migration/spine/reviews/%s_*.md' % bid]) if bid else []
    return {'folder': ghash(folder, [r for r in files(folder, ['**/*']) if not r.endswith('.log')]),
            'receipts': ghash(WS, rec, bid or '?'),
            'page': page_hash(os.path.join(WS, 'index.html')) + g_base_page(),
            'rules': g_rules(), 'docs': g_docs(), 'site': g_site(),
            'tools': g_tools_code(), 'tool-data': g_tools_data(), 'sources': g_sources()}


def folder_name(folder):
    """a spine folder's stamp name: its path under the workspace"""
    return os.path.relpath(os.path.abspath(folder), WS).replace(os.sep, '/')


def brief_id(folder):
    for e in sorted(glob.glob(os.path.join(folder, '10_*_spine.json'))):
        try:
            return json.load(open(e, encoding='utf-8'))['edits'][0]['brief']
        except (OSError, ValueError, KeyError, IndexError):
            pass
    return None


def ship_groups(check, page=None, attr_only=None):
    if check == 'rules-migrate':
        return {'tools': g_tools_code(), 'tool-data': g_tools_data()}
    if check == 'rules-gate':
        # the gate's code and rule files (OPEN_WORK "Ship time"); the page to ship is gated by the gate check itself
        return {'tools': g_tools_code(), 'tool-data': g_tools_data(), 'docs': g_docs(), 'rules': g_rules(),
                'site': g_site(), 'gate-repo': g_gate_repo()}
    if check == 'gate':
        return {'page': page_hash(page), 'search-index': beside(page, 'search.json'),
                'base': ('attr-only ' + _run(['git', 'rev-parse', '%s:./index.html' % attr_only])) if attr_only else head_page(),
                'tools': g_tools_code(), 'tool-data': g_tools_data(), 'docs': g_docs(), 'rules': g_rules(),
                'site': g_site(), 'gate-repo': g_gate_repo()}
    if check == 'render':
        return {'page': page_hash(page), 'tools': ghash(WS, ['tools/render.js', 'tools/render_allowlist.txt',
                                                              'package-lock.json'], _run(['node', '--version']))}
    if check == 'vendor-scan':
        return {'repo': g_repo(), 'sources': g_sources(),
                'tools': ghash(WS, ['tools/vendor_scan.py', 'tools/local_only.txt'])}
    if check == 'vendor-orphan':
        return {'page': page_hash(page), 'repo': g_repo(), 'sources': g_sources(),
                'tools': ghash(WS, ['tools/vendor_scan.py', 'tools/local_only.txt'])}
    raise SystemExit('stamps: unknown check %s' % check)


# ---- store
def path(check, name):
    return os.path.join(STORE, check, name.replace('/', '__') + '.json')


def combined(groups):
    return hashlib.sha256(json.dumps(groups, sort_keys=True).encode()).hexdigest()[:16]


def lookup(check, name, groups):
    """(hit entry or None, changed group names against the newest stamp)"""
    try:
        rec = json.load(open(path(check, name), encoding='utf-8'))
    except (OSError, ValueError):
        return None, ['no stamp']
    if off():
        return None, ['AX_STAMPS=off']
    k = combined(groups)
    for e in rec.get('entries', []):
        if e.get('key') == k:
            return e, []
    last = (rec.get('entries') or [{}])[0].get('groups', {})
    return None, sorted(g for g in set(groups) | set(last) if groups.get(g) != last.get(g)) or ['key']


def write(check, name, groups, **meta):
    p = path(check, name)
    try:
        rec = json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        rec = {'check': check, 'name': name, 'entries': []}
    k = combined(groups)
    e = dict(meta, key=k, groups=groups, date=time.strftime('%Y-%m-%d %H:%M'))
    rec['entries'] = [e] + [x for x in rec.get('entries', []) if x.get('key') != k][:KEEP - 1]
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'
    json.dump(rec, open(tmp, 'w', encoding='utf-8'), indent=1)
    os.replace(tmp, p)
    return e


def main(argv):
    if not argv or argv[0] not in ('check', 'commit', 'show'):
        sys.exit(__doc__)
    if argv[0] == 'show':
        for p in sorted(glob.glob(os.path.join(STORE, argv[1] if len(argv) > 1 else '*', '*.json'))):
            rec = json.load(open(p, encoding='utf-8'))
            e = (rec.get('entries') or [{}])[0]
            print('%-14s %-40s %s %s' % (rec.get('check'), rec.get('name'), e.get('date'), (e.get('summary') or '')[:80]))
        return 0
    if argv[0] == 'commit':
        pend = json.load(open(argv[1], encoding='utf-8'))
        summary = argv[2] if len(argv) > 2 else ''
        write(pend['check'], pend['name'], pend['groups'], summary=summary.strip().splitlines()[0] if summary.strip() else '')
        return 0
    check, pending = argv[1], argv[2]
    page = argv[argv.index('--page') + 1] if '--page' in argv else None
    attr = argv[argv.index('--attr-only') + 1] if '--attr-only' in argv else None
    try:
        groups = ship_groups(check, page, attr)
    except Exception as ex:  # noqa: BLE001  a stamp error never skips a check: the check runs and no stamp is written
        print('%s: runs (stamp error: %s: %s)' % (check, type(ex).__name__, str(ex)[:160]))
        return 1
    name = check
    json.dump({'check': check, 'name': name, 'groups': groups}, open(pending, 'w', encoding='utf-8'))
    hit, changed = lookup(check, name, groups)
    if hit:
        print('%s (stamp %s: same inputs)' % (hit.get('summary') or check + ': PASS', hit['date']))
        return 0
    print('%s: runs (stamp miss: %s)' % (check, ', '.join(changed)))
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
