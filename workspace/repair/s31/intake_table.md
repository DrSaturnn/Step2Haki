# s31 NBME intake table (Pediatrics form, form name unknown)

Source: repair/sources/s31_questions.md (local-only, verbatim). This file paraphrases; option labels are quoted only to record NBME phrasing. Pasted 2026-09-24; 27 items, of which 22 were missed and 5 answered right. Q1 and Q2 repeat the two s28-linked items, so they are recorded as same_as and not duplicated. Task types follow the lead-in. "Owner" is the intake reading of the candidates (nbme_match top 5 plus a keyword search of the page), to be confirmed per nbme-intake step 3; no sort (covered / new angle / conflict / new) is assigned yet.

| Q | nbme_id | fingerprint | key | task | result | time | same_as | owner (intake reading) |
|---|---|---|---|---|---|---|---|---|
| 1 | peds-cms-fdc19e | fdc19ea8c1 | Cyclic neutropenia | dx | incorrect | 1:15 | peds-cms-fdc19e (s28, same fingerprint fdc19ea8c1) | cgd (s28 link) |
| 2 | peds-cms-aa91d7 | aa91d7708d | Rocky Mountain spotted fever | dx | incorrect | 0:54 | peds-cms-aa91d7 (s28, same fingerprint aa91d7708d) | rmsf (s28 link) |
| 3 | peds-cms-56f5bb | 56f5bbfbe3 | Delayed / delayed / delayed | development | incorrect | 0:32 |  | growth; bs-preterm-followup (weak) |
| 4 | peds-cms-bd082e | bd082ea01b | Tetralogy of Fallot | dx | incorrect | 2:39 |  | cyanotic-chd |
| 5 | peds-cms-e43eb8 | e43eb88d89 | Enzyme deficiency | mechanism | incorrect | 0:20 |  | neonatal-jaundice; bs-spherocytosis (G6PD) |
| 6 | peds-cms-f52102 | f52102d3bf | Pseudomonas aeruginosa | organism | incorrect | 0:49 |  | NONE (osteomyelitis only as a mimic in bone-tumors) |
| 7 | peds-cms-03615c | 03615c9d56 | Herpes simplex virus | organism | incorrect | 1:13 |  | neonatal-rash (neonatal HSV item); febrile-seizure (HSV on CSF) (weak) |
| 8 | peds-cms-cb45d9 | cb45d9c1cd | Measurement of serum concentration of C3 | next step dx | incorrect | 2:01 |  | bs-nephritic |
| 9 | peds-cms-42aa4f | 42aa4fc095 | Congestive heart failure | mechanism | incorrect | 4:06 |  | kawasaki (missed by nbme_match; found by keyword); myocarditis |
| 10 | peds-cms-80d5b8 | 80d5b8a4c5 | Influenza-induced myositis | dx | incorrect | 0:45 |  | NONE |
| 11 | peds-cms-dd1427 | dd14275ada | Topical nystatin | mgmt | incorrect | 1:24 |  | diaper-dermatitis (candida; no vulvovaginitis) (weak) |
| 12 | peds-cms-d74882 | d74882ed03 | Optic nerve glioma | mechanism (risk) | incorrect | 0:48 |  | tumor-syndromes |
| 13 | peds-cms-123615 | 1236155277 | Chromosome 15 deletion, maternally inherited | mechanism (genetics) | correct | 1:19 |  | NONE (malform-syndromes / aneuploidy nearest) |
| 14 | peds-cms-ae7cd7 | ae7cd759d6 | HIV infection | mechanism (disease) | incorrect | 1:24 |  | ig-panel; hiv-vax (weak) |
| 15 | peds-cms-060d9c | 060d9ca19a | Thyroid function tests | next step dx | incorrect | 1:07 |  | congenital-hypothyroid |
| 16 | peds-cms-2944bc | 2944bca243 | Gonococcal conjunctivitis | dx | incorrect | 0:37 |  | redeye (neonatal conjunctivitis timing row) |
| 17 | peds-cms-dd721b | dd721b647f | Fresh frozen plasma | mgmt | correct | 0:31 |  | bs-fat-soluble-vitamins |
| 18 | peds-cms-6facf4 | 6facf4b156 | Reassurance (rash resolves in a few days) | mgmt | correct | 0:49 |  | neonatal-rash |
| 19 | peds-cms-9a2ab1 | 9a2ab14e11 | Blood pressure measurement by auscultation | next step dx | incorrect | 0:54 |  | NONE |
| 20 | peds-cms-dbb94d | dbb94d9ec8 | Bone marrow aspiration | next step dx | correct | 1:34 |  | bs-leukemia |
| 21 | peds-cms-9b4c4f | 9b4c4f897d | Infected thyroglossal duct cyst | dx | correct | 1:12 |  | lymphadenitis (thyroglossal duct cyst item) |
| 22 | peds-cms-f627e3 | f627e3263b | Hepatoblastoma | dx (explanation of a mass) | incorrect | 0:44 |  | bs-abdominal-mass |
| 23 | peds-cms-e6a460 | e6a460da4f | Rheumatic fever | dx | incorrect | 2:56 |  | arf |
| 24 | peds-cms-42419d | 42419d1d00 | Spirochete | organism | incorrect | 0:52 |  | bs-fever-rash-arthralgia (secondary syphilis row) (weak) |
| 25 | peds-cms-6b35bd | 6b35bd50d3 | Repeat urinalysis at bedtime and on awakening | next step dx | incorrect | 0:34 |  | NONE |
| 26 | peds-cms-e52ce6 | e52ce6c99d | Poorly developed acetabulum | mechanism | incorrect | 0:25 |  | limp (DDH row); bs-torticollis (weak) |
| 27 | peds-cms-5c434b | 5c434b6f9b | NAAT for C. trachomatis and N. gonorrhoeae | screening | incorrect | 0:47 |  | cervicitis |

