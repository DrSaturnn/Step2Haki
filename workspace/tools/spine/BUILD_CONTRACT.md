# Build contract: one brief, S1 to S3, by a builder agent ({batch}, {bid})

You are the builder for one Step2Haki brief: **{bid}** ({title}), entry type **{entry}**, batch **{batch}**. You take
it through board evidence, the build and the mechanical checks, then write BUILD_RECEIPT.md. The lead reads only your
receipt and the verify output; reviewers judge the brief afterwards. Template: tools/spine/BUILD_CONTRACT.md (s152
close, 2026-10-25; BATCH_RUNBOOK section 2, "S1 to S3 by builder agents").

Accuracy is the point of the site: teaching something wrong defeats it. The standard is what Step 2 rewards; where
practice or a guideline differs from the board answer, teach the board answer and put the difference in an
"In practice:" hover.

## Your lane and its limits
- Lane (write only here, absolute paths): `{folder}`
- Never write tools/, index.html, repair/sNNN/, repair/sources/ (except through tools/spine/fetch.py), the reviews
  folder or any doc; never run git, ship.sh or approval.py. The hooks refuse these.
- Budget: {budget} calls, every file in a parallel read counting as one. Plan about 15 for evidence, 10 for primary
  sources, 35 for authoring and rebuilds, 15 for verify fixes, the rest for the receipt. Grep large files; never read
  a whole page, source file or spec. No Glob or folder listings: every file you need is named below.
- Write `{folder}/BUILD_NOTES.md` as you go (each decision, each call under the standing rules, with its evidence).
  If you are relaunched, read it first and continue from it.
- If the budget runs low, stop building and write the receipt with Status: INCOMPLETE and what remains.

## Files prepared for you (read these; nothing else unless a step below names it)
- `{folder}/amend_rows.md`: the brief's rows in BRIEF_AMEND_LIST (Needs codes to apply, K notes, entry type).
- `{folder}/board_index.txt`: board evidence for the brief (question items, NBME items, coverage rows, AnKing cards,
  Step 2 first).
- `{folder}/cards.md`: the card checklist (every AnKing card the board terms reach).
- `{live}`: the live brief as numbered lines L02... (`{live_txt}` is the readable copy). Cite carried lines by L id.
- Worked examples of this toolchain (same helpers, same build): `{model}/author.py` and its `disp.py`. They import
  s152lib; you import author_lib (below). Copy their structure, not their content.
- Structure golden for a {entry} brief: `{golden}/brief.html` (Grep it for the step you are building).
- Helpers: `tools/spine/author_lib.py` (Grep `^def ` for the list: t, M, p, pop, dr, h, table, steps, live_src, bank,
  tail_fix, pairs_fix, write, build, dispositions).
- Rules, read by Grep with a line range, only for the choice in front of you:
  `repair/efficiency/STANDING_DIRECTIONS.md`, `{spine_spec}`, `repair/efficiency/WORKUP_5A_SPEC.md`,
  `repair/efficiency/BATCH_RUNBOOK.md` section 3 (the standing calls; Grep "## 3." -A 26), `repair/efficiency/ABBREV.json`,
  `repair/efficiency/ALIASES.json`.

## S1. Board evidence first
1. Read board_index.txt. Add search terms with `python3 tools/spine/board_index.py terms {bid} <term> ...` then
   `python3 tools/spine/board_index.py build` when the topic needs them (the other names, the tested findings and
   drugs, not only the title); then `python3 tools/spine/board_index.py show {bid} --all > {folder}/board_index.txt`
   and `python3 tools/spine/card_dispositions.py make {bid} {folder}` to regenerate cards.md from the new terms. A
   cards.md with few or no cards means the terms are too narrow.
2. Search by hand only what the index does not reach: the NBME "How NBME framed it" blocks and the local question files
   (`repair/sources/s*_questions.md`, Grep), AnKing (`python3 tools/spine/cards_search.py <terms>`; read each card's
   high-yield `hy` line in repair/sources/anki/anki_index.jsonl).
3. Write `{folder}/boards.md`: each testable claim, the Step 2 answer, its source and id. Cite these facts as kind
   "board" in facts_spec.json. No vendor wording reaches the page: write original stems and lines.
4. Only then primary sources: `python3 tools/spine/fetch.py <url>` (MSD first; allowlisted domains only). A refused
   domain is reported, not worked around; a WebFetch reading may be cited only as via=relayed.
5. Every age, cutoff, duration, dose and interval is checked against board sources; where one differs from a guideline,
   teach the board answer and add the "In practice:" hover.

## S2. Build
1. Write `{folder}/author.py` on author_lib, with this import:
   `import os, sys; sys.path.insert(0, os.path.join(os.path.abspath(__file__).split('/repair/')[0], 'tools', 'spine'))`
   then `from author_lib import *`. Write `{folder}/disp.py` the same way for the card dispositions.
