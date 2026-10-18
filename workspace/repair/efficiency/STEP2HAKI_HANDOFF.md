# Step2Haki running handoff (the single running state file)

Last updated: 2026-10-17, by the s147 lead (continuation chat 4, S5 and S6 done).
It lives in the repo at workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (added 2026-10-14 so Claude Code sessions outside the project can read it; a session rewrites State here after every step and pushes), with copies in the project (STEP2HAKI_HANDOFF.md) and on the Mac (~/Documents/Step2Haki/), refreshed at ships when those are reachable.
Batch history lives in each batch's file (claude/pending/S134.md, S136.md, S137.md and so on), not here (s135 efficiency item 4).

## Restart prompt (the only current one)

```
Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.
```

s147 is open; a fresh chat continues it with the line above.

## State (rewrite after every step)

- **Open batch: s147** (Phase 2 renal and GU B, pediatric), launched 2026-10-17 17:53; branch wip/s147 in both repos.
  Briefs: peds-uti-recurrent, enuresis, peds-aki, bs-puv (disease), bs-abdominal-mass, bs-distal-rta, aq-puffy-eyes,
  scrotum (hubs). Golden nephrotic-child (peds lens); voices for hubs. Budget 24 agents, 220 API calls, 9M tokens
  (WAVE.json).
- **Step: S5 done, S6 done (continuation chat 4, 2026-10-17 21:00); next is S7, follow-up review round 2, after
  Jonathan answers the budget question** (round 1 used 6.70M of the 9M tokens; round 2 projects about 6M more).
  Round 1: 10 lanes, 30 of 32 receipts (no flags receipt for aq-puffy-eyes or scrotum: flags-B hit its cap). Every MED
  adjudicated and fixed or rejected with evidence (repair/s147/S147.md, S5). All eight MECHANICAL PASS (--fast); batch
  preview build, gate, render PASS; vendor_scan 0; preflight P1 1 (held by cuts); legib 0 below contrast. Words:
  peds-uti 934, enuresis 1,063, peds-aki 870, bs-puv 800; bs-abdominal-mass 681, bs-distal-rta 734, aq-puffy-eyes 731,
  scrotum 643.
- **S7 plan:** packets with review_packet.py --diff (changes.md against the live brief is the whole brief for these new
  conversions, so give each lane the S5 edit list from S147.md as the scope) plus the r1 receipt; acc A and B (opus, 4
  briefs, Budget 24), read A and B, flags A (4 changed briefs) and B (bs-abdominal-mass changed; aq-puffy-eyes and scrotum
  full, flags owed from round 1), display A and B with phone-study images of the changed steps only. Lane builder:
  /tmp scripts are gone in a new container; rebuild from repair/s147/S147.md (S4 notes).
- **Spend:** 10 agents, 114 calls, 6.70M tokens (usage_ledger).
- **Mac:** caught up at the s146b ship; nothing owed. The stray ~/step2haki-private-push/_xfer_pub.bundle is still there.
- **Lessons for lanes (s146, s146b, s147):** the callgate counts every tool use, each file of a parallel batch included.
  Inline the lane instructions in the launch prompt (s147: saves a call per agent). Tokens, not calls, bound s147: about
  59k tokens per call in round 1.
- **Open small items:** brief header still in the old style (p.sub subtitles kept on converted briefs, e.g. bs-puv
  "drain, then image"); sinopulm phone sticky bar truncates the title; hypercalcemia study mode shows "Bisphosphonates are
  usually the drugs of choice in malignancy" beside the masked rung; polyuria "common" in Pairs with; legib clashes on
  hover buttons inside table cells and on count buttons; Treatment rung labels (ABLATE, DRAIN, DIALYSIS) stay visible in
  study mode (site-wide, display LOW); deferred LOWs in repair/s141 to s147 batch files.

## Next launch prompt (paste into a fresh chat)

```
Step2Haki: launch batch s147 (Phase 2, renal and GU B, pediatric) per claude/BATCH_RUNBOOK.md. Briefs: peds-uti-recurrent, enuresis, peds-aki, bs-puv, bs-abdominal-mass, bs-distal-rta, aq-puffy-eyes, scrotum (folders: claude/pending/FOLDERS_S142_S160.md, listed there as s146; peds-uti-recurrent and enuresis have merge folders, the other six build from the page and repair/sources). Golden: nephrotic-child (peds lens); voices for any hub. Budget for the whole batch: 24 agents, 220 API calls, 9M tokens. Method: s142, with write-first review lanes (each reviewer writes a brief's receipt before reading the next; lane instructions name every file and ban globs; Budget 5 calls per brief plus 4, display 7 per brief plus 4). Setup tool fixes first: review_packet.py adds ALIASES.json and ABBREV.json to the read packets; legib_audit stops counting the dotted underline on pointer links (.xref) as a clash.
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
- Start a fresh chat when the context passes about 350k (Jonathan 2026-10-17; a chat starts at about 122k to 130k). Continuation chats use the short read list in the runbook.
