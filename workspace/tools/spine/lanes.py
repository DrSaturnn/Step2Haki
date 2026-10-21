#!/usr/bin/env python3
"""lanes: write one review round's lane folders and INSTRUCTIONS.md from a JSON spec (s148 efficiency fix 5; from the
s148 scratch lanes.py, lanes2.py and lanes3.py). Runbook S4 (round 1) and S7 (follow-up rounds).

  python3 tools/spine/lanes.py <spec.json> [--dry]

Spec (paths relative to workspace/ or absolute):
  {"batch": "s149", "plan_step": "s149", "round": 1,
   "context": "batch s149 (Phase 2, musculoskeletal B) converts these briefs to decision spine v2",
   "out": "repair/efficiency/lanes/s149/r1",
   "packets": "<dir>",          review_packet.py output per brief: <packets>/<brief>/<part>/ (with deps.txt)
   "sheets": "<dir>",           display images <brief>_*.png (sheets.py)
   "lanes": [{"part": "acc", "group": "A", "briefs": ["x", "y"], "budget": 18}, ...],   budget optional
   "types": {"x": "presentation hub, FM lens (steps 5 to 8 greyed)", ...},
   "steps": {"x": "1, 3 and 4"},                       follow-up display: the steps shown
   "prior": {"acc": {"x": "<last receipt path>"}, ...},  follow-up: each part's last receipt per brief
   "adjudication": {"x": "<lead adjudication path>"},   follow-up: the lead's S5 notes per brief
   "notes": {"read": ["a decision the reviewer must not report"]},
   "extra_judge": {"acc": ["Timelines (Jonathan ...): ..."]},
   "custom": {"flags": {...}}}                          s148h: a part reviewed by a batch-specific scope (below)

custom (s148h, a review narrower than a whole brief, e.g. the per-choice reasons): per part, any of
  "text"     replaces the part's judging text (%(plan)s, %(extra)s and %(budget)d are filled in);
  "plan"     the call plan sentence put in place of %(plan)s (default: the part's per-brief plan);
  "files"    the per-brief packet files copied into each brief folder (default: the part's usual files);
  "combine"  [file, chunk chars]: each brief's packet <file> joined, in lane order, into lane-root files
             <part>_packet_<k>.md of at most chunk chars each (one Read can take about 25k tokens), split at brief
             boundaries; the lane then needs no brief folders;
  "images"   glob patterns under "sheets" copied into the lane root (display sheets that span briefs);
  "receipt"  "lane": one receipt for the whole lane at <lane>/receipt.md, a section per brief.
A custom part with its own text in a follow-up round gets no FOLLOW block (its text says what the round covers).

Round 1 copies each part's packet files; a follow-up round copies them too and writes review.md (acc, read, flags: the
last receipt, the adjudication, then changes.md from review_packet.py --since) or round1.md (display: the last receipt
and the adjudication). Budgets default to the runbook's call plan: round 1 acc and display 7 per brief plus 4, read and
flags 5 per brief plus 4; follow-up rounds 5 per brief plus 4, display 7 per brief plus 4. A lane over the hook's cap of
25 calls is refused (split it). Prints one line per lane with its budget.
"""
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..'))
CAP = 25
ROLE = {'acc': 'acc-review', 'read': 'read-review', 'display': 'display-review', 'flags': 'flag-review'}
FILES = {'acc': ['brief_text.txt', 'facts.json', 'claim_map.json', 'cards.md', 'cards_disposition.json'],
         'read': ['brief_text.txt', 'sibling_titles.txt', 'drawer_targets.txt', 'ALIASES.json', 'ABBREV.json'],
         'flags': ['brief_text.txt', 'outline_flags.txt', 'line_sources.txt', 'facts.json'],
         'display': ['brief_text.txt']}
PER = {1: {'acc': 7, 'read': 5, 'flags': 5, 'display': 7}, 2: {'acc': 5, 'read': 5, 'flags': 5, 'display': 7}}


def budget(part, rnd, n):
    return PER[1 if rnd == 1 else 2][part] * n + 4


