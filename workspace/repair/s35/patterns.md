# How NBME builds pediatric questions: patterns across s31, s34 and s35

Paraphrase only. Sources: repair/s31/intake_table.md and sort_1..4.md (27 items), repair/s34/sort_1.md (3 items), repair/s35/sort.md (12 items). "In block" means the pattern is already a line in the page's "How NBME words questions" block (id nbme-wording, 10 lines as of HEAD c46c048). "Extends" means the block has the idea but not this form. Brief ids for s35 are the owners in repair/s35/sort.md; bs-distal-rta and bs-eyelid-lump are proposed, not yet on the page.

## A. How the lead-in hides the task

| # | Pattern | Example (paraphrased) | Brief | Status |
|---|---|---|---|---|
| A1 | The diagnosis is given as its mechanism | CGD keyed as impaired microbicidal activity among adhesion, chemotaxis and degranulation (s35 Q11); ITP as increased platelet destruction (s34 Q3) | cgd; aq-bruising | In block (DDH, G6PD). s35 adds the step-series form, see C4 |
| A2 | The lead-in asks about a secondary finding | "Cause of this toddler's hypokalemia" when the acid-base column decides (s35 Q4) | bs-distal-rta | New |
| A3 | Prevention lead-in skips the diagnosis | "Which vaccine would have prevented this" for a rash that reads as rubella while the explanation says measles; MMR covers both (s35 Q12) | bs-exanthems | New |
| A4 | Lead-in and option type disagree | Mechanism lead-in, disease-name options: Kawasaki tachypnea keyed as heart failure (s31 Q9); perinatal HIV among primary immunodeficiencies (s31 Q14) | kawasaki; ig-panel | New |
| A5 | The lead-in grants part of the answer | "In addition to vitamin K" (s31 Q17); "in addition to analgesia and weight-loss counseling" for SCFE (s35 Q6) | bs-fat-soluble-vitamins; scfe | In block |
| A6 | A lab direction is the question | Rickets asked as which value is increased (alkaline phosphatase) (s34 Q2) | bs-fat-soluble-vitamins | New |
| A7 | Risk compared with the general population | NF1 never named; asked which tumor risk is raised (s31 Q12) | tumor-syndromes | New |
| A8 | Immunization asked by disease, not product | "Immunization against which of the following" with Chickenpox and Shingles as separate options, one virus (s35 Q3) | bs-adolescent-vax | New |

## B. How the stem hides the decider

