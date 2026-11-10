# s172c: docs refactor. One home per document, a three-path router, plan files a cheaper agent can run

Status: SHIPPED 2026-11-10 (Jonathan "ship" 13:19; wip/s172c fast-forwarded to main in both repos; tools and docs
only, no page change). Scripts: workspace/repair/s172c/ (project_cleanup.py, its input and output).
Not read whole: DECISIONS_DIGEST, OPEN_WORK history, STANDING_DIRECTIONS (edited by anchored replacement and grep).

## Jonathan's words
- 2026-11-10 08:23: "can you resolve all these issues with the .mds and help establish a better agent and .md workflow.
  Whether that's consolidating .mds, pointing agents better, or having a better .md system or folder, etc."
- 2026-11-10 08:33: "Let's proceed based on your recommendations. The missing folder has been attached. I will be sure
  to attach it in the project for all future runs. You may now begin implementing the changes needed in order to
  improve the workflow, including deleting old documents. You have my approval to do so."
- 2026-11-10 12:16: "continue s172c (docs refactor, tools and docs only, no page change) per
  claude/pending/DOCS_REFACTOR.md, from its State. Jonathan approved every pick and the deletions on 2026-11-10 08:33."

## Picks (DIGEST D-20261110-1 to -5)
1. Old project copies of the rule documents: deleted (D-20261110-1).
2. Shipped-batch files under claude/pending/ in the project: deleted after a script confirms a record in a repo; any
   that fails is kept and listed (D-20261110-2).
3. WITHDRAWN: ~/Documents/Step2Haki exists; the project instruction stays as written (noted in D-20261110-3).
4. Handoff State capped; older entries in docs/SHIPLOG.md (D-20261110-3).
5. Launch read order by batch type, tools/spine/launch.py (D-20261110-4).
6. Mac folders refreshed to origin; stale untracked copies removed (D-20261110-5).

## Evidence (TESTED by listing, grep or the named command on 2026-11-10 unless marked ASSUMED)
1. Before: one document in up to five places, drifted (project copies from October; Mac ~/Step2Haki 102 commits
   behind; ~/step2haki-private at s147 with an untracked docs/).
2. Before: private main at 7a19960 held the s171b State; wip/s172 (7deba5d) held the s172 State.
3. Before: doc_lint with the new checks on the live docs: 20 stale path mentions (runbook 5, STANDING 4, handoff 11),
   no RESUME batch line, State 25 entries (commit dd7b9ad, public wip/s172c).
4. Before: handoff 45,384 bytes; OPEN_WORK 164,374 bytes; RESUME named s172 as open after it shipped.
5. After: handoff 2,865 bytes; SHIPLOG 21,941 bytes (24 entries); OPEN_WORK 14,570 bytes; OPEN_WORK_CLOSED 157,936
   bytes; RESUME 5,641 bytes; runbook 48,721 bytes (it gained sections 10 and 11 and the handoff's setup text).
6. After: `launch.py <type>` totals against the ten-document order read whole (409.1 KB): content 136.1 KB, patch
   86.5 KB, site 48.9 KB, tools 26.3 KB, plan 5.6 KB.
7. ASSUMED: the byte totals turn into a matching drop in context at the first edit. The next two launches record
   `usage_ledger.py --context` at the first edit in their batch file.
8. After: doc_lint (digest, paths, state) PASS, 60 ids; test_doc_lint 10 of 10; test_hooks 155 of 155; test_gate_rules
   38 of 38 (two new cases); gate on the site page PASS, 54 checks.
9. Rule-preservation grep before the handoff sections were removed: every "Standing rules" line is in
   STANDING_DIRECTIONS or the runbook except the pause point's word-cap exemption, which moved to runbook section 10;
   "Session start", "Where things live" and "Getting the page and publishing" moved whole into section 10; "Docs in
   this project" was a file list and was dropped.
10. Mac: all 25 untracked files in ~/step2haki-private (docs/, CONTENT_BATCHES_S170.md, content_audit_s169/) exist
    as blobs in the private repo (git cat-file -e on each hash) and were removed.

## State (rewrite after every step)
- DONE step 0: private main fast-forwarded to 7deba5d and pushed; wip/s172c branched in both repos.
- DONE step 1: doc_lint path_errors, state_errors, plan_errors; tools/spine/test_doc_lint.py; red first (dd7b9ad).
- DONE step 2: docs/RESUME.md rewritten from the project text; its batch line is written by tools/spine/docstate.py.
- DONE step 3: handoff holds state only; 24 State entries in docs/SHIPLOG.md; launch prompts in
  claude/pending/CONTENT_BATCHES_S170.md section 6 (private repo); setup text in runbook section 10.
- DONE step 4: runbook, STANDING_DIRECTIONS and handoff path hits fixed; check green.
- DONE step 5: OPEN_WORK split; an index of 55 "Open" clauses from the ship lines is in OPEN_WORK (not rechecked).
- DONE step 6: runbook "Read order by batch type", section 9 closing steps, sections 10 and 11; tools/spine/launch.py;
  resume.py reads the new State form and repair/<batch>/PLAN.md.
- DONE step 7, project: 37 documents deleted, 82 kept (48 for no record in a repo): project_cleanup.md.
- DONE step 7, Mac: ~/Step2Haki fast-forwarded to d3c914b (two local edits to the old efficiency RESUME and handoff
  are in `git stash`); ~/step2haki-private: the 25 untracked files removed. NOT DONE: its `git pull` (the Mac shell
  here has no credentials for the private repo; the gh_token covers the public repo only). Jonathan runs
  `git -C ~/step2haki-private pull` on the Mac; until then that clone has no docs/ folder.
- DONE step 8: DIGEST lines; gate and tests green; presented.
- DONE ship (Jonathan 2026-11-10 13:19: "ship"): main fast-forwarded in both repos; State entry "s172c SHIPPED";
  docstate.py sync; the handoff copied to the project and ~/Documents/Step2Haki, RESUME to the project;
  claude/pending/DOCS_REFACTOR.md deleted from the project (this file is the record).

## Open after this batch
- Context at the first edit on the next two launches (Evidence 7).
- 48 project documents with no record in a repo (project_cleanup.md, KEEP): each needs a keep, commit or delete call.
- OPEN_WORK index: 55 clauses not rechecked for closure.
- TEXTBOOK_STYLE, CARD_SPEC and the specs stay in the public repo (repair/efficiency/); moving them to the private
  docs/ would touch verify.py and the packet tools and was left out.
- The STANDING_DIRECTIONS edit (three path fixes) makes earlier review receipts stale, as in s165b and s170.

## Steps (tools-and-docs batch; no page change)
| # | Kind | Step | Done when |
|---|---|---|---|
| 0 | APPLY | Private repo: wip/s172 to main; branch wip/s172c in both repos | done |
| 1 | APPLY | doc_lint checks (a) to (d), each failing first | done |
| 2 | APPLY | RESUME from the project text; batch line written by a tool | done |
| 3 | APPLY | Handoff: State cap, SHIPLOG, sections moved after the rule grep | done |
| 4 | APPLY | Fix every stale path hit | done |
| 5 | APPLY | OPEN_WORK split | done |
| 6 | APPLY | Runbook read order by type, planning chats, launch.py, closing steps | done; two launch measurements open |
| 7 | APPLY | Project cleanup; Mac refresh | done except the Mac private pull |
| 8 | APPLY | DIGEST lines; gate; present; ship on "ship" | shipped 2026-11-10 |