COMMON = """Do not use Glob or list folders: every path you need is named here. Every file in a parallel read counts as one call. Write-first: finish one brief and write its receipt before you open the next brief's files. Budget %(budget)d is a hard cap (the hook stops you there); if you near it, write the receipt with what you have rather than read more. Grep large files rather than reading them whole.

Context: %(context)s (steps 1 Illness script or Presentation, 2 Urgent risks, 3 Differential, 4 Workup, 5 Diagnostic criteria, 6 Severity, 7 Treatment, 8 Follow-up; a hub stops after Workup and hands off by drawer; then Practice, the bank). In brief_text.txt hovers appear as [hover: label] with their text, masked study-mode answers as [masked in study mode: ...], and bank items as [item id, type] with lead-in and distractors; older items are compact one-line chains (stem -> answer -> next step) with no lead-in, as on the page: not a finding by itself.
"""

FOLLOW = """
This is follow-up round %(round)d (S7). You or a reviewer of your part reviewed these briefs before; the lead fixed or answered every finding. In each brief folder, one file holds the round's context: review.md (acc, read, flags) or round1.md (display): your part's last receipt, then how the lead adjudicated its findings (ACCEPT, PARTIAL or REJECT with the reason), then, in review.md, the changes: a line diff of the brief as the learner reads it, your last version against this build, with context, and the files your part needs (below). Scope: (1) every changed line, judged in its context by your part's rules; (2) each finding in your last receipt: resolved, or still open (say why); a REJECT or a "settled by Jonathan" item is closed unless the new text makes it wrong in a new way. Lines that did not change and were not in your last findings are out of scope.
"""

RECEIPT = """Receipt format: line 1 `part: %(part)s`; line 2 the deps line listed for that brief above, copied exactly; line 3 its brief-sha line; line 4 `Verdict: PASS`, `Verdict: PASS-IF` or `Verdict: FAIL`; then %(earlier)s`Findings`%(new)s, numbered, each with severity (HIGH, MED, LOW), area, the exact text and where it is (step, row, item id), the problem and a concrete fix; then, for a PASS-IF, `Replacements:`; then `Checked and fine:` (one line per area you checked).
Verdicts: PASS = no findings that need a change; PASS-IF = no HIGH or MED, and every LOW you want fixed comes with an exact replacement; FAIL = any HIGH or MED stands (HIGH wrong or misleading for the exam; MED contradiction, unsupported or uninterpretable line, broken cross-reference, display defect that hides content; LOW wording).
A PASS-IF replacement is written
    1. old: {{text copied exactly from one line of brief_text.txt}}
       new: {{replacement}}
and must be text only (no <, > or &), inside one line, not crossing a bold, hover or masked span; no changed numbers, no new facts or citations, never an item's stem, key, distractors or lead-in; at most 8 replacements of at most 40 new words each; keep hedge words, negations and diagnosis, drug and test names unless changing them is the point.
Write each receipt with the Write tool to the absolute path given for that brief. Final message: per brief, the verdict and the counts of findings by severity.
"""

FACTS_KEY = ('facts.json (every cited source quote by id: b = AnKing card or other board source, kind "board"; u, v = '
             'UWorld articles, kind board; L = the old brief\'s own line, a valid source for carried content; other '
             'letters = MSD, AAFP, guideline or label pages)')