## Per question: topic, NBME framing, nbme_match top 5

### Q1 Cyclic neutropenia (peds-cms-fdc19e)

- NBME framing: Name-swap decoy: "Fanconi syndrome" (renal tubule) sits beside marrow-failure options where Fanconi anemia would belong; a 9-option list of neutropenias and marrow failures.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. cgd (0.183), Recurrent Abscesses and Granulomas | q_bd617d53d7c3c8f78cff -> Cyclic neutropenia
  2. cyclic-vomiting (0.096), Cyclic Vomiting Syndrome | q_7f71d5f727d4704c2a31 -> Personal or family history of migraine
  3. del22q11 (0.076), 22q11.2 Deletion Syndrome | q_64be248830bc5ff18b97 -> The live attenuated rotavirus vaccine
  4. ig-panel (0.068), The Immunoglobulin Panel | q_123276d9f025df1d53fe -> Autoimmune polyendocrine syndrome type 1
  5. aq-infant-fever (0.056), Fever in an Infant | q_1608e3829bcc736d5831 -> Chest x-ray

### Q2 Rocky Mountain spotted fever (peds-cms-aa91d7)

- NBME framing: Kawasaki offered under its formal name "Mucocutaneous lymph node syndrome"; no tick exposure is given (June, rural setting, mosquito bites as decoys).
- Candidates (nbme_match: brief, title, closest item, its key):
  1. rmsf (0.329), Tick-Borne Fever and Rash | q_f301e03be41b7aa167b0 -> Rocky Mountain spotted fever
  2. bs-exanthems (0.044), Exanthems in a Child | q_baaf6a02a943c8a51e61 -> Varicella
  3. neonatal-rash (0.040), Benign Neonatal Rashes | q_ee07b7cec8875310382c -> Reassurance only
  4. bs-nat-fracture (0.039), Suspected Child Abuse: Fractures and the Next Step | q_ec5293dc6e06a0df9c41 -> Langerhans cell histiocytosis
  5. neonatal-bowel (0.037), The Distended Abdomen in a Newborn or Infant | q_d6ae55f4494c28124dcd -> Intestinal malrotation with midgut volvulus

### Q3 Development at 4 years (peds-cms-56f5bb)

