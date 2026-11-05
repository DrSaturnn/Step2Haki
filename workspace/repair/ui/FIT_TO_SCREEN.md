# Fit to screen (desktop brief layout): mockup record

Status: mockup only, nothing shipped, no batch. Artifact "Step2Haki Layout Mockup" (v4, 2026-11-05) shows the
3-column grid read across rows, with a mockup-only switch to compare reading down columns, and the shelf-section rail. Generators in this folder, each run on the live index.html:
- make_rows.py: v4 (current artifact): across rows or down columns, equal 36 px gaps between steps, rail of shelf sections.
- make_cols.py: v3, 3 scaled columns read down, rail of the brief's steps.
- make_sheet.py: the paged version (steps restyled and flowed through screen-sized pages). Screenshots attached to the chat.
- make_fit.py: v2, summary tiles with open-one-closes-others (set aside: Jonathan wants the fit solved before open/close).
- make_mock.py: v1, Scroll / Columns / Pages / Spreads (superseded).

## Jonathan's direction (2026-11-05, his words)
- "I want to create a additional way or layout for a whole brief to be displayed on a single screen ... only be accessible
  from the desktop and not mobile, so mobile should not be affected."
- "it would involve resizing and removing much of the negative space, it should be able to be applied to all briefs as well"
- "in general, they should all be viewable. And then when ... the content exceeds a certain threshold, then that's when they
  would be collapsed. And opening one step would close others. Rather than making too many different modes."
- On v2: "theres still much better ways to display the full fitted steps, bringing up the title higher up, connecting steps
  in one larger tile, tighter spacing, i want to literally attempt to fit the whole brief in one or two pages. this should be
  done before we decide how we want to open or close specific brief sections. in the case we need to open sections, they
  should open within the same format rather than reverting back to the scrolling format."
- "consider having the side bar become collapsible like google chromes new vertical tab feature. Consider if the we can more
  simply have a 3 column version that is more simply a scaled down version of the current scolling website, along 3 columns
  that can still scroll to any remaining steps or simply the Questions."
- "the text size changer can be omitted for this setting given it is already a compact space"

## v3 (3 columns) does
- Fit on (desktop, 1101 px and wider): sidebar collapses to a 56 px rail: expand, search, then the brief's steps as numbered
  buttons with their names on hover; steps on screen are marked. Expand opens the full sidebar over the page with a collapse
  button beside settings; a click outside or Escape closes it; picking a brief closes it.
- Title beside the toolbar; the toolbar's step label is hidden (the rail shows what is on screen).
- Steps keep their current look, scaled so three columns of 520 CSS px fit (0.77 on a 1512 px window, 1.0 at 1920), split in
  reading order so the columns end as evenly as possible; the page scrolls; practice questions full width below.
- No text size control. Phones unchanged (checked with Fit saved on).

## Measurements (headless Chromium, live page 2026-11-05; screens = height of steps 1 to 8 over window height)
| Brief | Scroll today, 1512x945 | v3 3 columns, 1512x945 | v3, 1920x1080 | Paged, 1512x945 (sidebar hidden) | Paged, 1920x1080 |
|---|---|---|---|---|---|
| Heart Failure | 6.7 | 2.2 | 2.5 | 2 pages, 94% text | 1 page, 82% |
| Polymyalgia Rheumatica | about 8 | 2.9 | 3.2 | 2 pages, 82% | 2 pages, 100% |
| Kawasaki Disease | about 8.5 | 3.5 | 3.9 | 2 pages, 76% | 2 pages, 100% |
| Lithium Therapy | about 8.3 | 3.6 | 4.0 | 2 pages, 76% | 2 pages, 88% |
| Psychosis | about 11 | 5.4 | 6.0 | 3 pages, 76% | 2 pages, 76% |
Today's figures other than Heart Failure are scaled from the step heights measured earlier the same day (estimates).
At 1920 v3 does not scale (1.0), so it runs longer than on the laptop.

## Trade-offs found
- v3 is simple: it moves whole steps into columns and scales them; no component is restyled, nothing is split, so it is the
  cheapest to keep working as briefs change. Costs: 2 to 5 screens on a laptop; one long step (a Workup) makes its column
  much taller than the others; reading order runs down column 1, then 2, then 3.
- Paged is the only version that reaches one or two pages for most briefs, but it restyles every component (flattened
  cards, stacked 3-column tables, stacked workup, vertical milestone strip, title lift) and splits steps across columns with
  "continued" labels; each component needs a narrow-column rule and a check, and auto text size went down to 76%.
