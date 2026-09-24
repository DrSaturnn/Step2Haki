# RULES_worker.md coverage map

Every rule or section of the two governing skills, mapped to the rules-sheet line that carries it, or "omitted: <why>" (only where irrelevant to a one-question backfill into an existing brief). Skill hashes are in the RULES_worker.md header; when either changes, walk this table again.

## board-brief/SKILL.md

| Rule / section | Rules sheet |
| --- | --- |
| Purpose: teach what decides the question, discrimination and management | W1, W2 |
| Register (concise tutor, less likely / not appropriate / excluded, bold deciders, causal verbs) | W24 |
| Depth preference (fast rule + one exception, deeper after reveal, existing table, no second table) | W2 |
| HTML transfer: presentation and metadata contracts | W15, W17, W14; format in tools/EDITS.md |
| Part 1 Step 0 scope the concept; title check | W4 (title untouched; every word true of new items) |
| Step 1 route (discriminator vs ladder; task distinctions) | W2, W10, W14 |
| Step 2 ledger / deciding comparison | W2, W8 |
| Step 3 miss diagnosis; reported/inferred/unknown; performance metadata | W9 |
| Check existing coverage; default to existing brief | W1, W16 |
| Correct-answer case (no miss analysis, no padding) | W9, W3 |
| Step 4 sketch bank, assign types, next-share advisory, no invented variants | W10, W13, W16 |
| Step 5 draft in template | W1, W2 (backfill edits existing blocks) |
| Step 6 boundary pass | W2 (one exception), W28 (report) |
| Step 7 self-check, fix don't annotate | W28 (verify loop), W15 |
| Part 2 template: card | omitted: optional, never rendered as a block; backfills do not add cards |
| Part 2 template: decision point, criteria, pertinent +/-, discriminator table, management block, spine, bank, distractor analysis, decoy, pearls, pairs with, transferable rule | W2, W18, W19, W21, W22 (existing blocks are edited in place) |
| Outside-the-brief block | W9, W28 (report) |
| Length calibration (no minimum, no padding) | W2, W3 |
| Shared contract: immutable ids, version bump, labels, lead-in, status, preserve src/nid/unknown attrs | W14, W15, W17, W12 (status) |
| Arrow grammar: direct-child arrows; keyed = segment 2 | W17 |
| Prose notes are not questions | W10 (only typed items via add_item) |
| Clinical rule guard (negative test, completed tier, culture-before-antibiotics scope) | W8 |
| Rule 1 meta-discussion outside the brief | W9, W28 |
| Rule 2 every sentence earns its place | W3 |
| Rule 3 criteria tile holds criteria only | W18 (tile grammar); content rule folded into W3 |
| Rule 4 tables sized to the discrimination | W2 |
| Rule 5 author options with the question; context sufficiency | W11, W13 |
| Rule 6 distractors from supported comparisons | W11 |
| Rule 6a one best answer, F1 to F6 | W11, W12 |
| Rule 7 pattern names describe temptation | W21 |
| Rule 8 triggers are numbers or named failures; study gap | W8 |
| Rule 9 numbers are liabilities; ⚠︎; digit collision; flags never silently dropped | W7 |
| Rule 10 links load-bearing; bidirectional; discriminator as question | W22 |
| Rule 11 paraphrase; no letters or percentages in Q; no vendor figures | W5, W20 |
| Rule 12 source and provenance separate; UWorld/local as references | W6, W9 |
| Rule 13 bank tests the way the exam asks; type by options; next rungs; threshold ⚠︎ | W10, W13, W7 |
| Rule 13 avoid items key the forbidden act | W10 |
| Rule 13a complete labels; rationale needs a verified consumer | W15 |
| Rule 13b stem does not advertise options; shuffled-review context | W13 |
| Rule 13c one precise prompt via lead-in | W14 |
| Revealed explanation: decisive finding first, closest competitor | W2 (companion segment after reveal) |
| Rule 13d answer-cue review, every cue class | W15 |
| Rule 13d batch before/after cue metrics | omitted: batch/renderer-change measurement run by the orchestrator, not a one-question worker |
| Rule 14 brief scoped to concept | W4 |
| 4.1 item authoring (companion, variant prompts) | W10, W13, W2 |
| 4.2 canonical tuple | omitted: add_item carries the same six fields plus metadata; tuple form is for chat/Word output |
| Distractor rules 1 to 8 | W11, W15 (7, 8) |
| F1 to F6 table and F6 test | W11 |
| 4.3 dual rendering; never author two copies of the bank | W17 (single chain line); rendering is automatic |
| 4.4 distractor analysis and pattern catalog | W21 |
| New pattern naming | W21 (leave unnamed rather than coin) |
| 5.1 discriminator table spec; data-mask="3" | W19, W2 |
| 5.2 management block (classify first, fingerprint, ladder, gates, exit ramps) | W8, W19, W2 |
| 5.3 criteria tile scale rule | W23 (scale owed in place), W18 |
| Part 6 worked brief | omitted: full-brief example; backfills edit an existing brief shown in the packet |
| 7.1 teaching value | W3 |
| 7.2 read the ledger | W8 |
| 7.3 trigger archaeology | W8 |
| 7.4 naming patterns | W21 |
| 7.5 document is an organism (twins) | W22 |
| 7.6 exam framing and source support | W6 |
| 7.7 calibration | W2 |
| 7.8 behavioral coaching | W9 |
| 7.9 control document growth | W1 |
| 8.1 provenance classes; study aids not clinical evidence | W6, W7 |
| 8.2 quality bar 1 to 12 | W2, W20, W4, W18, W19, W21, W11, W7, W22, W28, W1, W15 |
| 8.3 placement on the page | W1 (existing brief); new placement omitted: no new briefs in a backfill |
| 8.4 poster output | omitted: poster/PNG output, not page backfill |
| 8.5 tone | W24 |
| Part 9 optional card | omitted: see Part 2 card |

