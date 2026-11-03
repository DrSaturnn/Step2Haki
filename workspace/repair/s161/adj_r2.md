# s161 S5 adjudication, round 2 (lead, chat 4, 2026-11-02)

Receipts filed by local/s161/chat2/file_cards.py 2: acc pc-ssri r2 PASS, pc-other r2 PASS-IF (1 LOW); read mood-anticonv
r7 PASS-IF (5 LOW), pc-ssri r2 PASS-IF (3 LOW), pc-tca r2 PASS-IF (2 LOW), pc-cog r2 FAIL (1 MED 2 LOW), pc-other r2 PASS-IF
(1 LOW); flags pc-ssri r2 PASS, pc-cog r2 PASS-IF (1 LOW), pc-other r2 PASS. Spend round 2: 4 agents, 36 calls, 1.59M.
Pair files local/s161/chat4/<card>_r2.py (cog_r2b.py), applied with local/s160/chat4/ed.py; every card rebuilt
`AX_BATCH=s161 build_brief.py <folder> --verify`: MECHANICAL PASS, 0 FIX, 0 warn; page s3 gate PASS, squeeze 0.

## Accepted
- pc-cog read F(MED A) and flags R1 (memantine titration Why "the dose rises in 5 mg steps to 10 mg a day"): the 10 mg
  read as the target, and the renal row's "5 mg twice daily" then looked like no reduction. Fact m8 was cut mid-sentence;
  now the whole label sentence (cached cf9889272eedaa5c): "The dose should be increased in 5 mg increments to 10 mg/day
  (5 mg twice daily), 15 mg/day (5 mg and 10 mg as separate doses), and 20 mg/day (10 mg twice daily)." Why now "the dose
  rises in 5 mg steps to 20 mg a day" (the "(10 mg twice daily)" tail dropped: outline C1 cap 615 of about 600). The
  flags R1 wording is superseded by this fix, not applied.
- pc-cog read R1 (Alzheimer disease). pc-tca read R1, R2. mood-anticonv read R1 (a true repeat: the Mechanism line keeps
  "2 to 4 weeks"; STANDING "Trim only true repeats"), R2, R4, R5. pc-ssri read R2 ("except with citalopram": the card's
  own torsade note), R3. pc-other acc R1 (phentermine-topiramate contains phentermine (qs1), so the class commit names
  it). pc-other read R2 (modafinil named).
- pc-ssri read lead item 5: item q_61deac008512c99b4e3f key why "the most in its class" removed (no board quote ranks the
  SSRIs: adj_r1 flags F1); now "Dose-dependent QT prolongation; avoided after a recent heart attack".
- pc-ssri read R1 (distractor 2 "With sertraline"): author.py already read "Like sertraline" from chat 3, but the shell
  bank was never rewritten (author.py rewrites it only when an item id is missing). Tool fix: local/s161/chat4/bank_sync.py
  rewrites the shell bank from ITEMS (both copies); diff: only the two item reasons above.

## Rejected (with evidence)
- mood-anticonv read R3 ("the question asks" to "you are asked"): the NBME framing pattern, 11 times on the batch page.
- pc-other read R1 ("modafinil or armodafinil is first line"): the board owner (peds-sleep) names modafinil only; adding
  armodafinil as first line goes beyond it.
- pc-ssri read item 4 (masked fluvoxamine Rule a fragment): the Rule column is terse by design (every Rule cell).
- pc-cog read LOW (rivastigmine "mild-to-moderate" severity): reviewer asked no change; none made.
- Notes, not findings: pc-other owners row naming peds-sleep for hypersomnolence and shift work (unchanged since r1, no
  reviewer finding); phentermine-topiramate cardiovascular wording (no Qsymia quote in the packet; the commit names it as a
  class member only).

## Why round 3
Replay could not carry the receipts: content replacements (a drug name added, an item reason, the memantine number) are
not wording-only for other parts, and acc pc-tca, mood-anticonv and pc-cog and flags pc-tca and mood-anticonv were stale
from the chat 3 fixes. Round 3: acc on all five, read on pc-ssri, mood-anticonv, pc-cog, pc-other, flags on all five.
