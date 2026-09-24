# Edit format (edits.json)

One JSON file per worker or task: `{"edits": [op, op, ...]}`. Ops run in order; each sees the result of the one before. The applier (`tools/apply_edits.py`) splices by offset, so bytes outside the edited ranges never change. Save batch files as `repair/sNN/NN_<brief>.json`; `repair/build.py sNN` applies them in name order.

Rules
- Anchors (`find`, `anchor`) are verbatim snippets of the current HTML, entities included (`&amp;`, `&middot;`, `&gt;`). Each must occur **exactly once inside its brief** and must lie **outside the brief's `ol.bank`**; otherwise the op fails and nothing is written. Items change only through `add_item` and `set_attr`.
- Never delete a brief or an item. Never edit an id. Any meaning change to an item (stem, keyed answer or distractor label) requires `set_attr` `data-item-version` `+1`; formatting alone does not (gate enforces the key and label part). Preserve `data-src`, `data-nid`, `data-recon` and unknown attributes.
- New item ids come from `tools/idgen.py` via `add_item`; do not write ids by hand.
- Check before finishing: `python3 tools/verify_edits.py <edits.json> --nids <source.md>` (applies to a scratch copy, runs gate and render, flags near-duplicate items, and checks every added `data-nid` is a nid of a question in that source and not already on another brief). Loop until it prints PASS.

## replace: swap a unique snippet inside a brief (outside its bank)
```json
{"op": "replace", "brief": "pmr", "find": "PMR responds to <b>low</b>-dose steroids", "with": "PMR responds to <b>low</b>-dose prednisone"}
```

## insert_before / insert_after: add HTML next to a unique anchor
```json
{"op": "insert_before", "brief": "pmr", "anchor": "<div class=\"traps\">", "html": "<div class=\"pearls\"><span class=\"lbl\">Pairs with</span> Part I <b>Giant Cell Arteritis</b>: is there a new headache or jaw claudication?</div>\n"}
```
```json
{"op": "insert_after", "brief": "pmr", "anchor": "every PMR diagnosis gets a GCA symptom screen", "html": " before steroids start"}
```

## add_item: append one question to the brief's ol.bank
`stem`, `answer`, `companion` are HTML without arrows (the applier writes `stem → <b>answer</b> → companion`). `d1`/`d2` are plain text. Optional: `lead_in`, `status` (default `ready`), `src`, `nid`, `after_item` (insert after that item instead of at the end), `attrs` (extra `data-*`), `bold_answer` (default true).
```json
{"op": "add_item", "brief": "pmr", "type": "test",
 "stem": "70 yo M with 3 weeks of shoulder and hip stiffness, full strength, new temporal headache and jaw pain when chewing",
 "answer": "Temporal artery biopsy after starting high-dose glucocorticoids", "companion": "Giant cell arteritis",
 "d1": "Creatine kinase level", "d2": "MRI of both shoulders",
 "lead_in": "Which of the following is most likely to confirm the diagnosis?", "src": "uworld", "nid": "12345"}
```

## set_attr: attribute-only change on an item (by `q_` id) or a brief (by id)
`value` is plain text; `"+1"` on `data-item-version` increments it. Identity attributes (`id`, `data-item-id`, option ids) are refused. A link-only pass ships with `tools/ship.sh sNN "<msg>" --attr-only`.
```json
{"op": "set_attr", "target": "q_3a5d925430f85de2b063", "attr": "data-item-version", "value": "+1"}
```
```json
{"op": "set_attr", "target": "q_f301e03be41b7aa167b0", "attr": "data-nbme", "value": "peds-cms-5-12"}
```

## new_brief: insert one complete brief after an existing brief
`html` must be exactly one `<div class="brief ...">` block with a new id, `data-shelf` and `data-bp`. `nav` adds the sidebar link after an existing link (class defaults from the brief kind: `bs`, `aq` or none; a topic link also increments its `.sect` count). The system header count is computed at runtime.
```json
{"op": "new_brief", "after": "pmr", "html": "<div class=\"brief\" id=\"gca\" data-shelf=\"fm\" data-bp=\"msk cv\">\n<h4>Giant Cell Arteritis</h4>\n...\n</div>",
 "nav": {"after_link": "pmr", "title": "Giant Cell Arteritis"}}
```
Part II briefs go directly after the system's `.bsband` run (use `after` = the last board-style brief of that system) and need a `.vignette` with a `<b>Q</b>` line before `.dp`.

## replace_global: page chrome only (CSS, scripts, nav); orchestrator use, never in worker packets
The `find` text must occur exactly once in the whole page and lie outside every brief. Script edits are checked by `node --check` in the gate and by the jsdom render.
```json
{"op": "replace_global", "find": ".nbmechip{display:inline-block;", "with": ".nbmechip{display:inline-block;"}
```
