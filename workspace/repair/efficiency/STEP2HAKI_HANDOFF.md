# Step2Haki running handoff (the single running state file)

Last updated: 2026-10-31, by Claude (s156 chat 6 done: S7 done, all READY; next S8 report).
It lives in the repo at workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (added 2026-10-14 so Claude Code sessions outside the project can read it; a session rewrites State here after every step and pushes), with copies in the project (STEP2HAKI_HANDOFF.md) and on the Mac (~/Documents/Step2Haki/), refreshed at ships when those are reachable.
Batch history lives in each batch's file (claude/pending/S134.md, S136.md, S137.md and so on), not here (s135 efficiency item 4).

## Restart prompt (the only current one)

```
Step2Haki: continue the current batch per claude/RESUME.md.
```

## State (rewrite after every step)

- **RESUMED 2026-10-31** after s159 shipped (0debc69; earlier, 2026-10-29, after s157 shipped, ff25fba): main merged into wip/s156 in both repos (conflicts were record
  files only; 2026-10-31: handoff, WAVE.json kept the s156 wave, ledger_spine.csv took both sides). Continue with
  the restart line. Everything below stands as written at the park.
- **Open batch: s156** (Claude lead, launched 2026-10-29 07:49; Phase 2, infectious disease B, pediatric: meningitis,
  dtap, lymphadenitis, herpangina, bs-pta, bs-fever-rash-arthralgia, aq-infant-fever), branch wip/s156 in both repos.
  Step: S7 done: all READY (chat 6, 2026-10-31): S6 restored meningitis "most common sequela" (card question c22q);
  rounds 2 to 4 left all seven READY (verify). Next: S8 report and S9 in a fresh chat (rebuild the batch page on the
  current main first). Four lead recommendations stay parked for Jonathan (S156.md "Parked recommendations"): not
  approved, do not apply. Spend: wave 27 agents, 663 calls, 70.02M of 78M; lead 74.9M measured of 90M (chat 6 about 13.3M)
  (ledger_lead). Batch file repair/s156/S156.md.
    Never relaunch s156 from a launch prompt; continue with the restart line.

- **Previous: s159 SHIPPED 2026-10-31** (Claude lead; Psych Pharmacology B1 of 4: the section layer, card tools and
  three class cards, pc-maoi (MAOIs), pc-snri (SNRIs), pc-antidep (Other antidepressants); antidep-other retired into
  them as an alias span; drawers retargeted in mdd, ssri-effects, tca-tox, adhd-meds, sud-meds): commit 0debc69, page
  7b4d7cb3b5c3 (approved candidate e1bc544742ca), version.json build s159 (live checked). Reviewers 14 of 19 agents, 220
  calls, 16.66M of 18M (builders 11.86M of 10M); lead 7 chats, about 115M of 110M (chats 5 to 7 measured, 29.8M). The
  first ship run aborted at the ready gate: the 2 s159 temporary allowlist lines must stay until ship.sh passes and come
  out after (s155 precedent); gate on the shipped page 0 failures, 0 stale. Record repair/s159/S159.md (S8, S9). Open:
  OPEN_WORK s159 line. Next pharm batch B2 (s160) needs Jonathan's NBME-item display decision first (prompt below).

- **Previous: s158 SHIPPED 2026-10-30** (Claude lead; four new psych briefs: trauma-stress, cluster-c, sexual-dysfunction,
  stages-change (lookup); drawer pointers in 11 live briefs): commit 98b3f1b, page 00395be2f003 (approved candidate
  07e8fe2497dd), version.json build s158. The first "ship" aborted at the ready gate (drawer briefs' receipts unfiled, then
  stale on specs); rounds 4 and 5 removed the voices L22 and mdd L60 drawers; Jonathan re-approved. Agents 19 of 20, 315
  calls, 26.13M of 58M; lead 6 chats, about 80M of 80M. Record repair/s158/S158.md (S8, S9). Open: the source calls and
  tool notes in OPEN_WORK (s158 line).

- **Previous: s157b SHIPPED 2026-10-30** (Claude lead; patch of the 2026-10-29 NBME intake, Psychiatry CMS Form 8:
  toxidrome, antipsych-effects, ssri-effects, mood-anticonv): commit 50bef79, page d3e594f55987; main (8883ae5) merged
  into wip/s156 in both repos on 2026-10-30, branch State and WAVE kept (s157b budget added to batch_budgets). The s156
  batch page must be rebuilt on the new live page before its S8 (the four briefs above changed on main).

