#!/usr/bin/env python3
"""review_packet: the lean packet for the four review parts of one spine brief (SPINE_SCALE_PLAN.md section 2), written
into each reviewer's lane. It replaces the lead's hand-built R3 round-1 packets, which dropped every bank item's
lead-in and type (two false MED findings) and listed only 132 of 177 brief titles (one false MED).

  python3 tools/spine/review_packet.py <brief dir> <review dir> [--page index.html] [--proposals FILE] [--diff]

Writes <review dir>/<part>/ for part acc, read, display, flags: brief_text.txt (the brief as the learner reads it, each
bank item shown with its type and lead-in), deps.txt (the receipt's deps line and brief-sha, from verify.py),
HOLISTIC_REVIEW.md, RECEIPT_FORMAT.md (PASS, PASS-IF with replacements, FAIL) and, with --proposals, the
proposed replacements; acc adds facts.json and claim_map.json; read adds sibling_titles.txt (every brief: id and title,
all of them), drawer_targets.txt (each drawer or pointer in the brief and whether its target exists) and the shared
ALIASES.json and ABBREV.json (s147: the other-names and abbreviation tables the read rules cite); flags adds
facts.json, outline_flags.txt and line_sources.txt (every line's cited ids, each quote once; s144). With --diff (s141), every part also gets changes.md: a line diff of the brief as
the learner reads it, the page's current brief against this build, so a rollout review can find each change without
comparing two briefs by hand. Screenshots for display come from shots.py separately.
"""
import difflib
import hashlib
import html as H
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import pagelib as P  # noqa: E402
import verify as V  # noqa: E402


RECEIPT_FORMAT = """# Receipt format (part: %s)

Line 1 `part: <part>`; line 2 the deps line copied exactly from deps.txt; line 3 the brief-sha line from deps.txt;
line 4 the verdict; then `Findings`, numbered; then, for a PASS-IF, `Replacements:`; then `Checked and fine:`.

Verdicts:
- `Verdict: PASS`: no findings that need a change, or only LOW findings you do not need fixed.
- `Verdict: PASS-IF` (conditional PASS, Jonathan 2026-10-12): no HIGH or MED, and every LOW you want fixed comes with an
  exact replacement. The brief then ships READY with any of your replacements applied and nothing else changed.
- `Verdict: FAIL`: any HIGH or MED stands.

A PASS-IF lists its replacements like this, the old text copied exactly as it reads in brief_text.txt:

    Replacements:
    1. old: {{loop diuretic as in rung 1}}
       new: {{loop diuretic as in card 1 above}}

Rules for a replacement (verify refuses any other):
- text only: never markup or study-mode masks, so no <, > or & in old or new; the old text must sit inside one line of
  brief_text.txt and must not cross a bold, a hover or a masked span;
- no changed numbers; no new facts or citations; never an item's stem, key, distractors or lead-in;
- at most 8 replacements, at most 40 words of new text each;
- keep hedge words (may, usually, often, can, rarely, about, consider), negations and diagnosis, drug and test names as
  they are unless changing them is the point of the finding: a replacement that changes any of these counts only for
  your own receipt, and the other three parts then need a normal follow-up review.
If proposed_replacements.md is in your lane, approve each proposal that is in your lane's scope by listing it (you may
reword it within these rules), and say in Findings why you reject any.
"""


def item_line(m):
    a = P.attrs(m.group(1))
    lead = a.get('data-lead-in', '')
    opts = [a.get(k) for k in ('data-d1', 'data-d2') if a.get(k)]
    # s135 S5 packet error: the receipts could not check distractors, so the item line names them (the key is the first bold)
    return '\n[item %s, type %s] Lead-in: %s%s\n' % (a.get('data-item-id', '?'), a.get('data-type', '?'), lead or '(none)',
                                                    ('; distractors: ' + ' / '.join(opts)) if opts else '')


