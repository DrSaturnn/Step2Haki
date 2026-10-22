# Step2Haki: instructions for Codex

Step2Haki is a Step 2 CK study page (workspace/index.html, deployed from discriminator-briefs-site/ by Vercel). Its
briefs are built in batches by a lead agent under a runbook. Since 2026-10-21 Codex (GPT-6.1 Sol) may lead batches in
the interim while Claude's usage is limited (DECISIONS_DIGEST 2026-10-21).

Before anything else, read in this order:
1. workspace/repair/efficiency/STEP2HAKI_HANDOFF.md, the State section (current batch, step, spend, Lead line);
2. workspace/repair/efficiency/CODEX_LEAD.md (what differs when Codex leads: the lock, doc locations, hooks, reviews,
   cost, shipping, and the authoring failure modes to avoid);
3. workspace/repair/efficiency/BATCH_RUNBOOK.md (the process; its read list, with the paths mapped by CODEX_LEAD.md
   section 1).

Restart line (Jonathan pastes it to continue an open batch):
`Step2Haki: continue the current batch per claude/BATCH_RUNBOOK.md.`
For Codex it means: take the lock per CODEX_LEAD.md section 0, then follow the runbook from the State's step.
A launch prompt (a new batch id) means: CODEX_LEAD.md section 2 item 4 (create wip/sNN in both repos), then section 2a
(which build to copy) and section 7 (failure modes, read before S1).

Hard rules, always:
- Accuracy over speed. Every fact comes from a board source (NBME, UWorld, AnKing) or a primary source fetched that day
  with tools/spine/fetch.py, with a verbatim quote. Teach the Step 2 answer.
- No vendor text (UWorld, NBME, AnKing wording) in this public repo. The private repo DrSaturnn/Step2Haki-private holds
  the sources and must never be copied into this one.
- No emojis, no em dashes. Commit as DrSaturnn with the noreply email. Never print a token.
- Never change ship.sh, the gate, approval.py or any check to make work pass. Codex does not ship (CODEX_LEAD.md
  section 5).
- Stop and ask Jonathan only for the reasons in the runbook's section 6.