PART1 = {
'acc': """Part acc (areas B and G, every claim, every key). Files in each brief folder: brief_text.txt; """ + FACTS_KEY + """; claim_map.json (each claim S### with its text and cited fact ids); cards.md (the AnKing cards the brief's board terms reach); cards_disposition.json (each card's disposition); deps.txt (already given below; do not read it). Read brief_text.txt whole; Grep facts.json, claim_map.json and cards.md for the ids and terms you need; never read those three whole.

Call plan per brief: 1 Read of brief_text.txt, at most 4 Greps (batch several ids into one regex), 1 Write: 6 per brief, %(plan)s.

Judge:
- Every claim is correct for Step 2 CK and supported by the fact(s) it cites: the quote states the claim itself, not only its topic. Every number, age, cutoff, duration, dose and interval is right and quoted.
- B. One understanding: wherever the brief states the same fact (body, hovers, tables, ladder, bank explanations, Pearls, notes, rules), the statements agree in numbers, qualifiers, ages, order of steps and drug choice.
- G. Board fit: read the bank items as a test taker; the body gives what you need to answer each, and no body line contradicts a key or explanation.
- Card dispositions: spot-check cards_disposition.json against cards.md (Grep): a "covered" card whose fact the cited claims do not teach, or a "scope" or "not-topic" card that the bank or the Step 2 answer needs, is MED.
%(extra)sStandard of correct: what Step 2 CK rewards. Where literature or practice differs from the exam, the brief teaches the exam answer (NBME keys, then UWorld, then AnKing) and may name the difference in an "In practice:" hover; a line that teaches newer literature in place of the exam answer is a finding. Any line that would lead a test taker to a wrong answer is HIGH, wherever it sits. Zebras are taught as safeguards: flag a line that implies a zebra is common, or a missing safeguard a board question would test. Board facts outrank MSD, AAFP and guidelines. Not your scope: display, style, word count.
""",
'read': """Part read (areas A, C, D, E; you do not judge medical truth). Files in each brief folder: brief_text.txt; sibling_titles.txt (every brief on the page: id and title); drawer_targets.txt (each drawer or pointer in the brief and whether its target exists); ALIASES.json (the shared other-names table); ABBREV.json (the shared abbreviation allowlist); deps.txt (already given below; do not read it). Read brief_text.txt and drawer_targets.txt whole; Grep sibling_titles.txt, ALIASES.json and ABBREV.json for the names you check.

Call plan per brief: 1 Read of brief_text.txt, 1 Read of drawer_targets.txt, at most 2 Greps, 1 Write: 5 per brief, %(plan)s.

Judge:
- A. Coherence: each step answers its heading and the subtitle question; the bottom line predicts what the steps teach; one owner per decision (the same decision made twice with different wording is MED); the steps hand off (a workup result branches to where the differential or treatment picks it up).
- C. Lines that stand alone: each line interpretable without its source; no fragment, undefined label or abbreviation, "this" or "it" without a referent, or author shorthand; a masked study-mode cell still leaves a question the learner can answer.
- D. Syntax and voice: grammar, parallel lists, punctuation, consistent tense and names for the same thing, plain labels (no catchy headers), no em dashes, arrows only for "leads to".
- E. Cross-references: every drawer and pointer names a live brief once, by its current title, with a description that matches what that brief teaches.
%(extra)sStructure rules (STANDING_DIRECTIONS): step names as above, absent steps numbered and greyed; hubs open with the presentation and stop after Workup; bottom line 3 lines at most; Differential ordered by how tempting each option is, each Decides-it cell led by its timeline in bold when the diagnosis has one; Workup = the diagnostic workup tree (zones First step, Targeted tests, Next step, Diagnostic test, Skip; caption "Diagnostic workup"; never opens with a question), then the clue table (Clue | Points to | Next best step, no questions, no chips), then the pause point; Treatment one ladder, each rung tag, trigger, move; captions and headers plain labels. Abbreviations: those on ABBREV.json are written short; anything else is spelled out at first use or in a hover. Other names: a diagnosis with more than one name shows its other names at first mention and in its differential row (ALIASES.json). Row drawers: a differential row whose diagnosis owns a brief is a drawer. Repeated links are allowed but keep clutter down.
""",
'display': """Part display (area F and study-mode leaks; you do not judge content). Files in each brief folder: <brief>_phone_sheet1.png (and sheet2 when present): the whole brief on a 390 px phone in normal mode; <brief>_phone-study_sheet1.png (and sheet2): the same in study mode (masks on); <brief>_desktop_workup.png: the desktop Workup step; brief_text.txt (Grep it for exact wording only); deps.txt (already given below; do not read it). How the sheets are packed: the phone page is cut into 1,500 px columns placed left to right (grey gutters between columns), so content runs down one column and continues at the top of the next; a cut at a column's foot is the packing, not a clip; a red bar marks a step boundary. Known capture artifact, not to report: the previous brief's sticky step rail over this brief's rail title.

Call plan per brief: one Read per image (3 to 5), at most 1 Grep, 1 Write: at most 7 per brief, %(plan)s.

Judge in the images: nothing clipped, overlapping, unreadable or out of order; tables legible on phone; every value in a phone table card starts on one left edge; no text squeezed into a narrow column (a few words per line: Jonathan's "widen, don't shorten"); charts and timelines labelled, horizontal, pastel, in the voices-chart style (per-row legends, no nested frames, tick labels on every row); in study mode the answers and only the answers are hidden (a repeated answer left unmasked elsewhere is a leak, MED); the 5a workup on phone: clue full width, arrow and order on the next line; meanings colored in the words; no dark purple number discs; mnemonics vertical with the capital centered; hubs show steps 5 to 8 greyed.
%(extra)s""",
'flags': """Part flags (area H). Files in each brief folder: outline_flags.txt (the X1 lines: each line that cites two or more sources, with every cited quote under it); line_sources.txt (every line with its cited ids, each quote listed once at the end); facts.json (every source quote by id); brief_text.txt; deps.txt (already given below; do not read it). Read outline_flags.txt whole; Grep line_sources.txt, facts.json or brief_text.txt only for what outline_flags.txt does not show.

Call plan per brief: 1 Read of outline_flags.txt, at most 3 Greps, 1 Write: 5 per brief, %(plan)s.

Judge (X1 combined): for each line citing two or more sources, does the line keep each source's conditions (population, setting, threshold, hedge)? Does any line state more than its quotes together support (a number, age or interval no quote gives; "always" or "never" where a quote hedges; an adult source carried to children without "as in adults")? L ids are the old brief's own lines: valid for carried wording, but not for a new number. List only the lines that fail, each with the fix; then the count checked and fine. A line that would teach a wrong exam answer is HIGH; a claim its quotes do not support is MED; a lost hedge or condition that changes nothing on the exam is LOW.
%(extra)s""",
}

