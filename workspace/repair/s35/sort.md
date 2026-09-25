# s35 sort (Q1 to Q12)

Sort per nbme-intake section 4, confirmed by reading each candidate brief (tools/pagelib.py, one brief at a time) and searching the page for the key and the deciding finding. Paraphrase only; the source text stays in repair/sources/s35_questions.md (local-only). Option labels are quoted only to record NBME phrasing.

Batch facts: the paste holds 12 questions, not 13 (12 answer keys, 12 option runs, 12 explanations). 9 incorrect, 3 correct (Q2, Q5, Q7). No fingerprint or nbme_id is already in repair/nbme/coverage.csv or on the page, and no stem matches an older source file (s08 to s34), so there is no same_as. Form name not given; ids are peds-cms-<first 6 of fingerprint>, fingerprint as in s34 (sha1 of key lowercased + "|" + first 12 tokens of the stem).

| Q | nbme_id | fingerprint | key | task | result | time | sort | brief (data-bp) | item carrying the decision |
|---|---|---|---|---|---|---|---|---|---|
| 1 | peds-cms-d90531 | d90531cd5a | Adrenal adenoma | dx | incorrect | 0:29 | new angle | precocious-puberty (endo) | none; nearest q_da0183afd85955af9b62, q_aa34051b68ae504b9bbd |
| 2 | peds-cms-723033 | 7230339994 | Posterior urethral valve | dx | correct | 1:25 | new angle | bs-puv (renal newborn) | none; nearest q_0dc9b7ebaebf5161897a, q_673f589cff4d5d1580c5 |
| 3 | peds-cms-ce7f06 | ce7f06970e | Rotavirus | prevention (which vaccine now) | incorrect | 1:53 | new angle | bs-adolescent-vax (gen) | none; nearest q_b6cf4fa2dd07599eb91a |
| 4 | peds-cms-0354fa | 0354fa6e7d | Renal tubular acidosis | dx (cause of a lab) | incorrect | 2:52 | new | proposed bs-distal-rta (renal) | none; bs-ftt q_c58ffe3da98457e3843f only orders the test |
| 5 | peds-cms-c4694e | c4694e76b7 | Pulmonary stenosis | dx | correct | 1:28 | covered | ped-murmur (cv) | q_fb94648142ed51749518 |
| 6 | peds-cms-3d1862 | 3d1862ca4b | Internal fixation | mgmt | incorrect | 0:35 | new angle | scfe (msk) | none (treatment is in prose only) |
| 7 | peds-cms-0efcba | 0efcba16c3 | Pneumonia due to Mycoplasma pneumoniae | dx | correct | 0:52 | new angle (carrier item) | mycoplasma (resp) | none; decision point prose matches |
| 8 | peds-cms-6821fe | 6821fe82bf | Polycystic kidney disease | dx | incorrect | 0:27 | new angle | bs-abdominal-mass (renal multi) | none; nearest bs-puv q_0db3b05afa39584a8a69 |
| 9 | peds-cms-7a44ef | 7a44ef1140 | Warm compresses | mgmt | incorrect | 0:41 | new | proposed bs-eyelid-lump (neuro) | none (no hordeolum content on the page) |
| 10 | peds-cms-44f3d3 | 44f3d30e35 | α1-Antitrypsin deficiency | dx | incorrect | 0:17 | new angle | asthma-copd (resp) | none; nearest q_fc488cc379ca5efd9dac (adult, test task) |
| 11 | peds-cms-252cd2 | 252cd2ab65 | Impaired leukocyte microbicidal activity | mechanism | incorrect | 0:46 | covered | cgd (immune) | q_1f7b49f7314459b8b98f |
| 12 | peds-cms-9fb189 | 9fb189ce6c | Measles-mumps-rubella | prevention (which vaccine would have prevented) | incorrect | 0:10 | new angle | bs-exanthems (multi skin) | none; nearest q_1116e1bfe041c2c88774 (measles dx) |

Conflicts: none on any key. Two keys rest on weak stems (Q10, Q12) and three explanations describe a different entity from the stem (Q5, Q8, Q12); see each question and the list at the end.

---

## Q1 Virilized 10-year-old girl, adrenal source (peds-cms-d90531)

