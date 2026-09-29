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
- R4 (fresh worker): checks PASS; reviewer ACCEPT; found the golden's own Tier-table mask defect (M1) and mixed-case acronyms (V1), both now checked; golden repaired again (Tier mask, HbSS, one stem without objective data).
- R5 (fresh worker): checks PASS at the time; reviewer REJECT (an "and" became "or" in a carried claim; a stem of labels with no vitals; an unmarked inferred role). Became Q1b, I8, R1, plus C1 (clue census). Under the new checks R5 fails on 10 stems without objective data, which the reviewer had only partly seen.
- Current candidate: R4 output plus reviewer fixes (repair/migration/kawasaki/brief.html): passes all 42 self-test cases and every check. R6 (the re-test of the final skill text) was cut off by the org spend limit before writing anything; skill proposals wait on it.
- Jonathan (2026-09-28): the CRASH and Burn mnemonic must be saved and highlighted. Every run had flattened it into the criteria tile or stripped its highlights, and the claim map did not see it because the words survived. Now checks K1 (mnemonic block, letter highlight, bold phrases, pearl mnemonics) and K2 (scaleref link); candidate restored with the mnemonic block and highlighted initials (page CSS and transform change listed in MIGRATION_CONTRACT.md, preview only). Self-test 47/47.
- R6 (fresh worker, final skill text incl. mnemonic rule, 242,291 tokens): checks PASS with no help; reviewer ACCEPT, no CRITICAL; mnemonic kept and highlighted. Minors fixed in the candidate (subtitle day-10 wording, BP role, MIS-C vs toxic shock deciding column and confirm cells, one weak distractor). The recurring "obvious discomfort" softening became a check (Q1 intensity words). Candidate = R6 plus those fixes (repair/migration/kawasaki/brief.html). Self-test 48/48. Skill proposals released after this run.

## Layout standard and re-tests (2026-09-29)
- Jonathan chose the accent-bar serif headers, the compact illness script (iPhone: stacked with a color bar per disease; desktop: side-by-side table), dense row cards, and one shaded first-steps group ("together, in either order"). All page CSS: tools/typec/typec.css; preview: tools/typec/preview.py. Checks L1 to L3; golden hip moved to the new markup.
- R7 ACCEPT (reviewer: script lines untraced, one timing drift) -> N2. R8 ACCEPT (reviewer: CRP "triggers echo" inside the group; new table cells untraced) -> L2 routing check, N2 on dense cells.
- R9 REJECT: the worker satisfied L2 by deleting the carried "triggers" sequence and relabeling Supports/Staging as First for "vocabulary" -> Q1 sequence words, O1 order labels, L2 message says move, never delete.
- R10 REJECT: relabeled the echocardiogram By branch to keep the group clean, though it is done at diagnosis in every case -> dual-path rule in board-brief and reviewer list item 7.
- R11 (final text) PASS with no help; reviewer ACCEPT, no CRITICAL. Candidate = R11 plus the reviewer's minors (infant evaluation trigger limited to 6 months or younger, "argues against" for mitral obstruction, no embellished "no discharge", MIS-C age 9, emergency department clue restored). Self-test 57/57.
- Lesson: a check can push a worker to game it (R9, R10). Every check's message now names the structural fix, and the reviewer list treats relabeling or deleting to pass a check as CRITICAL.
