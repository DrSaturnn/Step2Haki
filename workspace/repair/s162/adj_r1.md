# s162 round 1 adjudication (lead, chat 2, 2026-11-03)

Receipts filed as repair/migration/spine/reviews/<card>_<part>_r1.md (local/s162/chat2/file_cards.py 1). Findings
survey local/s162/chat2/survey_r1.md (0 HIGH, 6 MED, 36 LOW counted by numbered line).

Verdicts: acc PASS-IF x4 (pc-atypical 2 LOW, pc-antichol 1, pc-typical 2, pc-td 3). flags PASS-IF pc-atypical (1 LOW
+ K1 note), pc-antichol (1 LOW), pc-td (3 LOW); FAIL pc-typical (1 MED, 2 LOW + K1). read FAIL x4: pc-atypical 1 MED
5 LOW, pc-typical 1 MED 6 LOW, pc-antichol 2 MED 3 LOW, pc-td 1 MED 5 LOW.

Edits are made in each card's author.py (s161 method: pair files local/s162/chat3/<card>_p*.py), then
`AX_BATCH=s162 build_brief.py <folder> --verify` (MECHANICAL PASS, 0 FIX), 10_ copied to repair/s162, `patch.py s3
s162`, squeeze by hand on the four ids. "old -> new" strings are as shown in brief_text.txt; find the author.py source
string by grep (a masked or hover span may split it).

## Not findings (no edit)
- "[end of Bottom line]" (read pc-atypical L6, pc-typical L7): review_packet.py line 131 adds the marker to every
  brief_text; it does not render.
- Timeline and onset chart event names unmasked in brief_text (read pc-atypical L5, pc-typical L6): s159 display saw
  them masked in study mode (S159.md L234).
- K1 "no card checklist at packets/<brief>/cards.md" (flags pc-atypical L2, pc-typical L4): packet path gap (s161 tool
  note); cards.md is in each acc folder.
- read pc-atypical L2 (ANC decision in danger row and Monitoring) and pc-typical L4 (ECG decision three times):
  rejected; CARD_SPEC allows danger rows and the monitoring table both, each cell masked, no contradiction.
- read pc-atypical L3 (no Sexual Dysfunction pointer): rejected; the Hyperprolactinemia drawer and the NBME block's
  antipsych-effects drawer carry it; 14201a's coverage owner sexual-dysfunction already holds the item.
- read pc-antichol L3 (masked "Anticholinergic delirium" near "Anticholinergic toxicity"): rejected, weak synonym.
- read pc-antichol L5 (fragments "No benefit in tardive dyskinesia ...", "Not for tardive dyskinesia"): rejected,
  card register.
- acc pc-atypical L1 (clozapine windows): card unchanged (label lines match the quotes). Report item stands:
  antipsych-effects L27/L34 (3 months, 4 weeks) sit inside the label windows; align or note there (OPEN_WORK).

## Accepted edits

### pc-atypical (ATYP)
1. MED read L1, NBME block 1 Setup: "Sertraline, clomipramine and risperidone; erectile dysfunction and mild breast
   growth" -> "An SSRI, a tricyclic and an antipsychotic started; erectile dysfunction and mild breast growth".
2. acc L2, danger row "Older adults with dementia": "If delirium agitation has cleared, choose" -> "If an older
   adult's delirium agitation has cleared on an antipsychotic, choose".
3. flags L1, Uses: "first line; clozapine after 2 failed trials" -> "first line in newly diagnosed disease; clozapine
   after 2 failed trials".
4. read L4, hover "Weight-neutral drugs": "(first, middle and last letters)" -> "(first, middle and last letters of
   the alphabet)".

### pc-typical (TYP)
1. MED read L1, Where the choice is made: "What benztropine and diphenhydramine relieve" -> "What the anticholinergic
   drugs relieve" (chip pc-antichol unchanged).
2. MED flags L1 + acc L2, Interactions row: first cell "Pimozide plus clarithromycin or an azole antifungal" ->
   "Pimozide plus clarithromycin, itraconazole or ketoconazole"; Result cell "Sudden deaths reported" -> "Sudden
   deaths reported with clarithromycin" (claim ids pz3, pz6 unchanged).
3. flags L3, bank item q_d6b90a2a436c98b15996 key reason: "A macrolide: it prolongs QT itself, and the pimozide label
   bars it after sudden deaths" -> "A macrolide: it prolongs QT itself, and the pimozide label bars it; sudden deaths
   were reported with clarithromycin" (item edited in author.py; the bank is rebuilt, not apply_edits).
