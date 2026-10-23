# Step2Haki running handoff (the single running state file)

Last updated: 2026-10-22, by Codex, s150 lead chat 2 (S6 complete; S7 round 2 starting).
It lives in the repo at workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (added 2026-10-14 so Claude Code sessions outside the project can read it; a session rewrites State here after every step and pushes), with copies in the project (STEP2HAKI_HANDOFF.md) and on the Mac (~/Documents/Step2Haki/), refreshed at ships when those are reachable.
Batch history lives in each batch's file (claude/pending/S134.md, S136.md, S137.md and so on), not here (s135 efficiency item 4).

## Restart prompt (the only current one)

```
Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.
```

## State (rewrite after every step)

- **Batch:** s150 open, Phase 2 musculoskeletal C, pediatric: myositis-ossificans, scheuermann,
  bs-puncture-osteomyelitis, bs-torticollis, bs-brachial-plexus. Golden scfe; all five disease, peds lens.
- **Step:** S6 self-check complete; starting S7 round 2 on final source-resolved builds.
  All five full mechanical checks and combined gate/render/vendor checks pass. Current computed contrast is zero
  across all 12 required combinations, and current phone/study captures are readable. The extra full-page pixel
  audit is still active; assess its raw output before closing S7, without claiming an in-progress check passed.
  Jonathan approved the source publishers and 300 calls. Three clinical source gaps now have direct references;
  S7 independently judges scope, including the torticollis orthopedic-reassessment inference. No brief READY.
- **Budget/spend:** 25 reviewer agents, 300 calls, 10M tokens; lead 230M. Used reviewers 8 agents, 136 calls;
  reviewer and lead tokens unknown (Codex usage display unavailable). S7's prescribed 8 lanes plan 142 calls;
  164 calls remain. ledger_codex.csv records actual per-lane counts and unknown tokens.
- **Lead:** Codex, since 2026-10-22, chat 2 (S4 continuation). Original lock bc5cd1288547; continuation lock committed and pushed alone before review work.
- **Branches:** wip/s150 in both repos. Local public /Users/jmontsfit/Documents/Step2Haki/s150-public;
  private /Users/jmontsfit/Documents/Step2Haki/s150-evidence (selective checkout; contains claude mirrors and selected
  local-only evidence). Sources restored only into gitignored workspace paths. Record repair/s150/S150.md.
- **Resume:** current s149 disease builds are the code pattern (septic-hip and sjia); scfe structure and voice.
  Brachial folder now exists, built from the live page. No hooks in Codex; manual budgets and clean checkpoints.
  Required fresh-chat restart after S3 and S7. Codex stops at S8, writes repair/s150/REPORT.md;
  Claude runs CODEX_AUDIT.md, re-presents, and ships only after Jonathan's approval.
- **Owed:** s149 Mac catch-up (handoff, live index.html and repo bundle), retained until Claude's audit/ship.

- **Carried:** From s149: growing-pains unverified marks (rhabdomyolysis "admit", "no braces"); q_bcc4 explanation no
  longer addresses "Restrict running" (preflight P3); lanes.py single-brief path wording; review_packet drawer_targets
  lists in-page anchors; tinted-theme contrast on site-wide elements (not a required mode). SITE_BODY_GLANCE item 3 unscheduled; legib_audit mid-reflow false failures (cross-check with
  repair/s148b/contrast_computed.py; tinted theme repair/s148f/tinted_pixels.py); public wip/s147, wip/s148f, wip/s148e
  and wip/s148h branches; stray Mac bundle; mdd duration-window timeline offered; deferred LOWs (sz-psychosocial
  nonadherence wording, psychosis-duration "non-bizarre"); ae20 answer text at the next antipsych-effects intake;
  review_packet.py omits long quotes from line_sources.txt and renders the folder build (no reasons; s148h used
  repair/s148h/packets.py; fix with tests); peds-sleep age-window chart offered; s148f prose sweep list
  (repair/s148f/prose_sweep.md); legib track-label false positive. From s148e: the 14 MDD gap cards (mdd's next batch)
  and the psych-medical Parkinson card (S148E.md Proposal; not yet in BRIEF_AMEND_LIST); a later "Salicylate and
  Acetaminophen Poisoning" brief (Jonathan's call). From s148h: folder builds lag live (reasons in
  repair/s148h/data/reasons.json, pairings in data/pairs.json, s148g bold; the next rebuild of each brief carries them);
  N1 and APAE folder build.py fail against live; antipsych-effects q_45e13940 explanation wording; psychosis-duration
  S153 hedge; P5 key-in-stem warnings (7). Site list: 5a Targeted tests rows with empty Result and Means cells on
  desktop, ladder "when" followed by a capital, tca-tox Insights mask could run to the line end; the flags lane has no
  link file (do not ask flags to confirm drawers).

## Next launch prompt (paste into a fresh chat)

```
Step2Haki: launch batch s150 (Phase 2, musculoskeletal C, pediatric) per claude/BATCH_RUNBOOK.md, Codex leading per repair/efficiency/CODEX_LEAD.md. Briefs: myositis-ossificans, scheuermann, bs-puncture-osteomyelitis, bs-torticollis, bs-brachial-plexus. Golden: scfe. Brief set rules of 2026-10-20 apply (three reasons per item, bold bottom line, First step pairing). Budget for the whole batch: 25 agents, 220 API calls, 10M tokens; lead 230M tokens. Method: s148 with the efficiency patch; Codex stops at S8 and a Claude chat audits and ships.
```

Budget basis (s149 measured): reviewers about 4 agents, 37 calls, 1.7M tokens per brief; lead about 47M per brief.
After s150: the plan's remaining 107 unconverted briefs (BATCHES_S151_S160.md, private repo); its batch numbers
shift by one.

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
