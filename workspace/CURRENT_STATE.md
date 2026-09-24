# AxBx: current state (read this first; one page)

Updated 2026-09-24. Replaces reading OPEN_WORK.md or past transcripts. Open OPEN_WORK.md only for history of a specific pass.

## What it is
Step 2 CK / Peds and FM shelf study page: `/home/claude/axbx/index.html` (git repo). 201 briefs, 1,942 questions, 13 organ-system sections. Brief kinds: topic (`brief`), board-style (`brief bs`), Aquifer workup (`brief aq`). Every brief carries `data-bp` (NBME system). Questions are `<li>` in `ol.bank` with immutable ids from `tools/idgen.py`.

## How a batch ships
1. Save the pasted source close to verbatim: `repair/sources/sNN_questions.md` (never embed vendor images; page text is paraphrase).
2. Grep each nid; find the owning brief (`tools/nbme_match.py "<key>" "<stem>"` ranks candidates).
3. Route: UWorld -> board-brief rules; NBME forms -> `nbme-intake` skill (four-way sort, `data-nbme` link, coverage row); Aquifer case -> `aquifer-workup` skill.
4. Draft. Backfills into an existing brief: worker packet (`python3 repair/efficiency/make_packet.py <T> <brief> <source.md> "<Q heading>" "<task>" index.html <out.md>`), one agent per brief, agent runs `tools/verify_edits.py`. New briefs and Aquifer workups: full spec (`repair/workup/SPEC_s19.md`, `SPEC_aq.md`) until piloted.
5. Build `repair/build_sNN.py` from the previous builder, then `tools/ship.sh sNN "<message>"` (build, apply, gate, render, commit, copy outputs in one call), then SendUserFile.
6. Log one line in OPEN_WORK.md; questions for Jonathan go in PENDING_DECISIONS.md.

## Standing rules
No emojis, no em dashes in prose; plain voice, no slogans; label speculation; ⚠︎ only for memory-sourced or unverified specifics; Step 2 depth; emphasize cutoffs and tells; plain captions ("X: the differential", "Diagnostic workup"). Current guidelines set facts; NBME sets key and framing; then UWorld; then authored. Never delete questions; attribute-only edits use the ledger `set_attr` op and `gate.py --attr-only HEAD`.

## Open
See PENDING_DECISIONS.md (VUR fixes researched not written; thumbnail pilot; retitles; spelling pass; 17 blueprint judgment rows; Aquifer narratives; s23 UWorld text). NBME plan phase 7 (review weighting) not started. Efficiency: worker packet adopted for backfills only (repair/efficiency/RESULTS.md).

## Chat efficiency (measured 2026-09-24)
Each tool call re-reads the whole chat context. This chat reached 670k context; one call cost ~670k cached tokens, and a typical batch (about 20 calls) cost 7 to 8M. Rules:
- Start a fresh chat when context passes ~250k, seeded with this file only.
- One shipping call per batch (`tools/ship.sh`); print summaries, not files; read only the part of a file you need.
- Agents return 3 to 6 line reports.
- Paste question text; attach an image only when it carries information the text lacks, and once.
- Measure with `python3 tools/session_usage.py <transcript.jsonl> --since <time>`.