- A middle path, not built: v3 plus only the safe parts of paged (flattened inner cards, tighter gaps, smaller step headings)
  and 4 columns at 1800 px and wider. Gain not measured.

## v4 (2026-11-05) Jonathan: "is it able to read left to right at all? my concern is that it does almost look more
overwhelming and like a block of text in this version. also, steps would need to be equidistant from one another."
"for the side rail, when collapsed, i dont think the steps should be in the collapsed rail, how can we display the shelf topics?"
- Rail: shelf sections as short labels (Pres, MSK, Peds, CV ... Psych, Pharm), full name and count on hover; a click opens a
  panel of that section's briefs with its sub-headers; the current brief's home section is marked. No steps in the rail.
- Steps are separated by one equal gap (36 px before scaling) in both reading directions.
- Measured, 1512x945, steps 1 to 8 (screens; share of the grid left empty):
  | Brief | Across rows | Rows, tall steps span 2 columns | Rows, tall steps capped at about 1.15x the median | Down columns |
  |---|---|---|---|---|
  | Heart Failure | 3.84; 53% | 3.37; 29% | 2.25 (3 capped) | 2.2 |
  | Psychosis | 5.91; 40% | 6.05; 34% | 4.35 (3 capped) | 5.4 |
  | Lithium Therapy | 3.96; 35% | 3.96; 35% | 3.83 (2 capped) | 3.6 |
  | Polymyalgia Rheumatica | 4.17; 46% | 4.22; 36% | 2.40 (3 capped) | 2.9 |
  | Kawasaki Disease | 4.26; 44% | 3.44; 22% | 2.69 (3 capped) | 3.5 |
  Reading across costs 35 to 53% empty space because one step (usually Workup) is 2 to 4 times the others and sets its row.

## v5 (2026-11-05) Jonathan: "this size looks more appropriate at 80% chrome zoom"; on the workup in a column, "how we can
better close the negative space here"; "inner cards should expand too"
- Fit sets the whole page (toolbar, rail, title, steps) to the size Chrome shows at 80% zoom (body zoom 0.8); the steps then
  need almost no extra scaling (0.99 on a 1512 px window).
- Workup in a column: each test is one card the full width of the workup: clue and test on top, then each result beside
  what it means (arrow, accent), so no blank space under the test name; tests without results are a single rounded card.
  Checked in light and dark. Screens are about the same as v4 (same content scale); the gain is the empty space inside Workup.

## v6 (2026-11-05) Jonathan: "fit multiple steps in one column where able ... steps going vertically, then, where it reaches
the end of the page, continuing into the next column, that way vertical scrolling only has to happen once they have read all
the steps visible on the first page"
- Default arrangement "Down, screen by screen": each page is one screen tall with 3 columns; steps run down column 1, then 2,
  then 3, then the next screen (a rule between screens, scroll snaps to each screen). Cards move whole unless taller than
  0.6 of a column; those break between rows with rounded edges on both parts; a step that continues gets "Name, continued".
- Pages for steps 1 to 8 (last page partly filled):
  | Brief | 1512x945 | 1920x1080 |
  |---|---|---|
  | Heart Failure | 3 (last 333 px) | 2 |
  | Polymyalgia Rheumatica | 3 | 3 (last 290 px) |
  | Kawasaki Disease | 4 (last 547 px) | 3 |
  | Lithium Therapy | 4 (last 324 px) | 3 (last 455 px) |
  | Psychosis | 5 | 4 |
- Tested and not kept: smaller step headings and gaps (no page saved); letting more cards break (saves under a fifth of a
  page). The size of the content, not spacing, sets the page count at the 80% size.

## v7 (2026-11-05) Jonathan: "Both are just off. The vertical step pattern fitted best, but was more difficult to read.
Evaluate the absolute best way to meet the current goal of making a brief readable and flow with scrolling being done only
after all the content in the page was read." and "the side bar and top navigator should be increased back up slightly while
the main page is maintained at the current percentage zoom"
- Recommendation built: screen pages of WHOLE steps. A step never splits unless it is taller than a whole column (then it
  breaks between its cards with "continued"). Columns: 2 unless each of 3 columns can stay at least 620 CSS px wide (so 2 on
  a 14-inch MacBook, 3 at 1920). Mockup switch: Auto / 2 / 3.
