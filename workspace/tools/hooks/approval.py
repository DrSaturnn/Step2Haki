#!/usr/bin/env python3
"""G-APPROVE, made mechanical (Jonathan 2026-10-12): ship.sh refuses a batch unless an approval record exists, and the
record is written only after Jonathan says "ship" in reply to the screenshots.

  approval.py present sNN SHOT [SHOT ...]   lead: after the preview and screenshots are built, register them (pending)
  approval.py hook                          UserPromptSubmit hook: Jonathan's message; "ship" approves the pending batch
  approval.py check sNN PAGE                ship.sh: PAGE is the batch built by repair/build.py; exit 0 only if approved
  approval.py status                        print pending and approved batches

The manifest binds the batch files, its changelog entry, the built page and every screenshot by sha256. The hook writes
approvals/sNN.json only when a pending manifest exists and the message says ship (not "don't ship" or a question), and
names that batch when more than one is pending. Any later change to the batch, the changelog entry or the built page
breaks the match, so ship.sh refuses and the batch must be presented again. The lead cannot write approvals/ (callgate).
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def fsha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def batch_sha(b):
    files = sorted(glob.glob(os.path.join(C.WS, 'repair', b, '*.json')))
    if not files:
        sys.exit('approval: repair/%s has no batch files' % b)
    h = hashlib.sha256()
    for f in files:
        h.update(os.path.basename(f).encode() + b'\0' + open(f, 'rb').read() + b'\0')
    return h.hexdigest(), [os.path.basename(f) for f in files]


def log_entry(b):
    """the batch's changelog entry, as its JSON (repair/changelog/axlog.py prints the whole log)"""
    if os.environ.get('AX_TEST_LOG'):
        return os.environ['AX_TEST_LOG']          # test_hooks.py only
    out = subprocess.run([sys.executable, os.path.join(C.WS, 'repair', 'changelog', 'axlog.py')], capture_output=True,
                         text=True).stdout
    try:
        rows = json.loads(out)
    except ValueError:
        return None
    n = int(re.sub(r'\D', '', b) or 0)
    hit = [r for r in rows if isinstance(r, dict) and r.get('v') == n]
    return json.dumps(hit[0], sort_keys=True) if hit else None


def build(b):
    t = tempfile.mkdtemp(prefix='approve-')
    out = os.path.join(t, 'index.html')
    r = subprocess.run([sys.executable, os.path.join(C.WS, 'repair', 'build.py'), b, '--out', out], capture_output=True,
                       text=True)
    if r.returncode:
        sys.exit('approval: build failed: ' + (r.stdout + r.stderr).strip())
    return out


def present(b, shots):
    if not shots:
        sys.exit('approval present: name the screenshot files Jonathan will review')
    missing = [s for s in shots if not os.path.isfile(s)]
    if missing:
        sys.exit('approval present: missing screenshot(s): %s' % ', '.join(missing))
    entry = log_entry(b)
    if not entry:
        sys.exit('approval present: add the changelog entry for %s first (repair/changelog/axlog.py); it is part of '
                 'what Jonathan approves' % b)
    bs, files = batch_sha(b)
    page = build(b)
    m = {'batch': b, 'presented_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'presented_epoch': time.time(),
         'batch_sha': bs, 'files': files, 'log_sha': C.sha(entry), 'page_sha': fsha(page),
         'shots': {os.path.abspath(s): fsha(s) for s in shots}, 'status': 'pending'}
    json.dump(m, open(C.state('present', '%s.json' % b), 'w', encoding='utf-8'), indent=1)
    old = C.state('approvals', '%s.json' % b)
    if os.path.exists(old):
        os.remove(old)              # a new presentation voids any earlier approval of this batch
    print('approval: %s presented (%d files, %d screenshot(s), page %s). Send the screenshots; ship.sh will run only '
          'after Jonathan replies "ship".' % (b, len(files), len(shots), m['page_sha'][:12]))
    return 0