- **Previous: s157 SHIPPED 2026-10-29** (Claude lead; psych pharm section, five new drug briefs in the Psychiatry
  Medications subgroup: antidep-other, mood-anticonv, sedatives, adhd-meds, sud-meds; drawer pointers in substance, mdd,
  bipolar-mania, ssri-effects, panic, tics, tca-tox, peds-sleep): commit ff25fba, page c2e028891b47 (approved
  candidate 5e670282e349), version.json build s157. Agents 24 of 24; measured 14 agents, 378 calls, 43.75M of 72M
  (chats 4 and 5 reviewers unmeasured, transcripts in reclaimed containers); lead 6 chats, about 90M of 90M. Record
  repair/s157/S157.md (S8, S9). Open: tics Pairs with unlinked row (pre-existing); mood-anticonv no clue table; deferred
  LOWs adhd-meds, sud-meds (OPEN_WORK). Tool notes: resume.py still misses the "- **Open batch:" bullet; batch.py s8
  skips present on any pointer_check problem, pre-existing included; ledger loses agents whose chat container was
  reclaimed before usage_ledger ran (run it at the end of every chat that launches agents).

- **Previous: s155** SHIPPED 2026-10-29 (Claude lead; Phase 2, infectious disease A, seven briefs rebuilt on
  the decision spine: tb, hiv-vax, cervicitis, rmsf, bs-anaphylaxis, bs-isolation, bs-foodborne; hiv-vax and
  bs-isolation as lookups): commit e1eb23b (main 32bcf37 after merging main's 29b928d, a docs-only older State),
  page a1878d5c4db1 (approved candidate 5bf0352e0aaf), version.json build s155. Agents 25 of 32, 709 calls, 75.39M of
  76M (builders 64.16M; reviewers 11.23M of the 11M plan); lead 9 chats, about 81M of 100M. Record repair/s155/S155.md
  (S8 and S9). Report flags carried for Jonathan: cervicitis 2-week test of cure (card, no QID; CDC 3 to 4 weeks in a
  hover), bs-foodborne infant drug for high-risk nontyphoidal Salmonella (no board source), bs-isolation mumps endpoint
  (MSD vs CDC/AAP 5 days, unverified), bs-anaphylaxis scombroid epinephrine (card, no QID), hiv-vax Tdap window owned
  by preg-vax, bs-isolation scabies 24 hours carried unsourced; word overages tb, cervicitis, rmsf, bs-foodborne.
  Tool notes: resume.py misreads the "- **Open batch: sNN**" bullet; verify pools replacements only from each part's
  latest receipt; batch.py ship needs AX_SESSION as the full session URL; one-brief verifies need an allowlist line for
  a live-only gate finding that the batch removes (restored for S8, deleted at ship). Next: s156 (prompt below).

Older State bullets (s154 to s154j and the 2026-10-26/28 NBME intakes) moved to repair/efficiency/STATE_ARCHIVE.md at
the s159 ship (runbook S9: keep the start-up files small).

## Next launch prompt (paste into a fresh chat)

Psych Pharmacology B2 (s160), after s156 ships or is re-parked, and only after Jonathan decides how a card shows an NBME
item owned by another brief (PSYCH_PHARM_BATCHES.md section 6 "Before B2"; recommendation: NBME framing on the card, a
link to the item in its owning brief, the item does not move). Budget proposed by the s159 report (measured 5.9M per
card for builders): builders 8, 540, 40M; reviewers 17, 270, 10M; lead 90M; Jonathan sets it at launch.
```
Step2Haki: launch batch s160 (Psych Pharmacology section, batch 2 of 4: Benzodiazepines, Other anxiety agents, Sleep agents, Orexin antagonists, ADHD, Substance use and cessation) per claude/BATCH_RUNBOOK.md, claude/pending/PSYCH_PHARM_V2.md, claude/pending/PSYCH_PHARM_BATCHES.md and claude/CARD_SPEC.md. sedatives, adhd-meds and sud-meds retire into the cards (items carried with ids; drawers retargeted). NBME items owned by another brief: <Jonathan's decision>. s156 stays on wip/s156. Budget: 25 agents, 810 calls, 50M agent tokens (builders 8, 540, 40M; reviewers 17, 270, 10M); lead 90M.
```

NBME presentation layer mockup (no batch; Jonathan 2026-10-26: cross-domain question types first, then how NBME
describes symptoms):
```
Step2Haki: mock up the NBME presentation layer per claude/pending/NBME_PRESENTATION_SPEC.md and DECISIONS_DIGEST 2026-10-26 (cross-domain, both kinds: X1 tags and filter, X2 urgent-risk rows; then NBME behavior descriptions visible in table rows with extras in hovers, and view C; psychosis-duration and bipolar-mania; private artifact for review; no batch, no ship).
```

Population entry type mockup (no batch):
```
Step2Haki: mock up the population entry type with Perinatal Psychiatry per claude/pending/NEW_BRIEFS_2026-10-26.md section 1 (private artifact for review; no batch, no ship).
```

s157 (psych pharm section; Jonathan 2026-10-29; plan claude/pending/PSYCH_PHARM_SECTION.md). The budget is the
planning chat's proposal; Jonathan sets it at launch:
```
Step2Haki: launch batch s157 (psych pharm section: five new drug briefs) per claude/BATCH_RUNBOOK.md and claude/pending/PSYCH_PHARM_SECTION.md. Briefs: SNRIs, Atypical Antidepressants and MAOIs (antidep-other); Anticonvulsant Mood Stabilizers (mood-anticonv); Anxiolytics and Sedative-Hypnotics (sedatives); ADHD Medications (adhd-meds); Medications for Substance Use Disorders (sud-meds). Goldens: lithium-effects, tca-tox (drug entry, psych lens); B0 confirms they fit. S1 to S3 by builder agents. Substance overlap: option A (sud-meds owns maintenance pharmacotherapy; substance's maintenance rows become drawer pointers). s156 stays parked on wip/s156. Budget: 24 agents, 850 calls, 72M agent tokens (builders 7, 630, 62M; reviewers 17, 220, 10M); lead 90M.
```

s156 is PARKED (launched 2026-10-29; never relaunch it from this prompt; resume per the State after s157 ships).
Its original launch prompt, kept for the record (the plan BATCHES_S151_S160.md calls it "s155"):
```
Step2Haki: launch batch s156 (Phase 2, infectious disease B, pediatric) per claude/BATCH_RUNBOOK.md. Briefs: meningitis, dtap, lymphadenitis, herpangina, bs-pta, bs-fever-rash-arthralgia, aq-infant-fever. Goldens: nephrotic-child, scfe (peds lens); B0 confirms they fit, hub golden voices if aq-infant-fever is a hub. S1 to S3 by builder agents. Budget: 32 agents, 950 calls, 78M agent tokens (reviewers 23, 330, 12M; builders 9, 620, 66M); lead 90M.
```

New board questions, any time (intake only; the skill never edits the page):
```
Step2Haki: intake these board questions per the board-brief skill (propose new briefs; do not build).
```

The next patch of shipped briefs, when new intake proposals queue up (runbook 8b; one chat; budget from s154b (used 4 agents, 14 calls, 0.42M; lead about 20M): 6 agents,
30 calls, 1M reviewer tokens; lead 30M):
```
Step2Haki: run the queued intake amendments as a patch batch per claude/BATCH_RUNBOOK.md section 8b.
```
The 2026-10-28 intake patch as launched (s154h form):
```
Step2Haki: launch batch s154i (patch of the 2026-10-28 NBME intake proposals, Psychiatry CMS Form 7: disruptive-behavior, antipsych-effects, ssri-effects, bipolar-mania, tca-tox, suicide-risk, somatic; repair/sources/intake/*_2026-10-28.md) per claude/BATCH_RUNBOOK.md section 8b. Baits: as inferred unless I name changes here. Budget: 8 agents, 40 calls, 1.5M reviewer tokens; lead 40M.
```
The pause point repair, after s154i ships:
```
Step2Haki: launch batch s154j (pause point repair: 34 blocks in 22 briefs plus the pause-content checker rule) per claude/BATCH_RUNBOOK.md section 8b, using the private repo claude/pending/s154j/ (S154J_PAUSE_REPAIR.md, delta_s154j.json, lint_pause_content.patch). Budget: 10 agents, 70 calls, 3M reviewer tokens; lead 60M.
```

complete (all 17 spine briefs READY, s140). After the s141 rollout, the next work is Phase 2 (plan section 8:
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
- Hover-card text, the collapsed systems panel and the pause point do not count against the word cap (2026-10-13; pause point 2026-10-26); hovers and the panel are the place for guideline-only detail.
- Start a fresh chat at the H6 finish notice, start + 200k, about 330k (Jonathan 2026-10-27, was 225k, before that 350k; a chat starts at about 122k to 130k), after finishing the step in hand. Continuation chats use the short read list in the runbook.
