# Batch runbook: one batch from launch to "ship" in a fresh chat (2026-10-12)

Jonathan, 2026-10-12: "make it so that a fresh chat can complete the batch from start to finish without these extra back and forths."

Adopted for every batch by Jonathan 2026-10-12 (DECISIONS_DIGEST). Repo copy of the project doc claude/BATCH_RUNBOOK.md.

A batch is one or more briefs taken through evidence, build, review, fixes and follow-up review to one approval report. Jonathan is asked twice:
- **at launch:** his launch prompt names the briefs, the budget and any decisions;
- **at the end:** he replies "ship", or names what to change.

Everything between is decided by the lead under the rules below, recorded in the batch file, and disclosed in the final report, where Jonathan can reverse any of it before shipping.

This runbook sits under DECISIONS_DIGEST, STANDING_DIRECTIONS and the plan (claude/SPINE_SCALE_PLAN.md v4). Where they conflict, a dated digest line wins, then STANDING_DIRECTIONS, then the plan, then this file. It changes only when Jonathan asks.

**Read order for any fresh chat:**
1. STEP2HAKI_HANDOFF.md (its State names the current batch, its step and its spend);
2. this file;
3. claude/STANDING_DIRECTIONS.md;
4. claude/DECISIONS_DIGEST.md;
5. claude/SPINE_SCALE_PLAN.md, sections 0, 2, 4, 5 and 8;
6. the batch file, claude/pending/<batch>.md, if one exists (otherwise the handoff State is the batch record);
7. claude/pending/BRIEF_AMEND_LIST.md;
8. claude/SPINE_SPEC.md (decision spine v2: entry types, step names, lenses), before building or reconciling any brief;
9. claude/design/WORKUP_5A_SPEC.md;
10. conditional PASS: claude/pending/POST_SHIP_R3.md section 2, with the s133 digest lines (hedge words count as meaning; text-only replacements).

**Continuation chats** (Jonathan 2026-10-17): a chat that continues an open batch reads only the handoff State, the batch file, DECISIONS_DIGEST lines from 2026-10-15 on, and the batch's own rows and notes in BRIEF_AMEND_LIST (grep, not the whole file); the full read order above is for launches. A chat that starts S4 after the S3 restart also reads, per brief, boards.md, cuts.json and the cards_disposition.json counts (not the cards). A chat that starts S8 after the S7 restart reads only the State, the batch file's S5 and S7 sections and each receipt's verdict line (s148 efficiency fix 1).

**Reading and paths** (s148 efficiency fix 4, Jonathan 2026-10-18): do not call register_repo_root (the repos have no CLAUDE.md; each registration re-sends the whole skill list); use absolute paths and never cd into another folder in a command (a working-folder change re-sends the environment and memory context); read docs by Grep or a line range, never whole when the read list allows less.

**Restart line**, the same every time; Jonathan pastes it when a chat fills: `Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.`

**The paste step** (Jonathan 2026-10-17: "always give me the paste step"): every message that stops a chat for a restart ends with the exact line to paste, alone in its own code block, so it can be copied in one tap; the same holds for the next launch prompt at a batch close.

