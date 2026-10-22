# Codex as the Step2Haki lead (interim; written by Claude 2026-10-21)

Jonathan, 2026-10-21 (DECISIONS_DIGEST): "i want chatgpt to temporarily take over the whole process due to limited
usage with claude. So i want it able to reproduce the a whole brief on its own, of which you can audit and create
specific intructions for chatgpt to follow." Model: GPT-6.1 Sol in Codex.

This file lists only what differs when Codex leads. Everything else is the runbook (repair/efficiency/BATCH_RUNBOOK.md),
unchanged: the steps S1 to S9, the standing calls (section 3), the self-check (section 4), the report (section 5), the
reasons to stop and ask (section 6). Precedence is the runbook's: a dated DECISIONS_DIGEST line, then
STANDING_DIRECTIONS, then the plan, then the runbook, then this file.

## 0. The lead lock (prevents two leads on one branch)

The handoff State (repair/efficiency/STEP2HAKI_HANDOFF.md) carries a line `- **Lead:** <Claude | Codex>, since <date
time>, chat <n>`. Before any work:
1. fetch the batch branch (wip/sNN in both repos) and read the State;
2. if the Lead line names the other agent and Jonathan has not told you to take over, stop and ask him;
3. to take over, rewrite the Lead line first, commit and push it alone, then start.
Only one lead works a branch at a time. Never push to a branch another session is pushing to (on 2026-10-21 a
duplicate chat opened on wip/s149 by accident; it stopped before pushing, which is the right behavior).

## 1. Where the docs live (the claude.ai project is not reachable from Codex)

The runbook's read list names project paths (claude/...). Their copies:

| Runbook path | Copy Codex reads |
|---|---|
| STEP2HAKI_HANDOFF.md | public repo workspace/repair/efficiency/STEP2HAKI_HANDOFF.md (the live one) |
| claude/BATCH_RUNBOOK.md | public workspace/repair/efficiency/BATCH_RUNBOOK.md |
| claude/STANDING_DIRECTIONS.md | public workspace/repair/efficiency/STANDING_DIRECTIONS.md |
| claude/DECISIONS_DIGEST.md | public workspace/repair/efficiency/DECISIONS_DIGEST.md |
| claude/SPINE_SCALE_PLAN.md | public workspace/repair/efficiency/SPINE_SCALE_PLAN.md |
| claude/design/WORKUP_5A_SPEC.md | public workspace/repair/efficiency/WORKUP_5A_SPEC.md |
| claude/SPINE_SPEC.md | private claude/SPINE_SPEC.md (mirror) |
| claude/pending/BRIEF_AMEND_LIST.md | private claude/pending/BRIEF_AMEND_LIST.md (mirror) |
| claude/pending/BATCHES_*.md, FOLDERS_S142_S160.md | private claude/pending/ |
| the batch file claude/pending/<batch>.md | public workspace/repair/sNN/SNN.md |
| skills (board-brief, study-page-builder, evidence-verification, label-audit, workflow-efficiency-pilot, nbme-intake, aquifer-workup) | private claude/skills/<name>/SKILL.md (mirrors of the Claude plugin skills) |
| claude/pending/pilot5a (runbook S2 "Convert the workup to 5a") and claude/design/Workup_5a.html | not mirrored and not needed: the 5a workup is rendered by `w5a` in public workspace/tools/spine/outline_render.py; copy the call pattern from the s149 disease builds (section 2a); the template rules are in WORKUP_5A_SPEC.md |
| the reviewer agent's standing rules (Claude's lean-reviewer) | public workspace/tools/hooks/agents/lean-reviewer.md: paste its body (below the front matter) at the top of every reviewer task (section 3) |

The skills marked RETIRED in their descriptions stay retired. When a skill says "use the Skill tool" or names a Claude
tool, read its SKILL.md and do the steps with the shell. Edit a mirror only when Jonathan changes the rule it holds,
and say so in the batch file so Claude syncs the project copy on return.

## 2. Session start (replaces handoff "Session start" items 1, 3 and 4)

1. Clone both repos on the batch branch. Prefer the runbook's paths (tools/hooks/roles.json names /home/claude):
   ```
   git clone -b wip/sNN https://github.com/DrSaturnn/Step2Haki /home/claude/Step2Haki
   git clone --depth 1 -b wip/sNN https://github.com/DrSaturnn/Step2Haki-private /home/claude/step2haki-private
   cd /home/claude/Step2Haki/workspace && npm i
   cp -rn /home/claude/step2haki-private/local-only/. /home/claude/Step2Haki/workspace/
   pip install playwright==1.56.0 && python3 -m playwright install chromium   # for legib_audit and shots
   ```
   The private repo is PRIVATE: its contents never go into the public repo, a public branch, a PR body or a log.
