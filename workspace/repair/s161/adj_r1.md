# s161 S5 adjudication, round 1 (lead, chat 3, 2026-11-02)

Receipts: repair/migration/spine/reviews/<card>_<part>_rN.md (mood-anticonv acc r6, read r6, flags r5; the other four
cards r1). "Rn" = the receipt's replacement n; "Fn" = finding n. Survey local/s161/survey_r1.md (local/s161/chat3/survey.py).
Pair files local/s161/chat3/<card>_p*.py, applied with local/s160/chat4/ed.py; every card rebuilt with
`AX_BATCH=s161 build_brief.py <folder> --verify`: MECHANICAL PASS, 0 FIX, 0 warn, disp unresolved none.

Precedents applied (S159 adj_r1, S160 adj_r1): the Key point is blurred whole in study mode (div.dp), so a Key point
naming a masked answer is not a leak; study mode is progressive recall, the clue stays visible and the test is masked
(STANDING, Study mode); a Why cell that repeats its masked Check is a leak; a danger-row commit is prevention (CARD_SPEC 4).

## Rejected (with evidence)
- mood-anticonv read F7 (Key point gives the masked actions): Key point blurred whole (S159 precedent; CARD_SPEC 2 asks
  for the action in the Key point).
- pc-ssri read F3 (NBME Deciding clues name the stop): the Setup lines already show the stop unmasked; the clue is the
  visible half of progressive recall, the answer (discontinuation syndrome) stays masked (STANDING Study mode).
- pc-cog read F10 capitalization: lowercase lcw "Why/Shows" lines are the site pattern on every card (pc-ssri, pc-maoi);
  only the fragment fixed. pc-cog read F11 ("rivastigmine label only"): "only" would assert the donepezil label is silent,
  not in the packet; kept as the source tag. pc-cog read F5 (Uses vs dementia): kept; the Uses lines are class uses, the
  hallucination decision stays with dementia (owners row). pc-cog read F6: owners confirmed by grepbrief.py (parkinson:
  "Parkinson disease dementia: consider a cholinesterase inhibitor or memantine"; tca-tox: physostigmine contraindicated
  in tricyclic poisoning; toxidrome: organophosphate poisoning, atropine then pralidoxime).
- pc-other read F10 (insulin Result): the Result states no direction ("may change"); the masked Rule holds the direction.
  pc-other read F9 hover "In practiceIn practice": the site's hover label plus title pattern (as on pc-ssri).
- mood-anticonv read F9, the "or ... (nephrogenic)" half: lint alias needs the AVP name with "(nephrogenic)" at first
  mention (rebuilt warn); the list fix stands ("mild thyroid dysfunction" removed).
- mood-anticonv acc F3 (lamotrigine "In practice:" hover): not added (lead default from chat 1 kept); the board rule is
  UWorld's, and the item's 3-week gap gives the same answer under the label. Record only.

## Accepted (applied in chat 3)
mood-anticonv: acc R1 (commit tied to "which result is abnormal"); acc F2 (cards_disposition reason, disp.py); flags R1
  (speech dysfunction); read F1 (chips "Lithium Therapy": LIB label); F2 (row "Carbamazepine in Asian ancestry", allele not
  named in the finding); F3 (row "Confusion on valproate"; note "Once confirmed: stop valproate and look for an underlying
  urea cycle disorder"); F4 ("resolves after the cause is removed"); F5 (Monitoring Why cells no longer name the masked
  test: valproate, carbamazepine before and during, oxcarbazepine "An adverse effect in about 2.5%" (w01), and topiramate
  "Its acid-base label warning", the same pattern though unflagged); F6 (NBME Deciding "point to its toxicity"; danger
  finding drops the 6-month window, which the chart holds: F8 in part); F9 (list); F10 ("Faster valproate clearance" in
  the Result so the masked "Its level falls" has one referent: lint mask-leak blocked "Valproate level falls"; DRESS note
  "Eosinophilia is often present (lamotrigine label)").
