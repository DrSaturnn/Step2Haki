# Efficiency pilot: results (2026-09-24)

Rubric frozen before the runs: RUBRIC.md (commit 70333ed). Raw outputs, blind key and reviewer scores: runs/.

## Setup
4 real backfill tasks from the s26 batch (biliary atresia, isotretinoin intracranial hypertension, tuberous sclerosis, CVID), drafted against the page as it stood before s26. Arm C = current workflow (full spec; worker reads skill files, spec, source and page). Arm P = worker packet (condensed rules, the one source question, the brief's HTML, brief titles, verifier). Same model, same output contract, one run per arm per task. Quality scored mechanically (tools/verify_edits.py) and by a blinded reviewer against fixed checklists.

## Efficiency (Agent tool usage report)
| Task | C tokens | P tokens | C tool uses | P tool uses | C seconds | P seconds |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | 130,016 | 77,603 | 15 | 3 | 162 | 94 |
| T2 | 134,437 | 79,195 | 16 | 5 | 196 | 90 |
| T3 | 130,337 | 83,837 | 13 | 5 | 167 | 99 |
| T4 | 135,475 | 88,383 | 18 | 4 | 187 | 97 |
| Mean | 132,566 | 82,255 | 15.5 | 4.25 | 178 | 95 |

Tokens per task fell 38%; every one of the 4 pairs fell (range 35% to 41%). Tool calls fell 73%; wall time fell 47%.

## Quality
- Mechanical: 8 of 8 drafts clean (anchors unique, edits apply, gate passes, no new near-duplicates, source nids correct).
- Blinded review, accepted under the frozen rule: C 3 of 4, P 3 of 4.
  - C rejected T4: critical factual error ("any of these defects: no live vaccines", wrong for selective IgA deficiency and too broad for CGD).
  - P rejected T2: kept an aphorism that was already in the brief inside a rewritten sentence, and added nerve sheath fenestration/shunting (edge of Step 2 scope). Not a factual error.
  - Reviewer preference: P in T1 and T4, C in T2, equivalent in T3.

## Decision
Tokens per accepted task: C 176,755; P 109,673 (38% lower). P meets all three adoption criteria (acceptance equal, no critical defect that C avoided, at least 25% fewer tokens per accepted task). Adopted as the default for Task A backfills.

Two instructions added to RULES_worker.md from the failures seen (rewrite slogans you touch; do not stretch a restriction across a group).

## Not proven
- n = 4 pairs, one run each; run-to-run variance is unmeasured.
- New briefs (Task B) and Aquifer workups were not tested; they keep the current workflow until a pilot of their own.
- Control workers also found and used the new verifier, so the gain measured is mostly from context, not tooling; the true gain from the whole change may be a little larger.
- Token counts are the harness's per-agent totals, not billed cost. The orchestrator's own tokens and the one-time setup (rules sheet, packet script, verifier) are not included; packet building is a script run of under a second.
- The reviewer is the same model family as the workers.
- RULES_worker.md condenses board-brief and SPEC_s19; when either changes, re-check the rules sheet and re-run a small pilot.
