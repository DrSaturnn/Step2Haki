# s159 round 1 adjudication and round 2 fixes (lead; for round 2 reviewers)

### S5 adjudication, round 1 (lead)
Rejected (with evidence):
- read pc-maoi F1 and the Key point part of F2, read pc-snri F1 and F2, read pc-antidep L2 (Key point names a masked
  answer): the Key point is blurred whole in study mode (div.dp; lead checked local/s159/shots_r1/study
  pc-snri_phone-study_step0a.png, and display confirmed it on all three cards). Not a leak. Read missed it (no study
  images in its packet).
- display pc-maoi F2, display pc-snri L2, pc-antidep L (Key point blurred while the rows restate its content): the Key
  point is the summary; the drug rows are the detail it summarizes, as dp works on every brief. Kept; report item.
- read pc-maoi L10 (onset chart event names unmasked): display saw them masked in study mode.
- read pc-snri F4 (card decides discontinuation management): the danger-row commit (stopping venlafaxine -> slow taper)
  is prevention, which CARD_SPEC section 4 asks each danger row to commit; management beyond it is pointed to
  ssri-effects. Partly accepted through the note rewrite below.
- read pc-maoi L4 (serotonin syndrome commit) and L5 (overdose admit line): kept; first step only, and the admit line is
  the MAOI-specific window quoted from the label.
- read pc-snri L7 (hover label "Pain order" against title "Neuropathic pain"): label-plus-title convention (the reader
  withdrew it); only the Low Back Pain chip placement remains (fix 13).
- display pc-maoi L6 (dark teal top-tier bars): the lcw palette tokens of the live charts; not a card fault (deferred to
  a site-layer look at the lcw palette if Jonathan wants it).
Deferred: acc pc-antidep L (vilazodone, vortioxetine absent from the MAOI and serotonin syndrome rows; needs Viibryd and
  Trintellix label quotes) -> OPEN_WORK s159 line. ssri-effects reassurance-first against UWorld 11957 restart-then-taper
  (acc pc-snri report item) -> OPEN_WORK and the report: ssri-effects conditions reassurance on a patient who prefers to
  stay off (its item q_6f875a3df168eda248ea, d1 reason), the pc-snri item stem is a patient who ran out; the two fit, but
  ssri-effects never states the restart case for a patient who wants to continue. A live-brief content change is out of
  this batch's scope (patch lane is drawers only).
Accepted (the fixes below).
Who found what: study-mode leaks in rows and hovers found by read and display together (display on images, read on
  text); the discontinuation conflict by acc, read and display from three sides; the unsupported prescriber clause by
  flags only; acc missed the leaks (not its part).

## Fixes applied (chat 5)
- Session start per RESUME.md. The builder lanes' DailyMed fetches (chat 3) were never synced into the shared web cache
  and were lost with that container: pc-snri and pc-antidep could not rebuild (facts_from_spec FileNotFoundError).
  Re-fetched with fetch.py (9 spls.json lists, 4 drugInfo.cfm labels): every sha matched the cited id (content
  unchanged), so no fact changed. Synced to the private repo this time.
