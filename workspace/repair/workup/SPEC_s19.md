# s19 drafting spec: UWorld batch backfills and new briefs

You are drafting content for the AxBx study page `/home/claude/axbx/index.html` (USMLE Step 2 CK / pediatrics and FM shelf prep for a third-year medical student). READ-ONLY on index.html. Write only your output JSON file.

Read first:
1. `/root/.claude/skills/synced/6000d04b-e2f3-468a-8f85-28456b38ad2a_0da4c745-3832-44b3-9734-e17c6361b511/board-brief/SKILL.md` (the authoring method; follow Parts 1 to 4 and 8) and its `references/WORKED_BRIEF.md`.
2. `/root/.claude/skills/synced/6000d04b-e2f3-468a-8f85-28456b38ad2a_0da4c745-3832-44b3-9734-e17c6361b511/study-page-builder/SKILL.md` (page contract: block classes, masking, bank items).
3. `/home/claude/axbx/repair/sources/s19_questions.md` (the condensed UWorld questions and explanations; your source).
4. The owning brief(s) you are assigned, in index.html, in full. For a new brief, also read two existing board-style briefs as models: `bs-spherocytosis` and `bs-sickle-trait` (class `brief bs`), and a "Diagnostic workup" table (e.g. in `septic-hip`).

## Scope rule (the user's top concern right now)
Step 2 CK level. Content comes from the UWorld explanation in s19_questions.md plus standard, commonly taught Step 2 facts. Do NOT add specialist-level detail (named assays, rare genes, subspecialty thresholds, second-line specialist tests) that a Step 2 question would not test. When in doubt, leave it out. Any specific number or claim not in the explanation and not standard Step 2 teaching gets ` ⚠︎` in place, or is omitted. Do not use ⚠︎ on standard facts.
Emphasize decision cutoffs (ages, sizes, timing thresholds) and the specific tells that separate the key from its mimics; the user asked for this explicitly.

## Voice
Plain, natural clinical English; concise; no slogans or aphorisms; no em dashes (use commas, semicolons, colons); no emojis; American spelling. Bold only deciding words. Never reproduce vendor text verbatim or embed vendor images; paraphrase. No option letters or selection percentages in learner-facing text.

## Bank items (both tasks)
Each item is an object: {"brief","type","stem","key","companion","d1","d2","lead"(or null),"src"("uworld" for the source question, else "authored"),"nid"(space-separated nids for the source item only, else null)}. Plain text, no HTML (the assembler escapes it). Types: next, dx, test, mech, avoid, screen, stage, claim; the key and both distractors must be the same category (Rule 13). Use `lead` when the default prompt would misstate the task (defaults: next "most appropriate next step in management?", dx "most likely diagnosis?", test "most appropriate test?", mech "most likely cause, organism, or complication?", avoid "contraindicated or should be avoided?", screen "most appropriate screening or preventive measure?"). NBME lead-ins: "Which of the following is the most appropriate diagnostic study to obtain at this time?", "Which of the following laboratory studies is most likely to confirm the diagnosis?". Stems describe the patient only (no task phrase inside the stem), standalone (no "same patient"). Every distractor is a real mimic an informed classmate would weigh (no F6 dead options). Run the answer-cue check (length, grammar, repeated stem words, specificity) on every item. The source item reproduces the question's decision with paraphrased facts and uses the original key and two of the most tempting original distractors.

## Task A: backfill an existing brief -> output
{"kind":"backfill","edits":[...],"items":[...],"notes":"..."}
edits are ledger ops: {"scope":"brief:<id>","op":"insert_before"|"insert_after","anchor":"<exact text, occurs exactly once in that brief>","text":"<html>","why":"..."} or {"scope":"brief:<id>","op":"replace","old":"<exact, once in brief>","new":"<html>","why":"..."}. Verify each anchor/old occurs exactly once inside the brief's div with a script before finishing. Items are appended to the brief's existing `<ol class="bank...">` by the assembler; do not put <li> in edits. Prefer adding to existing structures (a row in the existing differential table, a `.pearls`/`.danger` block with `<span class="lbl">Label</span>`, a line in the Diagnostic workup table) over new tables. 2 to 4 new items per source question, including the source item. Do not duplicate items already in the bank.

## Task B: new brief -> output
{"kind":"new","id":"bs-<slug>","system":"<system h3 id>","shelf":"<data-shelf value e.g. 'peds' or 'fm peds'>","nav_label":"<short nav text>","html":"<the full brief div>","items":[...],"notes":"..."}
The html is a complete `<div class="brief bs" id="bs-<slug>" data-shelf="...">` ... `</div>` in the page's board-style format: h4 title (the concept, Rule 14), `<p class="sub">` subtitle ("<short tell> · UWorld · <decider as a question>"), `.vignette` source block (Pt · Labs · Q lines, paraphrased; one vignette per source question), `.dp` decision point, `.crit` criteria tile when earned, ONE differential table (data-mask on the discriminator column), a "Diagnostic workup" table ONLY if the topic has a test sequence (Test | Order | Result | What it points to; data-mask="4"; Order values Screen, First, Next, By branch, Supports, Confirms, Cause, Staging, Skip), then exactly `<h5 class="authored-hdr">Scenario bank</h5>\n<ol class="bank authored">\n</ol>` (empty; the assembler fills it), then `.danger` management line if earned, `.pearls` Pearls, `.pearls` "Pairs with" (verified existing brief ids only, use their visible titles in <b>), `.rule` Transferable rule, `.traps` traplines for the original distractors (pattern pills as in existing briefs). 5 to 8 items total. Keep it compact: roughly 400 to 700 words before the bank.
System h3 ids on the page: check with a grep for `<h3 class="system" id=`.

Validate the JSON parses. Final reply: what you drafted, items count, anything uncertain, and any conflict with existing page content.