- NBME framing: A 3-column Gross / Fine / Language grid of delayed-or-normal combinations (8 rows); the key is the all-delayed row, i.e. global delay.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. growth (0.164), Growth & Developmental Milestones | q_f5e98603c0245f03aa65 -> Refer for early intervention services
  2. cerebral-palsy (0.083), Cerebral Palsy and the MRI Pattern | q_8f4c04fe5f0655b280d9 -> Assess milestones against her corrected age of about 5 month
  3. bs-preterm-followup (0.059), Prematurity Follow-Up and Corrected Age | q_33dc7103cc6855a9ab44 -> She has had fewer weeks of growth and brain development
  4. bs-tanner (0.055), Sexual Maturity Rating | q_436570f2555851189f17 -> Reassurance and observation
  5. meralgia (0.050), Meralgia Paresthetica | q_3001b36e0d3a5bb0b7b6 -> Meralgia paresthetica

### Q4 Tetralogy of Fallot (peds-cms-bd082e)

- NBME framing: Plain disease-name list; the decider sits in the exam and spell history, not in the option wording.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. cyanotic-chd (0.147), Cyanotic Congenital Heart Disease | q_abf5415254ced3a48d5d -> Tetralogy of Fallot
  2. newborn-cyanosis (0.123), Cyanosis in the Newborn | q_72ff1748ba8d533fa2e2 -> Knee-to-chest positioning with supplemental oxygen
  3. bs-murmur-map (0.115), Murmur Man and Post-ToF Pulmonic Regurgitation | q_76c765842c585b2f9b6e -> Ventricular arrhythmia
  4. bs-shunt-timing (0.095), Congenital Shunts and the Transitional Clock | q_602dbb66f29254409016 -> Echocardiography
  5. hypoxemia-mech (0.090), Mechanisms of Hypoxemia | q_8969cd1d1d4a56c3add3 -> Titrating oxygen to a saturation of 100%

### Q5 G6PD deficiency, newborn jaundice (peds-cms-e43eb8)

- NBME framing: Key is the category "Enzyme deficiency" (G6PD is never named); maternal sulfonamide exposure and Mediterranean descent carry it; Coombs-negative.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. neonatal-jaundice (0.202), Neonatal Jaundice | q_c5b948d9253906aa4201 -> Phototherapy
  2. bs-spherocytosis (0.114), Hereditary Spherocytosis | q_49f4a3aadee2550ab8e0 -> Phototherapy
  3. bs-galactosemia (0.111), The Sick Jaundiced Neonate with a Positive Screen | q_9f0568882aea52bab399 -> Stop breast milk and start soy-based formula
  4. drug-hemolysis (0.104), Drug-Induced Immune Hemolysis | q_c92ec11000b25cf29208 -> Direct antiglobulin (Coombs) test
  5. congenital-hypothyroid (0.096), Congenital Hypothyroidism | q_eb6590b03f2f542b9c47 -> Slowed gastrointestinal motility with reduced hepatic biliru

### Q6 Puncture-wound osteomyelitis (peds-cms-f52102)

- NBME framing: Organism list with a water-borne decoy (Aeromonas hydrophila) and the usual Staphylococcus aureus; the key rests on the puncture-through-a-sneaker exposure.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. bs-pyelo-organism (0.090), Pyelonephritis: Naming the Organism | q_e7ad1e5c1b5a55d7a0ed -> Pseudomonas aeruginosa
  2. bs-tdap-preg (0.076), Tdap in Pregnancy at 10 Weeks | q_a2777f4f85c45b88b11b -> Tdap now
  3. septic-bursitis (0.059), Septic Bursitis | q_ffbf7b1ef5e556b18080 -> Aspirate the bursal fluid
  4. dtap (0.054), DTaP: Contraindication vs. Precaution | q_83b156a4fd375f838715 -> Precaution
  5. bs-adolescent-vax (0.050), Adolescent Immunization and the Age Platform | q_fcc597ce1eed524a82b8 -> Begin the HPV series today

### Q7 Neonatal HSV encephalitis (peds-cms-03615c)

