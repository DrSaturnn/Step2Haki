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

**Page-wide decisions (s33, Jonathan; apply to every system):**
- Trap lines are "Option: why": the option name, one colon, then the reason. Never "Option — why". `01_mechanical` already converted the plain cases (`.trapwhy` lines and the `<b>Option</b>` lines under the Distractors label). Where a trap line still has an em dash (the option sits inside a sentence, or the reason has a dash of its own), rewrite it as "Option: why" when the option can be named from the line; otherwise use a colon, semicolon or period. One colon per line: if the reason itself opens with a bold label and a colon (`<b>Desmopressin</b>: <b>skipped tier</b>: correct tier-2 drug...`), make the second one a semicolon or a new sentence.
- No em dashes in prose anywhere, trap lines, Pairs with and pearls included. The only allowed " — " is the structural `<b>Term</b> — definition` in a block with "·" (`&middot;`) rows whose segments start with a bold term: the page turns those rows into a two-column grid, so keep those dashes exactly. In a block with no "·", `<b>Term</b> — text` is prose: use a colon. Brief titles quoted in Pairs with keep their own punctuation (three titles contain an em dash; the verifier allows it).
- The trap section label is "Distractors" (renamed by `01_mechanical`). Keep it. Other labels such as "Decoy note" stay as they are.
- "How NBME framed it" text is final (reviewed in s31). Leave any block labelled "How NBME framed it", and any sentence that starts "How NBME framed it:", exactly as it is, even if it breaks a style rule here. End your `find` before it; if an op must span it, copy it into `with` unchanged. The verifier fails an op that changes it.

**Internal and workflow text: remove wherever seen** (it is not a clinical claim, so it needs no claim-map entry; if you list it, mark it `dropped` with a paraphrase that has no numbers or test names):
- batch notes such as `--- <i>Batch 5, brief 01 · 2026-09-10.</i>`: delete (the verifier ignores their digits);
- "Verified:" in front of a sentence: delete the word;
- "Store the discriminator as a question:": keep the question, introduced by "Ask:" (the GI precedent: "Ask: is the baby making urine?");
- "Candidate twin — confirm: ..." and "... are not yet written": keep any named conditions and their discriminating question as "Related conditions without their own brief: X (ask: ...?)"; drop the proposal about writing a brief;
- "owns", "takes over" (and "is the twin for" used as ownership) in Pairs with: "covers" (the GI precedent: "Part I <b>X</b> covers the child whose gait is normal; this brief covers ...");
- provenance tags "(clinic ledger)", "clinic-ledger", "exam ledger", "(in-context)", "(all in-context)", "in-context:": delete the tag and keep the fact ("(in-context: CBC is typically normal in RDS)" becomes "; the CBC is typically normal in RDS"). Keep ⚠︎ where it marks an unverified specific; "exam ledger versus clinic ledger" becomes "the exam answer versus clinical practice";
- any other note about the page, the batch, the ledger, a candidate or a verification step.
Pairs-with coverage claims must still match the page: name only briefs that exist, by their exact title.

If a block is already plain, leave it. If you are unsure a rewrite keeps the meaning, leave it and list it.

**Output:** edits JSON (replace ops, anchors unique within the brief) and a report of 3 to 5 lines: blocks changed, blocks left, anything uncertain.