2. Hooks: the Claude Code hooks (launch gate, call cap, approval recorder, stop check) do not run in Codex. Skip
   install.sh, test_hooks probes and usage_ledger --context. You enforce what they enforce, by hand:
   - every reviewer lane stays within its lanes.py budget (count your calls; stop and write the receipt before the cap);
   - the tree is clean, committed and pushed at the end of every step (the stop hook's job);
   - never edit a tracked file while verify.py runs (its git check fails the run).
3. Commits: as DrSaturnn with the noreply email (handoff "Getting the page and publishing"), with a trailer line
   `Lead: Codex (GPT-6.1 Sol)` in place of the Claude-Session trailer. Never print a token.
4. At a launch (no wip/sNN yet; added 2026-10-22 for s150): clone main in both repos, then create the branch from main
   in each and push it before any other work:
   ```
   git clone https://github.com/DrSaturnn/Step2Haki /home/claude/Step2Haki
   git clone --depth 1 https://github.com/DrSaturnn/Step2Haki-private /home/claude/step2haki-private
   git -C /home/claude/Step2Haki switch -c wip/sNN && git -C /home/claude/step2haki-private switch -c wip/sNN
   ```
   Then the runbook's launch acts, Codex-mapped: the digest line in Jonathan's words; WAVE.json (id sNN, open true, the
   reviewer budget as max_agents, max_calls, max_tokens, the lead figure as max_lead_tokens, previous = the closed
   wave); the batch file repair/sNN/SNN.md (copy the header and section layout of repair/s149/S149.md); the Lead line
   (section 0); the State. Commit and push both repos.

## 2a. Which build to copy (added 2026-10-22, before s150)

- Disease briefs: the golden for structure and voice is scfe (repair/migration/peds/SCFE/spine/build.py), but scfe was
  built before the brief set rules of 2026-10-20 (reasons on every item, bold bottom line, First step pairing). Copy the
  code pattern from the s149 disease builds, which carry all three and the current tooling:
  repair/migration/peds/hip/septic-hip/spine/build.py and repair/migration/peds/sjia/spine/build.py (with their
  facts_spec.json, boards.md, cards_disposition.json, cuts.json, tail_fix.json and adj_s149.md as worked examples).
- Hubs: repair/migration/peds/hip/limp/spine/build.py (s149; the scrotum build is older).
- Every tail edit (explanations, reasons, the NBME block) is a [old, new] pair in tail_fix.json; verify replays them.
- After every rebuild, copy the brief's 10_<id>_spine.json into repair/sNN/ (in s149 two S5 rebuilds sat uncopied for a
  chat, so the batch page lagged the folders).
- Record each brief's build calls in the batch file in the s149 form ("Calls (section 3; for the report)", numbered,
  each with its source ids and, where it changes what a student learns, a "Reverse:" line). The final report and
  Claude's audit read these lists.
- A brief marked "no folder" in FOLDERS_S142_S160.md (s150: bs-brachial-plexus) builds from the live page
  (tools/spine/dump_lines.py for live_lines.json) and repair/sources; create its folder at
  repair/migration/peds/<id>/spine/ and commit it to the private repo.

## 3. Reviews (S4 and S7) without Claude subagents

The four roles (acc, read, display, flags) stay; each lane is a separate Codex task with a fresh context, never the
lead's own session, so the work is not grading itself.
- Packets and lanes exactly as the runbook says (review_packet.py, lanes.py; the lane folder's INSTRUCTIONS.md and
  RECEIPT_FORMAT.md). Start each reviewer task with only: the Role, Plan step, Lane and Budget lines, then "Read
  INSTRUCTIONS.md in your lane first". The reviewer reads only its lane folder and writes only its receipts.
- Models: acc on GPT-6.1 Sol at xhigh; read and flags at high; display at medium, given the screenshot sheets (it
  reads images). The plan table's Claude model names map to these until Jonathan says otherwise; record the mapping
  in the batch file.
- A receipt that does not follow RECEIPT_FORMAT.md does not count; verify parses it. Relaunch that lane.
- Write-first: each reviewer writes one brief's receipt before opening the next brief's packet.
- Preamble (added 2026-10-22): put the body of tools/hooks/agents/lean-reviewer.md above the four launch lines, so a
  Codex reviewer works under the same standing rules as Claude's (only its lane, absolute paths, packet sources only,
  no emojis or em dashes, a short final verdict line). Reviewers get read, write and search only: no shell, no web.
