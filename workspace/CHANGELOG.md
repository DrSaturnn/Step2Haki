# Changelog

Newest first. Each entry is the commit body written by tools/ship.sh.

## 2026-09-24 s32: Mobile sidebar replaces the bottom sheet; full-text search on phone and desktop; Board-style only toggle replaces NBME-tested

```
Page: 207 briefs, 2014 items -> 207 briefs, 2014 items
Other page changes (nav, headers, scripts): +21852 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 207 briefs, 2014 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 207 | bankwraps 207 | mcq 2014 (axCheck 2014, reveal-only 0) | malformed 0 | crit gridded 123/124 | vignette gridded 129/129 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (42269 source shingles; page 0.031%)
```

## 2026-09-24 s31: NBME Peds batch: 27 questions linked; 6 new briefs, 12 backfills, NBME wording guide

```
Page: 201 briefs, 1942 items -> 207 briefs, 2014 items
Briefs added (6):
  - bs-puncture-osteomyelitis: Foot Puncture Wound Infection (5 items)
  - bs-acute-myositis: Benign Acute Childhood Myositis (8 items)
  - bs-adolescent-bp: Confirming High Blood Pressure in an Adolescent (6 items)
  - bs-isolated-proteinuria: Incidental Proteinuria in a Well Child (7 items)
  - bs-imprinting: Angelman Syndrome and Its Genetic Look-Alikes (7 items)
  - bs-genital-ulcer: Genital Ulcer: Painless or Painful (8 items)
Briefs changed (26):
  - limp (The Limping Child — Master Table): 2 items added (q_b599f8e62f2070a52991, q_11abb36f6ad6ea3085a4); prose edited (+2317 chars)
  - growing-pains (Benign Limb Pain in a Child): prose edited (+110 chars)
  - growth (Growth & Developmental Milestones): 3 items added (q_907cd6543effc4c0dec6, q_d0c9d6f19c78dd1fed12, q_eca33fcf91f5726143e5); prose edited (+2008 chars)
  - newborn-hormone (Maternal Hormone Effects in the Newborn): prose edited (+77 chars)
  - aneuploidy (Aneuploidy: Reading the Newborn): prose edited (+142 chars)
  - cyanotic-chd (Cyanotic Congenital Heart Disease): 2 items added (q_1dafa1911a5a64278be2, q_dc06038895874469075d); prose edited (+1628 chars)
  - kawasaki (Kawasaki Disease): 3 items added (q_5c5ebd26ef5fe11337d5, q_495dfa71396b7036d94a, q_e96fadc94a8327131c75); prose edited (+2035 chars)
  - arf (Acute Rheumatic Fever): attrs set (q_163add7fdad553c2a5e2 data-nbme); prose edited (+284 chars)
  - neonatal-jaundice (Neonatal Jaundice): 2 items added (q_68047f53bb547e1428b5, q_ea850ed3646b8e8e5167); prose edited (+1701 chars)
  - bs-umbilical (Umbilical Findings in a Newborn): attrs set (q_7e472e5bd7e09a357f4d data-nbme); prose edited (+278 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): 3 items added (q_44a4c5430977368dd3fc, q_187ede1b74536a0c7f62, q_ca7906ad3ce2003c2e2e); prose edited (+1423 chars)
  - nephrotic-child (Nephrotic Syndrome in a Child): prose edited (+148 chars)
  - bs-nephritic (Acute Nephritic Syndrome in a Child): attrs set (q_aeb588e544ebeb4b9c39 data-nbme); prose edited (+389 chars)
  - bs-abdominal-mass (Abdominal Mass in a Young Child): 3 items added (q_d9b8dd343b4ca836c41d, q_aacccbc0cf7974df049d, q_9ba68702a02ebc4483c1); prose edited (+1565 chars)
  - tumor-syndromes (Inherited Tumor Syndromes): 3 items added (q_791ab466c5d3371ac2d4, q_a73027aea794cb20e60e, q_07869c908680b86b0b69); prose edited (+2388 chars)
  - bs-leukemia (Pediatric Acute Lymphoblastic Leukemia): attrs set (q_d5a219c1127f50cba341 data-nbme); prose edited (+296 chars)
  - cervicitis (Acute Cervicitis): 2 items added (q_424c322e1a1fb44f35a6, q_6037409dfb4feb0f247f); prose edited (+2056 chars)
  - ig-panel (The Immunoglobulin Panel): 3 items added (q_6f1f0484f7cc597f3a69, q_ef6b8e7ad853646f5cd4, q_4319327c01c3ba7a9234); prose edited (+2702 chars)
  - rmsf (Tick-Borne Fever and Rash): prose edited (+243 chars)
  - lymphadenitis (Enlarged Lymph Nodes: Reading the Pattern): attrs set (q_bbe63e88a23044cd7f3a data-nbme); prose edited (+260 chars)
  - bs-torch (Congenital CMV and the TORCH Discriminations): 3 items added (q_f04e1e07cd1dacf1c640, q_92c751f85de71a0bcb69, q_a3ec9f313a821c1030d1); prose edited (+2501 chars)
  - bs-fever-rash-arthralgia (Fever, Rash and Joint Pain in a Child or Adolescent): prose edited (+103 chars)
  - redeye (The Red Eye): attrs set (q_bfc2adf60a295d1a841a data-nbme); prose edited (+288 chars)
  - cerebral-palsy (Cerebral Palsy and the MRI Pattern): prose edited (+161 chars)
  - neonatal-rash (Benign Neonatal Rashes): attrs set (q_ee07b7cec8875310382c data-nbme); prose edited (+242 chars)
  - diaper-dermatitis (Diaper Dermatitis): 2 items added (q_02665e6eb263aaa1aecd, q_ccd48da198c8448a6e8f); prose edited (+1986 chars)
Other page changes (nav, headers, scripts): +3593 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 207 briefs, 2014 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 207 | bankwraps 207 | mcq 2014 (axCheck 2014, reveal-only 0) | malformed 0 | crit gridded 123/124 | vignette gridded 129/129 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (42269 source shingles; page 0.033%)
```

