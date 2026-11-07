# Step2Haki running handoff (the single running state file)

Last updated: 2026-11-07, by Claude (s167 open).
It lives in the repo at workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (added 2026-10-14 so Claude Code sessions outside the project can read it; a session rewrites State here after every step and pushes), with copies in the project (STEP2HAKI_HANDOFF.md) and on the Mac (~/Documents/Step2Haki/), refreshed at ships when those are reachable.
Batch history lives in each batch's file (claude/pending/S134.md, S136.md, S137.md and so on), not here (s135 efficiency item 4).

## Restart prompt (the only current one)

```
Step2Haki: continue the current batch per claude/RESUME.md.
```

## State (rewrite after every step)

- **s167 OPEN 2026-11-07** (Claude lead; UI refactor part 2, site layer only, content frozen; D-20261107-1 to -4; lead
  100M, no agents; batch file repair/s167/S167.md, chunk table there). Branch wip/s167 lives only in this container and as
  the bundle claude/pending/s167/wip_s167.bundle in the private repo (the public repo attach was refused at launch): a
  continuation chat clones main, then `git fetch <bundle> wip/s167:wip/s167 && git checkout wip/s167`. Step: chunk 2
  (review redesign).

- **s165b SHIPPED 2026-11-06** (Claude lead, from the ledger chat; rules and gate patch, tools and docs only, no page
  change; D-20261106-8 to -11; Jonathan "ship" 23:58): commits 0267947, 43e206e, 2ff77a6 and the handoff commit,
  fast-forwarded to main. gate.py runs ui-lint, ui-site, doc-lint, prose-lint and prose-touched (48 checks; PASS on the
  live page); ship.sh lowers tools/spine/ui_baseline.json and prose_baseline.json in the ship commit and restores them
  on a failed ship. New tools/spine/prose_lint.py (tests 88), style_card.py; verify.py refuses READY on prose hits; the
  writing card from repair/efficiency/TEXTBOOK_STYLE.md heads every builder, review-round, patch and reviewer packet;
  bootstrap.sh checks bs4, lxml, tinycss2. Prose baseline 1,983 counted hits in 209 briefs (header word caps and meta
  words report-only). Doc sweep N15: STANDING core rule 9, digest D-8 to -11, CARD_SPEC, runbook, WORKUP_5A_SPEC,
  MIGRATION_CONTRACT, RULES_voice. Independent review: 2 blocking and 8 should-fix findings, all fixed. Tests: gate
  rules 34/34, hooks 132, lint 92, review_packet 20, lead_tools 40, verify suites pass; test_batch_tools 1 failure
  predates (also fails on 5c3af88). The edit to hashed specs stales every receipt; only rebuilt briefs are affected.
  Open for Jonathan: non-spring motion baseline kept at 60 (Claude's recommendation in the ship report; s167 converts
  them); whether headers get a word cap and the header list an exemption. Ledger: claude/pending/POST_REFACTOR_LEDGER.md
  (private repo, N1 to N20). wip/s166 must merge main before it resumes (digest ids -8 to -11 follow its -6 and -7).
  No batch open. Next per D-20261106-8: s167, refactor part 2 (repair/s164b/S164B.md "Deferred").

- **Previous: s165 SHIPPED 2026-11-06** (Claude lead; offline use, site layer only, content frozen; D-20261106-5; no agents):
  commit 061b33f (pushed to main), page a1dfb28b4e5d (approved candidate 422cf14303b4); version.json reads s165 (checked from the
  Mac VM, with sw.js, manifest.webmanifest and icons served). Worker site/pwa/sw.js, built beside the page and stamped
  per build by tools/site_build.py (ship.sh reruns it with --pwa-only after the stamp), saves the page, search.json,
  the manifest and 4 icons in cache step2haki-<build>; version.json, sw.js and api/ go to the network. Offline note,
  install tags and update hand-off: site/js/24-offline.js, site/pwa/head.html, 04-version (net:status, site:newer,
  site:ready, site:apply). Tests repair/s165/offline_test.js (desk and --phone) and liefi_test.js; record
  repair/s165/S165.md. Vendor scan on the Mac VM: 0 flagged (ship.sh printed NOT CHECKED: no private repo in this
  container). The repo attach was refused at launch and allowed at ship. Lead 1 chat, 27.2M of 60M.
  No batch open. Next (UI_REFACTOR_PLAN follow-ons, D-20261105-7): the phone redesign and Fit to screen (3 and 4,
  Jonathan may reorder), and the quiz and Review panel batch (D-20261105-9); Jonathan picks which launches next.

