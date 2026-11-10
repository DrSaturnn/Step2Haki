# s172e: hover anchors re-judged (patch; no sentence of brief text changes). One file: plan, evidence, picks, steps

Status: PICKED 2026-11-10, not launched. Nothing built. Step 1 (method) done in the planning chat. Scripts and data:
claude/pending/s172e/ (hover_pairs.py, pairs.csv). The earlier pass's tool is in the public repo:
workspace/repair/s170/anchors/anchors.py (survey, apply).
Model for the launch chat: Opus (every remaining step is APPLY).
Not read: the body of anchors.py apply beyond its first lines; the s170 sort-lane instructions.

## Jonathan's words
- 2026-11-08 10:52 (D-20261108-3): "a lot of the hovers are or have information not relevant to the word that they
  are attached to, as shown."
- 2026-11-10 15:18: "there is also the current issue of hovers being inappropriately added to words, such as with the
  very first brief, finklestein test, should describe the finklestein test rather than this."
- 2026-11-10 15:26: "yes" (empty the allow list and re-judge; fix by moving or by a label). D-20261110-8.
- 2026-11-10 15:58: "we can go based on your recommendations." (the hover pass next, with Claude's budget)

## Open calls
1. May a label trigger be added to a brief that has not been rewritten yet? The gate's prose-touched check holds any
   brief whose text changed to zero prose hits, and a label is new visible text, so the s170 pass left 113 label
   fixes on 68 briefs waiting for each brief's rewrite batch (repair/s170/anchors/anchor_own_pending.json).
   Options: (A) a label taken word for word from the card's own kicker or title does not count as a text change;
   (B) labels keep waiting for the rewrite batches (s173 to s180 and the 68 unconverted briefs). Recommendation: A,
   because the label adds no new wording and B leaves known wrong anchors live for weeks. Under B this batch applies
   moves only.

## Picks
1. repair/efficiency/ANCHOR_ALLOW.json is emptied and every anchored hover is re-judged against D-20261108-5 (each
   hover sits on the term its card explains), with a second reader on a sample (D-20261110-8).
2. A failing hover is fixed by moving its anchor to the term the card explains, or by its own short label trigger; a
   new card for the original term only where a board source tests it (D-20261110-8).
3. Budget (Claude's proposal, accepted 2026-11-10 15:58): 4 agents, 200 calls, 3M agent tokens; lead 30M. Lanes: two
   judging lanes on Opus (role patch-review-opus), one second reader on Sonnet over a 40-pair sample (role
   patch-review), one Sonnet lane that reviews the applied changes (role patch-review). The fourth lane is an
   addition to the three named to Jonathan; the token and lead caps are the ones he accepted.

## Evidence
Method line: live page d3c914b content, 209 briefs; script claude/pending/s172e/hover_pairs.py run from workspace/;
unit = one hover (trigger plus card).
### Counts  TESTED (hover_pairs.py, pairs.csv)
- 614 hovers; 435 anchored on a term in 122 briefs; 179 keep a label trigger.
- 147 anchored hovers share no content word with their card's kicker, title or first line.
- ANCHOR_ALLOW.json holds 421 pairs, 333 of them on the live page, including "Finkelstein test positive|De Quervain"
  (brief scaphoid, hover wh-pop-4, row "De Quervain tenosynovitis").
### Failure rate  ASSUMED (one reader, 30 random anchored hovers)
- 7 clearly fail the rule and 2 are borderline, which projects to about 100 to 130 of 435.
- Failing patterns seen: the card explains the row's diagnosis and the anchor sits on a finding in another cell; the
  anchor is a generic word ("New", "Offered", "board"); the anchor is a number or duration and the card explains an
  exception to it.
### Cause  TESTED (repair/s170/S170.md line 24; ANCHOR_ALLOW.json _doc line)
- The s170 pass sorted 615 hovers in two Sonnet lanes of 16 calls, then passed every pair that failed the word test
  by adding it to the allow list.

## Steps
Files touched: workspace/repair/s172e/ (decisions and edit files), repair/efficiency/ANCHOR_ALLOW.json,
tools/spine/allow_baseline.json (count lowered), the page through the patch pipeline (runbook section 8b).
| # | Kind | Step | Done when |
|---|---|---|---|
| 1 | DONE | Method, read from anchors.py and the s170 record (below the table) | written |
| 1b | APPLY | Extend anchors.py apply: a "move" decision may carry "cell": "row" to place the trigger on the first occurrence of `term` in the first cell of the same table row; add a test | on a scratch page, scaphoid wh-pop-4 opens from "De Quervain tenosynovitis" and the visible text of the brief is unchanged |
| 2 | APPLY | Rerun the survey on the live page; split the 435 anchored hovers into two lane packets by brief; each row shows the trigger, the full line, the row head, the kicker, title and body of the card | two packets, row counts sum to the survey |
| 3 | APPLY | Judging lanes (2, Opus). One question per hover: does this card define or explain the trigger term itself? Verdict KEEP, MOVE (name the exact term in the same row or line that the card explains) or LABEL (the card's kicker or a short noun label; no term in the line fits). A generic word, a bare number or a finding that only co-occurs with the card's subject is not KEEP. No rewording of any card | a verdict for every row |
| 4 | APPLY | Second reader (Sonnet, 40 rows drawn at random by script, verdicts hidden). Agreement on KEEP against not-KEEP under 36 of 40 stops the batch and returns the rubric to step 3 | agreement figure in the batch record |
| 5 | APPLY | Lead check of every MOVE and LABEL target against the page (the term exists once in that line; a label is on HEADERS.json or is the card's own kicker); apply through the method of step 1 | page built; no visible sentence changed (text diff shows only trigger positions and added labels) |
| 6 | APPLY | ANCHOR_ALLOW.json keeps only pairs both readers passed that still fail the word test; lower its count in tools/spine/allow_baseline.json; prose_lint hover_anchor on all briefs | lint green; allow list under 100 or the count explained |
| 7 | APPLY | Review lane (Sonnet) on the changed hovers: study-mode leak (a label or moved trigger must not name a masked answer), label wording, one anchor per term | receipts PASS |
| 8 | APPLY | S8 report with the count by verdict and ten before-and-after examples including scaphoid; ship on "ship" | shipped |
Method (step 1). Decisions file: {"<hover id>": {"verdict": "fits"} | {"verdict": "move", "term": "<exact text in the
line>"} | {"verdict": "own", "label": "<label>"}}. `python3 repair/s170/anchors/anchors.py apply index.html
DECISIONS.json index.html` splices the page in place; s170 committed the spliced workspace/index.html on its branch
(829a600) and ship.sh built on top of it. A move changes markup only, which prose-touched exempts, so moves apply to
every brief. A move reaches only the trigger's own block (li, td, p); the Finkelstein card needs the first cell of
its row, hence step 1b. An "own" label is new visible text: see open call 1. A rewritten brief keeps its anchors
because its rewrite lane places them (tools/spine/REWRITE_CONTRACT.md, "Hover anchors"). The s170 verdicts are in
repair/s170/anchors/anchor_decisions_now.json (fits 442, move 51, own 115; wh-pop-4 was marked fits); the judging
lanes of step 3 start from the survey, with those verdicts hidden.

A card that both readers judge wrong for every term in its row (it needs new content) is listed for Jonathan and left
as a LABEL; no card text is written in this batch.

## Launch line
"Step2Haki: launch batch s172e (patch: hover anchors re-judged against D-20261108-5; no brief sentence changes) per docs/BATCH_RUNBOOK.md section 8b and claude/pending/S172E.md. Decisions: D-20261110-8. Budget: 4 agents, 200 calls, 3M agent tokens (judging Opus 2, second reader Sonnet 1, review Sonnet 1); lead 30M."

## Notes for the launch chat
- `python3 tools/spine/launch.py patch --plan <this file> --batch s172e` prints the read order and copies this plan.
- hover_pairs.py needs bs4 and lxml and takes about four minutes on the live page; anchors.py survey may replace it.
- The trigger "Finkelstein test positive" sits inside a masked cell; a moved anchor must stay outside any mask or
  the review lane will report a leak.
- Every remaining step is written for an Opus lead. Verdict names: the plan says KEEP, MOVE, LABEL; the tool says
  fits, move, own.