## study-page-builder/SKILL.md

| Rule / section | Rules sheet |
| --- | --- |
| Use the current file; scoped edits | W27, W28 (packet holds the current brief HTML) |
| Approved authoring preference; preserve blur-and-tap | W2, W19, W20 |
| Architecture: transform, review module, script discovery | omitted: worker does not edit scripts; gate/render check them |
| Transform edits are exceptional | W27 (content only); gate enforces node --check |
| Shelf routing, ?shelf=, deep links | omitted: runtime behavior; W4 keeps data-shelf |
| Figures (inline SVG, fignote) | W5 (tables or spine over drawings; no vendor images) |
| Adding a Part I brief (skeleton) | omitted: backfills never add briefs (W1) |
| id permanence | W4, W17 |
| data-shelf | W4 |
| Every table titled | W19 |
| Source vignette rules | W20 |
| Criteria tile grammar | W18 |
| Scale peek; scale owed in place; point at criteria; scale gap is an authoring gap | W23 |
| Bank item grammar (direct-child arrows, plain-text options) | W17 |
| Typed and identified items; lead-in; status | W10, W14, W12 |
| Distractors hand-authored; cue review; capitalizing key is safe; keyed = segment 2 | W11, W15, W17 |
| One prompt, existing tables | W14, W2 |
| Labels and revealed explanations; verify consumers | W15 |
| Trapline form; bare pills upgraded | W21 |
| Pairs-with exact h4; reverse mention; <i> for missing partner | W22 |
| Preserve study interaction | W19, W20 (markup only; no controls) |
| Column-driven masking; data-mask | W19 |
| `·` and ` — ` structural | W18 |
| Inline flags t-em, t-peds | W23 (span class allowed); omitted detail: flags only where the brief already uses them |
| Escaping and allowlisted tags | W23 |
| Legibility / CSS rules | omitted: CSS is not edited in a backfill |
| Front matter | omitted: not edited |
| Shared contract (same as board-brief) | W14, W15, W17 |
| Structural parser axlib.py | omitted: tools/pagelib.py replaces it; worker edits by anchor |
| Clinical rule guard | W8 |
| Adding a Part II brief; bands | omitted: no new briefs |
| Sidebar and counts | omitted: no new briefs (new_brief op handles nav) |
| Distractor-pattern pills; adding a species costs four edits | W21 (use existing species only) |
| Mapping board-brief output onto the page | W18, W20, W21, W22 |
| Bulk insertions / converter / three traps | omitted: batch conversion tooling, not a single backfill; mask trap in W19 |
| Scoped edits by immutable id within exact bounds | W28 (anchors unique inside the brief), W17 |
| Parsing the page (depth-matching) | omitted: tooling (pagelib) |
| Corpus-wide sweeps | omitted: sweep workflow, not a backfill |
| Review mode, profiles, sync | omitted: runtime module |
| Deployment | omitted: orchestrator ships |
| Restructuring the document | omitted: not a backfill |
| Verification loop 0 to 5 | W28 (verify_edits runs gate and jsdom render); step 4 real-browser check omitted: orchestrator |
| Copyright and provenance | W5, W7, W20 |
