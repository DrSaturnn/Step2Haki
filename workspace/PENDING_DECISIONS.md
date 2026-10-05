# Questions waiting on you

A running list, updated each pass. Newest at the top of each section. Answer any in a line ("VUR: yes", "thumbnail: go") and I'll act on it.

## Decided 2026-10-03 (Jonathan: "I trust your decision for the remaining pending decisions")

Already resolved by earlier passes: precocious-puberty title (s73 merge "Puberty", with its own virilization section; the NBME item sits in its framing block); Bartter item (brief retitled "Hypokalemia and Acid-Base Disorders in a Child" in s66; item stays as the contrast case); cgd retitle ("Neutrophil Disorders: Number and Function", s66); "GI Bleeding in a Child" (s66); "The Distended Abdomen in a Newborn or Infant" kept.

Decisions batch shipped in s82 (2026-10-04): HIV rekey, HPV distractor, workflow text, 17 blueprint rows (3 retagged), spelling pass in questions, sidebar at 1100 px; VUR in s81. Traplines and the label needed no change. Still open: thumbnail pilot, hot-joint exception, audit items 10 to 14 (after the merge queue).

Decisions, to be carried out in a "decisions" batch between merge batches (status in OPEN_WORK.md):
- **HIV cervical screening item:** rekey to "Begin at 21 as usual" (HHS OI guideline 2024 and ASCCP 2026 are the current guidelines; current guidelines set facts). Reissue the item; keep the CDC STI wording only as a labeled note.
- **HPV distractor:** replace "Complete a three-dose series" with "Restart the series".
- **Trapline separator:** "Option: why" (colon) page-wide; no em dashes.
- **"Trap autopsy" label:** "Why the distractors fail" page-wide.
- **Non-GI internal workflow text:** mechanical pass now: drop "Verified:", "Candidate twin", batch and ledger notes; "Store the discriminator as a question" becomes "Ask:"; "owns" becomes "covers"; resolve "not yet written" (rmsf).
- **NBME plan defaults:** keep as built.
- **Blueprint judgment rows (17):** Claude reviews and retags them in the decisions batch, logging each change.
- **VUR corrections:** yes; write them from AUA and AAP sources opened that day (grade wording, ultrasound-gated VCUG item, prophylaxis and RIVUR).
- **Thumbnail pilot:** not now; revisit after the merge queue.
- **Short stature flowchart, precocious branch:** keep standard teaching.
- **British spelling inside questions:** yes, a spelling-only pass that keeps question ids (keys included only if the tooling can do it without reissuing; otherwise leave keys and fix prose).
- **Table squeeze at 1000 to 1100 px:** yes, collapse the sidebar at that width.
- **Hot joint, unstable patient:** add the exception only with a guideline quote (IDSA or equivalent) opened that day; otherwise leave the rule.
- **Open audit items 10 to 14:** after the merge queue, in that order.

## Earlier questions (decided above; kept for history)

- **Rekey the HIV cervical screening item? (2026-10-03, s65).** bs-cervical-gate item q_259e3ccc6f015dcc8656 (18 yo F newly diagnosed with HIV) keys "Screen now". The HHS adult and adolescent OI guideline (updated July 2024) and ASCCP (Feb 2026) start screening at 21 even with HIV; the CDC 2021 STI guideline still says 1 year after sexual debut, no later than 21. s65 changed the prose to state both. Options: rekey to "Begin at 21 as usual" (its current distractor; version bump), or keep the CDC STI key and label it.
- **HPV item distractor (2026-10-03, s65 review).** hpv item q_b8bb12655d3f5058984f keys "Repeat the second dose" (second dose 4 months after the first) with "Complete a three-dose series" as a distractor; repeating the dose is a third dose, so the distractor reads as also correct. Suggest replacing that distractor (for example "Restart the series").

- **precocious-puberty title fit (2026-09-25, s35).** The s35 NBME item is a 10-year-old girl with virilization from an adrenal tumor (q_a2533eb69947cf65b1ad); at 10 her pubic hair is not precocious, so "Precocious Puberty" only loosely covers it. Options: keep; retitle (for example "Early Puberty and Virilization"); or move the virilization content to its own brief.
- **Bartter item under "Hypokalemia with Acidosis in a Child" (2026-09-25, s35).** bs-distal-rta carries q_47cd4f715eae70ba65e1 (2-year-old, hypokalemic metabolic alkalosis, keyed Bartter syndrome), which contradicts the brief's title. Options: keep it as the contrast item; retitle the brief (for example "Hypokalemia in a Child: Reading the Acid-Base and Blood Pressure"); or move the item to a separate alkalosis brief.

