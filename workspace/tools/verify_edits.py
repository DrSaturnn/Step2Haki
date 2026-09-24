#!/usr/bin/env python3
"""verify_edits.py: the one check a worker runs before finishing.

  python3 tools/verify_edits.py <edits.json> [page] [--nids <source.md>] [--voice] [--no-render]

1. schema-checks every op; 2. applies the edits to a scratch copy (every anchor must be
unique in its brief); 3. runs tools/gate.py on the copy with the original page as base
(never delete, ids immutable, version bumped on key/distractor change); 4. runs
tools/render.js on the copy (0 malformed MCQs, no dead anchors, no JS errors) and checks
the MCQ count equals the static item count; 5. flags new or edited items that
near-duplicate an existing item; 6. with --nids <source.md>, checks every data-nid token the
edits add (on the brief div or any item) is a question nid listed on a heading line of that
source ("(nid X)" / "(nids X Y)") and is not already on a different brief. Prints each failure with its fix. Exit 0 = clean.
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
from pagelib import briefs, items, read_page, text, write_page  # noqa: E402
import apply_edits  # noqa: E402
import pagelib  # noqa: E402

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


def source_nids(md):
    """Question nids: digit runs after 'nid'/'nids' on markdown heading lines."""
    out = set()
    for line in md.split('\n'):
        if not line.startswith('#'):
            continue
        for m in re.finditer(r'\bnids?\b[\s:=#]*([^)\n]*)', line, re.I):
            out.update(re.findall(r'\b\d{8,}\b', m.group(1)))
    return out


def nids_by_brief(html):
    """brief id -> set of data-nid tokens on the brief div and its items."""
    out = {}
    for b in briefs(html):
        toks = set((b.attrs.get('data-nid') or '').split())
        for v in re.findall(r'<li\b[^>]*\bdata-nid="([^"]*)"', b.inner):
            toks.update(v.split())
        out[b.id] = toks
    return out


def nid_check(before, after, src_path):
    """Returns (n_added, [failure messages])."""
    qn = source_nids(open(src_path, encoding='utf-8').read())
    old, new = nids_by_brief(before), nids_by_brief(after)
    owners = {}
    for bid, toks in old.items():
        for t in toks:
            owners.setdefault(t, set()).add(bid)
    fails, n = [], 0
    for bid, toks in new.items():
        for t in sorted(toks - old.get(bid, set())):
            n += 1
            if t not in qn:
                fails.append('nid %s added to %s is not a question nid in %s\n      fix: use only the nids on the '
                             'source question heading; drop typos and nids from other questions' % (t, bid, os.path.basename(src_path)))
            elsewhere = sorted(owners.get(t, set()) - {bid})
            if elsewhere:
                fails.append('nid %s added to %s already sits on brief %s\n      fix: do not add it here; that brief '
                             'already owns the question (link it under Pairs with, or backfill that brief instead)' % (t, bid, ', '.join(elsewhere)))
    return n, fails


VOICE_BLOCKS = re.compile(r'<div class="(dp|rule|pearls|danger|traps)\b[^"]*"[^>]*>')
SEP_RE = re.compile(r'\s*(?:·|&middot;|&#183;)\s*')
DASH_RE = re.compile(r'—|&mdash;|&#8212;')


def voice_ranges(html, b):
    """(start, end, label) ranges a voice edit may touch inside brief b."""
    out = []
    for m in VOICE_BLOCKS.finditer(html, b.start, b.end):
        end = pagelib._match_close(html, m.start(), pagelib.DIV_TOKEN, '<div')
        out.append((m.end(), html.rfind('</div', m.start(), end), '.' + m.group(1)))
    sm = re.compile(r'<p class="sub"[^>]*>').search(html, b.start, b.end)
    if sm:
        close = html.find('</p>', sm.end())
        sep = SEP_RE.search(html, sm.end(), close)
        out.append((sm.end(), sep.start() if sep else close, 'p.sub first segment'))
    return out


def voice_check(before, spec):
    """Scope and keep-rules for a voice pass. Returns failure messages."""
    fails, html = [], before
    for n, e in enumerate(spec['edits'], 1):
        if e.get('op') != 'replace':
            fails.append('edit %d: voice passes use replace only (got %s)\n      fix: rewrite prose with replace ops' % (n, e.get('op')))
            continue
        try:
            b = apply_edits._brief(html, e['brief'], n, 'replace')
            at = apply_edits._unique(html, b.start, b.end, e['find'], n, 'replace', 'brief %s' % b.id)
        except apply_edits.EditError as ex:
            fails.append(str(ex))
            continue
        end = at + len(e['find'])
        where = [lab for s, t, lab in voice_ranges(html, b) if s <= at and end <= t]
        if not where:
            fails.append('edit %d (%s): anchor is outside the voice scope\n      fix: edit only inside .dp, .rule, .pearls, '
                         '.danger, .traps or the first segment of p.sub; never .vignette, tables, .crit or the bank' % (n, b.id))
        old_b = [text(x) for x in re.findall(r'<b>(.*?)</b>', e['find'], re.S)]
        new_b = {text(x) for x in re.findall(r'<b>(.*?)</b>', e['with'], re.S)}
        declared = {text(x) for x in e.get('reworded_bold', [])}
        lost = [x for x in old_b if x not in new_b and x not in declared]
        if lost:
            fails.append('edit %d (%s): bold term(s) dropped or renamed: %s\n      fix: keep every bold clinical term verbatim; '
                         'a bold slogan, aphorism or rhetorical label may be reworded only if listed in the op\'s '
                         '"reworded_bold": ["<old bold text>"]' % (n, b.id, '; '.join(lost)))
        stray = sorted(declared - set(old_b))
        if stray:
            fails.append('edit %d (%s): reworded_bold lists text that is not bold in find: %s\n      fix: copy the old bold '
                         'text exactly (tags stripped, entities decoded)' % (n, b.id, '; '.join(stray)))
        nums = lambda t: set(re.findall(r'\d+(?:[.,]\d+)?', t))  # noqa: E731
        lostn = sorted(nums(text(e['find'])) - nums(text(e['with'])))
        if lostn:
            fails.append('edit %d (%s): number(s) dropped: %s\n      fix: keep every number and cutoff' % (n, b.id, ', '.join(lostn)))
        labs = re.findall(r'<span class="lbl">(.*?)</span>', e['find'])
        new_labs = re.findall(r'<span class="lbl">(.*?)</span>', e['with'])
        relab = {text(x) for x in e.get('reworded_label', [])}
        bad = [l for l in labs if l not in new_labs and text(l) not in relab]
        if bad or len(new_labs) != len(labs):
            fails.append('edit %d (%s): label markup changed (%s)\n      fix: keep <span class="lbl">...</span> exactly, or declare a '
                         'slogan label rewrite with "reworded_label": ["<old label text>"]' % (n, b.id, '; '.join(text(l) for l in bad) or 'count'))
        for m in DASH_RE.finditer(e['with']):
            if not re.search(r'</b>\s*$', e['with'][:m.start()]):
                fails.append('edit %d (%s): em dash in prose near %r\n      fix: use a colon, comma, semicolon or period; the only '
                             'allowed em dash is the structural "<b>Term</b> — definition"' % (n, b.id, text(e['with'][max(0, m.start() - 30):m.end() + 20])))
                break
        try:
            html = apply_edits.apply_one(html, e, n, set(), [])
        except apply_edits.EditError as ex:
            fails.append(str(ex))
    return fails


def main(argv):
    render = '--no-render' not in argv
    voice = '--voice' in argv
    nid_src = None
    if '--nids' in argv:
        i = argv.index('--nids')
        if i + 1 >= len(argv):
            print('verify_edits: FAIL --nids needs the source .md path')
            return 2
        nid_src = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
        if not os.path.isfile(nid_src):
            print('verify_edits: FAIL --nids source %s not found' % nid_src)
            return 2
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
        if voice:
            vf = voice_check(before, spec)
            fails.extend(('voice', m) for m in vf)
            print_voice = 'voice: %d op(s) checked (scope, bold terms, numbers, labels, em dashes)%s' % (
                len(spec['edits']), ' | %d failure(s)' % len(vf) if vf else '')
        if nid_src:
            n_nid, nf = nid_check(before, after, nid_src)
            nid_line = 'nids: %d added, checked against %s%s' % (n_nid, os.path.basename(nid_src), ' | %d failure(s)' % len(nf) if nf else '')
            fails.extend(('nids', m) for m in nf)
        else:
            nid_line = 'nids: not checked (pass --nids <source.md>)'
        delta = len(items(after, with_briefs=False)) - len(items(before, with_briefs=False))
        status = 'FAIL' if fails else 'PASS'
        print('verify_edits: %s %d op(s), items %+d, near-dups %d' % (status, len(log), delta, len(dups)))
        print('  ' + gate_line)
        print('  ' + render_line)
        print('  ' + nid_line)
        if voice:
            print('  ' + print_voice)
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