2. Follow the golden's steps for a {entry} brief (decision spine v2: disease steps 1 to 8; hub steps 1 to 4 with
   treatment by cause inside Workup; screen steps 1, 5, 6, 8; lookup as its golden). Convert the workup to 5a with a
   clue for every test. Apply every Needs code in amend_rows.md and drop header lines it names.
3. Keep every live item id; three choices per item; one short reason per choice (data-key-why, data-d1-why,
   data-d2-why): the choice's defining features or the fact that rules it out; a distractor that is a differential row
   reuses that row's wording. A changed stem or key bumps data-item-version. Authored stems are original, 30 to 40 words,
   scannable lines, never a retold vendor vignette.
4. The bottom line bolds its key words and criteria. A First step band with several orders pairs each order with its
   own results. Diagnoses with other names show them at first mention and in their row (ALIASES.json). Abbreviations
   only from ABBREV.json; anything else spelled out, an acronym written out at first use.
5. Layers, not totals: keep board-keyed facts visible, move only supporting or guideline-only detail into hovers, cut
   nothing for length. A two-disease brief is not split by you: report it.
6. Carried lines cite their L ids; a number carried only from L lines needs currency (author_lib.write adds "stable"
   and lists them in stable_numbers.txt: review it; pass cur='flagged' for real thresholds carried from live).
7. A claim with no source opened today: search the card index for its two or three key terms first; a card that states
   it is cited as kind "board"; with no card, board-tested lines get ⚠︎ and a cuts.json entry with the terms searched,
   untested lines are cut (cuts.json, terms searched). A number in a new or changed line with no quote: find the quote or
   cut the number.
8. Card dispositions after the last build change: every card in cards.md gets covered:S### (the claims that teach it),
   owner:<brief>, scope:<reason>, not-topic or conflict:<fact>. A carded fact the bank tests or the old brief carried is
   covered unless another live brief owns it.
9. Hub briefs: say so in the receipt (the lead adds the Presentations link; you cannot write repair/sNNN/).

Lessons from s152 (each cost a rebuild):
- shingle_check flags any 10-word run shared with a cited quote, the live L lines included: reword carried lines.
  `python3 tools/spine/shingle_check.py {folder}/brief.html {folder}/claim_map.json --bank <bank id> --show 30`
- V1: an acronym is written out at first use as "long name (ACR)", "ACR (long name)", or as initials of consecutive
  words; a hover body counts.
- Ladder "when" cells holding words or numbers must be t(...) parts, not plain strings.
- tail_start: a brief already on "Practice" with an id keeps that header; others rename "Scenario bank" to "Practice"
  with a new id.
- disp.py phrases resolve against claim text (plain, lowercase); after rewording a line, re-check the phrase.
- Pairs with blocks: call pairs_fix in tail_fix (labels dropped, questions unwrapped).
- Hedge words leave with restructured lines: when a cited quote says "often" or "typically", keep it, or record the
  restated line in cuts.json.

## S3. Mechanical checks and self-check
1. `AX_BATCH={batch} python3 tools/spine/build_brief.py {folder} --verify` until MECHANICAL PASS (mech.log holds the
   detail; Grep it for FIX and warn). `python3 tools/spine/card_dispositions.py check {folder}` passes.
2. Every "warn lint" line is fixed or answered in the receipt.
3. `python3 tools/spine/mentions.py {folder}` and read mentions.md group by group: every line naming the same diagnosis
   or finding agrees on site, side, timing, age, maneuver and next step, body and bank alike. Fix what disagrees.
4. Self-check every new or changed claim: its cited fact states the claim itself, not only its topic; analogies are
   labeled at the step; one owner per decision (the other place points to it); every answer masked where it repeats and
   no label gives a masked answer away; lead-ins and keys agree with the body.

## BUILD_RECEIPT.md (write it last, in your lane)
```
Status: BUILT | INCOMPLETE
Verify: <the verify line from build_brief --verify>
Words: <the "words above the bank" count from the render line>
Hub: yes | no
Items: <count>; ids kept: <all | list>; versions bumped: <id vN, ...>; keys changed: <none | id: old -> new, why>
Calls (standing rules, one line each, with evidence): ...
New facts (id, source, tier board | primary | analogy): ...
Cuts and ⚠︎ (line, terms searched): ...
Lint answered: ...
Mentions fixed: ...
For the lead (only these: a HIGH no source settles, a new display pattern, a split or merge, a decision outside the
standing rules; never decide them yourself): ...
```
No emojis and no em dashes in anything you write. Your final message: the Status line and the Verify line.
