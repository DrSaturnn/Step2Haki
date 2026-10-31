# Continue the open Step2Haki batch (the restart line points here)

Jonathan, 2026-10-26: "Add whatever is needed so this issue does not happen again" (s154f chat 3 read whole docs and
ran to about 280k context before any edit). Project copy claude/RESUME.md; repo copy repair/efficiency/RESUME.md.

**Open batch: s159** (Psych Pharmacology B1 of 4, launched 2026-10-30; branch **wip/s159** in both repos; batch file
repair/s159/S159.md; next step: S159.md "Next (chat 3)" step 1; s156 stays parked on wip/s156). (The lead rewrites this
line, here and in the project copy claude/RESUME.md, when a batch opens or ships; "none" means no batch is open and a
launch prompt is needed.)

Do these four steps, in order, and read nothing else first. Do not open BATCH_RUNBOOK.md, STEP2HAKI_HANDOFF.md,
STANDING_DIRECTIONS.md or DECISIONS_DIGEST.md through the project tool: it loads them whole.

1. add_repo DrSaturnn/Step2Haki and DrSaturnn/Step2Haki-private (access push), then clone on the branch above, one at
   a time, with a long timeout:
   ```
   git clone -q --depth 50 -b <branch> https://github.com/DrSaturnn/Step2Haki /home/claude/Step2Haki
   git clone -q --depth 1 -b <branch> https://github.com/DrSaturnn/Step2Haki-private /home/claude/step2haki-private
   cd /home/claude/Step2Haki/workspace && npm i --silent && cp -rn /home/claude/step2haki-private/local-only/. .
   ```
   Do not call register_repo_root.
2. `python3 tools/spine/patch.py setup <batch>` (hooks, including H6, the context alarm: it warns at start + 150k and gives
   one finish notice at start + 200k; "start" is the chat's first reading, about 130k).
3. `python3 tools/spine/resume.py`: the handoff State, the batch file's sections with line ranges, its chunk table,
   the DIGEST lines naming the batch, and the reading rules.
4. Read only the batch-file section the State names as next (`sed -n A,Bp`), and start that step.

Reading rules for the rest of the chat:
- The runbook, STANDING_DIRECTIONS and DIGEST are grepped for the topic of the edit in hand, never read whole. Before
  any display or content edit, grep both for its topic: a rule may live outside the batch file.
- Briefs are read through scripts (pagelib, review_packet, lint, mentions, the batch's helpers), never as raw HTML.
- A survey (several briefs, or output over about 3k tokens) is written by a script to local/<batch>/survey_<topic>.md;
  the chat gets counts, and the file is read by section.
- Each chunk ends by writing the next chunk's exact edits into the batch file, then the State, commit and push.
- At the H6 warning, finish the step in hand; at the stop notice, write State and send only the restart message.

A launch (a new batch id in Jonathan's prompt) is not a continuation: it follows the runbook's full read order, read
from the repo copies by section after the clone.
