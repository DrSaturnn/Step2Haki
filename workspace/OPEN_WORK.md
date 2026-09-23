# AxBx open work — carried forward

Updated 2026-09-22. Replaces the stale lists in `RESIDUALS.md` where they disagree.

## Intake rule for pasted questions (user, 2026-09-22)
1. Every pasted question ends with its nid(s). Grep the page for each nid first: a match means a duplicate, skip it.
2. No nid match but the topic has a brief: backfill it there, with the new stem as a `data-src="uworld"` item carrying `data-nid`, plus any explanation facts the brief lacks.
3. Library entries pasted alongside: mine them for facts missing from the brief (or elsewhere on the page).
4. New brief only when no brief owns the objective.

## Gate (every pass)
- `tools/gate.py index.html --base <rev>`: item, option and brief id canaries (count vs set, Counter only on failure); every item answerable (3 distinct option ids and 3 distinct option texts); permanence (no id lost since base); nid reuse (info); near-duplicate stems with the same key via an inverted index (info, hand-check before quoting). About 1 s.
- `repair/apply_ledger.py` refuses to write if any new item or brief id is already on the page, then runs the gate after writing.
- New ids from `tools/idgen.py` (brief, type, full key, full stem). Earlier passes seeded on stem[:60] without the brief; those ids stay as they are.
- Open finding: the PDA item "Preterm infant with a continuous murmur below the left clavicle..." exists word for word in both `bs-murmur-map` and `bs-shunt-timing` (q_3f503b9a2dee51438e7c, q_9696867d34855f3c8457). User's call: keep, or rewrite one as a distinct variant.

## Waiting on source material (fill as questions are posted)

Standing workflow: paste the question **and the full vendor explanation** together. Numbers traced to the pasted explanation ship clean; anything else gets ⚠︎.

### needs_source items (user decision: hold, fill from future questions)
Left as `data-item-status="needs_source"`. They stay readable and are excluded from graded practice. When a matching question arrives, rewrite each as a standalone stem (no "Same patient…" opener, Rule 13b), bump `data-item-version`, set `ready`.

| Item | Brief | Tests | Needs |
|---|---|---|---|
| `q_9d537e5889785e8a9e13` | `osteoporosis` | FRAX before DXA | age, menopausal status, screening vs risk task |
| `q_20a5148448175ae08410` | `preg-vax` | Anti-D at 28 wk | Rh status, prior anti-D |
| `q_72513ee1f6ec5f1e8d41` | `preg-vax` | Tdap timing | gestational age, prior Tdap this pregnancy |
| `q_f255f175943c5046bf30` | `preg-vax` | MMR postpartum | rubella status, breastfeeding |

Corpus check 2026-09-22: these are the only four items opening with "Same…".

### New briefs (user decision: author when/if the question is posted)
- **Infant of a Diabetic Mother.** Never saved; must be re-authored. Salvage: three IDM items already in `bs-nrd` (surfactant `next`, PGE1 `next`, hyperinsulinism-delays-surfactant `mech`) and the IDM row in `del22q11`. Needs a source question for the `.vignette`.
- **Hodgkin lymphoma, supraclavicular node.** Zero coverage anywhere on the page.
- **Salt-wasting CAH.**
- **IgA vasculitis (HSP).**
- **Pellagra / nutritional-deficiency hub.**
- **Beckwith-Wiedemann.** Partial spine exists in `malform-syndromes` and `tumor-syndromes`; likely scope is "the overgrowth syndromes".
- **Scoped, unwritten (11):** hemangioma, Rett, Friedreich, neonatal cholestasis, pediatric acute hemiplegia, Meckel/intussusception, neurocutaneous syndromes, pediatric dehydration, neonatal jaundice, hypospadias, FGR.
- **Lost addenda (treat as unwritten):** `limp` x-ray-tell addendum; `precocious-puberty` obesity-mechanism item.

Before authoring any of these: check existing coverage first (board-brief 7.9). A fast miss on covered content is a review problem, not a new brief.

