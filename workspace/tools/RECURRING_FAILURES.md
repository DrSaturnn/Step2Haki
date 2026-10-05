# Recurring failures and what catches them

The failure types that audits kept finding (Jonathan, 2026-10-05, from the s98 to s104 audit
rounds). `tools/preflight.py` runs inside `ship.sh` and prints warnings. It never aborts a ship.
Run it before the audit as well (`python3 tools/preflight.py <built page> --base HEAD`) and paste
its lines into the audit packet. The auditor settles each line and covers the parts no script can.

| Failure | Script check | Auditor still checks |
|---|---|---|
| Dropped hedge or narrowed scope ("up to 6 hours" became "6 hours") | P1: a number the old brief qualified is now only bare; hedge words (may, usually, about, up to...) fell by 2 or more | Age or population scope: a rule for the second year of life applied to a 3-year-old; an adult-only guideline used to prove a pediatric line |
| Sibling line left behind | P2: a 6-word run whose page-wide count fell but did not reach zero | Paraphrased copies of the old claim in table rows, pearls, other explanations and other briefs (grep the key number and term) |
| A cut broke a question | P3: a distractor that its explanation used to address and no longer does; a relabeled distractor its explanation does not name; a new item's distractor named nowhere in its brief | Whether any source would defend a distractor (the key must stay uniquely best) |
| Neighboring questions with the same answer | P4: two items in one bank with the same key, one of them new or changed | Near-synonym keys ("Reassurance" vs "Reassure and observe") |
| New question retells a UWorld case, or its stem gives the answer away | P5: a diagnosis item whose stem holds the key's distinctive words; P6: an authored stem sharing most clue words and numbers with one source stem (needs local-only sources) | Clue pattern and order copied from the source even when words differ |
| Old edit file fails the vendor check after a wording change (s103) | P7, blocking in ship.sh: `vendor_scan.py --page <new page>` judges tracked edit files against the page about to ship, so the failure surfaces in this ship, not the next | Nothing |

Calibration (2026-10-05, replaying s97 to s104 against each parent): 5 to 16 warnings per ship.
P3 found real cuts that the audits passed. In s99 (neonatal-jaundice q_e3d8) and s102 (htn-drugs
q_9f89), removing a flagged line left both distractors unexplained. P7 reproduces the s103 failure
on the s102 build.

`preflight.py --all` runs P3 to P6 on every item. In that mode P6 lists 8 authored items whose stems
match a source stem closely (several still carry UWorld nids). Treat it as a review list, not proof.
