# s33 voice review: MSK (10_voice_msk_1..6)

This is an independent drift review. Base: `scratch/s33_base.html`. Each file was applied to the base on its own. Op index = 0-based position in the file's `edits` array. The verifier's "edit N" is this index + 1.

## Verification

Each file was run as `tools/verify_edits.py <file> scratch/s33_base.html --voice`, with the render step included:

| file | ops | result |
|---|---|---|
| msk_1 | 11 | PASS (gate PASS, render PASS, 1 voice warning) |
| msk_2 | 17 | PASS (5 warnings: long sentences, SI/IBD/HLA not expanded) |
| msk_3 | 18 | PASS (2 warnings: 32-word limp step 3, ACR expansion placement) |
| msk_4 | 26 | PASS (10 warnings: long sentences, NSAIDs/JIA first-use expansions) |
| msk_5 | 25 | PASS. Gate notes 2 stale allowlist lines, `pairs-with bs-lbp-acute:no` and `bs-septic-adult:tier_1_has_no_fork_in_adults`, left behind by the declared bold rewordings. Housekeeping only. |
| msk_6 | 14 | PASS |

The first runs timed out in render.js, which has a hard 90 s jsdom limit, while the machine was under load (load average about 30). The `--no-render` runs and a later sequential run with render included all passed.

## Summary

- CRITICAL: 0
- MINOR: 14

I found no dropped or strengthened numbers, cutoffs, ages, timing, drugs, tests or sequences, and no added clinical claims beyond acronym expansions. All acronym expansions are correct in context. That includes CPPD = calcium pyrophosphate dihydrate, RANKL, HLA-B27, PMN, CTA and LFCN.

## Flagged-uncertain items: verdicts

| file/op | brief | item | verdict |
|---|---|---|---|
| msk_3 op11 | synovitis | subtitle "Benign mimic of septic arthritis of the hip" | OK. Same meaning as "benign version of the same stem"; no new claim. |
| msk_3 op12 | synovitis | "Its laterality does [discriminate]" | OK. Same strength as OLD "Its laterality is not [a decoy]". The unilateral vs. unilateral-or-bilateral detail is kept. The claim carried_by "Kocher 0–1 of 4." sits in the unchanged bold just before the find and exists. |
| msk_1 op3 | biceps | "The shoulder tolerates immobilization uniquely poorly" | OK. Same meaning as "uniquely punished for immobilization"; "within weeks" is kept. |
| msk_4 op9 | scfe | subtitle "Patients who do not fit the stereotype" | MINOR (M5). No drift, but "the stereotype" is undefined in the subtitle. |
| msk_4 op16 | myositis-ossificans | "each absence helps exclude a competing diagnosis" | OK. Same as "each omission is doing eliminating work". See M9 for a wording point in the same sentence. |
| msk_4 op8 | nursemaid | pearls: `<b>Supracondylar…</b> —` changed to a colon | OK. columnize() makes a grid only when at least 60% of the "·" rows are term-led. Here 1 of 2 rows is, so this was a prose dash and the colon is correct. |
| msk_5 op2 | bone-tumors | GCT "behaves aggressively" (was "behaves badly") | OK. The same brief's .dp already says "Aggressive cortical destruction belongs to … giant cell tumor". Optional: "is locally aggressive". |
| msk_6 op3 | bs-torticollis | dropped "the stem's explicit note that the hips are stable…" | MINOR (M3). A stem finding was dropped along with the meta. |

## Findings

