# Migration pilot: frozen rubric (written before any run, 2026-09-28)

Question: does a lean worker packet cut tokens per accepted migration cluster without losing content, clues or questions, versus a worker that reads the full skills (board-brief, brief-migration, study-page-builder)?

## Design
- Cluster M1: `kawasaki` (one old brief, 10 items, 1 NBME item q_5c5ebd26ef5fe11337d5 / peds-cms-42aa4f, no data-nid). Primary id stays `kawasaki`; no aliases.
- Baseline page: commit b824f3f. Old block extracted to the scratch `kawasaki_old.html`.
- Arm C (full spec): TASK.md + reads the three SKILL.md files itself.
- Arm P (lean packet): TASK.md + PACKET.md (template, clue ledger, item rules, migration rules, voice, condensed); told not to open skill files or the page.
- Shared inputs in both arms: TASK.md, old brief HTML, NBME source text (local-only), Type C markup reference (the approved hip preview, hip3.html), tools/idgen.py, tools/migrate_check.py.
- Same model (inherited), one run per arm. Expected checklist below is not given to workers.

## Metrics
subagent tokens, tool uses, duration per arm, from the Agent tool result. Primary: tokens per ACCEPTED cluster. Packet build cost reported separately.

## Acceptance (all must pass)
Mechanical: `tools/migrate_check.py` PASS (WARN allowed); new brief renders in the live-page preview with no new console error; every item has 3 distinct options.

Content checklist (blinded reviewer; each point present and correct = 1; 14 points):
1. Diagnosis rule: fever 5 days or more plus 4 of 5 principal criteria, each criterion with its qualifier (bilateral nonexudative limbal-sparing conjunctivitis; polymorphous rash with perineal accentuation; cervical node 1.5 cm or more, usually unilateral, least common; red cracked lips and strawberry tongue without ulcers or exudate; hand and foot erythema and edema, then periungual desquamation in weeks 2 to 3).
2. IVIG 2 g/kg within 10 days of fever onset; still given after day 10 when inflammation persists; not delayed for workup or echo; aneurysm risk about 20 to 25% untreated vs 3 to 5% treated.
3. Aspirin high dose then low dose, as the exception to avoiding aspirin in children.
4. IVIG resistance: fever 36 hours after IVIG, second dose, with or without steroids or infliximab.
5. Echo at diagnosis, 2 weeks and 6 to 8 weeks; coronary changes alone justify treatment.
6. Incomplete disease: 2 or 3 criteria, infants under 6 months at highest risk, CRP/ESR then supplemental labs (anemia, low albumin, high ALT, sterile pyuria, platelets high after day 7) and echo.
7. Sterile pyuria is Kawasaki urethritis: no urine culture workup, IVIG not held.
8. Live vaccines (MMR, varicella) deferred 11 months after IVIG.
9. Mimics with discriminators: adenovirus, scarlet fever, SJS/TEN, staphylococcal scalded skin, toxic shock, measles, MIS-C.
10. Untreated sequelae: coronary aneurysm (expansion, rupture, infarction); heart failure picture (tachypnea, tachycardia, hypotension, cardiomegaly, ischemic ST depression); mitral regurgitation not stenosis; lungs and pulmonary vessels rarely involved.
11. NBME item carried with the same id and option ids, version bumped, stem now carries every source clue (age 18 months; 2 days of fast breathing and irritability; the illness 2 months earlier with high fever, conjunctivitis, red swollen hands, enlarged nodes, cracked red lips, resolving within 2 weeks without treatment; appears in obvious discomfort; T 38 C, HR 150, RR 60, BP 60/40; no other exam abnormality; cardiomegaly; right-axis deviation, left ventricular hypertrophy, ST depression in II and III), with its NBME framing note. MANDATORY.
12. All four NBME distractors (pericardial effusion, mitral valve obstruction, interstitial lung disease, thickened pulmonary arteriolar intima) each explained; the clue table gives each NBME clue a role.
13. All 10 old items accounted for; no item lost; no item opens "Same patient".
14. Pairs with New Heart Failure in a Child (myocarditis) kept; transferable rule (a diagnosis that explains only some findings is wrong) kept.

Quality points (each pass/fail): Step 2 scope (no specialist detail); factual accuracy (no wrong or changed claim; any correction has a source); voice (plain, no slogans, no em dashes, acronyms written out once).

Accept if checklist 13/14 or better with point 11 met, all 3 quality points pass, and the reviewer lists no CRITICAL finding (lost or changed fact, lost clue, lost question, wrong key).

## Decision rule
Adopt the lean packet for migrations only if (a) its acceptance equals or beats arm C across the two pilot clusters, (b) no critical defect appears in P that C avoided, and (c) tokens per accepted cluster fall 25% or more. This pilot is cluster 1 of 2 (the hip preview was built by hand and does not count).
