"""verify: one command for a spine brief, PASS or a list of fixes (PHASE0_SCRIPTS item 3).

  python3 tools/spine/verify.py <brief dir> [--fast] [--keep]
  python3 tools/spine/verify.py --shipped [--fast]          every spine brief on the page that has a local folder

<brief dir> holds outline.json (rendered by outline_render.py into a temp folder) or a legacy build.py (run in place;
its outputs are local-only build products). Runs, in order:
  render, quote_check (facts.json), shingle_check (claim quotes, vendor files, card text), outline_check,
  claim map complete, tail (the Practice section byte-identical to the live brief after tail_fix; a shipped brief
  must rebuild identical to the page), items carried (every old item id kept, version not lower),
  V1 (an acronym is written out at first use, in the line or a hover) and no em dash,
  and without --fast a preview build in a temp folder: apply the 10_*.json to index.html, then gate, render.js,
  preflight (P1 must be 0), vendor_scan --page and numbers.py --brief.
Then the temp folders are deleted and git must show no tracked change that verify made. Spec drift: once rules sheets exist
(repair/migration/spine/rules/*.md with a "provenance:" line of spec hashes), a mismatch refuses to run.
Passing these checks is MECHANICAL PASS only. READY also needs the newest holistic review of the brief
(repair/migration/spine/reviews/<id>_holistic_rN.md, written by a reader following HOLISTIC_REVIEW.md) to name the
current text by its sha and say "Verdict: PASS": rules met is not the same as a brief that reads as one whole.
Exit 0 READY; 2 mechanical pass, not ready (no review, a stale review, or a review that says FAIL);
1 with one "FIX <check>: ..." line per mechanical problem.
"""
import glob
import hashlib
import html as H
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import pagelib as P  # noqa: E402

PY = sys.executable
# MIGRATION_CONTRACT V1 allowlist, plus Roman numerals and clock times
ACR_OK = {'CRASH', 'ST', 'GI', 'COVID', 'SARS', 'II', 'III', 'HR', 'RR', 'BP', 'IV', 'US', 'NBME',
          'VI', 'VII', 'VIII', 'IX', 'XI', 'XII', 'AM', 'PM'}
BASELINE = os.path.join(HERE, 'verify_baseline.txt')


def load_baseline():
    """known debts of briefs shipped before verify existed: brief | check | token (V1: one acronym) # reason"""
    out = set()
    if os.path.exists(BASELINE):
        for line in open(BASELINE, encoding='utf-8'):
            line = line.split('#')[0].strip()
            if line.count('|') == 2:
                out.add(tuple(x.strip() for x in line.split('|')))
    return out


def sh(args, cwd=WS):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def last(s, n=1):
    return ' | '.join(s.strip().splitlines()[-n:])