- **Previous: s164c SHIPPED 2026-11-06** (Claude lead; load briefs on demand, site layer only, content frozen; D-20261106-3 and
  D-20261106-4; no agents): commit 27b1a73 (pushed to main), page 1fad3ed04e2b (approved candidate 1e65dba35063; the
  build stamp and the embedded changelog are the only differences); version.json reads s164c; search.json ships beside
  the page in discriminator-briefs-site/. Briefs are wrapped in templates by tools/site_build.py and built when opened
  or scrolled near (core.js AX.brief, 06-load-near.js); search reads the prebuilt index (tools/search_index.js, gate
  check search-index; in-page build only as the file:// fallback); long jumps seat through the sidebar (brief:go).
  Measured in the same run (median of 3, local HTTP): desk settled 6.3 s to 0.45 s, phone CPU 4x 33.8 s to 2.4 s;
  elements 223,878 to 3,405. Parity: ui_styles 12-brief sample desk and phone, only 1 px inline-span heights; search,
  landing, jumps, previews, drawers, NBME view, blueprint and Review equal to before.html (S164C.md "After").
  Behavior noted: the desk sidebar draws the first brief's step list at load (the live page drew it on first scroll);
  question snippets in search keep the index's choice order (choices reshuffle on each load). Vendor scan: ship.sh
  printed NOT CHECKED (the private repo could not be attached in the container); run by hand on the Mac's VM against
  wip/s164c with Documents/Step2Haki/local-only sources (2026-10-26): 0 flagged, page 0.009% shared, longest run 15
  words. Lead: 4 chats; chat 4 32.1M (ledger_lead.csv; chats 1 to 3 not recorded in this container's transcripts).
  No batch open. Next (UI_REFACTOR_PLAN follow-ons, D-20261105-7): offline use (item 2), then the phone redesign and
  Fit to screen (3 and 4, Jonathan may reorder), and the quiz and Review panel batch (D-20261105-9); Jonathan picks
  which launches next.

- **Previous: s164b SHIPPED 2026-11-06** (Claude lead; the UI refactor, site layer only, content frozen; D-20261105-8, cut short
  by D-20261106-2, Jonathan 14:22: "we can ship what we have, perform the on demand loading ship then consider this at
  another time later down the ledger"): commit e5d78c1 (pushed to main), page cbd0eeddd9c7 (approved candidate
  6076716debe6); version.json reads s164b; Jonathan checks the live site. The page's styles and scripts come from
  workspace/site/ (css in 5 layers, themes as color tokens per D-20261105-10; js modules) through tools/site_build.py,
  one minified style and one script bundle; ship.sh and approval.py run it. Briefs byte-identical. Known residues
  shipped: phone sculpted dark, a chrome table's 5 even rows lose the zebra tint; desk dark, the mdd popover title is
  muted (was ink-2). Tool changes: gate reads the minified page (OUT code map, mode-css reads every style block; 11
  pre-existing body.study rules allowlisted as backlog), rrweb-cssom 0.8.0 override so render.js parses @layer, ui_styles
  dump restarts after a renderer crash and has --norm. Deferred list (review redesign first, then raw colors, dehack,
  5b to 5f, step 6 parity and review agent, 6b gate tests, 7 baseline): repair/s164b/S164B.md "Deferred". Lead: 6 chats.
  No batch open. Next: load briefs on demand (UI_REFACTOR_PLAN follow-on 1), launch prompt needed; Jonathan to confirm it
  goes before the D-20261105-9 quiz and Review panel batch.
- **UI rules landed 2026-11-05** (doc commit, no site change; Jonathan "ship"): DECISIONS_DIGEST D-20261105-1 to -7 (UI
  architecture, no stale decisions, SwiftUI-style spring motion, order of work, Fit to screen next round, no decision
  narration in code, refactor scope and follow-on batches); STANDING_DIRECTIONS
  opens with a core rules block and gains a "UI architecture" section; tools/spine/ui_lint.py (ratchet, baseline
  tools/spine/ui_baseline.json) and doc_lint.py added (wired into gate.py and ship.sh in s165b). Next: the UI refactor batch
  in a fresh chat, launch prompt in repair/ui/UI_REFACTOR_PLAN.md; then on-demand brief loading, offline use, the phone redesign and Fit to screen
  (repair/ui/FIT_TO_SCREEN.md), each its own batch.

- **Previous: s164 SHIPPED 2026-11-05** (Claude lead; site layer plus patch, s163 carry-overs: phone in-brief rail marks the step
  being read (baseline before the mobile redesign); window figures and word forms in Differential criteria previews,
  102 tiles; 20 section-name pointers state the action; B4 masks in outlines; 4 stale private folders archived;
  test_outline_check goldens): commit 60d14ae, page 10098af401b5 (approved candidate 5f346af7bde7); version.json not
  checked here, Jonathan checks the live site. No agents; lead 2 chats, about 37M of 60M. Record repair/s164/S164.md.
  Open: OPEN_WORK s164 line (step-2 workup ladders in ascvd and bs-adolescent-bp may belong in Workup; local-only
  restores s155 to s158 lanes copies into the public tree). No batch open; next needs a launch prompt.

- **Previous: s163 SHIPPED 2026-11-05** (Claude lead; site layer plus patch: diagnostic criteria as step 2 in every
  brief, no step numbers or ownership words in brief text, NBME labels, Recall masks on repeated criteria cutoffs,
  criteria tile in Differential drawer previews): commit 6a4eb72, page d3c5799f2422 (approved candidate 35d5ddd3708f);
  version.json not checked here, Jonathan checks the live site. No agents; lead 5 chats, 98.66M of 100M before the
  ship (measured). First ship run refused by the commit hook on the s155 to s158 lanes copies restored from local-only
  (moved out; they live in the private repo). Record repair/s163/S163.md (chunk table, S9). Open: OPEN_WORK s163 line.

- **Previous: s162 SHIPPED 2026-11-04** (Claude lead; Psych Pharmacology B4 of 4: pc-atypical, pc-typical, pc-antichol,
  pc-td in 02 Antipsychotics; Q4 keep; section complete, 18 of 18 class cards): commit c50fd62 (main d920cfe after
  merging main's RESUME and handoff notes, ours kept), page a2d98e32f61f (approved candidate faaf259bc1be); version.json
  not checked here, Jonathan checks the live site. Wave 21 agents, 364 calls, 32.51M of 42M (builders 28.07M, no
  relaunch; reviewers 4.44M); lead 4 chats, 77.83M of 80M (measured). ship.sh had no token and main had moved (two doc
  commits): merged by hand, pushed. No temporary allowlist lines. Record repair/s162/S162.md (S8, S9). Open: OPEN_WORK
  s162 line.

- **Previous: s161d SHIPPED 2026-11-04** (Claude lead; site layer: the desktop sidebar fits wide windows under the 110%
  zoom): commit f817f18, page 59ff29b3cace (approved candidate 634020d29e52). Record repair/s161d/S161D.md. Open: OPEN_WORK
  s161d line (other 100vh panels unchecked).

- **Previous: s161c SHIPPED 2026-11-04** (Claude lead; site layer, Jonathan's words in DIGEST 2026-11-03/04: Presentations
  as its own section, page and sidebar, each brief listed once under a system sub-header): commit cab27f6, page f1e305b19c2d
  (approved candidate 9e5d6e2c28e4). Tools: gate nav-link one sidebar link per brief (s146c hub-in-both retired);
  apply_edits move_brief after_anchor. No agents; no brief changed. Record repair/s161c/S161C.md. Open: OPEN_WORK s161c
  line (stale system heading counts; batch.py post not run).

- **Previous: s161b SHIPPED 2026-11-03** (Claude lead; site layer, Jonathan's words in DIGEST 2026-11-03: one home per
  brief in the sidebar, Presentations browsing stays on Presentations, Shelf card under the search, flat theme default):
  commit 1885982, page fd0959548d47 (approved candidate 9b47429e1708), version.json build s161b (checked). No agents; no brief
  changed. Pilot repair/pilots/nav-home/make_pilot.py (artifact r1 to r6); record repair/s161b/S161B.md. Open: OPEN_WORK
  s161b line (dark legib run stopped; batch.py post not run, so no lead ledger row or private sync).

- **Previous: s161 SHIPPED 2026-11-02** (Claude lead; Psych Pharmacology B3 of 4: pc-ssri, pc-tca, mood-anticonv
  (Lithium and anticonvulsants; id kept, card in place), pc-cog, pc-other; Q4 keep; bipolar-mania drawer label):
  commit f1922cf, page 9acef4067ecf (approved candidate e98d1dd38c65); version.json not checked here, Jonathan checks the live
  site. Wave 26 agents, 529 calls, 48.62M of 52M (builders 40.32M, no relaunch; reviewers 8.30M); lead 5 chats,
  87.61M of 100M (measured). The first ship run aborted at the trailer (AX_SESSION unset). The temporary allowlist line
  psych-cms-c01111 deleted after ship.sh. Record repair/s161/S161.md (S8, S9) and S8_REPORT.md. Open: OPEN_WORK
  s161 line.

- **Previous: s160 SHIPPED 2026-11-02** (Claude lead; Psych Pharmacology B2 of 4: pc-benzo, pc-anxiety, adhd-meds
  (card in place, id kept), pc-sleep, pc-orexin, sud-meds (card in place, id kept); sedatives retired into the four new
  cards (alias span before pc-benzo); drawers retargeted in tics, peds-sleep, panic, stages-change, pc-antidep): commit
  8a42a4b, page 92d62c3d794b (approved candidate 31727475b3d6); version.json not checked
  here (fetch permission withdrawn), Jonathan checks the live site. Wave 28 agents, 697 calls,
  57.48M of 58.1M (builders 47.60M; reviewers 9.88M); lead 7 chats, 121.7M measured of 90M (over). The first ship run
  aborted at the ready gate: two folders claim each kept id (s157 psych/ADHD, psych/SUDM and the card folders
  pharm/ADHD, pharm/SUD); Jonathan chose the gate fix: ready_gate verifies the folder whose 10_ file matches the
  batch copy. The 3 s160 temporary allowlist lines deleted after ship.sh; gate on the shipped page 0 failures, 0
  stale. Record repair/s160/S160.md (S8, S9) and S8_REPORT.md. Open: OPEN_WORK s160 line (pregabalin requote and
  label, optional LOWs, no ADHD diagnosis brief). Next pharm batch B3 (s161) needs Jonathan's Q4 answer first.

Older State bullets (s156, s158 and s159 at the s162 ship; s155, s157 and s157b at the s160 ship; s154 to s154j and the 2026-10-26/28 NBME intakes at the
s159 ship) moved to repair/efficiency/STATE_ARCHIVE.md (runbook S9: keep the start-up files small).

## Next launch prompt (paste into a fresh chat)

s167 (UI refactor part 2) is next per D-20261106-8. The budget is Claude's proposal; Jonathan sets it at launch:
```
Step2Haki: launch batch s167 (UI refactor part 2; site layer only, content frozen) per claude/BATCH_RUNBOOK.md section 8, DECISIONS_DIGEST D-20261106-8 item 2 and repair/s164b/S164B.md "Deferred" items 1 to 5: the review redesign first, then the raw-color pass, the dehack of specificity workarounds and !important, all transitions and animations to spring timing (ui_lint motion_not_spring 60 to 0), steps 5b to 5f, and the 6b permanent gate tests. The ui_lint and prose ratchets are already in the gate (s165b, D-20261106-11); ship.sh lowers the baselines as each step lands. Item 6 (the two s164b residues) stays deferred. Same ship, docs: per Jonathan 2026-11-07, (a) no header word cap: header_long and title_long stay report-only (TEXTBOOK_STYLE rule 6, D-20261106-11 amended); (b) BATCH_RUNBOOK's hashed-specs paragraph lets a rules-only batch edit those files when its digest line records that receipts went stale, with that line for s165b; (c) motion baseline 60 confirmed until this batch converts them. Screenshots at the end for my ship. Budget: lead 100M.
```

s166 (phone navigation) is paused on wip/s166 (private bundle claude/pending/s166/wip_s166.bundle); it resumes after
s167 on the cleaned CSS, and wip/s166 merges main first (digest ids D-20261106-8 to -11 follow its -6 and -7).

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