| # | Pattern | Example (paraphrased) | Brief | Status |
|---|---|---|---|---|
| B1 | The finding is described, never named | SCFE x-ray says only a widened, irregular physis (s35 Q6); a hordeolum is a 3-mm lid-margin nodule after a red-eye opening (s35 Q9); cellulitis called a macular rash (s35 Q11); osteomyelitis never written (s31 Q6); influenza never written (s31 Q10) | scfe; bs-eyelid-lump; cgd | New |
| B2 | An exposure is planted as bait | Mosquito bites in a spotted-fever stem (s31 Q2); cat scratches beside a thyroglossal cyst (s31 Q21); Central American immigrant beside a typhoid option (s35 Q12) | rmsf; lymphadenitis; bs-exanthems | In block |
| B3 | Negatives are placed to close one decoy each | No abdominal pain or diarrhea closes typhoid (s35 Q12); no vomiting or diarrhea closes GI potassium loss (s35 Q4); previously healthy closes heart failure (s35 Q7); uncomplicated pregnancy and good Apgars close renal vein thrombosis (s35 Q8) | bs-exanthems; bs-distal-rta; mycoplasma; bs-abdominal-mass | New (mirror of B4) |
| B4 | One cue planted per decoy | Mother's breast cancer, BMI, irregular menses and sexual activity each point to a different screening test (s31 Q27) | cervicitis | New |
| B5 | The exposure is withheld | Fetal alcohol syndrome with no maternal drinking history; the face decides (s34 Q1) | teratogens | New |
| B6 | The clue sits in a relative | Maternal uncle died of fungal pneumonia (X-linked CGD, s35 Q11); the mother's history carries perinatal HIV (s31 Q14) | cgd; ig-panel | New |
| B7 | A lab panel with reference ranges carries the answer | DHEAS high with testosterone normal (s35 Q1); AFP high with catecholamine metabolites normal (s31 Q22); anion gap and urine pH (s35 Q4) | precocious-puberty; bs-abdominal-mass; bs-distal-rta | New |
| B8 | A planted lab that fits the decoys | Day-1 creatinine of 0.9 (maternal carryover) and urine blood tempt tumor and thrombosis (s35 Q8); AKI chemistry hides a nephritic picture (s31 Q8) | bs-abdominal-mass; bs-nephritic | New |
| B9 | A planted sign that fits a decoy better than the key | Clubbing and yellow sputum in an AATD key favor Kartagener (s35 Q10); a soft murmur after strep pulls toward echo for carditis (s31 Q8) | asthma-copd; bs-nephritic | New |
| B10 | Past tense means untreated | A rash-and-fever illness that "resolved on its own" was Kawasaki never treated (s31 Q9) | kawasaki | New |
| B11 | The mild form of a disease the page teaches severe | PUV in a well newborn with no Potter features (s35 Q2); ARPKD with no Potter facies or hepatomegaly (s35 Q8) | bs-puv; bs-abdominal-mass | New |
| B12 | A date in line one is data | October visit for a 4-month-old: the right month, the wrong age for influenza (s35 Q3); June sports physical (bs-adolescent-vax source) | bs-adolescent-vax | Extends (brief has it, block does not) |
| B13 | The imaging phrase belongs to a non-infectious mimic | "Diffuse perihilar infiltrate" is the language of pulmonary edema (s35 Q7); "hyperinflation" echoes congenital lobar emphysema (s35 Q10) | mycoplasma; asthma-copd | New |

## C. How the options are built

| # | Pattern | Example (paraphrased) | Brief | Status |
|---|---|---|---|---|
| C1 | Same noun at different organs | Adrenal, ovarian and pituitary adenoma; the question is location, answered by one lab and one normal image (s35 Q1) | precocious-puberty | New |
| C2 | Same-organ family separated by level | Every option a cause of prenatal hydronephrosis (duplex, neurogenic bladder, UPJ, VUR, valves); bladder wall and stream place the level (s35 Q2) | bs-puv | New |
| C3 | Lab grid | Nine causes of hypokalemia, each in one cell of potassium by acid-base by blood pressure; one cell fits (s35 Q4) | bs-distal-rta | New |
| C4 | One noun, a series of steps | Leukocyte adhesion, chemotaxis, degranulation, killing, plus marrow infiltration; two options map to one disease, so neither can be the key (s35 Q11) | cgd | Extends A1 |
| C5 | Treatment-of-a-mimic menu | Bracing and spica (DDH), traction (fracture), therapy (sprain) against fixation for SCFE (s35 Q6); tear-duct massage, amoxicillin, steroid and decongestant drops against warm compresses (s35 Q9); treatments paired with routes for vulvovaginitis (s31 Q11) | scfe; bs-eyelid-lump; diaper-dermatitis | New |
| C6 | Age-gate ladder | Four real vaccines each given at the wrong age for a 4-month-old (s35 Q3); only one of the vaccines actually due is listed | bs-adolescent-vax | New |
| C7 | Whole routine schedule plus one travel vaccine | Nine vaccines, eight routine and typhoid (s35 Q12) | bs-exanthems | New |
| C8 | Umbrella key | "Pulmonary stenosis" for a physiologic peripheral pulmonary stenosis murmur (s35 Q5); "polycystic kidney disease" with no inheritance (s35 Q8); "enzyme deficiency" for G6PD (s31 Q5) | ped-murmur; bs-abdominal-mass; neonatal-jaundice | New |
| C9 | The common real answer is left off | Nonclassic CAH absent from a virilization list (s35 Q1); asthma and CF absent in the AATD item, solved by eliminating four rare disorders (s35 Q10) | precocious-puberty; asthma-copd | New |
| C10 | A disease under a formal, older or histologic name | Kawasaki as mucocutaneous lymph node syndrome (s31); Wilms as nephroblastoma (s31 Q22, s35 Q8); Bartter as juxtaglomerular cell hyperplasia (s35 Q4); Sertoli-Leydig tumor as "ovarian adenoma" (s35 Q1) | arf; bs-abdominal-mass; bs-distal-rta; precocious-puberty | In block; s35 adds the histologic-name form |
| C11 | A decoy shares a name with a disease that would fit | Fanconi syndrome among marrow failures (s31 Q1) | cgd | In block |
| C12 | Key and decoy differ by one word | Chromosome 15 deletion, maternal versus paternal (s31 Q13) | bs-imprinting | In block |
| C13 | The organism asked as a class | Spirochete, obligate intracellular bacterium, gram-negative diplococcus (s31 Q24) | bs-genital-ulcer | In block |
| C14 | Option list mixes kinds | Organism pneumonias beside heart failure and tuberculosis (s35 Q7); virus, bacteria and a parasite for neonatal encephalitis (s31 Q7) | mycoplasma; bs-torch | New |
| C15 | The key is a procedure or a way of measuring | Split-urine protein; BP by auscultation (s31 Q25, Q19); NAAT written out with genus and species (s31 Q27) | bs-isolated-proteinuria; bs-adolescent-bp; cervicitis | In block |
| C16 | Wrong-organ or wrong-test imaging | CT of the head or liver and sweat chloride for congenital hypothyroidism (s31 Q15); abdominal CT and bone scan against marrow aspiration (s31 Q20) | bs-umbilical; bs-leukemia | New |
| C17 | Development as a grid | Delayed or normal rows across three domains (s31 Q3) | growth | In block |
| C18 | Same virus, two options | Chickenpox and shingles (s35 Q3) | bs-adolescent-vax | New |

