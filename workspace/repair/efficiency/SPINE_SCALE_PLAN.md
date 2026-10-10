# Spine at scale: agent execution plan (v2.2, 2026-10-09)

Goal: move the remaining briefs onto decision spine v2 at quality equal to the shipped spine briefs (s118 to s127), at lower token cost, by splitting the work: scripts do every mechanical check and all retrieval plumbing, cheap models do narrow extraction and transcription, Opus does the decisions, the wording and the audit.

Nothing here relaxes a standing rule: every fact sourced; adversarial audit; screenshots and Jonathan's approval before any ship; no vendor text in the repo; mnemonics identified, never invented; one owner per decision; no emojis or em dashes; handoff updated after each ship.

v2 folds in an adversarial self-audit and an independent Opus review of v1 (23 findings: 5 critical, 12 major, 6 minor; all accepted). v2.1 wires the AnKing deck index (0.6b) through every stage; v2.2 folds in a second independent review (section 9). Section 8 lists what changed and why.

## 0. Starting point (measured 2026-10-09)

| | Count |
|---|---|
| Briefs on the page | 177 (144 brief, 28 bs, 5 aq) |
| On the spine | 14, all psych |
| Left to convert | about 163; non-spine median 1,433 words, max 4,932 |
| With a migration claim map (approximate match by id) | about 80; the rest came from board-brief or UWorld backfill with no claim-level sources |
| Practice items on the page | about 3,140, all carried with ids intact |
| Subagents in this chat, s118 to s127 | 184; about 760M cached tokens read, 5.4M output |
| AnKing cards indexed | 30,480 notes: the AnKing Step Deck collection of 2026-10-10 (19,718 notes, read directly from its .apkg), the October Psych, Peds and FM exports, and the July full export; note ids for 23,000. 314 of the page's 384 data-nid values resolve, linking 88 of the 97 briefs that carry nids (median 3 cards, 6 statements per brief); 80 briefs carry no nid and get candidates only |

Cost driver: agents re-reading big contexts over many tool calls (up to 80 each), and the lead's own long context. Output is cheap. So the plan cuts reads and calls first, model price second.

Psych has no disease briefs left (the remaining psych work is hubs and screens), so the pilot and production run on FM and peds, which the current spec does not yet cover. Phase 0 fixes that first.

## 1. Roles

| Role | Who | Model, effort | Reads | Writes | Never |
|---|---|---|---|---|---|
| Lead | Main chat | Opus | This plan, CURRENT_STATE, script summaries, agent JSON | Batch list, adjudications, ship | Read whole builds or the page; adjudicate its own canary |
| Scripts | `tools/spine/` | none | Page, claim maps, ledgers, source cache | Inventory, packets, fetches, checks | Approve judgment |
| Extractor | Subagent | Haiku, low | Extract packet: old brief text with span offsets, leftover claims a script could not match | claims.json for the leftover only | Judge or reword |
| Architect | Subagent | Opus, high | Architect packet (below) | outline.json with the final learner-facing text of every line, chart specs, needs.json (questions), omissions.json | Write HTML; fetch pages |
| Scout | Subagent | Sonnet, medium | needs.json, allowlist, local source excerpts for the brief's source questions (located through the nid and QID headings of the question files) | URLs to fetch, then facts.json (verbatim single-fragment quotes, section heading, population, setting, date, and a fit tag per answer: matches, narrower, broader, different population, contradicts) | Write cache files; join fragments with "..."; confirm a claim instead of answering a question; see card statements (it answers blind; a separate conflict-check pass compares cards with facts.json afterwards) |
| Filler | Subagent | Sonnet (Haiku arm in the pilot) | Filler packet: RULES_spine_worker, spinelib API card, outline.json, golden build | build.py that renders the outline text exactly | Change a word of learner-facing text; add a line |
| Answerer | Subagent | Haiku, low | Bank stems and options without keys; with the full brief render (hover text and chart data tables included) and without it, each twice | Answers plus the brief line used | |
| Auditor | Subagent | Opus, high | Audit packet (below) | AUDIT_PROMPT findings plus a per-step "checked" list | Edit files |
| Approver | Jonathan | | Approval packet | Approve or change requests | |

Architect packet: the claims with their spans and sources, the card checklist (0.6b: must and candidate statements with ids), dropped claims from every ledger, bank keys and explanations, NBME framing, the brief's local source excerpts, sibling titles and bottom lines, OWNERS.json, the entry-type and lens rules, SPINE_SPEC rounds 2 to 4 verbatim, and DECISIONS_DIGEST.

