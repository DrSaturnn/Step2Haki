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

**Round 2 (after Jonathan's review of the live GI sample; no drift is the top priority):**
- One idea per sentence, about 25 words at most. Split arrow chains: at most one → per sentence. Where a block lists parallel items (for example three benign complaints), a "·"-separated row list is allowed in `.dp`, `.pearls`, `.danger` and `.rule`.
- No framing or meta sentences. Nothing that talks about the answer, the tier, the finding, the question, the stem or the decision instead of stating the clinical fact. "X and Y set the answer", "Two mimics change the tier" and "Parental distress is not a finding" become what to do, e.g. "Reassure; a thriving infant needs no formula change, suppository or stool workup."
- Acronyms: at first use within each block, bold the acronym and write it out in parentheses, unbolded: `<b>FPIES</b> (food protein-induced enterocolitis syndrome)`. Later uses in the same block stay plain. Common units and immunoglobulin names (IgE, IgA) count as acronyms only if a learner might not expand them; list every acronym you skip in your report. Do not create a "`<b>Term</b> — definition`" pattern by accident (never follow the bold acronym with " — ").
- Remove emphasis bold on non-terms (for example a bold "and"), and declare it in `reworded_bold`.
- The approved galactosemia `.dp` text stays unless it breaks a rule above.

**Drift protocol (mandatory; the verifier checks it):** every replace op carries a claim map.
- `"claims"`: every atomic clinical claim in the OLD text, one short sentence each, with exactly one of:
  `"to"`: the NEW sentence that now carries it, quoted exactly as visible text (tags stripped); or
  `"carried_by"`: a quoted passage elsewhere in the same brief (another block, a table cell or a bank item) that already states it; or
  `"dropped"`: the reason, allowed only for non-clinical framing. A dropped claim may not contain a number, drug, test or cutoff.
- `"new_claims"`: every clinical claim in the NEW text, each with `"from"`: the exact `"claim"` text of the old claim it came from, or `"expansion"` for a written-out acronym (the expansion must be the standard one).
- The verifier fails an op with no claims list, an unmapped claim, a quote that is not in the new brief, a new claim without `"from"` (or with a `"from"` that matches no old claim), or a dropped claim carrying clinical content. `--report` prints old text, new text and the claim map for the reviewer.

If a block is already plain, leave it. If you are unsure a rewrite keeps the meaning, leave it and list it.

**Output:** edits JSON (replace ops, anchors unique within the brief) and a report of 3 to 5 lines: blocks changed, blocks left, anything uncertain.
