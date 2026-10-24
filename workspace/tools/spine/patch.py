#!/usr/bin/env python3
"""patch: one command per step of a patch batch (Jonathan 2026-10-24: "we need to be even more token efficient with the
whole process"; runbook section 8b). The lead runs these and reads only their one-line outputs; details go to files.

  python3 tools/spine/patch.py setup <batch>                  hooks (install, /root copy, tests), start-up context
  python3 tools/spine/patch.py s3 <batch> <folder>...         facts_from_spec + build + copy 10_*.json, verify --mech,
                                                              batch page, gate, render, preflight, vendor, squeeze
  python3 tools/spine/patch.py review <batch> <round> --opus <folder,...> --sonnet <folder,...> [--since-round K]
                                                              packets (--since), one combined lane per model,
                                                              INSTRUCTIONS.md and LANE_PACKET.md; prints launch prompts
  python3 tools/spine/patch.py file <batch> <round>           split each lane's receipt.md into the acc, read and flags
                                                              receipts (repair/migration/spine/reviews/<id>_<part>_rN.md)
                                                              and print each brief's verify state
  python3 tools/spine/patch.py reps <batch> <folder> <receipt> [--only 1,2]   apply PASS-IF replacements to the delta
  python3 tools/spine/patch.py sync <batch> "<message>" <folder>...   copy brief folders, the delta tool and local/<batch>
                                                              into the private clone; commit and push both repos

<folder> is a spine folder relative to repair/migration/ (psych/N3/spine) or a brief id (tools/spine/folder_of.py).
Folders hold the s150e layout: facts_spec_<batch>.json, delta_<batch>.json, baseline_<batch>.html,
baseline_brief_text_<batch>.txt and a build.py that runs repair/migration/spine/<batch>_delta.py.

Combined review (patches only, Jonathan 2026-10-24 "One reviewer per lane (patches)"): one reviewer judges the acc, read
and flags parts of every changed line in its lane and writes one receipt.md with a section per brief and part. Lanes
holding a changed number, dose or next step run as patch-review-opus; the rest as patch-review (Sonnet).
"""
import difflib
import glob
import json
import os
import re
import shutil
import subprocess
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
REPO = os.path.dirname(WS)
PRIV = os.environ.get('AX_PRIVATE', '/home/claude/step2haki-private')
PAGE_LIVE = os.path.join(REPO, 'discriminator-briefs-site', 'index.html')
REVIEWS = os.path.join(WS, 'repair', 'migration', 'spine', 'reviews')
GIT_ID = ['-c', 'user.email=297481111+DrSaturnn@users.noreply.github.com', '-c', 'user.name=DrSaturnn']
PARTS = ('acc', 'read', 'flags')


def sh(cmd, cwd=WS, check=False, timeout=900):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, timeout=timeout)
    if check and r.returncode:
        sys.exit('patch: failed: %s\n%s%s' % (cmd, r.stdout[-2000:], r.stderr[-2000:]))
    return r


def folder(x):
    if '/' in x:
        return os.path.join(WS, 'repair', 'migration', x) if not x.startswith('/') else x
    out = sh([sys.executable, 'tools/spine/folder_of.py', x]).stdout.split()
    if len(out) < 2:
        sys.exit('patch: no folder for %s' % x)
    return os.path.join(WS, out[-1])


def brief_id(f, batch):
    return json.load(open(os.path.join(f, 'delta_%s.json' % batch)))['brief']


def logdir(batch):
    d = os.path.join(WS, 'local', batch)
    os.makedirs(d, exist_ok=True)
    return d


# ---------------------------------------------------------------- setup
def setup(batch):
    sh('bash tools/hooks/install.sh', check=True)
    os.makedirs('/root/.claude', exist_ok=True)
    os.makedirs('/home/claude/.config/axbx/hooks', exist_ok=True)
    shutil.copy('/home/claude/.claude/settings.json', '/root/.claude/settings.json')
    t = sh([sys.executable, 'tools/hooks/test_hooks.py']).stdout.strip().splitlines()[-1:]
    c = sh([sys.executable, 'tools/hooks/usage_ledger.py', '--context']).stdout.strip().splitlines()[-1:]
    print('setup %s: hooks installed (/root/.claude copy); %s; context %s' % (batch, ' '.join(t), ' '.join(c)))


