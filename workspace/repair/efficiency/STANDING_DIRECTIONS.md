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
- Word caps above the practice bank: disease about 1,300, drug about 1,000, presentation hub about 700. [DIG 2026-10-10]
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
- **Acronyms:** every acronym is written out at first use or in a hover. [SPEC r4]
- **Row drawers:** a differential row whose diagnosis owns a brief is a drawer button. [SPEC migration rule]

## Display
- **Diagnostic workup template: layout 5a (2026-10-11).**
  - Each clue and its order sit on one tinted band row: clue, then an arrow, then the order.
  - Below the band, untinted and smaller, each finding branches from a stem and leads to its meaning by a connector and arrowhead.
  - Zones: First step, By clue, Next step, Most accurate or Confirms, then Skip.
  - Spec and design file: claude/design/WORKUP_5A_SPEC.md and claude/design/Workup_5a.html.
  - This supersedes the s127 headed cards, the 2026-10-10 R1 rail removal and the "vertical line with dots"; the s130 numbered and forked layout stays rejected.
  - The build questions in the spec are open until Jonathan answers them. [DIG 2026-10-11]
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
