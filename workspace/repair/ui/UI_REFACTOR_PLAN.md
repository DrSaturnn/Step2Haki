# UI refactor batch: plan and launch prompt (2026-11-05)

Decisions: DECISIONS_DIGEST D-20261105-1 (architecture), -2 (stale decisions), -3 (motion), -4 (order of work), -6 (no decision narration in code), -7 (added scope and follow-on batches). Draft lines
for the repo are in claude/pending/layout_mock/DIGEST_ADD_2026-11-05.md; the updated STANDING_DIRECTIONS (core rules block
plus "UI architecture" section) is claude/pending/layout_mock/STANDING_DIRECTIONS.md. Both landed in the repo on 2026-11-05 (doc commit after
Jonathan's "ship"), with tools/spine/ui_lint.py, doc_lint.py and ui_baseline.json; step 0 is now only a check that they are
present and doc_lint passes.

**Content is frozen.** No brief text, fact, mask, item or table cell changes. The page must look and behave the same in every
theme, on desktop and phone, before and after; the only visible differences allowed are bugs the refactor fixes, each listed
for Jonathan.

## Launch prompt (paste into a fresh chat)
```
Step2Haki: launch the UI refactor batch per repair/ui/UI_REFACTOR_PLAN.md (project copy claude/pending/layout_mock/) (site layer only, content frozen). Attach DrSaturnn/Step2Haki (push) and DrSaturnn/Step2Haki-private (push) at session start. Read STANDING_DIRECTIONS core rules and DECISIONS_DIGEST D-20261105-1 to -7 first. No agents for the build; one review agent (Opus) for the before-and-after comparison report. Budget: lead 100M. Stop and ask before deleting any rule whose owner the coverage and screenshot evidence cannot settle.
```

## Steps
0. **Land the rules.** Append DIGEST_ADD_2026-11-05.md's five lines to workspace/repair/efficiency/DECISIONS_DIGEST.md; replace
   workspace/repair/efficiency/STANDING_DIRECTIONS.md with the pending copy (check it against the repo copy first: if the repo
   changed after commit 1cc935c, merge rather than replace); add tools/spine/ui_lint.py, tools/spine/doc_lint.py and
   tools/spine/ui_baseline.json from claude/pending/layout_mock/; doc-only commit, pushed by hand.
1. **Baseline evidence (before).** Screenshots of every brief (all 209) at desktop 1512x945 and phone 390x844, in each theme
   (sculpted, flat, dark, each accent the settings offer), in Read and Recall, sidebar open and closed; plus the open states
   that move things: a drawer, a hover card, the phone index, the question bank in Stack, List and Review. Record Chrome
   coverage (used and unused CSS and JS) over a scripted walk through all of these. Run legib_audit. This set is the parity
   target.
2. **Inventory.** For each of the 27 style blocks and 25 script blocks: what it styles or does, which batch and decision made
   it, and which later block overrides it. Output: UI_MAP.md draft with a Retired table (every selector or id whose design
   was replaced, with the decision that retired it).
3. **Stale-decision audit (display and UI topics).** Give the display and UI lines of DECISIONS_DIGEST and STANDING_DIRECTIONS
   ids and topic tags (workup, sidebar, timeline, theme, motion, phone-nav, bank, drawer ...); mark each line already replaced
   "(superseded by ...)" (example: 2026-10-09 s127 headed cards, superseded by the 2026-10-11 5a template). Every marking is
   listed for Jonathan; when two live lines disagree and no later line settles it, ask him. doc_lint must pass.
4. **Restructure** into source files that build back into one index.html (the site stays one page on Vercel):
   - css/tokens.css (colors, fonts, radii, shadows, motion springs: --spr, --bnc, add --snp), css/base.css, css/layout/*.css
     (frame, sidebar, phone, drawer, toolbar), css/components/*.css (table, workup, ladder, pause, timeline, mnemonic, bank,
     hover card), css/themes/*.css (token values only), under `@layer tokens, base, layout, components, themes`;
   - js/<feature>.js modules (sidebar, rail, recall, drawers, hover cards, bank, review, search, shelf, settings), each with
     init and teardown, talking through one small event list;
   - one build step (extend repair/build.py) that concatenates them in order; the ship pipeline is otherwise unchanged.
5. **Delete what was replaced.** Remove overrides whose target design is retired, the specificity workarounds
   (html:is([data-theme],:not([data-theme])) used 214 times) and !important (123) where the layer order makes them
   unnecessary. Move layout out of theme rules (90 today). Convert motion to the spring tokens (57 non-spring today).
5c. **Invisible fixes** (measured on the live page 2026-11-05; screen readers and keyboards only, no visual change):
   name the 209 per-brief buttons that have no accessible name; fix the 2 duplicate ids (rvpin, rvmsg); restore visible
   keyboard focus where 5 rules remove the outline (shown on keyboard focus only, `:focus-visible`, so mouse use is unchanged);
   clear the 2 console warnings or errors at load.
5d. **One settings module.** Every saved reader setting (today ax-bankview, ax-flat, ax-shelf, ax-study) read and written
   through one module with versioned keys and a migration, so a later change cannot silently reset a reader's settings.
5e. **Head tags and headers.** A page description and link-preview tags; a vercel.json with a content security policy,
   no framing by other sites, and caching that lets a new version reach readers promptly after a ship.
5f. **Internal documents to the private repo.** DECISIONS_DIGEST, STANDING_DIRECTIONS, the handoff, RESUME, the runbook,
   OPEN_WORK and repair/ui move to DrSaturnn/Step2Haki-private; the public repo keeps the site, the build and the tools;
   every path that names them (RESUME, runbook, hooks, tools, project copies) is updated in the same batch.
5b. **Strip narration from code.** Remove decision quotes, names, dates, batch ids and workflow terms from every source
   comment (586 comments in the shipped page today: 57 name Jonathan, 111 carry batch ids); keep a short "what this does"
   comment only where the code is not obvious; carry anything worth keeping into UI_MAP.md or the digest. The build step
   strips all comments from the shipped index.html and minifies it.
6. **Parity check (after).** Repeat step 1 exactly; pixel-diff every pair; every difference is either fixed or listed as an
   intended bug fix with its before and after screenshot. legib_audit passes. One review agent reads the diff report, not
   the code, and lists anything that looks like a regression.
6b. **Permanent tests in the gate.** Keep step 1's screenshot comparison as a standing check for every layout and theme;
   add an accessibility scan (axe-core) of a sample of briefs in each theme, failing on any new serious issue; add a
   performance budget (shipped page size, element count at load, load time in a fixed headless run; today 6.5 MB, about
   224,000 elements, 7.7 s from a local file) that fails a ship if any figure gets worse.
7. **Lower the baseline.** ui_lint baseline set to the new counts (expected: comments in the shipped page 0, style blocks per layer file, specificity
   workarounds 0, theme rules setting layout 0, !important near 0, non-spring motion 0); from then on layout in a theme and
   any Retired selector are hard fails. Wire ui_lint and doc_lint into gate.py and ship.sh; doc_lint also into the launch gate.
8. **Report and ship** per BATCH_RUNBOOK (one report: counts before and after, the parity diff summary, the stale-decision
   markings, the bug fixes, decisions needed); Jonathan replies "ship".

## After it ships: follow-on batches, in order (D-20261105-7)
These change behavior, so each is its own batch with its own screenshots and approval.
1. **Load briefs on demand.** Build a brief only when it is opened or scrolled near, instead of all 209 at load; search,
   the sidebar, links to a brief, Recall and Review keep working. Expected to cut load time several-fold (to be measured).
2. **Offline use.** A service worker so the site installs like an app and works without signal on rotations.
3. **Phone redesign** (already planned; claude/pending/MOBILE_NAV_PILOT.md).
4. **Fit to screen** in the layout chat, as a layout module (css/layout/fit.css, js/fit.js), from FIT_TO_SCREEN.md v12 with
   D-20261105-5: two columns, steps not pulled whole to the next screen. Jonathan may reorder 3 and 4.
Not planned: rewriting in a framework, or splitting the site into many pages (on-demand loading gives the speed without
breaking single-page search and Recall).
