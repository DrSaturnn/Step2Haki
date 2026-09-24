# Worker rules: backfill one UWorld question into one existing brief

Condenses (re-check when either hash changes: `sha256sum <file>`; coverage map in RULES_coverage.md):
- `board-brief/SKILL.md` sha256 `9de28dda41a95a7d535e44f7c953e463467962e73cc00cce9bf612839756eaa9`
- `study-page-builder/SKILL.md` sha256 `e3052755508fa3dfd28fd72ab44f53122ab5fdc36ab304e411ea47efb31414c9`
(skills folder: `/root/.claude/skills/synced/<account>/`). Condensed 2026-09-24. Deliverable: one `edits.json` (format below) plus a 3 to 6 line report.

**Scope**
- W1 Default to this brief. Add only what the question adds that the brief lacks: a discriminator row or cell, a variant item, one exception, a trapline. A new source question or another miss is not a new objective. If the question needs a distinct, uncovered objective, stop and say so; do not build a new brief.
- W2 Fast rule plus at most one relevant exception that changes the answer. Put initial test / confirmatory test / next step / organism / mechanism distinctions into existing table cells, rows or ladder rungs, only where relevant. No second table; no mini-brief for a mimic (link its owning brief). Deeper reasoning goes after reveal (companion segment, table cells), not in the fast rule.
- W3 Every sentence states the rule, a discriminator, a needed causal step or a boundary. Removal test: if nothing is lost, delete it.
- W4 Do not change the title, ids, `data-shelf` or `data-bp`. Every word of the title must stay true of every item you add.

**Sources and facts**
- W5 Paraphrase; never paste vendor text (the exact question asked may be quoted). Never embed vendor figures; redraw only as a table or spine.
- W6 Precedence: current guidelines set facts; NBME sets key and framing; then UWorld; then authored. The supplied explanation and this brief are your references for what is scored. No external literature audit; never invent support.
- W7 Numbers: from the supplied explanation (preserve the quantity it attaches to: digit-collision check), otherwise ⚠︎ in place. ⚠︎ only for memory-sourced or unverified specifics; never drop an existing ⚠︎ without real verification.
- W8 Guards: a negative test lowers probability per its performance; a completed tier closes that tier, not every test; culture-before-antibiotics applies to suspected joint infection in a stable patient (unstable: empiric treatment now, cultures as feasible). Triggers and gates are numbers or named failures, never "if no improvement"; otherwise write "trigger unknown — study gap".
- W9 Learner performance (chosen option, time, miss cause) never goes on the page. Report it outside, labeled reported, inferred or unknown.

**Bank items** (`add_item`; ids come from idgen automatically)
- W10 The type is what the three options already are: `next` `dx` `test` `mech` `avoid` `screen` `stage` `claim` (claim sparingly, never to dodge a fitting type). Key and both distractors are the same category. `avoid`: key the forbidden act; distractors are safe choices.
- W11 Distractors: real clinical entities from this brief's differential, ladder or competing tests; a mimic a prepared classmate would weigh; less appropriate than the key for a one-clause reason; not a synonym or subtype of the key; no distractor on more than ~60% of the brief's items. Fail codes: F1 not an entity, F2 same condition, F3 category mismatch, F4 equally defensible, F5 repeated-distractor tell, F6 nobody would pick it.
- W12 One best answer. An equally defensible alternative is repaired with supported facts in the stem, or the item gets `"status": "needs_repair"`.
- W13 Stems carry enough independent context (review shuffles items: never "Same patient..."); state the deciding fact; never advertise an option ("with MRI among the options"). `next` distractors: one rung too low and one too high or out of sequence when the ladder allows. Keys never name a subtype the stem cannot distinguish.
- W14 Add `lead_in` when the type's generic prompt misstates the task (initial vs confirmatory test, organism, mechanism). One prompt; no second question in the stem.
- W15 Labels complete and parallel: keep dose, duration, timing, anatomy, negatives; no teaching commentary inside a choice. Answer-cue review on every option set: length, grammar, specificity, repeated stem words, abbreviation style, sentence case, trailing punctuation. Fix the key first; never pad distractors or strip a deciding qualifier. Do not add `data-rationale-*` (no renderer consumes it).
- W16 No duplicates: if the page already asks the same decision, change the deciding variable or skip it. `verify_edits` flags near-duplicates.
- W17 Existing items: never delete, never edit ids. The keyed answer is arrow segment 2, not the first `<b>` (bold is sometimes in the stem). Changing a key or distractor label needs `set_attr data-item-version "+1"`; capitalizing or formatting alone does not.

**Markup inside the brief**
- W18 In `.pearls` `.danger` `.dp` `.rule` `.crit` `.vignette`, ` · ` splits facts and `<b>Term</b> — definition` builds the masked grid. Never put `·` mid-sentence; lists inside a definition use commas. Keep `.rule` last before `.traps`.
- W19 Tables: keep the caption (or h5) and any `data-mask`; no rowspan or colspan; never add `data-mask` to a `Tier` table. The last column masks when named as a verdict (tell, next step, management, diagnosis...).
- W20 `.vignette` stays paraphrased and unmasked; labeled `Pt · Labs · Imaging · Q` lines; no option letters or vendor percentages in the Q line or traplines.
- W21 Traplines: `<div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Option: one-clause reason it tempts and fails.</span></div>`. Species: p-salient, p-slot, p-class, p-attr, p-mirror, p-seq, p-number, p-trump, p-uniform, p-test. Leave unnamed rather than mislabel; upgrade a bare pill you touch.
- W22 Pairs with: `<b>` holds the partner's exact `<h4>`; a partner that does not exist goes in `<i>`; store the discriminator as a question. Name the reverse mention the partner needs in your report.
- W23 Escape `&` `<` `>` in text; inline tags only `b i span sup sub`. No markdown, emoji or escaped tags. A named scale owes its components in place (enumerate, or `<span class="scaleref" data-scale="id">` pointing at the components, never at a ladder); never invent a target.

**Voice**
- W24 Concise tutor to a colleague; lead with the decision; bold only deciding words; concrete subjects and causal verbs; "less likely", "not the appropriate next step" or "excluded" as the evidence supports. Plain captions ("X: the differential"). No emojis; no em dashes in prose (the structural ` — ` in Term — definition is required). Step 2 depth.
- W25 "rewrite slogans you touch": an aphorism already in a sentence you edit becomes plain causal prose.
- W26 "do not stretch a restriction across a group": state a contraindication or rule only for the members it applies to.

**Process**
- W27 Work only from this packet. Do not open the skill files or the full page. If something essential is missing, say so instead of guessing.
- W28 Write edits per the format below (anchors verbatim and unique inside the brief), run `python3 tools/verify_edits.py <edits.json>` and loop until PASS. Report outside the brief: what changed, ⚠︎ list, cue-review dispositions, candidate twins or reverse links, anything unresolved.
