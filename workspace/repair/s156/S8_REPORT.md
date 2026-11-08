**s156 final report: Phase 2, infectious disease B, pediatric (7 briefs)**
Bacterial Meningitis, Childhood Vaccine Schedule and Contraindications (lookup), Lymphadenopathy, Oral Lesions in a Child, Deep Neck Infections, Fever and Rash in a Child, Fever in an Infant. All seven READY (verify_all); gate PASS, 0 failures; render PASS; squeeze 0; pointers 48 checked, 0 problems. Presented as approval s156, page bfcc9ac56427.

**1. Decisions needed**
None. Your four parked recommendations (S156.md "Parked recommendations": repeat audit of the cap overages, the site-wide en dash patch, restemming the lymphadenitis adult items, the lanes .gitignore and resume.py fix) stay parked and unapplied.

**2. Calls made under section 3** (reply with the reversal to undo any)
1. Meningitis "hearing loss is the most common sequela in children" restored in S6. S5 had dropped it as unranked, but AnKing card 1513118547774's own question asks for the most common sequela; new quote c22q. This reverses my S5 verdict. Reverse: "use the screen-for wording".
2. Lymphadenopathy: a supraclavicular node with a normal CBC and chest film is not sent to biopsy on site alone. No source in the packet or the card index gives that rule (a06 ranks it higher risk; a11 gives the biopsy triggers). No bank item tests it. Reverse: "add supraclavicular as a biopsy trigger" (it would carry an unverified mark).
3. Lymphadenopathy round 1 adjudication reversed in round 2: I had assumed a Source vignette in the tail for the trapline referents; there is none, so each trap line now states its own facts.
4. Fever and Rash: post-exposure MMR "within 5 days" in the body and bank (AnKing, UWorld); MSD/CDC "3, possibly up to 5" stays in the hover. Reverse: "use 3 to 5 in the bank".
5. Fever in an Infant: the board 28-day rule (tap every neonate) stays the rule; the 2021 AAP guideline for well 8 to 60 day infants sits in an In practice hover that says it narrows the rule.
6. Word totals over the soft cap are reported, nothing cut (STANDING "Layers, not totals"; your 2026-10-29 "Trim only true repeats").
7. Trap labels (Salient decoy, Sequencing trap and the rest) kept as the site pattern; the Treatment by cause table inside a hub's Workup kept (DIGEST s148).
8. Meningitis Gram stain result labels keep the morphology (gram-negative diplococci); antigen and AFB labels now read "Positive" so they do not name the masked test.
9. Tool fixes: review_packet (block labels end their line; "[end of Bottom line]" marker; drawer buttons written as "[drawer: id]"); basepage.pending skips a shell whose id is already on the page as an alias (the s159 antidep-other retirement broke every verify); lint ACTION verbs gain secure, intubate, laryngoscopy; verify_all's default parallelism follows the core count (three jsdom renders on two cores timed out at 90 s in this chat's first S8 run).

**3. Edit list per brief** (S5 and S6 changes on the S3 build; new facts with quote, source, tier)

*Bacterial Meningitis*
- Step 2 deferral trigger "Hypotension or poor perfusion" -> "Hypotension or shock (cardiorespiratory compromise, most often in young infants)" (c18, i07), so mottling with a stable circulation no longer defers the tap, in line with the UWorld item.
- New: "ceftriaxone covers meningococcus and other gram-negatives; vancomycin is added for cephalosporin-resistant pneumococcus" (c11b, c77: AnKing, board).
- New: "hearing loss is the most common sequela in children; sensorineural loss is most common after pneumococcal meningitis" (c22q, c22: AnKing card question and answer, board).
- Viral row "well-appearing child" dropped (unsourced).
- Mask leaks: rung tag "Dexamethasone" -> "Adjunct"; antigen and AFB results -> "Positive"; rungs 1 and 2 tagged "Neonate" / "Child or adult".
- Eight hedges restored (gram-negative rods elderly only; Listeria also in pregnancy or immunocompromise; "most often").
- Rejected: immunocompromise in the step 2 CT row (step 4 owns it); hedging the Hib vs pneumococcal dexamethasone line (AnKing gives both unhedged).

*Childhood Vaccine Schedule and Contraindications (lookup)*
- Neither row: "an uncomplicated seizure in the first 3 days" (c05, c07), also in the pause point and an item reason.
- Moderate or severe illness hover: "an acute illness, with or without fever, that defers the dose; a fever over 39 C or a severe illness without fever is a clear reason to delay, while a cold, even with low fever, is not" (d04, o09, o03).
- "No closing window" (unsourced) -> "If this dose slips to 4 years or older, at least 6 months after the third, no fifth dose is needed" (d14: MSD, primary).
- Acellular pertussis now cites d13, purified components (MSD, primary).
- Mask leaks: hover "Why intussusception" -> "Why the early cutoff"; caption -> "Common histories at a vaccine visit".
- RV1/RV5 spelled out; live-vaccine bars no longer read as the whole list; oral polio "no longer used in the United States".

*Lymphadenopathy*
- Laryngocele item and note sourced (g01, g02: MSD Laryngoceles, primary): "often in wind-instrument players" (glassblowers dropped).
- q_0d12bf92 restemmed to a community where MRSA is uncommon so only cefdinir misses (v2); q_edcb24a1 node 1.5 cm, "observe and recheck in 10 to 14 days" (v2).
- Observe row stated: one node under 2 cm, soft, mobile, not red, not exquisitely tender, afebrile (c12, a01).
- Cat-scratch: node "within 2 weeks" (b02), "proximal to it, on its drainage path" (N03); "upstream" -> "draining".
- Malignancy flags get a CBC and chest film (l03); biopsy for firm, immobile, enlarging or longer than six weeks (a11), in the Bottom line and both tree branches.
- Pearl: a cephalosporin "that misses MRSA and oral anaerobes can fail".
- Trap lines rewritten to stand alone; mononucleosis pointer to Respiratory Infection removed (that brief does not teach it).

