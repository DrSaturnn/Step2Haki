# Task: review the changed hover triggers (no text is written or reworded)

The page's hover triggers were re-placed so that each hover sits on the term its card explains. LANE_PACKET.md in
this lane lists every changed hover. MOVE: the trigger now sits on another term of the same line or on the row head.
MARKER: the old trigger text is plain text again and the card opens from a small circled i after it. No visible wording
changed. Text in [[double square brackets]] is hidden in study mode until the student reveals it.

Check each hover for these four things, and report only the failures:

1. LEAK (HIGH). The new trigger is marked "visible in study mode". A student can open its card before revealing the
   masked text. It is a leak when the card's kicker, title or body states the content of a [[masked]] stretch of the
   same row or line (the same test, drug, finding, number or diagnosis, in the same or other words) so that reading
   the card gives away the masked answer. A card that only explains the visible term is not a leak. Hovers whose old
   trigger "was inside a mask" and whose new trigger is visible need the closest look. For a MARKER judge the same way.
2. FIT (MEDIUM). MOVE only: the new trigger is not the card's subject (the card explains something else in the row).
3. DOUBLE (LOW). The new trigger's term carries another trigger in the same row or line, or two triggers sit on
   overlapping text.
4. SPAN (LOW). The new trigger is cut mid-phrase or carries extra words (a leading article, a trailing verb or
   punctuation) so that it does not read as one term.

Do not judge the medical content of a card and do not propose rewording.

## Receipt
Write one file, %(lane)s/receipt.md. First line `# receipt review`. Then one line per failure, pipe format:

`<pop id> | LEAK or FIT or DOUBLE or SPAN | HIGH or MEDIUM or LOW | <what, at most 20 words; for LEAK quote the masked words the card gives away>`

Then a line `CHECKED n` with the number of hovers you checked (%(n)d expected), and a last line `Verdict: PASS` when
there is no HIGH or MEDIUM line, `Verdict: FAIL` when there is one.

Calls: read this file, read LANE_PACKET.md (two or three reads), write receipt.md once. Budget %(budget)d calls. Final
message: the verdict and the counts by kind.