def close_masks(x):
    """s142 R1 packet error: a mask opened "[masked in study mode: " but its end was never shown, so text after a masked
    span (a rung note) read as masked; close each mask span with "]" at its own </span>, nested spans included"""
    out, depth, ends, pos = [], 0, [], 0
    for m in re.finditer(r'<span\b[^>]*>|</span>', x):
        out.append(x[pos:m.start()]); pos = m.end()
        if m.group(0) == '</span>':
            depth -= 1
            out.append(']' if ends and ends[-1] == depth else m.group(0))
            if ends and ends[-1] == depth:
                ends.pop()
        else:
            if re.match(r'<span class="mask[^"]*">', m.group(0)):
                ends.append(depth); out.append('[masked in study mode: ')
            else:
                out.append(m.group(0))
            depth += 1
    out.append(x[pos:])
    return ''.join(out)


def text_of(brief_html):
    x = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', brief_html, flags=re.S)
    x = re.sub(r'(<li\b[^>]*data-item-id="[^"]+"[^>]*>)', lambda m: item_line(m), x)
    x = re.sub(r'<button[^>]*class="[^"]*sp-pop[^"]*"[^>]*>(.*?)</button>', r'[hover: \1]', x, flags=re.S)
    # s135 S5 packet error: arrow and operator glyphs are empty role="img" spans, so the text lost them ("decline over the
    # first 5 years then plateaus" was read without its arrow); write each as the glyph or its label
    x = re.sub(r'<span[^>]*role="img"[^>]*aria-label="([^"]+)"[^>]*>\s*</span>',
               lambda m: {'leads to': ' \u2192 ', 'and': ' + ', 'plus': ' + '}.get(m.group(1), ' [%s] ' % m.group(1)), x)
    x = close_masks(x)
    x = re.sub(r'</(p|li|div|tr|h\d|figure|caption)>|<br\s*/?>', '\n', x)
    x = re.sub(r'</t[dh]>', ' | ', x)
    x = re.sub(r'<[^>]+>', '', x)
    x = H.unescape(x)
    return '\n'.join(l.strip() for l in re.sub(r'[ \t]+', ' ', x).split('\n') if l.strip())


def line_sources(cm):
    """every claim line with the ids it cites, then each cited quote once (s144 packet fix: the flags packet showed only the
    X1 lines' sources, so lines cited to the old brief's own text read as unsourced and drew false MED findings)"""
    out = ['# Sources for every line (from claim_map.json): each line, then the ids it cites; each quote is listed once',
           '# at the end. L ids are the old brief\'s own lines (a valid source for carried content); b ids are board facts;',
           '# m and a ids are primary pages.', '']
    quotes = {}
    for c in cm.get('claims', []):
        srcs = c.get('sources') or []
        out.append('%s: "%s"  <- %s' % (c.get('id', '?'), (c.get('new_text') or c.get('text') or '')[:240],
                                         ', '.join(s.get('id', '') for s in srcs)))
        for s in srcs:
            quotes.setdefault(s.get('id', ''), '%s: %s' % (s.get('source', '')[:120], (s.get('source_says') or '')[:600]))
    out += ['', '## Quotes', '']
    out += ['[%s] %s' % (k, quotes[k]) for k in sorted(quotes)]
    return '\n'.join(out) + '\n'


def legacy_flags(cm, txt):
    """flags for a legacy build.py brief (no outline.json): the outline_check X1 rule read from the claim map (a line whose
    sources are two or more different documents, each shown with its quote) plus every unverified (warning-sign) line"""
    out = ['# Flagged lines (derived from claim_map.json; legacy build.py brief, no outline_check run)', '']
    n = 0
    for c in cm.get('claims', []):
        srcs = c.get('sources') or []
        docs = {re.sub(r'\s*\(.*$', '', s.get('source', ''))[:60] for s in srcs}
        if len(docs) < 2:
            continue
        n += 1
        out.append('X1 %s: "%s"' % (c.get('id', '?'), (c.get('new_text') or c.get('text') or '')[:300]))
        for s in srcs:
            out.append('   - [%s] %s: %s' % (s.get('id', ''), s.get('source', '')[:140], (s.get('source_says') or '')[:1500]))   # s135 S5: 400 cut the mszProg quote
        out.append('')
    warn = [l.strip() for l in txt.splitlines() if '\u26a0' in l]
    out.append('Unverified (warning-sign) lines: %d' % len(warn))
    out += ['   ' + l[:300] for l in warn]
    out.insert(1, 'X1 lines: %d' % n)
    return '\n'.join(out) + '\n'


