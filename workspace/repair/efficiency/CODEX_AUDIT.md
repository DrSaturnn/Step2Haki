# Claude's audit of Codex-led work (run on return, before any ship)

Written 2026-10-21 with CODEX_LEAD.md. Accuracy is non-negotiable (Jonathan): nothing Codex built or reviewed ships
until this audit passes. Record every finding in the batch file under "Codex audit", by kind, so CODEX_LEAD.md section
7 can be tightened.

1. **Lock and state.** Read the State and the Lead line; take the lock (rewrite the Lead line, push alone). Check both
   repos are pushed and the batch file records every step Codex ran.
2. **Mechanical, from scratch.** For every brief Codex built or changed: rebuild (build.py), facts_from_spec.py,
   quote_check.py (100% verified, 0 relayed unless disclosed), card_dispositions.py check, verify --mech, the batch build
   and gate. Any difference from what Codex recorded is a finding.
3. **Meaning sample.** Per brief, 15 claims chosen across steps (bottom line, urgent rows, differential Decides-it,
   workup, treatment) plus every claim with a number: the cited quote states the claim itself; the board answer is
   taught where a source differs; no hedge dropped from a taught clause. Two or more meaning errors in the sample: audit
   every claim of that brief.
4. **Board evidence.** boards.md covers the bank's keys and the board index's question items; cards.md dispositions are
   honest (spot-check 10 "covered" against the claim text and every "scope").
5. **Bank.** ids unchanged; version bumps where a key or choice changed; reasons on every item and none contradicting
   the body.
6. **Reviews.** If Codex ran S4 or S7, re-run the acc lane with the Claude lean-reviewer on each brief Codex built
   (budget permitting; ask Jonathan when it does not fit), and compare: what Codex's reviewers missed is a finding.
7. **Display.** shots_all.py and the phone sheets: no squeezed columns, masks intact in study mode.
8. **Consistency across authors** (Jonathan 2026-10-22: Claude evaluates Codex's final briefs "for any additional
   considerations regarding specific Codex rules in order to maintain consistency across brief authorships"). Compare
   each Codex brief side by side with the nearest Claude-built brief of its entry type (disease: septic-hip, sjia and
   the golden scfe; hub: limp), from the built page and the phone sheets, not from Codex's notes:
   - structure: step names and order, greyed steps, the bottom line (3 lines at most, bolded criteria), the illness
     script in template order with exactly two Insights, the 5a bands and First step pairing, the clue table, the pause
     point, the treatment ladder with its Raise tier, the When | Do follow-up table, Practice, NBME block, Pairs with,
     Transferable rule;
   - voice: plain labels, "If X, choose Y" rows, row grammar and length, the same words for the same idea across
     briefs (names, aliases, abbreviations from ABBREV.json and ALIASES.json), hedges kept where quoted;
   - layers: what is visible versus hover or systems panel ("Layers, not totals"), "In practice" hovers for guideline
     detail, the board answer visible;
   - the bank: stem length (30 to 40 words, scannable lines), original stems, three reasons per item worded like the
     differential rows, distractors drawn from the differential;
   - density: words above Practice and claim counts against the comparison briefs (a brief far thinner or denser than
     its siblings is a finding to explain, not a failure by itself).
   Each difference is either a defect (fix it before present) or a pattern (Codex does it consistently and the rules
   allow both ways). Patterns go to step 9.
9. **Rule feedback.** Turn every defect kind that a mechanical check could not catch, and every pattern that should be
   fixed one way, into a proposed numbered addition to CODEX_LEAD.md section 7 (the s149 items 19 to 27 are the
   model: the rule, then the case that showed it). Present them to Jonathan in the report as options with a
   recommendation; write the ones he approves into CODEX_LEAD.md and a digest line, before Codex's next launch.
10. **Report.** Re-present with approval.py present only after 1 to 8 pass; the report adds a "Codex audit" section
   (findings by kind, what was fixed, the consistency comparison, the proposed rules). Then ship on "ship".