# ---------------------------------------------------------------- s3
def s3(batch, folders):
    L = logdir(batch)
    os.makedirs(os.path.join(WS, 'repair', batch), exist_ok=True)
    res = []
    for x in folders:
        f = folder(x)
        b = brief_id(f, batch)
        spec = os.path.join(f, 'facts_spec_%s.json' % batch)
        if os.path.exists(spec):
            r = sh([sys.executable, 'tools/spine/facts_from_spec.py', spec])
            if r.returncode:
                res.append('%s facts FAIL: %s' % (b, (r.stdout + r.stderr).strip()[-300:]))
                continue
        sh([sys.executable, os.path.join(f, 'build.py')], check=True)
        for j in glob.glob(os.path.join(f, '10_*_spine.json')):
            shutil.copy(j, os.path.join(WS, 'repair', batch))
        r = sh([sys.executable, 'tools/spine/verify.py', f, '--mech'])
        log = os.path.join(L, 'mech_%s.log' % b)
        open(log, 'w').write(r.stdout + r.stderr)
        fixes = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith('FIX')]
        res.append('%s mech %s%s' % (b, 'PASS' if r.returncode == 0 else 'FAIL', (': ' + ' | '.join(fixes))[:400] if fixes else ''))
    page = os.path.join(L, 'index.html')
    out = []
    for name, cmd in (('build', [sys.executable, 'repair/build.py', batch, '--out', page]),
                      ('gate', [sys.executable, 'tools/gate.py', page, '--base', 'HEAD']),
                      ('render', ['node', 'tools/render.js', page]),
                      ('preflight', [sys.executable, 'tools/preflight.py', page, '--base', 'HEAD']),
                      ('vendor', [sys.executable, 'tools/vendor_scan.py', '--page', page]),
                      ('squeeze', [sys.executable, 'tools/spine/squeeze_check.py', page,
                                   ','.join(brief_id(folder(x), batch) for x in folders)])):
        r = sh(cmd)
        open(os.path.join(L, 's3_%s.log' % name), 'w').write(r.stdout + r.stderr)
        lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
        key = {'vendor': 'vendor_scan:', 'preflight': 'preflight:'}.get(name)
        pick = [l for l in lines if key and l.startswith(key)] or lines[-1:]
        out.append('%s %s%s' % (name, 'ok' if r.returncode == 0 else 'EXIT %d' % r.returncode, (': ' + pick[0][:160]) if pick else ''))
        if name == 'build' and r.returncode:
            break
    print('s3 %s\n  ' % batch + '\n  '.join(res + out) + '\n  logs: local/%s/' % batch)


