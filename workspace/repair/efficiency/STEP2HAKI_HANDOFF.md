# Step2Haki running handoff (the single running state file)

Last updated: 2026-10-30, by Claude (s157b shipped; s156 still parked).
It lives in the repo at workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (added 2026-10-14 so Claude Code sessions outside the project can read it; a session rewrites State here after every step and pushes), with copies in the project (STEP2HAKI_HANDOFF.md) and on the Mac (~/Documents/Step2Haki/), refreshed at ships when those are reachable.
Batch history lives in each batch's file (claude/pending/S134.md, S136.md, S137.md and so on), not here (s135 efficiency item 4).

## Restart prompt (the only current one)

```
Step2Haki: continue the current batch per claude/RESUME.md.
```

## State (rewrite after every step)

- **Open batch: s158** (Claude lead; launched 2026-10-30 00:41 EDT; wip/s158 in both repos; batch file
  repair/s158/S158.md). Four new psych briefs: trauma-stress (disease), cluster-c (disease), stages-change (lookup),
  sexual-dysfunction (disease); plan claude/pending/NEW_BRIEFS_2026-10-30.md. Budget 20 agents, 700 calls, 58M agent
  tokens (builders 6, 520, 50M; reviewers 14, 180, 8M); lead 80M. Step: S1 to S3 builders done (4 BUILT, lead verify PASS); S3 chat 1 done (coverage rows,
  batch page gate PASS); next: S3 chat 2, drawer pointers in live briefs (repair/s158/S158.md "Next chat: exact steps").
  Spend: builders 4 agents, 198 calls, 21.23M of 58M; lead chat 1 108 calls, 24.96M of 80M.

- **Parked: s156** (wip/s156 in both repos, main merged in after the s157 ship; batch file repair/s156/S156.md).
  Its own State, as parked on 2026-10-29, is in that branch's copy of this file (13.2M of 78M agent tokens left); the
  restart line continues it per RESUME.md.

- **Previous: s157b SHIPPED 2026-10-30** (Claude lead; patch of the 2026-10-29 NBME intake, Psychiatry CMS Form 8:
  toxidrome Barbiturate row, antipsych-effects Dementia commit line, ssri-effects and mood-anticonv bait items): commit
  50bef79, page d3e594f55987 (approved candidate 9175b91425a2). Reviewers 4 agents, 18 calls, about 0.12M of 1.2M; lead
  one chat. Record repair/s157b/S157B.md. Main merged into wip/s156 in both repos after the ship.

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

- **Previous: s154i SHIPPED 2026-10-28 (Claude lead; patch of the 2026-10-28 NBME intake proposals,
  Psychiatry CMS Form 7, seven briefs: disruptive-behavior, antipsych-effects, ssri-effects, bipolar-mania, tca-tox,
  suicide-risk, somatic): commit c58a0e7, page c8ae474533a5 (approved candidate bbde22d77c91); reviewers 6 agents, 24
  calls, 0.74M of 1.5M; lead one chat, about 13M of 40M. Record repair/s154i/S154I.md (S9). queue.csv: six 2026-10-28
  NBME rows closed "picked up s154i". Open: nephrotic-child and airway "Pairs with" pointer problems; bipolar-mania
  claim S924 summary wording (record only); disruptive-behavior header "Disorder" over the normal-development row.

