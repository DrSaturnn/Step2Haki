# Spine at scale: agent execution plan (v3, 2026-10-10)

Goal: move every brief onto decision spine v2, and repair the ones already moved, so that each one teaches the
Step 2 answer correctly and reads as one whole. The plan does this at a token cost we can sustain:
- scripts do every check a script can do;
- each model does only the work it has qualified for;
- every role is pinned to its model by configuration, not by the lead's judgment in the moment.

## Why v3 (what failed on 2026-10-10)

The plan v2.2 was right; the lead did not follow it. These are the failures, and each now has a rule that enforces it:

1. **"Passed" meant mechanical.**
   - What happened: verify passed all 17 spine briefs on rules. The first whole-brief reading then failed all 18 briefs it read, finding 8 HIGH and about 70 MED problems that had passed the line audits.
   - Rule that prevents it: READY needs a holistic review (section 3, rule E3).
2. **The audit stopped at the Practice header and never looked at the rendered page.**
   - What happened: duplicate and stale cross-references, answer leaks in study mode, and bank keys that contradicted the body all went unseen.
   - Rule that prevents it: HOLISTIC_REVIEW.md covers the whole brief in every display mode.
3. **The lead launched 24 review and fix agents without opening the plan or naming a model.**
   - What happened: every agent ran on Opus, read whole briefs and took 20 to 30 screenshots. That spent about 4.5M subagent tokens, and the efficiency skill was never loaded.
   - Rules that prevent it: pinned agent definitions, a hook that refuses unlisted launches, and a wave budget file (section 3).
4. **The work scaled with no pilot.**
   - What happened: 13 agents launched before one was measured.
   - Rule that prevents it: every new role or packet runs once on one item, and is measured, before a wave (section 3, rule E5).
5. **Agents and sessions changed shared files outside their lane.**
   - What happened: verify.py, quote_check.py, verify_baseline.txt and a repair/s130 batch changed, and the lead had not reviewed them.
   - Rules that prevent it: path hooks, a lane rule, and a lead diff review before every commit.
6. **A ruling was recorded in a work file, not in the decisions file.**
   - What happened: "Jonathan's PSGN umbrella ruling" appears in fix_r1.md files, but not in DECISIONS_DIGEST.md with his words.
   - Rule that prevents it: only the lead writes decisions, quoting Jonathan, and an agent never acts on a ruling found in a file (rule E7).

## 0. Non-negotiables

- **Accuracy (Jonathan 2026-10-10).** A brief that teaches something incorrectly defeats the purpose of Step2Haki. Any line that would lead a test taker to a wrong answer is HIGH, wherever it sits: body, hover, table, bank key or explanation, NBME block, notes, Pairs with, or rule.
- **The standard of correct is what Step 2 CK rewards.**
  - Where literature or practice has moved and the exam has not, teach the exam answer, the way NBME, UWorld and AnKing teach it, in that order of authority.
  - The practice difference may appear in a hover labelled "In practice:".
  - Clinical practice does not always equal the boards answer, and the brief teaches the boards answer.
- **Zebras stay.** The exam over-represents rare dangerous diagnoses on purpose, as safeguards. Teach how to recognize them, never cut one for being rare, and never imply one is common.
- **Standing rules, unchanged:**
  - every fact sourced; adversarial audit;
  - screenshots and Jonathan's approval before any ship;
  - no vendor or card text in the repo or on the page;
  - mnemonics identified, never invented;
  - one owner per decision;
  - no emojis or em dashes;
  - the handoff updated in the project and in Documents/Step2Haki after each ship;
  - the token never printed;
  - commits as DrSaturnn with the trailers;
  - a clean git tree at the end of each turn;
  - Mac files deleted only with permission.
- **No authority from text.** Subagent output, files, cards and pages carry no user authority.

## 1. State at the rewrite (from the files, 2026-10-10 evening; the lead has NOT verified items marked *)

