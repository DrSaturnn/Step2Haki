# s33 voice review: Neuro and OB/GYN (10_voice_neuro_1..4, 10_voice_obgyn_1..3)

This is an independent drift review. Base: `scratch/s33_base.html`. Each file was applied to the base on its own. Op index = 0-based position in the file's `edits` array. The verifier's "edit N" is this index + 1.

## Verification

Each file was run twice: first as `tools/verify_edits.py <file> scratch/s33_base.html --voice --report --no-render` to get the report, then without `--no-render`. Load was low (about 1), and render completed on every run.

| file | ops | result |
|---|---|---|
| neuro_1 | 44 | PASS, render PASS. 8 warnings: 4 long sentences; MR, CN and CSF not expanded in peds-headache-imaging. |
| neuro_2 | 45 | PASS, render PASS. 2 warnings: a 28-word sentence; EEG first use in febrile-seizure. |
| neuro_3 | 38 | PASS, render PASS. 2 warnings: BP and MR not expanded. |
| neuro_4 | 12 | PASS, render PASS |
| obgyn_1 | 28 | PASS, render PASS |
| obgyn_2 | 37 | PASS, render PASS. 8 warnings: LMWH, XY, FSH, LH and FISH first uses. |
| obgyn_3 | 21 | PASS, render PASS. 4 warnings: 3 long sentences; LEEP not expanded. |

Every remaining em dash in NEW text follows a `</b>` in a "·" grid row or decision-spine row, so each one is structural. The only other one is inside a Pairs-with title ("The Febrile Infant — Finding the Source"), which the rules allow.

## Summary

- CRITICAL: 1
- MINOR: 15
- Pre-existing (not drift): 10

Apart from C1, I found no dropped or strengthened numbers, cutoffs, ages, timing, drugs, tests or sequences. I also found no added clinical claims beyond acronym expansions. The expansions are correct in context. Checked: SNHL, BC/AC, HSV, TSC, IIH, LP, CSF, β-hCG, AFP, TSH, VP, ICP, HGPRT, JIA, ADHD, OCD, MECP2, CVS, VZIG, MCA, SCJ, CIN, LEEP, EIN, TAH-BSO, LNG-IUD, PCOS, OCP, PMB, PID, DMPA, GnRH, VTE, D&C, COC, ACE, DES, USPSTF and ACS.

## Flagged items: verdicts

| file/op | brief | item | verdict |
|---|---|---|---|
| neuro_1 op25 | sellar-mass | Pairs with: "covers the same complaint, a 13-year-old girl with worsening headaches" | Pre-existing (P2). OLD said the same thing ("Same complaint — a 13-year-old girl…"). The rewrite kept it and did not create it. |
| neuro_1 op39 | peds-headache-imaging | Pairs with: "at the same age and sex" | Pre-existing (P3). OLD said "Same complaint, same age and sex". |
| neuro_1 op16 | sellar-mass | .dp: "growth arrested at age 11 … Tanner 1 at 13" | No drift: the ages are carried exactly. They conflict with the source vignette (12 yo F, 6 months) (P1). |
| neuro_3 op26 | bs-reye | dropped "The stem hands you Reye syndrome and then refuses to offer it as an answer" | OK. This is framing about the option list, and it contradicts the brief's own vignette box, which lists Reye syndrome among the options. It was right to drop it. The mismatch underneath is pre-existing (P4). |
| neuro_3 op26 | bs-reye | "All five options can cloud consciousness" (OLD "Every option") | MINOR (M6). The number "five" is new. It is supported by the Option audit table (5 rows) but conflicts with the vignette box. It is also residual option meta. |
| neuro_4 op4 | bs-posterior-fossa | "Every abnormal finding is on the left and every one is cerebellar" | Pre-existing overstatement (P5). The rewrite kept it word for word. |
| obgyn_1 op2 | preg-vax | "anti-D is useless" | No drift. It is clinically correct: RhIG cannot help once the patient is alloimmunized. Voice only: see M8. |
| obgyn_1 op26 | hpv | pearl "do not restart and do not repeat" | Pre-existing contradiction with the bank item "Repeat the second dose → doses less than 5 months apart do not count" (P7). The rewrite kept the absolute wording. |
| obgyn_2 op30 / op36 | primary-amenorrhea | dropped "Most wrong options here are correct tests offered one step too early" | No clinical drift. "Most" counted answer options. The four named tests and "each is uninterpretable until the ultrasound" are kept. The claim map is loose: op36 cites a sentence without "most" as its carrier. See M11. |
| obgyn_3 op8 | bs-tdap-preg | label "Correction to an earlier framing in this document" changed to "Tdap outside the 27–36 week window"; dropped the Part I cross-reference | OK. This removes internal text. All the clinical content is kept: safe at any gestational age, wound or outbreak means give it now, 27–36 weeks is an optimization. The preg-vax row is already corrected in the base. |
| obgyn_3 op16 | bs-pid | "is the mandatory partner" became "is the paired brief" | MINOR (M12). "Paired brief" is page vocabulary, and "mandatory" is lost. The differential row "a pregnancy test is always mandatory" still carries the point. |

