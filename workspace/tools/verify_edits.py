#!/usr/bin/env python3
"""verify_edits.py: the one check a worker runs before finishing.

  python3 tools/verify_edits.py <edits.json> [page] [--nids <source.md>] [--voice [--report]] [--no-render]

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


HARD_RE = re.compile(
    r'\d|[<>≤≥]|\b(mg|mcg|kg|mL|mmol|mEq|IU|units?|percent|percentile|hours?|days?|weeks?|months?|years?)\b|'
    r'\b(test|testing|scan|ultrasound|ultrasonography|radiograph|x-ray|film|CT|MRI|MRCP|ERCP|endoscopy|colonoscopy|biopsy|'
    r'series|serology|culture|titer|assay|level|antibod\w*|panel|screen\w*|smear|stain|swab|manometry|enema|'
    r'epinephrine|formula|antibiotic\w*|steroid\w*|laxative\w*|suppositor\w*|fluids?|dose|cutoff|threshold)\b|'
    r'\w+(mab|pril|olol|sartan|statin|cillin|mycin|floxacin|azole|prazole|sone|olone|dipine|tidine|vir|parin)\b|'
    r'(?-i:\b[A-Z][A-Z0-9]{1,}\b)', re.I)
ACR_SKIP = {'IgA', 'IgE', 'IgG', 'IgM', 'US', 'UK', 'MD', 'IV', 'IM', 'PO', 'NBME', 'OK', 'II', 'III', 'IV', 'HIV', 'DNA', 'RNA', 'CT', 'MRI'}
ROMAN_RE = re.compile(r'(?=[IVXL])X{0,3}(IX|IV|V?I{0,3})')
SENT_RE = re.compile(r'(?<=[.?!])\s+(?=[A-Z<(])|\s*·\s*')
ARROW_RE = re.compile(r'→|&rarr;')
NBME_RE = re.compile(r'How NBME framed it')  # s31-reviewed text; a voice pass leaves it verbatim
BATCH_NOTE_RE = re.compile(r'-{2,}\s*<i>\s*Batch \d[^<]*</i>')  # workflow note, removed in the voice pass


try:
    _ACR = json.load(open(os.path.join(HERE, 'acronyms.json'), encoding='utf-8'))
    EXPANSIONS = sorted(set(_ACR['expansions'].values()), key=len, reverse=True)
    ACR_SKIP_EXTRA = set(_ACR.get('skip', []))
except Exception:
    EXPANSIONS = []
    ACR_SKIP_EXTRA = set()


def strip_exp(t):
    """Remove standard acronym expansions ' (x)' / ' [x]' so quotes survive a later expansion pass."""
    for x in EXPANSIONS:
        t = t.replace(' (%s)' % x, '').replace(' [%s]' % x, '')
    return re.sub(r' \(([A-Za-z]{2,6}s?), [^)]*?\)', '', t)


def norm_q(t):
    """Text for quote matching: tags stripped, entities decoded, whitespace collapsed, curly quotes plain."""
    t = text(t).replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    return re.sub(r'\s+', ' ', t).strip()


def _mnemonic(acr, after):
    """True when the text after the dash spells the acronym out (first word matches, several capitalized words)."""
    w = re.findall(r'[A-Za-z]+', after)
    caps = [x for x in w[:8] if x[:1].isupper()]
    return bool(w) and w[0][:1].upper() == acr[0].upper() and len(caps) >= 3


def acronym_misses(seg):
    """Acronyms whose first use in a block is not followed (directly or after its enclosing bold span) by a
    parenthesis or bracket. Skips labels, Pairs-with partner titles, roman numerals (factor VII, type II),
    25-OH style chemistry, immunoglobulin names and ACR_SKIP."""
    pairs = 'Pairs with' in seg[:80]
    spans = [(m.start(), m.end()) for m in re.finditer(r'<span class="lbl">.*?</span>', seg, re.S)]
    bolds = [(m.start(), m.end()) for m in re.finditer(r'<b>.*?</b>', seg, re.S)]
    out, seen = [], set()
    for m in re.finditer(r'(?<![A-Za-z0-9-])([A-Z][A-Za-z]*[A-Z][A-Za-z0-9]*|[a-z][A-Z]{2,}[A-Za-z]*)(?![A-Za-z0-9])', seg):
        acr = m.group(1)
        lt, gt = seg.rfind('<', 0, m.start()), seg.rfind('>', 0, m.start())
        if lt > gt or acr in seen or any(a <= m.start() < b for a, b in spans):
            continue
        if re.match(r'(?:</b>)?\s*(—|&mdash;)', seg[m.end():m.end() + 14]) and re.match(r'(?:</b>)?\s*(?:—|&mdash;)\s*[A-Z]', seg[m.end():m.end() + 24]) \
                and len(acr) >= 3 and _mnemonic(acr, norm_q(seg[m.end():m.end() + 120])):
            continue  # mnemonic row: "HELLP — Hemolysis, Elevated Liver enzymes, Low Platelets"
        if acr in ACR_SKIP or acr in ACR_SKIP_EXTRA or ROMAN_RE.fullmatch(acr) or acr == 'OH' or re.search(r'\d-$', seg[:m.start()]) or \
                re.fullmatch(r'Ig[A-Z]', acr) or not re.search(r'[A-Z].*[A-Z]', acr) or re.search(r'[a-z]{2}', acr):
            continue
        inb = [(a, b) for a, b in bolds if a <= m.start() < b]
        if pairs and inb:
            continue
        seen.add(acr)
        end = inb[0][1] if inb else m.end()
        if re.match(r'(?:</b>)?\s*[(\[]', seg[m.end():m.end() + 6]) or re.match(r'\s*[(\[]', seg[end:end + 3]):
            continue
        out.append(acr)
    return out


def voice_check(before, spec, report=None):
    """Scope, keep-rules and the drift protocol for a voice pass.
    Returns (failures, warnings); appends reviewer lines to `report` when given."""
    fails, warns, html, quotes = [], [], before, []
    titles = {norm_q(t) for t in re.findall(r'<h4>(.*?)</h4>', before, re.S)}
    touched = {}
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
        blk = [s for s, t, lab in voice_ranges(html, b) if s <= at and end <= t]
        if blk and html.startswith('<span class="lbl">How NBME framed it</span>', blk[0]):
            fails.append('edit %d (%s): a "How NBME framed it" block is out of scope (reviewed in s31)\n      fix: leave the block '
                         'exactly as it is' % (n, b.id))
        nbme_txt = [html[k.start():html.find('</div>', k.start())] for k in NBME_RE.finditer(html, b.start, b.end)]
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
        carried = ' '.join(c.get('carried_by', '') for c in e.get('claims', []) if isinstance(c, dict))
        lostn = sorted(nums(text(BATCH_NOTE_RE.sub('', e['find']))) - nums(text(e['with'])) - nums(carried))
        if lostn:
            fails.append('edit %d (%s): number(s) dropped: %s\n      fix: keep every number and cutoff' % (n, b.id, ', '.join(lostn)))
        labs = re.findall(r'<span class="lbl">(.*?)</span>', e['find'])
        new_labs = re.findall(r'<span class="lbl">(.*?)</span>', e['with'])
        relab = {text(x) for x in e.get('reworded_label', [])}
        bad = [l for l in labs if l not in new_labs and text(l) not in relab]
        if bad or len(new_labs) != len(labs):
            fails.append('edit %d (%s): label markup changed (%s)\n      fix: keep <span class="lbl">...</span> exactly, or declare a '
                         'slogan label rewrite with "reworded_label": ["<old label text>"]' % (n, b.id, '; '.join(text(l) for l in bad) or 'count'))
        ctx0 = html[max(0, at - 200):at]
        titled = [(t.start(), t.end()) for t in re.finditer(r'<b>(.*?)</b>', e['with'], re.S) if norm_q(t.group(1)) in titles]
        for m in DASH_RE.finditer(e['with']):
            if any(a <= m.start() < z for a, z in titled):
                continue  # a quoted brief title (Pairs with) keeps its own punctuation
            if not re.search(r'</b>\s*$', ctx0 + e['with'][:m.start()]):
                fails.append('edit %d (%s): em dash in prose near %r\n      fix: use a colon, comma, semicolon or period; the only '
                             'allowed em dash is the structural "<b>Term</b> — definition"' % (n, b.id, text(e['with'][max(0, m.start() - 30):m.end() + 20])))
                break
        # ---- drift protocol: claim map
        claims, newc = e.get('claims'), e.get('new_claims')
        if not isinstance(claims, list) or not claims:
            fails.append('edit %d (%s): no "claims" list\n      fix: list every atomic clinical claim of the OLD text with '
                         '"to", "carried_by" or "dropped" (see the claim-map format)' % (n, b.id))
            claims = []
        if not isinstance(newc, list):
            fails.append('edit %d (%s): no "new_claims" list\n      fix: list every clinical claim of the NEW text with "from"' % (n, b.id))
            newc = []
        old_texts = set()
        for k, c in enumerate(claims, 1):
            ct = norm_q(c.get('claim', '')) if isinstance(c, dict) else ''
            if not ct:
                fails.append('edit %d (%s): claim %d has no "claim" text' % (n, b.id, k))
                continue
            old_texts.add(ct)
            keys = [x for x in ('to', 'carried_by', 'dropped') if c.get(x)]
            if not keys:
                fails.append('edit %d (%s): claim %d is unmapped: %r\n      fix: give "to" (the new sentence, quoted), '
                             '"carried_by" (a quoted passage elsewhere in this brief) or "dropped" (reason, framing only)' % (n, b.id, k, ct[:90]))
            for x in ('to', 'carried_by'):
                if c.get(x):
                    quotes.append((n, b.id, k, x, norm_q(c[x]), ct))
            if c.get('dropped'):
                hm = HARD_RE.search(ct)
                if hm:
                    fails.append('edit %d (%s): claim %d is dropped but carries a number, drug, test or cutoff (%r): %r\n      '
                                 'fix: keep it ("to") or show where the brief already carries it ("carried_by")' % (n, b.id, k, hm.group(0), ct[:90]))
        for k, c in enumerate(newc, 1):
            if not isinstance(c, dict) or not norm_q(c.get('claim', '')):
                fails.append('edit %d (%s): new_claims %d has no "claim" text' % (n, b.id, k))
                continue
            fr = c.get('from')
            if not fr:
                fails.append('edit %d (%s): new claim %d has no "from": %r\n      fix: name the old claim it came from, '
                             'or "expansion" for a written-out acronym' % (n, b.id, k, norm_q(c['claim'])[:90]))
            elif fr != 'expansion' and norm_q(fr) not in old_texts:
                fails.append('edit %d (%s): new claim %d "from" does not match any old claim of this op: %r\n      fix: copy the '
                             '"claim" text of the old claim exactly, or use "expansion"' % (n, b.id, k, fr[:90]))
        # ---- round 2 style: arrows, sentence length, acronyms
        for sent in [x for x in SENT_RE.split(norm_q(e['with'])) if x.strip()]:
            if len(ARROW_RE.findall(sent)) > 1:
                fails.append('edit %d (%s): more than one arrow in a sentence: %r\n      fix: split the chain; at most one → '
                             'per sentence' % (n, b.id, sent[:100]))
            w = len(sent.split())
            if w > 35:
                fails.append('edit %d (%s): %d-word sentence: %r\n      fix: one idea per sentence, about 25 words' % (n, b.id, w, sent[:100]))
            elif w > 25:
                warns.append('edit %d (%s): %d-word sentence: %r' % (n, b.id, w, sent[:80]))
        if report is not None:
            report.append('=' * 78)
            report.append('edit %d  brief %s  %s' % (n, b.id, ' '.join(where) if where else '(OUT OF SCOPE)'))
            report.append('OLD: ' + norm_q(e['find']))
            report.append('NEW: ' + norm_q(e['with']))
            for c in claims:
                if isinstance(c, dict):
                    dest = ('to: ' + norm_q(c['to'])) if c.get('to') else ('carried_by: ' + norm_q(c['carried_by'])) if c.get('carried_by') \
                        else ('DROPPED: ' + str(c.get('dropped'))) if c.get('dropped') else 'UNMAPPED'
                    report.append('  - %s\n      %s' % (norm_q(c.get('claim', '')), dest))
            for c in newc:
                if isinstance(c, dict):
                    report.append('  + %s   <- %s' % (norm_q(c.get('claim', '')), c.get('from', 'NO FROM')))
        try:
            html = apply_edits.apply_one(html, e, n, set(), [])
        except apply_edits.EditError as ex:
            fails.append(str(ex))
            continue
        nb0 = [x for x in briefs(html) if x.id == b.id]
        if nb0 and any(t not in html[nb0[0].start:nb0[0].end] for t in nbme_txt):
            fails.append('edit %d (%s): the "How NBME framed it" text changed (reviewed in s31)\n      fix: end find before '
                         '"How NBME framed it", or copy that text into with unchanged' % (n, b.id))
        # acronyms: first use in the changed block (on the new page) is followed by its expansion
        try:
            nb = [x for x in briefs(html) if x.id == b.id][0]
            rng = [(s0, t0, lab) for s0, t0, lab in voice_ranges(html, nb) if s0 <= at <= t0]
        except IndexError:
            rng = []
        for s0, t0, lab in rng[:1]:
            touched.setdefault(b.id, set()).add(lab)
    for bid, labs in touched.items():
        nb = [x for x in briefs(html) if x.id == bid]
        for s0, t0, lab in (voice_ranges(html, nb[0]) if nb else []):
            if lab in labs:
                for acr in acronym_misses(html[s0:t0]):
                    warns.append('%s %s: acronym %s at first use is not followed by its expansion' % (bid, lab, acr))
    # quotes must exist in the new page (the brief's visible text after every op)
    btext = {}
    for n, bid, k, x, q, ct in quotes:
        if bid not in btext:
            try:
                bb = [b for b in briefs(html) if b.id == bid][0]
                btext[bid] = norm_q(bb.inner)
            except IndexError:
                btext[bid] = ''
        if q not in btext[bid] and strip_exp(q) not in strip_exp(btext[bid]):
            fails.append('edit %d (%s): claim %d "%s" quote not found in the new brief: %r\n      fix: quote the new text '
                         'exactly (visible text, tags stripped)' % (n, bid, k, x, q[:100]))
    return fails, warns


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
            rep = [] if '--report' in argv else None
            vf, vw = voice_check(before, spec, rep)
            fails.extend(('voice', m) for m in vf)
            print_voice = 'voice: %d op(s) checked (scope, bold terms, numbers, labels, em dashes, claim map, arrows, length, acronyms)%s%s' % (
                len(spec['edits']), ' | %d failure(s)' % len(vf) if vf else '', ' | %d warning(s)' % len(vw) if vw else '')
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
            for w in vw:
                print('  [voice warning] ' + w)
            if rep:
                print('\n'.join(rep))
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
