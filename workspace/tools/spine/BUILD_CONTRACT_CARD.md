# Build contract: one class card, S1 to S3, by a builder agent ({batch}, {bid})

You are the builder for one Step2Haki Psych Pharmacology class card: **{bid}** ({title}), entry type **{entry}**,
batch **{batch}**. You take it through board evidence, the build and the mechanical checks, then write BUILD_RECEIPT.md.
The lead reads only your receipt and the verify output; reviewers judge the card afterwards. Template:
tools/spine/BUILD_CONTRACT_CARD.md (s159, 2026-10-30; written from BUILD_CONTRACT.md: the card rules in
`{card_spec}` replace the decision-spine steps).

Accuracy is the point of the site: teaching something wrong defeats it. The standard is what Step 2 rewards; where
practice, a label or a guideline differs from the board answer, teach the board answer and put the difference in an
"In practice:" hover.

## Your lane and its limits
- Lane (write only here, absolute paths): `{folder}`
- Never write tools/, index.html, repair/sNNN/, repair/sources/ (except through tools/spine/fetch.py), the reviews
  folder or any doc; never run git, ship.sh or approval.py. The hooks refuse these.
- Budget: {budget} calls, every file in a parallel read counting as one. Plan about 15 for evidence, 15 for primary
  sources and label checks, 30 for authoring and rebuilds, 15 for verify fixes, the rest for the receipt. Grep large
  files; never read a whole page, source file or spec. No Glob or folder listings: every file you need is named below.
- Write `{folder}/BUILD_NOTES.md` as you go (each decision, each call under the standing rules, with its evidence;
  every page fetched with fetch.py). If you are relaunched, read it first and continue from it.
- If the budget runs low, stop building and write the receipt with Status: INCOMPLETE and what remains.

## Files prepared for you (read these; nothing else unless a step below names it)
- `{folder}/LEAD_NOTES.md`: your card's scope (its drugs, what it owns, what it points to, its siblings), the items the
  lead moved into your shell, and any lead call. Read it first; it overrides this contract where they differ.
- `{folder}/05_<id>_new.json` (the shell; your card id with "_" for "-"): the lead's `new_brief` edit. It holds the card
  head (`p.pc-grp`, `h4`, `p.sub`), the Practice header and the bank with the items moved from **{source}** (ids,
  versions and text unchanged), and its "after" fallbacks. basepage applies it, so your build replaces its body.
- `{folder}/amend_rows.md`: the card's rows in BRIEF_AMEND_LIST, if any.
- `{folder}/board_index.txt`: board evidence (question items, NBME items, coverage rows, AnKing cards, Step 2 first).
- `{folder}/cards.md`: the card checklist (every AnKing card the board terms reach).
- `{live}`: the source brief **{source}** (the s157 brief this card helps retire) as numbered lines L02... (`{live_txt}`
  is the readable copy). Cite carried lines by L id; live_src() saves them under your card id and the cite names
  {source}. Only the lines about your card's drugs are yours; the others belong to sibling cards.
- Worked example (the model card, same helpers, same build): `{model}/author.py` and its `disp.py`, `facts_spec.json`
  and `05_*_new.json`. Copy their structure, not their content.
- Structure golden: `{golden}/brief.html` (Grep it for the block you are building: keypoint, pc-script, pc-blocks,
  lcw, pc-tbl, pc-owners).
- Helpers: `tools/spine/author_lib.py` (Grep `^def ` for the list: t, M, p, pop, dr, h, table, live_src, write,
  build, claim_of, dispositions). Block types: `tools/spine/outline_render.py` docstring and Grep "s159 card".
- Rules, read by Grep with a line range, only for the choice in front of you: `{card_spec}` (the card rules; Grep its
  "## " sections), `repair/efficiency/STANDING_DIRECTIONS.md` (every rule that is not about the decision spine still
  applies: accuracy, sources, board answer first, hovers, bold key words, masks, other names, abbreviations),
  `repair/efficiency/BATCH_RUNBOOK.md` section 3 (the standing calls; Grep "## 3." -A 26), `repair/efficiency/ABBREV.json`,
  `repair/efficiency/ALIASES.json`.
- Seed only, never cited or quoted, layout not carried: Psych Pocket 1.7.2
  (`repair/sources/refs/2026-10-29/psych-pocket-1.7.2-contents.md`, Grep your drugs) and the Medication List
  (`medication-list.txt`, same folder). They are coverage checklists: every line you teach needs a board or primary
  source of its own.

## S1. Board evidence first
1. Read board_index.txt. Add search terms with `python3 tools/spine/board_index.py terms {bid} <term> ...` then
   `python3 tools/spine/board_index.py build` when the class needs them (each drug's generic name, the tested
   reactions and interactions); then `python3 tools/spine/board_index.py show {bid} --all > {folder}/board_index.txt`
   and `python3 tools/spine/card_dispositions.py make {bid} {folder}` to regenerate cards.md. A cards.md with few or no
   cards means the terms are too narrow.
