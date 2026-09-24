<!-- provenance: board-brief/SKILL.md sha256 9de28dda41a95a7d535e44f7c953e463467962e73cc00cce9bf612839756eaa9 ; study-page-builder/SKILL.md sha256 e3052755508fa3dfd28fd72ab44f53122ab5fdc36ab304e411ea47efb31414c9 ; condensed 2026-09-24, amended after audit -->
# Worker rules: backfill one UWorld question into one existing brief

Deliverable: one `edits.json` (format below) and a 3 to 6 line report.

**Scope**
- W1 Default to this brief. Add only what the question adds: a row or cell, a variant item, one exception, traplines. A new question or miss is not a new objective; if it needs a distinct uncovered objective, stop and say so.
- W2 Fast rule plus at most one exception that changes the answer. Put test / confirm / next-step / organism / mechanism distinctions into existing cells, rows or rungs where relevant. No second table; no mini-brief for a mimic (link its owner). A row whose cells do not discriminate becomes a sentence. Deeper reasoning goes after reveal.
- W3 Every sentence states the rule, a discriminator, a needed causal step or a boundary; if removing it loses nothing, delete it.
- W4 Do not change title, ids, `data-shelf`, `data-bp`. Every word of the title stays true of every item you add.
- W5 The brief keeps the one stem its `.dp` argues about. The new question's case goes into the bank as an item, never into the `.vignette`.

**Sources and facts**
- W6 Paraphrase; never paste vendor text (the exact question asked may be quoted). No vendor figures: redraw as a table, a spine, or original inline SVG (`.figure` + `.fignote`) only when the branching is the content.
- W7 Current guidelines set facts; NBME sets key and framing; then UWorld; then authored. Never replace source content from memory: flag the discrepancy with ⚠︎ and list it in the report. No external literature audit; never invent support.
- W8 Numbers come from the supplied explanation, attached to the same quantity (digit-collision check); otherwise ⚠︎ in place. ⚠︎ only for memory-sourced or unverified specifics; never drop an existing ⚠︎ without real verification.
- W9 A negative test lowers probability per its performance; a completed tier closes that tier, not every test; culture-before-antibiotics is for suspected joint infection in a stable patient (unstable: empiric treatment now, cultures as feasible).
- W10 Ladder triggers are numbers or named failures, never "if no improvement" (else "trigger unknown — study gap"); add stop or de-escalation criteria when testable.
- W11 Explanations lead with the decisive finding and why it favors the key; address the closest competitor when useful. Never invent a mechanism for an association.
- W12 Learner performance (chosen option, time, miss cause) never goes on the page; report it labeled reported, inferred or unknown.

**Bank items** (`add_item`; ids are generated)
- W13 Type = what the three options already are: `next dx test mech avoid screen stage claim` (claim sparingly). Key and both distractors are one category. `avoid` keys the forbidden act; its distractors are safe choices.
- W14 Distractors: real entities from this brief's differential, ladder or competing tests; a mimic a classmate would weigh; worse for a one-clause reason; not a synonym or subtype; none on more than ~60% of the brief's items. `mech`/organism items: source-supported alternatives of the same kind; never invent rows to hold them. Fail codes: F1 not an entity, F2 same condition, F3 category mismatch, F4 equally defensible, F5 repeated tell, F6 nobody would pick it.
- W15 One best answer. An equally defensible alternative is fixed with supported facts, else `"status": "needs_repair"`. Missing source facts: `"status": "needs_source"`.
- W16 Stems carry independent context (review shuffles: never "Same patient..."), state the deciding fact, never advertise an option. `next`: one rung too low and one too high or out of sequence. Keys never name a subtype the stem cannot distinguish.
- W17 `lead_in` when the type's generic prompt misstates the task; one prompt, no second question in the stem.
- W18 Labels complete and parallel (dose, duration, timing, anatomy, negatives); no commentary in a choice. Cue review on every option set: length, grammar, specificity, repeated stem words, abbreviation, case, trailing punctuation. Fix the key first; never pad or strip a deciding qualifier. No `data-rationale-*`.
- W19 No duplicate decisions (`verify_edits` flags near-duplicates). An untyped `<li>` is a prose note: no ids, distractors or prompt (add it with `insert_after`, not `add_item`).
- W20 Existing items: never delete, never edit ids. The key is arrow segment 2, not the first `<b>`. Any meaning change (stem, key or distractor) needs `set_attr data-item-version "+1"`; formatting alone does not. Preserve `data-src`, `data-nid`, `data-recon` and unknown attributes.

**Markup**
- W21 In `.pearls .danger .dp .rule .crit .vignette`, ` · ` splits facts and `<b>Term</b> — definition` builds the masked grid. No `·` mid-sentence; lists inside a definition use commas. `.rule` stays last before `.traps`.
- W22 `.crit` holds criteria only (no epidemiology, treatment or supporting features), tested criterion first.
- W23 Tables: keep the caption (or h5) and any `data-mask`; no rowspan or colspan; never `data-mask` on a `Tier` table; the last column masks when named as a verdict.
- W24 `.vignette`: paraphrased, never masked, `Pt · Labs · Imaging · Q` lines, about 110 words at most; no option letters or vendor percentages there or in traplines.
- W25 Every original distractor of the source question gets its own task-specific trapline: `<div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">{option} — {why it fails here}</span></div>`. Pill only when a species fits (p-salient p-slot p-class p-attr p-mirror p-seq p-number p-trump p-uniform p-test); upgrade bare pills you touch.
- W26 Pairs with: `<b>` holds the partner's exact `<h4>`; an absent partner goes in `<i>`; store the discriminator as a question; name the needed reverse mention in the report.
- W27 Escape `& < >`; inline tags only `b i span sup sub`; no markdown, emoji or escaped tags. A named scale owes its components in place (enumerate, or `.scaleref data-scale` to the components, not a ladder); never invent a target.

**Voice**
- W28 Concise tutor to a colleague; lead with the decision; bold only deciders; concrete subjects, causal verbs; "less likely", "not the appropriate next step" or "excluded" as the evidence supports. Plain captions ("X: the differential", "Diagnostic workup"). No emojis; no em dashes in prose (the structural ` — ` is required). Step 2 depth.
- W29 "rewrite slogans you touch": an aphorism in a sentence you edit becomes plain causal prose.
- W30 "do not stretch a restriction across a group": state a rule only for the members it applies to.

**Process**
- W31 Work only from this packet; do not open the skill files or the full page. If something essential is missing, say so rather than guess.
- W32 Anchors verbatim and unique inside the brief; run `verify_edits` until PASS. Report: what changed; boundary-pass result (does a supported change defeat the fast rule?); ⚠︎ and discrepancy list; cue-review dispositions; reverse links or candidate twins; anything unresolved.