PART2 = {
'acc': """Part acc (areas B and G, every changed claim, every changed key). Files in each brief folder besides that one: brief_text.txt (the whole brief); """ + FACTS_KEY + """; claim_map.json (each claim S### with its text and cited fact ids); cards.md and cards_disposition.json (the AnKing cards and each card's disposition); deps.txt (already given below; do not read it).

Call plan per brief: 1 Read of review.md, at most 2 Greps (batch the claim texts, fact ids and terms you need into one regex per file: claim_map.json, facts.json, cards.md or brief_text.txt), 1 Write: 4 per brief, %(plan)s. Never re-read a file; if a Grep finds nothing, decide from what you have.

Judge:
- Every changed claim is correct for Step 2 CK and supported by the fact(s) it cites: the quote states the claim itself, not only its topic. Every number, age, cutoff, duration, dose and interval in a changed line is right and quoted.
- B. One understanding: a changed line agrees with every other place the brief states the same fact (Grep brief_text.txt for the key term).
- G. Board fit: a changed key, explanation or body line still answers each bank item it touches; no body line contradicts a key.
- Card dispositions: where a change re-keyed a card (review.md says so), spot-check it.
%(extra)sStandard of correct: what Step 2 CK rewards (NBME keys, then UWorld, then AnKing); the difference from literature may sit in an "In practice:" hover. Any line that would lead a test taker to a wrong answer is HIGH. Not your scope: display, style, word count.
""",
'read': """Part read (areas A, C, D, E; you do not judge medical truth). Files in each brief folder besides that one: brief_text.txt (the whole brief); sibling_titles.txt (every brief: id and title); drawer_targets.txt (each drawer or pointer and whether its target exists); ALIASES.json; ABBREV.json; deps.txt (already given below; do not read it).

Call plan per brief: 1 Read of review.md, at most 2 Greps (brief_text.txt for context, or ALIASES.json, ABBREV.json, sibling_titles.txt or drawer_targets.txt for a name a changed line uses), 1 Write: 4 per brief, %(plan)s. Never re-read a file; if a Grep finds nothing, decide from what you have.

Judge each changed line:
- A. Coherence: it answers its step; one owner per decision (the same decision made twice with different wording is MED); the steps still hand off.
- C. Stands alone: interpretable without its source; no fragment, undefined label or abbreviation, "this" or "it" without a referent, or author shorthand; a masked cell still leaves an answerable question.
- D. Syntax and voice: grammar, parallel lists, punctuation, consistent names, plain labels, no em dashes, arrows only for "leads to".
- E. Cross-references: a changed drawer or pointer names a live brief by its current title.
%(extra)sStructure rules (STANDING_DIRECTIONS): hubs stop after Workup; Differential ordered by how tempting, each Decides-it cell led by its timeline in bold when the diagnosis has one; Workup = the diagnostic workup tree (caption "Diagnostic workup"; never opens with a question), then the clue table (Clue | Points to | Next best step), then the pause point; Treatment one ladder, each rung tag, trigger, move. Abbreviations on ABBREV.json are written short; others spelled out at first use or in a hover. A diagnosis with other names shows them at first mention and in its differential row.
""",
'display': """Part display (area F and study-mode leaks; you do not judge content). Files in each brief folder besides that one: <brief>_phone_sheet1.png (and sheet2 when present): the changed steps on a 390 px phone in normal mode; <brief>_phone-study_sheet1.png (and sheet2): the same in study mode (masks on); <brief>_desktop_workup.png: the desktop Workup step; brief_text.txt (Grep it for exact wording only); deps.txt (already given below; do not read it). How the sheets are packed: the phone steps are stacked and cut into 1,500 px columns placed left to right (grey gutters between columns), so content runs down one column and continues at the top of the next; a cut at a column's foot is the packing, not a clip; a red bar marks a step boundary. Only the steps changed since your last review are shown (listed per brief below); the Practice section is not shown (its changes are text only). Known capture artifacts, not to report: the previous brief's sticky step rail over this brief's rail title; the sticky rail truncating step names (queued site-wide).

Call plan per brief: 1 Read of round1.md, one Read per image (3 to 5), 1 Write: at most 7 per brief, %(plan)s. Never re-read a file.

Judge in the images: nothing clipped, overlapping, unreadable or out of order; tables legible on phone; every value in a phone table card starts on one left edge; no text squeezed into a narrow column (a few words per line: "widen, don't shorten"); figures titled, stacked full width on a phone, horizontal on desktop, labelled and legible, meanings masked in study mode; in study mode the answers and only the answers are hidden (a repeated answer left unmasked elsewhere is a leak, MED; by site convention subtitles, illness-script lines, tail prose cards and clue labels stay unmasked: not a finding); the 5a workup on phone: clue full width, arrow and order on the next line; meanings colored in the words; hubs show steps 5 to 8 greyed.
%(extra)s""",
'flags': """Part flags (area H). Files in each brief folder besides that one: outline_flags.txt (the X1 lines: each line that cites two or more sources, with every cited quote under it); line_sources.txt (every line with its cited ids, each quote once at the end); facts.json (every source quote by id); brief_text.txt; deps.txt (already given below; do not read it).

Call plan per brief: 1 Read of review.md, at most 2 Greps (outline_flags.txt, line_sources.txt or facts.json for the changed lines' ids and quotes; one regex per file), 1 Write: 4 per brief, %(plan)s. Never re-read a file; if a Grep finds nothing, decide from what you have.

Judge each changed line that cites sources: does it keep each source's conditions (population, setting, threshold, hedge)? Does it state more than its quotes together support (a number, age or interval no quote gives; "always" or "never" where a quote hedges; an adult source carried to children without "as in adults")? L ids are the old brief's own lines: valid for carried wording, not for a new number. A line that would teach a wrong exam answer is HIGH; a claim its quotes do not support is MED; a lost hedge that changes nothing on the exam is LOW.
%(extra)s""",
}

