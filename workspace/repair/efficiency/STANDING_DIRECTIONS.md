# Step2Haki standing directions (every direction Jonathan has given, compiled with its source)

Compiled 2026-10-10 because the plan v4 restart prompt pointed new chats only to the handoff, the plan and the
decisions digest. Most of Jonathan's directions on brief format live elsewhere, so the second chat re-proposed a
workup that opens with a question, which he had already dropped on 2026-10-07.

**Read this file before any brief, display or content work.** If a direction here conflicts with a later dated
decision in DECISIONS_DIGEST.md, the later one wins; say so and update this file.

Source keys:
- [SPEC] claude/SPINE_SPEC.md, with its dated rounds;
- [DIG] claude/DECISIONS_DIGEST.md;
- [MEM] Jonathan's saved directions in Claude memory (the Step2Haki area files);
- [PREF] his saved preferences;
- [HO] the handoff's standing rules;
- [CS] the 2026-10-03 CURRENT_STATE;
- [OW] OPEN_WORK.md.

## Accuracy and sources
- PSGN latency wording, wherever stated: "weeks, not days: about 1 to 3 weeks after strep throat, up to about 6 weeks after impetigo; often summarized as 2 to 4 weeks." [DIG 2026-10-12]
- Accuracy is non-negotiable; teaching something incorrectly defeats the purpose of Step2Haki. [DIG 2026-10-10]
- The standard of correct is what Step 2 rewards. Where literature or clinical practice differs from the boards, follow UWorld's and AnKing's approach (NBME, then UWorld, then AnKing). [DIG 2026-10-10] [MEM]
- Zebras are taught as safeguards for recognizing rare dangerous diagnoses, never as claims that they are common. [DIG 2026-10-10] [MEM]
- Every fact comes from a UWorld question, explanation or library page, or from a primary source. [SPEC Boundaries]
- Content comes from the pasted source or a verified source; it must be Step 2 relevant and must not overdo scope. [MEM]
- No drift from source content: this is the highest priority when migrating or reauthoring. [MEM]
- Use every clue from UWorld and NBME source stems, pertinent positives and negatives included; none is omitted or retired. [MEM] [CS]
- Mnemonics are never invented; only widely accepted ones (for example in AnKing, or explicitly taught to medical students and clinicians). [MEM]
- Pink text on AnKing cards (the Extra field) correlates very strongly with tested topics; treat it as priority content when mining cards. [MEM] [DIG 2026-10-09]
- Label anything unverified. [HO] [PREF]
- Vendor text never enters the public repo; saved question sources stay local. [MEM] [HO]

## Scope of a brief
- Main text is what UWorld and NBME test. Guideline-only details go into hover cards or the collapsed panel, never their own rows or rungs. Contested labels that are not tested are cut, and the tested competitor gets the row (PANDAS cut, Sydenham chorea kept). [SPEC r4]
- Include only what a Step 2 item could key or use as a distractor; doses only where tested. [SPEC Boundaries]
- Brief titles are generalized, as wide as is reasonable, to avoid many briefs on similar topics; a brief that truly stands on its own can stay separate. [MEM]
- Word caps above the practice bank: disease about 1,300, drug about 1,000, presentation hub about 700. [DIG 2026-10-10] They are soft: a brief may exceed its cap for board-tested content, and each overage is listed for Jonathan with its count and what would have to go. [DIG 2026-10-12]
- A brief may run over its word target because of a mnemonic. [MEM]
- Peds authoring priority: cardiovascular and respiratory first, then endocrine and female reproductive, then neuro and MSK, skin last; outpatient framing; weighted toward recognizing the diagnosis. [MEM]
- Peds shelf (2026-09-25) felt more nuanced than covered content, with few derm and many outpatient questions; use this as the guide for upcoming peds briefs. [MEM]