- Brief at 80%; toolbar, sidebar, rail and section panel at 90%.
- Screens for steps 1 to 8 (share of each screen filled):
  | Brief | MacBook, 2 cols | 1920, 3 cols |
  |---|---|---|
  | Heart Failure | 4 (77%) | 3 (68%) |
  | Polymyalgia Rheumatica | 5 (72%) | 3 (75%) |
  | Kawasaki Disease | 5 (76%) | 3 (77%) |
  | Lithium Therapy | 5 (85%) | 3 (77%) |
  | Psychosis | 7 (79%) | 4 (88%) |
- Trade: more screens than v6 (3 to 5 on the laptop), in exchange for whole steps, table widths close to today's, and an
  open-book reading order (left column, then right, then scroll).

## v8 (2026-11-05) Jonathan: "still way too much negative spacing. How do we resolve that? additionally, the scenario bank
and next/back are too wide apart"; "the side bar should be able to be left open and simply pushes the layout out for people
that want to leave it open as they read"
- Empty space came from large cards (Workup, Differential and clue tables, ladders) that had to move whole, leaving the rest
  of a column blank. Now a card taller than about a third of a column continues in the next column between its rows (never
  mid-row), with "Name, continued" and the table header repeated; small cards still move whole; workup zone headings stay
  with their first test.
- The practice questions flow as the last block at column width (Back and Next about 690 px apart on the MacBook, was the
  full page); the question card itself never splits.
- Sidebar: a "Keep sidebar open" button beside the collapse button pins the full sidebar; the brief moves over and re-lays
  out; a click outside no longer closes it; the collapse button unpins. Remembered per browser.
- Share of each screen filled, with questions included (was 72 to 85% in v7):
  | Brief | MacBook, 2 cols | 1920, 3 cols |
  |---|---|---|
  | Heart Failure | 4 screens, 80% | 3, 86% |
  | Polymyalgia Rheumatica | 5, 85% | 3, 88% |
  | Kawasaki Disease | 5, 88% | 3, 91% |
  | Lithium Therapy | 5, 92% | 3, 83% |
  | Psychosis | 7, 90% | 4, 90% |
  The remaining gap is mostly the end of the last screen.

## v9 (2026-11-05) Jonathan: on a step that ends one screen in the right column and continues in the left column of the
next ("my only concern is how the differential reads in the right column then flows in the left column"); "the steps font
size can be decreased, and further tightened overall"; "the transferable rule would be aligned to the tile rather than the top"
- A step that would begin in the last column of a screen and carry over starts the next screen whole instead (unless it is
  taller than about a screen). Steps that begin in an earlier column can still continue onto the next screen.
- Step headings 30 px to 20 px with a 26 px badge; gaps between steps 22 px; card, table-row, ladder and workup padding
  tightened; workup zone numbers keep counting across a continued workup.
- Table captions and headers stay with their first row. The questions can start in a column under the last step; the
  closing "End of" line sits under the pages, not in a column.
- When the transferable rule starts the column beside the question card, it lines up with the card's top (a spacer, since
  margins at a column top are dropped); it is skipped if it would push content to another screen.
- Screens with questions included: MacBook (2 cols) Heart Failure 3 (86% filled), Polymyalgia Rheumatica 4 (82%), Kawasaki
  4 (93%), Lithium 5 (89%), Psychosis 6 (83%); 1920 (3 cols) 2, 3, 3, 3, 4.

## v10 (2026-11-05) Jonathan: "it works well for 3 columns, for 2 columns it still introduces the negative space"; "should
expanding the side bar action push the content out with the side by side button being the overlay?"; "the work ups steps
should be better aligned ... the distance between step 2 is closer to the prior step than its own step"; "the page break
could simply be under the step rather than giving way to excess negative space"
- Auto picks 3 columns whenever each column can stay at least 420 CSS px wide: 3 on the 14-inch MacBook and at 1920; 2 only
  on narrower windows (including the MacBook with the sidebar open).
- A step starting in the last column moves whole to the next screen only when that leaves under a quarter of the column empty.
- Each screen ends right under its longest column instead of at the bottom of the window (the next screen starts there).
- Sidebar, Chrome model: the rail's Expand button opens the full sidebar and pushes the brief over (stays until collapsed);
  the rail's section labels and search open over the page; the separate keep-open button is removed.