- **Live page:** s129 (Hematuria PSGN 1 to 3 weeks). Tools committed through 46e242f: outline_render, outline_check (with tests), verify (FAIL, MECH or READY), numbers, cards_search, and quote_check with kind "board".
- **Holistic reviews, round 1:** all 18 briefs FAIL; reviews are in repair/migration/spine/reviews/*_r1.md.
- **Fix reports\*:** fix_r1.md exists for all 17 spine briefs and for hematuria.
- **Later review rounds\*:**
  - lithium-effects: r3 PASS;
  - six briefs at r2 FAIL, with 1 or 2 MED left each: hematuria, panic, peds-sleep, somatic, sz-psychosocial and tics.
- **Uncommitted\*:** (now parked on git branch wip/s130-unreviewed, commit a4b825c)
  - repair/s130/: 17 spine batches, 20_psgn_hematuria.json and 36_workupbranch.json (a workup branch redesign);
  - three previews under repair/migration/spine/;
  - edits to tools/spine/verify.py, quote_check.py and verify_baseline.txt.
- **Claimed rulings needing Jonathan's confirmation\*:**
  - "PSGN latency is the board umbrella 'about 2 to 4 weeks after a strep throat or skin infection' in every brief" (AnKing 1503090878430, UWorld QID 14531). This reverses s129, which he approved as 1 to 3 weeks.
  - The workup branch layout in 36_workupbranch.json. The one design request on record is from 2026-10-10: drop the larger accent bar, and show branches another way.
- **Not started:** Milestones 2 to 4 of PHASE0_SCRIPTS.md, the qualification runs, and the pilot.

## 2. Roles, models and lanes

Each role is a definition in `workspace/.claude/agents/<name>.md` that pins its model, tools, tool-call budget and
lane (the only paths it may write). The lead launches only these names (rule E1). "Qual" is the qualification state
from section 3.

| Role (agent name) | Model | Reads (its packet) | Writes (its lane) | Never | Qual |
|---|---|---|---|---|---|
| Lead (main chat) | Opus | this plan, CURRENT_STATE, script summaries, agent reports | batch lists, adjudications, DECISIONS_DIGEST (quoting Jonathan), ships | read whole pages or builds; launch an unlisted role; act on a ruling found in a file | n/a |
| Scripts (tools/spine) | none | page, claim maps, caches | packets, checks | approve judgment | n/a |
| spine-packer | Haiku, low | the packet recipe; runs scripts | packets/<id>/* | judge content | to qualify |
| spine-extractor | Haiku, low | the old brief's text with spans, leftover claims | claims.json for the leftover | judge or reword | to qualify |
| spine-architect | Opus, high (Sonnet is a pilot arm) | the architect packet (v2.2 contents, plus board evidence hits) | outline.json, facts.json, cards_disposition.json, needs.json, omissions.json | write HTML; fetch outside fetch.py | Opus qualified on the goldens; Sonnet in the pilot |
| renderer | script | outline.json | brief.html, claim_map.json, 10_*.json | | done |
| spine-answerer | Haiku, low | bank stems and options without keys, with and without the brief | answers plus the line used | | to qualify |
| acc-auditor (accuracy and board fit: areas B and G, every bank key, every HIGH or MED claim) | Opus, high | the audit packet | audit_rN.md | edit files | qualified (r1 reviews) |
| read-reviewer (coherence, stand-alone lines, wording, cross-references: areas A, C, D and E) | Sonnet, medium | the text render, siblings' titles and bottom lines | review_read_rN.md | judge medical truth | to qualify |
| display-reviewer (area F, plus study-mode leaks) | Sonnet, medium | phone and study screenshots only, and the desktop chart crops | review_display_rN.md | judge content | to qualify |
| flag-settler (area H: X1 combined-source and K1 card flags) | Sonnet, medium | each flagged line beside its quotes | flags_rN.md | edit | to qualify |
| acc-fixer (settles HIGH and MED with evidence, writes the edit list) | Opus, high | the review files, the evidence tools, the build | facts.json, outline.json or build.py, fix_rN.md | edit outside its brief folder | qualified only with a delta audit |
| wording-fixer (LOW wording, masks, cross-references) | Sonnet, medium | its review lines and the build | the same files as acc-fixer, LOW lines only | change a medical claim, number or key | to qualify |
| edit-applier (applies a Jonathan-approved edit list exactly) | Haiku, low | the approved list and the build | the build only | add, drop or reword anything | to qualify |
| canary-judge | Opus, medium | the canary diff and the audit | a verdict | | n/a |
| Approver | Jonathan | the approval packet | approve or change | | |

The holistic review (HOLISTIC_REVIEW.md) is split across four roles: acc-auditor, read-reviewer, display-reviewer and
flag-settler. A brief's review counts as PASS only when all four pass on the same brief sha. The lead merges their
files into reviews/<id>_holistic_rN.md and applies verify's READY rule to that file.

Screenshots are taken by script (shots.py), never by an agent hunting with a browser. Only the display-reviewer reads
images, and only phone, study-mode and chart crops; reading desktop is optional.

## 3. Qualification: audit each model until it does not fail

A role runs in production only after its model qualifies on cases with known answers. "Fails" means it misses
what the answer key holds, or invents a HIGH.

**Q1. Answer keys (frozen in repair/efficiency/QUAL/, local-only, never shown to the model being tested):**
- **Review roles.** Use the 18 round-1 reviews, on frozen pre-fix snapshots of their briefs. The findings the lead confirms against sources become the key; unconfirmed findings are left out. Add the 18 seeded defects from v2.2, plus new ones from today:
  - a "Pairs with" entry naming a brief twice;
  - a stale title in "Pairs with";
  - a hover with no referent;
  - a masked answer leaked by an unmasked cell;
  - a bank key that contradicts the body;
  - a newer guideline taught in place of the exam answer (restless legs);
  - an omitted zebra safeguard (Wernicke);
  - a dialysis threshold missing a board criterion (lithium);
  - an action verb in a Decides-it cell.
- **Fix and apply roles.** Edit lists with exact expected diffs, taken from the accepted s130 fixes.
- **Extractor.** Old briefs with their full span maps.
- **Answerer.** Bank items with their keys.

**Q2. Pass bar per run:**
- **HIGH recall is 100%.** One missed HIGH fails the run.
- **MED recall is at least 90%.**
- **At most 1 invented HIGH per brief.** Invented MED and LOW findings are counted and reported.
- **Mechanical roles:** verify PASS with an exact diff (applier), 100% span coverage (extractor), and answers matching the key (answerer).

**Q3. Qualifying.** The role must pass 3 consecutive runs on 3 different briefs, including the hardest one in the set (most items, a chart).

**Q4. When a run fails:**
1. Fix the packet, the rules sheet or the prompt, never the bar.
2. Run again on a fresh brief.
3. After 3 failed fix cycles, the role moves up one tier (Haiku, then Sonnet, then Opus) and that is recorded.
4. A role may move back down only through a new qualification.

**Q5. In production, the role stays under audit:**
- **Shadow (first 2 batches).** Opus re-does every qualified role's work. Any HIGH the cheaper role missed sends it back to qualification.
- **Afterwards:**
  - acc-auditor re-checks every HIGH and MED line;
  - a 1-in-5 sample of the cheaper roles' outputs is re-done by Opus;
  - each batch carries one rotating canary, judged by canary-judge.
- **Demotion.** A missed HIGH in a sample, a missed canary, or any HIGH found after a ship sends the role back to qualification. Until it requalifies, that role runs at the tier above.

**Q6. Ledger.** repair/efficiency/QUALIFICATION.md records, per role and model: run, brief, recall by severity, invented findings, tokens and the verdict. Jonathan sees it before the pilot.

## 4. Enforcement: definitions, hooks and gates

Each item has a dummy test before it is trusted (record the result in this file).

**Agent definitions.** One file per role in workspace/.claude/agents/ (tracked). Each states:
- its `model:` (haiku, sonnet or opus) and effort;
- its allowed tools;
- its tool-call budget: packer 15, extractor 8, architect 10, answerer 4, acc-auditor 12, read-reviewer 10, display-reviewer 8, flag-settler 10, acc-fixer 25, wording-fixer 15, applier 10;
- its lane, the paths it may write;
- one line pointing to its rules sheet, never the whole skill files.

**Hooks (workspace/.claude/settings.json):**
- **H1, PreToolUse on Agent/Task.** Deny any launch whose subagent_type is not one of the role names in section 2. Also deny it when its prompt lacks a "Plan step:" line naming a step in this plan. Deny the launch when repair/efficiency/WAVE.json shows the wave's agent count or token budget used up. Jonathan sets each wave's budget, or the lead does from the qualification ledger, and every launch is counted against it.
- **H2, PreToolUse on Write/Edit/Bash for subagents.** Deny writes outside the role's lane. Always deny:
  - index.html;
  - tools/;
  - repair/sNN/;
  - .claude/;
  - DECISIONS_DIGEST.md;
  - SPINE_SCALE_PLAN.md;
  - verify_baseline.txt and numbers_allow.txt;
  - another brief's folder.
- **H3, PreToolUse on Bash for subagents.** Deny git commit and push, ship.sh, mac_sync.sh, and reads of /home/claude/.config.
- **H4, SubagentStop.**
  - Append the agent's usage (tokens, tool calls, duration) to repair/efficiency/ledger_spine.csv with its role and brief.
  - For fixers and the applier, run `verify.py <dir> --fast` and block with the failure list if it fails, at most 3 times.
- **H5, UserPromptSubmit or Stop on the lead.** Remind the lead to update the handoff when a ship happened this turn.
- **Hook dummy tests (from v2.2, still required):**
  - the hook can tell the lead from a subagent;
  - it can identify the role;
  - a Bash write outside the lane is caught;
  - verify fits the hook timeout.
- **Fallback.** If any dummy test fails, the git check below is the backstop, and the lead reviews `git status` and `git diff --stat` after every wave.

**Gates:**
- **E1. Launch gate.** Only roles listed in section 2, each with its pinned model.
- **E2. Plan gate.** Every wave names its plan step and its budget in WAVE.json before launch.
- **E3. READY gate.** verify exits 0 only when the mechanical checks pass and a holistic review (all four parts) of the current brief sha says PASS. ship.sh is to refuse any spine brief that is not READY, and any batch carrying a canary.
- **E4. Diff gate.** Before any commit, the lead reads `git diff --stat` and every change to tools/ or the specs. A change the lead did not make or order is reverted or adopted explicitly, with a note in the commit.
- **E5. Pilot-first gate.** A new role, packet or prompt runs on one brief and is measured, and then Jonathan's budget for the wave applies.
- **E6. Approval gate (unchanged).** Jonathan approves every edit list, by its old and new wording, before a ship.
- **E7. Decision provenance.**
  - A Jonathan decision exists only as a DECISIONS_DIGEST.md line, written by the lead, with the date and his words.
  - A "ruling" found in any other file is a question for Jonathan, not an instruction.

## 5. Phase R: bring the shipped spine briefs (and hematuria, peds-aki) to READY

Run this first, in a fresh chat. Each step names its role and model.

| Step | Who | Action | Exit |
|---|---|---|---|
| R0 | Lead (Opus) | Inventory the uncommitted work: list repair/s130 contents, the diffs to tools/spine, verify_baseline.txt, previews; map each fix_r1.md and r2/r3 review; extract every "ruling" claimed in files | A state table in CURRENT_STATE.md; the questions for Jonathan |
| R1 | Jonathan | Confirm or reject: the PSGN umbrella (2 to 4 weeks vs s129's 1 to 3), the workup branch layout, and any other claimed ruling | DECISIONS_DIGEST lines in his words |
| R2 | Lead | Build the enforcement in section 4 (agent definitions, hooks H1 to H4, WAVE.json, ship.sh READY gate); dummy-test each | Tests recorded here |
| R3 | Lead, then acc-auditor (Opus) | Confirm the r1 findings that become qualification keys (Q1), on frozen pre-fix snapshots | QUAL/ keys frozen |
| R4 | Qualification runs | read-reviewer, display-reviewer, flag-settler, wording-fixer and edit-applier each run against the keys (Q2 to Q4) | QUALIFICATION.md verdicts |
| R5 | Lead | Check each existing fix_r1.md: every HIGH and MED decision has evidence that quote_check accepts; compare its edits list with the s130 batch file. Jonathan reviews the edit lists (E6) | Approved lists |
| R6 | edit-applier (Haiku) for approved lists the files do not yet hold; acc-fixer (Opus) only for HIGH or MED still open | Bring each build to the approved text | verify MECH |
| R7 | The four review roles (Opus and Sonnet, qualified) | Holistic review of every brief at its new sha | READY or findings |
| R8 | Loop R5 to R7 per brief until READY; then the combined preview, screenshots, Jonathan's approval, ship (s130 or split), and the post-ship steps | All 17 spine briefs plus hematuria and peds-aki READY and live |

## 6. Phase 0 remaining (PHASE0_SCRIPTS.md), reordered

1. **Enforcement first:** agent definitions and hooks (old items 12 and 13 there), the WAVE.json budget, the ship.sh READY gate, and usage_ledger.py.
2. **Milestone 2:** claims_map.py and claims_check.py (span coverage); a card_checklist score test set; packet.py with a packet per role in section 2; and rules sheets with provenance hashes. RULES_architect gains the board-standard rule, the zebra rule and the HOLISTIC_REVIEW areas.
3. **Milestone 3:**
   - answer_score.py, with the Haiku answerer;
   - canary.py;
   - the seeded-defect kit, now the Q1 keys;
   - chart specs with data, so numbers.py can check chart values. The s125 REM case is still open.
4. **Milestone 4:** batch.workflow.js, which runs only when Jonathan asks for a workflow; postship.sh; and the mutation runner.

Acceptance checks for each item are as written in PHASE0_SCRIPTS.md.

## 7. Phase 1: pilot (unchanged from v2.2, with these additions)

- **Arms:**
  - C, the current process (Opus author, Opus audit, lead fixes);
  - the Opus architect with the lean packet and scripts;
  - the Sonnet architect with the same.
- **Audit in every arm.** The full holistic review, with its four parts, by qualified roles. The acc-auditor is Opus in every arm, and audit cost counts in every arm.
- **Tasks.** 2 reference tasks (psych spine briefs rebuilt from pre-spine snapshots under quarantine), plus 3 new FM or peds tasks (one with a claim map, one without, one hard). Every task runs twice per arm.
- **Acceptance per brief:**
  - verify READY;
  - zero HIGH;
  - the HIGH plus MED count no higher than C's;
  - Jonathan's blinded review of every arm's first run;
  - answerability no lower than the old brief.
- **Adoption.** An arm is adopted only if all three hold: acceptance at least C's; no HIGH that C avoided; tokens per accepted brief down at least 25%.
- **Frozen first.** The rubric is committed before any run, in repair/efficiency/RUBRIC_spine.md. Results go to RESULTS_spine.md, with the not-proven list.

## 8. Phase 2: production loop per batch (6 to 8 briefs, one cluster, a fresh chat each)

| Step | Who (model) | Action | Exit |
|---|---|---|---|
| B0 | Lead (Opus) | Pick a cluster (entry types and lenses with a golden only); write WAVE.json budgets | Batch list |
| B1 | Scripts, spine-packer (Haiku) | Snapshot old briefs; packets for every role; quarantine assert | Packets under size targets |
| B2 | Scripts, spine-extractor (Haiku) | claims_map, then the leftover | claims_check 100% span coverage |
| B3 | Script | Harvest dropped claims | Count logged |
| B4 | spine-architect (Opus) | outline.json with final text; facts.json (fetch.py, then board evidence for any literature-vs-exam question, NBME then UWorld then AnKing); cards_disposition.json after facts are saved | outline_check PASS |
| B4.5 | Script, Lead, architect | Ownership merge (OWNERS.json); delta passes | No double owner |
| B5 | Scripts | quote_check, numbers, renderer | PASS |
| B6 | spine-answerer (Haiku) | Bank with and without the brief | Scores; misses to the audit |
| B7 | acc-auditor (Opus) and read-reviewer, display-reviewer, flag-settler (Sonnet) | Holistic review, four parts, same sha; one canary brief per batch | Review files |
| B8 | Lead | Adjudicate every HIGH and MED with evidence; reject what the evidence does not support | Dispositions logged (AMEND_LEDGER) |
| B9 | acc-fixer (Opus) for HIGH and MED; wording-fixer (Sonnet) for LOW | Edit lists with old and new text | verify MECH |
| B10 | Review roles again on changed briefs (delta plus 3 lines of context for every HIGH fix) | Loop to READY | verify READY |
| B11 | Scripts | Combined preview: gate, render.js, preflight (P1 0), vendor_scan, legib, numbers; canary absent | Clean |
| B12 | Lead | Approval packet: decisions and edits first (old and new wording), dropped list, new facts with sources, card recall and conflicts, audit counts, then phone and desktop crops | Jonathan approves |
| B13 | Lead | ship.sh (READY gate), postship (OPEN_WORK, log commit, push, version check, handoff in the project and on the Mac, mac_sync) | Live; clean tree |
| B14 | Lead | Ledger: tokens per role per brief, qualification samples, any post-ship defect becomes a rule (defect to rule) | Ledger row |

## 9. Cost controls (the efficiency skill, applied)

- **Load the efficiency skill.** Load workflow-efficiency-pilot before any multi-agent wave. Its pilot, frozen-rubric and adoption method governs every new role or packet.
- **Fresh chats.** One fresh chat per batch or phase. The lead reads JSON summaries and review counts, never whole briefs.
- **Packets only.** Workers read their packet, never skill files, the whole page or other briefs, and report a gap instead of browsing.
- **Screenshots by script.** Only the display-reviewer reads images, and only phone, study and chart crops.
- **Pinned models and capped effort.**
  - Models are pinned per role.
  - Effort is low on Haiku roles, medium on Sonnet roles, and high only for the architect, acc-auditor and acc-fixer.
  - Schema outputs are capped at 40 lines.
- **Budgets.**
  - Tool-call budgets come from the agent definitions.
  - Wave token budgets come from WAVE.json. Hitting a budget means the packet is missing something; fix packet.py.
- **Ledger.** ledger_spine.csv (written by H4) records tokens per role per brief, with the setup and qualification cost separately.
- **Stop rule.** Tokens per shipped brief, averaged over 2 batches after the shadow period, must sit at least 25% below the s123 to s127 average. If not, stop and revert that role.
- **Today's baseline, for comparison:**
  - a holistic review by one Opus agent: about 150k to 205k tokens per brief;
  - a fix by one Opus agent: about 185k to 245k per brief.
  - The split review targets under 60k per brief: Opus accuracy about 30k, Sonnet parts about 30k.

## 10. Quality safeguards (each risk, then what catches it)

Carried from v2.2 (1 to 29) with two amended for the board-evidence rule; new ones 30 to 40.

1. A claim silently disappears: script pointers, 100% span coverage including hover and chart text, the dropped list shown to the auditor and Jonathan, and the B6 stop rule (old v2.2), now enforced by the claims_check step.
2. Fabricated, paraphrased or spliced quotes: only fetch.py writes the cache; one verbatim fragment per fact; 300 characters of context for the auditor.
3. Right quote, wrong population: population and setting per fact; outline_check P1; the acc-auditor checks scope.
4. Meaning drifts at a handoff: the architect writes every word; the renderer is a script (round-trip identical).
5. The architect's decisions are wrong and get rendered faithfully: the acc-auditor attacks decisions; answerability with and without the brief; the approval packet shows decisions in words.
6. Charts carry unsourced or contradicting values: one fact id per datum; numbers.py on chart values (once charts carry data); full-resolution crops.
7. Lean packets lose context: sibling bottom lines, OWNERS.json and SPINE_SPEC rounds verbatim; drawers for owned diagnoses; the B4.5 merge.
8. Correlated blind spots (same model family): an omission lens, a rotating canary judged by a second agent, the shadow period, and Jonathan as the last check.
9. Rubber-stamp audits: a per-step checked list; a second auditor for any zero-finding audit of a brief over 900 words.
10. Fixes introduce errors: changes outside named lines reported; a delta review for HIGH fixes; preflight again.
11. Scope creep and bloat: caps enforced at the outline (C1, 2% slack then error); S2 basis for new rows; guideline-only detail in hovers.
12. Lost hedges and qualifiers: preflight P1; hedge diff against the cited fragment; Q1 and Q2 on the auditor list.
13. A bank item is lost or altered: the tail check after tail_fix; items carried; a changed stem, key or distractor must bump its version (verify items check); the gate.
14. Vendor text leaks: shingle_check (quotes, vendor files, card text), vendor_scan, local-only packets and caches.
15. Agents act outside their lane: hooks H2 and H3, lanes in the agent definitions, the git and diff gates.
16. Parallel collisions: one folder per brief, own scratch folders, nothing shared until the combined preview.
17. Spec drift: provenance hashes; verify refuses on drift; a re-pilot after a spec change.
18. Briefs without claim maps: every old line sourced or dropped with a reason; a drop touching a tested item stops for the Lead.
19. Invented mnemonics: sourced (K3, K4); existing ones keep data-mn-src.
20. Entry types or lenses with no golden: excluded until one is approved.
21. Approval fatigue: the approval packet leads with decisions and edits; batches of 6 to 8.
22. A cheap model failing a long spec: narrow schema tasks only, qualification first (section 3), and escalation after 3 failed loops.
23. Gradual decay: a per-batch quality ledger; revert a role after two batches above the s123 to s127 HIGH rate or any post-ship HIGH.
24. (Amended) Card text drifts onto the page as fact: cards may now be cited only as kind "board", meaning evidence of what the exam rewards where literature or practice differs or no fetched source covers the exam answer. The page line is always in our words (shingle_check), and card errors go to card_conflicts.md.
25. Card checklist bloat or silent cuts: anchors over Extra; must and candidate tiers; a cap of 15 candidates with the cut logged; stable hash ids; one owner per item.
26. Card wording copied onto the page: card text is vendor source for vendor_scan and shingle_check.
27. (Amended) A card steering a fact: fetched references answer mechanism and numbers first. Board evidence (NBME, then UWorld, then AnKing) settles only what the exam rewards when sources disagree, and the acc-auditor checks every kind "board" citation.
28. A deck update mid-batch: the index hash is frozen per batch.
29. Shadow period: the first 2 batches get Opus re-dos of every cheaper role.
30. "Passed" read as quality: verify's three states (FAIL, MECH, READY); READY needs the four-part holistic review on the current sha; ship.sh refuses non-READY.
31. Audit blind to the page as rendered: the display-reviewer on phone and study crops; the review covers everything from the title to the Transferable rule.
32. Cross-references stale or duplicated: area E, with every pointer checked against the live target title.
33. Study mode leaks answers or hides non-answers: area F, with masks fixed in the build.
34. A newer guideline taught over the exam answer: the board-standard rule, with board evidence required for any literature-vs-exam line.
35. A zebra safeguard omitted or implied common: the zebra rule in HOLISTIC_REVIEW and RULES_architect.
36. An unpinned or mass launch: H1 (role list, plan step, wave budget), E5 pilot first.
37. Shared files changed outside a lane: H2, the E4 diff gate, and lead review of every tools/ or spec change.
38. A ruling invented or mis-attributed in a work file: E7. Decisions live only in DECISIONS_DIGEST, in Jonathan's words.
39. Screenshot tooling hides content: shots.py forces layout (no lazy sections, instant scroll), tiles long sections and captures to the brief's end; the display-reviewer reports any slice that looks cut.
40. Review findings that are themselves wrong: the lead adjudicates every HIGH and MED with evidence before any fix (B8), and fixers record ACCEPT, PARTIAL or REJECT with evidence.

## 11. Decisions

Decided by Jonathan:
1. The plan was approved 2026-10-10; Phase 0 runs first.
2. Word caps above the practice bank: disease about 1,300, drug about 1,000, presentation hub about 700.
3. D1: a script, outline_render.py, replaces the filler. The pilot arms are C, an Opus architect and a Sonnet architect.
4. D2: the scout folds into the architect, which opens cards only after its facts are saved.
5. Jonathan does the blinded pilot review.
6. The full AnKing Step Deck is indexed.
7. s129: Hematuria PSGN latency is 1 to 3 weeks after pharyngitis (approved). A later reversal to "2 to 4 weeks" is claimed in files; see R1.
8. 2026-10-10:
   - Accuracy is non-negotiable.
   - The standard is the Step 2 answer: follow NBME, then UWorld, then AnKing where literature or practice differs.
   - Zebras are taught as safeguards.
   - Both remediation steps were approved: fix all findings and re-review until PASS; review the 14 psych briefs.
9. 2026-10-10: remake the plan with named models, qualification until each model does not fail, and hooks and safeguards (this v3).
10. 2026-10-10 (design request): drop the larger accent bar in the diagnostic workup; show each branch another way.

Still open:
- the source allowlist;
- workflow runs need Jonathan's explicit "use a workflow";
- 70 unresolved page nids, and a UWorld QID in data-nid;
- card conflicts for AnkiHub;
- the R1 confirmations;
- each wave's token budget (Jonathan sets it, or approves the lead's proposal from the qualification ledger).

## 12. History

- v1 to v2 (2026-10-09): self-audit plus an independent Opus review, with 23 findings all accepted. Changes:
  - only fetch.py writes the cache;
  - no "..." splices;
  - the architect owns final text;
  - quarantine for the pilot;
  - acceptance matches the real bar;
  - answerability with and without the brief;
  - span coverage;
  - script pointers;
  - needs as questions;
  - delta passes;
  - caps at the outline;
  - drop stops on tested items;
  - the B4.5 ownership merge;
  - FM and peds lenses with goldens;
  - charts owned and audited;
  - hook assumptions tested;
  - a canary;
  - scripted retrieval;
  - cost accounting with a stop rule.
- v2.1 and v2.2 (2026-10-09): the AnKing index wired in:
  - a checklist from the Extra field, with must and candidate tiers;
  - dispositions;
  - card text in the copy check;
  - a blind scout;
  - frozen deck hash;
  - a second independent review, with all findings taken.
- v2.2 to v3 (2026-10-10): the whole-brief failure, and the lead's process failures listed at the top. Changes:
  - roles split by model, with qualification;
  - enforcement by definitions and hooks;
  - the READY gate;
  - the board-standard rule;
  - the board evidence kind;
  - Phase R before anything else.
  - The v2.2 text is kept in git history (commit 46e242f and earlier).