# ---------------------------------------------------------------- review
RULES = """# Combined patch review (acc, read and flags in one pass)

You review only the CHANGED lines of shipped briefs (lines marked "+" in each brief's Changes block), judging each
against the lines around it. Unchanged lines were reviewed and shipped before: do not report them, except where a
changed line now contradicts one (report that on the changed line).

Judge every changed line on three parts and write a verdict for each part per brief:
- acc (accuracy): each new claim is stated by its cited fact (the quote says the claim, not only its topic); board
  answers win over guidelines; every number, age, cutoff and duration in a changed line has a quote that holds it; hedge
  words in the quote (may, often, usually, typically, can) are not dropped where they change the meaning; nothing in the
  line would teach a student a wrong Step 2 answer; masked answers stay masked.
- read (readability and structure): plain clinical wording, no AI prose or figures of speech; the line reads cleanly in
  its table or row; abbreviations are on the allowlist below or spelled out at first use (in the line or a hover); a
  diagnosis with other names shows them (Grep %(aliases)s if unsure); no label, first cell or visible text gives away
  a masked answer; one owner per decision (a changed line must not set a second threshold for a decision another line
  owns); consistent with the brief's structure rules (Clue | Points to | Next move tables hold no questions; Decides-it
  cells lead with the timeline in bold when there is one).
- flags (provenance): every changed line is covered by a new claim whose ids name facts with verbatim quotes; nothing
  in the line goes beyond what the cited quotes and the surrounding shipped lines support; no vendor wording copied
  beyond short clinical phrases.

Abbreviation allowlist (written short without expansion): %(abbrev)s

Severity: HIGH (teaches a wrong answer or unsafe step), MED (misleading, unsupported, or a mask leak), LOW (wording).

Verdicts per part: PASS (no finding needing a change); PASS-IF (only LOWs, each with an exact replacement); FAIL (any
HIGH or MED). A PASS-IF replacement: text only (no <, > or &), the old text copied exactly from one line of the brief
text in LANE_PACKET.md, not crossing a bold, hover or masked span; no changed numbers, no new facts, never a practice
item; at most 40 words of new text; keep hedge words, negations and drug, test and diagnosis names.

## Receipt (one file, written once, at the end)

Write ONE file with the Write tool to the absolute path %(receipt)s. For each brief, in lane order, three sections,
acc then read then flags, each exactly in this shape (the deps and brief-sha lines copied exactly from LANE_PACKET.md):

    === <brief id> <part>
    part: <part>
    deps: <copied>
    brief-sha: <copied>
    Verdict: PASS | PASS-IF | FAIL
    Findings:
    1. <SEVERITY>, <the changed line, quoted briefly>: <what is wrong and the fix>   (or "none")
    Replacements:            (PASS-IF only)
    1. old: {{exact old text}}
       new: {{new text}}
    Checked and fine: <one line naming what you checked>

Call plan: read INSTRUCTIONS.md (this file), read LANE_PACKET.md (one read), at most one Grep per brief when you must
check a source file or table it names, then the single Write. Do not use Glob or list folders. Budget %(budget)d calls.
"""


def text_window(bt, changed, pad=6):
    lines = bt.splitlines()
    keep = set()
    for c in changed:
        for i, l in enumerate(lines):
            if l.strip() and l.strip() == c.strip():
                keep.update(range(max(0, i - pad), min(len(lines), i + pad + 1)))
    out, last = [], -2
    for i in sorted(keep):
        if i != last + 1:
            out.append('...')
        out.append(lines[i])
        last = i
    return '\n'.join(out)


