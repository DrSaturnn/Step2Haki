# Efficiency pilot: frozen rubric (written before any run, 2026-09-24)

Question: does a trimmed worker packet (efficient-review) cut tokens per accepted backfill without losing quality, versus the current full-read spec?

## Design
- Baseline page: commit 7714aba (before s26), worktree /home/claude/bench/base. Read-only.
- Tasks (one brief each, from repair/sources/s26_questions.md):
  T1 Q2 biliary atresia -> neonatal-jaundice; T2 Q4 isotretinoin IIH -> peds-headache-imaging;
  T3 Q5 tuberous sclerosis -> tumor-syndromes; T4 Q6 CVID long-term IVIG -> ig-panel.
- Arm C (control): current workflow: SPEC_s19-style prompt, agent reads skill files, spec, source and brief itself.
- Arm P (packet): one generated packet per task (condensed rules + source excerpt + brief HTML + existing bank) and a verifier script. Agent is told not to open skill files or the full page.
- Same model (inherited), same output contract (Task A backfill JSON), same per-task instructions text for content.
- One run per arm per task (pilot, n=4 pairs). Expected outcomes are not given to workers.

## Metrics
- Efficiency: subagent_tokens, tool_uses, duration_ms per task, as reported by the Agent tool. Primary: tokens per ACCEPTED task.
- Setup cost (packet build) reported separately; reviewer cost is evaluation cost, not production cost.

## Acceptance (a task output is accepted only if all pass)
Mechanical (verify_edits.py against the baseline page):
1. JSON parses; list of backfill objects with edits and items.
2. Every anchor/old occurs exactly once in its brief span; edits apply cleanly in order.
3. Items: valid type; 3 distinct non-empty options; source item present with src uworld, correct nids, correct key concept; 2 to 4 new items for the brief.
4. No em dash character in new prose; no emoji; no <li> inside edits.
5. After applying to a copy of the baseline, gate passes (ids unique, answerable) and no new near-duplicate item.
Judgment (blinded reviewer, per task checklist; each point present and correct = 1):
- T1: direct bili high + GGT high + retics normal pattern; acholic stools/2-8 weeks; small or absent gallbladder or triangular cord; intraoperative cholangiogram (or biopsy) confirms; Kasai (eventual transplant); distractor map (PFIC normal GGT, HLH, hemolysis, breast milk indirect).
- T2: drug list (retinoids/vitamin A, tetracyclines, growth hormone); bilateral papilledema with full fields vs chiasm lesion; MRI with MR venography before LP; LP opening pressure over 250 with normal CSF; stop the drug (weight loss, acetazolamide); optic neuritis painful, usually unilateral.
- T3: periungual fibroma; calcified subependymal nodules on CT; epilepsy/first seizure any age; cardiac rhabdomyoma or renal angiomyolipoma; surveillance; splits vs NF1, VHL, ataxia-telangiectasia, endocarditis.
- T4: IVIG for CVID long term; SCID HSCT; DiGeorge thymus transplant; CGD interferon gamma (+ prophylaxis); cellular defects antiviral/antifungal prophylaxis; CVID features not duplicated.
- Plus 3 quality points per task: Step 2 scope (no specialist detail); factual accuracy (no wrong claim); voice (plain, no slogans).
- Accept if checklist >= 5/6 (T1-T4 have 6 points each) and all 3 quality points pass, and no factual error.

## Decision rule
Adopt arm P as the default drafting workflow only if (a) its acceptance count >= arm C's, (b) no critical defect appears in P that C avoided, and (c) mean tokens per accepted task drops by 25% or more. Otherwise keep C and record why.
