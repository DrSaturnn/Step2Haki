# s33 plan: plain-voice pass, every system except GI

Base page: `scratch/s33_base.html` = index.html (HEAD eec1555) + `repair/s33/01_mechanical.json`. GI (21 briefs) had its voice pass in s29/s30 and gets only the mechanical ops. Do not commit, push or run ship.sh until Jonathan reviews.

## Files, in build order

1. `01_mechanical.json` (280 replace ops, page-wide, GI included): 8 trap section labels renamed to "Distractors" (7 "Trap autopsy", 1 "Why the distractors fail"); 249 `.trapwhy` lines and 23 `<b>Option</b>` lines in the renamed blocks changed from "Option — why" to "Option: why". Verify PASS; render unchanged (mcq 2014, crit gridded 123/124, vignette gridded 129/129, dl.rows 420, ul.facts 206, masks 3823, identical before and after).
2. `10_voice_<system>_<n>.json`: one per packet below, written by workers against the base, each verified with `python3 tools/verify_edits.py repair/s33/10_voice_<system>_<n>.json scratch/s33_base.html --voice`. Packets: `repair/sources/s33_voice/packet_<system>_<n>.md` (local-only).

## Counts per system

| System | Briefs | Packets |
|---|---|---|
| msk | 30 | 6 |
| peds | 13 | 3 |
| cv | 18 | 4 |
| pulm | 15 | 3 |
| renal | 20 | 4 |
| endo | 13 | 3 |
| heme | 10 | 2 |
| id | 20 | 4 |
| neuro | 18 | 4 |
| derm | 8 | 2 |
| obgyn | 14 | 3 |
| prev | 7 | 2 |
| **Total** | **186** | **40** |

## Packets