| # | file | op | brief | class | quote (NEW) | correct wording |
|---|---|---|---|---|---|---|
| M1 | msk_2 | 6 | hippos | MINOR: ambiguity near drift (subtitle) | "Hip fracture versus posterior dislocation: leg positions often reversed" | OLD meant that learners mix the positions up ("free points, frequently reversed"). NEW can be read as a clinical claim that the positions themselves are often reversed in patients. Use: "Hip fracture versus posterior dislocation: leg positions are often confused". |
| M2 | msk_5 | 21 | bs-synovitis-mgmt | MINOR: hedge lost | dropped `<span class="ex">Kocher is clinic-ledger — not stated in the bank explanation…</span>` | Per RULES, provenance tags are deleted but the fact is kept. This note is also a hedge: Kocher reasoning comes from clinical practice, not from the source explanation. Keep it in plain form: "Kocher scoring comes from clinical practice; the source explanation does not state it." Or confirm that dropping it is intended. |
| M3 | msk_6 | 3 | bs-torticollis | MINOR: stem fact dropped; claim map mislabels it "not a clinical claim" | "…When you find one, examine for the rest." | Add: "In this infant the hips are stable." |
| M4 | msk_5 | 4, 5, 10, 12, 13, 14, 15, 19, 20 | bone-tumors, scheuermann, bs-septic-adult, bs-lbp-acute, bs-synovitis-mgmt | MINOR: claim map not honest | new_claims repeat OLD wording that is not in NEW, e.g. "When the options are natural courses…", "The comorbidities point the opposite way from how they read.", "The stem spends its sentences deleting red flags.", "A wall of negatives is permission to do less.", "supports the keyed next step" | The page text is fine. Rewrite new_claims to quote NEW, e.g. "To predict a bone lesion's natural course, name the lesion first…", "Obesity, hypertension and diabetes may suggest a metabolic cause such as gout…", "no red flags in the history". |
| M5 | msk_4 | 9 | scfe | MINOR: vague subtitle | "Patients who do not fit the stereotype" | "Not only the obese teenager" or "SCFE outside the obese-teenager stereotype". |
| M6 | msk_5 | 12 | bs-septic-adult | MINOR: residual jargon/meta | "In adults, tier 1 has no fork… Only in children does tier 1 differ" | "In adults, every acute hot joint is aspirated. Only in children does the first step depend on toxicity and inflammatory signs, not on the presence of fluid." |
| M7 | msk_3 | 8 | septic-bursitis | MINOR: residual figurative | "Post-injection steroid flare: the benign twin of iatrogenic infection." | "Post-injection steroid flare: a benign mimic of iatrogenic infection. Timing separates them, not severity." |
| M8 | msk_4 | 22 | growing-pains | MINOR: residual meta | "the one benign-looking mimic on the list" | "the one benign-looking mimic" (or "in the differential"). |
| M9 | msk_4 | 16 | myositis-ossificans | MINOR: wording | "The history includes no fever, erythema, night pain or weight loss" | Erythema is an exam finding. Use "There is no fever, erythema, night pain or weight loss, and each absence helps exclude a competing diagnosis." |
| M10 | msk_4 | 7 | nursemaid | MINOR: residual meta (inherent to the brief) plus a 29-word sentence | "In the newer 'Patient Information' format… The exam line '…' describes the reduction and confirms that it worked." | Acceptable if the brief is about the format. Otherwise split: "The exam describes the reduction: … 15 minutes later. Reaching for toys confirms it worked." |
| M11 | msk_2 | 10 | gtps | MINOR: readability; SI not expanded | "(<b>OA</b> (osteoarthritis), <b>AVN</b> (avascular necrosis), fracture, labral tear)" | Avoid nested parentheses: "groin → the joint itself: osteoarthritis (OA), avascular necrosis (AVN), fracture, labral tear". Expand "SI (sacroiliac) joint". |
| M12 | msk_2 | 1 | scaphoid | MINOR: redundancy | "…leads to <b>avascular necrosis</b> and nonunion. <b>AVN</b> (avascular necrosis) risk…" | "…leads to <b>avascular necrosis</b> (AVN) and nonunion. AVN risk is highest…" |
| M13 | msk_3 | 1 | oa-pharm | MINOR: expansion format | "The ACR/Arthritis Foundation 2019 guideline (ACR, American College of Rheumatology)" | "The 2019 American College of Rheumatology (ACR)/Arthritis Foundation guideline", or keep the bold and write "(ACR: American College of Rheumatology)". |
| M14 | msk_5 | 17 | bs-lbp-acute | MINOR: style | Sentence opens with "~90% of acute low back pain…" | "About 90% of acute low back pain and about 90% of sciatica resolve within 6 weeks." |

Below the finding threshold (noted, no change needed):
- Long-sentence warnings in msk_1 op5, msk_2 op11/12 (the count includes the label), msk_3 op15 (numbered age list) and msk_4 op10/17. These are acceptable.
- msk_1 op0: "<b>ESR ≥50</b> (erythrocyte sedimentation rate)" puts the expansion after the number. It reads acceptably.

## Blocks checked with no issue

- msk_1: pmr .dp/.pearls, biceps .dp, cts .dp/.pearls, dequervain .dp/.rule/.pearls, meralgia .dp/.pearls.
- msk_2: scaphoid .dp/.rule, backpain .dp/.pearls/.rule, hippos .dp/.danger, gtps sub/.pearls/.rule, inflam-back .dp/.danger/.pearls/.rule.
- msk_3: oa-pharm .dp/.pearls/.rule, septic-bursitis .dp/.pearls/Pairs/.rule, septic-hip .dp/.danger, synovitis .rule (the relabel to "Transferable rule" is declared), limp sub/spine/.danger/Pairs.
- msk_4: sjia all ops, scfe .dp/.danger/Pairs/.rule, myositis-ossificans .dp/.danger/Pearls/Pairs/.rule, growing-pains .dp/row/Pearls/Pairs/.rule.
- msk_5: bone-tumors .dp/.danger/.pearls/Pairs/.rule (text), scheuermann all ops (text), bs-septic-adult .dp (the carried_by quote exists in op13 NEW)/crystals/.rule, bs-lbp-acute sub/.dp/distractors/Pairs/.rule (text), bs-synovitis-mgmt .dp/exit ramps/mnemonic/Pairs.
- msk_6: all ops except op3.