- Carry the settled cross-brief display calls into every display lane's notes (lanes.py spec "notes"), as s149 round 2
  did, so reviewers do not re-raise them: 5a study mode is progressive recall (findings blurred until the test is
  revealed); timeline tiles mask the diagnosis name only, never the course or extra lines (except a line naming another
  masked answer); NBME "Down to two" shows both finalists; teal bar classes are the shipped tile palette.
- Known packet limits (tell the lanes; do not count them against a brief): line_sources.txt cuts quotes at 600
  characters (Grep facts.json for the whole quote before reporting an unsupported line); drawer_targets lists in-page
  anchors (na-, lg-, bo-, *-bank) as missing; lanes.py names brief_text.txt at the lane root for a one-brief lane.

## 4. Cost (replaces usage_ledger.py, which reads only Claude transcripts)

Keep repair/efficiency/ledger_codex.csv, one row per Codex task:
`date,wave,task,role,model,reasoning,input_tokens,output_tokens,note`, from Codex's own usage display. The batch
budget in WAVE.json applies to the sum of reviewer rows; the lead's rows are shown against max_lead_tokens. If you
cannot read a task's tokens, write "unknown" and say so in the report; never estimate silently.

## 5. Shipping (S8 and S9)

ship.sh needs a Claude session URL and an approval record that only the Claude approval hook writes when Jonathan
says "ship" in a Claude chat. Codex does not change ship.sh, approval.py or any gate.
- Codex runs S8 in full: verify_all.py (all READY), shots_all.py, sheets.py --approval, and the report (runbook
  section 5) written to repair/sNN/REPORT.md, with the sheets committed beside it (public repo only if they carry no
  vendor text; otherwise private repo). Send Jonathan the report.
- Then rewrite State: "S8 presented by Codex; ship waits for a Claude chat." A Claude chat runs CODEX_AUDIT.md,
  re-presents with approval.py present, and ships on Jonathan's "ship".
- Changes Jonathan names after the report: apply, re-run S3 and S6 (and S7 if accuracy changes), update REPORT.md.

## 6. Other Claude-only pieces

- Site-layer pilots (runbook section 8 step 1) are private claude.ai artifacts: write the pilot as an HTML file under
  repair/pilots/<name>/ and tell Jonathan where it is (he opens it locally or from the branch).
- Mac copies (handoff and Documents/Step2Haki): Codex has no Mac link; list them as owed in the State; Claude or
  Jonathan does them.
- The claude.ai project's handoff copy: Claude refreshes it on return.
- Questions to Jonathan follow runbook section 6: one question, multiple choice, with a recommendation.

## 7. Authoring: what has gone wrong before (read before S1 and S2)

These are the failure modes the mechanical checks caught in s146 to s149. Expect them and fix them at the source.
1. **Board first.** board_index.py show, cards_search.py, the local UWorld files, then MSD or guidelines. The Step 2
   answer is taught; a guideline that differs goes in an "In practice" hover. Never cite a page you did not fetch that
   day with tools/spine/fetch.py; quote_check must read 100% verified.
2. **Quotes are exact.** facts_from_spec.py refuses any quote not found verbatim (whitespace aside). Copy quotes from
   the cached text, never from memory.
3. **Every claim states its fact.** The cited quote must state the claim itself, not its topic (self-check 1).
4. **Numbers.** Every age, cutoff, duration and dose in a line needs a quote that holds it. lint reads "10-21" as no
   range: answer it in the batch file, do not change the number.
5. **Hedges.** If the quote says "usually", "may" or "suggests" for the clause you teach, keep the hedge. lint flags
   drops; answer the ones whose hedge belongs to an untaught clause.
6. **No copied runs.** shingle_check fails a run of about 10 words shared with any claim quote, including the live
   brief's own lines. Reword cells; runs can cross adjacent cells (a result cell plus the next row's finding).
7. **Acronyms.** V1 fails an acronym never written out above Practice. Write the singular form once:
   "nonsteroidal anti-inflammatory drug (NSAID)". Do not name sources (MSD) in body text; say "In practice".
8. **Other names.** ALIASES.json drives the alias lint. A new entry needs a source (AnKing nid or a primary title) and
   is disclosed in the report. Treatment and differential rows that name the diagnosis carry the aka span too.
