# Phase 0: the remaining scripts (build plan, 2026-10-10)

Companion to SPINE_SCALE_PLAN.md (section 2). Already built and in use: anki_index, card_checklist, inventory,
fetch, passages, quote_check, shingle_check and shots (all in tools/spine/). This file plans everything else that
has to exist before the pilot. It is ordered so that each milestone is usable on its own.

## What the goldens taught (s128), and what it changes

- Cost per golden, from the agents' usage lines:
  - Opus author: 250k to 340k tokens.
  - Two Opus audit rounds: about 300k.
  - Fix rounds and a delta audit on top.
  - Roughly 1M tokens per brief. The pilot measures it properly with tools/session_usage.py.
- The audits, not the authoring, found the costly problems. Many were mechanical and a script could have caught them first:
  - a hedge lost against its quote;
  - a number that disagrees with a bank item;
  - an adult threshold in a child brief;
  - an undefined term;
  - a card marked covered when it was not.
  - Each script below names the golden defect it would have caught.
- The build.py files are already a structured outline. Every learner-facing string is a T(text, ids) call inside a spinelib component, and the goldens use about 12 component types: bottom line, script rows, systems panel, urgent rows with chips and a commit line, tables, workup tree, criteria tile, chips (role, warn, why, drawer), notes, pause point, ladder rungs and stepper.
- So the "filler" role in the plan (a cheaper model turning an outline into build.py) can be replaced by a script. outline_render.py turns outline.json into the same HTML through spinelib.
  - This removes a whole agent and its drift risk.
  - The cheaper-model question moves to where it can save the most: can Sonnet do the architect's job with a lean packet, with Opus auditing?
  - This is decision D1 below.

## Milestone 1: the authoring loop (needed by everything else)

### 1. outline schema and outline_render.py
- **What:** a JSON schema for one brief (steps 1 to 8; each component typed; every learner-facing string is {"text", "ids"}; drawers as {"drawer": brief-id}). outline_render.py reads outline.json plus the claim map and facts.json, builds SRC the same way for every brief, and renders through spinelib.
- **Replaces:** the bespoke SRC plumbing each golden wrote for itself, and the filler role.
- **Accept:** round-trip on all three goldens.
  - An agent converts each golden's build.py into outline.json.
  - The renderer's brief.html must equal the shipped brief.html, ignoring whitespace.
  - Any difference is a missing component type.
- **Mutation tests:** an unknown component; a string without ids; an id not in SRC; a drawer to a brief that does not exist.

### 2. outline_check.py (plan 0.8)
- **Steps:** the steps allowed for the entry type; absent steps marked None.
- **Caps and counts:** word caps enforced here (1,300 disease, 1,000 drug, 700 hub); bottom line at most 3 lines; Insights exactly 2.
- **Differential rows:** each needs a tempting_because field. Decides-it cells must not be a treatment or a rule:
  - flag any cell whose text starts with a verb of action ("give", "treat", "film");
  - flag a cell whose text appears in another row of the same table.
- **Ladder:** a trigger with a time or a named failure (G2); Top rung only last (G3).
- **Numbers:** every carried number has a currency status (N1).
- **Combined sources:** a line citing facts from two source sections is flagged combined (the s124 splice in a new form).
- **Population:** a peds brief citing a fact whose population is adult or cirrhosis is flagged. That would have caught the round-1 vaccine threshold and the peritonitis row in nephrotic-child.
- **Undefined labels:** a label used three or more times and never defined is flagged. Nephrotic-child round 1 had "atypical features" and the steroid-response bands.
- **Old claims:** every old claim needs a disposition.
- **Cards:** every card item in cards.md needs a disposition in cards_disposition.json. The SCFE "tall, thin" card was marked covered but was absent; cross-check that a covered:<line> pointer names a line whose text shares the card's key terms.
- **Accept:** one mutation test per rule, and all pass on the goldens' outlines.

### 3. verify.py (plan 0.9): one command, PASS or a list of fixes
- **Runs, in order:**
  - render;
  - quote_check;
  - shingle_check (claim quotes, vendor files and card text);
  - outline_check;
  - claim map complete;
  - the bank tail byte-identical to the live brief, except listed tail_fix edits;
  - ids, items and versions carried;
  - V1 acronyms and no em dash (through content_rules);
  - a preview build in a unique directory;
  - gate, render.js, preflight (P1 must be 0), vendor_scan --page and numbers.py.