pc-ssri: acc F1 (lead check, chat 2): Rule "theophylline to a third of its dose, with levels"; new fact sxT1 from the
  cached DailyMed fluvoxamine label (a6013c927ff9f6e0, 5.8 Theophylline: "its dose should be reduced to one-third of the
  usual daily maintenance dose and plasma concentrations of theophylline should be monitored"), added to author.py web.
  acc F3 (PPHN hover is a class effect). flags F1 MED: no board quote ranks the SSRIs (grep of anki and library: only
  "citalopram does have potential dose-dependent QT prolongation", "Fewest drug-drug interactions = citalopram", k03 "long
  half-life therefore no need to taper"); Key point, Citalopram and Fluoxetine rows reworded to the quotes (dose-dependent
  QT, avoided after a recent heart attack; first-trimester heart-defect signal; long half-life, so no taper): also read F9.
  flags R1 to R6; read F1 (Adverse effects line "Abrupt stop of a short half-life SSRI such as paroxetine: flu-like,
  neurologic and psychiatric symptoms within days", in1029_ss01 ss03, chip SSRI Adverse Effects; serotonin syndrome stays
  in the Interactions table with its chip, no new danger row); read F2 (mdd teaches the adequate trial and the switch,
  grepbrief: "at least 4 to 6 weeks at a therapeutic dose"): owner line "Which antidepressant, and the next step after an
  adequate trial", timeline Why "a change comes only after an adequate trial" (read F4); read F6, F7, F8 (with flags R1;
  the citalopram overdose note "may be delayed: keep the heart monitored", sx35).
pc-tca: acc R1, R2; read F1 ("GABA-A antagonism: seizures" its own line, the clomipramine hover moved with it); F2 (Why
  "Added arrhythmia risk"); F3 (chip to the Result cell); F4; F5 and the lead-found LOW (MI row): Why "Both labels warn
  about the acute recovery period" (a "contraindicated" Why would repeat the masked "Do not use").
pc-cog: flags R1 to R5 (R1 and R2 the MEDs; the drawer line now "Delirium from anticholinergic drugs"); acc F1 (pc-uv
  mark dropped on the s3 row: MSD is a primary source, CARD_SPEC 1); read F1 to F4 (Result or Why no longer names the
  masked rule or check; row 2 trigger "If that check is abnormal"), F7 (with flags R4), F8, F9, F10 fragment, F12.
pc-other: flags F1 HIGH: masked commit "an option that is not a norepinephrine-releasing sympathomimetic (phentermine,
  diethylpropion or benzphetamine)" (ak4 ak5 ph4); the bank item on the row has no such distractor. acc F1 MED
  ("uncontrolled" out of the commit and the Monitoring check; disp anchor updated); acc F2 + read F3 subtitle "wake-promoting
  and weight-loss agents · modafinil · armodafinil · phentermine · phentermine-topiramate" (shell 05 json both copies,
  make_shells.py, head_fix); flags R1 to R5; read F1 (Why cells: "Alertness may not be fully restored"; "Rules out a
  contraindication it shares with phentermine alone"); read F2 (peds-sleep owns the narcolepsy order, grepbrief:
  "Narcolepsy: Modafinil"; "Methylphenidate or an amphetamine" when wake-promoting drugs fail): Uses keeps "first line",
  the second-line clause out, AnKing 1509195119384.4179278fde now owner:peds-sleep; read F4, F6 (hedged "thought to
  raise"), F7, F8, F9; read F5 in part (Obesity Uses line adds phentermine-topiramate, qs1; no Mechanism line).

## Report items
- ssri-effects onset line ("up to 6 weeks" read as the outer limit; pc-ssri acc F2): fix belongs to the deep brief (OPEN_WORK).
- pc-ssri "Adequate trial: 6 weeks at full dose" (AnKing k04) against mdd "at least 4 to 6 weeks at a therapeutic dose":
  no exam answer differs on the logged items; flag for Jonathan, not changed.
- pc-other preflight P3: item q_c0af502ae0b80dd8c4ed distractor "Space the two doses 12 hours apart" named nowhere else.
- Tool notes: patch.py s3 needs build.py in a folder (card folders have author.py; run s3 with no folders, copy 10_ files
  by hand, squeeze by hand); git exclude lines need the workspace/ prefix (repo root is Step2Haki).