**Token rules** (Jonathan 2026-10-24: "no screenshots remove the bind needing screenshots"; "for briefs with small
additions, no need to recheck/reprove the whole brief just the changes"):
- No screenshots in a content batch: no display reviewer, no legib_audit, no approval sheets. Jonathan checks the live
  site after the ship. Screenshots, the display part and legib_audit run only in a batch that changes styles, scripts
  or layout or adds a new display pattern (section 8). Study-mode leaks are judged from text (the read part, area F, and
  lint mask-leak); squeezed phone text from the DOM (`tools/spine/squeeze_check.py`).
- Small additions to a live brief (a row, a line, a table, a rename): board evidence, build and review cover the changed
  lines only, with the targeted replay on the live brief (the latest repair/migration/spine/sNNN_delta.py) and packets
  from `review_packet.py --since` the live brief's text. Never re-prove, regenerate cards.md or re-review the rest.
- One batch per chat: after a ship and its post-ship steps the chat ends; the next batch or patch starts in a fresh chat
  with its launch prompt. S8 and S9 stay in one chat (the approval record lives in the container that presented).
- Patches (Jonathan 2026-10-24: "we need to be even more token efficient with the whole process"): section 8b.
  One chat from launch to ship (no S3 or S7 restart), tools/spine/patch.py for every mechanical step, delta-ready
  intake, and one combined reviewer per lane.
- Find, don't search: `tools/spine/folder_of.py <brief>` gives a brief's spine folder; `tools/spine/pointer_check.py`
  checks drawers and Pairs with in a running page; shots_all and legib_audit carry a 240 s timeout. Write no scratch
  wrappers for these.

## 1. Launch

The launch prompt names:
- the batch id and its briefs;
- the budget for the whole batch, all rounds included: agents, API calls, tokens;
- any decisions for this batch.

The lead's first acts:
1. Write the launch prompt's decisions to DECISIONS_DIGEST in Jonathan's words (G-DECIDE). Write the budget to WAVE.json.
2. Do the session start from the handoff:
   - clone the repo;
   - restore local-only by direct staging (nothing written into Documents), for each brief in the batch: its folder under repair/migration/ (parked build, outline, facts, claim map), repair/migration/spine/ (specs and earlier reviews), the web-cache pages its facts cite, and the board sources (question files, Aquifer cases, AnKing index);
   - install the token;
   - the hooks: when the step2haki-tools plugin's hooks are live (`python3 tools/hooks/test_hooks.py` passes and a probe Agent launch with no model is refused by the launch gate), skip install.sh; otherwise run `bash tools/hooks/install.sh` (and the /root/.claude copy, handoff Session start 4), asking Jonathan when the permission check holds it; then run the hook tests (s148 item 9);
   - check the start-up context: `python3 tools/hooks/usage_ledger.py --context` (s135 efficiency item 9). A WARNING means a tool list grew; name it in the report;
   - check that the Agent tool lists `step2haki-tools:lean-reviewer` (the plugin in Jonathan's account; s135 item 1). The launch gate runs the four review roles only as that type, so if it is missing the review steps cannot run (section 6).
3. Rewrite the handoff State: batch id, briefs, budget, step, spend.

Then run section 2 to the end without asking.

## 2. Steps (each ends with a rewrite of the handoff State)

- **S1. Board evidence first.** For each brief, before any build or fix:
  - Look the brief up in the board-evidence index first: `python3 tools/spine/board_index.py show <brief>` (question items, page NBME items, coverage rows, AnKing cards, Step 2 first). Add terms with `board_index.py terms <brief> ...` and rebuild (`build`, seconds) when the topic needs them; search the sources by hand only for what the index does not reach (s135 item 5).
  - Search the board sources for the topic:
    - NBME items: the bank's "How NBME framed it" blocks and the nbme-intake log;
    - the local UWorld question files (repair/sources/s*_questions.md);
    - AnKing (tools cards_search.py).
  - Card checklist (Jonathan 2026-10-17, after s146 dropped a carded fact): `python3 tools/spine/card_dispositions.py make <brief> <folder>` writes cards.md, every AnKing card the brief's board terms reach (cards linked by note id plus up to 90 Step 2 candidates, ranked by how many board terms they name). Before the build is final, give every card a disposition in cards_disposition.json: covered:S### (the claim ids that teach it), owner:<brief>, scope:<reason>, not-topic, or conflict:<fact>. A carded fact the bank tests, or one the old brief carried, is covered unless another live brief owns it. Write the dispositions after the last build change: covered entries name claim ids, and a row added or removed above them shifts the ids, so re-derive them after any later edit. `card_dispositions.py check <folder>` must pass; verify runs it whenever cards.md exists, and the acc reviewer audits the dispositions.
  - Write boards.md in the brief folder: each testable claim, the Step 2 answer, its source and id. Cite these facts as kind "board" in facts.json. No vendor wording reaches the page.
  - Only then go to MSD, guidelines and other primary sources (fetch.py), for mechanism, numbers and support. Where one differs from the board answer, teach the board answer and put the difference in an "In practice:" hover.
  - In the first batch only, report how much the local UWorld files cover (question count, systems).
- **S2. Build or reconcile.**
  - Parked builds: adjudicate every change in the diff against live as ACCEPT, REJECT or PARTIAL, with evidence. Never reverse a digest decision.
  - Convert the workup to 5a (claude/pending/pilot5a), with a clue for every test.
  - Drop header lines and apply the brief's Needs codes from the amendment list.
  - Sidebar placement (Jonathan 2026-10-17, s146c):
    - a brief that becomes a hub (data-entry="hub") also gets a plain link in the sidebar's Presentations group, and that
      group's count goes up by one; the gate fails a hub missing from Presentations;
    - a new or converted Psychiatry brief goes into one of the six disorder-family groups (Psychosis and mood; Anxiety,
      somatic and sexual; Cognition, substances and medical causes; Child and adolescent; Medications; Safety and
      violence), under its sidebar sub-label and in the same page order; briefs are moved with the move_brief edit
      (tools/apply_edits.py), which never changes a brief's content.
- **Brief set rules of 2026-10-20** (Jonathan: "each new brief set automatically includes them"; DECISIONS_DIGEST
  2026-10-20), for every brief a batch merges, builds or rewrites, from s149 on (the psych briefs get them in s148h):
  - every practice item carries one short reason per choice (data-key-why, data-d1-why, data-d2-why): the choice's
    defining features or the fact that rules it out; a distractor that is a differential row reuses that row's wording;
    items keep 3 choices;
  - the bottom line bolds its key words and criteria (the deciding counts, durations, ages and cutoffs, the diagnosis
    named, the action chosen); verify's lint flags a bottom line with no bold;
  - a First step band with several orders pairs each order with its own results (one row group per order);
  - the display rules (question card sizing, hover cards on touch, linked-brief panel, timeline tile) are site-wide in
    the page script and styles, so a brief gets them by being on the page; nothing per brief.
- **S3. Mechanical checks.**
  - verify --mech (G-MECH), which includes the card check;
  - `tools/spine/squeeze_check.py <page> <changed briefs>` (0 squeezed) and, when pointers or titles changed,
    `tools/spine/pointer_check.py <page> <briefs>`; legib_audit only in a layout batch (token rules).
  - Then restart, except in a patch (section 8b) (Jonathan 2026-10-17, s146 cost review): rewrite the handoff State with S3 done and send only "S3 done. Paste into a fresh chat: Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md." The review and ship steps run in a fresh chat, which reads the batch file, each brief's boards.md, cuts.json and claim map before judging findings; so every build call made in S1 to S3 is written down there, not left in the chat.
- **S4. Review round 1.**
  - Three roles (acc, read, flags) on the models in the plan table; display only in a layout batch (token rules). For a
    brief with small additions, round 1 already reviews only the changed lines (`review_packet.py --since` the live text).
  - Packets from tools/spine/review_packet.py only.
  - Write-first lanes (Jonathan 2026-10-17, after s146 lost six receipts at the cap): the lane instructions tell each reviewer to read one brief's packet and write that brief's receipt before opening the next brief.
  - Budget per lane from a call plan: first-round acc 7 calls per brief plus 4; display 7 per brief plus 4 (its screenshots); read, flags, and acc in follow-up rounds, 5 per brief plus 4; at most 4 briefs per acc lane. The hook caps each reviewer at 25 calls, so split a lane that would need more.
  - Lane instructions (Jonathan 2026-10-17, after s146b round 1 lost six receipts and round 2 lost none): name every file in each brief folder, ban Glob and folder listings, say that every file in a parallel read counts as one call, and tell reviewers to Grep large files rather than read them whole.
  - Each lane's RECEIPT_FORMAT.md names only the lane's receipt paths: strip the line that review_packet.py writes with its own output folder when the packet is built outside the lane (s146 packet error).
  - Lane folders and INSTRUCTIONS.md come from `tools/spine/lanes.py <spec.json>` (round, lanes, briefs, budgets, the prior receipts and adjudication notes; s148 fix 5). Its budgets are the call plan above, 2 spare calls per lane at least; the gate counts the batch's earlier containers from the committed ledger (fix 3), so never cut spare calls by hand.
  - Foreground lanes (s148 fix 2): launch every lane of the round in ONE message with run_in_background false, so all receipts return in one turn and no reviewer wakes the lead on its own. Launch prompts stay short: the Role, Plan step, Lane and Budget lines, then "Read INSTRUCTIONS.md in your lane first".
  - After the round: `python3 tools/hooks/usage_ledger.py` and commit repair/efficiency/ledger_spine.csv (fix 3), and `usage_ledger.py --lead --record <wave>` (fix 7).
- **S5. Adjudicate and fix.**
  - Every HIGH and MED, with evidence.
  - Every LOW sorted into fixed, deferred (with where it goes) or rejected.
  - Record which role found or missed what.
- **S6. Lead self-check** (section 4) on every changed line.
- **S7. Follow-up review.**
  - The same roles, on the changed lines with context, each given its last receipt: packets from `review_packet.py --since <the reviewer's last brief_text.txt>` (changes.md; it prints the changed steps for the display sheets, `sheets.py --steps`), lanes from lanes.py, launched in the foreground as in S4, the ledger committed after the round.
  - Write-first lanes, 5 calls per brief covered plus 4, display 7 per brief plus 4, with the same lane instructions as S4 (Jonathan 2026-10-17; was 4 per brief plus 2, s139). A reviewer that relays a verdict without writing its receipt counts as no receipt: relaunch it on the same lane with the call plan in the prompt.
  - A reviewer with only LOW findings returns PASS-IF (conditional PASS) with exact replacements; the lead applies the approved ones (`tools/spine/reps.py <brief dir> <receipt> --only N,...`), and verify keeps the receipts current without another round. A replacement that only adds a hedge word found in the quote its line cites counts as wording-only for the other parts (s148 fix 8, Jonathan 2026-10-18).
  - Loop S5 to S7 until READY or the budget is spent.
  - Restart point, except in a patch (section 8b) (s148 fix 1, Jonathan 2026-10-18): when the last follow-up round leaves every brief READY (or the budget stops it), rewrite the handoff State ("S7 done: all READY") and send only "S7 done. Paste into a fresh chat:" with the restart line alone in its own code block. S8 and S9 run in the fresh chat (approval records live in the presenting container).
- **S8. Final report** (section 5):
  - `python3 tools/spine/verify_all.py <brief dirs>` (three at a time; all READY);
  - register the batch with `approval.py present sNN` (no screenshots: it binds the batch files, the changelog entry
    and the built page; a layout batch may still add sheets);
  - send the report and wait for "ship".
- **S9. Ship and post-ship**, per the handoff:
  - ship.sh with AX_SESSION;
  - check version.json in Chrome; Jonathan checks the live site;
  - OPEN_WORK and the log commit;
  - Mac copies;
  - the handoff in the project and on the Mac;
  - a ledger row;
  - keep the start-up files small (s135 item 4): move the batch's history out of the handoff into its batch file, so the handoff keeps only State and the standing sections; fold settled digest lines into STANDING_DIRECTIONS as single rules, archiving the rest.

## 3. Standing calls (decide, record, disclose; never ask)

| Situation | Call |
|---|---|
| Word count over the soft cap | Superseded 2026-10-19 by "Layers, not totals" (STANDING_DIRECTIONS): keep board-keyed facts visible, move only supporting or guideline-only detail into hovers, cut nothing for length, split a two-disease brief (Jonathan decides the split), report the count. |
| A step supported only by a source about another population | Keep it only if a board source teaches the step, and label the analogy at the step itself ("as for ... in ..."). |
| A board answer differs from a guideline | Teach the board answer; the guideline goes in "In practice:". Every age, cutoff, duration, dose and interval is checked against board sources. |
| A claim with no source opened that day | Before any cut or ⚠︎ (Jonathan 2026-10-17): search the card index for the claim's two or three key terms (`cards_search.py`, plus `board_index.py show <brief>`), and for each card found read its high-yield (pink) lines, the `hy` field in repair/sources/anki/anki_index.jsonl. A card that states the claim is cited as kind "board" and the line stays. Only with no card: board-tested, label it unverified (⚠︎) and list it; not board-tested, cut it. Each cuts.json entry records the terms searched. |
| A number in a new or changed line with no quote | Find the quote or cut the number. |
| Two places decide the same action | One owner; the other points to it. |
| A study-mode leak from a repeated table or line | Mask the repeat; never delete it. |
| A parked change or a reviewer suggestion that reverses a digest decision | Reject it. |
| Reversing the lead's own earlier verdict | Allowed with a recorded reason; listed in the report. |
| A finding caused by the reviewer packet | Record it as a packet error with evidence, fix review_packet.py, and do not count it against the brief. |
| LOW findings | Sort them; none blocks. |
| A tool or check change a step needs | Allowed, with offline tests for the risky cases; the diff goes in the report (G-DIFF). |
| A display choice the spec does not cover | Follow the nearest STANDING_DIRECTIONS line and name it in the report. |
| An abbreviation (Jonathan 2026-10-12) | Very common labs and imaging are written short, from the shared allowlist (repair/efficiency/ABBREV.json; for example CBC, BUN, US, CT, CT angiography, MRI). Anything not on the list is spelled out. A new entry is added to the list and disclosed in the report. |
| A diagnosis with more than one name (Jonathan 2026-10-12) | Name it with its other names at first mention and in its differential row, for example "Conversion disorder (functional neurological symptom disorder)", because NBME often uses the less familiar name. Names come from the shared table (repair/efficiency/ALIASES.json), built from AnKing cards, NBME items and DSM-5-TR or ICD names. |
| A psych-tagged brief filed under another shelf's section (today bs-learning, tics, peds-sleep; Jonathan 2026-10-17, decision D) | A line stays when a board source of any shelf the brief is tagged for tests it. A line none of them tests moves only to a live brief that already carries it, and the brief keeps a drawer to it. Nothing is deleted; every move follows the card-search rule. No separate psych-perspective brief. |
| Text that wraps into a narrow column on phone (Jonathan 2026-10-12) | Widen it (on phone, a 5a clue takes the band's full width); never shorten content to fit a column. |

## 4. Lead self-check (S6): before the follow-up review, and again before the report

1. Every new or changed claim: the cited fact states the claim itself, not only its topic.
   - R3 example: "MSD Ascites lists nephrotic syndrome among the causes" did not support paracentesis.
2. Every age, cutoff, duration, dose and interval: board sources checked, and any difference handled per section 3.
   - R3 example: the age-based biopsy branch was missing, and IPNA's "over 12, case by case" needed the board check.
3. Every number in a changed line has a quote.
   - R3 example: "median 3".
4. Analogies are labeled at the step.
5. One owner per decision.
6. Masks:
   - every answer is masked where it repeats;
   - no label or first cell gives away a masked answer (lint mask-leak answered); contrast only in a layout batch.
7. Bank:
   - lead-ins and keys agree with the body;
   - versions are bumped per the item rule.
8. Digest decisions are intact:
   - PSGN option C;
   - hedged mechanisms;
   - workups not question-led;
   - the caption "Diagnostic workup";
   - and every later line.
9. The word count is taken again after the last change.
10. Reviewer misses are recorded per role, for R4.
11. Abbreviations match the allowlist; every diagnosis with other names shows them.
12. squeeze_check.py reports 0 squeezed blocks on the changed briefs (phone, a few words per line).
13. Every cut and every removed number was searched in the card index (key terms, high-yield lines) before it was made (Jonathan 2026-10-17); the search terms are in its cuts.json entry.
14. Every card in cards.md has a disposition and `card_dispositions.py check` passes; each "covered" names the claims that teach it, and no carded fact the old brief or the bank holds was dropped without one (Jonathan 2026-10-17).
15. Every "warn lint" line from verify (tools/spine/lint.py: next-step cells with no action, missing other names, a hedge dropped from the cited quote, one decision with two thresholds, a number no quote holds) is fixed or answered in the batch file before the reviewers run (s148 fix 6). The lint is advisory: an answered warning may stand.

## 5. The final report: one message, the first one to Jonathan since launch (apart from section 6)

In this order:
1. **Decisions needed.** The target is none; only the items section 6 allows.
2. **Calls made under section 3.** One line each, with what Jonathan says to reverse it.
3. **Edit list per brief:**
   - old and new wording;
   - each new fact with its quote, source and tier (board, primary or analogy);
   - parked changes rejected, and why;
   - reversals.
4. **Word count:** the count, and any overage or cuts.
5. **Reviews:**
   - findings by severity, per round;
   - packet errors;
   - what each Sonnet role missed against Opus, and what Opus missed.
6. **Cost:**
   - measured per role (usage_ledger.py, output estimated from what each agent wrote), against the budget;
   - the lead's own tokens (`usage_ledger.py --lead --record <wave>`, one row per chat in repair/efficiency/ledger_lead.csv) and start-up context, beside the reviewer cost (s135 item 3); the batch total is the reviewers plus every lead row of the wave, against the budget, and against WAVE.json's max_lead_tokens when the launch prompt names one (shown only; the gate enforces the reviewer caps); s148 fix 7;
   - projected cost per brief at scale;
   - a proposed budget for the next batch.
7. **The closing line:** Reply "ship" to publish, or name what to change.

If Jonathan names changes:
- apply them;
- re-run S3 and S6, and S7 for any accuracy-relevant change while budget remains;
- present again.

## 6. The only reasons to message Jonathan before the final report

- A HIGH finding that no source settles either way.
- A decision not covered by the digest, STANDING_DIRECTIONS or section 3 that would change what a student learns or how the site looks. Examples: a new display pattern, merging or retiring a brief, a new entry type.
- A required hook test fails and agent steps cannot run.
- The budget runs out before READY. Stop at the cap; report the spend, what remains and the amount needed. Never exceed it.
- Anything irreversible: deleting Mac files, deleting a branch, force-pushing, rewriting history.
- The context is full (past about 350k; Jonathan 2026-10-17, was 250k). Rewrite the handoff State and send only: "Context full. Paste into a fresh chat: Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md."

Each such message asks one question, multiple choice where possible, with a recommendation.

## 7. Context discipline

- The lead reads summaries, receipts, diffs and script output, never whole briefs or pages.
- Long outputs go to files in the brief folder; the chat gets counts.
- The handoff State is rewritten after every step, so the restart line is always enough.

## 8. Patch and site-layer batches (Jonathan 2026-10-17)

- **Naming:** a patch of shipped briefs or a site-layer batch between numbered batches takes a letter after the last
  number (s146b, s146c), with its own changelog entry ("146b" in repair/changelog/axlog.py); ship.sh and approval.py
  match the exact id. Numbered batches keep the plan's numbering.
- **Site-layer batches** (navigation, layout, scripts or styles; no brief content changes), as in s146c:
  1. build a pilot from the live page with a script (repair/pilots/<name>/), publish it as a private artifact, and let
     Jonathan try it; revise until he approves it;
  2. generate the batch from the live page with the same changes (repair/sNNNx/gen_*.py writing the *.json);
  3. run the build, gate, render, preflight and vendor checks, legib_audit on the briefs the change touches, and
     screenshots at the widths it affects; confirm every brief is byte-identical unless the batch moves it;
  4. a tool or check change it needs follows section 3 (offline tests; the diff in the report);
  5. present with approval.py, then ship on "ship".
  No reviewer agents run when no brief content changes; any brief content change makes it a normal batch.

## 8b. Patch pipeline (Jonathan 2026-10-24)

Jonathan, 2026-10-24: "we need to be even more token efficient with the whole process". The lead is about 90% of a
batch's cost and nearly all of it is the conversation re-read on every call, so a patch keeps lead calls few and short.
Adopted: pipeline scripts, delta-ready intake, no restarts in patches, one reviewer per lane (DECISIONS_DIGEST).
A patch is any batch of small additions to shipped briefs (rows, lines, hovers, renames; no new brief).

1. **Intake is delta-ready.** The board-brief skill writes each change proposal with, per edit, the exact old HTML on
   the live brief, the new HTML, and the facts_spec rows (fact id, source file under repair/sources, title, verbatim
   quote; AnKing cards by note id). The patch lead copies them into the folder's facts_spec_<batch>.json and
   delta_<batch>.json without re-scoping. Every ship marks its queue.csv rows "picked up sNNN", so the next launch
   reads open rows only.
2. **Folder layout** (as s150e): baseline_<batch>.html (the live brief), baseline_brief_text_<batch>.txt
   (review_packet.text_of of it), claims_before_ and facts_before_<batch>.json, facts_spec_ and facts_<batch>.json,
   delta_<batch>.json, and build.py calling repair/migration/spine/<batch>_delta.py (copy the latest one and rename).
   A restated shipped line carries its old claim's fact ids in the delta's ids, so its shipped wording stays sourced.
3. **One chat, these commands** (the lead reads their one-line outputs; logs go to local/<batch>/):
   - launch: digest line, WAVE.json, branch wip/<batch> in both repos (private from main), restore, then
     `patch.py setup <batch>` (hooks, /root copy, tests, start-up context);
   - `patch.py s3 <batch> <folders>`: facts, builds, verify --mech, batch page, gate, render, preflight, vendor, squeeze;
   - `patch.py review <batch> <round> --opus <folders> --sonnet <folders> [--since-round K]`: packets, one lane per
     model, INSTRUCTIONS.md and LANE_PACKET.md, and the launch prompts; launch the lanes in one message, foreground;
   - `patch.py file <batch> <round>`: splits each lane's receipt.md into the acc, read and flags receipts and prints
     each brief's verify state;
   - `patch.py reps <batch> <folder> <receipt> [--only N]`: applies a PASS-IF's replacements to the delta and rebuilds
     (reps.py does not reach delta-built folders). A replacement adding a hedge word not in the quote makes read stale:
     review that brief once more;
   - verify_all, ready_gate, approval.py present, the report, ship.sh on "ship";
   - `patch.py sync <batch> "<message>" <folders>`: copies the folders, delta tool, packets, reviews and logs into the
     private clone and commits and pushes both repos.
4. **Review: one reviewer per lane.** Role patch-review (Sonnet), or patch-review-opus (Opus) for a lane holding a
   changed number, dose or next step; agent type lean-reviewer, as the gate requires. The reviewer judges the acc, read
   and flags parts of the changed lines and writes one receipt.md with a section per brief and part; READY is
   unchanged (acc, read and flags receipts current and PASS). Budget per lane: 3 calls plus 1 per brief plus 2 spare.
   A follow-up round covers only the briefs not READY (--since-round the previous round). No display part, no
   screenshots (token rules).
5. **Report and post-ship** as sections 5 and 2 S9, in the same chat; the report's cost line names the lead calls.

Measured, s150e (six briefs): reviewers 6 agents, 20 calls, 0.46M tokens across four rounds.

Where these rules live: here and in DECISIONS_DIGEST only. STANDING_DIRECTIONS.md, WORKUP_5A_SPEC.md and
MIGRATION_CONTRACT.md are hashed into every acc and read receipt ("specs", tools/spine/verify.py), so any edit to them
makes every shipped brief's receipts stale (found at the s150e ship). Process-only rules never go into those files;
brief-content rules do, and are edited only in a batch that re-reviews.

## 9. Closing a batch (Jonathan 2026-10-12)

Closing a batch: the post-ship report ends with the complete launch prompt for the next batch (batch id, briefs, budget, decisions needed), ready to paste into a fresh chat unchanged.
