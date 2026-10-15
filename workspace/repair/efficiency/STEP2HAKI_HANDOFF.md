# Step2Haki running handoff (the single running state file)

Last updated: 2026-10-15, by the s140 lead (s140 SHIPPED, commit 0cf4b06; Claude Code on the web, no Mac).
It lives in the repo at workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (added 2026-10-14 so Claude Code sessions outside the project can read it; a session rewrites State here after every step and pushes), with copies in the project (STEP2HAKI_HANDOFF.md) and on the Mac (~/Documents/Step2Haki/), refreshed at ships when those are reachable.
Batch history lives in each batch's file (claude/pending/S134.md, S136.md, S137.md and so on), not here (s135 efficiency item 4).

## Restart prompt (the only current one)

```
Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.
```

No batch is open. The next batch starts from the launch prompt below.

The runbook (claude/BATCH_RUNBOOK.md; repo copy repair/efficiency/BATCH_RUNBOOK.md) gives the read order, the steps, the standing calls and the one final report.

## State (rewrite after every step)

- **Plan:** v4 (repair/efficiency/SPINE_SCALE_PLAN.md). Phase R done (all 17 spine briefs READY after s140).
- **Open batch: s141** (site rollout of the s140 conventions), launched 2026-10-14 on the Mac desktop app, moved to
  the cloud the same day (the Mac session hit the weekly plan limit; cloud sessions use the cloud session credits).
  **Branch wip/s141** (check it out; main does not have the launch records).
- **Scope:** arrows for high and low measured values, bold lab cutoffs with condition hovers, underline-only hovers
  (pill retired site-wide); lithium-effects first (hemodialysis cutoffs from the AnKing card, conditions in a hover);
  then the other 13 READY spine briefs (all spine briefs except mdd, copd, scfe); vendor_scan exempts AnKing wording;
  the s140 deferred display LOWs. Non-spine briefs: hover restyle by site CSS only ("Yes"). First Phase 2 cluster:
  "Lead's pick", named in the s141 closing launch prompt.
- **Budget:** 16 agents, 90 API calls, 5M tokens (WAVE.json s141 open). **Spend:** 0 batch agents (the Mac live hook
  probes T1 to T4, T8, T9 all passed, outside the budget per the standing hook-test allowance).
- **Step:** S1 done (10 briefs). S2/S3 lithium-effects: conventions applied, verify --mech PASS, 1,152 words, legib 0
  except the pre-existing desk sculpted caution-cell clash (fix: mask outside sp-cw, as s140 mdd) and the known flat
  "Stack" switch. Next: that fix, then S2/S3 for the other 9 (method in repair/s141/S141.md), then S4. Brief-folder work
  is on step2haki-private branch wip/s141: after the cp -rn restore from main, copy that branch's local-only over it
  (cp -r) before working. Spend: 0 of 16 batch agents.
- **Tool change at launch (disclose, G-DIFF):** tools/hooks/common.py defaults the hook state and transcripts paths to
  ~/.config/axbx/hooks and ~/.claude/projects on a Mac with no /home/claude (no effect in the cloud). test_hooks 80/80.
- **Folders for the four waiting briefs (added 2026-10-15 by a planning session, not the s141 lead):** nephrotic-child,
  panic, peds-sleep and tics now have their folders on step2haki-private main (merge/nephrotic-child, psych/N5,
  psych/SLEEP, psych/TICS under local-only/repair/migration). Per the s141 lead's call they join s141 only if Jonathan
  says "include them"; otherwise they are s142. Re-run the cp -rn restore from private main to pick them up.
- **Open small items:** as at s140 (see the s140 State in git history: 98a9ed7).
- **Live:** s140 (0cf4b06).

## Next launch prompt (paste into a fresh chat)

```
Step2Haki: launch batch s141 (site rollout of the s140 conventions) per claude/BATCH_RUNBOOK.md. Scope: arrows for high and low measured values, bold lab cutoffs with condition hovers, and underline-only hovers (retire the pill style site-wide), lithium-effects first (hemodialysis cutoffs from the AnKing card, conditions in a hover); then the other 13 READY spine briefs; vendor_scan exempts AnKing wording; the s140 deferred display LOWs. Budget for the whole batch: 16 agents, 90 API calls, 5M tokens.
1. Non-spine briefs (about 160) get the hover restyle by site CSS only, with arrows and cutoffs left for their own batches: yes or no.
2. After s141, the first Phase 2 cluster (plan section 8): name it, or "lead's pick".
```

## After s141

Phase R is complete (all 17 spine briefs READY, s140). After the s141 rollout, the next work is Phase 2 (plan section 8:
unconverted briefs by cluster).

The forward plan lives in the PRIVATE repo (DrSaturnn/Step2Haki-private), under claude/pending/, outside local-only/,
so the cp restore does not copy it; read it from the clone (/home/user/step2haki-private/claude/pending/):
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
3. Install the hooks: `bash tools/hooks/install.sh`, then `python3 tools/hooks/test_hooks.py` (80 checks), `python3 tools/hooks/usage_ledger.py --context`, and check the Agent tool lists `step2haki-tools:lean-reviewer` (install.sh also installs a local `lean-reviewer`; either passes the launch gate). Re-run the live tests T1 to T4, T8, T9 with one probe wave before any agent work (a temporary probe wave in WAVE.json, then restore the batch wave). A new container has no hooks (T10).
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
- Start a fresh chat when the context passes about 250k (a chat starts at about 122k to 130k).
