# s34 NBME intake table (Pediatrics CMS, form and item numbers not given)

Source: repair/sources/s34_questions.md (local-only; pulled from the pasted chat message by script, not retyped). This file paraphrases. 3 items: 1 correct, 2 incorrect. Fingerprints use the same method as s31 (see nbme-intake section 2). No fingerprint or key matched an existing coverage.csv row.

| Q | nbme_id | fingerprint | key | task | result | time | same_as | owner (nbme_match top candidate, confirmed by reading) |
|---|---|---|---|---|---|---|---|---|
| 1 | peds-cms-8e3e76 | 8e3e76654e | Fetal alcohol syndrome | dx | correct | 0:51 |  | teratogens (0.181; closest item q_72958560a14350fc9ef7 keys FAS from the face) |
| 2 | peds-cms-acdeb0 | acdeb09151 | Alkaline phosphatase activity | lab direction (found) | incorrect | 0:25 |  | bs-fat-soluble-vitamins (rank 3, 0.079; item q_f2bd6151932e23a717e6 keys 25-hydroxyvitamin D); liver-preg and bs-nat-fracture ranked higher on word overlap only |
| 3 | peds-cms-b095ba | b095bad2fb | Increased platelet destruction | mechanism (found) | incorrect | 0:25 |  | aq-bruising (keyword search; ITP dx item and differential); nbme_match ranked factor-inhibitor, bs-leukemia, preop, anemia-thrombocytopenia |
