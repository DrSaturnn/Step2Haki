# Step2Haki running handoff (the single running state file)

Last updated: 2026-10-24 13:30 EDT, by Claude (s150e open: S3 done).
It lives in the repo at workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (added 2026-10-14 so Claude Code sessions outside the project can read it; a session rewrites State here after every step and pushes), with copies in the project (STEP2HAKI_HANDOFF.md) and on the Mac (~/Documents/Step2Haki/), refreshed at ships when those are reachable.
Batch history lives in each batch's file (claude/pending/S134.md, S136.md, S137.md and so on), not here (s135 efficiency item 4).

## Restart prompt (the only current one)

```
Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.
```

## State (rewrite after every step)

- **Open batch: s150e** (Claude lead, patch of shipped briefs, section 8), launched 2026-10-24 12:27 EDT. Briefs:
  sz-psychosocial (N3), cluster-b (PDB), substance (TOX), peds-sleep (SLEEP), ssri-effects (N4), panic (N5): the queued
  intake proposals of 2026-10-23 and 2026-10-24. Budget 12 agents, 220 calls, 6M reviewer tokens; lead 150M (WAVE.json
  s150e). Batch file repair/s150e/S150E.md. Branch wip/s150e in both repos (private: main plus wip/s150c merged).
- **Step: S3 done** (all six MECHANICAL PASS; batch page gate PASS; squeeze 0; vendor 0). Next: S4 round 1, changed
  lines only (acc, read, flags; no display). Packets with --since <folder>/baseline_brief_text_s150e.txt; plan in the
  batch file's last section. Spend: reviewers 0 of 12 agents, 0 of 220 calls; lead chat 1 not yet recorded.
- **Restore for s150e:** clone both repos, check out wip/s150e in each, cp -rn the private local-only into workspace,
  rebuild the batch page with `python3 repair/build.py s150e --out local/s150e/index.html`.
- **Token rules (2026-10-24):** no screenshots in content batches (approval binds the report, batch and page; READY
  needs acc, read, flags); small additions reviewed on changed lines only; one batch per chat. Runbook "Token rules".
  Owed by Jonathan: turn off Figma, Vercel and the healthcare plugin for this project (start-up context 193K against a
  130K baseline; s150e start-up measured 128,376).
- **s151 (Codex):** S7 done, all seven READY, released to Claude for S8 and S9 (wip/s151, cardiovascular; no brief shared
  with s150e). Whichever of s150e and s151 ships second merges main first (the 2026-10-23 parallel rule).
- **s150d shipped** 2026-10-24 11:05 EDT on Jonathan's "ship": commit 0fa5d5f (main, by hand). psych-medical is now
  "Medication- and Illness-Induced Psychiatric Disorders" (tile removed); disruptive-behavior has a Time frames table.
  Record repair/s150d/S150D.md. Its private folder changes join the owed files below.
- **s150c:** s150c shipped by Claude 2026-10-24 08:05 EDT on Jonathan's plain "ship" (approval hook in
  this container). Production ship dfacd00 (main, pushed by hand: no token here); live version.json confirms s150c;
  built page sha256 starts 200be105e2c6 (presented candidate f4d236d75c4d). Record: repair/s150c/S150C.md (S8, S9).
- **Completed (s150c):** new Cognitive Decline and Dementia in an Adult (hub, after delirium; Presentations link),
  Eating Disorders (after somatic) and Defense Mechanisms (first lookup brief, last in Anxiety, somatic and sexual);
  additions to suicide-risk, substance and disruptive-behavior; pointers in mdd and ssri-effects. All eight READY.
  Independent S8 audit (fresh Opus acc lanes) found 9 MED and 6 LOW in the new briefs; all fixed; round 4 READY.
