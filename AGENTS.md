# Step2Haki: instructions for Codex

Step2Haki is a Step 2 CK study page (workspace/index.html, deployed from discriminator-briefs-site/ by Vercel). Its
briefs are built in batches by a lead agent under a runbook. Since 2026-10-21 Codex (GPT-6.1 Sol) may lead batches in
the interim while Claude's usage is limited (DECISIONS_DIGEST 2026-10-21).

**Status 2026-10-23: Claude leads again** (Jonathan: "I’m transitioning back to Claude as lead"; DECISIONS_DIGEST
2026-10-23). Codex does not take the lead lock or launch, build or ship a batch unless Jonathan assigns it again in
writing; CODEX_LEAD.md is dormant until then.

Who it is for: Jonathan, a third-year medical student, studying for USMLE Step 2 CK. Each brief is one topic (a
disease, or a presentation hub that sorts a complaint into its diagnoses) built on the "decision spine": numbered steps
from the presentation to treatment, a differential, a diagnostic workup, practice questions with a reason under every
choice. What a brief teaches must be what Step 2 rewards: board sources first (NBME, then UWorld, then AnKing cards),
then primary sources, every fact with a verbatim quote. Teaching something wrong defeats the purpose of the page.
Jonathan decides content and display; the lead decides only what the runbook's section 3 lets it decide, and records
every call for his approval report.

Before anything else, read in this order:
1. workspace/repair/efficiency/STEP2HAKI_HANDOFF.md, the State section (current batch, step, spend, Lead line);
2. workspace/repair/efficiency/CODEX_LEAD.md (what differs when Codex leads: the lock, doc locations, hooks, reviews,
   cost, shipping, and the authoring failure modes to avoid);
3. workspace/repair/efficiency/BATCH_RUNBOOK.md (the process; its read list, with the paths mapped by CODEX_LEAD.md
   section 1).

Restart line (Jonathan pastes it to continue an open batch):
`Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.`
For Codex it means: take the lock per CODEX_LEAD.md section 0, then follow the runbook from the State's step.
A launch prompt (a new batch id) means: CODEX_LEAD.md section 2 item 4 (create wip/sNN in both repos), then section 2a
(which build to copy) and section 7 (failure modes, read before S1); a launch that names new briefs also follows
section 9. New board questions with no batch open go through the board-brief skill (intake only; it never edits the
page).

Hard rules, always:
- Accuracy over speed. Every fact comes from a board source (NBME, UWorld, AnKing) or a primary source fetched that day
  with tools/spine/fetch.py, with a verbatim quote. Teach the Step 2 answer.
- No vendor text (UWorld, NBME, AnKing wording) in this public repo. The private repo DrSaturnn/Step2Haki-private holds
  the sources and must never be copied into this one.
- No emojis, no em dashes. Commit as DrSaturnn with the noreply email. Never print a token.
- Never change ship.sh, the gate, approval.py or any check to make work pass. Since 2026-10-23 Codex ships its own
  batches, and only after Jonathan replies with the plain word "ship" to the presented screenshots (CODEX_LEAD.md
  section 5: S8 audit in a fresh task, present, relay his reply verbatim, `AX_LEAD=codex tools/ship.sh`).
- A new brief is authored only when Jonathan names it in a launch prompt (CODEX_LEAD.md section 9).
- Stop and ask Jonathan only for the reasons in the runbook's section 6.

## Project map (added 2026-10-22)

Public repo (DrSaturnn/Step2Haki):
- `workspace/index.html`: the working page; `discriminator-briefs-site/index.html`: the deployed copy (ship.sh writes
  both). Briefs are `<div class="brief" id="<brief id>">` blocks; the practice bank is `ol.bank` inside each.
- `workspace/tools/`: page tooling. `ship.sh` (Claude, or Codex with AX_LEAD=codex), `gate.py`, `render.js`, `preflight.py`,
  `vendor_scan.py`, `legib_audit.py`, `apply_edits.py` (edits files; see `tools/EDITS.md`).
- `workspace/tools/spine/`: the brief pipeline. Build: `outline_render.py` (rendering, incl. the 5a workup `w5a`),
  `dump_lines.py` (live lines), `facts_from_spec.py`, `quote_check.py`, `fetch.py` (the only way to open a web
  source). Board evidence: `board_index.py`, `cards_search.py`, `card_dispositions.py`, `bank_items.py`. Checks:
  `verify.py`, `verify_all.py`, `lint.py`, `shingle_check.py`, `outline_check.py`. Reviews: `review_packet.py`,
  `lanes.py`, `reps.py`, `condpass.py`. Screens: `shots.py`, `shots_all.py`, `sheets.py`. Each tool's usage is in
  its docstring (`sed -n 1,20p <tool>`); `test_*.py` beside it are the offline tests.
- `workspace/tools/hooks/`: Claude Code hooks and `agents/lean-reviewer.md` (the reviewer preamble). Codex does not
  run the hooks (CODEX_LEAD.md section 2).
- `workspace/repair/efficiency/`: every governing doc (handoff, runbook, CODEX_LEAD, CODEX_AUDIT, STANDING_DIRECTIONS,
  DECISIONS_DIGEST, SPINE_SCALE_PLAN, WORKUP_5A_SPEC), the budgets (WAVE.json), ledgers, ABBREV.json, ALIASES.json,
  board_terms.json, and review lanes (`lanes/<batch>/`).
- `workspace/repair/sNNN/`: one folder per batch: the batch file `SNNN.md` and the `10_<id>_spine.json` (and
  `40_presentations.json`) files that `repair/build.py sNNN` applies to the page. Read the newest (s149) as the model.
- `workspace/repair/changelog/axlog.py`: the reader-facing changelog (one entry per ship).
- `workspace/repair/migration/spine/reviews/`: review receipts (`<brief>_<part>_r<round>.md`); `.../spine/packets/`.
- `workspace/OPEN_WORK.md`: one history line per ship (current). `workspace/CHANGELOG.md`: commit log (generated).
- Stale, do not follow: `workspace/CURRENT_STATE.md`, `workspace/PENDING_DECISIONS.md`, `workspace/repair/merge_plan.md`,
  anything under `workspace/repair/archive/` and the batch folders before s141 (history only).

Private repo (DrSaturnn/Step2Haki-private; never copied into the public one):
- `local-only/`: restored over `workspace/` with `cp -rn` at session start. It holds `repair/sources/` (AnKing index,
  UWorld question files, NBME intake, Aquifer cases, the web cache that fetch.py fills), `repair/migration/<shelf>/<brief>/`
  (each brief's folder; the spine work goes in its `spine/` subfolder: build.py, facts_spec.json, facts.json,
  boards.md, cards.md, cards_disposition.json, cuts.json, tail_fix.json, adj_<batch>.md), and `local/` (shots, legib).
- `claude/`: mirrors of the claude.ai project docs (SPINE_SPEC.md, pending/BRIEF_AMEND_LIST.md, pending/BATCHES_*.md,
  pending/FOLDERS_S142_S160.md) and `claude/skills/` (the Step2Haki skills). Its STEP2HAKI_HANDOFF.md is a copy; the
  live handoff is the public one.

The claude.ai project "Step2haki" (Jonathan's) is not reachable from Codex; everything a batch needs is in the two
repos.