- NBME framing: Neonatal organism list mixing a virus, bacteria and a parasite (CMV, E. coli, GBS, HSV, Toxoplasma); key by day-of-life and CSF pattern.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. febrile-seizure (0.102), Seizure with Fever in a Child | q_16fe3ec314b65593b554 -> Herpes simplex encephalitis
  2. aq-infant-fever (0.085), Fever in an Infant | q_ba095e97628c1fd44705 -> Bacterial meningitis
  3. meningitis (0.068), Bacterial Meningitis | q_86dde21b2b1d58f59f7e -> Viral meningitis
  4. aq-infant-hypotonia (0.066), Hypotonia in an Infant | q_f789042784394e65a807 -> SMN1 deletion testing
  5. ig-panel (0.061), The Immunoglobulin Panel | q_e9d935e4bd31ca6ce785 -> Impaired B-cell differentiation into plasma cells

### Q8 Poststreptococcal GN (peds-cms-cb45d9)

- NBME framing: Procedure phrasing: "Measurement of serum concentration of C3" as the next diagnostic step.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. aq-puffy-eyes (0.109), Child with Puffy Eyes | q_c20dc17b4c19a5dd8bc1 -> Renal biopsy
  2. polyuria (0.100), Polyuria: Water or Solute | q_6ad8368a69544663af2f -> Water deprivation test
  3. bs-nephritic (0.100), Acute Nephritic Syndrome in a Child | q_aeb588e544ebeb4b9c39 -> Serum C3 level
  4. hematuria (0.091), Hematuria | q_3b7389e870885b086d99 -> Serum creatinine, complement levels and CBC
  5. myocarditis (0.083), New Heart Failure in a Child | q_02b05f4554e854d7b193 -> Viral myocarditis

### Q9 Kawasaki disease: tachypnea (peds-cms-42aa4f)

- NBME framing: Mechanism options written as pathology: "Thickened internal layer of pulmonary arterioles", "Mitral valve obstruction", "Pericardial effusion"; key "Congestive heart failure".
- Candidates (nbme_match: brief, title, closest item, its key):
  1. myocarditis (0.097), New Heart Failure in a Child | q_aa13968d642451bd8d1f -> Kawasaki disease
  2. cyanotic-chd (0.068), Cyanotic Congenital Heart Disease | q_d78b7bf3e2315e9d8c37 -> Complete atrioventricular canal defect
  3. angina (0.068), Anginal Equivalents & Stress Test Selection | q_c31e1ab3b50758dfb9bb -> Typical angina
  4. scd-dyspnea (0.063), Chronic Dyspnea in Sickle Cell Disease | q_c20af37f9e8951efa7cf -> CT pulmonary angiogram
  5. newborn-cyanosis (0.062), Cyanosis in the Newborn | q_bc8c10a704495f0f85a5 -> Start CPAP

### Q10 Influenza myositis (peds-cms-80d5b8)

- NBME framing: Kawasaki again as "Mucocutaneous lymph node syndrome"; "Influenza-induced myositis" named by cause and tissue.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. myositis-ossificans (0.099), The Post-Traumatic Limb Mass | q_6d1f3fc9cc1e56b3bd79 -> Myositis ossificans
  2. growing-pains (0.069), Benign Limb Pain in a Child | q_790ff3a627b65e83b421 -> Order a complete blood count with peripheral smear
  3. bs-nephritic (0.050), Acute Nephritic Syndrome in a Child | q_a7769a969941371a1cbd -> Furosemide
  4. peds-headache-imaging (0.048), Headache in a Child: What Earns Imaging | q_85ab0235bfba5f5e8ac2 -> Continuing the daily as-needed analgesic
  5. hiv-vax (0.046), Vaccines in HIV | q_486f1f0d5fe1549c8797 -> Inactivated influenza vaccine

### Q11 Prepubertal vulvovaginal candidiasis (peds-cms-dd1427)

- NBME framing: Treatment options each paired with a route (IM ceftriaxone plus oral azithromycin, oral acyclovir, oral metronidazole, topical nystatin); the child-abuse STI regimen is the decoy.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. neonatal-rash (0.127), Benign Neonatal Rashes | q_23a20fc8b90a23d471e6 -> Topical nystatin
  2. diaper-dermatitis (0.110), Diaper Dermatitis | q_1113dd8ae2e857bea16f -> Topical nystatin to the diaper area plus oral nystatin
  3. newborn-hormone (0.092), Maternal Hormone Effects in the Newborn | q_427ef9f92e5859848b84 -> Report for suspected sexual abuse
  4. pmb (0.068), Postmenopausal Bleeding | q_705026981adf58c59c7b -> Endometrial cancer until proven otherwise
  5. bs-nat-fracture (0.059), Suspected Child Abuse: Fractures and the Next Step | q_ec5293dc6e06a0df9c41 -> Langerhans cell histiocytosis

