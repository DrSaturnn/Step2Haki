# CARD_SPEC: the Psych Pharmacology class card (s159, 2026-10-30)

Project copy claude/CARD_SPEC.md. Jonathan's decisions behind it are DECISIONS_DIGEST 2026-10-30 ("psych pharm
section redo", "psych pharm mockup decisions") and the s159 launch line; the plan is claude/pending/PSYCH_PHARM_V2.md
and PSYCH_PHARM_BATCHES.md. The model card is MAOIs (mockup v3, ported in s159; repair/pilots/psych-pharm/ and the
live card pc-maoi once shipped). This file is hashed into card receipts only (tools/spine/verify.py "specs" for a brief
with data-entry="card"); STANDING_DIRECTIONS.md is not edited for cards until a batch that re-reviews every brief.
Every rule in STANDING_DIRECTIONS that is not about the decision spine still applies to cards (accuracy, sources,
board answer first, "In practice:" hovers, bold key words, hovers on touch, layers not totals, masks, theme tokens,
other names, abbreviations, no emojis, no em dashes).

## 1. What a card is
- One short card per drug class, grouped under the Psych Pocket headers in the standalone sidebar and page section
  "Psych Pharmacology" (after Psychiatry & Behavioral Health): 01 Antidepressants (SSRIs, SNRIs, Other
  antidepressants, TCAs, MAOIs); 02 Antipsychotics (Atypical, Typical, Anticholinergic, Tardive dyskinesia agents);
  03 Mood and cognition (Lithium and anticonvulsants, Cognitive agents); 04 Anxiety and benzodiazepines
  (Benzodiazepines, Other anxiety agents); 05 ADHD and sleep (ADHD, Sleep agents, Orexin antagonists); 06 Substance use
  and other (Substance use and cessation, Other agents). 18 cards.
- A card holds what the drug does. The choice of drug stays in the disease briefs and is reached through "Where the
  choice is made". No numbered steps, stepper, differential, workup, pause point or bottom line.