4. acc L1, danger row QT: "Thioridazine, IV haloperidol, pimozide; torsades and sudden death" -> "Thioridazine,
   chlorpromazine, IV haloperidol, pimozide; torsades and sudden death".
5. read L3, Key point: "QT: low potency and IV haloperidol" -> "QT: low potency, IV haloperidol and pimozide".
6. flags L2, Tourette row: "Tourette tics: haloperidol, fluphenazine, pimozide" -> "Tourette tics that resist
   standard treatment: haloperidol, fluphenazine, pimozide".
7. read L2, Dementia adverse-effect line: chip dementia -> antipsych-effects (pc-atypical's boxed warning row already
   points there; confirm by grep that antipsych-effects teaches the boxed warning; if not, leave and note).
8. read L5, hover "Who is at risk": "older women, parkinsonism and tardive dyskinesia" -> "older women are likeliest to
   get parkinsonism and tardive dyskinesia".

### pc-antichol (ACHOL)
1. MED read L1, Uses: "Drug-induced parkinsonism: short-term relief when the dose cannot come down; amantadine is the
   other option" -> "Drug-induced parkinsonism: short-term relief only".
2. MED read L2, danger row "An older adult": chip delirium -> antipsych-effects (antipsych-effects owns it: "Parkinsonism:
   Lower the dose or switch to a second-generation drug; amantadine, or an anticholinergic short term"; delirium stays
   in Where the choice is made).
3. acc L1, Mechanism: "less contraction of sweat glands, salivary glands, bladder and bowel" -> "less secretion from
   sweat and salivary glands, less contraction of bladder and bowel" (the n6 claim stays; a15 supports the glands).
4. flags L1, Interactions "Another anticholinergic" Result: "Additive block; fatal heat stroke and paralytic ileus have
   been reported" -> "Additive block; heat stroke and paralytic ileus, sometimes fatal, have been reported".
5. read L4, Key point: "Class cost:" -> "Class adverse effects:".

### pc-td (TD)
1. MED read L1, Monitoring "Before and during, in Huntington disease" Why: "Boxed warning; untreated depression rules
   out two of the drugs" -> "Boxed warning; two labels bar use when it is untreated".
2. acc L1, deutetrabenazine: "better tolerated than tetrabenazine" -> "appears better tolerated than tetrabenazine".
3. acc L2, Reserpine hover: "In practice: the deutetrabenazine label asks for at least 20 days off reserpine first." ->
   "Label: the deutetrabenazine label asks for at least 20 days off reserpine first." (hover title "In practice" ->
   "Label" if separate).
4. acc L3, Where the choice is made: "recognition and the management order (stop anticholinergics, taper or switch,
   clozapine)" -> "recognition and the management order (stop anticholinergics, valbenazine or deutetrabenazine if
   moderate to severe, stop or switch, eg clozapine)".
5. flags L1: "Parkinsonism and akathisia: lower the dose or stop" -> "... lower the dose or stop if clinically
   significant"; Monitoring "During treatment" Why "Lower the dose or stop" -> "For parkinsonism or akathisia, if
   significant: lower the dose or stop".
6. flags L2: "QT prolongation: avoid with" -> "QT prolongation (valbenazine and deutetrabenazine labels): avoid with".
7. flags L3: "the most common; no driving" -> "the most common with valbenazine; no driving".
8. read L2, Monitoring Why: "Poor metabolizers keep a lower dose" -> "Poor metabolizers clear it slowly".
9. read L3, owners line: "MAOI washout before a VMAT2 inhibitor" -> "MAOI timing before a VMAT2 inhibitor".
10. read L4, Key point: "Tetrabenazine and reserpine deplete dopamine the same way, for Huntington chorea" ->
    "Tetrabenazine and reserpine also deplete dopamine, for Huntington chorea".
11. read L5, Mechanism hover label "Unclear" -> "Mechanism in tardive dyskinesia".
12. read L6, danger row "Depression and suicidality": "can worsen both, the boxed warning on valbenazine,
    deutetrabenazine and tetrabenazine" -> "can worsen both; this is the boxed warning on all three drugs".

## Round 2 (S7) scope
read all four (each had a MED), flags pc-typical (MED); acc and the other flags parts are PASS-IF: their
replacements were applied as given (pc-typical acc 2 was widened by the flags MED fix; include acc-B pc-typical in
round 2 for that row). Packets --since each part's r1 brief_text.