### Q12 NF1: optic glioma risk (peds-cms-d74882)

- NBME framing: Risk framing: the lead-in asks what this patient is at increased risk for, compared with the general population; the diagnosis (NF1) is left unnamed.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. tumor-syndromes (0.094), Inherited Tumor Syndromes | q_f48046d17f7b58fcb6de -> Neurofibromatosis type 1
  2. aq-child-headache (0.062), Headache in a School-Age Child | q_bc4dac9c50620bc08599 -> Blocked axoplasmic flow in the optic nerve
  3. sellar-mass (0.051), Sellar and Suprasellar Masses | q_4d1a62e938a053759510 -> Compression of decussating nasal retinal fibers at the optic
  4. bs-exanthems (0.049), Exanthems in a Child | q_f58b089883599c60d997 -> Supportive care with an oral antihistamine
  5. bs-adolescent-vax (0.048), Adolescent Immunization and the Age Platform | q_99716f748294537e8362 -> Tdap

### Q13 Angelman syndrome (peds-cms-123615)

- NBME framing: Genetic-defect options by chromosome and parent of origin ("Chromosome 15 deletion, maternally inherited" vs "paternally inherited"), plus MECP2 and trisomies.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. aneuploidy (0.092), Aneuploidy: Reading the Newborn | q_d1c66454a7c08641eabc -> Turner syndrome
  2. bs-ftt (0.079), Faltering Weight | q_1858059b7d5a5c2d82c7 -> An endocrine cause — growth hormone deficiency or hypothyroi
  3. bs-preterm-followup (0.078), Prematurity Follow-Up and Corrected Age | q_79c5134acd5d58ec80c5 -> Refer for developmental evaluation and early intervention
  4. malform-syndromes (0.077), Multiple Anomalies in a Newborn | q_c26a6ed7a75b2e24be66 -> Trisomy 13
  5. aq-infant-hypotonia (0.071), Hypotonia in an Infant | q_b89face125781fdc8e1e -> Karyotype of both parents

### Q14 Pediatric HIV (peds-cms-ae7cd7)

- NBME framing: "Mechanisms of disease" lead-in with a list of immunodeficiencies; the key is an infection (HIV infection) among primary immunodeficiencies.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. ig-panel (0.175), The Immunoglobulin Panel | q_b07107552c26c47f26e7 -> Severe combined immunodeficiency
  2. cgd (0.092), Recurrent Abscesses and Granulomas | q_bd617d53d7c3c8f78cff -> Cyclic neutropenia
  3. bs-leukemia (0.088), Pediatric Acute Lymphoblastic Leukemia | q_2516a22d0e2c558b8421 -> Complete blood count with differential and peripheral smear
  4. aq-infant-fever (0.087), Fever in an Infant | q_3ee904c7ec2e5e6ffb78 -> 4 mL twice daily
  5. aq-bruising (0.079), Bruising and Purpura in a Child | q_c0d8dd73fbfb5b6ab1e9 -> Bone marrow examination

### Q15 Congenital hypothyroidism (peds-cms-060d9c)

- NBME framing: Test options include wrong-organ imaging (CT of the head, CT of the liver) and sweat chloride; key "Thyroid function tests".
- Candidates (nbme_match: brief, title, closest item, its key):
  1. bs-umbilical (0.105), Umbilical Findings in a Newborn | q_7e472e5bd7e09a357f4d -> Serum TSH and free T4
  2. neonatal-maternal-labs (0.075), Maternal Carryover in Newborn Labs | q_88bba0bacc3c594cafc1 -> Observe with serial platelet counts
  3. congenital-hypothyroid (0.066), Congenital Hypothyroidism | q_3e20457c599a58018c77 -> Thyroid ultrasound or radionuclide uptake scan
  4. bs-galactosemia (0.059), The Sick Jaundiced Neonate with a Positive Screen | q_ca8409261f4b50c7a726 -> Breast milk
  5. newborn-cyanosis (0.056), Cyanosis in the Newborn | q_4ee70a03ddd6595b8c98 -> Breast milk jaundice