- **Then:** deletes the preview directory and checks that git shows no tracked changes.
- **Modes:** --fast (no page build) for hooks and inner loops, and --full.
- **Spec drift:** refuses to run if a rules sheet's provenance hashes do not match the specs.
- **Accept:** PASS on the 17 shipped spine briefs; each mutation from items 1 and 2 fails with its fix line.

### 4. numbers.py (plan 0.10)
- **What:** a page-wide registry of (term, number, unit, brief, source id) from brief text, chart data, and bank stems and explanations.
  - It flags the same term with different numbers in different briefs.
  - It flags a brief number that contradicts its own bank.
- **Accept, real cases:**
  - it must flag hematuria's "PSGN 2 to 4 weeks" against nephrotic-child's "1 to 3 weeks" (live today);
  - it must flag the s125 REM-at-90-minutes chart against its bank item (replayed from the s124 page);
  - it must flag the SCFE bilateral 20 to 40% against 18 to 50% (replayed from the pre-s128 page).
- **Noise control:** an allowlist for legitimately different contexts (rheumatic fever and PSGN both near "2 to 4 weeks after strep"). The report lists pairs; the Lead settles them.

## Milestone 2: inputs and packets

### 5. claims_map.py and claims_check.py (plan 0.5)
- **What:** split the old brief's learner text, including hovers, titles, SVG and chart labels, into spans. Match each span to existing claim-map rows by fuzzy text match (a script, not a model); the leftover goes to the extractor (Haiku).
- **Rules:** coverage is the union of spans, 100%. A pointer's similarity must clear a threshold, calibrated on the 17 spine briefs' old versions.
- **Accept:** mutations (dropped sentence, dropped cell, dropped hover, merged claim losing a qualifier, wrong pointer) all fail.

### 6. card_checklist.py: fix the candidate score (plan 0.6b)
- **What the goldens showed:** 42 of 148 card items were "not on topic":
  - photo-credit lines in Extra;
  - word-only matches such as preeclampsia and hydatidiform mole on nephrotic-child.
- **Changes:**
  - anki_index drops Extra lines that are image credits or source lines;
  - a candidate must name a term in its cloze anchor or Text;
  - candidates are ranked by Step 2 subject tags shared with the brief's linked cards;
  - candidates are capped at 15.
- **Accept, frozen test set:** the three goldens' dispositions (covered or owner = relevant, not-topic = irrelevant), plus 2 more briefs labeled by an Opus agent and spot-checked by the Lead. Target: at least 80% of kept candidates relevant, with no linked must card lost.

### 7. packet.py (plan 0.4)
- **What:** one file per role per brief, under repair/migration/spine/packets/<id>/.
  - **Architect:** RULES_architect, the outline schema card, SPINE_SPEC rounds 2 to 4 verbatim, DECISIONS_DIGEST, the claims with spans, dropped claims, bank keys and explanations, NBME framing, cards.md, sibling bottom lines, OWNERS.json and the facts gathered so far.
  - **Auditor:** AUDIT_PROMPT, the text render with hover text and chart data, crops, claim map with 300 characters of context, outline, bank, old text, dropped list, card dispositions, and the verify, numbers and answerability lines.
  - **Answerer** and **extractor:** see items 5 and 9.
- **Rules:** prints sizes against targets (architect 35k tokens, audit 40k). Quarantine: pilot reference briefs' spine dirs, NEW_SOURCES entries and digest lines never appear.
- **Accept:** no packet holds another brief's full HTML or a whole skill file; the quarantine assert fires on a seeded leak.

### 8. Rules sheets with provenance (plan 0.12)
- **What:** three sheets, each headed by the sha256 of every file it condenses; verify.py checks the hashes.
  - **RULES_architect.md:** AUTHOR_SPEC condensed, plus the lenses, scope rule, source precedence, reviewer items 1 and 9 to 14, and what the goldens added: cards_disposition, own scratch folder, combined-source rule, population rule.
  - **RULES_auditor.md:** AUDIT_PROMPT plus the round-2 lessons (walk every bank item through the brief; check card dispositions).
  - **outline_schema.md:** the component card the architect writes against.
- **Accept:** an Opus reviewer compares each sheet with its sources and lists anything dropped; zero dropped rules.

