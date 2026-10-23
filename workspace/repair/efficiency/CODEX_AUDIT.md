# The S8 audit of Codex-led work (before any ship)

Written 2026-10-21 with CODEX_LEAD.md; run by Claude for s150 (2026-10-22, record in repair/s150/S150.md "Codex
audit"). Since 2026-10-23 (Jonathan: "ill have codex ship") it is run at S8 by a fresh Codex audit task (GPT-6.1 Sol,
xhigh), never the lead's own session, before approval.py present (CODEX_LEAD.md section 5). Claude runs it only when
Jonathan asks. Accuracy is non-negotiable (Jonathan): nothing ships until this audit passes. The auditor writes
repair/sNN/AUDIT.md with every finding by kind; the lead fixes or answers each one and copies the summary into the
batch file under "Audit", so CODEX_LEAD.md section 7 can be tightened.

What the s150 audit caught that three review rounds passed (look for these first): a carried explanation naming a drug
the rebuilt body dropped (MED); a modifiability tag the quote did not support; an explanation implying the commonest
organism was only a skin pathogen; a bottom line that dropped the source's "about"; hover buttons glued to the word
before them; a Pairs with card reading "And"; meta-worded ladder rungs.

1. **State.** Read the State and the batch file. Check both repos are pushed and the batch file records every step the
   lead ran. (A Claude auditor also takes the lock: rewrite the Lead line, push alone.)
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
6. **Reviews.** Read each brief's latest acc receipt against the brief: any claim the auditor finds unsupported that
   the receipt passed is a finding against the review, recorded by role. (A Claude auditor, when Jonathan asks for one,
   instead re-runs the acc lane with the Claude lean-reviewer on each brief, budget permitting.)
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
10. **Report.** Present with approval.py present only after 1 to 8 pass and every fix has had its follow-up round; the
   report adds an "Audit" section (findings by kind, what was fixed, the consistency comparison, the proposed rules).
   Then ship on Jonathan's plain "ship" (CODEX_LEAD.md section 5).