### Q16 Neonatal gonococcal conjunctivitis (peds-cms-2944bc)

- NBME framing: Conjunctivitis list by cause (allergic, chemical, chlamydial, gonococcal) plus Kawasaki as "Mucocutaneous lymph node syndrome"; timing (day 2) decides.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. redeye (0.104), The Red Eye | q_bfc2adf60a295d1a841a -> Gonococcal conjunctivitis
  2. aq-puffy-eyes (0.081), Child with Puffy Eyes | q_8442cb229ccc78bc8c39 -> Bacterial conjunctivitis
  3. newborn-hormone (0.068), Maternal Hormone Effects in the Newborn | q_c4ef4b784ada51bcb9ab -> Vertical Chlamydia trachomatis transmission
  4. bs-nat-fracture (0.060), Suspected Child Abuse: Fractures and the Next Step | q_081dcb3c76e53c9c5e6b -> Report to child protective services
  5. uri (0.059), Pediatric Upper Respiratory Infection | q_71e6b236832b5f26879f -> Supportive care with saline irrigation and analgesics

### Q17 Vitamin K deficiency bleeding (peds-cms-dd721b)

- NBME framing: Lead-in takes vitamin K as already given and asks what to add; blood-product list.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. bs-fat-soluble-vitamins (0.110), Fat-Soluble Vitamin Deficiency and Toxicity | q_6a602762b258ee5a7b37 -> Excess vitamin A intake
  2. factor-inhibitor (0.046), Hemophilia A Inhibitor | q_6cc975a7283b3006d023 -> Factor XIII deficiency
  3. bs-isolation (0.043), Isolation Precautions | q_a3438738a3b75ac6ccf0 -> Airborne precautions
  4. peutz-jeghers (0.038), Peutz-Jeghers Syndrome | q_ee9358efb98dc94119ee -> Upper and lower endoscopy
  5. bs-nat-fracture (0.038), Suspected Child Abuse: Fractures and the Next Step | q_3f17fa44a5e091076a45 -> Nutritional rickets

### Q18 Erythema toxicum (peds-cms-6facf4)

- NBME framing: Management options written as full actions (reassure the parents that the rash is transient, culture plus antibiotics, KOH stain); the key begins "Reassurance to the parents".
- Candidates (nbme_match: brief, title, closest item, its key):
  1. neonatal-rash (0.110), Benign Neonatal Rashes | q_ee07b7cec8875310382c -> Reassurance only
  2. newborn-hormone (0.066), Maternal Hormone Effects in the Newborn | q_be77176c899550fcbdb3 -> Reassurance and observation
  3. bs-infant-feeding (0.065), Infant Feeding at Six Months | q_278680a9a4af5d4b99c2 -> Limit milk under 24 oz daily and start oral iron
  4. bs-exanthems (0.058), Exanthems in a Child | q_1116e1bfe041c2c88774 -> Measles
  5. neonatal-bowel (0.053), The Distended Abdomen in a Newborn or Infant | q_44131b0bc9eaa69fa316 -> Abdominal x-ray with air in the bowel wall and portal veins

### Q19 Adolescent BP measurement (peds-cms-9a2ab1)

- NBME framing: Procedure options that differ only in technique and timing: "Blood pressure measurement by auscultation" vs oscillometric repeats (daily for 3 days, or in 2 weeks) vs 24-hour ambulatory.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. bs-short-stature (0.063), Short Stature and Growth Velocity | q_2a59e2776d02bcb2e0be -> Glucocorticoid excess
  2. copd (0.062), COPD: Which Interventions Improve Survival | q_8ae0956915f654db8cea -> Long-term oxygen therapy
  3. aq-infant-fever (0.057), Fever in an Infant | q_e412ee0850cc0bde9b60 -> Probably a false positive
  4. bs-pid (0.050), Pelvic Inflammatory Disease | q_607090b879cb59b89132 -> Treat and leave the device in place
  5. bs-dexa-highrisk (0.049), DEXA: When Screening Starts Early | q_c6114373cc3256e6bda1 -> DEXA at 65