- Sort: new angle. Owner precocious-puberty has an adrenal-tumor row (autonomous adrenal androgen, virilization) and items on virilization (q_da0183afd85955af9b62, 17-hydroxyprogesterone) and on a peripheral androgen source in a boy (q_aa34051b68ae504b9bbd). Nothing on the page reads DHEAS against testosterone; DHEAS, 17-ketosteroids and androgen-secreting ovarian tumors appear nowhere (grep). The task (localize the androgen source from labs and a normal pelvic ultrasound) and the look-alikes (ovarian tumor, PCOS, pituitary, androgen insensitivity) are new.
- Teaching points:
  - Clitoral enlargement is virilization, which normal adrenarche never causes; at 10 the pubic hair alone would be ordinary, the clitoromegaly is not.
  - DHEAS is made almost only by the adrenal (zona reticularis of the cortex); testosterone in a girl comes mostly from the ovary. High DHEAS with normal testosterone and a normal pelvic ultrasound points to the adrenal; high testosterone with an adnexal mass points to an ovarian (Sertoli-Leydig) tumor.
  - A DHEAS this far above range in a child is a tumor until proven otherwise; pediatric virilizing adrenocortical tumors are often carcinomas and labs cannot separate adenoma from carcinoma, so the exam answer "adenoma" means "adrenal tumor", not a benign label.
  - The common real-world alternative (nonclassic congenital adrenal hyperplasia, raised 17-hydroxyprogesterone) is not offered; the page's 17-OHP item covers it.