2. Search by hand only what the index does not reach: the NBME "How NBME framed it" blocks and the local question files
   (`repair/sources/s*_questions.md`, Grep), the UWorld library pages named in LEAD_NOTES.md, AnKing
   (`python3 tools/spine/cards_search.py <terms>`; read each card's high-yield `hy` line in
   repair/sources/anki/anki_index.jsonl). Pink AnKing text is priority content.
3. Write `{folder}/boards.md`: each testable claim, the Step 2 answer, its source and id. Cite these facts as kind
   "board" in facts_spec.json. No vendor wording reaches the page: write original lines and stems.
4. Only then primary sources: `python3 tools/spine/fetch.py <url>` (DailyMed label, MSD, StatPearls first; allowlisted
   domains only). A refused domain is reported under For the lead, not worked around; a WebFetch reading may be cited
   only as via=relayed.
5. Every onset, window, washout, dose, level and interval is checked against board sources; where one differs from a
   label or guideline, teach the board answer and add the "In practice:" hover. A timeline time with no board source
   comes from a primary source, named in the receipt.
6. Trade names (CARD_SPEC section 4): a name is shown only when a current FDA label on DailyMed carries it. Fetch the
   label (fetch.py) and record its setid and revision date in the fact. A name the seed documents list without a
   current label is left out and listed in the receipt.
7. A seed-document line with no board or primary source found after the searches: keep it with the unverified mark
   (`span.pc-uv`, "⚠︎ pharm document line; no board source found yet") and list it with the terms searched; never
   drop it silently. A seed line that is outdated is corrected and the correction labeled.

## S2. Build
1. Write `{folder}/author.py` on author_lib, with this import:
   `import os, sys; sys.path.insert(0, os.path.join(os.path.abspath(__file__).split('/repair/')[0], 'tools', 'spine'))`
   then `from author_lib import *`. It writes outline.json with "entry": "card", "lens": "psych", the shell's prefix and
   bank id, and "tail_start" the shell's Practice header exactly. Write `{folder}/disp.py` the same way for the card
   dispositions.
