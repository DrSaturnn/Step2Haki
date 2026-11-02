# s160 round 2: lead adjudication context

Round 1 adjudication follows (adj_r1.md), then the chat 4 lead calls on how each fix was applied, then the S6 self-check.

# s160 S5 adjudication, round 1 (lead, chat 3, 2026-11-01)

Receipts: repair/migration/spine/reviews/<card>_<part>_rN.md (acc and read and flags r1 for the four new cards; r5/r4
for adhd-meds and sud-meds), lane copies repair/efficiency/lanes/s160/r1/<part>-<A|B>/<card>/receipt.md. "Rn" below =
the receipt's replacement n; "Fn" = finding n. Survey local/s160/survey_r1.md.

Precedents applied (S159.md "S5 adjudication, round 1"): the Key point is blurred whole in study mode (div.dp), so a
Key point naming a masked answer is not a leak; a danger-row commit is prevention (CARD_SPEC section 4), management
beyond it is pointed to the owner; a Why cell that repeats its masked Check is a leak (s159 MAOI fix: "first Why line no
longer repeats the masked 2 weeks"); read cannot see study mode, so a chart "leak" needs a study-shot check first.

## Accepted (fix in chat 4)

pc-benzo
1. acc F1 (MED): long-acting withdrawal row teaches the board time first: text "About 2 days to a week after the last
   dose", bar 2 d to 7 d, cite the UWorld library fact (within 2 days) and the MSD fact; drop the hover that now repeats it.
2. acc F2 (LOW) + read F3 (MED): timeline row label "Short- and intermediate-acting withdrawal (alprazolam, lorazepam)";
   the half-life hover's "Tables differ" note unchanged.
3. flags R1, R2, R3 (LOW, hedges): apply as written.
4. read F2 (MED) older-adult drugs masked in the Monitoring row but named unmasked elsewhere: unmask nothing; reword the
   other mentions to the class hint ("a shorter-acting agent with no active metabolite") wherever the masked list is
   restated outside the Key point. Lead greps brief_text for lorazepam, oxazepam, temazepam first.
5. read F5 (MED) Uses "Insomnia" drawer -> pc-sleep "Sleep agents" (the class card for hypnotic choice); the Where line
   "Insomnia treatment" keeps peds-sleep, reworded "Whether to treat insomnia with a drug (CBT-I first)" (s159 fix 17:
   peds-sleep owns that decision).
6. read F4 (MED, ownership) partly: the danger-row commits stay (prevention: taper, flumazenil caution, older adult);
   reword the Where lines that hand those same choices away to name what the owner keeps: substance "Managing sedative
   or alcohol withdrawal once it starts"; delirium "Managing delirium". Read R-lines for F7 to F9 (LOW, stand-alone):
   apply where given.

pc-sleep
7. acc F1 (HIGH, RBD): replace with "Melatonin, acting at melatonin receptors (or clonazepam): first-line drug for rapid
   eye movement sleep behavior disorder". Source: AASM 2023 RBD guideline (Howell et al., JCSM, PMC10071384; AASM news
   page: "specific medications, such as clonazepam and immediate-release melatonin", all conditional). Fetch the PMC page
   with fetch.py, add the fact, cite it with z12; drop "such as ramelteon". If the guideline page will not fetch, drop
   "such as ramelteon" and keep z12 alone (no clonazepam). Add z12's card to cards.md / cards_disposition.json.
8. acc F2 (MED): Monitoring "Driving or skilled work" Why -> "Label: next-day impairment if under 7 to 8 hours in bed"
   citing l02 (Ambien only; see 9).
9. flags F1 (MED): apply the flags receipt replacement (adds the quoted 5 mg zolpidem dose; allowed, it is quoted);
   "7 to 8 hours" attributed to the zolpidem label only; drop "or joins another depressant".
10. read F1, F2 (MED, study mode): flumazenil and ramelteon/no Z-drug named unmasked in their own rows or other rows
    (outside the Key point): reword those mentions to class hints; the older-adult choice stated once in the danger row,
    pointed (not restated) from Monitoring.
11. read F3 (MED): Where line to peds-sleep reworded "Whether to treat insomnia with a drug (CBT-I first)"; flumazenil
    pointer to substance reworded "Managing an overdose beyond reversal". read F4 (LOW): add a pc-orexin drawer on the
    Uses line that names orexin antagonists, or a Where line "Orexin antagonists" -> pc-orexin.

pc-anxiety
12. flags R1 to R3 (LOW): apply (R3 names gabapentin, not the class).
13. read F1 (MED): Interactions row 1 Result reworded so it no longer states the masked Rule.
14. read F2 (MED): the two fragments after the pc-uv mark made whole sentences (read receipt replacements).
15. read F3 (MED): taper pointer stays on substance; add a pc-benzo "Benzodiazepines" drawer on the line comparing
    buspirone with a benzodiazepine. read LOWs with replacements: apply.

adhd-meds
16. acc F1 (MED): item q_ba15dad5e9ff27f32d26 stem "urine drug screen negative" -> "urine drug screen positive for
    amphetamine only" (item id kept; a lead stem edit, disclosed in the report); the danger-row finding line drops "; a
    urine toxicology screen sorts them".