class Verify:
    def __init__(self, d, fast, keep):
        self.d, self.fast, self.keep = os.path.abspath(d), fast, keep
        self.fix, self.ok, self.base = [], [], []
        self.baseline = load_baseline()
        self.tmp = tempfile.mkdtemp(prefix='verify-')

    def F(self, check, msg):
        if (getattr(self, 'bid', ''), check, '*') in self.baseline:
            self.base.append('base %s: %s' % (check, msg[:120]))
        else:
            self.fix.append('FIX %s: %s' % (check, msg))

    def G(self, check, msg):
        self.ok.append('ok  %s: %s' % (check, msg))

    # ---- 0. spec drift
    def drift(self):
        sheets = glob.glob(os.path.join(WS, 'repair', 'migration', 'spine', 'rules', '*.md'))
        if not sheets:
            self.G('drift', 'no rules sheets yet (PHASE0 item 8): nothing to compare')
            return True
        bad = []
        for s in sheets:
            m = re.search(r'^provenance:\s*(.+)$', open(s, encoding='utf-8').read(), re.M)
            for pair in (m.group(1).split(',') if m else []):
                path, _, h = pair.strip().partition('@')
                p = os.path.join(WS, path)
                if not os.path.exists(p) or hashlib.sha1(open(p, 'rb').read()).hexdigest()[:10] != h:
                    bad.append('%s (%s)' % (os.path.basename(s), path))
        if bad:
            self.F('drift', 'rules sheet older than its spec: %s; regenerate the sheet' % ', '.join(bad))
            return False
        self.G('drift', '%d rules sheet(s) match their specs' % len(sheets))
        return True

    # ---- 1. render
    def render(self):
        ol = os.path.join(self.d, 'outline.json')
        if os.path.exists(ol):
            import outline_render as OR
            self.o = json.load(open(ol, encoding='utf-8'))
            self.out = os.path.join(self.tmp, 'render')
            os.makedirs(self.out)
            try:
                import io
                import contextlib
                with contextlib.redirect_stdout(io.StringIO()):
                    OR.render(ol, self.out)
            except Exception as ex:  # noqa: BLE001
                self.F('render', '%s: %s' % (type(ex).__name__, str(ex)[:200]))
                return False
            self.mode = 'outline'
        elif os.path.exists(os.path.join(self.d, 'build.py')):
            self.o = None
            rc, out = sh([PY, os.path.join(self.d, 'build.py')])
            if rc:
                self.F('render', 'build.py failed: %s' % last(out, 2))
                return False
            self.out, self.mode = self.d, 'build.py'
        else:
            self.F('render', 'no outline.json or build.py in %s' % self.d)
            return False
        self.brief_html = open(os.path.join(self.out, 'brief.html'), encoding='utf-8').read()
        self.bid = re.match(r'<div class="[^"]*" id="([^"]+)"', self.brief_html).group(1)
        self.cm = json.load(open(os.path.join(self.out, 'claim_map.json'), encoding='utf-8'))
        self.edits = glob.glob(os.path.join(self.out, '10_*_spine.json'))
        self.G('render', '%s via %s' % (self.bid, self.mode))
        return True

    # ---- 2 to 4: sources, copy, outline rules
    def sources(self):
        fj = os.path.join(self.d, 'facts.json')
        if os.path.exists(fj):
            rc, out = sh([PY, os.path.join(HERE, 'quote_check.py'), fj])
            (self.F if rc else self.G)('quote_check', last(out, 3 if rc else 1))
        else:
            self.G('quote_check', 'no facts.json (a brief from the old claim map)')
        bank = re.search(r'<h5 class="[^"]*authored-hdr[^"]*" id="([^"]+)"', self.brief_html)
        args = [PY, os.path.join(HERE, 'shingle_check.py'), os.path.join(self.out, 'brief.html'), os.path.join(self.out, 'claim_map.json')]
        if bank:
            args += ['--bank', bank.group(1)]
        rc, out = sh(args)
        (self.F if rc else self.G)('shingle_check', last(out, 4 if rc else 1))
        if self.mode == 'outline':
            rc, out = sh([PY, os.path.join(HERE, 'outline_check.py'), os.path.join(self.d, 'outline.json'), '--quiet'])
            (self.F if rc else self.G)('outline_check', out if rc else last(out))

    # ---- 5. claim map
    def claims(self):
        rows = self.cm.get('claims', [])
        bad = [r['id'] for r in rows if not r.get('sources') or not all(s.get('source') and s.get('source_says') for s in r['sources'])]
        if not rows:
            self.F('claims', 'claim map has no claims')
        elif bad:
            self.F('claims', '%d claim(s) without a source and quote: %s' % (len(bad), ', '.join(bad[:6])))
        else:
            self.G('claims', '%d claims, each with a source and quote' % len(rows))
        olds = self.cm.get('old_claims', [])
        if not olds:
            self.F('claims', 'no old_claims: every section of the old brief needs a disposition')

    # ---- 6, 7: tail and items against the live page
    def live(self):
        page = P.read_page(os.path.join(WS, 'index.html'))
        b = P.brief_by_id(page, self.bid)
        live = page[b.start:b.end]
        new = self.brief_html
        hdr = re.search(r'<h5 class="[^"]*authored-hdr', new)
        if 'data-spine="2"' in live[:400]:
            if new.strip() == live.strip():
                self.G('tail', 'shipped brief rebuilds identical to the page')
            else:
                a, z = 0, 0
                while a < min(len(new), len(live)) and new[a] == live[a]:
                    a += 1
                self.F('tail', 'shipped brief does not rebuild identical to the page (first difference at char %d: "%s" vs "%s")'
                       % (a, new[a:a + 40].replace('\n', ' '), live[a:a + 40].replace('\n', ' ')))
        elif hdr:
            t_new = new[hdr.start():]
            lh = re.search(r'<h5 class="[^"]*authored-hdr', live)
            t_old = live[lh.start():] if lh else ''
            fixes = (self.o or {}).get('tail_fix', [])
            if self.o and fixes:
                import outline_render as OR
                R = OR.Renderer(self.o, self.d)
                for old, nw in fixes:
                    t_old = t_old.replace(old, R.r(nw), 1)
            if t_new.strip() == t_old.strip():
                self.G('tail', 'Practice section identical to the live brief%s' % (' after %d tail_fix edit(s)' % len(fixes) if fixes else ''))
            else:
                self.F('tail', 'Practice section differs from the live brief beyond tail_fix; carry it verbatim')
        old_items = dict(re.findall(r'data-item-id="([^"]+)"[^>]*?data-item-version="(\d+)"', live))
        new_items = dict(re.findall(r'data-item-id="([^"]+)"[^>]*?data-item-version="(\d+)"', new))
        lost = [i for i in old_items if i not in new_items]
        down = [i for i in old_items if i in new_items and int(new_items[i]) < int(old_items[i])]
        if lost or down:
            self.F('items', 'lost %s; version lowered %s' % (lost[:5], down[:5]))
        else:
            self.G('items', '%d item(s) carried, versions kept' % len(old_items))

    # ---- 8. V1 and em dash
    def v1(self):
        hdr = re.search(r'<h5 class="[^"]*authored-hdr', self.brief_html)
        above = self.brief_html[:hdr.start()] if hdr else self.brief_html
        vis = re.sub(r'<(script|style)\b.*?</\1>', ' ', above, flags=re.S)
        mn = ' '.join(re.findall(r'<ul class="[^"]*mnem[^"]*".*?</ul>', vis, flags=re.S))
        mn_ids = {x for v in re.findall(r'(?:id|data-scale)="([^"]+)"', above) for x in re.split(r'[-_]', v.lower())}
        mn_tokens = set(re.findall(r'\b[A-Z]{2,}\b', H.unescape(re.sub(r'<[^>]+>', ' ', mn))))   # a mnemonic's own name
        text = H.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<ul class="[^"]*mnem[^"]*".*?</ul>', ' ', vis, flags=re.S)))
        if '—' in text or '&mdash;' in above:
            self.F('emdash', 'em dash above the Practice header: use a spaced en dash or a colon')
        hover = H.unescape(' '.join(re.findall(r'data-(?:body|title)="([^"]*)"', above)))
        everything = text + ' ' + hover
        seen, bad = set(), []
        for m in re.finditer(r'\b([A-Z][A-Z0-9]{1,5})s?\b', text):
            a = m.group(1)
            if a in seen or a in ACR_OK or a in mn_tokens or a.lower() in mn_ids or not re.search(r'[A-Z].*[A-Z]', a) \
                    or text[max(0, m.start() - 1):m.start()] == '*':          # a genotype (PI*ZZ)
                continue
            seen.add(a)
            if re.search(r'\(%s\b|\b%s\)|, %s[;),]|\b%s\s*\(' % (a, a, a, a), everything):   # (ACR), ACR (...), (long name, ACR)
                continue
            words = [w for w in re.findall(r'[A-Za-z]+', everything)]
            initials = ''.join(w[0] for w in words).upper()
            letters = re.sub(r'[0-9]', '', a)
            if len(letters) >= 2 and letters in initials:      # written out somewhere as its initials ("chronic obstructive...")
                continue
            bad.append(a)
        known = [a for a in bad if (self.bid, 'V1', a) in self.baseline]
        bad = [a for a in bad if a not in known]
        if known:
            self.base.append('base V1: %s (baseline, shipped before verify)' % ', '.join(known))
        if bad:
            self.F('V1', 'acronym(s) never written out above the Practice header: %s' % ', '.join(bad[:12]))
        else:
            self.G('V1', '%d acronym(s), each written out' % len(seen))

    # ---- 9. preview build and page checks
    def preview(self):
        sys.path.insert(0, os.path.join(WS, 'tools'))
        import apply_edits
        page = P.read_page(os.path.join(WS, 'index.html'))
        new = page
        try:
            for e in self.edits:
                new, _ = apply_edits.apply(new, json.load(open(e, encoding='utf-8')))
        except Exception as ex:  # noqa: BLE001
            self.F('build', '%s: %s' % (type(ex).__name__, str(ex)[:200]))
            return
        pv = os.path.join(self.tmp, 'preview.html')
        P.write_page(pv, new)
        self.G('build', 'preview %+d chars' % (len(new) - len(page)))
        for name, args, okf in [
                ('gate', [PY, 'tools/gate.py', pv], lambda rc, o: rc == 0),
                ('render.js', ['node', 'tools/render.js', pv], lambda rc, o: rc == 0),
                ('preflight', [PY, 'tools/preflight.py', pv, '--base', 'HEAD'], lambda rc, o: re.search(r'\bP1 0\b', o) is not None),
                ('vendor_scan', [PY, 'tools/vendor_scan.py', '--page', pv], lambda rc, o: rc == 0 and ' 0 flagged' in o),
                ('numbers', [PY, os.path.join(HERE, 'numbers.py'), pv, '--brief', self.bid], lambda rc, o: rc == 0)]:
            rc, out = sh(args)
            if okf(rc, out):
                self.G(name, last(out.splitlines()[0] if name in ('vendor_scan', 'numbers') else out))
            else:
                self.F(name, '\n      '.join(out.splitlines()[-6:]))

    def run(self):
        before = sh(['git', 'status', '--porcelain', '--untracked-files=no'])[1]
        try:
            if not self.drift():
                return self
            if self.render():
                self.sources()
                self.claims()
                self.live()
                self.v1()
                if not self.fast:
                    self.preview()
        finally:
            if not self.keep:
                shutil.rmtree(self.tmp, ignore_errors=True)
        rc, out = sh(['git', 'status', '--porcelain', '--untracked-files=no'])
        if out.strip() != before.strip():               # only what verify itself changed
            self.F('git', 'verify changed tracked files: %s' % ' '.join(sorted(set(out.split()) - set(before.split()))[:8]))
        self.holistic()
        return self

    # ---- 10. the whole-picture gate: mechanical checks are necessary, never sufficient
    def holistic(self):
        """READY needs the newest holistic review (HOLISTIC_REVIEW.md) to be of THIS brief text and to say PASS"""
        self.ready = 'no review'
        bid = getattr(self, 'bid', None)
        if not bid or not getattr(self, 'brief_html', ''):
            return
        page = P.read_page(os.path.join(WS, 'index.html'))
        b = P.brief_by_id(page, bid)
        shas = {hashlib.sha1(self.brief_html.encode()).hexdigest()[:10]}
        if b:
            shas.add(hashlib.sha1(page[b.start:b.end].encode()).hexdigest()[:10])
        files = sorted(glob.glob(os.path.join(WS, 'repair', 'migration', 'spine', 'reviews', '%s_holistic_r*.md' % bid)),
                       key=lambda f: int(re.search(r'_r(\d+)\.md$', f).group(1)) if re.search(r'_r(\d+)\.md$', f) else 0)
        if not files:
            self.ready = 'no holistic review yet (repair/migration/spine/HOLISTIC_REVIEW.md)'
            return
        txt = open(files[-1], encoding='utf-8').read()
        sha = re.search(r'brief-sha:\s*([0-9a-f]{10})', txt)
        verdict = re.search(r'Verdict:\s*(PASS|FAIL)', txt)
        name = os.path.basename(files[-1])
        if not sha or sha.group(1) not in shas:
            self.ready = '%s reviewed an older text of the brief: review again' % name
        elif not verdict or verdict.group(1) != 'PASS':
            self.ready = '%s says FAIL: fix its findings, then review again' % name
        else:
            self.ready = 'READY'


def spine_dirs():
    """local folders of spine briefs on the page, by the brief id their build writes"""
    page = P.read_page(os.path.join(WS, 'index.html'))
    live = set(re.findall(r'id="([^"]+)" data-entry="[^"]*" data-lens="[^"]*" data-spine="2"', page))
    out = {}
    for d in sorted(glob.glob(os.path.join(WS, 'repair', 'migration', '*', '*', 'spine'))):
        for e in glob.glob(os.path.join(d, '10_*_spine.json')):
            bid = json.load(open(e, encoding='utf-8'))['edits'][0]['brief']
            if bid in live:
                out[bid] = d
    return out, live


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    fast, keep = '--fast' in argv, '--keep' in argv
    if '--shipped' in argv:
        dirs, live = spine_dirs()
        missing = sorted(live - set(dirs))
        bad, nb, ready = 0, 0, 0
        for bid, d in sorted(dirs.items()):
            v = Verify(d, fast, keep).run()
            state = 'FAIL' if v.fix else ('READY' if v.ready == 'READY' else 'MECH')
            print('%-5s %-22s %s%s' % (state, bid, os.path.relpath(d, WS), '' if state != 'MECH' else '  (' + v.ready + ')'))
            for f in v.fix:
                print('     ' + f)
            nb += len(v.base)
            ready += v.ready == 'READY'
            bad += bool(v.fix)
        print('verify --shipped: %d brief(s), %d failing the mechanical checks, %d READY (holistic review PASS on the '
              'current text), %d baseline debt line(s) (tools/spine/verify_baseline.txt)%s' % (
                  len(dirs), bad, ready, nb, ('; no local folder: ' + ', '.join(missing)) if missing else ''))
        return 1 if bad else 0
    v = Verify(argv[0], fast, keep).run()
    for line in v.ok + v.base + v.fix:
        print(line)
    if v.fix:
        print('verify %s: FAIL (%d fix(es))' % (getattr(v, 'bid', argv[0]), len(v.fix)))
        return 1
    if v.ready != 'READY':
        print('verify %s: MECHANICAL PASS, NOT READY: %s' % (v.bid, v.ready))
        return 2
    print('verify %s: READY (mechanical checks pass and the current holistic review says PASS)' % v.bid)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
