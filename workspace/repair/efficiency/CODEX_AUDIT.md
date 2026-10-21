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
8. **Report.** Re-present with approval.py present only after 1 to 7 pass; the report adds a "Codex audit" section
   (findings by kind, what was fixed). Then ship on "ship".