PLAN_PER = {1: {'acc': 6, 'read': 5, 'flags': 5, 'display': 7}, 2: {'acc': 4, 'read': 4, 'flags': 4, 'display': 7}}


def ab(p):
    return p if os.path.isabs(p) else os.path.join(WS, p)


def plan_text(part, rnd, n, b):
    per = PLAN_PER[1 if rnd == 1 else 2][part]
    use = per * n + 1
    return '%d for %d brief(s), plus the 1 Read of these instructions: %d of your %d, %d spare' % (per * n, n, use, b, b - use)


RECEIPT_LANE = """Receipt format (one receipt for the lane): write it with the Write tool to %(path)s. Line 1 `part: %(part)s`; line 2 `lane: %(lane)s`; then one section per brief, in the order above: `## <brief>`, its deps line and its brief-sha line copied exactly from the list above, `Verdict: PASS`, `Verdict: PASS-IF` or `Verdict: FAIL`, then `Findings` (numbered, each with severity HIGH, MED or LOW, the exact text and where it is (item id and which reason, or the step and row), the problem and a concrete fix), then for a PASS-IF `Replacements:`, then `Checked and fine:` (one line). A brief with nothing to report still gets its section with `Verdict: PASS`.
Verdicts: PASS = no findings that need a change; PASS-IF = no HIGH or MED, and every LOW you want fixed comes with an exact replacement; FAIL = any HIGH or MED stands (HIGH wrong or misleading for the exam; MED contradiction, unsupported or uninterpretable line, display defect that hides content; LOW wording).
A PASS-IF replacement is written
    1. old: {text copied exactly from the packet}
       new: {replacement}
text only (no <, > or &), inside one line; no changed numbers, no new facts; never an item's stem, key, distractors or lead-in (a reason may be replaced); keep hedge words, negations and diagnosis, drug and test names unless changing them is the point.
Final message: per brief, the verdict and the counts of findings by severity.
"""


