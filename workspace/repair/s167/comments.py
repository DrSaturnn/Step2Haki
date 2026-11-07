#!/usr/bin/env python3
"""comments.py: s167 step 5b, decision narration out of the site/js source comments (D-20261105-6).

The comments that name a person, a date, a batch id, a review round or a planning document are rewritten to say what
the code does, or removed where the code says it. NEW maps the index of each such comment (in file order, the order
`python3 repair/s167/comments.py --list` prints; run once: afterwards the list is empty) to its replacement ('' removes it). A comment the map does not cover
fails the run, so a new narration comment is not passed over.

  python3 repair/s167/comments.py [--list] [--dry]
"""
import glob, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NARR = re.compile(r'Jonathan|\bs1\d\d[a-z]?\b|DIGEST|STANDING|handoff|Decided|D-20\d{6}|20\d\d-\d\d-\d\d|\br\d\b')
COMMENT = re.compile(r'/\*.*?\*/|(?<![:\'"\\/])//[^\n]*', re.S)

NEW = {
 0: '// flat is the default',
 1: '/* BOARD-STYLE ONLY starts off on every visit: a remembered switch could hide whole shelves on one device. */',
 2: '/* switching shelf releases a pin the new shelf does not include; otherwise a stale #brief in the address bar keeps\n   that brief, its system section and its sidebar link on every shelf. */',
 3: '// an instant jump; axnav then seats the target while lazy briefs above it render',
 4: '/* Prebuilt index: the build writes search.json beside the page (tools/search_index.js; format in its header) and the\n   gate fails when the file does not match the page. The page fetches it once the loader settles, versioned by the\n   build stamp. A brief built before the file lands, or after, is read from the page. A failed fetch, a file that does\n   not list this page\'s briefs, or a page opened from disk builds the index in the page (sxBuild over template copies);\n   the result list says so. */',
 5: '/* study mode masks the bottom line and the pause point in every spine brief */',
 6: "/* the choice's one-line reason, shown under it once the answer is revealed */",
 7: '/* 3 briefs a session */',
 8: '/* the sheet shows the briefs a session will review before it starts; buildSession then reviews exactly those */',
 9: '/* scheduled reviews only, never the shelf total */',
 10: '/* zoomed px in, CSS px out */',
 11: '/* the status-bar Review sheet drives this scheduler through window.axRv */',
 12: '/* scheduled reviews only, never the shelf total */',
 13: '/* one outline per exam. Rows list the exam\'s own categories; a brief counts in the row of its first data-bp code, or\n   in that exam\'s "Other systems" row. Sources: nbme.org subject exam content outlines (Pediatrics, Psychiatry, Medicine,\n   Surgery, Obstetrics & Gynecology, Clinical Neurology, Family Medicine) and usmle.org Step 2 CK content specifications. */',
 14: '/* Decision spine.\n   Popovers: mechanisms and "why order it" notes. Desktop (fine pointer): hover or click opens a card. Touch: tap opens the\n   same text inline under the whole line.\n   Drawers: the reasoning moves into another brief. The drawer shows that whole brief, cloned, minus its practice questions.\n   Any link inside a drawer closes it and jumps to the real brief, so a drawer never opens another drawer. */',
 15: '// html zoom 1.1 at 1500 px and wider; rects and scroll are zoomed px, CSS lengths are not',
 16: "// through the sidebar's seating (brief:go); a smooth hash scroll across unbuilt briefs overshoots as they build",
 17: '/* practice questions as an overlapped stack with back and next. The question cards are not moved or rebuilt: the\n   stack only marks one card current, so answers, filters, study mode and progress keep working. */',
 18: '/* Brief boundaries. Builds, for every brief: a sticky bar (<=1100px), a sticky section rail (>1100px) and an end cap.\n   Sections: spine briefs follow their stepper (absent steps greyed); other briefs use their section headings, after an Overview\n   entry for the top of the brief. Built at load from the page itself; nothing is stored. Drawer clones strip all three (spine.js). */',
 19: "/* the rail fill ends at the highlighted section's link, not at the brief's scroll height: sections differ in length\n     while the links are evenly spaced, so a height-based fill disagreed with the highlight */",
 20: '// a step is current once its heading passes 32% of the window, on desktop and phone: the same line as the sidebar index',
 21: '/* Timeline axis labels. Greedy two-line layout for every .rax: each label stays on line 1 if it clears the label\n   before it (and the end arrow), else drops to line 2, else hides. Re-runs whenever an axis changes width (panels opening,\n   drawers, resizes). Nothing is stored. */',
 22: '/* Timeline charts as cards: give every row of a keyed timeline chart its own legend, listing only the marks that\n   row draws, then hide the shared legend when every row has one. Charts without a legend are left as they are. */',
 23: "/* Workup stages as headed cards: move each stage label into its card as the card's header. Stages without a card\n   keep their label where it is. Runs once at load; nothing is stored. */",
 24: "/* Site layout. Presentation only; never adds or removes brief text.\n   1. Accent setting: a reader choice under the theme switches, stored per viewer; Slate default.\n      Dark theme: a switch beside Flat theme, stored per viewer, light by default.\n   2. Desktop hovers: open on pointer enter, close on leave, stay open once clicked (a second click closes).\n   3. Desktop glass toolbar: the current section's number and name, Read and Recall, open or close every panel.\n   4. Sidebar systems fold and unfold; the system holding the current brief opens itself. */",
 25: '// tinted glass: dark plus accent-tinted translucent surfaces',
 26: '/* the rail may sit in the sidebar */',
 27: '',
 28: '/* 5. Mnemonic key column fits its widest key, so a long key does not overrun the 28 px column on desktop or push\n     phone text into a narrow column. Only a list with a key wider than one letter changes. */',
 29: '/* Review in the status bar. A Review pill in the glass toolbar (desktop) and the phone bar\'s Review button open one\n   glass sheet: who is studying (with a passcode pad when the name has a PIN), the 3 briefs the scheduler recommends\n   next, Start review and Quiz me instead; no total briefs count. The scheduler, sync and PIN check are the page\'s own\n   (window.axRv, exposed by the review script); this file is presentation only. */',
 30: '// zoomed px in, CSS px out',
 31: '/* Display layer. Presentation only: never adds, removes or rewords brief content; the brief HTML in the page is unchanged.\n   1. Diagnostic workup as Test | Result | Means tables per numbered zone (header cells, row spans, group tints).\n   2. Clue table column "Next best step".\n   3. Mnemonic rows: the key text sits in its own cell beside the tinted capital.\n   4. Desktop: the current brief\'s section steps nest under it in the sidebar (fill-to-current-link rule kept). */',
 32: '// the sidebar draws its own rail',
 33: '// a rail already nested stays nested, so a class change in the sidebar does not move it out and back',
 34: '// the axnav component keeps its own list in view',
 35: '/* Sidebar movement. Presentation only.\n   1. The current step is marked by one lens that glides between steps on a spring.\n   2. Steps a brief does not use say so ("Not used"); "Urgent" reads "Urgent risks", as the step heading does.\n   3. The sidebar list keeps the current step in view, and on a new brief brings that brief near the top.\n   4. The list fades at its top and bottom edges.\n   5. Opening the page on a brief\'s link lands on that brief: the layout scripts reflow the page after the browser\'s\n      first jump to the link, so it is placed again until the reader moves. */',
 36: '// the axnav component draws the rail',
 37: '// axnav seats the landing',
 38: '/* an arrow for a high or low value stays on the line of the word it qualifies. Presentation only: the space beside the\n   arrow becomes a no-break space; no text changes. */',
 39: "/* The sidebar as one component. Presentation only: no text is invented. The old #navlinks list stays in the page,\n   hidden, because the shelf, Board-style only and search scripts write their filters onto it; this list mirrors its\n   visibility and counts and draws: systems that fold (chevron, name, count), brief tiles, and under the current brief\n   its step rail with the fill and one lens that glides between steps. A step is current once its heading passes 32% of\n   the window; a click on a step takes effect at once and the spy waits 0.9 s. The list keeps the current step in view.\n   The switches the sidebar does not carry (shelf, Board-style only, Recall, themes, accent, the change log) move into\n   a display sheet behind the round button in the brand row. */",
 40: '/* the shelf card; the shelf <select> lies invisibly over it */',
 41: '// under the search',
 42: '// the shelf picker is a card under the search',
 43: '// one home per brief: the rail always sits under the home tile (the system tile; a',
 44: "// Presentations-only brief's home is its Presentations tile); the other tile is marked, never current (earlier: the",
 45: '// browsing Presentations, follow its tile',
 46: '// a click in Presentations keeps the sidebar there',
 47: '// already current, so bring its home tile (or, browsing, this tile) into view',
 48: '/* brief:go id: a jump to a brief from elsewhere on the page (07 drawer links) takes the same path as a sidebar\n     click: the hash, then the target seated until it holds while the briefs above it build */',
 49: '/* Onset timeline placement: the timeline boxes fit all their text. After layout and on every resize: walk the events\n   left to right and put each card on the lowest tier where it overlaps no card (8 px gap), its leader line crosses no\n   card below it, and it covers no leader line from above; each tier sits on the tallest card below it and the chart\n   height follows. If the cards cannot fit at a width, the figure takes the phone list layout. Phone and study mode keep\n   their list layouts. */',
 50: '/* Question tiles one size with a chip row, a Review grouped by result, hover cards that animate out as well as in,\n   linked-brief previews with an open icon, and Pairs with as a list. Presentation only: no brief text or markup in the\n   page source changes. */',
 51: '// the three choices, each with its reason',
 52: "/* in a Differential row, the preview adds the linked brief's diagnostic criteria (its step 2), cloned from\n     that brief when the preview opens, so no copy exists to drift. Only when the row names that brief's diagnosis or\n     one of its criteria blocks; a row whose drawer opens a broader brief gets none. */",
 53: '/* word forms read as one word: an abbreviation as its words, an adjective as its noun (after the plural trim) */',
 54: "// fg, the step's window figures (figure.lcw)",
 55: "/* a window figure one of whose rows names the row's diagnosis (Brief psychotic disorder, Delirium tremens) */",
 56: '/* Hover cards float on touch as on desktop, and a linked brief opens as a panel grown from its link (desktop) or a\n   near-full-screen sheet grown from the tapped link (phone). The per-choice reasons, the card sizing, the First step\n   split and the timeline tile are in the page script (mcq), the 20-site-148f script and the styles. Presentation only:\n   no brief text changes. */',
 57: '/* NBME presentations view, built at load from the page itself: framing blocks (div.nbq and pp-b[data-nbme]), linked\n   practice items (li or .mcq[data-nbme]), NBME descriptions ([data-nbme-src]) and cross-domain tags ([data-xdom]), plus\n   the static table of logged CMS items whose key or decoy crosses a domain. */',
 58: '/* Presentations sub-headers: shown only while a brief under them is shown; the count is the briefs shown */',
}


def main(a):
    k, files, found = 0, {}, []
    for f in sorted(glob.glob(os.path.join(WS, 'site', 'js', '*.js')) + glob.glob(os.path.join(WS, 'site', 'pwa', '*.js'))):
        src = open(f, encoding='utf-8').read()
        def rep(m):
            nonlocal k
            c = m.group(0)
            if not NARR.search(c):
                return c
            i = k; k += 1
            found.append((i, os.path.basename(f), c))
            if i not in NEW:
                raise SystemExit('comments.py: comment %d in %s has no replacement: %s' % (i, os.path.basename(f), c[:80]))
            return NEW[i]
        new = COMMENT.sub(rep, src)
        if new != src:
            files[f] = new
    if '--list' in a:
        for i, f, c in found:
            print('###', i, f); print(c)
        return 0
    print('comments: %d narration comments rewritten in %d files' % (len(found), len(files)))
    if '--dry' not in a:
        for f, s in files.items():
            open(f, 'w', encoding='utf-8').write(s)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
