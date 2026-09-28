# Type C and migration contract (rule, authority, check, test)

One row per rule. A rule is only trusted when it has a mechanical check and a mutation test, or is on the reviewer's list. The golden brief is `tools/tests/migrate/golden_hip.html` (the approved septic hip brief, repaired 2026-09-28: ids, aliases, acronyms).

Before confirming any Type C brief or migration: `python3 tools/test_migrate_check.py` (every case must pass; 32 cases on 2026-09-28), then `tools/migrate_check.py <old> <new> <map> --page=index.html --source=<local source>`, then the reviewer list below. A brief is not reported as done while any of the three fails.

## Defect to rule (the audit loop)
When Jonathan or a reviewer finds a defect the checker passed, in the same batch: (1) add the check to `migrate_check.py`, (2) add a mutation to `test_migrate_check.py` that reproduces it, (3) add the rule to the skill that authors it (board-brief, brief-migration or study-page-builder) and a row here, (4) re-run the self-test, then re-check every brief already produced in the batch. The brief is not re-shown until all four are done.

## Questions (items)
| Code | Rule | Authority | Skill | Test |
|---|---|---|---|---|
| I0 | The claim map (or `--topic`) names the topic diagnoses stems must not give away | Peds priority rule 3; board-brief 4.1 | brief-migration step 5 | no topic terms |
| I1 | Every item has `data-src` (`nbme` or `authored`) and an explicit `data-lead-in` ending in "?" | Approved hip brief (every item) | board-brief 4.1 item contract | lead-in missing; data-src missing |
| I2 | Stem is a board-style vignette: opens with age and sex written in full ("18-month-old boy"), then complaint and duration, history, vitals with units, exam, labs with units, imaging; facts separated by semicolons; no shorthand ("4 yo M") | NBME style; approved hip brief | board-brief 4.1 item contract | shorthand age; no age/sex opening |
| I3 | Stem, key and companion: the companion states the deciding clue or rule; never empty | board-brief 4.1; approved hip brief | board-brief 4.1 | no companion |
| I4 | A dx, test or stage stem never names the topic diagnosis or the key; other types name it only for a diagnosis already made and treated ("was drained", "after IVIG") | Peds priority rule 3; board-brief 4.1 | board-brief 4.1 | dx stem names topic |
| I5 | Key and both distractors distinct, same category | board-brief 4.2 | board-brief 4.2 | options not distinct |
| I6 | A carried item whose stem changed gets a version bump; option ids kept unless the label's meaning changed | study-page metadata contract | brief-migration step 4 | stem changed, no version bump |
| I7 | Temperature carries units (WARN) | NBME style | board-brief 4.1 | (warn only) |
| I9 | NBME items first in the bank, followed by a "How NBME framed it" note and a Distractors block | board-brief Part 2 | board-brief Part 2 | NBME item after authored |
| (gate) | No `data-src="uworld"` item, no `.vignette`, no stem opening "Same patient" | board-brief Rule 11, 13b | board-brief | UWorld item on page; Same patient stem |
| carried | Every old item restyled to I1 to I4 when carried; none carried as shorthand | Jonathan 2026-09-28 ("implement the questions the same way") | brief-migration step 4 | covered by I1 to I4 on every item |

## Content and voice
| Code | Rule | Authority | Test |
|---|---|---|---|
| claims | Every old claim has a disposition; carried text is found in the new brief | brief-migration step 3 | carried text absent |
| clues | Clue rows have a role and are never dropped | Jonathan 2026-09-28 (every clue is used) | clue dropped; clue without role |
| items | Every old item id accounted for | brief-migration step 4 | old item unaccounted |
| A1 | An acronym the old brief wrote out stays written out | pilot M1 defect (arm P) | acronym expansion lost |
| V1 | Every acronym written out, and at its first use, not later (allowlist: CRASH, ST, GI, COVID-19, SARS, II, III, HR, RR, BP, IV, US, NBME) | standing voice rule; R3 reviewer (expansions placed after first use) | acronym never written out; acronym used before written out |
| voice | No em dash; no "noise" or "separates nothing" | standing rules | em dash; banned wording |
| markup | Tables in `.tw` with a caption; jump links resolve; replaced ids have alias spans | study-page-builder | table not wrapped; alias missing |
| H1 | The new `<h4>` keeps the old title unless every inbound Pairs-with reference and the sidebar link are listed in `inbound_rewrites` and rewritten (run with `--page=index.html`) | study-page-builder xrefs (exact-title links); audit run defect 2026-09-28 | title changed, inbound references break |
| Q1 | A carried claim keeps its qualifiers (only, especially, usually, never, not, must, most, highest, wrong...); a changed qualifier is a sourced `corrected` row, or `qualifier_ok` states why the meaning is the same | pilot M1 (arm C "especially" to "most common"; arm P "is wrong" to "is less likely"); audit run reviewer | qualifier softened |
| S1 | A corrected number lists `stale_patterns` (old wordings); none may remain anywhere in the brief, items included | audit run reviewer (old echo schedule reappeared in an item stem) | corrected value left behind; corrected number without stale patterns |
| I6b | An option id changes only when its label's meaning changed, and the item row lists it in `changed_options` with the reason (otherwise WARN) | study-page metadata contract | (warn) |
| P1 | Every Pairs-with partner in `<b>` is an existing `<h4>` on the page (`--page`) | study-page-builder xrefs; R3 reviewer could not verify | Pairs-with partner not on the page |
| V2 | No run of 10 or more words, lead-ins and option labels included, copied from the vendor source (`--source=repair/sources/...`) | Rule 11 (paraphrase the vendor); R3 copied the NBME lead-in | vendor lead-in copied |
| N1 | Every carried number (dose, schedule, window, threshold) is checked against current guidance: `currency` verified (with source), flagged (⚠︎ on page) or stable | "current guidelines set facts"; audit run defect 2026-09-28 (2004 echo schedule carried) | number without currency |

## Reviewer list (cannot be checked mechanically; blinded reviewer, CRITICAL if violated)
1. No carried claim changed meaning (for example "is wrong" softened to "is less likely"); a change needs a `corrected` row with a clinical source, not a style rule.
2. Every clue in each source stem appears in the NBME item stem or the clue table with its role.
3. Every item matches the golden brief's question style (I2 order, units, semicolons) and tests recognition from findings.
4. One best answer; each distractor a real mimic a prepared student would weigh (F1 to F6).
5. Corrections are right per current guidelines and cited, and no outdated number was carried as `stable`.
6. A clue role that is the worker's reading, not the source's, is marked ⚠︎ (role inferred) on the page.
7. Every claim in the worker's report is backed by a check (for example "no inbound references" must match `--page`).