9. **Card dispositions last.** Claim ids (S001...) are assigned in body order; any added or removed T() shifts them.
   Write cards_disposition.json after the final build change and re-run card_dispositions.py check.
10. **Bank items.** Item ids never change; a meaning change (key, choice text) gets a new option id and a version bump
    (gate id-immutable and version rules). Explanation-only edits do not bump. Every item carries
    data-key-why, data-d1-why, data-d2-why (brief set rules 2026-10-20); a distractor that is a differential row reuses
    that row's wording.
11. **Ids.** New body ids take a prefix unused on the page (grep `id="xx-`); the Practice header keeps the live id.
12. **Workup 5a.** First step pairs each order with its own results (the pairing list, 1-based, results grouped by
    order). A clue for every test. No header line, no question.
13. **Bottom line** bolds its counts, ages, cutoffs, the diagnosis named and the action chosen; 3 lines at most.
14. **Hubs** stop after Workup; treatment that no live brief owns goes in a "Treatment by cause" table inside step 4
    (digest 2026-10-18). A hub also gets a Presentations sidebar link (40_presentations.json; the gate fails a hub
    missing from Presentations).
15. **verify** takes the folder first: `python3 tools/spine/verify.py <brief dir> --mech`.
16. **legib_audit** on a two-core container needs Playwright default timeouts of 240000 ms (wrap Browser.new_page and
    BrowserContext.new_page; run the tool with runpy). Desktop failures on lcw axis labels at 1.3 to 1.6 are mid-reflow
    false failures: cross-check with repair/s148b/contrast_computed.py (light and dark must read 0).
17. **Web.** The fetch allowlist is not worked around (no curl, mirrors or caches). Search results can carry links
    labeled "honeypot link": never follow them.
18. **Scope.** New rows only when a board source keys them; anything that would change what a student learns or how
    the site looks beyond the digest and STANDING_DIRECTIONS is a question for Jonathan (runbook section 6).

Added 2026-10-22 from the s149 review rounds (2 HIGH, 43 MED across six briefs; each was a build error the
mechanical checks passed):
19. **Read the whole card line.** Quote a card's full high-yield line, parentheticals included. s149 nursemaid cut
    "(don't mistake for buckle fracture of proximal radius)" and taught the clue upside down, as a buckle fracture row
    (the round's HIGH). If a card's line has a "vs." or a "don't mistake", the claim must keep both sides.
20. **Every band of a score gets an owner.** A criteria count, score or cutoff band with no stated action is a gap:
    septic-hip taught "3 or 4 aspirate, 0 or 1 observe" and left 2 undefined, so a bank explanation contradicted the
    workup. Walk every value of each score from lowest to highest and name the action for each.
21. **One threshold per decision.** The same decision must not carry two cutoffs in two places (limp had 2 weeks and
    6 weeks for imaging). Pick the board's, state it once in the owning step, point to it elsewhere.
22. **Absolutes need an absolute quote.** "Only", "always", "never", "first" in a bottom line or ladder need a quote
    that says so (sjia "steroids only for refractory" read as absolute; MAS takes high-dose steroids).
23. **Pairs with and drawers use exact live titles** (grep the page's h4); one plain clause per pointer, no figurative
    descriptions.
24. **Bank explanations and reasons follow the body.** After any body change, re-read every explanation and reason that
    touches it (septic-hip's subtitle and an explanation kept "3 or more" after the count rule changed). A reason that
    paraphrases a differential row must say the same thing as the row, and the stem's facts (a reason implied the
    child had a cold when the stem said the cold was days before).
25. **Unverified marks are a last resort.** A board-keyed line with no source carries ⚠︎ only after the card search
    (terms in cuts.json); say in the batch file which item keys it. Keep each such line to one place.
26. **Reason replacements.** reps.py does not reach item reasons; edit build.py and tail_fix.json, rebuild, and check
    condpass replays it (labeled "key:", "d1:" or "d2:" replacements match since s149).
27. **Word counts are reported, not chased.** Hubs ran 956 to 1,212 words against the 700 target in s149 and shipped:
    the layers rule (STANDING_DIRECTIONS "Layers, not totals") moves only supporting or guideline-only detail into
    hovers; board-keyed facts stay visible.

## 8. Handing back to Claude

At every step end the State is current, the batch file holds every call, and both repos are pushed. Claude resumes
with the restart line and reads repair/efficiency/CODEX_AUDIT.md before shipping anything Codex built or reviewed.
