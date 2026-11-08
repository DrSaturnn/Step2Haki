# Rewrite lane contract: {bid} ({title}), batch {batch}

Role {role}, budget {budget} tool calls. Lane folder {folder}; your files are in {rd}/. Write only
{rd}/rewrite_{batch}.json and {rd}/NOTES.md. Do not edit brief.html, claim_map.json, facts.json, build.py or any file
outside the lane folder; tools/spine/rewrite_lanes.py writes those from your JSON.

## Task

Rewrite the brief's lines into review-book register (the writing card above; full rules and the approved rows in
{style}), and carry out the items and calls in items.md. Every fact, number, hedge, negation and claim id survives.
The brief has {n_units} units and {n_hits} prose lint hits. A finished lane leaves the rebuilt brief with zero prose
hits and passes the check command below.

## Read, in this order

1. items.md: the items (N rows) and calls (C rows) this lane carries out, and the lead's notes.
2. units.md: every unit by step, with its text, its claim ids and its prose hits ("HITS"). Hits are the minimum; every
   line in the brief is held to the writing card.
3. header_map.md: header renames that apply here. nbme.md and step2.md: the NBME blocks and step 2 lines to settle.
4. units.json: the exact html of a unit, when you rewrite it. Read it by uid (grep), never whole.
5. {style}: the approved rows (sections "Approved examples") and the header list, when a line needs a model. Read by
   section with grep and sed.

Do not read the page, the runbook, STANDING_DIRECTIONS or the digest whole. Grep them for the topic in hand.

## What you write: {rd}/rewrite_{batch}.json

```
{"brief": "{bid}",
 "units": [{"uid": "U012", "new": "<li>...</li>", "note": "why, one line"},
           {"uid": "U013", "new": "", "carried_by": ["U012"], "note": "merged into U012"},
           {"uid": "U020", "new": "...", "lock_ok": ["UWorld"], "lock_reason": "source name moved to data-src (N4)"},
           {"uid": "U031", "new": "...", "claims": ["S014", "S015"]}],
 "raw": [{"old": "<exact html from baseline_{batch}.html>", "new": "...", "claims": [], "note": "block move"}],
 "new_claims": [{"text": "plain text of the new line", "ids": ["fact id"]}],
 "facts_local": {"cards": [[id, nid, quote]], "web": [[id, sha, section, quote]], "local": [[id, file, title, quote]]}}
```

- "new" replaces the unit's whole html (the element and everything inside it, hover included). Keep the element's tag,
  ids, classes, data-* attributes, aria-controls pairs and hover ids unless an item says to change them.
- A unit you leave alone is not listed. A unit listed twice, or two changes that overlap, fail collect.
- Removal: "new": "" with "carried_by" (the units now holding its facts), "lock_ok" + "lock_reason", or "cut" (a
  cuts.json id the lead approved).
- Adding a block: write it into the "new" of the unit it follows (old html + new block).
- "raw" is for a change no unit covers (moving a whole table or div between steps). Its "old" must occur exactly once in
  baseline_{batch}.html and must not overlap a unit you changed. Record every step move in NOTES.md (block, from, to,
  class, reason); the lead writes repair/{batch}/step_moves.json from it.
- Claims: the claim ids inside a unit keep their ids and sources; collect sets each one's text to your new line. A unit
  that is part of a longer claim updates that claim's text in place. Name "claims" only when you move a claim to a
  different unit. A new fact needs a new claim with a fact id, and that fact must come from facts.json or from
  facts_local with a quote that occurs verbatim in its source (tools/spine/facts_from_spec.py checks every quote).
- Hover lines (TEXTBOOK_STYLE rule 6; site/css/components/lines.css): inside span.sp-pop-b each line is
  `<span class="sp-l">...</span>`; a cause-and-effect line under the line above is
  `<span class="sp-l sp-la"><span class="op op-a" role="img" aria-label="leads to"></span> ...</span>`; a block
  heading is `<span class="sp-l sp-bh">...</span>`. Keep span.sp-ct (the card title) first. No kicker naming a source.
  A line runs to about 12 words, 16 at most (prose_lint hover_line_long).
- Key point lists: a block heading is `<li class="sp-bh">`, its lines `<li class="sp-bl">`. Script rows: `p.sp-bh` and
  `p.sp-bl`.
- Header renames from header_map.md: list the dropped words in "lock_ok" with "lock_reason": "header rename Hn"
  (the meaning lock reads "most" in "most tempting first" as a hedge).
- Sources (N4): a source name leaves the visible text; put it on the line element as data-src="..." and list the
  dropped token in lock_ok with lock_reason "source name moved to data-src (N4)".
- NBME blocks outside a pause point: carry the stem details that separate the options into the brief's lines (symptom
  line, mimic line, next step), then remove the block with "carried_by".
- Step 2 holds diagnostic criteria only. A workup ladder found there moves to the Workup step (raw change + NOTES.md row).

## Check, then finish

Run from the workspace folder (/home/claude/Step2Haki/workspace):

```
python3 tools/spine/rewrite_lanes.py check {batch} {bid}
```

It collects your JSON into delta_{batch}.json, builds the brief, then prints one FIX line per problem: meaning lock
(a changed line dropped a number, hedge, negation, side or name), prose lint on the whole rebuilt brief, and the
content gate (NBME block, step 2 workup, step moves). Fix every FIX line and run it again. A FIX you believe is a false
positive goes in NOTES.md with the line and the reason; the lead decides.

Then write {rd}/NOTES.md: what you changed by item and call, every step move (block, from, to, class, reason), every
lock_ok and its reason, any fact you could not source, and any line you left with a hit and why. Finish with one line:
`DONE {bid}: <changes> changes, check <PASS|FAIL n>`.