## 2026-09-24 s30: GI plain-voice round 2: shorter sentences, acronyms written out, claim-mapped for no drift

```
Page: 201 briefs, 1942 items -> 201 briefs, 1942 items
Briefs changed (21):
  - liver-preg (Liver Disease in Pregnancy): prose edited (+246 chars)
  - masld (MASLD / Metabolic Fatty Liver): prose edited (+149 chars)
  - cholestasis (Cholestasis & the LFT Patterns): prose edited (+209 chars)
  - zenker (Zenker Diverticulum): prose edited (+17 chars)
  - infant-stool (Infant Stool Complaints: Dyschezia, FPIAP & Secondary Lactase Deficiency): prose edited (+312 chars)
  - fap (Familial Adenomatous Polyposis): prose edited (+233 chars)
  - peutz-jeghers (Peutz-Jeghers Syndrome): prose edited (+74 chars)
  - feeding-refusal (Toddler Food Refusal): prose edited (-56 chars)
  - rlq-pain (Right Lower Quadrant Pain): prose edited (-73 chars)
  - peds-constipation (Constipation in a Child): prose edited (-194 chars)
  - cyclic-vomiting (Cyclic Vomiting Syndrome): prose edited (+3 chars)
  - neonatal-jaundice (Neonatal Jaundice): prose edited (+204 chars)
  - neonatal-bowel (The Distended Abdomen in a Newborn or Infant): prose edited (+366 chars)
  - occult-gi-bleed (Occult GI Bleeding in a Child): prose edited (+172 chars)
  - bs-galactosemia (The Sick Jaundiced Neonate with a Positive Screen): prose edited (+249 chars)
  - bs-impaction (Fecal Impaction & Overflow Diarrhea): prose edited (+31 chars)
  - bs-tef (Tracheoesophageal Fistula with Esophageal Atresia): prose edited (+192 chars)
  - bs-umbilical (Umbilical Findings in a Newborn): prose edited (+109 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): prose edited (+824 chars)
  - bs-water-soluble-vitamins (Water-Soluble Vitamin Deficiency): prose edited (+233 chars)
  - bs-wilson (Wilson Disease: Copper in the Liver, Brain and Eye): prose edited (+22 chars)
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 201 briefs, 1942 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 201 | bankwraps 201 | mcq 1942 (axCheck 1942, reveal-only 0) | malformed 0 | crit gridded 120/121 | vignette gridded 123/123 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (27616 source shingles; page 0.033%)
```

## 2026-09-24 s29: Badges follow NBME first; subtitles drop provenance; GI plain-voice pass (sample)