def titles(page):
    out = []
    for b in P.briefs(page):
        m = re.search(r'<h4[^>]*>(.*?)</h4>', page[b.start:b.end], re.S)
        out.append('%s | %s' % (b.id, H.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else '(no title)'))
    return out


def section(md, title):
    """one '## title' section of a markdown file, heading included ('' when absent)"""
    m = re.search(r'^## %s\n.*?(?=^## |\Z)' % re.escape(title), md, re.S | re.M)
    return m.group(0) if m else ''


def part_rules(part):
    """the standing rules a part judges by (s139 S5 packet errors: display reviewers flagged progressive recall and the
    5a desktop arrows, and a read reviewer the absent step 6, because the packet lacked these rules)"""
    eff = os.path.join(WS, 'repair', 'efficiency')
    sd = open(os.path.join(eff, 'STANDING_DIRECTIONS.md'), encoding='utf-8').read()
    if part == 'display':
        spec = open(os.path.join(eff, 'WORKUP_5A_SPEC.md'), encoding='utf-8').read()
        dg = open(os.path.join(eff, 'DECISIONS_DIGEST.md'), encoding='utf-8').read()
        glance = '\n'.join(m.group(0) for m in re.finditer(r'^- 2026-10-1[34] (Glance layout direction|s137 route).*?(?=^- |\Z)', dg, re.S | re.M))
        return ('# Display rules for this review (from STANDING_DIRECTIONS.md, DECISIONS_DIGEST.md and WORKUP_5A_SPEC.md)\n\n'
                + section(sd, 'Display') + '\n## Later display decisions (digest; these win over the spec)\n\n' + glance + '\n\n' + spec)
    if part == 'read':
        return ('# Structure rules for this review (from STANDING_DIRECTIONS.md)\n\n' + section(sd, 'Brief structure (decision spine)')
                + '\n## Tables in your folder (s147)\n\nALIASES.json (other names) and ABBREV.json (the abbreviation allowlist) '
                'are in your folder. Grep them for the names and abbreviations you check; do not read them whole.\n')
    if part == 'acc':   # s146b: card dispositions (Jonathan 2026-10-17)
        return ('# Card dispositions (acc)\n\nWhen cards.md and cards_disposition.json are in your folder: every AnKing card the '
                "brief's board terms reach has a disposition (covered:S### claim ids, owner:<brief>, scope:<reason>, "
                'not-topic, conflict:<fact>). Spot-check them: a "covered" card whose fact the cited claims do not teach, or a '
                '"scope" or "not-topic" card the bank or the Step 2 answer needs, is a MED finding. Grep cards.md; do not read '
                'it whole.\n')
    return ''


READ_TABLES = ('ALIASES.json', 'ABBREV.json')   # s147 (Jonathan): the read part judges other names and abbreviations