2. Card blocks only, in CARD_SPEC section 2 order: keypoint; script2 with cls "pc-script" (rows Drugs, Mechanism,
   Uses, Adverse effects, then Monitoring or Other only when a fact needs it); rows with cls "pc-blocks" for the
   board-tested dangerous reactions (src = the reaction, finding, commit "If ..., choose ..." with the answer masked,
   at most one p.pc-note extra); lcw charts (onset chart mask "name"; washout or monitoring-window chart mask "win";
   first tick 0, the same ticks on every row, one bar per window, a "Shows" or "Why" line per row); table with cls
   "sp-dx pc-tbl" (interactions: Combined with | Result | Rule, Rule masked; monitoring: When | Check | Why, Check
   masked); owners (one line per decision owned elsewhere, each ending in a drawer); the NBME block only for a logged
   NBME item of the class. Skip a section the class lacks; never reorder. No steps, stepper, h blocks, pause point,
   bottom line, differential, workup or ladder (outline_check S1 and the gate's card-format refuse them).
3. The head (class tag, title, subtitle) is the shell's. Change it only through outline "head_fix" with sourced rich
   text, and say so in the receipt.
4. Practice: the moved items stay verbatim (ids, versions, text, reasons). Add new items to the shell's `ol.bank` so
   the card reaches about three items where the board sources test that much: data-src "authored", data-item-version
   "1", a new unique data-item-id ("q_" plus 20 hex), three choices, data-key-why, data-d1-why and data-d2-why (one short
   reason per choice: the choice's defining features or the fact that rules it out), original 30 to 40 word stems in
   scannable lines, never a retold vendor vignette; each new item's key fact is in boards.md with its source. A changed
   stem or key of a moved item bumps its data-item-version and is named in the receipt.
5. Owner rule (CARD_SPEC section 1): the card holds what the drug does (mechanism, uses named, adverse effects,
   dangerous reactions, interactions, washouts, monitoring); the choice of drug for a disorder stays in its disease
   brief and is reached through "Where the choice is made". Where a live brief teaches a fact your card also needs,
   teach it once in your words with its own source and keep it consistent with the live line (mentions). One owner per
   timed window: a window is drawn once on its owning card; elsewhere point to it. A reaction owned by another brief
   or card carries a drawer chip to it rather than a second copy.
6. Bold the key words of every Key point line and drug line. Generic names bold, trade names in `span.pc-tn`.
   Mechanism lines use the arrow from cause to effect. Diagnoses and reactions with other names show them at first
   mention (ALIASES.json). Abbreviations only from ABBREV.json; anything else spelled out, an acronym written out at
   first use. Mnemonics only with a cited original (an AnKing card or a named source); never invented.
7. Layers, not totals: board-keyed facts stay visible, supporting or label-only detail moves into hovers, nothing is
   cut for length. About 420 words above the bank is the model; the cap is about 600 (outline_check C1, soft): an
   overage for board-keyed content is listed in the receipt's cap_overage line.
8. Carried lines cite their L ids; a number carried only from L lines needs currency (author_lib.write adds "stable"
   and lists them in stable_numbers.txt: review it; pass cur='flagged' for real thresholds carried from live).
9. A claim with no source opened today: search the card index for its two or three key terms first; a card that states
   it is cited as kind "board"; with no card, board-tested lines get ⚠︎ and a cuts.json entry with the terms searched,
   untested lines are cut (cuts.json, terms searched). A number in a new or changed line with no quote: find the quote or
   cut the number.
10. Card dispositions after the last build change: every card in cards.md gets covered:S### (the claims that teach it),
    owner:<brief>, scope:<reason>, not-topic or conflict:<fact>. A carded fact the bank tests or {source} carried for
    your drugs is covered unless another live brief or sibling card owns it.

Lessons carried from s152 to s158 (each cost a rebuild):
- shingle_check flags any 10-word run shared with a cited quote, the L lines included: reword carried lines.
  `python3 tools/spine/shingle_check.py {folder}/brief.html {folder}/claim_map.json --bank <bank id> --show 30`
- V1: an acronym is written out at first use as "long name (ACR)", "ACR (long name)", or as initials of consecutive
  words; a hover body counts.
- Masked answers must not be readable from an unmasked label, a commit lead-in, a table head or a chart's "Shows" line;
  no double-nested masks in one cell.
- One rule worded once across this card and its siblings (a washout, an interval, a level).
- Action words with no source (a drug, a route, "immediate" anything): find the quote or cut.
- Hedge words leave with restructured lines: when a cited quote says "often" or "typically", keep it, or record the
  restated line in cuts.json.
- disp.py phrases resolve against claim text (plain, lowercase); after rewording a line, re-check the phrase.
- The gate (G1) flags "to be confirmed", "to be determined", "TBD", "placeholder" and "??" anywhere on the page.

## S3. Mechanical checks and self-check
1. `AX_BATCH={batch} python3 tools/spine/build_brief.py {folder} --verify` until MECHANICAL PASS (mech.log holds the
   detail; Grep it for FIX, warn and card-format). `python3 tools/spine/card_dispositions.py check {folder}` passes.
2. Every "warn lint" line is fixed or answered in the receipt.
3. `python3 tools/spine/mentions.py {folder}` (card mode: drug names, danger rows and timed windows as subjects) and
   read mentions.md group by group: every line naming the same drug, reaction or window agrees on timing, dose, level,
   rule and next step, card, bank and live briefs alike. Fix what disagrees on your card; name a live brief that
   disagrees under For the lead.
4. Self-check every new or changed claim: its cited fact states the claim itself, not only its topic; analogies are
   labeled; one owner per decision and per window (the other place points to it); every answer masked where it repeats
   and no label gives a masked answer away; commits and item keys agree with the rows.
5. Under parallel load render.js can time out: run verify once alone; if it still times out, stop retrying, write the
   receipt (BUILT if every other check passes) and name it under For the lead.

## BUILD_RECEIPT.md (write it last, in your lane)
```
Status: BUILT | INCOMPLETE
Verify: <the verify line from build_brief --verify>
Words: <the "words above the bank" count from the render line>; cap_overage: <none | the board-keyed lines over 600>
Sections: <the CARD_SPEC sections present, by number>
Items: <count>; moved from {source}: <ids>; new: <ids>; versions bumped: <id vN, ...>; keys changed: <none | id: old -> new, why>
Trade names (name, setid, label revision): ...; left out (no current label): ...
Unverified seed lines kept (pc-uv, terms searched): ...
Calls (standing rules, one line each, with evidence): ...
New facts (id, source, tier board | primary | analogy): ...
Cuts and ⚠︎ (line, terms searched): ...
Lint answered: ...
Mentions fixed: ...
Web: <every page fetched with fetch.py>
Drawer retargets: <each live line (brief, L id or item id, a few words) that pointed to {source} for a fact this card now owns, with the drawer label to {bid}>
For the lead (only these: a HIGH no source settles, a new display pattern, a split or merge, a decision outside the
standing rules or LEAD_NOTES.md; never decide them yourself): ...
```
No emojis and no em dashes in anything you write. Your final message: the Status line and the Verify line.
