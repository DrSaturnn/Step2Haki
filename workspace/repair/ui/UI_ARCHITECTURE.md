# UI architecture rules and how they are enforced (draft, 2026-11-05)

Status: approved 2026-11-05 (D-20261105-1 to -3); in the repo 2026-11-05 (doc commit). Nothing here is in DECISIONS_DIGEST, the runbook or the repo yet. On approval, section 1
goes into DECISIONS_DIGEST (his words) and STANDING_DIRECTIONS (Display), section 3 into tools/, and the refactor in section 4
becomes a batch.

Jonathan, 2026-11-05: "all legacy layout content removed ... in the context of items that were replaced or decided to be
retired"; "the coding should be modular in design"; "themes would exist isolated to layout design"; "sounds like we need to
add this to the .md and whatever .py scripts beforehand for plausible future ui changes"; "the .md/decisions digest should be
hardened to ensure they are always followed ... due to agents or new chats skipping reading a section".

## 1. The rules
1. **Replace, never append.** A UI change edits or deletes the rule it replaces in the same commit. No new override block
   per batch. A retired design's code is deleted, not outvoted; git history keeps it.
2. **Three layers, one job each**, in this order, declared with CSS `@layer tokens, base, layout, components, themes;`
   - tokens: every color, font, radius and shadow as a named value;
   - layout: page frame, sidebar, columns, Fit to screen, phone layout; no colors;
   - components: table, workup, ladder, pause point, timeline, question card; no page positioning;
   - themes: redefine token values only. A theme rule never sets size, position, spacing, display or zoom.
3. **One module per feature in script**, each with an on/off entry point; a feature never reaches into another feature's
   elements (the sidebar, Recall, Fit, hover cards and the bank talk through a small shared event list).
4. **A module map**, `UI_MAP.md`: every layout, component and script module, what it owns, which decision created it, and
   what it replaced. A retired item moves to a Retired table with the selectors and ids it used.
6. **Code holds code** (D-20261105-6): comments in source only explain what non-obvious code does; no decision quotes,
   names, dates, batch ids or workflow terms; the build strips every comment from the shipped page.
5. **Desktop-only and phone-only code** sit under one named breakpoint each, so a desktop feature cannot change phones.

## 2. Hardening the docs
Docs alone cannot guarantee compliance: a chat that skips a section still ships. So:
1. **Checks, not reading.** Every rule above that can be measured becomes a check in the gate (section 3). A rule that
   cannot be measured is marked "manual" and listed in the runbook S2 checklist, which the batch report must answer item by item.
2. **Core rules on top.** STANDING_DIRECTIONS and RESUME open with a 10-line core block (the rules a UI change must not
   break), above everything else, since the top of a file is what a skimming reader sees.
3. **IDs and supersession.** Each digest decision gets an id; a later decision names the id it replaces, and the replaced
   entry is marked "superseded by" in place, so an old line is never read as current.
4. **Retired means checked.** The Retired table's selectors and ids are grepped by the gate; finding one in the page fails it.
5. **Launch proof of reading** (option, needs Jonathan's call): the batch file records the commit hash of STANDING_DIRECTIONS
   and the digest the lead read; the launch gate refuses a batch whose recorded hash is older than the current files.

## 3. ui_lint.py (tools/spine/ui_lint.py; run by gate.py as ui-lint and ui-site, baseline lowered by ship.sh since s165b)
Ratchet: records today's counts and fails any build that makes one worse; a refactor lowers the baseline.
Live page today (commit 1cc935c), measured:
| Count | Now | Rule it guards |
|---|---|---|
| Style blocks | 27 (s116 to s159 layered) | 1 |
| Script blocks | 25 | 3 |
| `!important` | 123 | 1, 2 |
| `html:is([data-theme],:not([data-theme]))` specificity workaround | 214 | 1 |
| Theme-scoped rules that set layout | 90 | 2 |
| Selectors defined 4 or more times | 29 | 1 |
To add once the layers exist: no theme rule may set a layout property (hard fail, not ratchet); retired selectors absent;
screenshots of every layout in every theme (legib_audit and shots.py extended).
Test: the Fit to screen mockup, built as a patch on top of the page, fails the ratchet (style and script blocks +1,
`!important` 123 to 255), which is the behavior wanted: Fit must be built into the layers, not added on top.

## 4. Refactor batch (proposal, no content changes)
1. Split the page's CSS into the five layers and its scripts into feature modules; build them back into one index.html.
2. Delete the overrides each later block replaced; keep only what current designs use (Chrome coverage plus screenshots of
   all briefs in all themes, before and after, must match).
3. Write UI_MAP.md and the Retired table; lower the ui_lint baseline.
4. Then build Fit to screen as a layout module (FIT_TO_SCREEN.md v12 as the spec).