## Milestone 3: quality instruments

### 9. answer_score.py and the answerer packet (plan 0.11)
- **What:** bank stems and options without keys, answered twice by Haiku, once with the full render and once without. An item counts as taught only when the answer is right with the brief and wrong without it, and the cited line is found in the render. Wrong-with-brief items go to the audit packet.
- **Accept:** a baseline recorded on the 17 spine briefs. The COPD round-1 overlap error must show as wrong-with-brief when replayed on that version.

### 10. canary.py (plan 0.15)
- **What:** plants one defect per batch in one brief's audit copy, rotating through RECURRING_FAILURES and the goldens' real defects. It records the diff, and a second agent judges whether the audit caught it.
- **ship.sh guard:** refuses if any canary text is on the page.
- **Accept:** a planted canary that reaches the page makes ship.sh fail.

### 11. Seeded-defect kit for the pilot
- **What:** seeded_defects.py injects the 18 pilot defects (plan section 3) into copies of a brief and scores an audit report against the key. It reuses the canary injector.
- **Accept:** each injection applies cleanly to a golden; the scorer counts a hit only when the finding names the right line.

## Milestone 4: orchestration

### 12. Agent definitions and hooks (plan 0.13, 0.14)
- **Agents:** .claude/agents/ for spine-architect, spine-auditor (read-only), spine-extractor and spine-answerer (Haiku), and spine-scout if the scout stays separate (see D2). Each lists its allowed tools and tool-call budget.
- **Hooks:** deny git commit and push, ship.sh and token reads for subagents; on SubagentStop, the architect runs verify.py --fast.
- **First:** a dummy test of the four hook assumptions (lead vs subagent, which agent, Bash writes, timeout). The B8 git check stays regardless.

### 13. batch.workflow.js, postship.sh and usage_ledger.py
- **batch.workflow.js:**
  - per brief: extract, architect, verify, answer and audit;
  - schema outputs under 40 lines;
  - audits written to audit_rN.md files, and fixers read the file. In s128 the Lead retyped an adjudication without the findings, which cost a round.
  - It runs only on your "use a workflow".
- **postship.sh:** OPEN_WORK line, log commit, push, version check, handoff in the project and on the Mac, mac_sync, in one call.
- **usage_ledger.py:** tokens per brief per role from the session transcript into ledger_spine.csv.

### 14. Mutation-test runner
- **What:** tools/tests/spine/run.py runs every mutation above, and a row goes into MIGRATION_CONTRACT for each new check.
- **Accept:** all green before the pilot.

## Order and size

| Milestone | Items | Who builds | Rough size |
|---|---|---|---|
| 1 Authoring loop | 1 to 4 | Lead writes the scripts; one Opus agent converts the 3 goldens to outline.json for the round-trip | one session |
| 2 Inputs | 5 to 8 | Lead; one Opus agent labels 2 briefs for the card test set and one reviews the rules sheets | one session |
| 3 Instruments | 9 to 11 | Lead | half a session |
| 4 Orchestration | 12 to 14 | Lead | half a session |
| Pilot | plan section 3 | workflow run | one to two sessions |

Link repairs (inventory): one brief (bone-tumors) carries UWorld QIDs in data-nid, and 69 card ids do not resolve. A script lists them and the Lead fixes them in the batch that rebuilds each brief, not as a separate ship.

## Decisions

- **D1. Replace the filler with outline_render.py (recommended).**
  - The pilot arms become:
    - **C:** the current process, an Opus author writing build.py;
    - **H-Opus:** an Opus architect writing outline.json from the lean packet, plus scripts;
    - **H-Sonnet:** a Sonnet architect, same packet and scripts.
  - Opus audits all three arms. Haiku keeps the extractor and answerer jobs, where scripts check its work.
  - This replaces the Sonnet and Haiku filler arms you chose. The filler job disappears, and the question that saves the most (the judgment role) gets tested instead.
- **D2. Fold the scout into the architect (recommended).**
  - In the goldens the authors gathered sources themselves with fetch.py and passages.py, and quote_check verified every quote. All facts passed, and only one page needed a relayed reading.
  - A separate scout adds a handoff without adding a check. Keeping the "answer questions blind to the cards" rule is the main reason for a separate scout. The architect can keep it instead: cards.md is opened only after facts.json is written, and verify.py checks the file times.