def review(batch, rnd, opus, sonnet, since_round=None):
    root = os.path.join(WS, 'repair', 'efficiency', 'lanes', batch, 'r%d' % rnd)
    pk = os.path.join(WS, 'repair', 'migration', 'spine', 'packets', '%s-r%d' % (batch, rnd))
    page = os.path.join(logdir(batch), 'index.html')
    abbrev = json.load(open(os.path.join(WS, 'repair', 'efficiency', 'ABBREV.json')))
    keys = []
    for k, v in abbrev.items():
        if not k.startswith('_'):
            keys += list(v) if isinstance(v, (dict, list)) else []
    allow = ', '.join(sorted({str(x) for x in keys}))
    prompts = []
    for model, group in (('opus', opus), ('sonnet', sonnet)):
        if not group:
            continue
        lane = os.path.join(root, 'lane_%s' % model)
        if os.path.isdir(lane):
            shutil.rmtree(lane)
        os.makedirs(lane)
        packet = ['# Lane packet: %s round %d (%s)\n' % (batch, rnd, model)]
        for x in group:
            f = folder(x)
            b = brief_id(f, batch)
            since = os.path.join(f, 'baseline_brief_text_%s.txt' % batch)
            if since_round:
                since = os.path.join(WS, 'repair', 'migration', 'spine', 'packets', '%s-r%d' % (batch, since_round),
                                     b, 'acc', 'brief_text.txt')
            out = os.path.join(pk, b)
            if os.path.isdir(out):
                shutil.rmtree(out)
            sh([sys.executable, 'tools/spine/review_packet.py', f, out, '--page', page, '--since', since], check=True)
            ch = open(os.path.join(out, 'acc', 'changes.md')).read()
            bt = open(os.path.join(out, 'acc', 'brief_text.txt')).read()
            # every line the batch changed (against the shipped baseline), so a fact-only fix still shows its line
            base = open(os.path.join(f, 'baseline_brief_text_%s.txt' % batch)).read().splitlines()
            plus = [l[1:] for l in difflib.unified_diff(base, bt.splitlines(), lineterm='', n=0)
                    if l.startswith('+') and not l.startswith('+++')]
            new = json.load(open(os.path.join(f, 'facts_%s.json' % batch)))['facts'] \
                if os.path.exists(os.path.join(f, 'facts_%s.json' % batch)) else []
            fid = {x['id'] for x in new}
            claims = [c for c in json.load(open(os.path.join(f, 'claim_map.json')))['claims']
                      if set(c.get('derived_from', [])) & fid]
            cited = {i for c in claims for i in c.get('derived_from', [])}
            facts = [x for x in json.load(open(os.path.join(f, 'facts.json')))['facts'] if x['id'] in cited]
            packet.append('\n## Brief: %s\n' % b)
            for p in PARTS:
                packet.append('%s receipt lines:\n%s' % (p, open(os.path.join(out, p, 'deps.txt')).read().strip()))
            packet.append('\n### Changes (since the last reviewed text)\n' + ch.split('\n', 3)[-1].strip())
            packet.append('\n### Brief text around every line this batch changed\n' + text_window(bt, plus))
            packet.append('\n### Facts cited by the changed lines (verbatim quotes)\n' + '\n'.join(
                '- %s (%s, %s): "%s"' % (x['id'], x.get('kind'), x.get('title'), x['quote']) for x in facts))
            packet.append('\n### New claims (each changed line\'s claim and its fact ids)\n' + '\n'.join(
                '- %s: %s [%s]' % (c['id'], c['new_text'], ', '.join(c['derived_from'])) for c in claims))
        open(os.path.join(lane, 'LANE_PACKET.md'), 'w').write('\n'.join(packet) + '\n')
        n = len(group)
        budget = min(25, 3 + n + 2)
        open(os.path.join(lane, 'INSTRUCTIONS.md'), 'w').write(RULES % {
            'aliases': os.path.join(WS, 'repair', 'efficiency', 'ALIASES.json'), 'abbrev': allow,
            'receipt': os.path.join(lane, 'receipt.md'), 'budget': budget})
        role = 'patch-review-opus' if model == 'opus' else 'patch-review'
        prompts.append('Role: %s\nPlan step: %s\nLane: %s\nBudget: %d\nRead INSTRUCTIONS.md in your lane first, then '
                       'LANE_PACKET.md; write one receipt.md.' % (role, batch, lane, budget))
    print('\n---\n'.join(prompts))


# ---------------------------------------------------------------- file
def file_receipts(batch, rnd):
    root = os.path.join(WS, 'repair', 'efficiency', 'lanes', batch, 'r%d' % rnd)
    done = []
    for rc in sorted(glob.glob(os.path.join(root, 'lane_*', 'receipt.md'))):
        txt = open(rc).read()
        for m in re.finditer(r'^=== (\S+) (acc|read|flags)\s*\n(.*?)(?=^=== |\Z)', txt, re.S | re.M):
            b, p, body = m.group(1), m.group(2), m.group(3).strip() + '\n'
            if not body.startswith('part: %s' % p):
                sys.exit('patch: %s %s section does not start with "part: %s"' % (b, p, p))
            have = [int(re.search(r'_r(\d+)\.md$', f).group(1)) for f in glob.glob(os.path.join(REVIEWS, '%s_%s_r*.md' % (b, p)))]
            n = max(have or [0]) + 1
            open(os.path.join(REVIEWS, '%s_%s_r%d.md' % (b, p, n)), 'w').write(body)
            v = re.search(r'^Verdict: (\S+)', body, re.M)
            done.append((b, p, n, v.group(1) if v else '?'))
    briefs = sorted({d[0] for d in done})
    for b in briefs:
        print('%s: %s' % (b, ', '.join('%s r%d %s' % (p, n, v) for bb, p, n, v in done if bb == b)))
        f = folder(b)
        r = sh([sys.executable, 'tools/spine/verify.py', f, '--fast'])
        last = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith('verify ')]
        print('  ' + (last[-1][:220] if last else 'verify: no summary'))


