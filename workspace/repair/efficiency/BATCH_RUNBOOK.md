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
6. the batch file, claude/pending/<batch>.md;
7. claude/pending/BRIEF_AMEND_LIST.md;
8. claude/design/WORKUP_5A_SPEC.md.

**Restart line**, the same every time; Jonathan pastes it when a chat fills: `Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.`

## 1. Launch

The launch prompt names:
- the batch id and its briefs;
- the budget for the whole batch, all rounds included: agents, API calls, tokens;
- any decisions for this batch.

The lead's first acts:
1. Write the launch prompt's decisions to DECISIONS_DIGEST in Jonathan's words (G-DECIDE). Write the budget to WAVE.json.
2. Do the session start from the handoff:
   - clone the repo;
   - restore local-only by direct staging (nothing written into Documents);
   - install the token;
   - install the hooks and run their tests.
3. Rewrite the handoff State: batch id, briefs, budget, step, spend.

Then run section 2 to the end without asking.

## 2. Steps (each ends with a rewrite of the handoff State)

- **S1. Board evidence first.** For each brief, before any build or fix:
  - Search the board sources for the topic:
    - NBME items: the bank's "How NBME framed it" blocks and the nbme-intake log;
    - the local UWorld question files (repair/sources/s*_questions.md);
    - AnKing (tools cards_search.py).
  - Write boards.md in the brief folder: each testable claim, the Step 2 answer, its source and id. Cite these facts as kind "board" in facts.json. No vendor wording reaches the page.
  - Only then go to MSD, guidelines and other primary sources (fetch.py), for mechanism, numbers and support. Where one differs from the board answer, teach the board answer and put the difference in an "In practice:" hover.
  - In the first batch only, report how much the local UWorld files cover (question count, systems).
- **S2. Build or reconcile.**
  - Parked builds: adjudicate every change in the diff against live as ACCEPT, REJECT or PARTIAL, with evidence. Never reverse a digest decision.
  - Convert the workup to 5a (claude/pending/pilot5a), with a clue for every test.
  - Drop header lines and apply the brief's Needs codes from the amendment list.
- **S3. Mechanical checks.**
  - verify --mech (G-MECH);
  - legib_audit with 0 failures in sculpted, flat and study, on phone and desktop.
- **S4. Review round 1.**
  - The four roles on the models in the plan table.
  - Packets from tools/spine/review_packet.py only.
  - The hook caps each reviewer at 25 calls.
- **S5. Adjudicate and fix.**
  - Every HIGH and MED, with evidence.
  - Every LOW sorted into fixed, deferred (with where it goes) or rejected.
  - Record which role found or missed what.
- **S6. Lead self-check** (section 4) on every changed line.
- **S7. Follow-up review.**
  - The same four roles, on the changed lines with context, each given its first-round receipt.
  - At most 10 calls each.
  - Loop S5 to S7 until READY or the budget is spent.
- **S8. Final report** (section 5):
  - preview and screenshots;
  - register them with `approval.py present`;
  - send the report and wait for "ship".
- **S9. Ship and post-ship**, per the handoff:
  - ship.sh with AX_SESSION;
  - check version.json in Chrome;
  - OPEN_WORK and the log commit;
  - Mac copies;
  - the handoff in the project and on the Mac;
  - a ledger row.

## 3. Standing calls (decide, record, disclose; never ask)

| Situation | Call |
|---|---|
| Word count over the soft cap | Up to 5% over, made of board-tested content or fixes for findings: keep it and list it. More than 5%: cut lines no board source tests (adult-only lines in a peds brief, mechanism hovers) until within 5%, and list each cut with its words so Jonathan can restore it. Recount after the last fix. |
| A step supported only by a source about another population | Keep it only if a board source teaches the step, and label the analogy at the step itself ("as for ... in ..."). |
| A board answer differs from a guideline | Teach the board answer; the guideline goes in "In practice:". Every age, cutoff, duration, dose and interval is checked against board sources. |
| A claim with no source opened that day | Board-tested: label it unverified (⚠︎) and list it. Not board-tested: cut it. |
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
   - contrast shows 0 failures in every mode.
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
12. Phone screenshots: no text squeezed into a narrow column (a few words per line).

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
   - measured per role (usage_ledger.py), against the budget;
   - projected cost per brief at scale;
   - a proposed budget for the next batch.
7. **Screenshots** registered with `approval.py present`: phone and desktop, sculpted and study.
8. **The closing line:** Reply "ship" to publish, or name what to change.

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
- The context is full (past about 250k). Rewrite the handoff State and send only: "Context full. Paste into a fresh chat: Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md."

Each such message asks one question, multiple choice where possible, with a recommendation.

## 7. Context discipline

- The lead reads summaries, receipts, diffs and script output, never whole briefs or pages.
- Long outputs go to files in the brief folder; the chat gets counts.
- The handoff State is rewritten after every step, so the restart line is always enough.

## 8. Closing a batch (Jonathan 2026-10-12)

Closing a batch: the post-ship report ends with the complete launch prompt for the next batch (batch id, briefs, budget, decisions needed), ready to paste into a fresh chat unchanged.
