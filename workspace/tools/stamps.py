#!/usr/bin/env python3
"""stamps.py: input-hash stamps for the ship checks (s171b; D-20261109-4, 2026-11-09: "no reason to run things
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

Checks (ship.sh): rules-migrate, rules-gate, rules-stamps, gate, render, vendor-scan, vendor-orphan; verify (one stamp
per spine folder, written by verify.py on READY); ui_gate tests (parity, a11y, perf, twopane, tour, tourfit; theme keeps
style_surface's record). Each group holds only what its check opens (spec() below): the code closure of the
check's entry scripts, its data and documents, its page, folder or tree. tools/test_stamps.py (ship step rules-stamps)
traces each check and fails on a file opened outside its groups. Files opened and left out on purpose are listed in
EXEMPT with the reason.
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
# AX_STAMPS_DIR is honored only beside AX_HOOK_STATE (test_hooks.py), a variable callgate refuses in the lead's commands
STORE = (os.environ.get('AX_STAMPS_DIR') if os.environ.get('AX_HOOK_STATE') else None) or os.path.join(WS, 'local', 'stamps')
KEEP = 5
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


# ---- what each check reads. A group hashes only files its check opens: the code it runs (the static closure
# of its entry scripts: imports, required modules and script paths named in the code), the data and documents named
# for it below, and its page, folder or tree. tools/test_stamps.py traces a real run of each check and fails when it
# opens a file outside its groups, so a new read is added here before a stamp can go stale on it.
CODE_DIRS = ('tools', 'tools/spine', 'tools/typec', 'tools/hooks', 'tools/githooks', 'repair', 'repair/migration/spine',
             'repair/changelog')
ENTRY = {'rules-migrate': ['tools/test_migrate_check.py'], 'rules-gate': ['tools/test_gate_rules.py'],
         'gate': ['tools/gate.py'], 'verify': ['tools/spine/verify.py'], 'render': ['tools/render.js'],
         'vendor-scan': ['tools/vendor_scan.py'], 'vendor-orphan': ['tools/vendor_scan.py']}
_IMP = re.compile(r'^[ \t]*(?:from[ \t]+([\w.]+)[ \t]+import[ \t]+([\w., \t]+)|import[ \t]+([\w., \t]+))', re.M)
_LIT = re.compile(r'''['"]([\w./-]*\w\.(?:py|js|mjs|sh))['"]''')
_REQ = re.compile(r'''require\(\s*['"](\.{1,2}/[^'"]+)['"]\s*\)''')
_closure = {}


def _deps(rel):
    """the code files one file names: imported modules, required scripts, script paths in string literals"""
    p = os.path.join(WS, rel)
    try:
        src = open(p, encoding='utf-8', errors='replace').read()
    except OSError:
        return set()
    here = os.path.dirname(rel)
    dirs = [here] + [d for d in CODE_DIRS if d != here]
    out = set()

    def add(cands):
        for c in cands:
            c = os.path.normpath(c).replace(os.sep, '/')
            if not c.startswith('..') and os.path.isfile(os.path.join(WS, c)):
                out.add(c)
    if rel.endswith('.py'):
        for a, b, c in _IMP.findall(src):
            names = set()
            for chunk in (a, b, c):
                for n in re.split(r'[,\s]+', chunk or ''):
                    if n and n != 'as':
                        names.update((n.split('.')[0], n.split('.')[-1], n.replace('.', '/')))
            add('%s/%s.py' % (d, n) for d in dirs for n in names)
    for r in _REQ.findall(src):
        add(os.path.join(here, r + x) for x in ('', '.js', '.json'))
    for lit in _LIT.findall(src):
        add([lit, os.path.join(here, lit)] + ['%s/%s' % (d, os.path.basename(lit)) for d in dirs])
    return out


def closure(entries):
    """every code file a run of the entry scripts can load (a superset: a path named only in a message counts)"""
    key = tuple(sorted(entries))
    if key not in _closure:
        seen, todo = set(), [e for e in entries if os.path.isfile(os.path.join(WS, e))]
        while todo:
            r = todo.pop()
            if r not in seen:
                seen.add(r)
                todo += sorted(_deps(r) - seen)
        _closure[key] = sorted(seen)
    return _closure[key]


def _versions():
    return 'node %s | python %s' % (_run(['node', '--version']), sys.version.split()[0])


UI_ONLY = {'tools/spine/perf_baseline.json', 'tools/spine/a11y_baseline.json'}
# records the tools write as they run (budgets, audit and context records, the State archive); no check reads them as
# rules, and counting them would void every stamp at the next theme pass or State move
RECORDS = ('WAVE.json', 'style_audits.json', 'context_baseline.json', 'STATE_ARCHIVE.md', 'RESULTS.md')
TOOL_DATA = ['tools/**/*.json', 'tools/**/*.txt', 'tools/**/*.csv', 'tools/**/*.md', 'tools/tests/**/*',
             'tools/fixtures/**/*']
RULES = ['repair/efficiency/*.json', 'repair/efficiency/*.md', 'repair/migration/spine/rules/*.md']
GATE_REPO = ['repair/migration/**/spine/06_*_retire.json', 'repair/archive/**/*', 'repair/nbme/coverage.csv']
BASE_PAGE = ['repair/migration/**/spine/05_*_new.json', 'repair/migration/**/spine/06_*_retire.json']
# the private documents each check opens. The gate's doc-lint reads the digest; verify runs the gate with
# --no-doc-lint (the documents are judged by the ship gate, the launch gate, launch.py, resume.py and docstate.py), so
# a decision line written between S8 and the ship leaves every verify stamp in place.
GATE_DOCS = ['DECISIONS_DIGEST.md', 'STANDING_DIRECTIONS.md', 'BATCH_RUNBOOK.md', 'PLAN_TEMPLATE.md', 'ui/*.md']
DOCS = {'gate': GATE_DOCS, 'rules-gate': GATE_DOCS, 'verify': ['STANDING_DIRECTIONS.md', 'ui/UI_MAP.md']}
# files a check opens that stay out of its key on purpose, each with its reason (the trace test allows only these)
EXEMPT = {
    'gate': [('docs:RESUME.md', 'state file: the state checks rerun at every State rewrite (docstate, resume, launch)'),
             ('docs:STEP2HAKI_HANDOFF.md', 'state file: as RESUME')],
    'rules-gate': [('docs:*', 'the self-test copies docs/ whole into its fixture; the files its cases judge are in '
                              'the docs group')],
    'verify': [('repair/efficiency/WAVE.json', 'only the wave id is read (basepage); the id is in the page group'),
               ('repair/migration/*/spine/10_*_spine.json', 'other folders: read only for the brief id (ids group)'),
               ('repair/migration/*/*/spine/10_*_spine.json', 'as above, hub folders'),
               ('tree:changed', 'changed and untracked files of the working tree, read by the preview vendor_scan; '
                                'ship.sh runs vendor-scan and vendor-orphan on that tree at every ship whose tree changed')],
}


def _data(check):
    tool = [r for r in files(WS, TOOL_DATA, exclude=UI_ONLY) if not r.startswith(('tools/plugin/', 'tools/hooks/'))]
    tool += files(WS, ['tools/hooks/agents/*.md', 'tools/plugin/**/agents/*.md'])
    if check == 'rules-migrate':
        return files(WS, ['tools/tests/**/*'])
    return sorted(set(tool))


def head_page():
    return _run(['git', 'rev-parse', 'HEAD:./index.html']) or '-'


def page_hash(p):
    return fhash(os.path.abspath(p))[:16] if p else '-'


def _wave():
    try:
        return json.load(open(os.path.join(WS, 'repair', 'efficiency', 'WAVE.json'), encoding='utf-8')).get('wave') or ''
    except (OSError, ValueError, AttributeError):
        return ''


def _ids():
    """(path, brief id) of every spine folder's edit file: verify maps brief ids to folders through them"""
    out = []
    for e in files(WS, ['repair/migration/*/*/spine/10_*_spine.json', 'repair/migration/*/*/*/spine/10_*_spine.json']):
        try:
            out.append('%s=%s' % (e, json.load(open(os.path.join(WS, e), encoding='utf-8'))['edits'][0]['brief']))
        except (OSError, ValueError, KeyError, IndexError):
            out.append(e + '=?')
    return '\n'.join(out)


