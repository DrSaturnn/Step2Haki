# Migration pilot, cluster M1 (kawasaki), 2026-09-28

Frozen rubric: ../RUBRIC_migration.md. Blinded reviewer saw X = lean packet (P), Y = full spec (C).

| Arm | Tokens | Tool uses | Minutes | migrate_check | Checklist | Quality | Reviewer verdict |
|---|---|---|---|---|---|---|---|
| C full spec | 207,743 | 26 | 8.9 | PASS | 14/14 | voice fail (acronyms not written out) | REJECT strict; ship this one |
| P lean packet | 166,668 | 17 | 8.7 | PASS | 13/14 | voice fail (lost 3 old acronym expansions still marked carried) | REJECT |

- P saved 19.8% of tokens, under the 25% bar, and changed the meaning of the transferable rule ("is wrong" to "is less likely") on a style rule, with no clinical source. C kept every old claim's meaning.
- Neither arm had a CRITICAL finding (no lost fact, clue, question or wrong key). Both carried all 10 old items and added 4.
- C made one sourced correction: echocardiogram at diagnosis, then 1 to 2 and 4 to 6 weeks after treatment (AHA 2017, McCrindle, Circulation 2017;135:e927), verified against the ACC summary; the old 2 and 6 to 8 week schedule is the 2004 statement.
- Accepted output = C plus a mechanical pass: acronyms written out at first use, "especially in infants under 6 months" restored, verified warning flags removed, one companion "KD" written out (q_c99ce2a03174582f9a18 v2). migrate_check PASS with no WARN; live-page render 14 cards, no overflow at 390 px.
- Reviewer cost (evaluation, not production): 154,243 tokens.
- Checker gaps found: both arms passed migrate_check with unexpanded acronyms, so migrate_check now WARNs on acronyms never written out.

Decision after cluster 1: packet not adopted. Before cluster 2, the packet needs: keep every existing acronym expansion; write every acronym out at first use; never reword a carried claim for style (only a sourced `corrected` row changes meaning).

## Audit after Jonathan's review (2026-09-28): the skill, not only the output
Jonathan: the questions were not implemented the way the approved hip brief implements them, and the rules that prevent regression were not all in the skills. Confirmed: every carried item kept its old shorthand stem ("4 yo M, fever 6 days..."), 11 of 14 had no explicit lead-in, 2 had no companion, 2 named the diagnosis; migrate_check passed all of it, and the reviewer did not look.

Loop run (defect -> check -> mutation test -> skill line -> re-run):
- Checks added: I0 to I9 (item contract), A1 (lost expansion), V1 (acronym at first use), H1 (title change breaks inbound links), N1 (number currency), Q1 (qualifier dropped), S1 (corrected value left behind), P1 (Pairs-with target exists), V2 (10-word vendor run). Self-test: tools/test_migrate_check.py, 32 cases, golden brief clean.
- Golden brief audited too: it failed (aliases missing, 8 acronyms never written out); repaired before becoming the reference (tools/tests/migrate/golden_hip.html).
- Audit run R2 (fresh worker, drafted skills): passed its checks but changed the title (5 inbound links would break; the worker reported "no inbound references") and carried the 2004 echo schedule, including a new item keyed on it. Both became checks (H1, N1, S1).
- Audit run R3 (fresh worker, revised skills, no help): checks PASS; reviewer ACCEPT, no CRITICAL; minors became checks (V1 first use, P1, V2) and were fixed. The earlier accepted arm C fails V2 (a copied 10-word run), which the old checker missed.
- Tokens: R2 231,313; R3 231,798; reviewers 125,320 and 130,350.
