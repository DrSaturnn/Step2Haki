<!-- provenance: board-brief/SKILL.md sha256 9de28dda41a95a7d535e44f7c953e463467962e73cc00cce9bf612839756eaa9 ; study-page-builder/SKILL.md sha256 e3052755508fa3dfd28fd72ab44f53122ab5fdc36ab304e411ea47efb31414c9 ; condensed 2026-09-24, amended after audit -->
# Backfill worker rules (AxBx study page)

You add one UWorld/NBME question's teaching to ONE existing brief. Everything you need is in this packet: these rules, the source question, the brief's current HTML, the list of brief titles, and the edit format. Do not open skill files or index.html; if something essential is missing, say so in your report instead of guessing.

## Content
- Step 2 CK depth. Use the source explanation plus standard Step 2 facts. Leave out specialist detail (named assays, rare genes, subspecialty thresholds). A number that is neither in the source nor standard gets ` ⚠︎` or is left out; never flag standard facts.
- Teach what decides the question: the deciding finding, the cutoff, the tell that separates the key from the tempting distractors. Map each original distractor to why it fails.
- Add only what the brief lacks. Read its tables, criteria, pearls and bank first; extend an existing table row or block before adding a new one. No second table on the same comparison.
- Do not stretch a rule across a group (for example a vaccine or drug restriction that applies to some immunodeficiencies, not all); name the ones it applies to.
- Current guidelines set facts; the source sets the key and framing. If the brief contradicts the source, fix the brief and say so in your report.

## Voice
Plain clinical English, concise, American spelling. When your edit rewrites an existing sentence, fix any slogan or aphorism in it rather than carrying it forward. No slogans, no aphorisms, no emojis. No em dash character in prose; use a colon, comma or semicolon. The page's structural ` &mdash; ` between a term and its definition inside `.crit`, `.pearls`, `.danger` or `.vignette` blocks is allowed. Bold only the deciding words. Captions plain ("X: the differential", "Diagnostic workup"). Never copy vendor text verbatim; paraphrase.

## Page blocks you may add (copy the markup style already in the brief)
`<div class="pearls"><span class="lbl">Label</span> ...</div>`, `<div class="danger"><span class="lbl">Label</span> ...</div>`, a table row `<tr><td>..</td>...</tr>` matching the table's columns, a Diagnostic workup row (Test | Order | Result | What it points to; Order is one of Screen, First, Next, By branch, Supports, Confirms, Cause, Staging, Skip), a trapline copied from an existing `.trapline`, and one sentence appended to the "Pairs with" block naming another brief by its exact title from the list.

## Edits (`{"edits": [...]}`, format at the end of the packet)
`{"op":"insert_before"|"insert_after","brief":"<id>","anchor":"<text>","html":"<html>","note":"why"}` or `{"op":"replace","brief":"<id>","find":"<text>","with":"<html>","note":"why"}`. Every anchor/find must occur exactly once inside the brief's HTML and must not be inside the `<ol class="bank...">`. Also add the source nids to the brief div: `{"op":"set_attr","target":"<id>","attr":"data-nid","value":"<nids>"}`, where the value is the brief's existing `data-nid` (if any) plus the source nids, space-separated. Never put `<li>` in edits; questions go in `add_item` ops.

## Items (2 to 4, including the source item), as `add_item` ops in the same `edits` list
`{"op":"add_item","brief","type","stem","answer","companion","d1","d2","lead_in","src","nid"}`; plain text, no HTML, no arrows (the applier writes them).
- Types: next, dx, test, mech, avoid, screen, stage, claim. Key (`answer`) and both distractors are the same kind of thing.
- `lead_in` only when the default prompt would misstate the task (defaults: next "most appropriate next step in management?", dx "most likely diagnosis?", test "most appropriate test?", mech "most likely cause, organism, or complication?", avoid "contraindicated or should be avoided?", screen "most appropriate screening or preventive measure?"). NBME test lead-ins: "Which of the following is the most appropriate diagnostic study to obtain at this time?" / "Which of the following laboratory studies is most likely to confirm the diagnosis?".
- The source item: `src` "uworld", `nid` = all its nids space-separated, the original key as `answer`, the two most tempting original distractors as `d1`/`d2`, paraphrased facts.
- Authored items: `src` "authored", omit `nid`. Stems describe the patient only, standalone. Distractors are real mimics a classmate would pick. Answer-cue check: key not uniquely longer by more than about 4 characters, parallel grammar. Do not duplicate an item already in the bank.

## Before you finish
Run `python3 tools/verify_edits.py <your edits file>` from the repo root and fix every FAIL until it prints PASS. It does not check nids: confirm yourself that the source item's `nid` and the brief's `data-nid` carry every source nid. Output: the edits file at the path the packet names, one `{"edits":[...]}` object holding the page edits, the `set_attr` and the `add_item` ops. Final reply: 3 to 6 lines: what you added, item count, any conflict.