```
Page: 201 briefs, 1942 items -> 201 briefs, 1942 items
Briefs changed (99):
  - myositis-ossificans (The Post-Traumatic Limb Mass): prose edited (-17 chars)
  - growing-pains (Benign Limb Pain in a Child): prose edited (-17 chars)
  - bone-tumors (Bone Tumors: Location, Film, Course): prose edited (-16 chars)
  - bs-torticollis (Congenital Muscular Torticollis and Plagiocephaly): prose edited (-9 chars)
  - bs-brachial-plexus (Brachial Plexus Injury at Birth): prose edited (-9 chars)
  - shoulder-rom (Shoulder Pain: the Range-of-Motion Rule): prose edited (-16 chars)
  - neonatal-maternal-labs (Maternal Carryover in Newborn Labs): prose edited (-24 chars)
  - newborn-hormone (Maternal Hormone Effects in the Newborn): prose edited (-24 chars)
  - aneuploidy (Aneuploidy: Reading the Newborn): prose edited (-16 chars)
  - malform-syndromes (Multiple Anomalies in a Newborn): prose edited (-16 chars)
  - bs-learning (Specific Learning Disorder): prose edited (-9 chars)
  - bs-nat-fracture (Suspected Child Abuse: Fractures and the Next Step): prose edited (-16 chars)
  - bs-shock (Shock in Children): prose edited (-10 chars)
  - bs-infant-feeding (Infant Feeding at Six Months): prose edited (-10 chars)
  - bs-tanner (Sexual Maturity Rating): prose edited (-10 chars)
  - bs-ftt (Faltering Weight): prose edited (-10 chars)
  - bs-preterm-followup (Prematurity Follow-Up and Corrected Age): prose edited (-10 chars)
  - aq-infant-hypotonia (Hypotonia in an Infant): prose edited (-55 chars)
  - newborn-cyanosis (Cyanosis in the Newborn): prose edited (-24 chars)
  - myocarditis (New Heart Failure in a Child): prose edited (-16 chars)
  - del22q11 (22q11.2 Deletion Syndrome): prose edited (-16 chars)
  - bs-murmur-map (Murmur Man and Post-ToF Pulmonic Regurgitation): prose edited (-9 chars)
  - bs-shunt-timing (Congenital Shunts and the Transitional Clock): prose edited (-10 chars)
  - sinopulm-structural (Recurrent Sinopulmonary Infection): prose edited (-24 chars)
  - hypoxemia-mech (Mechanisms of Hypoxemia): prose edited (-24 chars)
  - abpa (When Antibiotics Fail in a Structural Lung): prose edited (-24 chars)
  - scd-dyspnea (Chronic Dyspnea in Sickle Cell Disease): prose edited (-24 chars)
  - bs-nrd (Neonatal Respiratory Distress): prose edited (-10 chars)
  - liver-preg (Liver Disease in Pregnancy): prose edited (-82 chars)
  - masld (MASLD / Metabolic Fatty Liver): prose edited (+2 chars)
  - cholestasis (Cholestasis & the LFT Patterns): prose edited (-55 chars)
  - zenker (Zenker Diverticulum): prose edited (-483 chars)
  - infant-stool (Infant Stool Complaints: Dyschezia, FPIAP & Secondary Lactase Deficiency): prose edited (-249 chars)
  - fap (Familial Adenomatous Polyposis): prose edited (-569 chars)
  - peutz-jeghers (Peutz-Jeghers Syndrome): prose edited (-424 chars)
  - feeding-refusal (Toddler Food Refusal): prose edited (-801 chars)
  - rlq-pain (Right Lower Quadrant Pain): prose edited (-746 chars)
  - peds-constipation (Constipation in a Child): prose edited (-1054 chars)
  - cyclic-vomiting (Cyclic Vomiting Syndrome): prose edited (-198 chars)
  - neonatal-jaundice (Neonatal Jaundice): prose edited (-293 chars)
  - neonatal-bowel (The Distended Abdomen in a Newborn or Infant): prose edited (-96 chars)
  - occult-gi-bleed (Occult GI Bleeding in a Child): prose edited (-227 chars)
  - bs-galactosemia (The Sick Jaundiced Neonate with a Positive Screen): prose edited (-345 chars)
  - bs-impaction (Fecal Impaction & Overflow Diarrhea): prose edited (-217 chars)
  - bs-tef (Tracheoesophageal Fistula with Esophageal Atresia): prose edited (-396 chars)
  - bs-umbilical (Umbilical Findings in a Newborn): prose edited (-70 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): prose edited (+0 chars)
  - bs-water-soluble-vitamins (Water-Soluble Vitamin Deficiency): prose edited (-8 chars)
  - bs-wilson (Wilson Disease: Copper in the Liver, Brain and Eye): prose edited (-14 chars)
  - vur (Vesicoureteral Reflux): prose edited (-24 chars)
  - peds-uti-recurrent (Recurrent Urinary Infection in a Child): prose edited (-24 chars)
  - polyuria (Polyuria: Water or Solute): prose edited (-16 chars)
  - nephrotic-child (Nephrotic Syndrome in a Child): prose edited (-24 chars)
  - bs-puv (Posterior Urethral Valves and Potter Sequence): prose edited (-10 chars)
  - bs-nephritic (Acute Nephritic Syndrome in a Child): prose edited (-16 chars)
  - bs-abdominal-mass (Abdominal Mass in a Young Child): prose edited (-16 chars)
  - aq-puffy-eyes (Child with Puffy Eyes): prose edited (-55 chars)
  - congenital-hypothyroid (Congenital Hypothyroidism): prose edited (-24 chars)
  - tumor-syndromes (Inherited Tumor Syndromes): prose edited (-24 chars)
  - precocious-puberty (Precocious Puberty): prose edited (-17 chars)
  - bs-short-stature (Short Stature and Growth Velocity): prose edited (-16 chars)
  - anemia-thrombocytopenia (Anemia with Thrombocytopenia): prose edited (-24 chars)
  - drug-hemolysis (Drug-Induced Immune Hemolysis): prose edited (-24 chars)
  - transfusion (Transfusion Reactions): prose edited (-24 chars)
  - bs-spherocytosis (Hereditary Spherocytosis): prose edited (-10 chars)
  - bs-sickle-trait (Sickle Cell Trait versus Disease): prose edited (-9 chars)
  - aq-bruising (Bruising and Purpura in a Child): prose edited (-55 chars)
  - ig-panel (The Immunoglobulin Panel): prose edited (-24 chars)
  - rmsf (Tick-Borne Fever and Rash): prose edited (-16 chars)
  - lymphadenitis (Enlarged Lymph Nodes: Reading the Pattern): prose edited (-16 chars)
  - herpangina (Oral Vesicles in a Child): prose edited (-16 chars)
  - cgd (Recurrent Abscesses and Granulomas): prose edited (-24 chars)
  - bs-pta (Peritonsillar Abscess and the Deep Neck Spaces): prose edited (-9 chars)
  - bs-torch (Congenital CMV and the TORCH Discriminations): prose edited (-9 chars)
  - bs-neonatal-sepsis (Neonatal Sepsis and Its Mimics): prose edited (-24 chars)
  - bs-fever-rash-arthralgia (Fever, Rash and Joint Pain in a Child or Adolescent): prose edited (-9 chars)
  - bs-exanthems (Exanthems in a Child): prose edited (-9 chars)
  - bs-anaphylaxis (Anaphylaxis and Its Mimics): prose edited (-16 chars)
  - bs-isolation (Isolation Precautions): prose edited (-16 chars)
  - bs-foodborne (Foodborne Diarrhea: Source and Organism): prose edited (-16 chars)
  - bs-febrile-infant (The Febrile Infant — Finding the Source): prose edited (-10 chars)
  - aq-infant-fever (Fever in an Infant): prose edited (-55 chars)
  - sellar-mass (Sellar and Suprasellar Masses): prose edited (-24 chars)
  - peds-headache-imaging (Headache in a Child: What Earns Imaging): prose edited (-24 chars)
  - cholesteatoma (Cholesteatoma and Chronic Ear Drainage): prose edited (-24 chars)
  - febrile-seizure (Seizure with Fever in a Child): prose edited (-24 chars)
  - cerebral-palsy (Cerebral Palsy and the MRI Pattern): prose edited (-24 chars)
  - retinitis-pigmentosa (Night Blindness): prose edited (-16 chars)
  - tics (Tics in a School-Age Child): prose edited (-16 chars)
  - bs-tethered (Tethered Cord and Closed Spinal Dysraphism): prose edited (-9 chars)
  - bs-peds-stroke (Stroke in a Child or Adolescent): prose edited (-16 chars)
  - bs-posterior-fossa (Posterior Fossa Localization): prose edited (-10 chars)
  - aq-child-headache (Headache in a School-Age Child): prose edited (-54 chars)
  - peds-alopecia (Patchy Hair Loss in a Child): prose edited (-24 chars)
  - diaper-dermatitis (Diaper Dermatitis): prose edited (-16 chars)
  - teratogens (Teratogenic Exposures): prose edited (-24 chars)
  - primary-amenorrhea (Primary Amenorrhea): prose edited (-24 chars)
  - bs-pid (Pelvic Inflammatory Disease): prose edited (-10 chars)
  - bs-adolescent-vax (Adolescent Immunization and the Age Platform): prose edited (-10 chars)
Other page changes (nav, headers, scripts): +1108 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 201 briefs, 1942 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 201 | bankwraps 201 | mcq 1942 (axCheck 1942, reveal-only 0) | malformed 0 | crit gridded 120/121 | vignette gridded 123/123 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (27616 source shingles; page 0.033%)
```

## 2026-09-24 s28d: Workspace in Step2Haki: ship updates the site copy, writes a changelog, pushes with a token

```
Page: 201 briefs, 1942 items -> 201 briefs, 1942 items
Page content unchanged.
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 201 briefs, 1942 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 201 | bankwraps 201 | mcq 1942 (axCheck 1942, reveal-only 0) | malformed 0 | crit gridded 120/121 | vignette gridded 123/123 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (27616 source shingles; page 0.033%)
```