# ---------------------------------------------------------------- sync
def sync(batch, msg, folders):
    tail = '\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'
    sess = os.environ.get('AX_SESSION')
    if sess:
        tail += '\nClaude-Session: ' + sess
    for x in folders:
        f = folder(x)
        rel = os.path.relpath(f, WS)
        dst = os.path.join(PRIV, 'local-only', rel)
        os.makedirs(dst, exist_ok=True)
        sh(['cp', '-a', f + '/.', dst + '/'], check=True)
    for extra in ('repair/migration/spine/%s_delta.py' % batch, 'local/%s' % batch,
                  'repair/migration/spine/packets', 'repair/migration/spine/reviews'):
        s = os.path.join(WS, extra)
        if os.path.exists(s):
            d = os.path.join(PRIV, 'local-only', extra)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            if os.path.isdir(s):
                os.makedirs(d, exist_ok=True)
                sh(['cp', '-a', s + '/.', d + '/'], check=True)
            else:
                shutil.copy(s, d)
    for repo in (REPO, PRIV):
        sh(['git', 'add', '-A'], cwd=repo)
        if sh(['git', 'diff', '--cached', '--quiet'], cwd=repo).returncode:
            sh(['git'] + GIT_ID + ['commit', '-q', '-m', msg + tail], cwd=repo, check=True)
        br = sh(['git', 'branch', '--show-current'], cwd=repo).stdout.strip()
        r = sh(['git', 'push', '-q', '-u', 'origin', 'HEAD:refs/heads/' + br], cwd=repo)
        head = sh(['git', 'rev-parse', '--short', 'HEAD'], cwd=repo).stdout.strip()
        print('%s %s %s %s' % (os.path.basename(repo), br, head, 'pushed' if r.returncode == 0 else 'PUSH FAILED: ' + r.stderr[-200:]))


# ---------------------------------------------------------------- reps
def reps(batch, x, receipt, only=None):
    """apply a PASS-IF receipt's approved replacements to the folder's delta_<batch>.json ("new" and the claim text),
    then rebuild; verify replays them, so the other parts' receipts stay current (reps.py edits build.py sources,
    which a delta-built folder does not use)."""
    f = folder(x)
    p = os.path.join(f, 'delta_%s.json' % batch)
    d = json.load(open(p))
    pairs = re.findall(r'old: \{\{(.*?)\}\}\s*new: \{\{(.*?)\}\}', open(receipt).read(), re.S)
    for k, (a, b) in enumerate(pairs, 1):
        if only and k not in only:
            continue
        hits = [c for c in d['changes'] if c['new'].count(a) == 1]
        if len(hits) != 1:
            print('%d miss (%d changes hold it): %s' % (k, len(hits), a))
            continue
        c = hits[0]
        c['new'] = c['new'].replace(a, b, 1)
        if c.get('claim') and a in c['claim']:
            c['claim'] = c['claim'].replace(a, b, 1)
        print('%d applied: %s -> %s' % (k, a, b))
    json.dump(d, open(p, 'w'), indent=1, ensure_ascii=False)
    sh([sys.executable, os.path.join(f, 'build.py')], check=True)
    for j in glob.glob(os.path.join(f, '10_*_spine.json')):
        shutil.copy(j, os.path.join(WS, 'repair', batch))
    r = sh([sys.executable, 'tools/spine/verify.py', f, '--fast'])
    print(([l for l in (r.stdout + r.stderr).splitlines() if l.startswith('verify ')] or ['verify: ?'])[-1][:250])


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    cmd, batch = a[0], a[1]
    if cmd == 'setup':
        setup(batch)
    elif cmd == 's3':
        s3(batch, a[2:])
    elif cmd == 'review':
        rnd = int(a[2])
        opt = {k: v for k, v in zip(a[3::2], a[4::2])}
        sp = lambda k: [x for x in opt.get(k, '').split(',') if x]
        review(batch, rnd, sp('--opus'), sp('--sonnet'), int(opt['--since-round']) if '--since-round' in opt else None)
    elif cmd == 'file':
        file_receipts(batch, int(a[2]))
    elif cmd == 'reps':
        o = [int(i) for i in a[5].split(',')] if len(a) > 5 and a[4] == '--only' else None
        reps(batch, a[2], a[3], o)
    elif cmd == 'sync':
        sync(batch, a[2], a[3:])
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
