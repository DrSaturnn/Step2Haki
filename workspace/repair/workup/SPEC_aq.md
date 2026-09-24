# Aquifer workup brief drafting spec (s27)

You draft ONE Aquifer symptom-workup brief for /home/claude/axbx/index.html (USMLE Step 2 CK / peds shelf). READ-ONLY on index.html; write only your output JSON.

Read first, in full:
1. /root/.claude/skills/synced/6000d04b-e2f3-468a-8f85-28456b38ad2a_0da4c745-3832-44b3-9734-e17c6361b511/aquifer-workup/SKILL.md (the method and skeleton; follow Sections 2 to 6 and 9 exactly).
2. The model brief `aq-bruising` in index.html (div class "brief aq"), end to end. Match its structure, classes (vignette, dp, cluet clue tables with data-mask="none", tw wrappers, tbody.grp for the first test's outcomes, danger grid, pairs, rule, traps) and its voice.
3. Your case source file (condensed Aquifer case summary) in /home/claude/axbx/repair/sources/aq/.
4. The existing briefs named in your task, so you link rather than duplicate.

Constraints:
- Only the case SUMMARY is available (no patient narrative). The source-case vignette block gets data-recon="partial" and describes only the case as the summary implies it (chief complaint, age, the final diagnosis the summary teaches); do not invent specific vitals or labs for the patient. Say so in notes.
- Content from the summary plus standard Step 2 knowledge. ⚠︎ only for memory-sourced numbers or thresholds not in the summary and not standard. Step 2 depth, no specialist detail.
- Voice: plain, senior-resident on rounds; no slogans; findings do not act; no em dashes in prose (the page's structural " &mdash; " label separators inside vignette/danger/crit blocks are allowed); no emojis; American spelling; plain captions (e.g. "Infant with fever: the differential", "First tests", "Finalists").
- Never embed Aquifer images.
- About 1,300 words before the bank.
- Div: <div class="brief aq" id="aq-<slug>" data-shelf="<shelves>" data-src="aquifer" data-case="<Course> <n>">. h4 = the complaint in plain words; p.sub = "Aquifer <Course> <n> &middot; symptom workup &middot; <branches, plainly>".
- Bank: exactly `<h5 class="authored-hdr">Scenario bank</h5>\n<ol class="bank authored">\n</ol>` (empty shell; the assembler fills it). 12 to 18 items per Section 6 coverage. Item object: {"brief","type","stem","key","companion","d1","d2","lead"(or null),"src"("aquifer" for the case item, else "authored"),"nid":null}. Types: next, dx, test, mech, avoid, screen, stage, claim. NBME lead-ins verbatim on test items: "Which of the following is the most appropriate diagnostic study to obtain at this time?" or "Which of the following laboratory studies is most likely to confirm the diagnosis?". Stems describe, do not name. Keys same category as distractors; answer-cue review (key not uniquely longest by more than about 4 characters). No duplicates of items in owning briefs (check their banks).
- Pairs with: verified existing h4 titles only (grep the page); include "reverse_links": [{"brief":id,"anchor":"<exact text occurring once in that brief, at the end of its Pairs with block before </div>>","sentence":"..."}] for 1 to 3 owning briefs.

Output JSON (a list with one object): {"kind":"new","id":"aq-<slug>","system":"<h3 system id>","shelf":"...","nav_label":"...","html":"<full div>","items":[...],"reverse_links":[...],"notes":"source contradictions, deviations, flags, narrative missing"}.
Validate: JSON parses; html has balanced <div>; the bank shell occurs once. Final reply: short summary, item count, notes.