## Brief structure (decision spine)
- **Step names**, in every brief: 1 Illness script (disease) or Presentation (hub), 2 Urgent risks, 3 Differential, 4 Workup, 5 Diagnostic criteria, 6 Severity (or the field's native term), 7 Treatment, 8 Follow-up. Absent steps stay numbered and greyed. [SPEC r3, r4]
- **Hubs and disease briefs:** presentation hubs open with the presentation, have no illness script, stop after Workup and hand off by drawer. Disease briefs open with the illness script. [SPEC r3]
- **Bottom line:** above the script, 3 lines at most, holding the decisions most likely to be tested. [SPEC r3]
- **Illness script:** in Jonathan's template order (What it is; Driver or Bug; Triggers or Spread, strongest first, non-modifiable marked; Chain in tiers of one kind of event; exactly two Insights). It holds only what no other step covers. [SPEC r3] [PREF]
- **Compact intro:** the intro is short phrases joined by + and arrows, with pale glyphs. Detail goes in the collapsed panel. [SPEC r4]
- **Differential:**
  - ordered by how tempting each option is;
  - every Decides-it cell leads with its timeline in bold when the diagnosis has one;
  - discriminator tables give each diagnosis's timeline, and are repeated in every topic brief they pertain to, because readers review one brief at a time and these are the most heavily tested contrasts. [SPEC r4] [MEM]
- **Psych tables:** they keep the duration column, because NBME tests long duration windows (for example 2 years); the long timelines are clarified. [MEM]
- **Step 4 Workup:** the diagnostic workup tree, then the clue table, then the pause point. [SPEC r2]
- **The Narrow or clue table:** Clue | Points to | Next move, with NO questions and no in or out chips. [SPEC, MDD pilot review 2026-10-07]
- **Workups are not question-led.** s115 (question-led workups) was dropped on 2026-10-07, and Jonathan re-stated the rule on 2026-10-10: a workup must not open with a question. [SPEC status] [Jonathan 2026-10-10]
- **Captions and headers** are plain labels, never catchy phrases. [SPEC r2] [OW s17]
- **The workup caption** is "Diagnostic workup". [OW s18]
- **Treatment:**
  - one ladder panel; numbered rungs joined by a rail; each rung reads tag, when (the trigger), then the move; the last rung is caution-colored;
  - before switching, a Raise tier for partial response. [SPEC r2, MDD review]
- **Severity:** a severity instrument is shown as the instrument itself, then a score bar with bands that name the action. [SPEC r2, MDD review]
- **Criteria tile:** names are short so they fit on one phone line; duration cutoffs are bold. The tile carries the mnemonic. [SPEC r4, MDD review]
- **Abbreviations:** very commonly used labs and imaging are written short (CBC, BUN, US for ultrasound, CT, CT angio or CT angiography, MRI), from one shared allowlist, repair/efficiency/ABBREV.json; less common items are spelled out at first use or in a hover; new allowlist entries are listed in the batch report. Replaces the narrower CT exception of 2026-10-11. [DIG 2026-10-12]
- **Other names:** a diagnosis with more than one name is named with its other names at first mention and in its differential row, for example "Conversion disorder (functional neurological symptom disorder)", because NBME often uses the less familiar forms; one shared table, repair/efficiency/ALIASES.json, built from AnKing cards, NBME items and DSM-5-TR or ICD names; alias words do not count against the soft word cap. [DIG 2026-10-12]
- **Widen, don't shorten:** text that wraps into a narrow column is widened, never cut to fit; on phone, a 5a clue takes the band's full width. [DIG 2026-10-12]
- **Row drawers:** a differential row whose diagnosis owns a brief is a drawer button. [SPEC migration rule]
- **Repeated links:** a link may appear more than once in a brief (not a hard rule), but keep clutter down overall. [DIG 2026-10-12]

## Display
- **Diagnostic workup template: layout 5a (2026-10-11).**
  - Each clue and its order sit on one tinted band row: clue, then an arrow, then the order.
  - Below the band, untinted and smaller, each finding branches from a stem and leads to its meaning by a connector and arrowhead.
  - Zones: First step, By presentation (renamed from "By clue"), Next step, Diagnostic test (Step 2's term), then Skip. [DIG 2026-10-11]
  - Phone: the finding column is a little wider than designed, for less wrapping. Desktop: the meaning cap stays, for grouping and scanning. [DIG 2026-10-11]
  - Spec and design file: claude/design/WORKUP_5A_SPEC.md and claude/design/Workup_5a.html.
  - This supersedes the s127 headed cards, the 2026-10-10 R1 rail removal and the "vertical line with dots"; the s130 numbered and forked layout stays rejected.
  - Phone finding column 120 px. Breaks fall after a slash, never mid-word. [DIG 2026-10-11]
  - No header line above the zones: the rollout drops all 60 numbered workup header lines (questions and summary lines alike). [DIG 2026-10-11]
  - Study mode is progressive recall:
    - the clue stays visible and the test is masked;
    - that band's findings wait, blurred, until the test is revealed;
    - each meaning then reveals on its own;
    - the Skip line is masked. [DIG 2026-10-11]
  - The build questions in the spec are answered (2026-10-11); see the digest.
- **Workup display rules (2026-10-10, carried into 5a):**
  - indication and test on one line in the darker tinted band, enlarged, vertically centered, reading left to right;
  - findings below, lighter and smaller;
  - no accent rule beside results;
  - clue-directed choices grouped apart from the next step and the most diagnostic test;
  - low cognitive load;
  - plain labels;
  - one aligned left edge. [Jonathan 2026-10-10]
- **Workup grouping:** first-line tests stay grouped in their own tile. [MEM]
- **Bottom lines:** split into short paragraphs, with ordered labs on indented lines. [MEM]
- **Timelines:** horizontal duration timelines (vertical was only a suggestion); for much of the psych content, timelines are authored in addition to the brief. [MEM]
- **Timeline ticks:** tick labels repeat on every timeline row, placed where they best line up with that row's bars. [MEM]
- **Chart and timeline colors:** a softer, pastel-leaning palette that still matches the app's theme. [MEM] [HO]
- **Timeline legibility:** charts use the voices-chart style site-wide (per-row legends, no nested frames). [DIG 2026-10-09]
- **Theme tokens:** every spine surface is a theme token; no raw colors; must pass legib_audit in sculpted, flat and study modes. [SPEC MDD review]
- **Phone table cards:** every value starts on one left edge. [SPEC MDD review]
- **Drawers:** a 520 px floating panel on desktop, a bottom sheet on phones; drawers show the whole linked brief minus its practice questions; they never nest. [SPEC r2, MDD review]
- **Inline explanations:** hover or click cards on desktop; on touch they open inline. [SPEC MDD review]
- **Mnemonics:**
  - the capital is centered in the tinted column; [SPEC r2]
  - the typography is legible, so the acronym's letters read down on their own. [MEM]
- **No NBME markers on psych chart rows,** because not all NBME questions have been authored yet. [MEM]
- **Mobile Index:** opens from the top left by tap, not by swipe. [MEM]
- **BOARD-STYLE ONLY filter:** resets to off on every visit. [MEM]
- **Board-style and NBME overlap:** board-style briefs that overlap an NBME question show only the NBME badge. [MEM]

## Practice questions
- **Original stems:** authored items are original. UWorld shows only the concept tested and which two answers it leans between. Stems are unique and concise, with pertinent positives and mimic traps, never a retold UWorld vignette. [MEM] [HO]
- **Length and layout:** authored stems are 30 to 40 words, in scannable lines. [MEM] [HO]
- **NBME questions:** they are not in the scenario bank. They live in the "How NBME framed it" block, as a de-fluffed stem plus the competing answers and the final two choices. [MEM]
- **Practice view:** stack by default (Stack | List | Review); Reveal all only in List. [SPEC r2]
- **Questions are never deleted;** item ids are immutable. [CS]

## Prose and voice
- **Plain prose:** clear and concise, with no cliché or slogan-style language; internal workflow terms (for example "handoff") never show on the page. [MEM] [CS]
- **No emojis, no em dashes.** [PREF] [HO]

## Process and approvals
- **Approval before shipping:** nothing ships to the live site without Jonathan's approval. A blanket "publish and continue" covers only the queue he named. Screenshots come before approval. [MEM] [SPEC Boundaries]
- **Mechanical approval gate:** ship.sh refuses a batch unless an approval record for that exact build exists, written only by the hook when Jonathan says "ship" in reply to the screenshots (tools/hooks/approval.py). [DIG 2026-10-12]
- **Board sources first (2026-10-12):** before building or fixing any brief, search the local UWorld questions, the AnKing deck and NBME items for the topic and record the Step 2 answer for each testable claim; MSD and guidelines then add support or "In practice" notes; where they differ, the brief teaches the board answer and labels the difference; no vendor wording; report how much of UWorld the local question files cover. [DIG 2026-10-12]
- **Analogy label:** a step supported only by a source about another population (for example cirrhosis) is labeled as an analogy at the step itself. [DIG 2026-10-12]
- **Word-cap overage:** up to 5% made of board-tested content or fixes for reviewer findings is approved without asking and listed in the report; ask above 5%. [DIG 2026-10-12]
- **LOW findings:** the lead sorts them into fixed, deferred (with where each goes) or rejected, without asking. [DIG 2026-10-12]
- **Follow-up reviews:** always the same four roles, changed lines only, 10 calls each, within the batch budget. [DIG 2026-10-12]
- **When to ask:** only for a HIGH finding no source settles, a decision not covered by the digest or these directions, a budget overrun, or anything irreversible. [DIG 2026-10-12]
- **One report per batch:** edit list with screenshots, decisions needed (ideally none), cost; Jonathan replies "ship". [DIG 2026-10-12]
- **Budgets** are Jonathan's to set; standing allowance for safeguard and hook tests only, up to 2M tokens per round, reported after. [DIG 2026-10-12]
- **Batch runbook (2026-10-12):** every batch runs under repair/efficiency/BATCH_RUNBOOK.md (project copy claude/BATCH_RUNBOOK.md). Jonathan is asked at launch and at "ship"; everything between is decided under its rules, recorded, and disclosed in the final report. Its standing calls (section 3), decided, recorded and disclosed without asking: [DIG 2026-10-12]
  - word count over the soft cap: up to 5% of board-tested content or fixes, keep and list; above 5%, cut lines no board source tests (adult-only lines in a peds brief, mechanism hovers) until within 5%, list each cut with its words; recount after the last fix;
  - a step supported only by a source about another population: keep it only if a board source teaches the step, and label the analogy at the step ("as for ... in ...");
  - a board answer that differs from a guideline: teach the board answer, the guideline goes in "In practice:"; every age, cutoff, duration, dose and interval checked against board sources;
  - a claim with no source opened that day: board-tested, label it unverified (⚠︎) and list it; not board-tested, cut it;
  - a number in a new or changed line with no quote: find the quote or cut the number;
  - two places deciding the same action: one owner, the other points to it;
  - a study-mode leak from a repeated table or line: mask the repeat, never delete it;
  - a parked change or reviewer suggestion that reverses a digest decision: reject it;
  - reversing the lead's own earlier verdict: allowed with a recorded reason, listed in the report;
  - a finding caused by the reviewer packet: a packet error with evidence; fix review_packet.py; not counted against the brief;
  - LOW findings: sorted; none blocks;
  - a tool or check change a step needs: allowed, with offline tests for the risky cases; the diff goes in the report (G-DIFF);
  - a display choice the spec does not cover: follow the nearest line in these directions and name it in the report;
  - abbreviations, other names, and text in a narrow column: per the Abbreviations, Other names and Widen lines under Brief structure.
- **Conditional PASS (2026-10-12):** a reviewer with only LOW findings may return "Verdict: PASS-IF" with exact old and new wording per finding; verify counts it as PASS when the brief differs from what was reviewed only by some of the approved replacements. Replacements change text only, never markup or study-mode masks; no new facts, no changed numbers, no changes to item stems, keys, distractors or lead-ins; at most 8 per receipt, 40 words each. A replacement approved by one part keeps the other parts' receipts current only if it passes the wording-only test (same numbers, negations, diagnosis, drug and test names, and hedge words: may, usually, often, can, rarely, about, consider); otherwise that part gets the normal follow-up review. [DIG 2026-10-12]
- **Per-brief budget (2026-10-12):** 12 agents, 90 API calls, 9.5M tokens until conditional PASS is proven in a live batch; then 8 agents, 60 calls, 6.5M. Batches: R5 at 2 briefs, 4 once a 2-brief batch finishes in one chat; step D the same. R4 deferred until a cheaper role is proposed to replace an Opus step. [DIG 2026-10-12]
- **Adversarial audits** on every brief. [SPEC Boundaries]
- **The holistic review:** each brief must read as one whole brief, not just meet its requirements. [DIG 2026-10-10]
- **Cheaper models:** multi-agent plans assign cheaper models (for example Haiku) to their planned portions; the efficiency pilot methods apply to batch authoring. [MEM]
- **Assessing past work:** judge prior work against the git push record and the in-page changelog. [DIG 2026-10-10] [MEM]
- **Who works on it:** only Claude works on Step2Haki. Codex and ChatGPT are used only to critique Claude's plans and documents. [MEM]
- **The handoff:** after each shipped batch, update STEP2HAKI_HANDOFF.md in the project and in Documents/Step2Haki. [Project instructions]
- **Pacing:** psych briefs are reauthored one at a time, to ensure accuracy. [MEM]
- **Cross-shelf content:** being weighed, as separate psych-perspective briefs for topics covered by other shelves. [MEM, 2026-10-05]

## Repo and files
- **The repo:** public, DrSaturnn/Step2Haki; the site deploys from discriminator-briefs-site. Each ship commits a description of what changed. [MEM]
- **The Mac folder:** Step2Haki lives in Documents/Step2Haki, its own folder, separate from AxBx iOS. [MEM]
- **No scratch files** in his Documents folder. [Jonathan 2026-10-10]
- **Commits and the token:** commit as DrSaturnn with the noreply email; never print the token; keep a clean tree at the end of every turn. [HO]

## On hold or pending
- **A Cluster A personality disorder brief:** on hold, to revisit later. [MEM]
- **A Step2Haki companion Chrome extension:** started 2026-10-09. [MEM]
- **PSGN latency figure:** an open R1 question. [handoff State]