- **Previous: s154j SHIPPED 2026-10-28 (Claude lead; pause point repair, 34 blocks in 22 briefs, plus the
  pause-content checker rule): commit 5d50b97, page 98584de30e65 (approved candidate dfe76de97831); reviewers 5 agents,
  20 calls, 0.76M of 3M; lead one chat, about 31M of 60M. Record repair/s154j/S154J.md (S9). The gate carry rule was
  reverted after the ship (strict rule passes the live page). Next: s154i (prompt below; re-take its bipolar-mania
  baseline, since s154j changed that brief's pause point). Open: nephrotic-child and airway "Pairs with" pointer problems.

- **NBME intake 2026-10-28 (no batch, log-only):** Psychiatry CMS Form 7, 21 items (16 new, 5 repeats of the s37
  items, whose form is now known to be Form 7); private main 0dbd6528, public 6b08d77. Seven delta-ready proposals,
  repair/sources/intake/*_2026-10-28.md: disruptive-behavior (normal adolescence row + item), antipsych-effects (item),
  ssri-effects (pointer), bipolar-mania (item), tca-tox (row), suicide-risk (row), somatic (row). Baits on the three
  misses are inferred. Next: patch s154i (prompt below). Pause points: Jonathan flagged some as repeating table info;
  Jonathan chose rewrite-or-delete plus a checker rule (STANDING_DIRECTIONS "Pause point content"). s154j is scoped
  delta-ready in the private repo, claude/pending/s154j/ (34 blocks in 22 briefs, all rewrites; lint patch; candidate
  page passes the gate). Order: s154i, then s154j (prompt below).

- **Previous: s154h SHIPPED 2026-10-27 (Claude lead; patch of the 2026-10-26n NBME intake proposals, seven
  briefs: capacity, lithium-effects, panic, psychosis-duration, somatic, substance, toxidrome; bipolar-mania dropped,
  shipped in s154g): commit b760dbd, page 61f7c01a67b0 (approved candidate 5f885ef53c56); reviewers 5 agents, 20 calls,
  0.66M of 1.5M; lead one chat, about 24M of 40M. Record repair/s154h/S154H.md (S9). queue.csv: the ten 2026-10-26 NBME
  rows of the 26n proposals closed "picked up s154h".

- **Earlier: s154g SHIPPED 2026-10-27 (Claude lead; NBME presentation layer: descriptions in 16 psych briefs,
  X2 valproate row, X1 tags, view C): commit 829b4df, page 2f991ffe3411 (version.json build s154g); reviewers 6 agents,
  19 calls, 0.55M of 4M; lead 2 chats, 36.5M of 120M. Record repair/s154g/S154G.md (S9). Next: the 2026-10-26n intake
  patch (s154h, prompt below; Jonathan confirms or corrects the inferred baits first).

- **Previous: s154f SHIPPED 2026-10-27 (Claude lead; psych format patch, 20 briefs): commit 6c004d5, page
  c01f18a2e48e; reviewers 10 agents, 44 calls, 1.96M of 4M; lead about 56M of 120M. Record in repair/s154f/S154F.md
  (S9 section). Next: s154g, the NBME presentation layer (S154F.md "C3", claude/pending/NBME_PRESENTATION_SPEC.md "Mockup
  v1"), launched by its own prompt per the runbook's full read order (a launch is not a continuation).

- **NBME intake 2026-10-26 (no batch, log-only):** 16 Psychiatry CMS items (form 6 inferred from AnKing Form_06 tags;
  Jonathan to confirm; no item numbers; NBME platform Q IDs 749759 to 749782) saved to their owners' s-intake files
  (private main 6fea4834); queue.csv and misses.csv rows dated 2026-10-26, source nbme. 7 correct, 9 incorrect; his
  picks were not in the paste, so every bait is inferred (each proposal says which distractor to swap if his pick
  differs). Eight delta-ready proposals, repair/sources/intake/<brief>_2026-10-26n.md (the "n" suffix because the
  same-date files shipped in s154d): panic (alprazolam rebound row; GAD bait item), psychosis-duration (older adult
  with chronic psychosis row; alcohol pause point block; negative-symptom bait item), lithium-effects, toxidrome and
  substance (bait items), capacity (comfort care row), bipolar-mania (valproate pancreatitis), somatic (optokinetic
  nystagmus row). Two new-brief rows (adjustment disorder with anxiety; PTSD in a neglected child) await the trauma
  home (NEW_BRIEFS_2026-10-26.md section 3). Analysis: claude/pending/NBME_VS_UWORLD.md (project and private repo).
  nbme-intake confirmed stale (retired 2026-10-13 but its description never said so); a card retiring it and
  updating board-brief was offered in the chat (form inference from tags, the platform Q ID, pp-b pause blocks,
  proposal file suffix).

- **s154e shipped** (Claude lead, 2026-10-26, site layer): 5bfeaa8, page 0a73166d7c32. The pause point has the muted
  caution tint again (ax-s154e; var(--caution-bg)). Record repair/s154e/S154E.md. No batch open.
- **s154d shipped** (Claude lead, 2026-10-26, patch): 1dd87de, page 00f49879e28d. Ten psych briefs amended from the
  2026-10-26 intake. Record repair/s154d/S154D.md. Spend: reviewers 4 agents, 15 calls, 0.57M of 1M; lead about 20M of
  30M. No batch open.
- **Open from s154d (none blocks):** functional tremor management has no home (somatic treatment step); psych-medical
  claim S903 says "often" where the line says "usually" (both within the quote); queue.csv open 2026-10-26 rows are the
  six new-brief rows (homes await Jonathan: trauma and dissociative, the first response in the interview, abnormal
  movements hub, Cluster A).
- **s154c shipped** (Claude lead, 2026-10-26): b002059, page 3c9ccb59ba04. Every spine brief's pause point (105) is
  question-style blocks (STANDING_DIRECTIONS "Pause point format"; gate and lint "pause-format"; builders use spinelib
  pause_blocks or a golden's div.sp-pause). Record repair/s154c/S154C.md. Spend: reviewers 11 agents, 51 calls, 2.47M of
  5M; lead about 36M of 80M. No batch open.
- **Open from s154c (none blocks):** private repo synced (main 883ad34d);
  33 folders keep outline_before_s154c.json (a later
  rebuild from outline must first fold in the s154c delta); the s154c tool notes (ready_gate AX_READY_JOBS=2 for big
  batches; a background command stops at 2 h). The "pause point does not count" rule lives in DIGEST
  2026-10-26 and the tools only: do not edit STANDING_DIRECTIONS for it (Jonathan 2026-10-26: "definitely dont need to re
  review every brief"); fold it in only in a batch that already re-reviews every brief.
- **Decision 2026-10-26 (DIGEST):** NBME wording in authored items held (older form); first work is cross-domain
  question types, then the NBME phrasing layer. Spec draft claude/pending/NBME_PRESENTATION_SPEC.md (project and private
  repo); the mockup prompt is below.
- **Next chat:** the NBME presentation mockup, or the patch of the 2026-10-26n NBME proposals (runbook 8b; confirm Jonathan's picks first, see
  each proposal's Edit note), or s155, or the population mockup (prompts below). The 2026-10-26 proposals that touch a
  pause point were written as question-style blocks (pp-b; gate "pause-format").
- **Queued 2026-10-26 (no batch open):** intake of 24 UWorld questions and 11 library articles; 11 delta-ready proposals
  in repair/sources/intake/*_2026-10-26.md (psychosis-duration, bipolar-mania, substance, psych-medical, mdd, eating-disorders,
  somatic, delirium, antipsych-effects, ssri-effects; the patch prompt below takes them). Decisions (DIGEST 2026-10-26): pointers
  to the owning brief; attribution traps in pause points; one bait-built practice item per covered miss; pause points
  became question-style blocks (s154c, shipped); a new
  population entry type (mock up Perinatal Psychiatry first) and the Cluster A hold lifted (claude/pending/NEW_BRIEFS_2026-10-26.md).
  Three homes await Jonathan (trauma and dissociative; the first response in the interview; abnormal movements hub).
  Board-brief skill update proposed as a card (bait items, pointers, pause point baits); its private copy is updated.
- **s154b shipped** (Claude lead, 2026-10-26, patch): 707bd07, live version s154b, page 82a09c3e0aee. Eight psych briefs
  amended from the 2026-10-25 intake. Record repair/s154b/S154B.md. Spend: reviewers 4 agents, 14 calls, 0.42M of 1.5M;
  lead about 20M of 40M. No batch open.
- **Open from s154b (none blocks):** private main lacks wip/s150c and wip/s150e (MDD, SLEEP, TOX, DEM, EAT folders now
  on private main via the s154b sync); s150cd tarball still owed; patch.py reps misses text held by two chained changes;
  queue.csv open: stillbirth new-brief row (64468a8fef), row 59 prolactin.
- **s154 shipped** (Claude lead, 2026-10-25): 78bb0a2, live version s154, page f6bfe9e7dae1. Seven pediatric GI briefs on the
  spine; infant-stool, feeding-refusal, rlq-pain, peds-constipation, cyclic-vomiting and bs-umbilical are hubs (Presentations
  36); bs-tef disease. Record repair/s154/S154.md; history in OPEN_WORK. "ship" took the report defaults (DIGEST 2026-10-25
  s154 ship). Spend: wave 24 agents, 633 calls, 58.77M of 60M; lead about 90M of 100M (four rows). No batch open.
- **Open from s154 (none blocks):** six deferred LOWs (repair/s154/adj_r2_passif.md; peds-constipation trap comma;
  feeding-refusal Wilms alias); ALIASES.json: patent urachus, patent omphalomesenteric duct, Wilms tumor (nephroblastoma);
  no brief owns appendicitis or Crohn disease; cyclic-vomiting prophylaxis (no board source); review_packet flattens blocks
  (packet error); builder lanes must sync their web cache; batch.py ship needs main fetched before its moved-main check;
  Mac copies of index.html and this file.
- **s153 shipped** (Claude lead, 2026-10-25): 7b301ef, live version s153, page 7c376718303a. Eight GI and hepatology A
  briefs on the spine; cholestasis and occult-gi-bleed are hubs (Presentations 30). Record repair/s153/S153.md; history
  in OPEN_WORK. Jonathan's "ship" took the report defaults (DIGEST 2026-10-25 s153 ship): S1 to S3 by builder agents
  adopted; liver-preg, fap, occult-gi-bleed and masld kept as built. Spend: agents 29 of 38, 752 of 1270 calls, 65.61M
  of 74M; lead about 104M of 120M (six rows).
- **Open from s153 (none blocks):** MASLD entry for ALIASES.json; lens "preg" not in SPINE_SPEC; bs-wilson bank stems
  carry INR and IgG unexpanded; cholestasis hub 858 words (cap 700); fap 1379 words above the bank; tool notes
  (build_brief needs AX_BATCH; verify sh() can hide a killed render.js; reps.py does not reach author.py builds; drop a
  stale gate allowlist line for a batch brief only after ship); carried tail blocks are not in claim_map; volvulus
  Step 2 card has no note id; Mac copies of index.html and this file (computer not reachable at the s153 ship).
- **Owed from s152:** the two newborn-cyanosis jaundice items (q_30529e70c634, q_4ee70a03ddd6) move to neonatal-jaundice
  when that brief is converted; deferred LOWs in repair/s152/S152.md "S7"; Kawasaki AHA 2024 In practice hover
  unsourced.
- **Private files owed (important):** s150cd_private_owed.tar.gz (s150c and s150d brief-folder changes after S7) was
  sent to Jonathan in the s150c chat and never pushed; the next session with push access and the file extracts it into
  the private clone's local-only/, commits on wip/s150c and merges to main.
- **Carried:** s150c round 4 deferred LOWs (dementia Korsakoff reason d1; eating-disorders "step 2 criterion"
  wording); defense-mechanisms intro clause unmasked; no reverse pointers to dementia or defense-mechanisms from
  delirium, parkinson or cluster-b; MPTP chemical-name LOW; s150b legibility advisories; the four s150b audit proposals;
  queue.csv open row 59 (prolactin); row 66 QID to link. Figma and Vercel are off (checked 2026-10-26); the healthcare and design plugins still load
  through the linked Mac (about 3k to 5k of start-up).

## Next launch prompt (paste into a fresh chat)

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
