# s31 sort, batch 1 (Q1 to Q7)

Sort per nbme-intake section 4, confirmed by reading each candidate brief (tools/pagelib.py, one brief at a time) and grepping the page for the key and the deciding finding. Paraphrase only; the source text stays in repair/sources/s31_questions.md.

| Q | nbme_id | sort | brief | item carrying the decision |
|---|---|---|---|---|
| 1 | peds-cms-fdc19e | covered (repeat of s28 item) | cgd | q_bd617d53d7c3c8f78cff (already data-nbme="peds-cms-fdc19e") |
| 2 | peds-cms-aa91d7 | covered (repeat of s28 item) | rmsf | q_f301e03be41b7aa167b0 (already data-nbme="peds-cms-aa91d7") |
| 3 | peds-cms-56f5bb | new angle | growth | none |
| 4 | peds-cms-bd082e | new angle | cyanotic-chd | none (nearest q_abf5415254ced3a48d5d) |
| 5 | peds-cms-e43eb8 | new angle | neonatal-jaundice | none |
| 6 | peds-cms-f52102 | new | proposed bs-osteo-organism (msk; data-bp="msk") | none |
| 7 | peds-cms-03615c | new angle | bs-torch | none (nearest q_7ac28509022d51f89357) |

---

## Q1 Cyclic neutropenia (peds-cms-fdc19e)

- Sort: covered. Owning brief: cgd. Item: q_bd617d53d7c3c8f78cff, which is this same NBME item written in during s28 and already carries data-nbme="peds-cms-fdc19e".
- Same key and same deciding finding: episodes about every 3 weeks lasting 3 to 5 days, well between them, isolated severe neutropenia (Hb and platelets preserved). The brief also has the confirm item (serial counts, q_0ba63d5246cebb009bff), the G-CSF item, the severe congenital neutropenia look-alike (q_c886f6f10705f542d3de), and a trapline for viral illness and for Fanconi syndrome.
- NBME framing lesson: the name-swap decoy (the renal tubule disorder offered where the marrow-failure disease of the same eponym belongs) inside a long list of neutropenias and marrow failures. Already on the page as a "Name trap" line and a true-fact-wrong-slot trapline, so no new framing line is needed.
- Same fingerprint as s28 (fdc19ea8c1), same nbme_id. Do not add a second data-nbme or a duplicate question. Whether s31 gets its own coverage/misses row is a lead decision: the gate fails a repeated fingerprint without same_as, so any second row must carry same_as.
- Conflict: none.

## Q2 Rocky Mountain spotted fever (peds-cms-aa91d7)

- Sort: covered. Owning brief: rmsf. Item: q_f301e03be41b7aa167b0, the s28 write-in of this same item, already data-nbme="peds-cms-aa91d7".
- Same key and deciding finding: early-summer rural child with days of fever and severe headache, then a petechial rash starting on the hands and palms. The brief's traplines already cover the mosquito bait (dengue needs tropical travel) and Kawasaki (fever only 4 days, rash petechial, not polymorphous).
- NBME framing lesson: no tick is ever mentioned (season, rural life and mosquito bites stand in), and Kawasaki disease is offered under its formal mucocutaneous-lymph-node-syndrome name. The formal name is not on the page (grep finds none), so a one-line "How NBME framed it" note naming it is the only possible add.
- Same fingerprint and nbme_id as s28; same duplicate-row caution as Q1.
- Conflict: none.

## Q3 Developmental assessment at 4 years (peds-cms-56f5bb)

