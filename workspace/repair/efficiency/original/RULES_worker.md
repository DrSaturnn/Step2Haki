# Backfill worker rules (AxBx study page)

You add one UWorld/NBME question's teaching to ONE existing brief. Everything you need is in this packet: these rules, the source question, the brief's current HTML, and the list of brief titles. Do not open skill files or index.html; if something essential is missing, say so in `notes` instead of guessing.

## Content
- Step 2 CK depth. Use the source explanation plus standard Step 2 facts. Leave out specialist detail (named assays, rare genes, subspecialty thresholds). A number that is neither in the source nor standard gets ` ⚠︎` or is left out; never flag standard facts.
- Teach what decides the question: the deciding finding, the cutoff, the tell that separates the key from the tempting distractors. Map each original distractor to why it fails.
- Add only what the brief lacks. Read its tables, criteria, pearls and bank first; extend an existing table row or block before adding a new one. No second table on the same comparison.
- Do not stretch a rule across a group (for example a vaccine or drug restriction that applies to some immunodeficiencies, not all); name the ones it applies to.
- Current guidelines set facts; the source sets the key and framing. If the brief contradicts the source, fix the brief and say so in notes.

## Voice
Plain clinical English, concise, American spelling. When your edit rewrites an existing sentence, fix any slogan or aphorism in it rather than carrying it forward. No slogans, no aphorisms, no emojis. No em dash character in prose; use a colon, comma or semicolon. The page's structural ` &mdash; ` between a term and its definition inside `.crit`, `.pearls`, `.danger` or `.vignette` blocks is allowed. Bold only the deciding words. Captions plain ("X: the differential", "Diagnostic workup"). Never copy vendor text verbatim; paraphrase.

## Page blocks you may add (copy the markup style already in the brief)
`<div class="pearls"><span class="lbl">Label</span> ...</div>`, `<div class="danger"><span class="lbl">Label</span> ...</div>`, a table row `<tr><td>..</td>...</tr>` matching the table's columns, a Diagnostic workup row (Test | Order | Result | What it points to; Order is one of Screen, First, Next, By branch, Supports, Confirms, Cause, Staging, Skip), a trapline copied from an existing `.trapline`, and one sentence appended to the "Pairs with" block naming another brief by its exact title from the list.

## Edits (JSON)
`{"scope":"brief:<id>","op":"insert_before"|"insert_after","anchor":"<text>","text":"<html>","why":"..."}` or `{"scope":"brief:<id>","op":"replace","old":"<text>","new":"<html>","why":"..."}`. Every anchor/old must occur exactly once inside the brief's HTML and must not be inside the `<ol class="bank...">`. Also add the source nids to the brief div with a replace on its opening tag's `data-nid` (or add the attribute). Never put `<li>` in edits; questions go in `items`.

## Items (2 to 4, including the source item)
`{"brief","type","stem","key","companion","d1","d2","lead","src","nid"}`; plain text, no HTML.
- Types: next, dx, test, mech, avoid, screen, stage, claim. Key and both distractors are the same kind of thing.
- `lead` only when the default prompt would misstate the task (defaults: next "most appropriate next step in management?", dx "most likely diagnosis?", test "most appropriate test?", mech "most likely cause, organism, or complication?", avoid "contraindicated or should be avoided?", screen "most appropriate screening or preventive measure?"). NBME test lead-ins: "Which of the following is the most appropriate diagnostic study to obtain at this time?" / "Which of the following laboratory studies is most likely to confirm the diagnosis?".
- The source item: `src` "uworld", `nid` = all its nids space-separated, the original key, the two most tempting original distractors, paraphrased facts.
- Authored items: `src` "authored", `nid` null. Stems describe the patient only, standalone. Distractors are real mimics a classmate would pick. Answer-cue check: key not uniquely longer by more than about 4 characters, parallel grammar. Do not duplicate an item already in the bank.

## Before you finish
Run `python3 /home/claude/axbx/tools/verify_edits.py <your output> --page /home/claude/bench/base/index.html --nids "<source nids>"` and fix every FAIL. Output: a JSON list with one object `{"kind":"backfill","edits":[...],"items":[...],"notes":"..."}`. Final reply: 3 to 6 lines: what you added, item count, any conflict.