def custom(spec, part):
    return (spec.get('custom') or {}).get(part) or {}


def chunks(spec, ln):
    """[(file name, text)] for a "combine" lane: the briefs' packet files joined in lane order, split at brief
    boundaries so no chunk passes the size limit (a brief larger than the limit gets a chunk of its own)."""
    cu = custom(spec, ln['part'])
    name, cap = cu['combine'][0], int(cu['combine'][1])
    out, cur = [], ''
    for br in ln['briefs']:
        t = open(os.path.join(ab(spec['packets']), br, ln['part'], name), encoding='utf-8').read().rstrip() + '\n\n'
        if cur and len(cur) + len(t) > cap:
            out.append(cur)
            cur = ''
        cur += t
    if cur:
        out.append(cur)
    return [('%s_packet_%d.md' % (ln['part'], k), t) for k, t in enumerate(out, 1)]


def lane_text(spec, ln, b):
    part, rnd, briefs = ln['part'], int(spec['round']), ln['briefs']
    lane = os.path.join(ab(spec['out']), '%s-%s' % (part, ln['group'])) + '/'
    cu = custom(spec, part)
    extra = ''.join('- %s\n' % x if part != 'display' and part != 'flags' else '%s\n' % x
                    for x in (spec.get('extra_judge') or {}).get(part, []))
    notes = ''.join('Not a finding (decided): %s\n' % x for x in (spec.get('notes') or {}).get(part, []))
    tmpl = cu.get('text') or (PART1 if rnd == 1 else PART2)[part]
    body = tmpl % {'plan': cu.get('plan') or plan_text(part, rnd, len(briefs), b), 'extra': extra, 'budget': b}
    head = ['Role: %s' % ROLE[part], 'Plan step: %s' % spec['plan_step'], 'Lane: %s' % lane, 'Budget: %d' % b, '',
            'Step2Haki %s, review round %d%s, part %s, for %d brief(s): %s. %s' % (
                spec['batch'], rnd, '' if rnd == 1 else ' (follow-up)', part, len(briefs), ', '.join(briefs),
                'One receipt covers the whole lane (%sreceipt.md).' % lane if cu.get('receipt') == 'lane' else
                'Each brief has its own folder in your lane (%s<brief>/) and gets its own receipt.' % lane), '',
            COMMON % {'budget': b, 'context': spec['context']} + ('' if rnd == 1 or cu.get('text') else FOLLOW % {'round': rnd}),
            body + notes, 'Briefs (in this order):']
    for br in briefs:
        deps = open(os.path.join(ab(spec['packets']), br, part, 'deps.txt'), encoding='utf-8').read().splitlines()
        extra_b = ''
        if part == 'display' and spec.get('sheets') and not cu.get('images'):
            imgs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ab(spec['sheets']), '%s_*.png' % br)))
            shown = (spec.get('steps') or {}).get(br)
            extra_b = '%s; images: %s' % ('; steps shown: %s' % shown if shown and rnd > 1 else '', ', '.join(imgs))
        if cu.get('receipt') == 'lane':
            head.append('- %s (%s): deps line: %s; brief-sha line: %s' % (
                br, (spec.get('types') or {}).get(br, 'spine brief'), deps[0], deps[1]))
            continue
        head.append('- %s (%s): receipt %s%s/receipt.md; line 2: %s; line 3: %s%s' % (
            br, (spec.get('types') or {}).get(br, 'spine brief'), lane, br, deps[0], deps[1], extra_b))
    if cu.get('combine'):
        head += ['', 'Packet files in your lane root, in this order (one Read each): %s.' % ', '.join(
            lane + f for f, _ in chunks(spec, ln))]
    if cu.get('images'):
        head += ['', 'Images in your lane root (one Read each): %s.' % ', '.join(
            lane + os.path.basename(f) for f in lane_images(spec, part))]
    if cu.get('receipt') == 'lane':
        head += ['', RECEIPT_LANE % {'path': lane + 'receipt.md', 'part': part, 'lane': lane}]
    else:
        head += ['', RECEIPT % {'part': part, 'earlier': '' if rnd == 1 else '`Earlier findings` (each number from '
                                'your last receipt: resolved, closed, or open with the reason); then ',
                                'new': '' if rnd == 1 else ' (new ones)'}]
    return lane, '\n'.join(head)


