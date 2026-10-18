# s148 efficiency patch: eight changes, shipped with s148 (Jonathan 2026-10-18)

Jonathan, after the lead's token efficiency check (continuation chat 4): "can we change all 8 changes to be shipped with
this next batch". The check (measured from this chat's transcripts): the lead used 55.0M tokens against the reviewers'
5.6M (91%); lead context grew from 127k to 457k (median 333k per call), so late calls cost three times early ones;
19 acknowledgment turns cost 6.0M; the S8 phase alone was 63 calls and 26.2M at about 415k each; round 3 cost about 26M
in all, two briefs pulled in only by hedge words. Cache reads are about 89% of the lead's tokens (billed at about a tenth
of fresh input at standard API pricing). Estimated savings below are the lead's estimates, not measurements.

All eight are tool and runbook changes (no brief content), built and tested in the fresh chat, committed on wip/s148,
and shipped with s148. The ninth item, owed at the close by Jonathan's earlier call ("launch round 2 and plugin at batch
close"), is built in the same chat because fix 1 depends on cheap restarts.

## Order of work in the fresh chat
1. Session start per the handoff (the hooks install will be held once more; ask). Do NOT call register_repo_root (fix 4).
2. Build fixes 3, 5, 6, 8 with offline tests; then fixes 1, 2, 4, 7 in the runbook (repo copy and project copy); then
   the plugin (item 9) through the cowork-plugin skill.
3. Re-present s148: verify --all (fix 5) on the nine briefs (expect READY; no brief changed), the batch checks, the
   screenshots (fix 5), approval.py present s148, a short report (the s148 report already sent stands; list only what
   changed: the tools, the runbook diff, tests), then wait for "ship" and run S9.

## 1. A second restart point, before S8 (about 15M a batch)
Runbook S7: when the last follow-up round leaves every brief READY (or the budget stops it), rewrite the handoff State
("S7 done: all READY") and send only "S7 done. Paste into a fresh chat:" with the restart line in its own code block.
S8 and S9 run in the fresh chat: it reads the State, the batch file's S5 and S7 sections and the receipts' verdict lines
only; it re-presents (approval records live in the presenting container). Section 6's context rule stays (350k).

