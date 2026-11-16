# Step2Haki: where an agent starts

Step2Haki is a Step 2 CK study page. The deployed page is discriminator-briefs-site/index.html (Vercel); the working
page is workspace/index.html. Briefs are built and changed in batches by a lead agent under a runbook, and nothing
ships without the owner's "ship".

## Start here
1. Clone both repos side by side: this one, and the private repo DrSaturnn/Step2Haki-private (rules, state, sources).
2. Read docs/RESUME.md in the private repo. It picks one of three paths from the owner's first line: continue an open
   batch, launch a new batch, or plan without building.
3. Run the tool that path names. Both print the core rules before anything else:
   - continue: `python3 workspace/tools/spine/resume.py`
   - launch: `python3 workspace/tools/spine/launch.py <content|patch|site|tools|plan>`

## Where things live
| What | Home |
|---|---|
| Rules, state, decisions, open work | private repo, docs/ (RESUME, STEP2HAKI_HANDOFF, STANDING_DIRECTIONS, DECISIONS_DIGEST, BATCH_RUNBOOK, SHIPLOG, OPEN_WORK, PLAN_TEMPLATE, ui/) |
| Sources and each brief's build folder | private repo, local-only/ (copied over workspace/ at session start) |
| Site code, tools, hooks | this repo, workspace/site/ and workspace/tools/ |
| Style and format specs, header and abbreviation lists, cost ledgers | this repo, workspace/repair/efficiency/ |
| A batch's plan and record | private repo, docs/batches/<batch>/ |
| A batch's edit files and scripts | this repo, workspace/repair/<batch>/ |
| Plan files before launch | the Claude project, claude/pending/ |

Tools find the private documents through workspace/tools/docs_path.py.

## Rules that hold everywhere
The nine core rules open docs/STANDING_DIRECTIONS.md and are printed at every chat start. Three that concern this
repo directly:
- No vendor text (question, card or exam wording) in this repo; the commit guard and the vendor scan refuse it.
- Code holds code: no decision quotes, names, dates or batch ids in comments.
- Never change ship.sh, the gate, approval.py or any check to make work pass.

## Checks an agent will meet
- Launch gate and call gate (workspace/tools/hooks/): an agent launch needs its role's model, a lane and a budget; an
  agent writes only inside its lane.
- The gate (workspace/tools/gate.py): 54 checks on the page, plus the document checks of
  workspace/tools/spine/doc_lint.py.
- Approval (workspace/tools/hooks/approval.py): ship.sh refuses a batch without the owner's recorded "ship".

## Other leads
Claude leads. Codex led batches from 2026-10-21 to 2026-10-23 and does not take the lead, launch, build or ship
unless the owner assigns it in writing; workspace/repair/efficiency/CODEX_LEAD.md describes that mode and predates the
move of the internal documents to the private repo.