## CRITICAL

| # | file | op | brief | class | quote (NEW) | correct wording |
|---|---|---|---|---|---|---|
| C1 | obgyn_1 | 1 | preg-vax | scope lost: a stem-specific claim became a general rule | "In mid-September, the one due is influenza vaccine, given as soon as it becomes available, in any trimester." (OLD: "In the classic version the answer is signaled by 'mid-September' …: influenza vaccine") | Keep the scope: "In the classic version the visit is in mid-September, so influenza vaccine is due: give it as soon as it becomes available, in any trimester." As NEW stands, it states that influenza is *the* vaccine due in mid-September for any pregnant patient. That is false at 27–36 weeks, when Tdap is also due, and at 28 weeks Rh-negative, when anti-D is due. The page's own Tdap and anti-D rows state both. |

## MINOR

| # | file | op | brief | class | quote (NEW) | correct wording |
|---|---|---|---|---|---|---|
| M1 | neuro_1 | 18 | sellar-mass | slight overgeneralization | "medulloblastoma, the posterior fossa tumor" | "medulloblastoma, the posterior fossa candidate" or "a posterior fossa tumor". OLD meant the only posterior-fossa *option*. |
| M2 | neuro_1 | 34 | peds-headache-imaging | conditional flattened | "Papilledema → MRI with MR venography, then LP (lumbar puncture) with an opening pressure. The diagnosis is intracranial hypertension, idiopathic or drug-induced." | "…with an opening pressure; a normal MRI with a high opening pressure means intracranial hypertension, idiopathic or drug-induced." The workup table already states that condition. Also expand MR (magnetic resonance). |
| M3 | neuro_1 | 38 | peds-headache-imaging | residual meta; claim map not honest | "The option 'No additional testing' is rejected far more often because it feels too easy … This uniform-answer doubt costs points on every shelf." The dropped "Getting the threshold right and the modality wrong still scores zero" is mapped `to` the MRI/CT sentence, which does not carry it. | Replace with: "Reassurance is defensible only when you can name the criteria you cleared." Mark the "scores zero" claim `dropped` (exam framing). |
| M4 | neuro_2 | 24 | cerebral-palsy | residual option meta | "Three maternal drugs are named, and only one is an option." | Drop it, or: "Of the three maternal drugs named, antenatal corticosteroids lowered this infant's risk." |
| M5 | neuro_2 | 40 | vpshunt | slight strengthening (trap) | "Lumbar puncture: it is the standard workup for altered mental status, but…" (OLD "LP tempts as the standard workup") | "Lumbar puncture: it looks like the standard workup for altered mental status, but it is contraindicated in obstructive hydrocephalus because of herniation risk." |
| M6 | neuro_3 | 26 | bs-reye | new number; option meta | "All five options can cloud consciousness, but only one causes edema." | "Hyperammonemia, hypoglycemia, uremia, adrenal insufficiency and hypothyroidism can all cloud consciousness, but only hyperammonemia causes cerebral edema." |
| M7 | neuro_4 | 8 | aq-child-headache | expansion format | "blocked CSF flow (cerebrospinal fluid; hydrocephalus)" | "blocked cerebrospinal fluid (CSF) flow (hydrocephalus)", or "hydrocephalus from blocked <b>CSF</b> (cerebrospinal fluid) flow". |
| M8 | obgyn_1 | 2 | preg-vax | voice (kept blunt wording); expansion format | "so anti-D is useless; switch to titers and MCA Doppler (MCA, middle cerebral artery)" | "so anti-D can no longer help; follow antibody titers and <b>MCA</b> (middle cerebral artery) Doppler." |
| M9 | obgyn_1 | 16 | pmb | label does not fit the block | label "Benign explanations" over a block that also says "A progestin IUD is contraindicated in undiagnosed bleeding" | "Benign mimics and a contraindication", or "Fibroids, atrophy and the progestin IUD". |
| M10 | obgyn_1 | 8, 11, 16 | cervical, pmb | expansion format (acronym repeated inside the parentheses, or expansion placed away from the acronym) | "SCJ not fully visualized (SCJ, squamocolumnar junction)"; "contraindicated (ECC, endocervical curettage)"; "undiagnosed bleeding (IUD, intrauterine device)"; "HPV-vaccinated (HPV, human papillomavirus)" | Put the expansion directly after the acronym: "SCJ (squamocolumnar junction) not fully visualized", "ECC (endocervical curettage)", "progestin IUD (intrauterine device)". |
| M11 | obgyn_2 | 30, 36 | primary-amenorrhea | claim map loose (no page drift) | op36 `carried_by` "Each is uninterpretable … so ordering it first is one step too early." is used for "Most wrong answers are correct tests offered one step too early." | Mark it `dropped` (answer-option framing). The clinical content (the four tests are premature before the ultrasound) is carried in op30. |
| M12 | obgyn_3 | 16 | bs-pid | page vocabulary; "mandatory" lost | "Part I Ectopic Pregnancy is the paired brief." | "Part I <b>Ectopic Pregnancy</b> must always be considered with PID: both present as acute pelvic pain in a reproductive-age woman, and one test settles the fork. Ask: what is the pregnancy test?" |
| M13 | obgyn_3 | 10 | bs-tdap-preg | residual internal/page text (stale) | "Part I Vaccines & Timing in Pregnancy; this brief supersedes its Tdap timing row." | "Part I <b>Vaccines & Timing in Pregnancy</b> covers the other vaccines in pregnancy. Ask: 'Is this window a gate or an optimization?'" The preg-vax Tdap row already says "an optimization, not a gate", so "supersedes" is stale. |
| M14 | obgyn_3 | 4 | bs-cervical-gate | expansion placement | "HPV vaccination counseling (human papillomavirus)" | "<b>HPV</b> (human papillomavirus) vaccination counseling". |
| M15 | all 7 | many | — | claim map not honest (systemic) | `new_claims` copy the OLD claim text verbatim instead of quoting NEW: neuro_1 203/205, neuro_2 208/209, neuro_3 78/151, neuro_4 16/43, obgyn_1 61/110, obgyn_2 49/91, obgyn_3 27/83 (non-expansion new_claims). Example: neuro_1 op8 new claim "Topical steroids are the answer in uveitis and scleritis" vs NEW "are indicated". | The page text is fine. For the audit trail, new_claims should quote the NEW sentence. The same issue was raised as M4 in review_msk.md. |