## 2. Foreground lanes (about 6M a batch)
Runbook S4 and S7: launch every lane of a round in ONE message with run_in_background false, so all receipts return in
one turn and no reviewer wakes the lead on its own. Launch prompts stay short (Role, Plan step, Lane, Budget, then "read
INSTRUCTIONS.md first"), so the prompt text stays out of the lead's context (s148 round 2 pattern).

## 3. The gate's spend survives a new container (about 3M; ends the zero-spare lanes)
tools/hooks/common.py: wave_spend() and the agent count in agentgate.py add the committed ledger
(repair/efficiency/ledger_spine.csv) rows of the wave whose agent ids have no transcript in this container (agents run in
an earlier chat). usage_ledger.py already writes those rows; the lead commits the ledger after every round (runbook S4,
S7). Tests in test_hooks.py: a wave with ledger rows from a past container is refused at its agent cap and its call cap.
Runbook: lanes get 2 spare calls again (S4 7 per brief plus 4; S7 5 per brief plus 4, display 7 plus 4: the runbook's own
numbers, which s148 rounds 2 and 3 cut to 0 spare by hand).

## 4. Fewer harness re-injections (about 4M)
Runbook session start: do not call register_repo_root (the repos have no CLAUDE.md; each registration re-sent the full
skill list, about 10k tokens, five times in s148 chat 4); use absolute paths and avoid cd into other folders in commands
(a working-folder change re-sends environment and memory context); read docs by Grep or line range, never whole when the
continuation read list allows less (s148 chat 4 printed a 24k-character batch-file section and a 20k lane file).

## 5. Lead tools in the repo (about 3M)
Move the s148 scratch tools into tools/spine/, parameterized, with tests where they decide anything:
- lanes.py (from lanes.py, lanes2.py, lanes3.py): writes a round's lane folders and INSTRUCTIONS.md from a JSON spec
  (round, groups, parts, briefs, budgets, the prior round's receipts and adjudication notes); round 1 full packets, later
  rounds review.md (last receipt, adjudication, diff) and round1.md for display.
- review_packet.py --since <old brief_text.txt>: changes.md diffs against the reviewer's last version (replaces diffs.py),
  and prints the changed step numbers (for display sheets).
- sheets.py --steps 1,3,4: packs shots.py images into review or approval sheets (from sheets.py; its own approval mode
  writes phone, phone-study, desk and desk-study per brief).
- reps.py: applies receipt replacements to build.py, tail_fix and head_fix sources, exactly once each, and reports
  misses (tail text with markup is reported, not forced).
- verify_all.py: runs verify.py on a list of brief folders, three at a time (nine at once timed out render.js), and
  prints one READY line per brief.
- shots.py --all-modes: phone, phone-study, desktop and desktop-study in one sequential run (four parallel runs were
  killed for memory).
- remap_disp.py (cards remap by claim text) and hand_disp.py, if still needed.

## 6. Pre-review lint (the lever behind round 3, about 26M a round avoided)
tools/spine/lint.py, run by verify --mech as advisory warnings and listed in the S6 self-check (runbook section 4, new
item 15). It catches the recurring round-1 MED categories before any reviewer runs:
- clue-table Next best step cells with no action (no verb or test or treatment term from a list; "Not X" alone);
- a diagnosis in ALIASES.json without its other name at first mention or in its differential row;
- a claim whose cited quote carries a hedge (may, usually, often, can, likely, typically, suggests) while the claim
  carries none;
- one decision stated with two thresholds (the same "past/after/within/under/over N unit" phrase with different N in
  body lines, as backpain "past 4 to 6 weeks" against "past 6 weeks");
- a number in a body line with no quote (numbers.py already; surfaced here).
Tests: tools/spine/test_lint.py with each s148 round-1 MED as a positive case and its fixed line as a negative case.

## 7. The lead counts in the budget
usage_ledger.py --lead --record <wave> appends or updates this session's row in repair/efficiency/ledger_lead.csv
(session, wave, calls, tokens with input, cache write, cache read, output). The report's Cost section gives the batch
total as reviewers plus every lead row of the wave, against the budget; WAVE.json gains "max_lead_tokens" when the launch
prompt names one (the lead proposes it at the close), shown in the report; the gate still enforces only the reviewer caps
(it cannot stop the lead). s148's earlier chats have no lead row (their transcripts are gone): the report says so.

## 8. A hedge from the cited quote is wording-only (rule change, Jonathan's call: adopted)
tools/spine/condpass.py: a replacement approved by another part that ADDS a hedge word counts as wording-only for this
part when every added hedge word appears in a quote that the claim map cites for the line the replacement lands in
(facts.json, claim_map.json). Removing a hedge, changing a number, a negation, an order or condition word, or a name still
needs the normal follow-up review. test_condpass.py: the s148 cases (oa-pharm "which may be contraindicated" from b50;
"likely the most specific site" from m06) pass; a hedge with no quote behind it, and a dropped "after" (septic-bursitis),
still fail. Digest line in Jonathan's words (2026-10-18); STANDING_DIRECTIONS conditional PASS line updated.

## 9. Hooks from the plugin (owed at the close; Jonathan: "launch round 2 and plugin at batch close")
tools/plugin/step2haki-tools: hooks/hooks.json with the three hooks (PreToolUse Agent|Task: agentgate.py; PreToolUse
all: callgate.py; UserPromptSubmit: approval.py hook). Each command runs the repo script only when it exists
(/home/claude/Step2Haki/workspace/tools/hooks or /home/user/Step2Haki/workspace/tools/hooks) and exits 0 otherwise,
never masking an exit 2. Version 0.2.0; README updated. Use the cowork-plugin skill to update the installed plugin and
give Jonathan the file to upload. Runbook session start: when the plugin's hooks are live (test_hooks passes and a probe
launch with no model is refused), skip install.sh; otherwise fall back to the install and ask. Unverified until the first
chat after the upload: whether this harness loads hooks from a synced account plugin (it loads the plugin's agent).
