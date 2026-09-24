# s31 sort, part 3 (Q15 to Q21)

Sort per nbme-intake section 4. Paraphrase only; the local source file holds the vendor text. A match means the same key and the same deciding finding, confirmed by reading the candidate items (pagelib) and grepping the page.

| Q | nbme_id | sort | brief | carrier item |
|---|---|---|---|---|
| 15 | peds-cms-060d9c | covered | bs-umbilical (topic owner congenital-hypothyroid) | q_7e472e5bd7e09a357f4d |
| 16 | peds-cms-2944bc | covered | redeye | q_bfc2adf60a295d1a841a |
| 17 | peds-cms-dd721b | new angle | bs-fat-soluble-vitamins | anchor q_d260ba614f8b376b52b7 (keys vitamin K, not FFP) |
| 18 | peds-cms-6facf4 | covered | neonatal-rash | q_ee07b7cec8875310382c |
| 19 | peds-cms-9a2ab1 | new | proposed bs-peds-bp, system cv, data-bp="cv" | none |
| 20 | peds-cms-dbb94d | covered | bs-leukemia | q_d5a219c1127f50cba341 |
| 21 | peds-cms-9b4c4f | covered | lymphadenitis | q_bbe63e88a23044cd7f3a |

## Q15 Congenital hypothyroidism: which test first (peds-cms-060d9c)

- Sort: covered.
- Carrier: bs-umbilical q_7e472e5bd7e09a357f4d (infant born without a newborn screen, reducible umbilical hernia, persistent jaundice, hypotonia and a large tongue; key serum TSH and free T4). Same key (thyroid function tests) and same deciding finding (umbilical hernia plus prolonged jaundice in a sleepy feeder with no screen on record).
- Why not congenital-hypothyroid: every item there hands over the TSH and T4 and asks for the cause, the treatment or imaging; its q_3e20457c599a58018c77 keys ultrasound or uptake scan, which is the step after TSH/T4, not this one. The brief's workup table does list serum TSH and free T4 as the confirming test.
- How NBME framed it: the stem gives no labs and a softer picture than the page item (no macroglossia or wide fontanelle; "good baby" who must be woken to feed, cool extremities, normal growth) and hides the missed screen behind "initial examination" at 2 months; the decoys are wrong-organ tests (karyotype, sweat chloride, head CT, liver CT) rather than thyroid imaging.
- Conflict: none with the page. The NBME explanation lists congenital adrenal hyperplasia as a karyotype diagnosis; that line is inaccurate and should not be carried onto the page.

## Q16 Neonatal gonococcal conjunctivitis (peds-cms-2944bc)

- Sort: covered.
- Carrier: redeye q_bfc2adf60a295d1a841a (purulent conjunctivitis on day 3 of life, key gonococcal conjunctivitis, parenteral ceftriaxone). The redeye timing line (day 0 to 1 chemical, day 2 to 5 gonococcal, day 5 to 14 chlamydial) teaches the deciding finding.
- How NBME framed it: a home birth delivered by the father stands in for "no ocular prophylaxis"; the tell is day 2 with hyperpurulent discharge and lid swelling so marked the conjunctiva cannot be seen; Kawasaki appears under its long name ("mucocutaneous lymph node syndrome") as a name-swap decoy.
- Conflict: none on the key. Minor page fact: redeye names oral erythromycin for neonatal chlamydial conjunctivitis, while the NBME explanation calls azithromycin the preferred agent; current Red Book guidance accepts either, so no fix is forced, but a later redeye pass could name both.

## Q17 Vitamin K deficiency bleeding: what to add to vitamin K (peds-cms-dd721b)

- Sort: new angle.
- Owning brief: bs-fat-soluble-vitamins. Its q_d260ba614f8b376b52b7 keys parenteral vitamin K and mentions FFP only in the companion; its management line says FFP as well for serious bleeding. No item keys FFP or tests the blood-product choice, and no page item uses cryoprecipitate, factor VIII or platelets as distractors for this disease.
- What must be taught:
  - Deciding finding: a newborn with vitamin K deficiency bleeding that is serious (intracranial, GI, multisite) needs clotting factors now, because vitamin K takes time to restore factor synthesis; key: fresh frozen plasma alongside vitamin K (NBME explanation; page management line).
  - Why FFP: vitamin K deficiency lowers factors II, VII, IX and X plus proteins C and S, and FFP carries all of them (NBME explanation; the page already names II, VII, IX, X).
  - Traplines: cryoprecipitate (fibrinogen, VIII, XIII, vWF; none of the vitamin K factors), factor VIII concentrate (hemophilia A or vWD), platelets (platelets stay normal in vitamin K deficiency, which the page already states), lactated Ringer (restores volume, not factors).
- How NBME framed it: the lead-in grants vitamin K up front ("in addition to") so the question is purely which blood product; the options are products named by content, and the bait is the product that sounds most like "clotting factor".
- Conflict: none with the page.

