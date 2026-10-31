# Handoff State archive

State bullets moved out of STEP2HAKI_HANDOFF.md to keep the start-up files small (runbook S9). Newest first.

## Moved at the s159 ship (2026-10-31)

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