def _repo():
    """everything vendor_scan reads: the tracked files (index blobs and working-tree changes) and untracked files git
    does not ignore"""
    idx = _run(['git', 'ls-files', '-s'])
    top = _run(['git', 'rev-parse', '--show-toplevel'])
    changed = _run(['git', 'ls-files', '-m', '--full-name']).splitlines() + \
        _run(['git', 'ls-files', '--others', '--exclude-standard', '--full-name']).splitlines()
    return top, sorted(set(changed)), idx


def brief_id(folder):
    for e in sorted(glob.glob(os.path.join(folder, '10_*_spine.json'))):
        try:
            return json.load(open(e, encoding='utf-8'))['edits'][0]['brief']
        except (OSError, ValueError, KeyError, IndexError):
            pass
    return None


def folder_name(folder):
    """a spine folder's stamp name: its path under the workspace"""
    return os.path.relpath(os.path.abspath(folder), WS).replace(os.sep, '/')


def spec(check, page=None, attr_only=None, folder=None):
    """{group: (root, [file under root, ...], extra text)}: what the check's key covers. hashed() turns it into the
    stored groups; covered() lists the files for the trace test."""
    d = _docs()
    code = lambda extra=(): (WS, closure(ENTRY[check] + list(extra)) + ['package-lock.json', 'package.json'], _versions())
    docs = (d, files(d, DOCS[check]), '') if d and check in DOCS else (WS, [], 'none')
    rules = (WS, files(WS, RULES, exclude={'repair/efficiency/' + f for f in RECORDS}), '')
    site = (WS, files(WS, ['site/**/*']), '')
    sources = (WS, files(WS, ['repair/sources/**/*']), '')
    pg = os.path.abspath(page) if page else None
    one = lambda p, extra='': ('/', [p.lstrip('/')] if p else [], extra)
    if check == 'rules-migrate':
        return {'tools': code(), 'tool-data': (WS, _data(check), '')}
    if check == 'rules-gate':
        # the gate's code and rule files (OPEN_WORK "Ship time"); the page to ship is gated by the gate check itself
        return {'tools': code(), 'tool-data': (WS, _data(check), ''), 'docs': docs, 'rules': rules, 'site': site,
                'gate-repo': (WS, files(WS, GATE_REPO), '')}
    if check == 'gate':
        base = ('attr-only ' + _run(['git', 'rev-parse', '%s:./index.html' % attr_only])) if attr_only else head_page()
        return {'page': one(pg), 'search-index': one(os.path.join(os.path.dirname(pg), 'search.json') if pg else None),
                'base': (WS, [], base), 'tools': code(), 'tool-data': (WS, _data(check), ''), 'docs': docs,
                'rules': rules, 'site': site, 'gate-repo': (WS, files(WS, GATE_REPO), '')}
    if check == 'render':
        return {'page': one(pg), 'tools': (WS, ['tools/render.js', 'tools/render_allowlist.txt', 'package-lock.json',
                                                'package.json'], _run(['node', '--version']))}
    if check in ('vendor-scan', 'vendor-orphan'):
        top, changed, idx = _repo()
        g = {'repo': (top, changed, idx), 'sources': sources,
             'tools': (WS, closure(ENTRY[check]) + ['tools/local_only.txt'], '')}
        if check == 'vendor-orphan':
            g['page'] = one(pg)
        return g
    if check == 'verify':
        # verify.py on one spine folder: the folder (logs it writes there left out), its receipts, the page it builds
        # on, the rules, the documents, the site layer, the code (with the folder's build.py and the delta tool it
        # imports), the tool data and the sources. Left out on purpose: the tracked tree its preview vendor_scan also
        # reads; ship.sh runs vendor-scan and vendor-orphan on that tree at every ship whose tree changed.
        folder = os.path.abspath(folder)
        bid = brief_id(folder)
        w = _wave()
        base = files(WS, BASE_PAGE) + (files(WS, ['repair/%s/0[0-4]_*.json' % w]) if w else [])
        fb = os.path.relpath(os.path.join(folder, 'build.py'), WS).replace(os.sep, '/')
        return {'folder': (folder, [r for r in files(folder, ['**/*']) if not r.endswith('.log')], ''),
                'receipts': (WS, files(WS, ['repair/migration/spine/reviews/%s_*.md' % bid]) if bid else [], bid or '?'),
                'page': (WS, ['index.html'] + base, 'wave %s | HEAD:index.html %s' % (w, head_page())),
                'ids': (WS, [], _ids()), 'rules': rules, 'docs': docs, 'site': site,
                'tools': code([fb] if not fb.startswith('..') else []), 'tool-data': (WS, _data(check), ''),
                'gate-repo': (WS, files(WS, GATE_REPO), ''), 'sources': sources}
    if check == 'rules-stamps':
        # the trace test itself: rerun when any tool, tool data file or delta tool changed
        allc = [r for r in files(WS, ['tools/**/*.py', 'tools/**/*.js', 'tools/**/*.sh', 'repair/build.py',
                                      'repair/migration/spine/*.py']) if not r.startswith('tools/plugin/')]
        return {'tools': (WS, allc + ['package-lock.json', 'package.json'], _versions()),
                'tool-data': (WS, _data(check), '')}
    raise SystemExit('stamps: unknown check %s' % check)


def hashed(sp):
    return {g: ghash(root, rels, extra) for g, (root, rels, extra) in sp.items()}


def covered(check, sp):
    """absolute paths the key covers (the trace test compares a run's opens against this)"""
    out = {os.path.realpath(os.path.join(root, r)) for root, rels, _ in sp.values() for r in rels}
    if 'repo' in sp:   # the index hash covers every tracked file
        top = sp['repo'][0]
        out |= {os.path.realpath(os.path.join(top, r)) for r in _run(['git', 'ls-files', '--full-name', ':/']).splitlines()}
    return out


def verify_groups(folder):
    return hashed(spec('verify', folder=folder))


def ship_groups(check, page=None, attr_only=None):
    return hashed(spec(check, page, attr_only))



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