def copy_read_tables(read_dir):
    """copy the shared other-names and abbreviation tables (repair/efficiency) into the read lane; returns the names
    copied. s146b packet gap: read reviewers were told to check ALIASES and ABBREV but had neither file."""
    eff = os.path.join(WS, 'repair', 'efficiency')
    done = []
    for f in READ_TABLES:
        src = os.path.join(eff, f)
        if not os.path.exists(src):
            sys.exit('review_packet: missing %s' % src)
        shutil.copy(src, os.path.join(read_dir, f))
        done.append(f)
    return done


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    d, out = os.path.abspath(argv[0]), os.path.abspath(argv[1])
    page = P.read_page(argv[argv.index('--page') + 1] if '--page' in argv else os.path.join(WS, 'index.html'))
    v = V.Verify(d, True, False)
    try:
        if not v.render():
            sys.exit('review_packet: render failed: %s' % v.fix)
    finally:
        shutil.rmtree(v.tmp, ignore_errors=True)
    brief = v.brief_html
    bsha = hashlib.sha1(brief.encode()).hexdigest()[:10]
    ids = {b.id for b in P.briefs(page)}
    tl = titles(page)
    targets = sorted(set(re.findall(r'data-brief="([^"]+)"|href="#([^"]+)"', brief)))
    drawers = ['%s | %s' % (t, 'exists' if t in ids else 'MISSING (not a brief id; may be a section anchor)')
               for t in sorted({a or b for a, b in targets})]
    txt = text_of(brief)
    props = argv[argv.index('--proposals') + 1] if '--proposals' in argv else None
    diff = None
    if '--diff' in argv:
        live = [b for b in P.briefs(page) if b.id == v.bid]
        old = text_of(page[live[0].start:live[0].end]).splitlines() if live else []
        dl = list(difflib.unified_diff(old, txt.splitlines(), 'page now', 'this build', n=1, lineterm=''))
        diff = ('# Changes in this build (s141 --diff)\n\nLines starting "-" are the page now; "+" this build; others are '
                'context. %s\n\n' % ('No change.' if not dl else '%d changed line(s).' % sum(
                    1 for x in dl if x[:1] in '+-' and x[:3] not in ('+++', '---')))) + '\n'.join(dl) + '\n'
    for part in ('acc', 'read', 'display', 'flags'):
        pd = os.path.join(out, part)
        os.makedirs(pd, exist_ok=True)
        open(os.path.join(pd, 'brief_text.txt'), 'w', encoding='utf-8').write(txt)
        open(os.path.join(pd, 'deps.txt'), 'w').write(v.deps_line(part) + '\nbrief-sha: ' + bsha + '\n')
        hr = os.path.join(WS, 'repair', 'migration', 'spine', 'HOLISTIC_REVIEW.md')
        if os.path.exists(hr):
            shutil.copy(hr, os.path.join(pd, 'HOLISTIC_REVIEW.md'))
        open(os.path.join(pd, 'RECEIPT_FORMAT.md'), 'w', encoding='utf-8').write(
            RECEIPT_FORMAT % part + '\nWrite the receipt with the Write tool to the absolute path %s (the lane gate refuses '
            'a relative path, and a refused write still counts against your call budget; s134).\n'
            % os.path.join(os.path.abspath(pd), 'receipt.md'))
        if props:
            shutil.copy(props, os.path.join(pd, 'proposed_replacements.md'))
        if diff is not None:
            open(os.path.join(pd, 'changes.md'), 'w', encoding='utf-8').write(diff)
        rules = part_rules(part)
        if rules:
            open(os.path.join(pd, 'RULES.md'), 'w', encoding='utf-8').write(rules)
    for f in ('facts.json', 'claim_map.json'):
        shutil.copy(os.path.join(d, f), os.path.join(out, 'acc', f))
    for f in ('cards.md', 'cards_disposition.json'):            # s146b: acc audits the card dispositions
        if os.path.exists(os.path.join(d, f)):
            shutil.copy(os.path.join(d, f), os.path.join(out, 'acc', f))
    shutil.copy(os.path.join(d, 'facts.json'), os.path.join(out, 'flags', 'facts.json'))
    open(os.path.join(out, 'flags', 'line_sources.txt'), 'w', encoding='utf-8').write(line_sources(v.cm))
    of = os.path.join(d, 'outline_flags.txt')
    if os.path.exists(of):
        shutil.copy(of, os.path.join(out, 'flags', 'outline_flags.txt'))
    else:                                   # a legacy build.py folder has no outline_check flags (s134)
        open(os.path.join(out, 'flags', 'outline_flags.txt'), 'w', encoding='utf-8').write(legacy_flags(v.cm, txt))
    open(os.path.join(out, 'read', 'sibling_titles.txt'), 'w', encoding='utf-8').write('\n'.join(tl) + '\n')
    open(os.path.join(out, 'read', 'drawer_targets.txt'), 'w', encoding='utf-8').write('\n'.join(drawers) + '\n')
    copy_read_tables(os.path.join(out, 'read'))
    n_items = len(re.findall(r'data-item-id=', brief))
    n_leads = len(re.findall(r'Lead-in: (?!\(none\))', txt))
    print('review_packet: %s, brief-sha %s, %d items (%d with lead-ins), %d brief titles, %d drawer targets'
          % (v.bid, bsha, n_items, n_leads, len(tl), len(drawers)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