- Sort: new angle. Owning brief: growth (it owns sorting a child's development domain by domain: q_869cbf41b8a95f1fb36c classifies an 18-month-old as isolated gross motor delay). The page has no preschool (3 to 4 year) milestone set and never defines global developmental delay; grep finds no copying-a-square, hopping-on-one-foot or stick-figure content. Topic match only: the 18-month set cannot decide this item.
- What must be taught:
  - The 4-year set, by domain, from the NBME explanation: gross motor, hops on one foot (and throws overhand); fine motor, copies a square and draws a simple stick figure; language, speaks in sentences that strangers understand and tells stories; social, plays cooperatively.
  - Reading the stem domain by domain: can jump but cannot stand on one foot = gross motor delayed; imitates a line but cannot copy a circle = fine motor delayed; word combinations with only half the speech understood = language delayed. Key: delayed in all three.
  - Global developmental delay = significant delay in two or more domains; such a child is evaluated for a cause and referred for early intervention services (speech, physical and occupational therapy).
  - Traplines: the all-normal row (the child does jump and combine words, which are younger milestones, so a skill he has is not the skill his age requires) and the rows that spare fine motor (imitating a line is not copying a shape).
- NBME framing lesson: the options are an 8-row grid of normal/delayed combinations across three domains, and the stem gives each domain as a pair of a skill present and a skill missing, so the answer comes from checking the missing skill against the age, one column at a time.
- Conflict: none. Side note: the page's line that the early-intervention referral is "the pathway under age 3" is not contradicted, since this item does not ask for the next step.

## Q4 Tetralogy of Fallot (peds-cms-bd082e)

- Sort: new angle. Owning brief: cyanotic-chd. Nearest item q_abf5415254ced3a48d5d (TOF from crying cyanosis relieved knee-to-chest, with a LUSB murmur; distractors truncus arteriosus and tricuspid atresia). Same key, but a different deciding finding and a different look-alike set: here the spell is witnessed with an oximetry drop and the murmur fading, and the distractors are the acyanotic lesions. The only page statement that the TOF murmur softens during a spell is a table cell in bs-shunt-timing, which also has a look-alike item (q_b9082f8a5ce55be4b990: a large VSD whose murmur has softened and who desaturates with crying = Eisenmenger physiology).
- What must be taught:
  - Deciding finding: an infant whose saturation falls sharply when agitated while the harsh systolic ejection murmur becomes nearly inaudible is having a tet spell. The murmur is made by flow through the narrowed outflow tract, so when the obstruction tightens and pulmonary flow drops, the murmur softens (NBME explanation; page cyanotic-chd, murmur from the RVOT not the VSD). Key: tetralogy of Fallot.
  - Camouflage: the visit is framed as a febrile GI illness with dehydration, and there is baseline cyanosis (saturation in the mid-80s); the spell during the IV attempt is the decider.
  - Traplines: VSD (holosystolic murmur, no cyanosis; the page's softening-VSD item is Eisenmenger physiology developing over months, not an acute spell with crying); isolated pulmonary stenosis (outflow murmur without the right-to-left shunt, so no spells); ASD (fixed split S2, left-to-right, no cyanosis); coarctation (arm hypertension with weak leg pulses and lower leg pressures, no cyanosis).
- NBME framing lesson: a plain list of five named lesions where four do not cause cyanosis; the answer sits in the spell's time course (desaturation plus a fading murmur), not in the option wording.
- Conflict: none on the key. The NBME explanation text calls the TOF murmur holosystolic at the left lower sternal border, while its own stem says harsh systolic ejection murmur and the page says systolic ejection murmur at the left upper sternal border from the outflow tract. Keep the page wording; do not import the explanation's holosystolic/LLSB description.

## Q5 G6PD deficiency in a jaundiced newborn (peds-cms-e43eb8)

- Sort: new angle. Owning brief: neonatal-jaundice. It has a G6PD row in its differential (indirect with anemia and high reticulocytes, often an oxidant trigger) and a workup row (Coombs-negative hemolysis points to G6PD or spherocytosis), but no item carries the decision. G6PD items in bs-spherocytosis and drug-hemolysis are older children with bite cells and Heinz bodies, not a newborn.
- What must be taught:
  - Deciding finding: a term newborn of Mediterranean descent, day 5, total bilirubin 20 with a direct fraction under 1, hematocrit 33% (anemia), negative direct and indirect Coombs, same blood group as the mother (no ABO or Rh setup), and sulfonamide exposure in late pregnancy. Coombs-negative hemolysis plus an oxidant exposure plus ancestry = G6PD deficiency.
  - Key worded as the class, "enzyme deficiency": G6PD makes NADPH, which keeps glutathione reduced; without it, sulfa-type oxidants cause hemolysis (NBME explanation).
  - Traplines: physiologic jaundice (the level of 20 exceeds the physiologic peak and anemia makes it pathologic; the page already teaches physiologic jaundice as immature conjugation); dehydration (the page's own enterohepatic mechanism item, but five stools a day and frequent feeds argue against it and it does not cause anemia); sepsis (can raise indirect bilirubin, but the infant is well); milk protein allergy (GI or allergic symptoms, not hemolysis).
  - Look-alike on the page: neonatal-jaundice teaches sulfonamides as dangerous in jaundiced newborns because they displace bilirubin from albumin (q_e3d808bf1661371049fc). Here the sulfa is the oxidant trigger for hemolysis; the new item or trapline should make the two roles explicit.
- NBME framing lesson: the key is class-level ("enzyme deficiency"); the enzyme is never named, and the stem hides it behind ancestry, a maternal drug history and a negative Coombs.
- Conflict: none.

## Q6 Osteomyelitis after a puncture wound through a shoe (peds-cms-f52102)

- Sort: new. No brief owns the organism decision for osteomyelitis. The osteomyelitis items on the page (bone-tumors, bs-synovitis-mgmt, limp, footulcer) all key the diagnosis or imaging; septic-hip lists joint organisms by host (S. aureus overall, Kingella, gonococcus, Salmonella in sickle cell) and sickle-trait says Salmonella for bone; nothing on the page mentions a puncture wound through a shoe or Aeromonas. Pseudomonas is keyed only for catheter pyelonephritis (bs-pyelo-organism).
- Proposed brief: bs-osteo-organism, "Osteomyelitis: Naming the Organism", system musculoskeletal, data-bp="msk". Pairs with septic-hip (host-based organism list) and bs-pyelo-organism (same organism, different site).
- What must be taught:
  - Deciding finding: a foot that stays painful, warm, red and tender weeks after a nail went through the shoe = osteomyelitis from direct inoculation. Key: Pseudomonas aeruginosa, the classic organism after a puncture through an athletic shoe (NBME explanation).
  - Work-up and treatment, per NBME: MRI is more sensitive than x-ray; surgical debridement with cultures to name the organism, and empiric antibiotics.
  - Traplines: S. aureus (the most common cause of osteomyelitis overall, and the page's default, but the puncture-through-a-shoe exposure changes the organism); Aeromonas (wound infection after fresh-water exposure, which the stem does not give); group A strep (skin and throat, not puncture osteomyelitis); Klebsiella (pneumonia in aspiration-prone adults).
  - Low fever and a tetanus booster at 5 are decoys; tetanus status does not name the organism.
- NBME framing lesson: an organism list with one water-borne look-alike and the usual most-common organism; the key rests entirely on the exposure (nail through the shoe), and the word "osteomyelitis" never appears in the stem.
- Conflict: none with the page. Do not carry the explanation's description of Aeromonas as anaerobic into the page; the trapline needs only its fresh-water exposure.

## Q7 Neonatal herpes simplex encephalitis (peds-cms-03615c)

- Sort: new angle. Owning brief: bs-torch, which has the neonatal HSV row (days 5 to 21, vesicles, seizures, temporal lobe) and q_7ac28509022d51f89357 (day-10 neonate with vesicles, seizures and temporal-lobe changes, distractors CMV and bacterial meningitis). Same key, different deciding finding: the NBME stem gives no vesicles and decides on the CSF. febrile-seizure teaches the CSF pattern (lymphocytes with red cells, q_16fe3ec314b65593b554) but in a 2-year-old. The intake table's candidates (neonatal-rash, febrile-seizure) are weaker owners; neonatal-rash keys HSV on the skin lesions.
- What must be taught:
  - Deciding finding: an 8-day-old with apnea, focal seizures, lethargy and upper motor neuron signs, and CSF with normal glucose, mildly raised protein, a modest pleocytosis (70) that is mostly lymphocytes, and many red cells. No skin lesions are given. Key: herpes simplex virus; confirm with CSF PCR, treat with IV acyclovir.
  - Traplines: E. coli and group B strep (the common neonatal meningitis bacteria, but the CSF would show low glucose and a much higher, neutrophil-predominant count, often over 1,000); CMV and Toxoplasma (congenital infections present from birth with calcifications, hearing loss or chorioretinitis, not an acute encephalitis in the second week).
  - The stem says antibiotics were started; the lesson is that acyclovir must be added (the febrile-seizure item's companion already says to add acyclovir to empiric therapy).
- NBME framing lesson: an organism list mixing a virus, two bacteria and a parasite, with no vesicles in the stem; the day of life and the CSF pattern (lymphocytes with red cells, normal glucose) do the work, and "antibiotics begun" pulls toward a bacterial answer.
- Conflict: none.