- **Private files owed (important):** the s150c brief-folder changes after S7 (DEM, EAT, DEF facts_spec, facts,
  build.py, disp_manual, cards_disposition, adj_s150c.md; audit and round 4 receipts in repair/migration/spine/reviews;
  packets s150c-audit and s150c-r4; sheets s150c-approval) were never pushed: this chat had the private repo
  read-only, and the Mac bridge dropped before they could be copied there. They (with s150d's) were sent to Jonathan in the
  s150c chat as s150cd_private_owed.tar.gz (507 files, 50 MB, paths relative to local-only/; raw shots left out).
  The next session with push access extracts it into the private clone's local-only/, commits on wip/s150c and merges
  to main. Until then a fresh cloud chat restoring from the private repo gets the S7 versions of those files.
- **Lead:** Claude holds s150e (wip/s150e). s151 S8 and S9 run in a separate Claude chat, which takes the lock on wip/s151.
- **Carried:** deferred LOWs from s150c round 4 (dementia Korsakoff item reason d1 "none are present here" would read
  better as "gait and eye movements are normal here"; eating-disorders "another step 2 criterion" and "any step 2
  criterion" would read better as "admission criterion (Urgent risks)"); the defense-mechanisms intro clause naming
  suppression stays unmasked in study mode (intro lines are not masked); no reverse pointers to dementia or
  defense-mechanisms from delirium, parkinson or cluster-b (outside the s150c scope); MPTP chemical-name LOW; s150b
  legibility advisories; the four s150b audit proposals (not rules); the other 2026-10-23 psychiatry amendments queued.
- **Mac:** NOT refreshed (the bridge dropped at post-ship): the handoff copy and index.html there are the s150b ones;
  axbx-repo.bundle must not come from a shallow clone. The project handoff copy was refreshed.

## Next launch prompt (paste into a fresh chat)

When Codex releases s151 (its State reads "S7 done: all READY; Lead: released to Claude for S8 and S9"), Claude runs
S8 and S9 with the restart line, in a chat with push access to both repos:
```
Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.
```
First in that chat: commit the owed s150c and s150d private files from s150cd_private_owed.tar.gz (State, Private files owed),
then refresh the Mac copies.

New board questions, any time (intake only; the skill never edits the page):
```
Step2Haki: intake these board questions per the board-brief skill (propose new briefs; do not build).
```

The next Claude-led authoring batch, only when Jonathan asks for it: the queued 2026-10-23 psychiatry amendments
(repair/intake/queue.csv). Proposed budget, from s150c (3 new briefs plus additions with an S8 audit): 32 agents,
380 calls, 14M reviewer tokens; lead 250M.

## After s141

Phase R is complete (all 17 spine briefs READY, s140). After the s141 rollout, the next work is Phase 2 (plan section 8:
unconverted briefs by cluster).

The forward plan lives in the PRIVATE repo (DrSaturnn/Step2Haki-private), under claude/pending/, outside local-only/,
so the cp restore does not copy it; read it from the clone (/home/claude/step2haki-private/claude/pending/):
- BATCHES_S141_S150.md: s142 (nephrotic-child, panic, peds-sleep, tics) and s143 to s150 (psychiatry remainder,
  pulmonary A and B, renal and GU A and B, musculoskeletal A to C), with launch prompts, goldens and default budgets.
- BATCHES_S151_S160.md: s151 to s160 (cardiovascular A and B, GI A and B, infectious disease A and B, newborn and
  immune, neuro and HEENT A, neuro B, endocrine), same format; 38 briefs remain after s160 (hematology, OB/GYN,
  dermatology, preventive, pediatrics and genetics) for the s160 report to plan.
- FOLDERS_S142_S160.md: each brief's local-only folder. All 52 were pushed from the Mac on 2026-10-15; briefs marked
  "no folder" have no migration work yet and build from the page and repair/sources.
Roster count (2026-10-15): 177 briefs on the page, 18 converted (17 spine plus hematuria), 159 unconverted (the s141
to s150 file's 160 still counted hematuria).
The next batch's launch prompt comes from those files unless the s141 closing report changes it.

## Docs in this project

- `STEP2HAKI_HANDOFF.md`: this file.
- `claude/BATCH_RUNBOOK.md`: one batch from launch to "ship".
- `claude/SPINE_SCALE_PLAN.md`: the governing plan (v4).
- `claude/DECISIONS_DIGEST.md`: Jonathan's decisions in his words; only the lead writes it, in the turn the decision is given (repo copy is current; the project copy is refreshed at ships).
- `claude/STANDING_DIRECTIONS.md`: every standing direction, compiled with its source; required before any brief, display or content work.
- `claude/SPINE_SPEC.md`, `claude/design/WORKUP_5A_SPEC.md`, `claude/design/Workup_5a.html`: the spine and the 5a workup template.
- `claude/pending/S137.md`: the s137 batch file. `claude/pending/S136.md`, `S136_RECORD.md`, `GLANCE_LAYOUT_PLAN.md`: s136 and the glance plan.
- `claude/pending/BRIEF_AMEND_LIST.md`: the work queue.
- Others are earlier batches, pilots or merge-era reference (`claude/archive/`; `claude/OPEN_WORK.md` is stale; the repo's workspace/OPEN_WORK.md is current).

## Session start

1. Attach and clone both repos (the session's own GitHub access; no token needed):
   - add_repo DrSaturnn/Step2Haki (access push) and DrSaturnn/Step2Haki-private (access push);
   ```
   git clone https://github.com/DrSaturnn/Step2Haki /home/claude/Step2Haki
   git clone --depth 1 https://github.com/DrSaturnn/Step2Haki-private /home/claude/step2haki-private
   cd /home/claude/Step2Haki/workspace && npm i
   cp -rn /home/claude/step2haki-private/local-only/. /home/claude/Step2Haki/workspace/
   ```
   The private repo (PRIVATE, never public) holds the local-only files batch s138 needs (README there lists them). Anything
   a batch needs that is not there comes from the Mac (`Documents/Step2Haki/local-only/`, device_stage_files, at most 50 per
   call, never a tarball or scratch file in Documents) and is then committed to the private repo so the next chat has it.
2. Pushing: with the repos attached, `git push origin HEAD:<branch>` works without the token (checked 2026-10-14). ship.sh
   pushes only when /home/claude/.config/axbx/gh_token exists; without it, it prints "push skipped: no token": then push
   HEAD to main by hand. The Mac's gh_token (fine-grained, Step2Haki only) is the fallback; never store it in a repo or doc.
3. Install the hooks (skip when the plugin's hooks are live: runbook section 1): `bash tools/hooks/install.sh`, then `python3 tools/hooks/test_hooks.py` (80 checks), `python3 tools/hooks/usage_ledger.py --context`, and check the Agent tool lists `step2haki-tools:lean-reviewer` (install.sh also installs a local `lean-reviewer`; either passes the launch gate). Re-run the live tests T1 to T4, T8, T9 with one probe wave before any agent work (a temporary probe wave in WAVE.json, then restore the batch wave). A new container has no hooks (T10).
4. Claude Code on the web (s138): the repo clones to /home/user/Step2Haki and the private repo to /home/user/step2haki-private; common.py maps roles.json's /home/claude paths onto the checkout. install.sh writes /home/claude/.claude/settings.json, which this harness does not read: write the same three hooks into /root/.claude/settings.json and `mkdir -p /home/claude/.config/axbx/hooks`. Install Python Playwright 1.56.0 (matches /opt/pw-browsers chromium-1194) for shots.py. step2haki.vercel.app is outside the default network policy: Jonathan checks version.json, or allows the host in the environment's Network access.
5. Do not edit tracked files while `verify.py` runs in the background: its git check reports any tracked change made during the run.

## Where things live

- Repo (public): https://github.com/DrSaturnn/Step2Haki. Clone to /home/claude/Step2Haki, work in `workspace/`.
- Live page: `workspace/discriminator-briefs-site/index.html`; `workspace/index.html` is the working page. Vercel deploys on push.
- History: `workspace/OPEN_WORK.md`. Decisions: `workspace/repair/efficiency/DECISIONS_DIGEST.md`. Plan: `workspace/repair/efficiency/SPINE_SCALE_PLAN.md`.
- The Mac folder `Documents/Step2Haki/` holds everything private; request access to `~/Documents/Step2Haki` in a new chat.
  - `gh_token`: the fallback push token (see Session start 2).
  - `local-only/`: the private files, the same tree as `workspace/` (`repair/sources/`, `repair/migration/`, `local/`); about 397 MB.
  - `index.html` and `axbx-repo.bundle`: the live page and the repo as of the last ship.
  - `STEP2HAKI_HANDOFF.md`: a copy of this file.
- After each ship: commit the new or changed local-only files to DrSaturnn/Step2Haki-private (local-only/...); when the Mac is linked, also copy them into its `local-only/` and replace `index.html` and `axbx-repo.bundle` there; update this file in the project (and in the Mac folder when linked).

## Getting the page and publishing

- **Publish a batch** only after `python3 tools/hooks/approval.py present sNN SHOTS` and Jonathan's "ship" reply (the hook records the approval; the record lives in the container that presented, so "ship" must go to that chat; a "ship" sent before present approves nothing): then `AX_SESSION=https://claude.ai/code/session_<id> tools/ship.sh sNN "message"`. It builds `repair/sNN/*.json` into the page, runs the gate, render and vendor checks, copies the page to the site folder, commits as DrSaturnn and pushes HEAD to main (a batch branch must have main merged in first). ship.sh refuses a spine build that is not READY (four receipts per brief, verify.py) and any batch changed after approval. Every ship needs an entry in repair/changelog/axlog.py.
- **Log-only and tool commits** are pushed by hand; the token goes only through environment variables:
  ```
  git -c user.email=297481111+DrSaturnn@users.noreply.github.com -c user.name=DrSaturnn commit -m "..."
  AUTH=$(printf 'x-access-token:%s' "$(cat <staged gh_token>)" | base64 -w0); GIT_TERMINAL_PROMPT=0 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="AUTHORIZATION: basic $AUTH" git push -q origin HEAD:<branch>
  ```
- **Check before shipping:** `T=$(mktemp -d); python3 repair/build.py sNN --out $T/index.html && python3 tools/gate.py $T/index.html --base HEAD`; then render.js, preflight.py (base HEAD), `vendor_scan.py --page $T/index.html` with the sources restored, legib_audit on the changed briefs (s137 added --theme and --accent).
- Edits inside a brief's `ol.bank` are refused by apply_edits; only add_item, set_attr or a whole-brief replace reach them.
- End every turn with a clean git tree (a stop hook checks).
- Confirm a deploy by opening `https://step2haki.vercel.app/version.json?t=<anything>` in Chrome (WebFetch caches for minutes).

## Standing rules

- Authored items are original stems, never retold UWorld vignettes; 30 to 40 words in scannable lines.
- No drift; every clue from every source stem is used.
- No emojis, no em dashes. Label anything unverified with ⚠︎.
- Content comes from the old briefs or from a source opened that day, with a verbatim quote. Board sources first.
- Mnemonics only if widely accepted. Pastel colors; horizontal timelines.
- Vendor text never enters the public repo. Commit as DrSaturnn with the noreply email. Never print the token.
- Hover-card text and the collapsed systems panel do not count against the word cap (2026-10-13); they are the place for guideline-only detail.
- Start a fresh chat when the context passes about 350k (Jonathan 2026-10-17; a chat starts at about 122k to 130k). Continuation chats use the short read list in the runbook.
