# Voice pass rules

**Task:** rewrite prose in plain, clear, concise clinical voice. Same facts, same meaning, same keyed logic. Shorter is better.

**Scope:** `.dp`, `.rule`, `.pearls`, `.danger`, `.traps` text, and `p.sub` first segment only. Do not touch: `.vignette`, bank items (`ol.bank` and its `li`), tables, `.crit`, ids, attributes, `data-*`.

**Remove:**
- slogans and aphorisms;
- personification ("the urine is the decider", "the phone call is the decoy");
- paired contrasts written for rhythm ("X names the panel, Y names the disease");
- dramatic openers and closers ("The fever is not incidental", "never after it", "everything", "the whole question");
- rhetorical framing about the question itself ("the trap is", "this question tests") unless it is in `.traps`, where one plain sentence per trap is fine;
- filler transitions;
- em dashes in prose.

**Keep:**
- every clinical fact, number, cutoff and named test;
- every bold clinical term (you may reword around it, not drop or rename it). A bold span that is itself a slogan, a full-sentence aphorism or a rhetorical label may be reworded: list its old text in the op as `"reworded_bold": ["<old bold text>"]` (the verifier accepts only declared removals). Keep the rewrite bold if it still carries the key idea;
- standard clinical phrases such as "until proven otherwise";
- the "·" row separators and "`<b>Term</b> — definition`" structure where they already exist (that " — " is structural, the only em dash allowed);
- `.rule` starts with its existing label markup; other block labels (`<span class="lbl">`) stay unless the label itself is a slogan or rhetorical label, in which case reword it and list the old text in `"reworded_label": ["<old label>"]`.

**Model (approved by Jonathan):**
- Before: The phone call is the decoy and the urine is the decider. Every option is on the newborn screen, so a positive screen eliminates nothing. What separates them is that this infant has conjugated hyperbilirubinemia, a large liver, and a non-glucose reducing sugar in the urine after ten days of milk feeds. That triad is galactose-1-phosphate accumulating in a GALT-deficient liver: classic galactosemia. The fever is not incidental. Galactosemia predisposes to Escherichia coli sepsis, and a febrile 10-day-old is septic until cultured — the sepsis workup runs in parallel with the metabolic answer, never after it.
- After: Conjugated hyperbilirubinemia, a large liver, and a non-glucose reducing sugar in the urine after ten days of milk feeds indicate classic galactosemia (GALT deficiency; galactose-1-phosphate accumulates in the liver). Galactosemia predisposes to Escherichia coli sepsis, so start the sepsis workup and antibiotics while stopping lactose.
- Subtitle before: The screen names the panel, the presentation names the disease · handoff · conjugated, big liver, reducing sugar
- Subtitle after: Sick neonate with a positive newborn screen · conjugated jaundice, hepatomegaly, urine reducing sugar

**Learned from GI review:**
- Never state that a test excludes what the brief says needs a different test.
- Keep hedges and quantifiers that set strength ("rather than presumed", "any one of", "until").
- Restate stem facts only as the vignette gives them.
- Pairs-with claims about coverage must match the page.
- Strip internal and workflow text (batch notes, ledger, candidate, verified).
- Reread every changed sentence for grammar.

If a block is already plain, leave it. If you are unsure a rewrite keeps the meaning, leave it and list it.

**Output:** edits JSON (replace ops, anchors unique within the brief) and a report of 3 to 5 lines: blocks changed, blocks left, anything uncertain.