- Workup zones: 19 px above a zone heading, 5 px below it (was the reverse).
- Measured (pages; height in screens; share filled):
  | Brief | MacBook, 3 cols | MacBook, sidebar open (2 cols) | 1920, 3 cols |
  |---|---|---|---|
  | Heart Failure | 3; 2.3; 79% | 4; 3.1; 84% | 2; 1.5; 92% |
  | Polymyalgia Rheumatica | 3; 2.5; 92% | 4; 3.4; 90% | 3; 1.9; 92% |
  | Kawasaki Disease | 4; 3.1; 91% | 5; 3.7; 94% | 3; 2.2; 88% |
  | Lithium Therapy | 4; 3.3; 84% | 5; 4.1; 91% | 3; 2.3; 89% |
  | Psychosis | 5; 4.2; 90% | 6; 5.2; 94% | 4; 3.2; 86% |

## v11 (2026-11-05) Jonathan: "are you suggesting there is no way to meet all our requirements/expectations? ... the workup
starts on the right side, then begins on the left side ... since this isnt a book, an intermediate between two pages is
visible ... Do your research about how to best display this type of website before attempting again"; sidebar: "closing it
works - tiles expand, but reopening it does not push the tiles at all"
- Sidebar fix: the push width was measured while the sidebar was still sliding in; it now uses the sidebar's resting width and
  re-lays out after the slide and on every layout. Checked: open, collapse, reopen all push the brief clear of the sidebar.
- Research: the CSS multi-column spec's author says columns taller than the screen force scrolling down one column and back
  up to the next, and prefers horizontal flow or "column flipping" (w3.org/Style/CSS/multi-column2.html); the W3C
  accessibility review of multicol names the same problem (public-apa 2021-04); Braganza et al. WWW 2009 found readers of
  multi-column text page screen by screen, and multi-column read no slower, but columns taller than a screen force back-and-
  forth scrolling; one participant asked for page boundaries.
- Tested "no step across a screen break" (NOCROSS, built, off by default): fill on the MacBook, 3 columns: Heart Failure 71%,
  Lithium 67%, Kawasaki 76%, Psychosis 75% (its Workup is longer than a whole screen and still crosses); Heart Failure's first
  screen leaves column 3 nearly empty. Conclusion: with steps of very different lengths, a scrolling page cannot have all of
  multi-column flow, no empty space, and no step read across a screen break.
- Recommended next (not built): fixed screen-height pages that flip (keys, a Next control, one wheel gesture per page)
  instead of scrolling, so the half-way state between two pages is never shown; steps may then continue from the last
  column to the next page like a book.

## v12 (2026-11-05) Jonathan asked which iteration is best "as though you were a user"; answer: v11 with whole steps per
screen (empty column space costs a reader little; a step read across a screen break costs the most). He said "yes and with the
other changes mentioned".
- Whole steps per screen on (NOCROSS): a step may run between columns of one screen but starts the next screen whole when it
  would cross a break, unless it is longer than a whole screen.
- 3 columns down to 340 CSS px per column, so the MacBook keeps 3 with the sidebar open; one text size everywhere (the
  sidebar narrows columns, it no longer shrinks text, which had made the sidebar-open view shorter than the closed one).
- Retired keep-open button code removed from the mockup generator.
- MacBook, sidebar closed (screens tall): Heart Failure 2.5, Polymyalgia Rheumatica 2.6, Kawasaki 3.5, Lithium 4.2,
  Psychosis 5.1 (its Workup, over 4,000 CSS px, crosses). Sidebar open: 2.6, 4.1, 4.4, 4.2, 5.1; at that width Psychosis's
  Diagnostic criteria and Differential are each longer than a screen and cross too. 1920: 1.5, 2.3, 2.3, 2.7, 3.5, none cross.

## Next round (D-20261105-5, Jonathan 2026-11-05 16:50)
"we should currently only work on making the fit to screen - two columns at this time and without the stickies pulling to
the next page". Next round: two columns; NOCROSS off (a step is not pulled whole to the next screen; it continues with a
"continued" label). Resumes in the layout chat after the UI refactor batch ships (D-20261105-4), built as a layout module
under the new rules (spring motion, no theme layout, no override blocks).

## Open before any batch
- Which version (v3, paged, or the middle path); whether the rail also replaces the sidebar outside Fit.
- Sidebar step marker and toolbar label read page scroll in the live code; the mockups drive their own marks.
- legib_audit and screenshots would need a Fit pass.