17. flags F1 (MED): Mania row text limited to the quotes: "An episodic course points to bipolar disorder, unlike
    chronic ADHD" (k13, p11b); or cite a bipolar-mania brief fact if one quotes the symptoms (lead greps).
18. flags R2 to R9 (LOW): apply. read F1 (MED): Monitoring Why cells rewritten so none names its masked Check. read R3,
    R4, R6 (LOW): apply. read F5 resolved by flags R5 (taper or stop). acc F2 (LOW): keep (AnKing k06); report item.

pc-orexin
19. acc R1 to R3 (PASS-IF): apply ("No or low physical dependence" wording per k25; narcolepsy commit names the drug
    class the quote gives).
20. flags F1 (MED): "Each visit" -> "During treatment" on both rows. flags R2 to R7 (LOW): apply.
21. read F1 (MED): third Monitoring row Why no longer restates the Check. read R2, R3 (LOW): apply. read F4 (LOW): add
    "suicidal ideation (dose-related, label)" to Adverse effects if b7/b8 support it.

sud-meds
22. acc F1 (MED): add to Uses "Liver disease or opioid use: acamprosate preferred" (u10, UWorld); Key point naltrexone
    clause "avoid with liver disease" (board), with the label's acute hepatitis or liver failure in an "In practice:"
    hover.
23. acc F2 (LOW): naltrexone interval in the body "7 to 10 opioid-free days" (vv1, label); drop the MSD "at least 7".
24. acc F3 (LOW): nicotine replacement angina line adds the caution from w20 (serious angina, or within 2 weeks of a
    myocardial infarction). acc F4 (LOW): grep the Antabuse label in facts or the cache for "14 days"; if quoted, add an
    "In practice:" hover; else report item.
25. flags F1 (MED): extend sx2 to the whole label sentence naming methadone (cached Suboxone/buprenorphine label); if the
    label does not name methadone, drop the clause.
26. flags R2 to R8 (LOW): apply. Confirm a quote for the masked rule "Only when alternatives are inadequate" (methadone
    plus benzodiazepine boxed warning).
27. read F1 (MED): drop the Where line "Which drug for alcohol or opioid use disorder, by situation -> substance" (this
    card owns it); read F8 (LOW): overdose and naloxone pointer -> toxidrome if toxidrome owns opioid overdose (grep).
28. read F3 (MED): Monitoring Why cells rewritten as in 18. read R4, R5 (LOW): apply. read F6 (LOW): move the
    antipsych-effects chip out of the masked Rule cell into the Result cell. read F7 (LOW, QTc in a frozen item): keep;
    QTc is a standard abbreviation; add it to ABBREV.json if lint objects.

## Needs a study-mode shot before it stands (chat 4: shots.py --phone --study on the rebuilt page)
- read sud-meds F2 (chart "When each drug can start" shows masked commits): CARD_SPEC 7 masks window text; s159 read
  pc-maoi L10 was masked in study mode. Fix only if the shot shows it unmasked.
- read pc-benzo F1 (NBME Answer line and "Deciding a short half-life"): check the pc-nbq answer mask.

## Rejected
- read lanes, any "leak" in the Key point (blurred whole; precedent).
- read pc-orexin F5 (peds-sleep drawer four times): allowed by the reviewer's own call; no change.
- read pc-benzo F10 "[end of Bottom line]": a brief_text dump marker, not page text.
- acc pc-anxiety F1 (advisory): buspirone delayed onset stays as a pc-uv line; report item.
- adhd-meds read F2 (narcolepsy drug order -> peds-sleep): peds-sleep is the live owner; no pc-sleep narcolepsy content.

## Who found what
acc: the three sourcing errors with clinical weight (RBD drug, naltrexone in liver disease, a self-contradicting stem).
read: study-mode leaks (Why cells, rows) and ownership lines; acc and flags missed these (not their parts).
flags: lost hedges and unquoted clauses (about 30 LOW, 4 MED). Patch lane: 15 of 15 PASS.


# Chat 4 lead calls (S5 fixes as applied)

## Chat 4 (2026-11-01, Claude lead)
- Session start per RESUME.md: public (depth 50, wip/s160 0f926a2), private (depth 1, 1d0f76ce); npm i; cp -rn
  local-only; `patch.py setup s160` 132 passed; context lead 130552. Stray lanes added to .git/info/exclude. Card
  builds need AX_BATCH=s160 in the environment (author_lib.live_src; tool note).