def lane_images(spec, part):
    out = []
    for g in custom(spec, part).get('images', []):
        out += sorted(glob.glob(os.path.join(ab(spec['sheets']), g)))
    return out


def build(spec, dry=False):
    out = []
    rnd = int(spec['round'])
    for ln in spec['lanes']:
        part, n = ln['part'], len(ln['briefs'])
        b = int(ln.get('budget') or budget(part, rnd, n))
        if b > CAP:
            raise SystemExit('lanes: %s-%s needs %d calls, over the hook cap of %d: split the lane' % (part, ln['group'], b, CAP))
        lane, txt = lane_text(spec, ln, b)
        out.append((lane, b, len(txt)))
        if dry:
            continue
        cu = custom(spec, part)
        os.makedirs(lane, exist_ok=True)
        if cu.get('combine'):
            for f, t in chunks(spec, ln):
                open(os.path.join(lane, f), 'w', encoding='utf-8').write(t)
        for f in lane_images(spec, part):
            shutil.copy(f, os.path.join(lane, os.path.basename(f)))
        for br in ln['briefs']:
            if cu.get('combine') or (cu.get('receipt') == 'lane' and not cu.get('files')):
                continue
            bd = os.path.join(lane, br)
            os.makedirs(bd, exist_ok=True)
            src = os.path.join(ab(spec['packets']), br, part)
            for f in cu.get('files') or FILES[part]:
                if os.path.exists(os.path.join(src, f)):
                    shutil.copy(os.path.join(src, f), os.path.join(bd, f))
            if part == 'display' and spec.get('sheets') and not cu.get('images'):
                for f in sorted(glob.glob(os.path.join(ab(spec['sheets']), '%s_*.png' % br))):
                    shutil.copy(f, os.path.join(bd, os.path.basename(f)))
            if rnd > 1:
                prior = ab(spec['prior'][part][br])
                ctx = "# Your part's last receipt\n\n" + open(prior, encoding='utf-8').read()
                adj = (spec.get('adjudication') or {}).get(br)
                if adj:
                    ctx += '\n\n' + open(ab(adj), encoding='utf-8').read()
                if part == 'display':
                    open(os.path.join(bd, 'round1.md'), 'w', encoding='utf-8').write(ctx)
                else:
                    ch = os.path.join(src, 'changes.md')
                    ctx += '\n\n' + (open(ch, encoding='utf-8').read() if os.path.exists(ch) else
                                     '# Changes\n\n(no changes.md: run review_packet.py --since)\n')
                    open(os.path.join(bd, 'review.md'), 'w', encoding='utf-8').write(ctx)
        open(os.path.join(lane, 'INSTRUCTIONS.md'), 'w', encoding='utf-8').write(txt)
    return out


def main(argv):
    if not argv:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    spec = json.load(open(argv[0], encoding='utf-8'))
    rows = build(spec, '--dry' in argv)
    for lane, b, n in rows:
        print('%s  budget %d  (%d chars)' % (lane, b, n))
    print('lanes: %d lane(s), %d calls in all%s' % (len(rows), sum(r[1] for r in rows), ' (dry run)' if '--dry' in argv else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
