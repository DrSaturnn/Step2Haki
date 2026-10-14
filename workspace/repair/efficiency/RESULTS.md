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

# Part 2: this chat (orchestrator), measured 2026-09-24
From the session transcript (`tools/session_usage.py`): 399 main-thread calls; 170M cached tokens read, 3.6M written, 0.48M output. Context grew from ~190k after the last compaction to ~670k, so later calls each re-read ~5x more. Batches: s25 22 calls 6.7M read; s26 22 calls 7.5M; s27 (Aquifer) 30 calls 12.6M; s28 19 calls 7.9M; the NBME build 106 calls 60.6M. By comparison the subagent saving from worker packets is ~50k per brief. The orchestrator's context size and call count dominate cost.

Lean arm for the orchestrator: fresh chat seeded with CURRENT_STATE.md; `tools/ship.sh` (one call replaces ~6); summary-only tool output; short agent reports; text over images.
Frozen test (before/after, not randomized; the orchestrator cannot be run twice on the same batch): the next comparable UWorld batch of 4 to 8 questions in the fresh chat versus s25/s26 (mean 22 calls, 7.1M read). Adopt the fresh-chat routine as standing practice if read tokens per batch fall by at least 60% with the gate, render and blinded quality spot-check unchanged. Confounds: batch difficulty and size differ; report calls and read tokens per question as well as per batch.

## s135 efficiency item 6: lean reviewer type and staggered launches (probe s135-probe, 2026-10-13)

Three read-review agents as `step2haki-tools:lean-reviewer` on Sonnet, each reading a one-line packet and writing a two-line receipt (all three receipts correct; launch gate, call gate and ledger recorded them). a1 launched alone; a2 and a3 launched together after a1 finished.

| Agent | Calls | First call: cache write | First call: cache read | Total tokens |
|---|---|---|---|---|
| a1 (alone) | 3 | 10,870 | 0 | 36,317 |
| a2 (after a1) | 3 | 7,032 | 3,838 | 36,325 |
| a3 (with a2) | 3 | 7,032 | 3,838 | 36,257 |

- Start-up context of the lean type: about 10.9k tokens, against about 83k for the general agent type (s133, s134).
- Staggering: a later launch reads about 3.8k of the 10.9k start-up from the cache (the shared system part); the rest (about 7k) is written again per agent. Small gain; launching one reviewer first is worth it only when it costs no wall time.
- Probe cost: 3 agents, 9 calls, 108,899 tokens, inside the standing 2M safeguard allowance.
