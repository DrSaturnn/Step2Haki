# s136 display review: what to judge

Batch s136 is the site layout Phase 1 (claude/pending/S136.md): CSS and a small page script for all briefs. **No brief
text changed.** You judge only how the page looks and behaves, on the screenshots in your lane, against the rules
below. Do not judge clinical content or wording.

## What Phase 1 must deliver (S136.md scope, Jonathan 2026-10-13 and 14)
1. **Accent setting.** A reader setting beside the theme switches (sidebar: "ACCENT", 8 swatches, the current name).
   Default Slate #3B5B8C; Indigo, Purple (the original), Navy, Ocean, Plum, Rose, Graphite. The accent colors the
   rail fill, the current step's outline and number, workup structure (labels, arrows, connectors), workup meaning
   words and the workup section's glow. It must NOT change confirm green, caution brown, principle indigo (hover
   chips, drawer links) or criteria teal. Ocean beside criteria teal and Rose beside caution brown must stay
   distinguishable.
2. **One job per color.** Workup meanings are colored words in the accent (no dots); step captions are grey; workup
   step numbers are neutral raised discs, never dark filled discs. No brown "act now" meanings in Phase 1.
3. **Alternating row tint** on wide tables (differential, clue, manage, monitoring, interactions, NBME competing
   answers, the systems panel): a faint recessed band with rounded ends replaces row rules. The 5a workup is tinted
   by test group; its clue band keeps its own darker tint.
4. **Secondary text** is the muted grey #5E5E6B; the faint grey is never used for text.
5. **Glass.** A floating glass toolbar (desktop) shows the current section's number and name and holds Read and
   Study and an Expand all control; hover cards and drawers are glass panels; a soft blur under the toolbar at the
   top edge.
6. **Hovers** (desktop): open on pointer enter, close on leave, stay open when clicked. Touch is unchanged.
7. **Sidebar:** light glass (not the old dark sidebar) with a visible edge; the selected brief is a white pill;
   systems fold and unfold. The desktop section rail keeps its fill ending at the highlighted step, now in the accent.

Out of scope (Phase 2, do not report as missing): workup tables, timelines, vertical mnemonics in the renderer,
"Next best step" wording, numbered workup zones, MCQ restyle beyond colors, phone layout changes beyond what the CSS
carries (but do report anything on phone that Phase 1 broke).

## Standing display rules that apply (claude/STANDING_DIRECTIONS.md, Display)
- Every surface passes the legibility audit in sculpted, flat and study modes (the lead ran it: 0 failures for every
  accent; you judge what the audit cannot: crowding, alignment, hierarchy, things that look broken).
- Workup 5a: indication and test on one line in the darker tinted band; findings below, lighter and smaller; one
  aligned left edge; low cognitive load; plain labels; no accent rule beside results.
- Phone table cards: every value starts on one left edge. Text that wraps into a narrow column is widened, never cut.
- Drawers: a floating panel on desktop, a bottom sheet on phones. Inline explanations: hover or click cards on
  desktop; inline on touch.
- Study mode: masked answers stay masked (blurred) until revealed; nothing the reader should recall shows through.
- Pastel-leaning palette; no emojis.

## Severity
- HIGH: something unusable or a study-mode leak (a masked answer readable), or text unreadable.
- MED: a scope item above not delivered or visibly broken (wrong color job, overlap, a control that does not work as
  described, a protected color changed by the accent).
- LOW: polish (spacing, alignment, a softer or stronger tint would read better).
Cite the screenshot file and where on it (section name, row) for every finding.