| Packet | System | Briefs |
|---|---|---|
| `packet_msk_1.md` | msk | pmr, biceps, cts, dequervain, meralgia |
| `packet_msk_2.md` | msk | scaphoid, backpain, hippos, gtps, inflam-back |
| `packet_msk_3.md` | msk | oa-pharm, septic-bursitis, septic-hip, synovitis, limp |
| `packet_msk_4.md` | msk | sjia, nursemaid, scfe, myositis-ossificans, growing-pains |
| `packet_msk_5.md` | msk | bone-tumors, scheuermann, bs-septic-adult, bs-lbp-acute, bs-synovitis-mgmt |
| `packet_msk_6.md` | msk | bs-puncture-osteomyelitis, bs-acute-myositis, bs-torticollis, bs-brachial-plexus, shoulder-rom |
| `packet_peds_1.md` | peds | growth, neonatal-maternal-labs, newborn-hormone, aneuploidy, malform-syndromes |
| `packet_peds_2.md` | peds | bs-learning, bs-nat-fracture, bs-shock, bs-infant-feeding, bs-tanner |
| `packet_peds_3.md` | peds | bs-ftt, bs-preterm-followup, aq-infant-hypotonia |
| `packet_cv_1.md` | cv | chf, ascvd, angina, ie-ppx, secondary-htn |
| `packet_cv_2.md` | cv | dvt, ped-murmur, cyanotic-chd, right-murmurs, htn-drugs |
| `packet_cv_3.md` | cv | newborn-cyanosis, kawasaki, arf, myocarditis, del22q11 |
| `packet_cv_4.md` | cv | bs-murmur-map, bs-shunt-timing, bs-adolescent-bp |
| `packet_pulm_1.md` | pulm | copd, asthma-copd, cough, pneumoconiosis, rhinitis |
| `packet_pulm_2.md` | pulm | sinopulm-structural, hypoxemia-mech, abpa, scd-dyspnea, airway |
| `packet_pulm_3.md` | pulm | mycoplasma, uri, asthma, bpd, bs-nrd |
| `packet_renal_1.md` | renal | pyelo, bph, nephropathy, hematuria, scrotum |
| `packet_renal_2.md` | renal | hypercalcemia, vur, peds-uti-recurrent, enuresis, polyuria |
| `packet_renal_3.md` | renal | peds-aki, nephrotic-child, bs-puv, bs-pyelo-organism, bs-incontinence |
| `packet_renal_4.md` | renal | bs-enuresis, bs-nephritic, bs-abdominal-mass, bs-isolated-proteinuria, aq-puffy-eyes |
| `packet_endo_1.md` | endo | thyroid, levo, gynecomastia, prolactin, osteoporosis |
| `packet_endo_2.md` | endo | preg-thyroid, congenital-hypothyroid, tumor-syndromes, precocious-puberty, homocystinuria |
| `packet_endo_3.md` | endo | bs-dexa-highrisk, bs-dm-bundle, bs-short-stature |
| `packet_heme_1.md` | heme | anemia-thrombocytopenia, drug-hemolysis, dipstick-mismatch, microcytic-anemia, factor-inhibitor |
| `packet_heme_2.md` | heme | transfusion, bs-leukemia, bs-spherocytosis, bs-sickle-trait, aq-bruising |
| `packet_id_1.md` | id | tb, meningitis, hiv-vax, dtap, cervicitis |
| `packet_id_2.md` | id | ig-panel, rmsf, lymphadenitis, herpangina, cgd |
| `packet_id_3.md` | id | bs-pta, bs-torch, bs-neonatal-sepsis, bs-fever-rash-arthralgia, bs-exanthems |
| `packet_id_4.md` | id | bs-anaphylaxis, bs-isolation, bs-foodborne, bs-febrile-infant, aq-infant-fever |
| `packet_neuro_1.md` | neuro | hearing, redeye, cluster, sellar-mass, peds-headache-imaging |
| `packet_neuro_2.md` | neuro | cholesteatoma, febrile-seizure, cerebral-palsy, abrs-complications, vpshunt |
| `packet_neuro_3.md` | neuro | retinitis-pigmentosa, tics, bs-tethered, bs-reye, bs-peds-stroke |
| `packet_neuro_4.md` | neuro | bs-imprinting, bs-posterior-fossa, aq-child-headache |
| `packet_derm_1.md` | derm | psoriasis, cellulitis, footulcer, eczemaherp, peds-alopecia |
| `packet_derm_2.md` | derm | neonatal-rash, diaper-dermatitis, bs-scabies |
| `packet_obgyn_1.md` | obgyn | preg-vax, cervical, pmb, ectopic, hpv |
| `packet_obgyn_2.md` | obgyn | adolescent-aub, contraception, fibroids, teratogens, primary-amenorrhea |
| `packet_obgyn_3.md` | obgyn | bs-cervical-gate, bs-tdap-preg, bs-genital-ulcer, bs-pid |
| `packet_prev_1.md` | prev | smoking, lipid-screen, preop, elder, vegan |
| `packet_prev_2.md` | prev | bs-adolescent-confid, bs-adolescent-vax |

## Notes for workers and review

- Left for the voice workers (not mechanical): 30 non-structural trap lines whose option sits inside a sentence ("Fibrinogen dysfunction tempts as a coagulopathy, but the PT is normal — ...", 13 with `&mdash;`, 17 with a literal dash), and 11 more whose reason has a second dash. The rules tell workers to rewrite these as "Option: why" or use other punctuation. A few converted lines now read "Option: label: reason" (bs-enuresis, bs-reye, bs-adolescent-confid); the rules ask for one colon per line.
- Not renamed: "Decoy note" (34) and one-off decoy labels ("Two familiar decoys", "The two traps in one stem"); they explain a stem decoy, not the distractor list.
- Three brief titles contain an em dash (The Limping Child — Master Table; The Febrile Infant — Finding the Source; Cerebral Edema in a Child — Reye Syndrome). Pairs-with quotes of them are allowed by the verifier; retitling stays in PENDING_DECISIONS.
- Verifier changes for this pass (`tools/verify_edits.py --voice`): digits inside `--- <i>Batch N ...</i>` notes do not count as dropped numbers; an em dash inside a bold span that is an exact brief title is allowed; an op that changes any "How NBME framed it" text, or edits a block with that label, fails.
- Rules added to `repair/efficiency/RULES_voice.md`: "Page-wide decisions (s33)" and "Internal and workflow text: remove wherever seen".