### Q20 ALL: marrow aspiration (peds-cms-dbb94d)

- NBME framing: Imaging options (abdominal CT, bone scan, gallium scan) against "Bone marrow aspiration"; liver biopsy as a decoy.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. bs-leukemia (0.140), Pediatric Acute Lymphoblastic Leukemia | q_2516a22d0e2c558b8421 -> Complete blood count with differential and peripheral smear
  2. sjia (0.101), Juvenile Idiopathic Arthritis | q_0f7557200bb25f49a751 -> Systemic juvenile idiopathic arthritis
  3. aq-bruising (0.093), Bruising and Purpura in a Child | q_c0d8dd73fbfb5b6ab1e9 -> Bone marrow examination
  4. septic-hip (0.084), Septic Arthritis of the Hip | q_6317a30c6b5d530ca106 -> Septic arthritis complicating juvenile idiopathic arthritis
  5. cgd (0.076), Recurrent Abscesses and Granulomas | q_bd617d53d7c3c8f78cff -> Cyclic neutropenia

### Q21 Infected thyroglossal duct cyst (peds-cms-9b4c4f)

- NBME framing: "Most likely cause of these findings" with infection-by-name options (cat-scratch disease, mononucleosis, tonsillitis, viral syndrome) against a congenital cyst.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. lymphadenitis (0.134), Enlarged Lymph Nodes: Reading the Pattern | q_bbe63e88a23044cd7f3a -> Thyroglossal duct cyst
  2. congenital-hypothyroid (0.079), Congenital Hypothyroidism | q_7419210396345d74a71a -> Dyshormonogenesis from a thyroid peroxidase defect
  3. airway (0.054), Pediatric Airway & Noisy Breathing | q_64ad875cee703a3733a9 -> Depressing the tongue to inspect the pharynx
  4. peds-alopecia (0.047), Patchy Hair Loss in a Child | q_d998fb4d51bf56518261 -> KOH examination of proximal hair shafts or fungal culture
  5. sellar-mass (0.044), Sellar and Suprasellar Masses | q_d3def13fcf725f61915c -> MRI of the brain with contrast

### Q22 Beckwith-Wiedemann: hepatoblastoma (peds-cms-f627e3)

- NBME framing: "Most likely explanation for this patient's mass" with the syndrome given; tumor names in formal form ("Nephroblastoma (Wilms tumor)", "Germ cell tumor").
- Candidates (nbme_match: brief, title, closest item, its key):
  1. peds-aki (0.089), NSAID Prerenal AKI in a Child | q_0e384a752b3b546baf53 -> Isotonic fluids and stop the ibuprofen
  2. bs-abdominal-mass (0.085), Abdominal Mass in a Young Child | q_cd6dcccab739215600ae -> Urine VMA and HVA
  3. bs-umbilical (0.066), Umbilical Findings in a Newborn | q_ef47cdcba6bd7ec534de -> Urgent surgical repair
  4. bs-fat-soluble-vitamins (0.059), Fat-Soluble Vitamin Deficiency and Toxicity | q_4c902ebf73a699b6fab7 -> Vitamin D 50,000 IU weekly for 8 weeks
  5. liver-preg (0.058), Liver Disease in Pregnancy | q_23614287ba85d6b63f1c -> Emergent delivery

### Q23 Acute rheumatic fever (peds-cms-e6a460)

- NBME framing: Travel-and-fever decoys (dengue, malaria, typhoid, Lyme) plus Kawasaki as "Mucocutaneous lymph node syndrome".
- Candidates (nbme_match: brief, title, closest item, its key):
  1. sjia (0.111), Juvenile Idiopathic Arthritis | q_dcc21109d541cdb738b2 -> Naproxen
  2. arf (0.097), Acute Rheumatic Fever | q_163add7fdad553c2a5e2 -> Acute rheumatic fever
  3. myocarditis (0.093), New Heart Failure in a Child | q_02b05f4554e854d7b193 -> Viral myocarditis
  4. bs-fever-rash-arthralgia (0.089), Fever, Rash and Joint Pain in a Child or Adolescent | q_2bdcffda772905c78f3f -> Acute rheumatic fever
  5. bs-murmur-map (0.078), Murmur Man and Post-ToF Pulmonic Regurgitation | q_12f2872861635d009adf -> Mitral stenosis

