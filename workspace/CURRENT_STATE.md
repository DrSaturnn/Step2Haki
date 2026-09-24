# AxBx: current state (read this first; one page)

Updated 2026-09-24 (workspace moved into the public Step2Haki repo; see OPEN_WORK.md). Replaces reading OPEN_WORK.md or past transcripts. Open OPEN_WORK.md only for history of a specific pass.

## What it is
Step 2 CK / Peds and FM shelf study page: `workspace/index.html` in the public GitHub repo https://github.com/DrSaturnn/Step2Haki (working copy `/home/claude/Step2Haki/workspace`; `/home/claude/axbx` is retired). The site Vercel deploys is `discriminator-briefs-site/index.html` (Root Directory = discriminator-briefs-site, skipped when that folder is unchanged); `tools/ship.sh` copies the page there. 201 briefs, 1,942 questions, 13 organ-system sections. Brief kinds: topic (`brief`), board-style (`brief bs`), Aquifer workup (`brief aq`). Every brief carries `data-bp` (NBME system). Questions are `<li>` in `ol.bank` with immutable ids from `tools/idgen.py`.

## Start of a session
1. `git clone https://github.com/DrSaturnn/Step2Haki /home/claude/Step2Haki && cd /home/claude/Step2Haki/workspace && npm i` (jsdom 24 from package.json).
2. Restore the private local-only files (vendor text, never in git): `tar -xzf axbx-local-only.tar.gz -C /home/claude/Step2Haki/workspace` from the Mac backup `AxBx iOS/study-page/axbx-local-only.tar.gz` (every ship also writes a fresh copy to /mnt/user-data/outputs). Without it, ship prints `vendor: NOT CHECKED`.
3. Pushing needs a GitHub token in `/home/claude/.config/axbx/gh_token` (one line, mode 600). Without it every ship still commits and prints `push skipped: no token`. The token file lives on the Mac at `Documents/AxBx iOS/study-page/gh_token` (fine-grained, Step2Haki only, Contents read/write, 90-day expiry); stage it and move it into place without printing it. Commits must use the GitHub noreply email (ship.sh sets it) or GitHub rejects the push.

## How a batch ships
1. Save the pasted source close to verbatim: `repair/sources/sNN_questions.md`. It is local-only (`tools/local_only.txt`, gitignored, removed from all history): vendor text never enters the public repo. Never embed vendor images; page text is paraphrase.
2. Grep each nid; find the owning brief (`tools/nbme_match.py "<key>" "<stem>"` ranks candidates).
3. Route: UWorld -> board-brief rules; NBME forms -> `nbme-intake` skill (four-way sort, `data-nbme` link, coverage row); Aquifer case -> `aquifer-workup` skill.
4. Draft. Backfills into an existing brief: worker packet (`python3 repair/efficiency/make_packet.py <T> <brief> <source.md> "<Q heading>" "<task>" index.html [--edits repair/sNN/10_bf_<brief>.json]`; packets go to local-only `repair/sources/<T>_packets/` and quote vendor text, so never write them elsewhere), one agent per brief, agent runs the packet's `tools/verify_edits.py <edits> --nids <source.md>` from the workspace folder. New briefs and Aquifer workups: full spec (`repair/workup/SPEC_s19.md`, `SPEC_aq.md`) until piloted.
5. Put the batch's edits files in `repair/sNN/*.json` (format: `tools/EDITS.md`; applied in name order by `repair/build.py sNN`, which replaces the per-batch `build_sNN.py`), then `tools/ship.sh sNN "<message>"`: build, gate, render, vendor scan (no source text in tracked files; page under 0.1% shared shingles and no shared run over 25 words), copy to `discriminator-briefs-site/index.html`, commit with a body generated from the page diff (also prepended to `CHANGELOG.md`), push to origin main when the token exists, and write `index.html`, `axbx-repo.bundle` and `axbx-local-only.tar.gz` to /mnt/user-data/outputs. Aborts before writing on any failure. Then SendUserFile.
6. Log one line in OPEN_WORK.md; questions for Jonathan go in PENDING_DECISIONS.md.

## Standing rules
No emojis, no em dashes in prose; plain voice, no slogans; label speculation; ⚠︎ only for memory-sourced or unverified specifics; Step 2 depth; emphasize cutoffs and tells; plain captions ("X: the differential", "Diagnostic workup"). Current guidelines set facts; NBME sets key and framing; then UWorld; then authored. Never delete questions; attribute-only edits use the `set_attr` op in an edits file and ship with `tools/ship.sh sNN "<message>" --attr-only` (runs `gate.py --attr-only HEAD`). The skills' older names map as: ledger / `repair/apply_ledger.py` -> `tools/apply_edits.py`; `gate.py index.html --base 092f98b` -> `gate.py` (base HEAD; the old hash is gone, the restored baseline is commit d233a96).

## Open
See PENDING_DECISIONS.md (VUR fixes researched not written; thumbnail pilot; retitles; spelling pass; 17 blueprint judgment rows; Aquifer narratives; s23 UWorld text). NBME plan phase 7 (review weighting) not started. Efficiency: worker packet adopted for backfills only (repair/efficiency/RESULTS.md, RUBRIC.md, runs/).

## Tooling (rebuilt 2026-09-24)
`tools/pagelib.py` (depth-matched parsing, offset splices), `gate.py` (mechanical invariants; `--list` shows them), `render.js` (jsdom smoke render; needs `npm i jsdom@24` in the repo, never v30), `apply_edits.py` / `verify_edits.py` / `EDITS.md`, `idgen.py`, `nbme_match.py`, `session_usage.py`, `ship.sh`; `repair/build.py`; `repair/efficiency/RULES_worker.md`, `RULES_coverage.md`, `make_packet.py`. Pre-existing baseline findings are allowlisted, not fixed: `tools/gate_allowlist.txt` (16), `tools/render_allowlist.txt` (1); fix them in a content pass and delete the lines. Also `tools/vendor_scan.py` (10-word shingle check against local-only sources; `--history` scans every blob), `tools/changelog.py` (commit body), `tools/local_only.txt` (private paths).

## Chat efficiency (measured 2026-09-24)
Each tool call re-reads the whole chat context. This chat reached 670k context; one call cost ~670k cached tokens, and a typical batch (about 20 calls) cost 7 to 8M. Rules:
- Start a fresh chat when context passes ~250k, seeded with this file only.
- One shipping call per batch (`tools/ship.sh`); print summaries, not files; read only the part of a file you need.
- Agents return 3 to 6 line reports.
- Paste question text; attach an image only when it carries information the text lacks, and once.
- Measure with `python3 tools/session_usage.py <transcript.jsonl> --since <time>`.