Audit packet: the text render (including attribute, hover, SVG and chart text, with each chart's data as a table), a phone-width crop of every chart and drawer, the claim map with each quote plus 300 characters of source context on each side, the outline, bank keys and explanations, NBME framing, the old brief text, the dropped list with reasons, the card checklist with each disposition, and the preflight, verify, numbers and answerability lines.

The architect is the only creative Opus pass and now owns every word a learner reads. The filler is pure transcription, which a script checks exactly. That removes the main drift point of v1, where the filler reworded lines and hedges could fall out.

## 2. Phase 0: one-time setup (each item has an acceptance check)

Status 2026-10-10:
- Done: 0.3 inventory (`tools/spine/inventory.py`; 177 briefs, 163 to convert, median 585 words above the bank, 5 over 1,300; 75 with a claim map; 88 with resolved cards; one brief, bone-tumors, carries UWorld QIDs in data-nid).
- Done: 0.6b AnKing index.
- Done: helpers moved to `tools/spine/` (shingle_check.py, which also reads card text and failed two seeded copies as it should; shots.py, steps and full-resolution chart crops).
- 0.1 FM and peds lens frozen as drafted (Jonathan gave no change); his review of the goldens approves it.
- 0.2 goldens chosen: nephrotic-child and scfe (peds), copd (FM). Built on the current process next.
- Next after the goldens: 0.4 to 0.17.

Scripts live in `tools/spine/` (tracked). Packets, caches, outlines and claim maps live under `repair/migration/` or `repair/sources/` (local-only; synced to the Mac by mac_sync). Helpers now in `/tmp/claude-0` (ovl_*.py, shootgen.py, shotcharts.py) move into `tools/spine/` first; they vanish with the container.

0.1 Spec for FM and peds. Generalize AUTHOR_SPEC and AUDIT_PROMPT beyond psych: the peds lens (age band filters the differential, non-accidental trauma as a standing can't-miss, caregiver history, growth, development, vaccines, weight-based dosing, age-restricted drugs, consent exceptions that vary by state) and the FM lens (setting and function, time as a test, multimorbidity and deprescribing, refer-when, return precautions). Add per-type word caps. The FM and peds lens lines also go into RULES_architect (0.12). Jonathan approves both. Accept: approved spec, frozen with a hash.

0.2 Goldens for FM and peds. Hand-author one peds disease brief and one FM disease brief on the current process (Opus author, Opus audit, lead fixes, Jonathan's approval). They become goldens and calibrate arm C. Hubs and screens stay out of the pipeline until each has a hand-built approved golden.

0.3 `inventory.py` writes `repair/migration/spine/inventory.json`: per brief, kind, shelf, format, words, item ids, NBME items, nids, claim map paths, dropped-claim count across every ledger, proposed entry type with reason, owner candidates for each differential diagnosis, cluster. Accept: matches section 0.

0.4 `packet.py <id> --role ...` builds one file per role under `repair/migration/spine/packets/<id>/`. Prints size; targets: extract 15k tokens, architect 35k, fill 20k, audit 40k. Asserts that no quarantined path or id (pilot references, section 3) appears. Accept: no packet holds another brief's full HTML or a whole skill file.

0.5 Claims and spans. `claims_map.py` assigns each piece of old text to existing claim-map rows by fuzzy match against `new_text` (script, not model); the extractor only handles the leftover. Every claim carries verbatim character spans of the old brief. `claims_check.py` requires the union of spans to cover 100% of learner-facing text above the Practice header, including attributes (title, data-tip, hover bodies) and SVG and chart labels, and flags any pointer whose text similarity falls below threshold. Thresholds are set by calibration on the 14 shipped spine briefs (the strictest value with no false miss) and frozen in the script. Accept: mutation tests (dropped sentence, dropped cell, dropped hover, merged claim losing a qualifier, wrong pointer) all fail.

0.6 Retrieval. `fetch.py <url>` is the only writer of `repair/sources/web/`: it fetches an allowlisted URL, strips HTML to text, hashes it and records URL and date. `passages.py <sha> "<terms>"` returns short passages, so no agent loads a whole page. Allowlist: StatPearls and NCBI Bookshelf, MSD Manual Professional, PsychDB, USPSTF, CDC, AAP, ACOG, AHA and ACC, IDSA, ADA, FDA labels and DailyMed, NIH, NIDA, NIAAA, plus the pasted NBME and UWorld material. AnKing cards are not on the allowlist: they are leads, never citations (0.6b). Anything else needs the Lead's yes. If a domain refuses the fetch, the source is dropped and reported; no workaround. Test first that fetch.py's text matches the page (WebFetch returns model-processed text, so it is not the cache writer). Accept: a paraphrased quote, a quote absent from the page, and a non-cache file all fail quote_check.

0.6b AnKing index (built 2026-10-09; extended the same day with Jonathan's full AnKing export of 2026-07-16, `~/Downloads/AnKing/AnKing.txt`, 24,094 notes, Step 1 and Step 2 subdecks; the October shelf exports take precedence where a note is in both: 27,376 notes in all, 42,116 Extra statements, 13,216 UWorld QIDs. Note ids so far cover only the 3,282 shelf-export notes; a no-media .apkg of the full deck adds the rest; Anki's data folder is protected and cannot be connected). `tools/spine/anki_index.py` reads the deck exports (Psych, Peds, FM; Notes in Plain Text with HTML and tags; kept local-only in `repair/sources/anki/exports/`) into `repair/sources/anki/anki_index.jsonl`: per note the Anki unique id (guid), AnkiHub id, note id (from the .apkg collection via `--db`; the plain-text export lacks it), Text and Extra (plain and HTML), emphasis marks in Extra, UWorld QIDs (Step 2, Step 1, COMLEX) and shelf tags. First run: 3,282 notes, 2,468 with a UWorld tag, 5,890 distinct QIDs; both QIDs recorded in our source files matched. Card text is never the cited source. Uses: (1) per brief, the deck's high-yield statements become a tested-concept checklist in the architect packet; outline_check requires each item's disposition (covered by line, owned by another brief, out of scope with reason, or conflicts with a source; a conflict is checked by the scout and the card error logged); (2) a card a fact was checked from is named in the claim map by guid or note id; (3) cards link to briefs by note id (the page's data-nid values) and to UWorld questions by QID. The deck's pink text is the Extra field (Jonathan 2026-10-09); the index splits it into statements (8,822 across 2,788 notes), and those statements are the checklist items. Verified from the .apkg exports (2026-10-09): the AnKingOverhaul notetype CSS colors #extra (navy; magenta in night mode), and `--db` adds every note id (3,282 of 3,282 matched by guid) and field names. The page's data-nid values are AnKing note ids: 206 of the page's 395 nids are in these three decks, linking 73 briefs; the rest need exports of the other shelf decks.
  - Checklist per brief (`tools/spine/card_checklist.py <id>`). Each card's **anchor** is its cloze answer (the fact the card tests); its Extra statements are context. **Must** items: anchors (and their Extra statements) of cards linked by note id to the brief or by UWorld QID to one of its source questions. **Candidate** items: anchors of cards whose text matches the brief's title, differential and key terms by a score defined in the script and frozen with a test set; capped at 15 per brief, with the cut logged (no silent caps). Statement ids are `<nid>.<key>`, key = hash of the normalized text, so ids survive re-exports; statements are deduplicated by key across the checklist, and header lines (ending in a colon) are joined to the lines under them (both done in anki_index.py, 2026-10-09: 8,634 statements, 6,163 distinct). The data-nid links are validated first: the Lead spot-checks 20 brief-card pairs, and any wrong link is fixed before checklists are trusted. The index file's hash goes into the packet so a batch uses one frozen deck version; re-export when AnkiHub updates the deck.
  - Dispositions (outline_check): every must and candidate item gets one code: `covered:<line id>`, `owner:<brief id>`, `scope:<reason>` (Step 1 depth, not tested, guideline-only detail kept in a hover), `not-topic` (candidates only), or `conflict?:<need id>` at B4, resolved at B6 to `conflict:<fact id>` or another code. B4.5 assigns each item one owning brief across the batch. An `owner:` pointing at a brief not yet converted is logged as an obligation in OWNERS.json and checked when that brief converts. OWNERS.json holds ids only and lives in `repair/migration/spine/`.
  - Cards are leads, never citations: quote_check accepts the card index only on mnemonic rows. The two exceptions: a mnemonic's source (K3; locator `AnKing, local: repair/sources/anki nid <nid>`, which the gate's K3 rule accepts, tested 2026-10-09; an `anki:nid:` locator fails it) and evidence that Step 2 tests something (S2), allowed only for a card's anchor (cloze) fact and only when the card carries a Step 2 UWorld QID tag.
  - Copy check: anki_index.py also writes `anki_cards.txt` (plain card text), and vendor_scan.py reads that one file as vendor source (the exports, index and databases beside it are skipped, so the 3-file stock rule cannot cancel card lines). Tested 2026-10-09: a card sentence pasted into a tracked file is flagged (16 of 18 shingles); the live page shares 0 shingles with the cards. verify.py's shingle check includes card text.
  - Card recall is benchmarked first on the 14 shipped spine briefs; that score, not 100%, is the bar. Recall counts `covered` plus `owner` only; `scope` and `not-topic` shares are reported separately. A statement the scout finds contradicted goes to `repair/sources/anki/card_conflicts.md` (nid, statement, contradicting fact id); the s125 MAOI washout card ("6 weeks") is the first entry. Submitting corrections to AnkiHub is Jonathan's call.

0.7 `quote_check.py`: every quote is one verbatim fragment (whitespace-normalized) of a fetch.py cache file, or of a local pasted source; no "..." joins (two fragments are two fact ids, each with its section heading, which stops the s124 splice of two buprenorphine induction methods); editorial brackets are not allowed inside a quote; every carried number gets contract N1's currency status (verified with a source, flagged on the page, or stable), with a source over 5 years old as one trigger for re-verification. Accept: mutation tests.

0.8 Outline schema and `outline_check.py`. Steps allowed for the entry type; every line holds final text and cites fact ids or a need id; per-type word caps enforced here, where cutting is still possible; bottom line at most 3 lines; Insights exactly two; differential rows ordered with a `tempting_because` field, each Decides-it cell leading with a sourced timeline when one exists; ladder triggers with a time or named failure (G2), Top rung only last (G3); every carried number has a `currency` field (contract N1); every omission cites where it is tested (an NBME item id, a nid or an AnKing card) and the script checks the reference exists; every must and candidate card statement carries a disposition code (0.6b); every old claim has a disposition (carried, moved to a step, moved to another brief, dropped: not tested, dropped: wrong, dropped: unsourced); chart specs (axes, events, values) cite a fact id per datum; a peds brief citing a fact marked adult-only, or the reverse, is flagged; a line citing two or more fact ids from different source sections or pages is flagged `combined`, and the auditor confirms the combination keeps each source's conditions (the s124 two-method failure in a new form). Accept: one mutation test per rule.

0.9 `verify.py <id>`: runs in a unique temp dir; exact match of every rendered learner-facing string to outline text (no extra line, no reworded line); T() ids in SRC; claim map complete; shingle check against every quote; hedge diff between each line and only the fragment it cites; bank tail byte-identical; ids, items and versions per the replace_brief contract; title change only with inbound rewrites (H1); briefs.json record keeps every nid; V1 acronyms; no em dash; then the preview build, `gate.py`, `render.js`, `preflight.py --base HEAD` (P1 = 0), `vendor_scan.py --page`, `legib_audit.py` in sculpted, flat and study modes, and `numbers.py`. Prints PASS or each FAIL with its fix, deletes its preview dir. Refuses to run when a rules sheet's provenance hashes do not match its specs. Word count above cap by more than 5% is reported, not fixed by the filler. Accept: clean on the 14 shipped spine briefs; every mutation fails.

0.10 `numbers.py`: page-wide registry of (term, number, unit, brief, source id), also fed by chart values and bank stems and explanations. Flags the same term with conflicting numbers across briefs, and a chart value that contradicts a bank item (the s125 REM at 90 minutes). Accept: catches both seeded cases.

0.11 Answerability. `answer_score.py` counts an item as taught by the brief only when the answerer is right with the brief and wrong without it, and the cited line is found verbatim in the render. Wrong-with-brief items go to the audit packet as possible contradictions. Accept: baseline recorded on the 14 shipped briefs.

0.12 Rules sheets with provenance hashes: `RULES_spine_worker.md` (filler), `RULES_architect.md` (lenses, scope rule, source precedence: guideline sets facts, NBME sets the key and framing, then UWorld; psych topic standards; reviewer list items 1 and 9 to 14; the FM and peds lens lines from 0.1; one owner per decision), and `DECISIONS_DIGEST.md` (each Jonathan decision and correction with date). Architect and filler packets also carry SPINE_SPEC rounds 2 to 4 verbatim, since a one-line digest loses detail.

0.13 Agent definitions in `workspace/.claude/agents/` (tracked): spine-extractor (haiku), spine-architect (opus), spine-scout (sonnet; may run fetch.py and passages.py, no file writes), spine-filler (sonnet), spine-answerer (haiku), spine-auditor (opus, read-only). Each states its tool-call budget: extractor 8, architect 10, scout 25, filler 20, answerer 4, auditor 12.

0.14 Hooks in `workspace/.claude/settings.json`: PreToolUse deny of git commit and push, ship.sh and reads of `/home/claude/.config` for subagents; SubagentStop on the filler runs verify.py and blocks with the failure list, at most 3 times. Dummy-test four things before relying on them: the hook can tell the lead from a subagent; it can identify the filler; a Bash write outside allowed paths is caught (if not, rely on the git check below); verify.py fits the hook timeout (else the hook runs a fast subset and B8 runs the full one). Regardless of hooks, B8 fails the batch if `git status` shows any tracked change.

0.15 `canary.py`: plants one defect per batch in one brief's audit copy, rotating through RECURRING_FAILURES and the s124 to s126 defects; records the diff; `ship.sh` refuses to ship if any canary text is present on the page. A second Opus agent, not the lead, adjudicates canary detection.

0.16 Workflow script `tools/spine/batch.workflow.js`: pipeline per brief through the stages below with schema outputs under 40 lines; full outputs stay in files. It runs only when Jonathan asks for a workflow run.

0.17 Contract upkeep: each new check gets mutation tests in `tools/tests/spine/` and a row in MIGRATION_CONTRACT (defect to rule).

## 3. Phase 1: pilot (frozen in `repair/efficiency/RUBRIC_spine.md` and committed before any run)

- Reference tasks (2): shipped psych spine briefs that are not goldens (for example psychosis and delirium), rebuilt from their pre-spine snapshots under the psych spec they shipped under. Quarantine their spine dirs, NEW_SOURCES_s123 to s126 entries, AMEND_LEDGER rows, DECISIONS_DIGEST and SPINE_SPEC lines that name them, and siblings' shipped bottom lines (siblings appear as pre-spine snapshots); packet.py asserts none appear.
- New tasks (3): unconverted FM or peds briefs other than the Phase 0 goldens: one with a claim map, one without, one hard (long, many items, a chart).
- Arms: C = current process on the frozen FM and peds spec (Opus author, Opus audit, lead fixes), given the same scripted retrieval (fetch.py, passages, quote_check) as the hybrids so source access does not differ between arms. H-S = hybrid with a Sonnet filler. H-H = hybrid with a Haiku filler. The architect and the auditor are Opus in both hybrid arms; audit cost counts in every arm.
- Runs: every task twice per arm (to see run-to-run variance); acceptance and audit counts use both runs.
- Frozen per-task checklist: the tested points each brief must teach (bank keys, NBME framing, and the must card statements from 0.6b), and for the reference tasks the decisions Jonathan approved. Card recall is a reported metric: the share of must statements covered or validly placed elsewhere.
- Acceptance per brief:
  - verify.py PASS;
  - an independent full-spec Opus audit, where the hybrid's HIGH plus MED total must not exceed C's;
  - a blinded Opus reviewer, seeing only the text render and a normalized claim map (line, quote, with arm-specific fields and formats stripped), scores the checklist, fidelity, scope and voice;
  - zero HIGH. Severity map: AUDIT_PROMPT HIGH = contract CRITICAL (reviewer list); MED = contract MINOR cases of items 9 and 13, overreach, hedge loss, contradiction, important omission; LOW = wording;
  - answerability not below the old brief.
- Before any arm is chosen, Jonathan reviews the 3 new briefs from every arm run (first run), blinded, as the text render plus screenshots; his change requests are counted and enter the adoption rule.
- Seeded-defect test of the lean audit packet plus scripts, 18 defects:
  - hedge lost, and turned to or, wrong timeline, causal arrow for an association;
  - contradiction with a bank key, adult rule in a peds brief, dropped tested claim, wrong drawer target;
  - spliced quote, chart value contradicting a bank item, differential row keyed to the wrong answer, illegible chart label;
  - a page fact whose only source is an AnKing card, a must card item marked `not-topic`, a candidate wrongly marked `not-topic`;
  - a sibling line left behind (P2), a cut that breaks a question (P3), two neighbor items with the same key (P4).
  - Pass at 17 of 18.
- Metrics: tokens per accepted brief including the lead, setup cost reported separately, tool calls, time, fix loops.
- Adoption: a hybrid is adopted only if all three hold. Haiku is chosen only if it meets the same rule against Sonnet.
  1. Acceptance equals or beats C, with Jonathan's change requests no higher.
  2. It shows no HIGH that C avoided.
  3. Tokens per accepted brief fall by at least 25%.
- Results in `repair/efficiency/RESULTS_spine.md`, with the not-proven list.

## 4. Phase 2: production loop per batch (6 to 8 briefs, one cluster)

Each batch starts in a fresh chat seeded with CURRENT_STATE.md, this plan and DECISIONS_DIGEST.md.

| Step | Who | Action | Exit condition |
|---|---|---|---|
| B0 | Lead | Pick a cluster from inventory.json; only entry types and lenses with a golden; siblings together | Batch list with entry type per brief |
| B1 | Script | Snapshot old briefs; packets for every role | Sizes under target; quarantine assert clean |
| B2 | Script, then Extractor | claims_map.py, extractor for the leftover | claims_check 100% span coverage |
| B3 | Script | Harvest dropped claims from every ledger | Count logged |
| B4 | Architect | outline.json (final text), chart specs, needs.json as questions, omissions.json (3 to 5) | outline_check PASS |
| B4.5 | Script, then Lead, then Architect | Merge batch outlines into OWNERS.json (diagnosis and card item to owning brief); Lead settles conflicts; each brief that lost an item gets an architect delta pass | No diagnosis or must item owned twice; outline_check PASS again |
| B5 | Scout, scripts | Answer each need blind from fetched passages, including contradicting sources, with a fit tag per answer; quote_check; then a separate conflict-check pass compares the brief's card items with facts.json | PASS; unanswered needs and card conflicts listed |
| B6 | Script, then Architect | Lines whose need went unanswered, or whose answer is tagged narrower, broader, different population or contradicts, go back to the architect for a delta pass; `conflict?` codes resolve. The brief stops for the Lead if any dropped claim is used by a bank key, explanation, NBME framing or nid, or if more than 15% of the old brief's text (by span) is dropped | outline_check PASS again |
| B7 | Filler | build.py rendering the outline exactly; verify.py loop | PASS (3 tries, then report) |
| B8 | Lead | Re-run verify.py on every brief; `git status` clean of tracked changes | All PASS |
| B9 | Answerer | Bank with and without the brief | Scores logged; misses into the audit packet |
| B10 | Auditor | Full audit, including every must card disposition and 5 random candidate dispositions; the canary brief is audited like the rest | Findings; canary judged by a second agent (missed means re-audit of the batch by a fresh auditor) |
| B11 | Lead | Adjudicate each HIGH and MED (accept or reject with reason); log in AMEND_LEDGER | Every finding has a disposition |
| B12 | Architect for wording, Filler for markup | Apply accepted findings; outline_check reruns on the changed outline; verify.py lists any change outside the named lines | PASS; no unnamed changes |
| B13 | Auditor | Delta audit of changed lines plus 3 lines of context for every HIGH fix | No new HIGH |
| B14 | Scripts | Combined preview; gate, render, preflight, vendor, legib, numbers on the combined page; canary absence | All clean |
| B15 | Script, Lead | Screenshots (desktop, phone, dark; each step open; full-resolution chart and drawer crops) and a contact sheet per brief; the Lead reviews crops, not thumbnails | No layout or legibility break |
| B16 | Lead | Approval packet to Jonathan: per brief the old vs new bottom line, the dropped list with reasons, new facts with sources, still-unsourced items, card recall and card conflicts, audit counts, then the screenshots | Approve or change requests |
| B17 | Lead | Apply changes; any defect a check missed goes through defect to rule (check, mutation test, rules line, re-check the batch) | Approved |
| B18 | Lead | ship.sh, then `postship.sh` (OPEN_WORK, log commit, push, version check, handoff in the project and on the Mac, mac_sync) | Live build matches; clean tree |

## 5. Cost controls

- A fresh chat per batch. The Lead reads JSON and script summaries, never whole builds or pages.
- Agents work from packets, never from skill files or the page, and report a gap instead of browsing.
- Retrieval is scripted: agents see passages, never whole web pages.
- Schema outputs are capped at 40 lines. Effort is low on Haiku stages and high only for the architect and the auditor.
- Tool-call budgets come from the agent definitions. An agent that hits its budget means the packet is missing something, so packet.py gets fixed.
- `repair/efficiency/ledger_spine.csv` records tokens per brief per role, every Opus pass (delta, shadow, second audits) and the setup cost.
- Stop rule: tokens per shipped brief, averaged over the 2 batches after the shadow period, must sit at least 25% below the s123 to s127 average. If not, stop and revert. Shadow-period cost is reported separately as a one-time cost.

## 6. Quality safeguards

Each risk is followed by what catches it.

1. A claim silently disappears: script-assigned pointers, span coverage at 100% including hover and chart text, a dropped list shown to the auditor and to Jonathan, and the B6 stop rule.
2. Fabricated, paraphrased or spliced quotes: only fetch.py writes the cache, quotes are single verbatim fragments, and the auditor sees 300 characters of context on each side.
3. Right quote, wrong population: population and setting are recorded per fact, outline_check flags a mismatch, and the auditor checks scope.
4. Meaning drifts at a handoff: the architect writes every word and the filler transcribes with an exact-match check. Rewording for shingles goes back to the architect.
5. The architect's decisions are wrong and get rendered faithfully:
   - the auditor attacks the decisions as well as the fidelity;
   - the two-pass answerability test;
   - the approval packet shows decisions in words.
6. Charts carry unsourced or contradicting values: the architect specifies each datum with a fact id, numbers.py checks chart values against bank items, and the auditor gets full-resolution crops.
7. Lean packets lose context:
   - sibling bottom lines, OWNERS.json and SPINE_SPEC rounds verbatim go into the packets;
   - a differential row whose diagnosis owns a brief must be a drawer;
   - the B4.5 merge catches ownership conflicts across the batch.
8. Correlated blind spots (same model family): a separate omission lens for the auditor, a rotating canary judged by a second agent, the shadow period, and Jonathan as the last check.
9. Rubber-stamp audits: a per-step checked list, and a second auditor for any zero-finding audit of a brief over 900 words.
10. Fixes introduce errors: changes outside the named lines are reported, there is a delta audit for HIGH fixes, and preflight runs again.
11. Scope creep and bloat: word caps enforced at the outline, a step2 basis for new rows (S2), and guideline-only detail kept in hovers.
12. Lost hedges and qualifiers: preflight P1, a hedge diff against the cited fragment only, and Q1 and Q2 on the auditor list.
13. A bank item is lost or altered: a byte-identical tail, the replace_brief contract, and the gate.
14. Vendor text leaks: the shingle check, vendor_scan, and local-only paths for packets, caches and quotes. Cached pages stay off the repo.
15. Agents act outside their lane: tool allowlists, hooks, and the B8 git check.
16. Parallel collisions: unique dirs per brief, with nothing shared until B14.
17. Spec drift: provenance hashes, and a re-pilot after any spec change.
18. Briefs without claim maps: each old line is either sourced or dropped with a reason, and any drop that touches a tested item stops for the Lead.
19. Invented mnemonics: the scout sources each one (K3, K4), and existing ones keep their data-mn-src.
20. Entry types or lenses with no golden: these stay excluded until one is approved.
21. Approval fatigue across about 25 batches: the approval packet leads with decisions and changes, and batches stay at 6 to 8 briefs.
22. Haiku failing a long spec: it only gets narrow schema tasks, and a brief escalates to Sonnet after 3 failed verify loops.
23. Gradual decay: a per-batch quality ledger tracks HIGH and MED before fixes, canary, answerability, Jonathan's change requests and post-ship defects. Revert the failing role to the current process if either happens:
    - two batches above the s123 to s127 HIGH rate;
    - any post-ship HIGH.
24. Card text drifts onto the page as fact (cards can be wrong: the s125 washout card): cards are leads only, quote_check refuses them as citations, and contradictions are logged, not imported.
25. Card checklist bloat or silent cuts: anchors over Extra detail, must and candidate tiers, a cap of 15 candidates with the cut logged, ids stable by hash, duplicates merged, and one owning brief per item.
26. Card wording copied onto the page: card text is vendor source for vendor_scan and verify.py.
27. A card steering the scout toward a wrong fact: the scout answers blind; cards are compared only afterwards.
28. A deck update changes cards mid-batch: the index hash is frozen per batch.
29. Shadow period: the first 2 production batches also get the full-spec Opus audit on every brief. Adopt fully only if it finds no HIGH that the lean audit missed.

## 7. Decisions

Decided by Jonathan 2026-10-10:
1. Plan approved; Phase 0 setup runs first. Psych hubs and screens may run on the current process alongside it; then the FM and peds goldens; then the pilot.
2. Word caps above the practice bank: disease about 1,300 words, drug about 1,000, presentation hub about 700.
3. Pilot arms: Sonnet and Haiku fillers (plus arm C).
4. Jonathan does the blinded pilot review of the 3 new briefs from every arm.
5. Full AnKing Step Deck indexed (2026-10-10).

Still open:
6. The source allowlist in 0.6 (default as written unless changed).
7. Workflow runs need Jonathan's explicit "use a workflow" each time unless he turns that on for the session.
8. Link repairs: 70 page nids do not resolve, and one brief carries a UWorld QID (115741) in data-nid; both go to the inventory.
9. Whether card conflicts should be collected for AnkiHub suggestions.

## 8. Audit log (v1 to v2)

Self-audit and independent Opus review, 2026-10-09. The critical changes:

- The cache can no longer be written by the scout. It was circular: the scout wrote what the check verified. Now only fetch.py writes it.
- Quotes can no longer be spliced with "...". A distance rule would still have passed the s124 buprenorphine splice.
- The architect now writes the final text. In v1 the filler reworded, so meaning could drift after the decisions were made.
- Pilot answers can no longer leak into the hybrid arms:
  - the goldens are no longer reference tasks;
  - quarantine is enforced.
- Pilot acceptance now matches the real bar: a full-spec audit, Jonathan's blinded review, and repeated runs for variance.

Major changes:

- Answerability now needs a with-brief and a without-brief pass, so outside knowledge can't hide gaps.
- Coverage is measured by spans, including attribute and chart text.
- Script-assigned source pointers.
- Needs are asked as questions, and contradictions are allowed.
- An architect delta pass after unsourced lines drop.
- Caps are enforced at the outline.
- The drop stop now keys on tested items.
- A batch ownership merge (B4.5).
- Lenses for FM and peds, plus goldens before the pilot.
- Charts are owned by the architect and audited from crops.
- Four hook assumptions are tested, with a git fallback.
- The canary can't ship and is judged by a second agent.
- Scripted passage retrieval, and full cost accounting with a stop rule.

Minor changes:

- The hedge diff runs against the cited fragment only.
- One severity scale.
- Recent real failures added to the seeded set.
- Blinding by a normalized render.
- SPINE_SPEC rounds included verbatim.
- Packet paths are local-only.

## 9. v2.1 (AnKing index wired in, 2026-10-09)

- The deck's Extra field (its pink text) becomes a per-brief checklist. Must statements come from cards linked by note id or UWorld QID; candidate statements come from subject and term matches, capped at 40 with the cut logged.
- Every statement gets a disposition code in outline_check, and one owner per batch.
- The architect, scout and auditor packets carry the checklist.
- The pilot reports card recall, and its seeded-defect set grows to 14.
- Cards stay leads, never citations. Contradictions go to card_conflicts.md.
- The index version is frozen per batch.
- An independent re-audit of v2.1 is recorded below when run.

Second independent review (Opus, 2026-10-09) of v2.1. Of the 23 v1 findings, 12 were fixed and 11 were partial. The partial ones are now closed:

- combined-source lines flagged (2);
- quarantine widened, and reference tasks run under the psych spec (4);
- two runs per task, and Jonathan reviews every arm before the choice (5);
- the answerer sees hover text and chart data, with two runs (6);
- fit tags trigger the delta pass, and the scout answers blind (9);
- B12 reruns outline_check (10);
- the 15% stop is measured by text span (11);
- the delta pass after an ownership loss (12);
- FM and peds lens lines, reviewer item 10, and N1 currency (13);
- the shadow cost is separated from the stop rule (17);
- a severity map (19);
- P2 to P4 seeded (20);
- the same retrieval in arm C, and stripped arm fields (21);
- scout excerpts keyed by question files (23).

The 15 new findings on the card wiring are all taken:

- card text added to the copy check (1, critical; code fixed and tested);
- a mnemonic locator the gate accepts (2, tested);
- `conflict?` codes at B4 (3);
- hash-based statement ids, deduplication and header joining (4, code fixed);
- cloze anchors and benchmarked recall (5);
- the S2 card exception narrowed (6);
- AnKing removed from the allowlist (7);
- a blind scout (8);
- a defined candidate score and validated data-nid links (9);
- candidates capped at 15 with sampled audit (10);
- owner obligations (11);
- OWNERS.json ids-only and local (12);
- the seeded count fixed (13);
- the recall definition (14);
- anki_index argument parsing and field selection by name (15, code fixed).