### Q24 Primary syphilis (painless chancre): organism class (peds-cms-42419d)

- NBME framing: Class-level organism options ("Spirochete", "Obligate intracellular bacterium", "Gram-negative diplococcus", "Protozoan", "Virus"); the disease is never named.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. bs-cervical-gate (0.074), Cervical Screening: the Age-21 Floor | q_4e03aecd840d573fbd70 -> No screening
  2. copd (0.054), COPD: Which Interventions Improve Survival | q_8ae0956915f654db8cea -> Long-term oxygen therapy
  3. bs-fever-rash-arthralgia (0.050), Fever, Rash and Joint Pain in a Child or Adolescent | q_5413d7739952fa996be1 -> Disseminated gonococcal infection
  4. gynecomastia (0.044), Gynecomastia vs. Male Breast Cancer | q_2939230240ef5bbabdfb -> Male breast cancer
  5. htn-drugs (0.043), Hypertension: Workup & Drug Choice | q_438a31b48ab6599eb15b -> Losartan

### Q25 Orthostatic proteinuria (peds-cms-6b35bd)

- NBME framing: Procedure phrasing: "Repeat urinalysis at bedtime and on awakening" (split-urine test) against imaging, steroids and biopsy.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. hematuria (0.051), Hematuria | q_3b7389e870885b086d99 -> Serum creatinine, complement levels and CBC
  2. copd (0.050), COPD: Which Interventions Improve Survival | q_8ae0956915f654db8cea -> Long-term oxygen therapy
  3. htn-drugs (0.049), Hypertension: Workup & Drug Choice | q_438a31b48ab6599eb15b -> Losartan
  4. enuresis (0.048), Nocturnal Enuresis | q_aee72a7d300a55b18d1a -> Urinary tract infection
  5. aq-bruising (0.039), Bruising and Purpura in a Child | q_9d65833030574e4c390e -> Urinalysis

### Q26 DDH: mechanism (peds-cms-e52ce6)

- NBME framing: Mechanism phrasing: "Poorly developed acetabulum", with "Displacement of the capital femoral epiphysis" and "Failure of osteoid to mineralize" standing for SCFE and rickets.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. bs-torticollis (0.083), Congenital Muscular Torticollis and Plagiocephaly | q_e85ad792a91453aca090 -> Congenital muscular torticollis
  2. synovitis (0.079), Transient Synovitis Mirror twin | q_5fc72e65e76553a39bcc -> Transient synovitis
  3. limp (0.077), The Limping Child — Master Table | q_bdee86ce98775e1e9a3f -> Developmental dysplasia of the hip
  4. bs-nrd (0.056), Neonatal Respiratory Distress | q_6a0cfe5187475cf7a8fa -> Transient tachypnea of the newborn
  5. gtps (0.055), Pain Around the Hip and Thigh | q_0209b3c970df55b2b276 -> Hip OA

### Q27 Adolescent chlamydia/gonorrhea screening (peds-cms-5c434b)

- NBME framing: Screening list of unrelated tests (mammography, fasting glucose, hemoglobin, Pap smear); key spelled out in full as nucleic acid amplification testing for both organisms, with genus and species written out.
- Candidates (nbme_match: brief, title, closest item, its key):
  1. cervicitis (0.128), Acute Cervicitis | q_0f6451e737de5aba9e3c -> Azithromycin
  2. bs-tanner (0.122), Sexual Maturity Rating | q_436570f2555851189f17 -> Reassurance and observation
  3. newborn-hormone (0.121), Maternal Hormone Effects in the Newborn | q_427ef9f92e5859848b84 -> Report for suspected sexual abuse
  4. primary-amenorrhea (0.105), Primary Amenorrhea | q_4538bb4d79a95a078a00 -> Pelvic ultrasonography
  5. bs-pid (0.081), Pelvic Inflammatory Disease | q_d52bb4ef2c735c419bb8 -> Evaluate and presumptively treat partners from the last 60 d