- Content: what the pharm documents show (Psych Pocket 1.7.2, the Medication List, Caplan and Stern 2008), plus what
  Step 2 tests about these drugs that the documents leave out. The documents are a seed only and are never cited:
  every fact is checked against a board source (NBME, UWorld, AnKing) or a primary source (FDA label on DailyMed,
  MSD Manual, StatPearls, guideline). A document line that is outdated is corrected and the correction labeled ("In
  practice:" hover or a note naming what changed). A document line with no board or primary source found is kept
  with the unverified mark (span.pc-uv, "⚠︎ pharm document line; no board source found yet"), never silently dropped.
- Markup: `<div class="brief sp pc" id="pc-<class>" data-entry="card" data-lens="psych" data-spine="2"
  data-shelf="psych" data-bp="behav">`. Ids: pc-<class>; an s157 brief that maps to exactly one card keeps its id
  (adhd-meds, sud-meds, mood-anticonv). Ids are immutable at the ship.

## 2. Section order (the gate's card-format check holds the structure)
1. Class tag `p.pc-grp` ("01 Antidepressants · class card"), title `h4` (the class), subtitle `p.sub` (the
   class's long name, then the drugs, joined by " · ").
2. **Key point** (`div.dp`, block `keypoint`): 2 to 4 lines, each bolding its key words; the one or two things the
   board asks about the class, with the action.
3. **Drug rows** (`div.sp-script.sp-s2.pc-script`, block `script2` with cls "pc-script"): rows Drugs, Mechanism,
   Uses, Adverse effects (withdrawal or discontinuation included), in that order; a class may add Monitoring or
   Other only when a fact needs it. Drugs: one line per drug, generic name bold, trade name in `span.pc-tn`, then a
   short qualifier. Mechanism lines use the arrow (Spine A) from cause to effect. Uses names the board uses and points
   to the owning disease brief with a drawer where the choice lives there.
4. **Danger rows** (`div.sp-rows.pc-blocks`, block `rows` with cls "pc-blocks"), when the class has a dangerous
   reaction the board tests (tyramine crisis, serotonin syndrome, priapism, seizures): source label = the reaction,
   finding = how it looks and what sets it off, commit = "If ..., choose ..." with the answer masked; a `p.pc-note`
   extra for the one trap to remember. A reaction owned by another brief carries a drawer chip to it.
5. **Toxicity and withdrawal timeline** (`figure.lcw.pc-lcw`, block `lcw`), when the class has timed toxicity,
   overdose, withdrawal or discontinuation windows: hours or days axis ("not to scale" when it is not), event names
   masked (mask "name"), one bar per window, a "Shows" line per row.
6. **Interactions table** (`div.sp-dx.pc-tbl`, block `table` with cls "sp-dx pc-tbl"), heads Combined with |
   Result | Rule, Rule masked; when the class has board-tested interactions.
7. **Washout, diet or monitoring-window timeline** (second `figure.lcw.pc-lcw`), weeks axis, window text masked
   (mask "win"), a "Why" line per row; when the class has washouts or timed limits.
8. **Monitoring table** (`div.sp-dx.pc-tbl`), heads When | Check | Why, Check masked; when the class has monitoring.
9. **Where the choice is made** (`div.pc-owners`, block `owners`): one line per decision owned elsewhere, each ending
   in a drawer to the owning brief (or card). At least one.
10. **How NBME framed it** (`div.pc-nbq`): only when a logged NBME item belongs to the class (repair/nbme/misses.csv,
    source nbme, subject the class's drug effect); never an empty block. How a card shows an NBME item owned by
    another brief is decided before B2 (PSYCH_PHARM_BATCHES.md section 6).
11. **Practice**: the card's own bank (`h5.authored-hdr` "Practice", `ol.bank.authored`), at the end of the card.
    Items from the retired s157 brief move here with ids unchanged; new items reach about three per card where the
    board sources test that much. Items follow the brief set rules (three choices, one reason per choice, original
    30 to 40 word stems).

Sections 4 to 8 and 10 appear only when the class has that content; the order never changes. No sources line under
the card (default off, 2026-10-30).

## 3. Timelines
- Bar timelines only, in the site's withdrawal-chart style (figure.lcw window rows, as substance's alcohol
  withdrawal chart); never the dot-on-line sp-on style.
- Toxicity and withdrawal onset in one chart (hours or days); washouts and diet or monitoring windows in a second
  chart (weeks), when the class has them.
- Tick labels repeat on every row, the same ticks down one chart (one axis per chart); the first tick is 0.
- Times come from a board source; else a primary source (label, StatPearls) named in the batch report. A board answer
  that differs from a label is taught, with the label in an "In practice:" hover.
- One owner per timed window: a window is drawn once on the card; a table that needs it points to the timeline
  ("washout as in the timeline") rather than repeating the number.
- Recall mode: the onset chart masks the event names, the washout chart masks the window text; bars stay unblurred
  (2026-10-30 default), as in the live substance chart.

## 4. Trade names
- Shown only when a current FDA label on DailyMed carries the name (checked at the build; the label's setid and
  revision date in facts). A name the documents list without a current label is left out (Psych Pocket warns its
  trade names "may be historical").

## 5. Words
- About 420 words above the bank for the MAOI card; cap about 600 (outline_check C1, soft: an overage for
  board-keyed content is listed in "cap_overage" for Jonathan). Layers, not totals: board-keyed facts stay visible,
  supporting detail moves into hovers; nothing is cut for length.

## 6. Sidebar and section
- Sidebar section `div.sect.pc-sect` "Psych Pharmacology" after Psychiatry, its count the live cards; six numbered
  `div.navsub` groups; every card listed in its group, live cards as plain links, planned cards greyed
  (`a.pc-plan`, linking to the section head #psych-pharm) until each card ships (2026-10-30 default).
- Page section `h3.system#psych-pharm` "Psych Pharmacology" with its system note, after the last Psychiatry brief;
  the cards follow in sidebar order.
- Retiring an s157 brief: its items ride in the cards' shells (ids unchanged), then apply_edits retire_brief removes
  it, keeps its id as an alias span before the card that best inherits it, and drops its nav link; drawers that pointed
  to it are retargeted to the owning card.
