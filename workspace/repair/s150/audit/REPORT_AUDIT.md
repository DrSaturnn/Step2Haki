# s150 approval report after Claude's audit (2026-10-22; supersedes repair/s150/REPORT.md where they differ)

All five briefs READY on the final page (sha256 1b2c138e1bc5...). Approval sheets: 34, in the private repo at
local-only/local/sheets/s150-approval/ (phone, phone-study, desktop, desktop-study). Claude presented in its own
container on 2026-10-22; Jonathan chose on 2026-10-23 to have Codex ship, so Codex presents again on the Mac with the
same sheets (CODEX_LEAD.md section 5) and ships on his plain "ship".

## Decisions needed
None block the ship. The rule options (RULES_PROPOSED.md 35 to 38) are recorded in CODEX_LEAD.md section 7a.

## Audit changes (all reviewed in follow-up round ca2: acc, read, display PASS on all three; flags PASS on two)
- Myositis: explanation "an NSAID such as indomethacin" to "an NSAID for symptoms" (MED; no fact or card supported
  it); bottom line "about 2 to 4 weeks after injury"; rung 3 "Surgical excision may be considered if the lesion
  persists beyond 6 to 12 months"; space before the rung 1 "In practice" button; Pairs with split into one title per
  clause (the SCFE card read "And").
- Puncture: explanation "early superficial cellulitis favors S. aureus or streptococci"; button spacing.
- Brachial: "(non-modifiable)" dropped from the maternal diabetes trigger; rung 4 "Consider nerve surgery when there is
  no improvement by 3 to 9 months"; C5-C6 button spacing (Codex's S8 LOW).
- Scheuermann, torticollis: unchanged; boards.md owner lines for off-topic board-index items.
- Rejected: the DVT reason rewording (the 2026-10-20 rule reuses the row's wording); dropping "2003" from the
  torticollis pathway hover (the AFP article's publication year, kept to date the pathway).
- Disclosed: the flags reviewer reached its call cap before writing brachial's follow-up receipt (relayed PASS, no
  findings); brachial is READY under verify because flags binds facts, outline and live page, none changed.

## Counts
Words above Practice: myositis 811, Scheuermann 641, puncture 755, torticollis 768, brachial 786. Item ids 32 unchanged;
96 reasons; no version change from the audit (explanation-only).

## Reviews and spend
Claude acc review (2 Opus agents, 30 calls): 1 MED and 4 LOW missed by three Codex rounds. Follow-up ca2 (4 agents, 43
calls). Claude reviewers 6 agents, 73 calls, 2.70M tokens; with Codex: 26 of 26 agents, 362 of 405 calls. Claude lead
44.1M tokens. Final checks: gate 39 PASS, render PASS, vendor PASS, preflight 28 answered advisories (unchanged).

## Consistency and rules
See S150.md "Codex audit" and RULES_PROPOSED.md; rules 28 to 35 are now in CODEX_LEAD.md section 7, options in 7a.