## Q18 Erythema toxicum neonatorum: management (peds-cms-6facf4)

- Sort: covered.
- Carrier: neonatal-rash q_ee07b7cec8875310382c (2-day-old, well, pustules on erythematous bases, palms and soles spared; key reassurance only). Same key and same deciding finding (well term newborn, day 2, small lesions on a red base, mostly truncal). q_1a0084c4964253578d96 carries the same pattern as a diagnosis item.
- How NBME framed it: the key is a full sentence of counselling ("reassure the parents it will clear in a few days"); the distractors are each a workup or treatment that would suit a different rash (culture plus antistaphylococcal therapy for impetigo, HSV culture, KOH for candida, topical steroid); the lesions are called small yellow papules rather than pustules.
- Conflict: none. The page says it resolves in about a week and NBME says a few days; both describe a self-limited rash and neither changes the key.

## Q19 Adolescent blood pressure: confirm an oscillometric reading (peds-cms-9a2ab1)

- Sort: new.
- No brief owns it: grep finds no oscillometric, auscultation, ambulatory monitoring or pediatric BP-percentile content; htn-drugs covers adult confirmation and drug choice, secondary-htn covers causes.
- Proposed brief: bs-peds-bp, "Elevated Blood Pressure in a Child or Adolescent", system cv, data-bp="cv", shelf peds (fm).
- What must be taught:
  - Deciding finding: a high BP obtained only by an automated oscillometric device, even when repeated on the same device; key: repeat the measurement by auscultation (the averaged auscultatory readings set the stage), because oscillometric devices tend to overestimate (NBME explanation).
  - The order: auscultatory confirmation in the office comes before ambulatory monitoring, echocardiography or drug therapy; first treatment is lifestyle change aimed at obesity (NBME explanation).
  - Traplines: 24-hour ambulatory monitoring (accurate, but comes after an auscultatory office reading); echocardiography (for end-organ assessment when drug therapy is starting, not to make the diagnosis); oscillometric repeats daily for 3 days or in 2 weeks (the same device repeats the same overestimate).
- How NBME framed it: the options differ only in technique and timing of the same measurement; the second device reading is placed in the stem to make "repeat it" look already done, so the answer is the method, not the interval.
- Conflict: none with the page (no page facts). Flag for authoring: the NBME explanation defines adolescent hypertension by the 95th percentile, and its objective says auscultate when the device reading is above the 90th; for age 13 and older current AAP (2017) thresholds are absolute (130/80 for stage 1), so the new brief should state current thresholds after evidence-verification and keep NBME only for the key and framing.

## Q20 ALL mislabelled as systemic JIA: bone marrow aspiration (peds-cms-dbb94d)

- Sort: covered.
- Carrier: bs-leukemia q_d5a219c1127f50cba341 (child carrying a presumed systemic JIA label with fever, limp and pancytopenia; key obtain bone marrow before any corticosteroid). Same key (bone marrow) and same deciding finding (counts going down in a child labelled systemic JIA). The brief's table also teaches that systemic JIA drives counts up while ALL drives them down, and q_9936babf787657dd88a3 keys marrow aspirate and biopsy once the CBC shows pancytopenia.
- How NBME framed it: the prior systemic JIA diagnosis and partial NSAID response are the anchor; the decoys are imaging (abdominal CT, bone scan, gallium scan) and liver biopsy, so the transaminases and hepatosplenomegaly invite an organ-directed test while the tri-lineage drop points to the marrow.
- Conflict: not with the key, but a page tension to note. The sjia brief teaches macrophage activation syndrome as a systemic JIA patient with cytopenias, liver dysfunction and a falling ESR, and calls the low ESR its pathognomonic tell; this stem carries that same pattern (ESR 12, cytopenias, high AST and ALT) and NBME reads it as ALL. The marrow key holds either way, and the page already says marrow before steroids, but a "How NBME framed it" line should say that in a child labelled systemic JIA, new cytopenias go to the marrow before the MAS label or any steroid.

## Q21 Infected thyroglossal duct cyst (peds-cms-9b4c4f)

- Sort: covered.
- Carrier: lymphadenitis q_bbe63e88a23044cd7f3a (tender midline neck cyst after a cold that rises with tongue protrusion; key thyroglossal duct cyst). Same deciding finding (midline tenderness that worsens with tongue protrusion or swallowing) and same key (NBME adds "infected"). The brief's congenital neck mass line gives the same localisation rule.
- How NBME framed it: a cat-scratch exposure is planted as bait next to a real cat-scratch option, alongside mononucleosis, tonsillitis and viral syndrome; the key is worded as a cause ("most likely cause of these findings"). The page's cat-scratch row (a tender regional node proximal to the scratch, building over weeks) already kills the bait: this is acute, midline and not a node.
- Conflict: none.
