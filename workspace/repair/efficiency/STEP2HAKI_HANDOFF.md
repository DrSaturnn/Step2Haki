# Step2Haki handoff (repo copy for cloud sessions)

Started 2026-10-14 for s138, the first batch run directly in Claude Code on the web (DECISIONS_DIGEST 2026-10-14 s138
launch, item 3). The project handoff (claude.ai project and Documents/Step2Haki) is not reachable from the cloud; this
file holds the State and the cloud session start. Restart line: `Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.`

## State
- Batch: s138 (R5 batch 3). Branch wip/s138 (from main 11e430b). Batch file: repair/s138/S138.md.
- Briefs: ssri-effects (psych/N4), antipsych-effects (psych/APAE), somatic (psych/SOMA), gppd (psych/N6), and
  lithium-effects (psych/P2; finish the held s137 glance rebuild, repair/s137/held: S6 to S8; round 1 receipts in
  repair/migration/spine/reviews/lithium-effects_{acc,read,flags}_r3.md, display_r4.md).
- Budget (whole batch): 20 agents, 160 API calls, 9.5M tokens (WAVE.json, wave s138 open).
- Step: S4 round 1 running (8 lean reviewers: acc, read, flags, display x drug pair ssri-effects + antipsych-effects
  and disease pair somatic + gppd; lanes repair/efficiency/lanes/s138/r1/<part>-<pair>/<brief>/). lithium-effects READY
  (S7 done: receipts acc_r4, read_r4, flags_r4, display_r5; replacements acc.1, read.2 applied).
- S1 and S2 done for all four (boards.md, adjudication.md, cuts.json in each spine folder, local-only); S3 clean on the
  combined preview (gate, render, preflight, vendor, numbers; legib 0 except the live page's pre-existing "Stack" button
  in flat mode). Words: ssri 1,050, antipsych 1,042 (drug cap about 1,000), somatic 1,250, gppd 1,022.
- Spend before round 1: 4 agents, 20 API calls, 366k tokens.
- Open with Jonathan: wip/s135, wip/s136, wip/s137 kept ("keep for now"); "Recall" name kept (s137 item 2, unanswered).

## Cloud session start (replaces bootstrap.sh's Mac staging)
1. The repo is cloned at /home/user/Step2Haki. Add and clone the private repo (add_repo DrSaturnn/Step2Haki-private,
   then `git clone --depth 1 https://github.com/DrSaturnn/step2haki-private /home/user/step2haki-private`).
2. Restore local-only: `cp -rn /home/user/step2haki-private/local-only/. /home/user/Step2Haki/workspace/` (gitignored
   paths; the permission check asks once).
3. Hooks: tools/hooks/common.py maps roles.json's /home/claude/Step2Haki paths onto the actual checkout (s138). Install
   into /root/.claude/settings.json (PreToolUse agentgate on Agent|Task, callgate on all; UserPromptSubmit approval.py
   hook), `mkdir -p /home/claude/.config/axbx/hooks`, then `python3 tools/hooks/test_hooks.py` (80 of 80 on 2026-10-14).
4. `python3 tools/hooks/usage_ledger.py --context` (lead 71,421 on 2026-10-14; baseline 130,263).
5. The Agent tool must list step2haki-tools:lean-reviewer (it did on 2026-10-14).
6. Shipping from the cloud: the session's GitHub access pushes; no Mac copies; the deploy is checked from version.json
   (may lag a few minutes); new or changed local-only files are copied back to step2haki-private and pushed there.