## Added after rebuild audit (untested in pilot)
From the rebuilt sheet's audit against board-brief and study-page-builder (W numbers in brackets); only what the rules above do not already say. If one seems to conflict with the rules above, the rules above win.
- **Uncovered objective** [W1]: a new question is not a new objective. If the source needs a distinct objective this brief does not cover, stop and say so in the report instead of building it here.
- **One exception** [W2]: the fast rule plus at most one exception that changes the answer.
- **No mimic mini-brief** [W2]: do not build out a mimic inside this brief; link the brief that owns it.
- **Rows must discriminate** [W2]: a table row whose cells do not separate the entities becomes a sentence.
- **Fixed identity** [W4]: do not change the title, ids, `data-shelf` or `data-bp`. Every word of the title stays true of every item you add.
- **Vignette untouched** [W5]: the brief keeps the one stem its `.dp` argues about; the new question's case goes into the bank as an item, never into the `.vignette`.
- **No vendor figures** [W6]: never reproduce a vendor image or figure; if its branching is the content, redraw it as table rows or text.
- **Number binding** [W8]: attach each number to the same quantity the source gives it (no digit collisions). Never remove an existing ⚠︎ without real verification.
- **Test-result logic** [W9]: a negative test lowers probability according to its performance; a completed tier closes that tier, not every test; culture before antibiotics is for suspected joint infection in a stable patient (unstable: empiric treatment now, cultures as feasible).
- **Ladder triggers** [W10]: escalation triggers are numbers or named failures, never "if no improvement" (else "trigger unknown: study gap"); add stop or de-escalation criteria when testable.
- **No invented mechanism** [W11]: never supply a mechanism for an association the source does not explain.
- **No learner performance** [W12]: the option chosen, time taken or cause of a miss never goes on the page; report it labeled reported, inferred or unknown.
- **Avoid polarity** [W13]: in an `avoid` item the key is the forbidden act and both distractors are safe choices. Use `claim` sparingly.
- **Distractor sourcing** [W14]: distractors come from this brief's differential, ladder or competing tests; never a synonym or subtype of the key; no single distractor on more than about 60% of the brief's items. `mech`/organism items use source-supported alternatives of the same kind; never add table rows just to hold them.
- **One best answer** [W15]: fix an equally defensible alternative with supported facts, else give the item `"status": "needs_repair"`; if the source lacks the facts, `"status": "needs_source"`.
- **Stem discipline** [W16, W17]: the stem states the deciding fact and never advertises an option; one prompt, no second question in the stem; the key never names a subtype the stem cannot distinguish. In a `next` item one distractor is a rung too low and one too high or out of sequence.
- **Full cue review** [W18]: option labels complete and parallel (dose, duration, timing, anatomy, negatives); no commentary in a choice. Check every option set for length, grammar, specificity, repeated stem words, abbreviation, case and trailing punctuation; fix the key first; never pad or strip a deciding qualifier. No `data-rationale-*` attributes.
- **Grid markup** [W21]: in `.pearls .danger .dp .rule .crit .vignette`, ` · ` (or `&middot;`) separates facts and `<b>Term</b> &mdash; definition` builds the masked grid; no `·` mid-sentence; lists inside a definition use commas. `.rule` stays last before `.traps`.
- **Criteria only** [W22]: `.crit` holds criteria only (no epidemiology, treatment or supporting features), tested criterion first.
- **Table integrity** [W23]: keep the caption (or h5) and any `data-mask`; no rowspan or colspan; never `data-mask` on a `Tier` table; the last column masks when named as a verdict.
- **Trapline per distractor** [W24, W25]: every original distractor of the source question gets its own task-specific trapline: `<div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">{option} &mdash; {why it fails here}</span></div>`. Pill only when a species fits (p-salient p-slot p-class p-attr p-mirror p-seq p-number p-trump p-uniform p-test); upgrade bare pills you touch. No option letters or vendor percentages in traplines.
- **Pairs-with format** [W26]: `<b>` holds the partner's exact title; a partner not on the page goes in `<i>`; phrase the discriminator as a question; name the reverse mention the partner needs in the report.
- **Escaping and tags** [W27]: escape `& < >`; inline tags only `b i span sup sub`; no markdown or escaped tags.
- **Named scales** [W27]: a named scale owes its components in place (enumerate them); never invent a target.
- **Calibrated exclusion** [W28]: write "less likely", "not the appropriate next step" or "excluded" as the evidence supports.
- **Report extras** [W32]: within the 3 to 6 lines, add when present: whether a supported change defeats the fast rule, each ⚠︎ and discrepancy, cue-review fixes, reverse links or candidate twin items, anything unresolved.