- **Trapline separator, page-wide (2026-09-24, s29/s30).** Traplines use the skill's "Option — why" form; the voice rules allow an em dash only after a bold term. GI traplines were kept as they are, except peds-constipation and the cholestasis distractor block, which now use a colon. Choose one for the whole page: keep "Option — why", or switch every trapline to "Option: why".
- **"Trap autopsy" label (2026-09-24, s29).** Renamed to "Why the distractors fail" in the GI section only (cholestasis). It is a house label from the management-brief skill. Rename it page-wide, or restore it in GI?
- **Scope of the non-GI internal-text cleanup (2026-09-24, s29).** Outside GI the page still shows workflow text in 115 briefs: "Store the discriminator as a question" (57), "Verified:" (17), "Candidate twin — confirm:" (5), "not yet written" (1, rmsf), "takes over" (3), "owns" (214), and batch or ledger notes in 10 briefs (e.g. myositis-ossificans, abpa, febrile-seizure). Options: a mechanical pass now (drop the markers, "Ask:" for the discriminator phrase, "covers" for "owns"), or fold it into each section's voice pass.

- **NBME plan defaults in use (NBME phases 1-6).** Built with: fingerprint ids when no form number is given; badge reads Board, UWorld or Aquifer; NBME chip and filter shown; NBME tag shown after a question is answered; one-line framing note for matched questions; Pediatrics and FM weights; misses logged for UWorld and NBME; s28 RMSF questions kept. Say which to change.
- **Blueprint judgment rows.** 17 briefs marked "review" in `repair/nbme/blueprint_map.csv` (for example abuse coded Multisystem, tics coded Behavioral, vitamins coded Multisystem). Spot-check and I'll retag.
- **Form numbers.** If you send "Peds CMS <form>, #<item>" with future NBME questions, ids become readable and cross-form repeats are caught exactly.
- **Retitle cgd?** "Recurrent Abscesses and Granulomas" now also holds low-neutrophil-count disorders. Option: "Neutrophil Disorders: Number and Function". *s28.*
0. **Retitled this pass (reversible):** "The Distended Newborn Abdomen" is now "The Distended Abdomen in a Newborn or Infant" (the malrotation question is a 7-month-old). Say "revert" if you prefer the old title. *s26.*
1. **VUR corrections (researched, not yet written).** Change the grade wording to "mild I–II, dilating III–V" (blunting starts at III, complete at IV; V adds tortuous ureter). Replace the item where a 2-year-old with a normal ultrasound gets a VCUG with a child under 2 whose ultrasound is abnormal. Add the AUA prophylaxis rules and the RIVUR result (prophylaxis halves repeat UTIs, no change in scarring). *Asked s23.*
2. **Thumbnail pilot.** Build one recreated figure (short stature evaluation flowchart) as a small preview on its tile that opens full size on click, for your review before rolling it out. *Asked s23.*
3. **Short stature flowchart: precocious puberty branch.** My notes filed it under "impaired velocity + advanced bone age"; the page keeps standard teaching (fast growth now, short adult height). Confirm against the UWorld figure. *Asked s23.*
4. **Rename "Occult GI Bleeding in a Child"** to "GI Bleeding in a Child: Meckel and Mimics", since it now carries visible-bleeding questions. *Asked s24.*
5. **British spelling inside existing questions** (e.g. "Giant cell tumour of bone", "anaemia"). A spelling-only pass that leaves question tracking unchanged. *Asked s24.*
6. **Table squeeze at 1000–1100 px wide.** Proposal: collapse the sidebar at that width. *Asked s18.*

## Waiting on material from you

- **Aquifer case narratives for Pediatrics 10, Neurology 10, Pediatrics 29, Pediatrics 31.** (2026-10-03: Pediatrics 10, Neurology 10 and Pediatrics 31 also unlock folding those cases into their topic briefs as collapsed case sections.) Only the summaries came through, so each new workup brief's source case is marked partial and the case question stems are reconstructed. Neurology 10's summary never names the tumor (the content points to a posterior fossa tumor, likely pilocytic astrocytoma); the brief keys "posterior fossa tumor" until the narrative confirms it. *s27.*
7. **s23 UWorld text** (apnea of prematurity, galactosemia, hereditary angioedema, Wilson). The full explanations were lost from the session; re-pasting lets me check cutoffs and swap in UWorld's real wrong answers for Wilson and angioedema. *s23.*
8. **Aquifer credit for bs-puv and bs-leukemia.** You said you'd send updated cases. *Held.*
9. **Peds 21 case narrative.** You said you'd send it. *Held.*

## Open audit items (my list; your call on priority)