*Oral Lesions in a Child*
- Rehydration has one owner (step 4): mild or moderate, small frequent oral amounts even if unwilling (d02, d04); severe with circulatory compromise, IV (d01). q_43576922 stem adds HR 160, cool hands, refill 4 s so its IV key meets d01 (v2).
- Pearl: "Front of the mouth (gums, tongue, lips) is herpes; back (soft palate, uvula, tonsillar pillars) is coxsackie", scoped to herpangina vs gingivostomatitis; two stems say "tonsillar pillars" (v3).
- SCID thrush row: c27 now quotes the card's answer (AnKing, board).
- Cyclic neutropenia "well in between" dropped; "Neutropenia during a bout" (n03). Seven hedges restored.

*Deep Neck Infections*
- Imaging rule has one owner (step 5): exam limited, diagnosis in doubt, deep neck spread (p14, c08, a09).
- Step 7 gains rungs: Epiglottitis "Airway in the operating room; then antibiotics" and Lemierre "Prolonged antibiotics covering anaerobes, 2 to 6 weeks" (rl6, rl7, rl8: Eilbert and Singla, Int J Emerg Med 2013, primary).
- Stridor not improving with racemic epinephrine: "Less likely croup: think epiglottitis or a deep neck abscess".
- Age hedges restored (retropharyngeal "less common after age 5"; adult route via foreign body or instrumentation).
- Epiglottitis next step: "Secure the airway in the operating room, where laryngoscopy confirms it; no tongue depressor."
- Mask leaks: zone label -> "Bulge and shifted uvula on the exam"; rung tag -> "Drooling or stridor".

*Fever and Rash in a Child*
- Aplastic crisis clue: "Sickle cell disease or hereditary spherocytosis with sudden pallor" (x08, c17), no rash order implied.
- Clue table next step: "Isolate with airborne precautions if measles is possible; order rubella IgM serology" (x05, r02, r21); MMR prevention moved to the rubella treatment row.
- q_67ed571f explanation "within 5 days of exposure"; q_42c50944 stem no longer names varicella twice (v2).
- "Nonimmune and either immunocompromised or pregnant"; Lyme "the knee most of all"; IgA vasculitis and ASO spelled out.

*Fever in an Infant*
- 2021 guideline hover labelled as narrowing the 28-day rule; "the Aquifer case".
- Underimmunized hover sourced to one MSD sentence (f31, primary): fever over 39 C, no source, white count 15,000 or more, pending blood and urine cultures.
- Bottom line adds "plus a lumbar puncture under 3 months" (f07); ill appearance as the fourth acyclovir trigger (f05).
- Gingivostomatitis "Usually 6 months to 5 years" (c27: AnKing, board), matching Oral Lesions.
- Result labels no longer name the masked test; eleven hedges restored.

**4. Word count** (above the bank, hover text included)
Meningitis 1425, dtap 1183, lymphadenitis 1119, herpangina 877, bs-pta 1573, bs-fever-rash-arthralgia 1624, aq-infant-fever 1309. Over the 1,300 soft cap: meningitis, bs-pta, bs-fever-rash-arthralgia, aq-infant-fever. No cuts (parked recommendation 1).

**5. Reviews**
- Round 1 (8 agents incl. one relaunch, 107 calls, 6.71M): 0 HIGH, 51 MED (s155 39, s153 48). Every brief needed S5.
- Round 2 (7 agents, 76 calls, 3.99M): acc and flags PASS on six, PASS-IF on lymphadenitis (LOWs); read PASS aq-infant-fever, PASS-IF five, FAIL lymphadenitis (2 MED: trap lines pointing at a vignette not on the page, which my round 1 adjudication caused; two biopsy conditions).
- Rounds 3 and 4 (5 agents, 42 calls, 1.23M): all PASS (read lymphadenitis PASS-IF, 2 LOWs applied exactly).
- Packet errors (not counted against briefs): fused NBME label and stem age ("question 14-month-old"), Bottom line boundary, drawer buttons dropped. About eight read findings came from them; all fixed in review_packet.
- Sonnet vs Opus: flags (Sonnet) found accuracy MEDs that acc (Opus) passed: dtap 39 C hover and "No closing window", bs-pta Lemierre action and hardened age hedges, meningitis's three unsourced claims, lymphadenitis biopsy routing, herpangina IV trigger. Acc found what Sonnet missed: the lymphadenitis laryngocele, two-answer item, missing observe branch and cat-scratch timing; bs-fever-rash 3-to-5 days and aplastic timing; the meningitis deferral trigger against UWorld; the herpangina SCID quote. Read (Sonnet) carried most packet false findings and missed the lymphadenitis referent problem in round 1.

**6. Cost**
- Wave: 27 agents, 663 calls, 70.02M of 78M. Builders (Opus) 7 agents, 438 calls, 58.10M; acc (Opus) 8, 102, 4.68M; flags (Sonnet) 6, 62, 3.89M; read (Sonnet) 6, 61, 3.35M. Reviewers 11.92M.
- Lead: 83.3M measured of 90M (three recorded chat rows 74.9M, this chat about 8.4M; the other chats ran in containers reclaimed before the ledger ran) (7 chats; start-up context about 130k each).
- Batch total: about 153M measured (wave 70.0M plus lead 83.3M).
- Per brief: about 10.0M wave (8.3M build, 1.7M review) plus about 11.9M lead.
- Proposed next batch (7 briefs): wave 78M (builders 60M, reviewers 14M, 4M reserve), lead 90M.

Reply "ship" to publish, or name what to change.
