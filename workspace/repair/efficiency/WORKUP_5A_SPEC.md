# Diagnostic workup template: layout 5a (adopted 2026-10-11)

Jonathan, 2026-10-11: "okay here is the new diagnostic work up design template". Made in Claude Design, starting from the Step2Haki design system and the hematuria test case. The design file is `claude/design/Workup_5a.html`: a bundled page that renders the 900 px brief width, a 390 px phone, and this spec.

## Layout

- One tile per zone: First step, By clue, Next step, Most accurate (or Confirms, a tweak), then a plain Skip line.
- **Band row (tinted):** clue, then an accent arrow, then the order. On desktop the columns are 200 px, 24 px and the rest; on a phone, 112 px, 20 px and the rest. The order is 17 px (16) at weight 750; several orders stack one per line.
- **Findings rows (untinted, below the band):**
  - a 1.5 px violet stem hangs from the band;
  - an 8 px tick leads to each finding (13 px, `muted`);
  - a connector line and arrowhead lead to its meaning (13.5 px, `ink-2`, bold lead term);
  - the finding column is 75% of the clue column;
  - meanings are capped at 360 px on desktop.
- **Study mode:** "Hide meaning" blurs meanings by 5 px; "Hide test and meaning" also blurs the orders.

## Designer's spec (from the file)

The values are for the 900 px brief width; phone values are in parentheses.

**Structure**
- **Tile:** one tile per zone (first step, by clue, confirm). Each clue is a band row (clue, arrow, order), followed by its findings rows (finding, arrow, meaning).
- **Band row grid:** clue column 200 px, arrow column 24 px, the order takes the rest (112 px, 20 px, rest). The clue column width is the one control; the rest derive from it.
- **Findings grid:** its own grid, tighter than the band. The finding column is 75% of the clue column (150 px), the arrow column 22 px, and the meaning takes the rest (85%: 95 px, 20 px, rest). Every arrowhead lands on one vertical.
- **Wrapping:** clues, findings and meanings wrap; nothing truncates. Meanings cap at 360 px (no cap on a phone). Findings hyphenate and break long words (hyphens auto, overflow-wrap anywhere).

**Color**
- **Band tint:** `--recess` #E4E6E6 behind the clue row; #DEDEEB in the first-step tile.
- **Tile surface:** `--raised` #EFF0F0, with findings rows untinted on it. The first-step tile uses `--grad-first`.
- **Clue:** `--chart-ink` #2B2F36. Placeholder clues use `--faint` #9C9CAA.
- **Order:** `--ink` #15151B.
- **Finding:** `--muted` #5E5E6B.
- **Meaning:** `--ink-2` #33333E, with a bold lead term.
- **Line work:** rgba(84,74,196,.42) for the stem, ticks and connectors; arrowheads at .70 alpha.
- **Band arrow:** `--accent` #544AC4.
- **Row rules:** `--hair` rgba(24,28,30,.09), inset 1 px above and below each band; rgba(84,74,196,.28) in the first-step tile.

**Type** (the system UI stack, no web font)
- **Zone label:** 11 px, weight 800, uppercase, tracking .09em, `--muted`.
- **Clue:** 15.5 px (14.5), weight 750, line height 1.3, text-wrap pretty. Draft clues get a dotted `--muted` underline, offset 3 px.
- **Order:** 17 px (16), weight 750, line height 1.3, tracking -.005em.
- **Band arrow:** U+2192, 17 px, weight 700, centered in its column.
- **Finding:** 13 px (12.5), weight 500, line height 1.4.
- **Meaning:** 13.5 px, weight 400 with a 700 lead term, line height 1.42, text-wrap pretty.

**Spacing**
- **Tile:** radius 14 px, overflow hidden, shadow `--e2` plus an inset 1 px hairline (1.5 px violet in the first-step tile). Zone label: 20 px above, 8 px below.
- **Band row:** padding 10 px 14 px; 4 px between the clue and the arrow column.
- **Findings row:** left padding 28 px for the tree, right 6 px. Top 10 px on the first finding, 6 px after; bottom 4 px, 11 px on the last. The meaning uses the same top and bottom padding, so both start on one line.

**Line work**
- **Stem:** 1.5 px vertical at x = 16 px. It starts at the bottom edge of the band, so it hangs from the clue row, and stops at the last tick.
- **Tick:** 8 px horizontal from the stem toward the finding, at the center of the first line (row top padding plus 9.5 px).
- **Connector:** starts 6 px after the end of the finding's first line (measured in script) and runs through the arrow column to the arrowhead. Same weight and color as the stem.
- **Arrowhead:** a 7 x 7 px box with 1.5 px top and right borders, rotated 45 degrees, stopping 6 px short of the meaning column. Hidden when a finding has no meaning.

**Behavior**
- **Study mode:** "Hide meaning" blurs meanings by 5 px; "Hide test and meaning" also blurs the orders. Transition .22 s.
- **Flat theme:** `data-theme` flat on the root turns `--e1` and `--e2` into hairline outlines, and gradients go flat.

## Decided by Jonathan (2026-10-11, answering the build notes)

1. **Phone finding column:** "on mobile only, this column for this can be pushed slightly for less word wrapping."
   - Widen the phone finding column a little, from 112 px toward about 130 px; set the exact value at the pilot screenshot.
   - Desktop is unchanged.
2. **Desktop meaning cap:** kept. "No, this helps with visual grouping and easier scanability."
   - The 150 px finding column and the 360 px meaning cap stay as designed.
3. **The last zone's label** is "Diagnostic test" ("both wrong, Diagnostic test is what step 2 usually uses"). This replaces both "Most accurate" and "Confirms".
   - "Both wrong" referred only to the two labels (Jonathan: "it was a joke"). The tests in this zone stay as designed.
4. **"By clue" is renamed.** Jonathan delegated the new name.
   - Claude's pick: "By presentation". It is plain, matches the clue column and pairs with "First step" and "Next step". Jonathan can swap it.
5. **"CT" may stay shortened** ("shortened to CT is fine"). "Contrast CT abdomen" is accepted as the design wrote it.

Zones are now: First step, By presentation, Next step, Diagnostic test, then Skip.

## Still open (build, not design)

- **Draft markers.** Dotted underlines and "[indication]" are authoring marks and never ship. Every indication needs a source. The meatus exam has none, and "Renal injury" has no meaning.
- **Connector lines.** They are measured in script, so a live build must handle resize, study mode and drawers.
- **Theme hooks.** The flat theme maps to the site's `body.flat` and `.axm-flat`; study mode maps to the site's `.mask` spans. The build must pass legib_audit in sculpted, flat and study modes.
