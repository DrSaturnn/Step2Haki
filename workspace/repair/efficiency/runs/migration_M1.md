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