10. (deferred 2026-10-05; recommended as lean rewrites of the 66 briefs instead of a table audit) **Scope and source audit** of the s18 workup tables: trim specialist rows, flag memory-sourced numbers.
11. (done s104; cervical ASC-US in s96) **s18 conflicts:** bs-puv VCUG vs cystoscopy; enuresis age gate; SCFE effusion claim; newborn-cyanosis items; DVT duration; cervical ASC-US; bs-torch confirmation after 3 weeks; empty trap labels; stray ⚠︎.
12. (done s102) **RSV isolation wording** (UWorld table says contact only; the library says many respiratory viruses need contact plus droplet).
13. (done s104) **Two older weak-distractor items** (angina with LBBB; dipstick mismatch).
14. (done s104: SSC 2021 'should not delay antibiotics 45 minutes or more' in suspected sepsis; joint-specific guidelines give no exception) **Hot joint: antibiotics before aspiration when unstable?** The merged brief keeps the old rule (no antibiotics before the fluid is sampled). The reviewer suggested an exception for an unstable or septic patient, or delayed aspiration (blood cultures, then antibiotics). Not in the old briefs; needs a source before it is added.

## From s90 (merge batch 10; Claude's notes, your call)

- (done s99) q_0053 key typo fixed to "5 years after diagnosis"; formatting only, stats kept.
- Thyroid: the PTU-in-first-trimester line is labeled ATA 2017; the 2026 ATA pregnancy guideline (Korevaar, Thyroid 2026;36(5):481-544) antithyroid-drug section (G) could not be opened. Recheck when a full text is available.
- Diabetes: the retinopathy schedule quotes ADA Standards 2022 section 12 (2024 to 2026 pages returned 403); the USPSTF CKD screening page is marked inactive.

## From s91 (merge batch 11; Claude's notes, your call)

- The CDC child schedule status (January 2026 revision stayed March 16, 2026; HHS appeal argued October 6, 2026) decides several HPV and childhood keys (q_06ed, q_652e, q_88f8, q_b8bb). Recheck after the First Circuit rules.
- Vaccines in Pregnancy: COVID-19 shows a ⚠︎ because CDC's pregnancy table says "No guidance/not applicable" while the 2026-27 COVID guidance recommends vaccine for all adults. The anti-D line "without recent anti-D" also carries ⚠︎ (no source opened).
- Childhood Vaccine Schedule and Contraindications has 11 questions, below the 12 to 18 aim; add one or two when convenient.

## From s98 (source pass; Claude's notes, your call)

- Thyroid PTU line still cites ATA 2017; the 2026 ATA section G remained unreachable (publisher and PMC blocked). Recheck when a full text is available.
- ADA Standards 2026 section 12 still returns 403; eye-exam lines are proved against ADA 2022 (same wording in a 2024 copy).
- Vaccines in Pregnancy: COVID-19 stays flagged (CDC pregnancy table: no guidance; CDC 2026-27 adult guidance: all adults; CDC pregnancy page: individual decision making for 2025-26). ACOG pages returned 402.
- Several author-written distractor dismissals were cut because no source supported them (preg-vax, adolescent-aub, bs-neonatal-sepsis); the keys are still explained. Add sourced dismissals later if wanted.
- bs-neonatal-sepsis: the open-fontanelle mechanism sentence in Management is supported only as "not necessary to routinely do CT before lumbar puncture in young children" (Merck); left as is.
- mdd says "about 6 more months (4 to 9)"; VA/DoD says "at least six months". Kept "about" in both briefs for consistency with the 4 to 9 range.

## From s99 (source pass 2; Claude's notes)

- Medscape is the only source found for two drug-hemolysis lines (Mycoplasma cold agglutinins positive after 7 to 10 days; splenectomy ideally after age 6); StatPearls, Merck and the BSH guideline (blocked) give no timing.
- Neonatal mastitis rests on two journal abstracts (no tertiary source reachable).
- ig-panel keeps its `&mdash;` separators: the page script columnize() consumes them (they are not displayed).

## From s100-s102 (source passes 3-5; Claude's notes)

- Two items retired as unprovable or ambiguous (q_15fe polycythemia mechanism; q_bea2 PPHN screen item, replaced). Both are in tools/retired_items.csv with archives.
- Some lines rest on a single journal abstract, Medscape, Merck Consumer or a Cureus review where society guidelines were blocked (ledgers say which): neonatal mastitis, GTPS refractory step, Mycoplasma cold-agglutinin timing.
- Acronym write-outs and em dashes (&mdash; separators, ~1,300 on the page) were found in many briefs by auditors; a page-wide em dash pass follows (s103).
- rmsf dengue item stem is 52 words (over the 40-word stem rule); not changed.
- Transfusion items q_1c2e and q_53f5 had no sex in the stem; one was chosen (no fact depends on it), noted in the ledger.