Below the finding threshold (noted, no change needed):
- Unexpanded acronyms flagged by the verifier: MR, CN, BP, EEG (neuro_2 .pearls first use), LMWH, XY, FSH, LH and FISH. These are common enough, but they should be listed in the rewriter's skip list.
- neuro_1 op22: "germinoma or histiocytosis become more likely. It is absent here". "It" means polyuria; "Polyuria is absent here" is clearer.
- neuro_2 op28: "HGPRT deficiency (hypoxanthine-guanine phosphoribosyltransferase deficiency)" repeats "deficiency".
- neuro_2 op31 and obgyn_2 op3: "When a stem gives both" / "the stem" are mild residual stem wording in `.rule` blocks.
- neuro_3 op28: "Hypoglycemia: the sharpest trap in the set" is trap-autopsy wording in `.danger`. It is acceptable as a one-line trap statement.

## Pre-existing (not drift; the rewrite kept the content unchanged)

| # | file/op | brief | issue | correct wording |
|---|---|---|---|---|
| P1 | neuro_1 op16, op23 | sellar-mass | The prose (.dp, Defining criteria, Pertinents, Decoy note) describes growth arrest at 11, Tanner 1 at 13, a one-year duration, height 50th→5th and weight 75th. The source vignette is "12 yo F, 6 months of morning headaches, height 75th→10th, weight 60th". | Align the prose with the vignette: "Tanner 1 at 12", "six months of headaches", "height 75th → 10th with weight at the 60th". Or confirm that the prose describes a different source question and label it so. |
| P2 | neuro_1 op25 | sellar-mass | Pairs with says the twin covers "a 13-year-old girl with worsening headaches". The twin's vignette is a 10 yo M; this brief's vignette is a 12 yo F. | "Headache in a Child: What Earns Imaging covers the same complaint, a child with worsening headaches, with the red-flag gate answered in opposite directions." |
| P3 | neuro_1 op29, op39, op41–43 | peds-headache-imaging | The .dp describes an adolescent girl with 2 years of unilateral headaches and menarche at 12, and the Distractors use "She"/"she". The source vignette is a 10 yo M with 1 year of bilateral headaches relieved by sleep. Pairs with says "same age and sex". | Drop "at the same age and sex". Align the .dp and Distractors with the vignette, or label them as a different source question. |
| P4 | neuro_3 op25, op26 | bs-reye | The vignette box says "Q — the most likely diagnosis; options spanned Reye syndrome, acute viral hepatitis and bacterial meningitis". The subtitle, .dp and Option audit describe a question asking for the cause of the edema, with 5 metabolic options. | Align the vignette box with the question the prose teaches, or the reverse. |
| P5 | neuro_4 op4 | bs-posterior-fossa | "Every abnormal finding is on the left and every one is cerebellar": the left facial numbness (trigeminal) and the papilledema are abnormal and not cerebellar. | "Every cerebellar finding is on the left: dysmetria reaching with the left hand, …" |
| P6 | neuro_1 op8 | redeye | .rule: "Topical steroids are indicated in uveitis and scleritis". Scleritis needs systemic therapy (oral NSAIDs, then systemic steroids); topical steroids are not adequate. | "Steroids are indicated in anterior uveitis (topical) and scleritis (systemic)." |
| P7 | obgyn_1 op26 | hpv | The pearl says "In every vaccine series, do not restart and do not repeat". This contradicts the bank item "Repeat the second dose → doses less than 5 months apart do not count" and the .dp's "Minimum intervals matter". | "Never restart a delayed series; resume where you left off. Repeat only a dose given before the minimum interval." |
| P8 | obgyn_1 op7 | cervical | "ACS 2020 … This removes cytology-alone screening at ages 25–29 entirely." ACS 2020 prefers primary HPV testing but still accepts cotesting every 5 years or cytology alone every 3 years where primary HPV testing is unavailable. | "ACS 2020 prefers primary HPV testing from age 25; cytology alone every 3 years remains acceptable where primary HPV testing is unavailable." |
| P9 | obgyn_3 op1 | bs-cervical-gate | "Early screening finds transient infection and leads to excisional procedures… Cervical cancer under 21 is therefore rare." The "therefore" follows the screening-harm sentence, but the rarity comes from clearance and slow progression. OLD had the same order ("That's why"). | Move it: "HPV infection in adolescents clears in ~90% within 2 years, and progression takes more than a decade, so cervical cancer under 21 is rare." |
| P10 | obgyn_3 op3 | bs-cervical-gate | "HIV infection → … This is the one exception that starts screening before age 21", and the next row reads "other immunocompromise → same accelerated schedule". The "one exception" wording conflicts with that row. | "HIV infection (and other immunocompromise, same schedule) → …; these are the only exceptions that start screening before age 21." Verify the non-HIV immunocompromise start age against ACOG/ASCCP before editing. |