- S5 fixes 1 to 28 of adj_r1.md done (pair files local/s160/chat4/<card>_p.py, applied by local/s160/chat4/ed.py);
  all six cards rebuilt, MECHANICAL PASS, card_dispositions 0 errors (anchors updated in each disp.py). Lead calls:
  - fix 4 (pc-benzo): the Mechanism line now reads "Agents cleared by glucuronidation alone ..."; Drugs-row names, the
    LOT hover and the Uses lorazepam clause kept (drug identity, not the masked list). read F7, F8 applied.
  - fix 7 (pc-sleep): PMC10071384 403 and aasm.org bot check (aasm.org added to fetch.py ALLOW, still blocked); MSD
    parasomnias (cached) gives clonazepam first, melatonin alternative; the board source found: UWorld library
    dlb.txt "Melatonin is the first-line therapy; clonazepam may be used if symptoms persist." (new local fact r01).
    Line: "Melatonin, acting at melatonin receptors, first; clonazepam if symptoms persist: REM sleep behavior
    disorder" (r01 z12); z12b dropped; card 1540593668559 added to cards.md and disp.py by hand. Report item: MSD
    orders clonazepam first; UWorld and AASM 2023 (both conditional) support melatonin first.
  - fix 9: hover reworded "leaves too little of the night for sleep" (the flags text copied the label: shingle_check).
  - fix 11 read F4: pc-orexin drawer on the Uses insomnia line (no orexin fact for a Where line).
  - fix 15: pc-benzo drawer on the buspirone Drugs line; read F4 somatic drawer added; read F5 owner line
    "Hypnotic choice in an older adult" -> pc-sleep.
  - fix 16 (adhd-meds): stem edited in repair/s160/01_pharm_s160.json; data-item-version 1 -> 2 (apply_edits refuses a
    changed stem at the same version). Card 1484792540444 sub-item (urine toxicology) -> owner:bipolar-mania.
  - fix 18 read F1 Why cells: "a baseline to compare against"; "Long-term use can affect a growing child"; "Boxed
    warning in youth; a rare serious label warning"; "Central blood pressure lowering; rebound after a stop".
  - fix 19 vs 21: acc R1, R2 took the shared Key point and Dependence lines (read R2, R3 not applied); read R1 applied.
    Row 3 Why "Dose-related label warnings; one of them means stopping the drug"; Adverse effects adds "Suicidal
    ideation, dose-related (label)" (b8).
  - fix 22: the acc reviewer's text, not a hover: Key point "avoid with liver disease, never with acute hepatitis or
    liver failure" (u12 k02 added; acute hepatitis is board-sourced, u03 and k02, so it stays in the body).
  - fix 24: Antabuse label quote found in the cached label (ds6 "reactions may occur with alcohol up to 14 days after
    ingesting disulfiram."): In practice hover on the disulfiram limits row. fix 25: sx2 now the whole label sentence
    naming methadone (flags rep 7 not applied). fix 23: bar [0, 67] for 7 to 10 days. fix 26: md2 quotes the rule.
  - fix 27: read F8 checked: substance teaches opioid overdose and naloxone in depth; pointer kept on substance.
  - fix 28 Why cells: "A life-threatening arrhythmia risk"; "Methadone is not detected the usual way"; "A rare,
    sometimes fatal organ injury"; "Events reported after marketing".
- Step 3: the six 10_*.json copied into repair/s160 by hand (patch.py s3 with no folders does not recopy: tool note);
  `patch.py s3 s160`: build OK (17 files, 30 ops), gate PASS 201 briefs (3 stale allowlist lines, the temporary ones),
  render PASS, preflight 23 warnings (P1 adhd-meds and sud-meds hedge losses as before), vendor 0. By hand on the 11
  briefs: squeeze_check 0 squeezed; pointer_check 60 pointers, 1 problem (tics Pairs with, pre-existing).
- Step 4 shots (local/s160/chat4/shots, phone study): sud-meds "When each drug can start" masks the drug names (read
  F2 stands, no fix); pc-benzo NBME Answer masked; the visible "Deciding clue" stays (s154g NBME-clause precedent).
- Synced: public a194311 and later, private 6c322402. Context alarm at 290k: stopped before S6.


## S6 lead self-check (chat 5, 2026-11-01): lines the lead could not settle; judge them
- pc-anxiety Uses, buspirone "In practice" hover: reads "Buspirone symptoms typically ease only once the dose reaches the upper range.; buspirone is taken on a schedule, not as a rescue dose" (doubled punctuation; "Buspirone symptoms" misattributes). Give replacement wording if it should change.
- pc-anxiety Adverse effects: "Gabapentinoids" became "Gabapentin: sedation, ataxia, dizziness, peripheral edema"; pregabalin is no longer named there. Judge whether pregabalin's adverse effects are now uncovered.
- pc-anxiety hydroxyzine adverse-effects line: the flag text and "; see Anticholinergic delirium below" run together; judge placement.
- adhd-meds Adverse effects: "Mania or psychosis, a small risk, as in diagnosed bipolar disorder" is unclear (risk in whom?). Give replacement wording grounded in the cited quotes.
- pc-sleep "In practice" hover: "...and the zolpidem label gives women 5 mg as the initial dose and older adults 5 mg" repeats itself; judge wording.
- pc-sleep REM sleep behavior disorder line puts the use after the drugs ("Melatonin ... first; clonazepam if symptoms persist: rapid eye movement sleep behavior disorder"); judge readability only (the drug order is a lead call, chat 4 fix 7).
- Checked by the lead, not findings: peds-sleep teaches cognitive behavioral therapy for insomnia (the new Where lines on pc-benzo and pc-sleep are owned); sud-meds dropped its "Which drug ... by situation" Where line on purpose.
