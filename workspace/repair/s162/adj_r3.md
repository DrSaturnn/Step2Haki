# s162 round 3 adjudication (lead, chat 3, 2026-11-04)

Lanes repair/efficiency/lanes/s162/r3 (spec repair/s162/r3_review_spec.txt; packets packets/s162r3, --since each
part's last judged brief_text). read pc-typical PASS. flags PASS pc-atypical, pc-typical; PASS-IF pc-antichol (1 LOW),
pc-td (1 LOW). acc: see below.

## Not applied (lead, with reason)
- pc-antichol flags LOW 1 (restore "if the dose cannot come down" on the Uses row): reverses read r1 MED 1, a
  study-mode leak (the visible condition names the masked danger-row answer "a lower antipsychotic dose"). The line
  "short-term relief only" is true and narrower; the condition lives in the danger row and in antipsych-effects.
- pc-td flags LOW 1 ("Genotype shows whether the patient is a poor metabolizer"): the Why cell sits beside the masked
  Check "CYP2D6 genotype", so the replacement shows the masked answer (the read r1 F-area rule). "Poor metabolizers
  clear it slowly" is true by the definition of a poor metabolizer; kept.
Both receipts judged the current text, so they stay current unapplied.

## acc (Opus, one lane): PASS pc-atypical, pc-typical; PASS-IF pc-antichol (1 LOW), pc-td (1 LOW)
- pc-antichol acc LOW 1 and flags LOW 1 (the same lost condition): applied as a masked repeat, per the runbook's
  standing call ("A study-mode leak from a repeated table or line: mask the repeat; never delete it"): "Drug-induced
  parkinsonism: short-term relief only, when [mask: the antipsychotic dose cannot come down]" (u5). This supersedes the
  "not applied" call above for pc-antichol.
- pc-td acc LOW 1: verified in the cached Xenazine label (repair/sources/web/6063dbba03c1309b.txt, 5.8 QTc
  Prolongation: "XENAZINE should also be avoided in patients with congenital long QT syndrome and in patients with a
  history of cardiac arrhythmias."). The r1 flags qualifier was wrong; the line now reads "QT prolongation (all three
  labels): avoid with congenital long QT syndrome or QT-related arrhythmias", new fact x12 cited.
After round 3: pc-atypical READY, pc-typical READY. Round 4: pc-antichol and pc-td, acc, read and flags on these two
lines only (spec repair/s162/r4_review_spec.txt).