## D. About the explanations

| # | Pattern | Example | Brief | Status |
|---|---|---|---|---|
| D1 | A definition or schedule may be dated | Adolescent BP at the 95th percentile (s31 Q19); zoster from 60 (now 50) (s35 Q3); pneumococcal from 65 (now 50) (s35 Q12) | bs-adolescent-bp; bs-adolescent-vax; bs-exanthems | In block (BP); s35 adds two vaccine ages |
| D2 | The explanation describes a different entity from the stem | Valvar PS explained for a physiologic PPS stem (s35 Q5); measles explained for a rubella-like stem (s35 Q12); holosystolic LLSB murmur explained for a TOF ejection murmur (s31 Q4) | ped-murmur; bs-exanthems; cyanotic-chd | New |
| D3 | The explanation carries a factual error | Zona reticularis "in the medulla" and the wrong CYP17 activity (s35 Q1); JG hyperplasia "causes hypertension" (s35 Q4); "downturned" Down fissures (s34 Q1); magnesium "no role" in PTH (s34 Q2) | precocious-puberty; bs-distal-rta; teratogens; bs-fat-soluble-vitamins | New (process rule, not a page line) |

## Candidates for new block lines (most reusable first)

1. C5 treatment-of-a-mimic menu (s35 Q6, Q9; s31 Q11).
2. B3 negatives placed to close one decoy each, with B4 as its mirror (s35 Q4, Q7, Q8, Q12; s31 Q27).
3. C1/C2 same-noun or same-organ family separated by location or level (s35 Q1, Q2).
4. C3 lab grid, with A2 lead-in on a secondary finding (s35 Q4).
5. C8/C9 umbrella key and the missing common answer (s35 Q1, Q5, Q8, Q10; s31 Q5).
6. B1 finding described but never named (s35 Q6, Q9, Q11; s31 Q6, Q10).
7. A3 prevention lead-in that skips the diagnosis, with C7 schedule list (s35 Q12).
8. C6 age-gate ladder with B12 date cue (s35 Q3; bs-adolescent-vax).
9. B6 clue in a relative (s35 Q11; s31 Q14).
10. D2 as a reader note: when the explanation and the stem disagree, the stem sets the facts.
