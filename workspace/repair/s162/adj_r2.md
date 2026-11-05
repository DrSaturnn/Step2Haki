# s162 round 2 adjudication (lead, chat 3, 2026-11-04)

Receipts filed as repair/migration/spine/reviews/<card>_<part>_r2.md (local/s162/chat2/file_cards.py 2): read PASS
pc-atypical, pc-typical, pc-antichol; read PASS-IF pc-td (3 LOW); flags PASS pc-typical; acc PASS-IF pc-typical (2 LOW).
0 HIGH, 0 MED.

## Applied
- pc-td read LOW 1: "stop or switch, eg clozapine)" -> "stop or switch, for example to clozapine)" ("eg" is not on
  ABBREV.json).
- pc-typical acc LOW 1: S021 (Key point QT line) cites pz2 too (the pimozide label's QT quote).
- pc-typical acc LOW 2: TYP 3 (the key reason of q_d6b90a2a436c98b15996) was in author.py but not built: the shell
  was rewritten only when an item id was missing. author.py now rewrites the bank when an item's text changed; the
  bank carries "and the pimozide label bars it; sudden deaths were reported with clarithromycin". Item version unchanged
  (a reason, not the stem or key; gate passes).
- TYP 7 check (acc and read asked): antipsych-effects teaches the dementia boxed warning ("Boxed warning, first- and
  second-generation alike: higher death risk in older adults with dementia"), so the chip stays on antipsych-effects.

## Not applied
- pc-td read LOW 2 (no visible referent for "when it is untreated"): naming it would show the masked answer; the
  reviewer agrees. LOW 3: no action.

## Round 3 scope
verify after round 2: acc and flags are stale on all four cards (their r1 PASS-IF receipts cannot replay the read MED
edits and the other parts' edits), and pc-typical read is stale on the bank change. Round 3 reviews only the lines
changed since each part last judged: acc x4 (Opus), flags x4 (Sonnet), read pc-typical (Sonnet).
