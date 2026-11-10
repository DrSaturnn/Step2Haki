# Task: judge hover anchors (no brief text is written or reworded)

A hover on the Step2Haki study page is a trigger (a word or phrase in a line of a brief) that opens a card. The rule
(D-20261108-5): each hover sits on the term its card explains. Your packet, LANE_PACKET.md in this lane, lists
hovers. For each one you get the trigger, the whole line it sits in, the row head (the first cell of the table row,
when the line is a table cell), and the card (kicker, title, body). Text in [[double square brackets]] is hidden in
study mode (masked).

## The one question per hover
Does this card define or explain the trigger term itself?

Find the card's subject first: what the title names, or what the body's first line is about. Then compare it with
the trigger.

- **KEEP**: the trigger is the card's subject, a standard synonym or abbreviation of it, or a phrase whose head noun
  is the subject. A reader who taps the trigger and asks "what is this, how does it work, when does it apply, what
  are its criteria, its causes, its exceptions" gets that answer about the trigger term.
- **MOVE**: the trigger is not the card's subject, and another term in the same Line or in the Row head is. Name that
  term.
- **LABEL**: no term in the Line or the Row head is the card's subject. The hover then gets its own short label
  trigger.

Never KEEP:
- a generic word as trigger ("New", "Offered", "board", "first", "also", "risk") when the card is about a specific
  subject;
- a bare number, dose, age, duration or interval as trigger, when the card explains something other than what that
  number measures (for example an exception, a different drug, a guideline position on another point). A number
  stays KEEP only when the card is about that number itself (why that cutoff, what the window means);
- a finding, test or drug that only appears together with the card's subject (same row, same disease) while the card
  explains the disease, the mechanism or another item. Example: trigger "Finkelstein test positive", row head
  "De Quervain tenosynovitis", card title "De Quervain", body "Stenosing tenosynovitis of the abductor pollicis longus
  and extensor pollicis brevis in the first extensor compartment." The card explains De Quervain, the trigger names a
  test: MOVE to row head term "De Quervain tenosynovitis".

Judge the fit only. Do not judge whether the card's medical content is right, and do not reword anything.

## MOVE rules
- The term is copied character for character from the Line or the Row head as shown in the packet (same case,
  spacing and punctuation), is one contiguous piece of text, and is the shortest phrase that names the card's subject
  (a noun phrase of 1 to 5 words; no leading article, no trailing punctuation).
- The term must lie outside [[masked]] text, with one exception: when the present trigger is itself inside a mask, a
  term inside the same masked stretch of the Line is allowed.
- Prefer a term in the Line. Use the Row head only when the Line has no fitting term.
- Give `where` as `line` or `rowhead`.

## LABEL rules
- The label is the card's kicker, copied word for word. When the card has no kicker, or the kicker is a source name
  (a label, a guideline, a book, "AnKing", "UWorld", "NBME"), use the card's title copied word for word.
- When the card fits no term of its row because the row needs a different card (the card's content is off-topic for
  the whole line), still give LABEL and add `NEEDS-CONTENT` at the start of the reason.

## Borderline
When KEEP and not-KEEP are close, ask: would a student who taps this exact trigger be surprised by what the card
talks about? Surprised: not KEEP. Say "borderline" in the reason.

## Receipt
Write one file, receipt.md, in your lane (absolute path: %(lane)s/receipt.md). First line: `# receipt %(name)s`.
Then one line per hover, in packet order, every hover exactly once, in this pipe format and nothing else on the line:

`<pop id> | KEEP | - | - | <reason>`
`<pop id> | MOVE | line or rowhead | <exact term> | <reason>`
`<pop id> | LABEL | - | <label> | <reason>`

Written out plainly, a line looks like:
wh-pop-4 | MOVE | rowhead | De Quervain tenosynovitis | card explains De Quervain, trigger is a test

The reason is at most 12 words and names the card's subject. No pipe characters inside a field. Last line of the
file: `TOTAL KEEP n MOVE n LABEL n` with counts that sum to the packet's hover count (%(n)d).

Calls: read this file, read LANE_PACKET.md (in two or three reads if long), write receipt.md once (a second write
only to complete it). Your budget is %(budget)d calls. Your final message: the three counts only.