## Structural work (no source needed)
- **Never-keyed diagnoses:** `nk.py --input index.html` reports 16 at ≥4× after s02. Advisory. Known alias gap: "hip osteoarthritis" is keyed as "Hip OA" in `gtps`, so it is a false positive. "Iron deficiency anemia" never keyed: fold into the `microcytic-anemia` tuple pass.
- **12 figures** not redrawn (list in `RESIDUALS.md`). Six now have a reference image in `~/pics/IMAGE_CATALOG.md`: tet episode (132, 1), cyanotic circuits (136), Potter cascade (93), FAS face (191), Friedreich cord (186), shunt circulation (17, partial).
- **Image catalogue** (`~/pics/IMAGE_CATALOG.md` + `.csv`): 228 unique AMBOSS images; 54 high and 51 med matched to 62 briefs. Reference only: never embed, recreate as SVG, table or spine. Next step (user's call): choose which to redraw first.
- **⚠︎ census after s04 (entity-decoded):** 179 total; 0 in bank items. Remaining flags are in tables, pearls, danger, crit and one dp. Count by decoding entities, never by grepping digits: option ids like `o_…9888…` false-match a raw "9888" search.

## Closed
- 2026-09-22 s01: `bs-adolescent-confid` rowspan restructure. Exceptions moved to a `.crit` tile (grids and masks); table reduced to the protected-services column. No item changes.
- 2026-09-22 s02: self-keying pass. The 7 briefs never keyed their own diagnosis (only a distractor). Retitled `cgd` → Recurrent Abscesses and Granulomas, `gtps` → Pain Around the Hip and Thigh, `eczemaherp` → Atopic Dermatitis Complications; nav for those three plus `lymphadenitis`. `cyanotic-chd` and `bs-shunt-timing` titles kept (6 inbound Pairs-with links, titles don't name the missing key). One new `dx` item per brief keying its diagnosis; 1,556 → 1,563 items. Cue review: key longest on 4/7 (TOF +1, VSD +1, lymphadenitis +4, GTPS +13 as a full disease name); no shape cues.
- 2026-09-22 s03: all-`dx` pass. 27 `next`/`test`/`avoid`/`screen`/`mech` items added across secondary-htn (4), cough (4), pneumoconiosis (4), liver-preg (3), thyroid (4), psoriasis (4), neonatal-rash (4), each built only from that brief's table, decision point or pearls; no new numbers; 4 carry `data-lead-in`. 1,563 → 1,590 items. Cue review: key uniquely longest 10/27 after relabelling three (PPI trial d2, psoriasis first rung, miliaria key).
- 2026-09-22 s04: residuals. Tuple-set line in `RESIDUALS.md` was stale: RDW/RBC items already live in `microcytic-anemia`; `vur` and `bs-torch` already mixed. Filled real gaps (+8 items): microcytic-anemia keys IDA and anemia of chronic disease; ped-murmur +2 `next`; bs-puv +2 `mech`; bs-leukemia +1 `next`, +1 `stage`. 1,590 → 1,598 items. Both bank-item flags resolved by targeted verification: `del22q11` v3 (IDSA 2013 live-vaccine gate stated; key unchanged); `bs-galactosemia` v2 (CSF culture added per AAP 2021 febrile infant guideline; ⚠ removed from inside the key, where it rendered on the correct option button only; distractors rewritten as parallel workups).
- File naming (corrected by prior session): `ax/w20.html` was that toolchain's working file and `index.html` the deploy copy; `w` + counter is a generation series (w16 = 152 briefs, w20.bak = 167, w20 = 181). This session does not use the `ax/` scripts and hands back `index.html`; if the `ax/` tooling is resumed, copy the result to `ax/w20.html` too.
- 2026-09-22 s05: backfill. `meningitis` + early meningococcal disease block, source item (nid 1481771577462), 1 dx item, 4 traplines. `febrile-seizure` + counselling/test-indication block from explanation and library, source item (nid 1513200856433), 3 items; one ⚠︎ cleared (complex seizure recurrence verified in library entry). nids added to earlier source items in airway, malform-syndromes, polyuria, occult-gi-bleed. 1,598 → 1,604 items; ⚠︎ 179 → 178.
- 2026-09-22 s06: backfill, 3 questions, no nid previously on items (IVH nid 1483930621644 was a shared alternate on `cerebral-palsy`, a different question). `bs-preterm-followup` + symptomatic IVH block, source dx item, cranial ultrasound item. `lymphadenitis` + infected branchial cleft cyst row, congenital neck masses by location block, source item, thyroglossal and laryngocele items. `cgd` + hyper-IgE row, reading-the-CBC block, source item, Chediak-Higashi and cold-abscess mechanism items. 1,604 → 1,612.
- Thalassemia miss selection: user says not needed. Dropped.
