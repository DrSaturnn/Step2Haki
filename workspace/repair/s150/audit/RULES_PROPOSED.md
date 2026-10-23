# s150 Claude audit: proposed CODEX_LEAD.md section 7 additions (CODEX_AUDIT item 9)

Status: proposals for Jonathan. Only the ones he approves go into CODEX_LEAD.md section 7 and a digest line, before
Codex's next launch.

## Defect kinds no mechanical check caught (rules, recommended)

28. **A space before every hover button.** Text or a closing tag followed directly by pop() or why() renders as
    "symptomsIn practice". Write `+' '+POP`. s150: myositis rung 1, puncture rung 1 and the brachial Erb row; three
    display rounds passed them (Codex's own S8 note caught one). The golden scfe has one too.
29. **One title per Pairs with clause.** The card renderer reads "A and B: text" as a card for A whose description is
    "And". Carried tail lines count. s150: myositis ("Slipped Capital Femoral Epiphysis and The Limping Child: ...").
30. **A carried line follows the rebuilt body.** When the rebuild drops a drug, number or test from the body, every
    carried line that still names it (bank explanations, reasons, tail) is re-sourced or reduced to the body's wording.
    s150: myositis explanation kept "an NSAID such as indomethacin" (old line L10) after step 7 dropped the agent; no
    fact or card supports it (the audit's one MED).
31. **Fact id letters follow the packet key.** b, u and v mean board sources to every reviewer; reference facts take
    other letters. s150: Scheuermann's b01, b02 and v01 to v09 were AFP and MSD pages.
32. **A modifiability tag needs support.** Mark a trigger non-modifiable only when it is fixed (age, sex, delivery
    events). s150: brachial "Maternal diabetes ... (non-modifiable)".
33. **Bottom-line hedges.** The bottom line keeps the source's "about", "usually" or "may" on a number. s150: myositis
    "after 2 to 4 weeks" for "about two to four weeks after injury".
34. **Plain rung text.** A ladder rung states the action and its condition once; no meta clauses. s150: myositis
    "Consider surgical excision; persistent lesions may be considered after ..."; brachial "... earlier referral is
    separate from the timing of repair".

## Patterns where both ways are allowed today (options; Jonathan decides)

35. **Time course.** Codex draws the chronology as text rows (no bars) in all five briefs; the s149 briefs plot
    horizontal duration bars, matching the standing preference for horizontal duration timelines.
    Recommend: plotted bars wherever the sources give durations; text rows only when they do not.
36. **Clue table wording.** Codex: caption "Clues that change the next step", column "Next best step" (the column
    follows the 2026-10-13 digest). Live: 59 captions read "Clues that change the answer"; 49 tables still say
    "Next move" (Claude drift from the digest). Recommend: caption "Clues that change the answer" everywhere, column
    "Next best step" everywhere, both normalized in one later site-layer batch.
37. **Links to owning briefs.** Codex differentials carry 0 to 3 drawers (s149 disease briefs 7 or 8); Scheuermann's
    tumor and sacroiliitis rows link nowhere (bone-tumors and sjia own them) and it has no Pairs with (15 Claude spine
    briefs also lack one). Recommend: a differential row whose diagnosis has a live brief carries its drawer; every
    disease brief ends with Pairs with.
38. **Legacy tail blocks.** Brachial keeps Management and prognosis, Pearls and four rule panels after Practice; 13
    Claude spine briefs keep similar blocks. Recommend: leave them now; fold them into the spine at each brief's next
    rebuild.
39. **Claude accuracy lane at S8 for Codex batches.** Claude's single acc round found 1 MED and 4 LOW that three Codex
    review rounds passed. Recommend: budget it in every Codex launch (about 2 Opus agents and 45 calls per 5 briefs).

## Tool change offered (not made)
- lint: warn on an sp-pop button whose preceding visible character is not whitespace (rule 28), with an offline test.