SHIP = re.compile(r'(?<![\w-])ship(?![\w-])', re.I)
NEG = re.compile(r"\b(don'?t|do not|never|not yet|hold|wait)\b[^.?!\n]{0,30}\bship\b|\bship\b[^.?!\n]{0,15}\?",
                 re.I)


def hook():
    d = json.load(sys.stdin)
    prompt = d.get('prompt') or ''
    C.log_event('prompt-seen', says_ship=bool(SHIP.search(prompt)))   # proves the hook fires; the text is not kept
    pend = []
    for p in glob.glob(os.path.join(C.STATE, 'present', '*.json')):
        m = json.load(open(p, encoding='utf-8'))
        if m.get('status') == 'pending':
            pend.append((p, m))
    if not pend or not SHIP.search(prompt):
        return 0
    if NEG.search(prompt):
        print('[approval hook] Jonathan\'s message mentions ship in a hold, condition or question; no approval recorded.')
        C.log_event('approval-skip', why='negated or conditional', quote=prompt[:300])
        return 0
    named = set(re.findall(r'\bs(\d+[a-z]?)\b', prompt))
    if named:
        pend = [(p, m) for p, m in pend if m['batch'][1:] in named]
    if len(pend) != 1:
        print('[approval hook] "ship" seen, but %d batches are pending and the message does not name one; no approval '
              'recorded. Ask Jonathan which batch.' % len(pend))
        return 0
    p, m = pend[0]
    rec = dict(m, status='approved', approved_at=time.strftime('%Y-%m-%dT%H:%M:%S'), approved_epoch=time.time(),
               quote=prompt[:500], session_id=d.get('session_id'), prompt_id=d.get('prompt_id'))
    json.dump(rec, open(C.state('approvals', '%s.json' % m['batch']), 'w', encoding='utf-8'), indent=1)
    m['status'] = 'approved'
    json.dump(m, open(p, 'w', encoding='utf-8'), indent=1)
    C.log_event('approved', batch=m['batch'], quote=prompt[:300])
    print('[approval hook] Approval recorded for %s from Jonathan\'s message (page %s).' % (m['batch'], m['page_sha'][:12]))
    return 0


def check(b, page):
    p = os.path.join(C.STATE, 'approvals', '%s.json' % b)
    if not os.path.exists(p):
        print('approval: no approval record for %s. Present it (approval.py present %s SHOTS), send the screenshots, and '
              'wait for Jonathan to reply "ship".' % (b, b))
        return 1
    a = json.load(open(p, encoding='utf-8'))
    bs, _ = batch_sha(b)
    entry = log_entry(b)
    bad = []
    if a.get('batch_sha') != bs:
        bad.append('the batch files changed after approval')
    if not entry or a.get('log_sha') != C.sha(entry):
        bad.append('the changelog entry changed after approval')
    if a.get('page_sha') != fsha(page):
        bad.append('the built page differs from the approved preview')
    if not a.get('approved_epoch') or a['approved_epoch'] <= a.get('presented_epoch', 0):
        bad.append('the approval does not follow the presentation')
    if bad:
        print('approval: %s is not approved as built: %s. Present it again.' % (b, '; '.join(bad)))
        return 1
    print('approval: %s approved %s ("%s")' % (b, a['approved_at'], re.sub(r'\s+', ' ', a.get('quote', ''))[:80]))
    return 0


def status():
    for kind in ('present', 'approvals'):
        for p in sorted(glob.glob(os.path.join(C.STATE, kind, '*.json'))):
            m = json.load(open(p, encoding='utf-8'))
            print('%-9s %-6s %-8s presented %s%s' % (kind, m['batch'], m.get('status'), m.get('presented_at'),
                                                    ' approved %s' % m['approved_at'] if m.get('approved_at') else ''))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    if a[0] == 'present':
        sys.exit(present(a[1], a[2:]))
    if a[0] == 'hook':
        sys.exit(hook())
    if a[0] == 'check':
        sys.exit(check(a[1], a[2]))
    if a[0] == 'status':
        sys.exit(status())
    sys.exit('approval: unknown command %s' % a[0])