- Distractor design:
  - Lead-in: plain "most likely diagnosis". What it hides: the labs are given as a sentence with reference ranges, so the decider is reading which androgen is high and which is normal; the vitals and the 50th-percentile growth are filler (no Cushing features, no tall stature).
  - Adrenal adenoma (key): androgen source that raises DHEAS and urine 17-ketosteroids.
  - Androgen insensitivity syndrome. Tempts: an androgen word in a genital-exam stem. Ruled out: it is a receptor defect in a 46,XY child with female external genitalia and no androgen effect, so it cannot cause clitoromegaly or hirsutism.
  - "Ovarian adenoma" (NBME's name for an androgen-secreting ovarian tumor). Tempts: virilizing tumor in a girl. Ruled out: testosterone normal and the pelvic ultrasound normal.
  - Pituitary adenoma. Tempts: the third "adenoma"; a pituitary cause of precocity. Ruled out: no headache or field loss, and pituitary tumors do not virilize (ACTH excess would bring Cushing features).
  - Polycystic ovarian syndrome. Tempts: hirsutism and acne. Ruled out: premenarchal and at the 50th percentile for weight, testosterone normal, ovaries normal on ultrasound; PCOS does not cause clitoromegaly.
  - Construction: same-noun family (adenoma at adrenal, ovary and pituitary), so the question is a location question dressed as a histology question; one androgen-receptor option and one common-endocrine option fill the list. The source is localized by one lab (DHEAS) and one negative image (normal ovaries).
- Not to transfer: the explanation places the zona reticularis in the adrenal medulla (it is the innermost layer of the cortex); it credits 17-alpha-hydroxylase with making DHEA(S) from 17-hydroxypregnenolone (that step is the 17,20-lyase activity of the same enzyme, CYP17A1, and the sulfation is a separate sulfotransferase step); it implies such labs identify an adenoma (pediatric reviews report higher DHEAS in carcinoma than adenoma; histology decides).

## Q2 Posterior urethral valves in a well newborn (peds-cms-723033)

- Sort: new angle. Owner bs-puv teaches PUV through Potter sequence with a palpable bladder (q_0dc9b7ebaebf5161897a) and has the ultrasound-to-VCUG step (q_673f589cff4d5d1580c5). This item is a well, feeding newborn with prenatal hydronephrosis and no Potter features, decided by the stream and the bladder wall, against other causes of prenatal hydronephrosis. Ureteropelvic junction obstruction and duplex systems are absent from the page (grep); neurogenic bladder appears only in adult and VUR contexts.
- Teaching points:
  - Prenatal hydronephrosis sorts by level: kidney only (UPJ obstruction), kidney plus ureter (VUR, distal ureteral or bladder-level causes), kidney plus ureter plus a thick-walled bladder (outlet obstruction).
  - Bilateral hydroureteronephrosis with a thick-walled bladder and a weak, dribbling stream in a boy is posterior urethral valves; confirm with a VCUG (dilated, elongated posterior urethra) and treat by endoscopic valve ablation.
  - A normal spine and neurologic exam is what removes neurogenic bladder, the one decoy that shares the whole ultrasound picture.
- Distractor design:
  - Lead-in: plain diagnosis. What it hides: the obstruction level is given across three sentences (prenatal image, voiding exam, postnatal image); normal urine output tempts away from obstruction.
  - Duplicated collecting system. Tempts: a cause of prenatal hydronephrosis and hydroureter. Ruled out: usually one kidney (upper-pole moiety), and it does not thicken the bladder or weaken the stream.
  - Neurogenic bladder. Tempts: the closest mimic, with a trabeculated thick bladder, bilateral hydroureteronephrosis and dribbling. Ruled out: no spinal dysraphism or neurologic finding; in a boy with a poor stream and a normal exam, the outlet is the lesion.
  - Ureteropelvic junction obstruction. Tempts: the commonest cause of prenatal hydronephrosis. Ruled out: the ureters are dilated too, and the bladder is normal in UPJ obstruction.
  - Vesicoureteral reflux. Tempts: bilateral hydroureteronephrosis. Ruled out: normal bladder wall and a normal stream; reflux is often secondary to valves, not their alternative.
  - Construction: same-organ family (every option is a congenital urinary-tract cause of hydronephrosis), separated only by anatomic level; the page's Potter-sequence version is replaced by a well newborn.
- Not to transfer: nothing that matters; the explanation's neurogenic-bladder paragraph describes adult overflow incontinence, not the infant with a dysraphism.

## Q3 Which vaccine at a 4-month visit in October (peds-cms-ce7f06)

- Sort: new angle. Owner bs-adolescent-vax teaches the age platform with a seasonal date buried in the stem (June versus October) at 11 years. No brief teaches the infant platform: the page has the DTaP schedule line (dtap) and rotavirus only as a live vaccine to withhold in immunodeficiency (del22q11, ig-panel). If the lead prefers not to widen an adolescent-titled brief, the alternative is a new bs-infant-vax (gen).
- Teaching points:
  - A 4-month visit gives the second doses of the 2-month set: rotavirus (oral, live), DTaP, Hib, pneumococcal conjugate and IPV. Rotavirus has hard age limits: first dose by 14 weeks 6 days, last dose by 8 months.
  - Influenza vaccine starts at 6 months, so October (the right month) does not help a 4-month-old.
  - MMR and varicella are live vaccines due at 12 to 15 months; zoster vaccine is an adult vaccine (recombinant, from age 50).
- Distractor design:
  - Lead-in: "immunization against which of the following", with diseases, not vaccine products, as options. What it hides: two options name one virus.
  - Chickenpox. Tempts: a routine childhood vaccine. Ruled out: first dose at 12 months.
  - Influenza. Tempts: the October date in line one. Ruled out: age under 6 months.
  - Measles-mumps-rubella. Tempts: routine and live like rotavirus. Ruled out: first dose at 12 months.
  - Shingles. Tempts: same virus as chickenpox. Ruled out: an adult vaccine.
  - Construction: age-gate ladder with a seasonal cue; every wrong option is a real vaccine given at the wrong age, and only one of the five vaccines actually due today is listed. "Immunizations up to date" means the 2-month doses were given.
- Not to transfer: the explanation dates zoster vaccination to age 60 (current CDC: two doses of recombinant zoster vaccine from 50, or from 19 if immunocompromised); "influenza from greater than 6 months" should read "from 6 months".

## Q4 Growth failure, hypokalemia and a normal-gap acidosis: distal RTA (peds-cms-0354fa)

- Sort: new. No brief owns reading a potassium and acid-base panel. bs-ftt lists RTA in its differential and has one item keyed to ordering electrolytes with a venous gas (q_c58ffe3da98457e3843f); secondary-htn covers hyperaldosteronism and renal artery stenosis with hypertension. Pseudohypoaldosteronism, Bartter syndrome and juxtaglomerular hyperplasia appear nowhere (grep). Proposed brief: bs-distal-rta, "Hypokalemia with Acidosis in a Child", system Renal, data-bp="renal"; link from the bs-ftt RTA row.
- Teaching points:
  - Anion gap 138 minus (112 plus 16) = 10: a normal-gap (hyperchloremic) metabolic acidosis. With no diarrhea, the loss is renal.
  - Urine pH above 5.5 during systemic acidosis means the distal tubule cannot secrete acid: distal (type 1) RTA, which wastes potassium and stunts growth in toddlers.
  - Sort hypokalemia by acid-base and blood pressure: with acidosis, diarrhea or RTA; with alkalosis and high BP, primary aldosteronism or renin excess; with alkalosis and normal BP, vomiting, diuretics or Bartter/Gitelman.
  - Pco2 by Winter's formula: 1.5 x 16 + 8 = 32 plus or minus 2; the measured 26 is at or below that range (appropriate or extra compensation, not "incomplete").
- Distractor design:
  - Lead-in: asks the cause of the hypokalemia, not of the growth failure or the acidosis. What it hides: the answer is decided by the acid-base column, and the K+ is the least specific value on the panel.
  - Addison disease. Tempts: metabolic acidosis and a low-normal BP. Ruled out: it raises potassium and lowers sodium.
  - Congenital adrenal hyperplasia. Tempts: an adrenal cause of growth problems. Ruled out: the salt-wasting form gives high potassium and low sodium; the hypertensive forms give alkalosis.
  - Hyperparathyroidism. Tempts: PTH can cause a mild hyperchloremic acidosis. Ruled out: no calcium given and it does not waste potassium or alkalinize the urine this way.
  - Juxtaglomerular cell hyperplasia (the histologic name of Bartter syndrome). Tempts: the closest mimic, a toddler with growth failure, hypokalemia and normal BP. Ruled out: Bartter gives metabolic alkalosis; this child is acidotic.
  - Pheochromocytoma. Tempts: an adrenal tumor. Ruled out: no hypertension or paroxysms.
  - Primary hyperaldosteronism. Tempts: the textbook hypokalemia. Ruled out: hypertension and alkalosis, both absent.
  - Pseudohypoaldosteronism. Tempts: hyperchloremic acidosis with growth failure in an infant. Ruled out: potassium is high in it.
  - Renal artery stenosis. Tempts: renin-driven hypokalemia. Ruled out: hypertension and alkalosis.
  - Construction: a nine-option lab grid in which each option sits in one cell of potassium (high or low) by acid-base (acid or alkali) by BP (high or normal); only one cell matches. Two options are disguised by name (juxtaglomerular hyperplasia for Bartter, pseudohypoaldosteronism). The stem's "no vomiting or diarrhea" closes the GI-loss cells.
- Not to transfer: the explanation says juxtaglomerular hyperplasia causes systemic hypertension (Bartter syndrome, whose hallmark it is, is normotensive with hypokalemic alkalosis); it calls the respiratory response a "compensatory respiratory alkalosis" and "incomplete" (the pH is 7.28, and the Pco2 is at or below Winter's range).

## Q5 New murmur on day 3 radiating to the axillae: pulmonary stenosis (peds-cms-c4694e)

- Sort: covered. Owner ped-murmur, item q_fb94648142ed51749518: a well 3-week-old with a soft midsystolic murmur at the upper sternal borders radiating to both axillae and the back is peripheral pulmonary stenosis, which resolves by 6 to 12 months; q_f159d63dc88654de85b9 covers the persistent murmur that earns an echo. Same deciding finding (well newborn, soft systolic murmur, pulmonic area, radiation to the lung fields and axillae). Link only, plus one "How NBME framed it" line.
- Teaching points (for the framing line only):
  - NBME keyed the umbrella term "pulmonary stenosis"; peripheral pulmonary stenosis is not offered, so the umbrella is the only fit.
  - A murmur that is new on day 3 tempts the lesions that appear as pulmonary resistance falls (VSD, PDA); the radiation to the axillae and the soft grade decide.
- Distractor design:
  - Lead-in: plain diagnosis. What it hides: the newborn exam at birth was normal, so the murmur is "new", which points to transitional physiology rather than a fixed defect.
  - Aortic stenosis. Tempts: ejection murmur at the base. Ruled out: right upper sternal border radiating to the carotids, not the axillae.
  - Atrial septal defect. Tempts: a pulmonic-area flow murmur. Ruled out: rarely heard in the first days; the tell is a fixed split S2.
  - Patent ductus arteriosus. Tempts: a murmur appearing in the first days in a term baby. Ruled out: continuous, under the left clavicle.
  - Ventricular septal defect. Tempts: the classic "new murmur as resistance falls". Ruled out: holosystolic at the lower left sternal border, not the pulmonic area.
  - Construction: the five commonest acyanotic lesions; the key names the category, not the entity the stem describes.
- Not to transfer: the explanation describes valvar stenosis (ejection click, parasternal heave, radiation to the back, balloon valvotomy) although the stem describes physiologic peripheral pulmonary stenosis, which needs no treatment and resolves in months; it calls supravalvar stenosis "also called peripheral"; its claim that PS is more common in girls is unsupported. Keep the page's ped-murmur wording.

## Q6 SCFE: internal fixation (peds-cms-3d1862)

- Sort: new angle. Owner scfe states the treatment in prose (non-weight-bearing, urgent in situ screw fixation, never reduce) and limp's table says pin in situ, but no item on the page keys the management decision (item search for fixation or pinning finds only a scaphoid item). New task: management, against the treatments of the other hip diseases.
- Teaching points:
  - Obese 13-year-old, weeks of groin pain and limp, lost internal rotation, obligate external rotation on flexion: SCFE, even when the x-ray shows only a widened, irregular physis (a pre-slip).
  - Treatment is surgical in situ fixation across the physis, with the child non-weight-bearing until then; bracing, casting, traction or therapy do not stop the slip.
  - Image both hips; the other side slips in a large minority.
- Distractor design:
  - Lead-in: "in addition to analgesia and weight-loss counseling", granting the supportive half so only the definitive step is left.
  - Physical therapy. Tempts: an overweight child with hip pain and stiffness. Ruled out: the physis is unstable; therapy is for strains.
  - Abduction bracing. Tempts: a real hip treatment. Ruled out: it treats DDH in infants.
  - Traction. Tempts: a hip-fracture reflex. Ruled out: no trauma; it lengthens displaced fractures.
  - Spica cast immobilization. Tempts: another hip treatment (and historically used for SCFE). Ruled out: DDH after reduction; casting SCFE is abandoned because of chondrolysis.
  - Construction: treatment-of-a-mimic menu; every wrong option is the right treatment for another hip problem (DDH twice, fracture, sprain). The stem never says "slip".
- Not to transfer: nothing material. The explanation's frog-leg view is fine for a stable slip; the stem used a cross-table lateral, which is the safer view.

## Q7 Mycoplasma pneumonia in a 10-year-old (peds-cms-0efcba)

- Sort: new angle (carrier item). Owner mycoplasma: its decision point is this exact case (school-age child, 1 to 2 weeks of gradual cough, low fever, bilateral diffuse findings), but no bank item keys Mycoplasma pneumonia as the diagnosis (items key its complications and the other atypicals), so data-nbme has nowhere to attach. Add one carrier item. The congestive-heart-failure and tuberculosis look-alikes are new to the brief.
- Teaching points:
  - Over age 5, gradual onset over 10 days, low-grade fever, bilateral crackles and a diffuse perihilar/interstitial film = Mycoplasma; treat with a macrolide.
  - RSV pneumonia is an infant's disease (under 2, with wheeze); pneumococcus is abrupt and lobar.
- Distractor design:
  - Lead-in: plain diagnosis, options written as "Pneumonia due to <organism>" beside two non-organism diagnoses.
  - Pneumonia due to RSV. Tempts: viral, diffuse. Ruled out: age 10.
  - Pneumonia due to Streptococcus pneumoniae. Tempts: the commonest bacterial pneumonia. Ruled out: gradual course, low fever, diffuse rather than lobar.
  - Congestive heart failure. Tempts: "diffuse perihilar infiltrate" and bilateral crackles are the words of pulmonary edema. Ruled out: previously healthy child with fever.
  - Tuberculosis. Tempts: subacute cough. Ruled out: no exposure, weight loss or night sweats; the film is not hilar adenopathy or cavitation.
  - Construction: organism-named pneumonias split by age and onset, plus an imaging-phrase mimic (the film is worded so a non-infectious diagnosis fits it).
- Not to transfer: the "vesicular rash" in the examination list is not a typical pneumonia finding; vesiculobullous lesions do occur (Mycoplasma-induced rash and mucositis), so it is not wrong, but it should not be taught as an exam sign of the pneumonia.

## Q8 Bilateral flank masses in a well newborn: polycystic kidney disease (peds-cms-6821fe)

- Sort: new angle. Owner bs-abdominal-mass (its source vignette used the same option set against Wilms tumor; its table has a polycystic kidney row and an MCDK newborn item). The page's only ARPKD item (bs-puv q_0db3b05afa39584a8a69) decides by Potter facies and hepatomegaly; this newborn has neither, and the decoys are tumors and renal vein thrombosis. Renal vein thrombosis appears only in nephrotic syndrome (aq-puffy-eyes).
- Teaching points:
  - Bilateral enlarged kidneys at birth in a well baby = autosomal recessive polycystic kidney disease until proven otherwise; ultrasound shows large echogenic kidneys; look for hepatic fibrosis.
  - A creatinine of 0.9 on day 1 is the mother's creatinine (the page's neonatal-maternal-labs item), not proof of renal failure.
  - Neonatal renal vein thrombosis also gives a flank mass and hematuria, but in a stressed infant (diabetic mother, asphyxia, dehydration, polycythemia), usually with thrombocytopenia.
- Distractor design:
  - Lead-in: plain diagnosis. What it hides: the key is written as "polycystic kidney disease" with no inheritance, and the ultrasound says "mixed echogenicity", not "cysts".
  - Nephroblastoma (Wilms tumor), under its formal name. Tempts: flank mass with hematuria. Ruled out: unilateral, age 2 to 5.
  - Neuroblastoma. Tempts: the commonest abdominal tumor of infancy. Ruled out: adrenal, displaces rather than enlarges the kidney, rarely symmetric.
  - Renal cell carcinoma. Tempts: renal mass with hematuria. Ruled out: a disease of adults and adolescents.
  - Renal vein thrombosis. Tempts: neonatal flank mass with hematuria and an enlarged kidney. Ruled out: uncomplicated pregnancy, good Apgars, normal hematocrit, no risk factor.
  - Construction: mass family by age (three tumors from the page's Wilms item plus one vascular mimic); the lab panel plants hematuria and a raised creatinine that fit the decoys.
- Not to transfer: the explanation's inheritance paragraph runs the autosomal dominant features (aneurysms, hepatic cysts) into the ARPKD discussion and then attributes fetal onset and Potter sequence with an ambiguous "it"; teach ARPKD (PKHD1, hepatic fibrosis, Caroli syndrome, Potter sequence) and ADPKD (adult, cysts, aneurysms) separately. Its reason for rejecting renal vein thrombosis (it would not distort intrarenal architecture) is weak; the risk factors are the real reason.

## Q9 Hordeolum: warm compresses (peds-cms-7a44ef)

- Sort: new. No hordeolum, chalazion, dacryocystitis or eyelid-lump content exists (grep). redeye (neuro) owns red-eye diagnoses and abrs-complications owns preseptal versus orbital cellulitis, but neither carries this decision. Proposed brief: bs-eyelid-lump, "Eyelid Lumps and Swelling in a Child", system Nervous system and special senses, data-bp="neuro"; pairs with redeye and abrs-complications.
- Teaching points:
  - A tender nodule at the lid margin with local redness is a hordeolum (acute, infected gland); a painless, rubbery lump away from the margin weeks later is a chalazion.
  - First-line treatment is warm compresses with gentle lid massage several times a day; oral antibiotics only if cellulitis spreads beyond the lesion; incision if it persists.
  - Swelling below the medial canthus is dacryocystitis; diffuse lid swelling is preseptal cellulitis; pain with eye movement or proptosis is orbital.
- Distractor design:
  - Lead-in: "most appropriate treatment". What it hides: the stem leads with a red, painful eye and conjunctival swelling (a conjunctivitis frame) and places the nodule last.
  - Nasolacrimal massage. Tempts: "massage" echoes the real treatment. Ruled out: that is for a blocked tear duct or dacryocystitis, at the medial canthus; this nodule is lateral, on the margin.
  - Oral amoxicillin. Tempts: an infection. Ruled out: no fever and no diffuse lid swelling, so no cellulitis.
  - Topical prednisolone. Tempts: inflammation of the eye. Ruled out: steroids are for uveitis and are avoided in infection.
  - Topical tetrahydrozoline. Tempts: treats the redness the stem opens with. Ruled out: a cosmetic vasoconstrictor that does nothing for the gland.
  - Construction: treatment-of-a-mimic menu across the red, swollen eye (tear duct, cellulitis, uveitis, symptomatic redness); the diagnosis is never named.
- Not to transfer: the explanation calls tetrahydrozoline an alpha-2 agonist; it is an imidazoline alpha agonist used for alpha-1 vasoconstriction, with alpha-2 activity that explains clonidine-like toxicity when swallowed, so "alpha-2 agonist" alone is incomplete. Its statement that topical antibiotic ointment helps is not a standard first-line recommendation (unverified here; leave it out).

## Q10 Early emphysema in a 16-year-old smoker: alpha-1 antitrypsin deficiency (peds-cms-44f3d3)

- Sort: new angle. Owner asthma-copd: its rule (emphysema before about 45 or with little smoking means test alpha-1 antitrypsin) and item q_fc488cc379ca5efd9dac (40-year-old, test task) teach the decision in an adult. New: a diagnosis task in an adolescent, against pediatric congenital lung lesions, ciliary dyskinesia and sarcoidosis.
- Teaching points:
  - Fixed hyperinflation and increased AP diameter in a young heavy smoker is early emphysema; emphysema this young means alpha-1 antitrypsin deficiency (unopposed neutrophil elastase; panlobular, basal).
  - Check the liver too: misfolded protein retained in hepatocytes causes neonatal cholestasis and later cirrhosis.
  - Clubbing is not a feature of COPD or of AATD; in a real child it points to cystic fibrosis or bronchiectasis.
- Distractor design:
  - Lead-in: plain diagnosis. What it hides: the most likely real diagnosis (severe asthma in a smoker) is absent, so the item is solved by eliminating four rare disorders; a past history of asthma admissions is offered as a distraction.
  - Congenital lobar emphysema. Tempts: the word emphysema and hyperinflation. Ruled out: presents in the newborn or infant as one overinflated lobe, not bilateral in a teenager.
  - Kartagener syndrome. Tempts: thick yellow sputum and clubbing. Ruled out: no situs inversus, chronic sinusitis or lifelong wet cough.
  - Pulmonary sequestration. Tempts: congenital lung lesion. Ruled out: recurrent pneumonia in one lobe and a mass on the film.
  - Sarcoidosis. Tempts: a chronic lung disease of the young. Ruled out: film has no hilar adenopathy or infiltrates.
  - Construction: rare-disease family with the common answer omitted; a planted sign (clubbing) that fits a decoy better than the key.
- Not to transfer: the explanation says the evaluation suggests basal emphysema, but the film shows only bilateral hyperinflation; clubbing is left unexplained. Label for the lead: emphysema at 16 after 4 years of smoking is unusual even with AATD (typical onset in smokers is the 30s to 40s; memory-sourced).

## Q11 CGD as impaired microbicidal activity (peds-cms-252cd2)

- Sort: covered. Owner cgd, item q_1f7b49f7314459b8b98f keys the same mechanism (decreased superoxide production: normal migration and ingestion, failed intracellular killing) against defective chemotaxis, opsonization, antibody and airway clearance. LAD (q_ea0c1b219556516eb0b8) and Chediak-Higashi (q_772d219c8bc8e1274236) items exist. Link only, plus one "How NBME framed it" line: no organism or granuloma is given; the deciders are recurrent abscesses, osteomyelitis and pneumonia plus a maternal uncle's death from fungal pneumonia (X-linked); the key is written as a verb ("impaired microbicidal activity"). The brief never mentions osteomyelitis or a pedigree cue.
- Teaching points (framing line only):
  - Recurrent skin abscesses, osteomyelitis and pneumonia in a boy whose maternal uncle died of a fungal pneumonia = X-linked CGD; the defect is killing, not migration.
- Distractor design:
  - Lead-in: "which mechanism of disease", with every option a leukocyte verb.
  - Abnormal leukocyte adhesion. Tempts: a neutrophil defect with recurrent skin infection. Ruled out: LAD has delayed cord separation, no pus and a very high WBC.
  - Abnormal leukocyte degranulation. Tempts: same family. Ruled out: Chediak-Higashi has albinism, neuropathy and giant granules.
  - Bone marrow infiltration. Tempts: fever and nodes. Ruled out: no cytopenias; years of infections without leukemia.
  - Impaired leukocyte chemotaxis. Tempts: the second LAD option. Ruled out: same as adhesion; two options map to one disease, so neither can be the key.
  - Construction: one noun, a series of steps (adhesion, chemotaxis, degranulation, killing) plus one off-family option; the "rash" is cellulitis with inguinal lymphadenitis, called a macular rash to disguise it.
- Not to transfer: the explanation's organism list includes Staphylococcus epidermidis, which is not a characteristic CGD pathogen; keep the page's list.

## Q12 Rash in an unvaccinated immigrant: MMR would have prevented it (peds-cms-9fb189)

- Sort: new angle. Owner bs-exanthems (the measles item q_1116e1bfe041c2c88774 and the rubella items in bs-fever-rash-arthralgia teach the diagnoses). New task: prevention, "which vaccine would have prevented this", which is answered without separating measles from rubella.
- Teaching points:
  - A descending maculopapular rash that starts on the face in an unvaccinated child is measles or rubella, and MMR prevents both, so the prevention question does not require the split.
  - Split them anyway: measles has high fever, cough, coryza, conjunctivitis, Koplik spots and a confluent rash in an ill child; rubella is mild, low-grade, with discrete pink lesions and posterior auricular or suboccipital nodes. This stem (low fever, mild rhinorrhea, discrete lesions, no eye or mouth lesions) reads as rubella.
  - Varicella is vesicular in crops and starts on the trunk; itching alone does not make it varicella.
- Distractor design:
  - Lead-in: prevention instead of diagnosis, which hides that the stem and the explanation disagree on the diagnosis.
  - DTaP, Haemophilus influenzae type b, hepatitis B, inactivated poliovirus, pneumococcal. Tempt: each is a vaccine an immigrant may have missed. Ruled out: none prevents a rash illness.
  - Influenza virus. Tempts: fever, fatigue, rhinorrhea. Ruled out: no rash.
  - Typhoid. Tempts: immigrant from Central America with fever and a rash (rose spots). Ruled out: the stem states no abdominal pain or diarrhea.
  - Varicella. Tempts: itching and a rash in an unvaccinated child. Ruled out: discrete maculopapules, not vesicles; face first.
  - Construction: the whole routine schedule as a nine-option list, plus one travel vaccine; negatives in the stem are placed to close the typhoid and measles-complication routes.
- Not to transfer: the explanation teaches measles (three Cs, Koplik spots, confluent rash) for a stem without conjunctivitis or oral lesions; do not write this stem into the page as measles. Its pneumococcal line (adults over 65) is dated: CDC now recommends pneumococcal conjugate vaccine for all adults from 50.

---

## NBME explanation errors not to transfer (checked)

| Q | Claim in the explanation | Status | Correct version | Source |
|---|---|---|---|---|
| 1 | Zona reticularis is in the adrenal medulla | confirmed error | It is the inner layer of the cortex | standard anatomy |
| 1 | 17-alpha-hydroxylase converts 17-hydroxypregnenolone to DHEAS | confirmed error | The 17,20-lyase activity of CYP17A1 makes DHEA; a sulfotransferase makes DHEAS | MedlinePlus CYP17A1; Soucy 2000 |
| 1 | Such labs indicate an adenoma | misleading | Very high DHEAS in a child raises carcinoma as much as adenoma; histology decides | Frontiers Endocrinol 2023 pediatric ACC review |
| 3 | Zoster vaccine from 60 | dated | Recombinant zoster vaccine from 50 (19 if immunocompromised) | CDC shingles vaccine recommendations |
| 4 | Juxtaglomerular cell hyperplasia causes hypertension | confirmed error | JG hyperplasia is the Bartter lesion: normotensive, hypokalemic metabolic alkalosis | LITFL Bartter syndrome |
| 4 | "Compensatory respiratory alkalosis", "incomplete" compensation | misnamed | Respiratory compensation; Pco2 26 is at or below Winter's 30 to 34 | Winter's formula |
| 5 | Describes valvar PS (click, heave, back radiation, valvotomy) | mismatch with stem | Stem is physiologic PPS: soft, to axillae and back, resolves by 3 to 6 months | AAFP 2022 pediatric murmurs |
| 7 | Vesicular rash as an exam finding | defensible, atypical | Vesicles and bullae occur (MIRM) but are not a pneumonia sign | DermNet Mycoplasma |
| 8 | ADPKD features placed in the ARPKD paragraph; ambiguous "it" | muddled | Teach ARPKD and ADPKD separately | standard |
| 9 | Tetrahydrozoline is an alpha-2 agonist | incomplete | Alpha agonist at alpha-1 and alpha-2; used for alpha-1 vasoconstriction | Wikipedia Tetryzoline (lower-grade source; ⚠︎ confirm against a label if it matters) |
| 10 | Bibasilar emphysema "suggested" by the evaluation | unsupported by stem | Film shows only hyperinflation; clubbing is not a COPD/AATD sign | clinical references on clubbing in COPD |
| 12 | Explanation diagnoses measles | mismatch with stem | Stem reads as rubella; MMR key holds either way | standard |
| 12 | Pneumococcal vaccine for adults over 65 | dated | All adults from 50 | CDC pneumococcal recommendations |