- Fixes 1 to 17 done as written, with these lead calls (all re-verified MECHANICAL PASS; card_dispositions 0 errors):
  - fix 4: the Foods hover's whole sentence "The low-dose selegiline patch needs no diet limits; above the 6 mg
    starting patch it does." dropped (ids now w02 c08).
  - fix 7 subtitle: head_fix on the shell's "monoamine oxidase inhibitors &middot;" (w04).
  - fix 8: U+2011 in the 9 MAO-A/MAO-B mentions of pc-maoi's body (only card with the term); desktop pc-tbl columns
    33/30/37% with table-layout fixed above 640 px (gen_section.py CSS, all three cards).
  - fix 9: masked middle clause via M(); stay-off clause cites new fact sn20, the Warner AFP 2006 quote that backs
    ssri-effects S112 (fetch edf46042a52a3b04), with an ssri-effects drawer chip in the note (the row's chips row also
    has one).
  - fix 14: c67 lists options, not an order, so the second clause is dropped: "An alpha-1 agonist constricts the
    helicine arterioles." (a09 plus new card fact a14, AnKing 1477011581106 "Phenylephrine is primarily a(n) [α1]
    agonist").
  - fix 16 Key point: the trigger list sits in the Key point line 1 (now the danger row's wording).
  - fix 17: peds-sleep teaches adult insomnia drugs (acute insomnia, trazodone as a sleep aid): owner line kept. mdd
    teaches "Insomnia or poor appetite -> Mirtazapine": mdd drawer added on the mirtazapine Uses line; mdd has no
    trazodone choice, so none there.
  - disp.py anchors updated for the changed text in all three cards (MAOI 3 inherited-covered warns, one new:
    1485048880722.8ddb98b66b, the 2-week number now owned by the washout chart; ANTIDEP 4 warns unchanged).
- lanes_r1.json renamed repair/s159/r1_review_spec.txt (build.py reads every repair/s159/*.json, S3 failed on it; the public guard refuses a lanes/ folder).
- S3 (`patch.py s3 s159`, no folders): build OK 13 files 15 ops; gate PASS (the 2 s159 temporary allowlist lines
  stale, expected); render PASS; preflight 0; vendor 0; squeeze run by hand on the 8 briefs, 0 (patch.py s3 with no
  folders passes an empty id list and reports "brief not found": tool gap); pointer_check 8 briefs 0 problems.


## The 17 fixes as written (old -> new)
Edit each card's author.py (pharm/<X>/spine), rebuild and verify per the card's BUILD_NOTES rebuild line; old text is
as in repair/migration/spine/packets/s159/<brief>/acc/brief_text.txt. Grep STANDING_DIRECTIONS and CARD_SPEC for "mask"
before editing masks.
pc-maoi:
 1. (flags MED) Why reserved hover: "Tranylcypromine often works after several failed antidepressant trials, given by a
    clinician experienced with MAOIs." -> "Tranylcypromine often works after several failed antidepressant trials."
 2. (display and read MED, leak) Mechanism line 3: "Irreversible block → new enzyme takes up to 2 weeks → diet limits and
    washout last 2 weeks after the last dose" -> "Irreversible block → new enzyme must be made → diet limits and washout
    outlast the last dose (timeline below)" (keep a03; drop the number, owned by the washout chart).
 3. (read MED, leak) diet row In practice hover: "Step 2 uses 2 weeks. StatPearls advises keeping the diet for 4 weeks
    after the last dose." -> "StatPearls advises keeping the diet for 4 weeks after the last dose, longer than the Step 2
    window."
 4. (read MED, leak) Mechanism line 4: "Selegiline: MAO-B only at low doses → the low-dose patch needs no diet limits" ->
    "Selegiline: MAO-B only at low doses → gut MAO-A spared at the low-dose patch"; Foods hover in the Interactions table:
    drop the sentence "The low-dose selegiline patch needs no diet limits" (the Monitoring row owns it, masked).
 5. (display LOW) toxicity chart value lines: "Within minutes of a tyramine meal or a decongestant" -> "Within minutes of
    the trigger"; "Usually within 6 hours of a serotonergic drug being added; nearly always within 24 hours" -> "Usually
    within 6 hours of the change; nearly always within 24 hours".
 6. (acc LOW) A and B hover: "selegiline and rasagiline block MAO-B selectively." -> "selegiline at low doses and
    rasagiline block MAO-B selectively."
 7. (read LOWs) subtitle "monoamine oxidase inhibitors" -> "monoamine oxidase inhibitors (MAOIs)"; serotonin syndrome
    finding "(SSRI), SNRI, tricyclic" -> "(SSRI), serotonin-norepinephrine reuptake inhibitor (SNRI), tricyclic"; Key
    point "Not first line: treatment-resistant or atypical depression; lethal in overdose" -> "Not first line; used for
    treatment-resistant or atypical depression; lethal in overdose"; Uses "first-line drugs first, an MAOI if they fail"
    -> "other first-line drugs first, an MAOI if they fail"; foods Rule (masked) "Avoid them every day" -> "Avoid these
    foods every day".
 8. (display LOWs, CSS in the card layer) "MAO-B" and "MAO-A" non-breaking hyphen (U+2011) in the card text, or
    white-space:nowrap on the term; desktop pc-tbl columns sized to content (Result and Rule no longer wrap two-word
    values; about 1.1fr 1fr 1.2fr), all three cards.
pc-snri:
 9. (acc, read, display MED) Discontinuation note: "Symptoms after an abrupt stop are discontinuation, not relapse or
    influenza; restarting it and then tapering slowly is the move taught for paroxetine (analogy)" -> "Symptoms after an
    abrupt stop are discontinuation, not relapse or influenza;" + masked (mask "ans") "a patient who wants to stay on
    venlafaxine restarts it, then tapers slowly, as the board teaches for paroxetine, the other short half-life drug" +
    "; one who prefers to stay off: SSRI Adverse Effects." Sources c25, c26, u08; the last clause borrows the
    ssri-effects claim behind item q_6f875a3df168eda248ea (sibling claim id). Item q_6c2aed51ed02f9dc133a unchanged.
10. (flags LOW) "Blood pressure up after a dose increase, more at higher doses" -> "Blood pressure up, more at higher
    doses".
11. (read LOWs) Key point "the most common SNRI adverse effect" -> "the most common adverse effect of
    serotonin-norepinephrine reuptake inhibitors (SNRIs)"; hover label "Discontinuation mnemonic (AnKing)" ->
    "Discontinuation mnemonic"; "Discontinuation symptoms after an abrupt stop, without seizures; block below" ->
    "Discontinuation syndrome after an abrupt stop, without seizures; block below"; "Nausea, mostly in the first 2 weeks;
    stimulant effects or sedation" -> "Nausea, mostly in the first 2 weeks; also stimulant effects or sedation".
12. (read LOWs) Interactions MAOI Rule (masked) "Never together; washout below" -> "Never together; washout as on the
    MAOIs card"; Drugs row: split "Levomilnacipran Fetzima and milnacipran Savella: milnacipran for fibromyalgia" into
    "Levomilnacipran Fetzima" and "Milnacipran Savella: fibromyalgia"; serotonin syndrome danger row trigger list:
    prefix "for example".
13. (read LOW) duloxetine Uses line: move the Low Back Pain drawer chip to the end of the back-pain clause.
pc-antidep:
14. (read MED, leak) priapism "Why / How it works" hover: "Phenylephrine constricts the helicine arterioles; surgical
    decompression is the other option." -> "An alpha-1 agonist constricts the helicine arterioles; surgery is the step
    after." (check the cited quote still supports it; else drop the second clause).
15. (flags LOW) "purging in bulimia or anorexia disturbs electrolytes and raises it further" -> "electrolyte
    abnormalities, as in bulimia or anorexia, raise it further".
16. (read LOWs) "a weight concern, or a wish to quit smoking" -> "concern about weight gain, or a wish to quit smoking";
    "A painful erection lasting over 4 hours on trazodone, from alpha-1 block" -> "An erection lasting over 4 hours on
    trazodone, usually painful, from alpha-1 block"; Key point trigger list -> the danger row's wording ("an abrupt stop
    of alcohol, a benzodiazepine, a barbiturate or an antiepileptic"); Interactions row 1 "An MAOI (monoamine oxidase
    inhibitor)" -> "A monoamine oxidase inhibitor (MAOI)"; "Wellbutrin SR, XL" -> expand SR (sustained release) and XL
    (extended release) as pc-snri does XR; split the vilazodone and vortioxetine Drugs line in two.
17. (read LOWs, check first) peds-sleep ownership of adult drug-for-insomnia: grep its brief text through pagelib; if it
    teaches adult insomnia drugs keep the owner line, else retarget to the brief that does (or drop the line). mdd drawer
    on the mirtazapine and trazodone Uses lines: add if mdd teaches that choice.
Then: re-copy each rebuilt 10_pc_*_spine.json into repair/s159 (patch.py s3 does not), `patch.py s3 s159` page checks,
new shots (shots.py phone, phone-study, desk into local/s159/shots_r2; sheets.py), S6 self-check, S7 follow-up round:
review_packet.py --since each part's round 1 brief_text.txt, lanes.py round 2 (copy the lane-root RULES.md fix again),
same models, budget left 3.41M (ask Jonathan before going over).
