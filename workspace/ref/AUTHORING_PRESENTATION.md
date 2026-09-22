# Board Brief presentation contract

This reusable contract governs presentation in the standalone study page. It complements [STUDY_PAGE_METADATA.md](STUDY_PAGE_METADATA.md). It does not modify any production database or governed drug-authoring schema.

## Teaching depth and placement

| Content | Place it here | Editorial boundary |
|---|---|---|
| Fast decision rule | Existing decision point and transferable-rule block | Concise rule for the usual exam presentation; preserve the qualifiers that make it valid. |
| Relevant exception | One short clause/sentence with the fast rule | At most one useful exception that changes the answer; omit when unsupported or unnecessary. Do not hide a qualifier required to make the rule correct. |
| Initial test, confirmatory test, next management step, organism, mechanism | Relevant cells/rows of the existing differential table or management ladder | Include only the distinctions this topic earns. No mandatory five-part section, duplicate table, or second question. |
| Explanation of the answer | Existing post-answer explanation area | Decisive finding → why it favors the key → why the closest alternative is less appropriate, when useful. Include necessary causal steps. |
| Further mimic teaching | Existing differential-table row; link the owning brief when it exists | Do not turn every row into a miniature brief. Record a candidate future brief in the handoff when fuller teaching is needed. |
| Learner performance and source uncertainty | Structured metadata or handoff ledger | Reported/inferred/unknown remain distinct. No assumed miss cause in shared clinical prose. |

The user's “80–90%” aim means useful, high-yield coverage rather than exhaustive exception coverage. It is not a measured accuracy guarantee and does not permit an incorrect key, missing deciding qualifier, or fabricated clinical support. No minimum word, pearl, or bank-item count applies. Use supplied UWorld explanations and local material as working sources; no routine external clinical audit is required.

## One precise task without more front-loaded text

Keep the existing `data-type` enum. It groups questions; it does not always specify their exact task. Use `data-lead-in` to replace a broad fallback with the actual question. For a question-form stem, preserve its facts and consolidate the question into one place rather than displaying both an interrogative stem and a second generic question.

An initial test, a confirmatory test, and a next action may differ. An organism and a mechanism are different answer categories. Do not infer the intended task from a regex, a default category, or one option in isolation. Review the stem, the complete option set, the brief, and the supplied explanation together.

Match context to the requested use. Do not expand within-brief recall into standalone vignettes unless that conversion is requested and supported by source facts. Preserve existing source-status exclusions. A genuine key ambiguity discovered during an edit must still be resolved from source or retained as unresolved.

## Complete labels and authored explanation

The existing contract already defines `data-label-answer`, `data-label-d1`, `data-label-d2`, and the corresponding `data-rationale-*` fields. No new tuple arity or metadata enum is introduced here.

1. Author the three option labels together. They should answer the same question, use parallel grammar, and preserve all meaning needed to distinguish the choice.
2. Put teaching commentary in the rationale or reference chain rather than only in the correct option. Preserve its source wording and locator during the move. Do not remove dose, duration, timing, anatomy, negation, or a compound action when it changes the answer.
3. Retain the source chain as provenance/reference and as the fallback explanation when no authored rationale exists. Labels are the selectable wording; they are not a replacement for the underlying source.
4. Author concise rationale text that explains the decision. Do not infer a mechanism from a mere association or diagnose why the learner chose an option. A wrong selection identifies the option, not the learner's thought process.
5. Map rationales to immutable source option IDs before shuffling. The fields `answer`, `d1`, and `d2` refer to source roles, not displayed A/B/C positions. Preserve absent rationales as absent.
6. Render authored text safely as text. Attribute encoding must round-trip quotes, ampersands, comparison signs, and units. Do not execute or inject authored explanation as HTML.
7. Version an item when task, stem, option, or key meaning changes. Moving commentary from a label to feedback without changing the clinical choice is a presentation edit; record it in the change ledger. Increment the version if the edit changes what an option actually means.

## Verify consumer support

Inspect the current page before relying on optional label, lead-in, or rationale fields. Do not claim that writing an attribute makes it visible. Verify conversion, storage, rendering after answer selection, legacy-item fallback, and source preservation. Keep the six-field tuple compatible; optional metadata travels alongside it keyed by permanent item ID.

When implementing rationale display, use the existing answer area and existing answer/reveal event. Show the key's reasoning and, when present and useful, the selected alternative's reason. Show the relevant comparison once; do not repeat the entire chain plus an identical rationale or add an explanation dashboard. Existing answer-reveal behavior, bank Review/Quiz views, source navigation, and print access must continue working.

## Interaction invariants

- Answers occupy their current space, blur in study mode, reveal on tap/click, and reblur on another tap/click. No visible Reveal/Hide-button redesign or collapsed answer space.
- Preserve keyboard operation, visible keyboard focus, concealed-answer accessibility behavior, source vignettes remaining sharp, and clone ID/control associations in scale peeks.
- Keep existing table masking. When a heading changes, explicitly retain the intended mask column; a four-column differential with the discriminator in column 3 uses `data-mask="3"`. Keep the current intervention mask on a Tier table.
- Preserve brief/question/option identities, shelf/search/review composition, profiles, progress format, schedule advancement rules, and backend behavior.
- In mixed practice, no rationale, key, source title, or teaching cue may become visible or accessible before the current answer/reveal event. The intended practice format does not permit a pre-answer leak.

## Acceptance for page edits

Verify behavior with representative actual edited items and at least one untouched legacy item:

1. One precise question appears. It asks the intended task without adding a duplicate question or deleting source facts.
2. All three complete labels remain distinct, parallel, and meaningful. Commentary moved out of a choice is still available after answering.
3. Correct and incorrect selections show the intended explanation under multiple option orders, using option IDs. Missing rationale fields retain the existing fallback. A literal quote/ampersand/comparison sign survives transfer as text.
4. Rationale content is unavailable before answering in the quiz and mixed overlay; after answering, the explanation and existing source link work. The established review/reveal-all/reset and print paths still expose the appropriate content.
5. At desktop and 390/320-pixel widths, edited content wraps without clipping, horizontal overflow, or changed blur/tap behavior. Table masks still conceal the same intended knowledge.
6. Existing runtime checks pass for source preservation, IDs, shuffled scoring, filters, source-blocked items, and progress. Hashes and reports must identify the newly edited HTML, not the supplied pre-edit version.

A prose scan or an attribute's presence is not evidence that its content renders correctly. Do not expand a presentation edit into a broad clinical audit or a different practice format.

## Mandatory answer-cue review

Review all new/edited option sets for unequal teaching detail, grammatical cues, specificity, abbreviations, repeated stem wording, and length. Repair a detected cue or record why a difference is clinically necessary. Do not truncate meaning, pad distractors, or require exact character parity. A batch/renderer change also needs before/after rendered metrics: uniquely longest keys, ties, expected longest-choice accuracy under random tie-breaking, and population counts. Inspect the edited bank as well as the full corpus; numerical flags prioritize review but do not replace it. The study-page-builder includes a read-only measurement script.
