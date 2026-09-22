# Study-page metadata contract v1

This additive contract applies only to the supplied standalone study page. It does not change a RapidRounds production schema or any governed AxBx drug schema.

The authored `<li>` remains the owner of its stem, key, companion, and distractors. The renderer preserves complete labels and uses the top-level arrow grammar used by the structural parser included with study-page-builder. Inline markup and arrows inside nested elements are content. A bank entry without question attributes is a note, not a question; prose notes belong outside the bank.

| Attribute | Meaning |
|---|---|
| `data-item-id` | Immutable question ID; never derive a new ID from an edited title, position, or stem. |
| `data-item-version` | Integer revision, starting at 1. Increment when the stem, task meaning, option meaning, or key changes. Formatting alone does not require an increment. |
| `data-key-id` | Immutable option ID for the source key. |
| `data-d1-id`, `data-d2-id` | Immutable IDs of the two source distractor options. Shuffle display positions while retaining each ID. |
| `data-item-status` | `ready`, `needs_source`, or `needs_repair`. Unresolved items remain readable and are excluded from graded mixed practice. |
| `data-lead-in` | Optional exact task override. Use when the general type prompt would misstate the task. |
| `data-objective` | Optional concise authored objective, when explicitly established. |
| `data-label-answer`, `data-label-d1`, `data-label-d2` | Optional exact display labels. Otherwise use complete source text after whitespace normalization. No runtime punctuation trimming or character limit. |
| `data-context-ref` | Optional source/context locator for a restored fact. Unknown means absent; do not invent a vendor question ID. |
| `data-rationale-answer`, `data-rationale-d1`, `data-rationale-d2` | Optional supported explanations. Absence means no separate authored rationale is available; do not infer one from the label. |

Preserve all existing attributes, including `data-src`, `data-nid`, and attributes not defined here. Preserve brief IDs and their URLs. Preserve source-vignette blocks and reconstruction flags. `data-nid` is retained without claiming what its numbers identify.

Keep any project identity registry with its original source locators and attributes. Original positions are historical locators, not ongoing question identity. Reuse assigned IDs; the runtime metadata remains on the authored HTML and does not require fetching the registry.

The runtime `.mcq` and option buttons retain the item and option identities. Correctness is determined by option identity through shuffling, while `data-a` remains the current display index for compatible local rendering. Brief-level progress storage, merge rules, and export codes remain unchanged.

Existing content keeps its source chain for reference and feedback. Explicit labels are the selectable wording; an explanation removed from a label must still be preserved in the authored reference/feedback. Never delete a qualifier that changes the clinical action to improve option-length balance.

**Consumer support:** inspect the actual page before relying on optional fields. A defined `data-rationale-*` attribute is not proof that the renderer displays it. Keep existing feedback until the authored explanation is visibly available after answering. See [AUTHORING_PRESENTATION.md](AUTHORING_PRESENTATION.md) for placement, preservation, option-ID mapping, and acceptance. Retain the six-field tuple; transfer optional metadata alongside it keyed by permanent item ID.

Missing-context content is not repaired by excluding it. The visible notice and handoff must identify what remains unresolved. A reduced set of ready questions cannot advance a brief when the usual required sample is unavailable because of quarantined items.
