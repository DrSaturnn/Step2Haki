# Questions waiting on you

A running list, updated each pass. Newest at the top of each section. Answer any in a line ("VUR: yes", "thumbnail: go") and I'll act on it.

## Awaiting a yes/no

- **bs-impaction vignette contradicts the brief (2026-09-24, s30).** The vignette (77 yo F, empty rectal vault, prior laparotomy) describes adhesive small bowel obstruction: it matches bank item q_3d6cc290365e594cb0a9, one of the distractor variants. The brief teaches fecal impaction (firm stool in the vault, last movement 5 days ago that was loose, oxybutynin, warm dry skin). No local source exists: the brief has no nid and predates `repair/sources/`. Options: (a) rebuild the vignette from the brief's own facts and mark it `data-recon="partial"`; (b) you supply the original question and I rebuild it from that.
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

- **Aquifer case narratives for Pediatrics 10, Neurology 10, Pediatrics 29, Pediatrics 31.** Only the summaries came through, so each new workup brief's source case is marked partial and the case question stems are reconstructed. Neurology 10's summary never names the tumor (the content points to a posterior fossa tumor, likely pilocytic astrocytoma); the brief keys "posterior fossa tumor" until the narrative confirms it. *s27.*
7. **s23 UWorld text** (apnea of prematurity, galactosemia, hereditary angioedema, Wilson). The full explanations were lost from the session; re-pasting lets me check cutoffs and swap in UWorld's real wrong answers for Wilson and angioedema. *s23.*
8. **Aquifer credit for bs-puv and bs-leukemia.** You said you'd send updated cases. *Held.*
9. **Peds 21 case narrative.** You said you'd send it. *Held.*

## Open audit items (my list; your call on priority)

- **peds-headache-imaging vignette mismatch:** the vignette is a 10-year-old boy but the decision point argues an adolescent girl after menarche (already on the s18 list; flagged again). *s26.*

10. **Scope and source audit** of the s18 workup tables: trim specialist rows, flag memory-sourced numbers.
11. **s18 conflicts:** bs-puv VCUG vs cystoscopy; enuresis age gate; SCFE effusion claim; newborn-cyanosis items; DVT duration; cervical ASC-US; sellar-mass and peds-headache vignette mismatches; bs-torch confirmation after 3 weeks; empty trap labels; stray ⚠︎.
12. **RSV isolation wording** (UWorld table says contact only; the library says many respiratory viruses need contact plus droplet).
13. **Two older weak-distractor items** (angina with LBBB; dipstick mismatch).
