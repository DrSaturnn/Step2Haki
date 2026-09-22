# AxBx open work — carried forward

Updated 2026-09-22. Replaces the stale lists in `RESIDUALS.md` where they disagree.

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
- **All-`dx` briefs:** secondary-htn, cough, pneumoconiosis, liver-preg, thyroid, psoriasis, neonatal-rash.
- **Tuple sets unapplied:** PUV, ped-murmur, bs-leukemia, vur, microcytic-anemia (RDW/RBC), bs-torch (no action).
- **12 figures** not redrawn (list in `RESIDUALS.md`).
- **Bank-item ⚠︎ that could ship a wrong key:** `del22q11` (live vaccines at CD3+ 210/mm³), `bs-galactosemia` (E. coli sepsis, ampicillin + gentamicin).
- **⚠︎ census 2026-09-22 (entity-decoded):** 181 total: 69 td, 57 pearls, 42 danger, 10 crit, 2 bank li, 1 dp.

## Closed
- 2026-09-22 s01: `bs-adolescent-confid` rowspan restructure. Exceptions moved to a `.crit` tile (grids and masks); table reduced to the protected-services column. No item changes.
- 2026-09-22 s02: self-keying pass. The 7 briefs never keyed their own diagnosis (only a distractor). Retitled `cgd` → Recurrent Abscesses and Granulomas, `gtps` → Pain Around the Hip and Thigh, `eczemaherp` → Atopic Dermatitis Complications; nav for those three plus `lymphadenitis`. `cyanotic-chd` and `bs-shunt-timing` titles kept (6 inbound Pairs-with links, titles don't name the missing key). One new `dx` item per brief keying its diagnosis; 1,556 → 1,563 items. Cue review: key longest on 4/7 (TOF +1, VSD +1, lymphadenitis +4, GTPS +13 as a full disease name); no shape cues.
- Mirror `ax/w20.html`: retired by user decision; `index.html` is the only working copy.
- Thalassemia miss selection: user says not needed. Dropped.
