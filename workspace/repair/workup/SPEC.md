# Diagnostic workup tables: drafting spec

You are drafting "Diagnostic workup" tables for briefs in the AxBx study page `/home/claude/axbx/index.html` (a medical board-prep page; each brief is `<div class="brief..." id="ID">...</div>`). Read-only on index.html: do NOT edit it. Write your output as JSON to the path you are given.

## Goal
The user (a third-year medical student) wants every brief whose topic has a real diagnostic sequence to show that sequence inside the brief: the screening or first test, the next step by branch, the confirmatory test, and the tempting test to skip. NBME tests exactly this ("most appropriate diagnostic study to obtain at this time" vs "most likely to confirm the diagnosis").

## Reference examples already on the page (read them first)
- `aq-bruising`: the table captioned "Diagnostic workup" (the model the user loves).
- `bs-spherocytosis`, `septic-hip`, `congenital-hypothyroid`: pilot tables captioned "Diagnostic workup".
- `secondary-htn`: an existing table extended with a "Confirms, then" column.

## Table shape (for action "new")
Columns: Test | Order | Result | What it points to. 4 to 7 rows, in the order a clinician would actually order them.
- Order values, use only: `Screen`, `First`, `Next`, `By branch`, `Supports`, `Confirms`, `Cause`, `Staging`, `Skip`. "Confirms" must appear when a confirmatory test exists. If the diagnosis is clinical (no test confirms it), include a row: Test "None: clinical diagnosis" (or similar plain wording), Order "Confirms", and say what the tests are for (excluding mimics).
- Include one `Skip` row when there is a classic tempting wrong test (board trap), especially one the brief or its question bank already names.
- Result cell: the finding, with exactly one `<b>...</b>` on the deciding word or phrase. Other cells: no bold.
- Keep cells short: Test up to about 8 words, Result up to about 14, What it points to up to about 16.
- Content must agree with the brief's own text and its question bank (`<ol class="bank">` items: stem → <b>key</b> → note). Read the whole brief before drafting. Do not repeat the brief's differential table; this table is about tests and their order.

## Voice and style (strict; the user rejects violations)
- Plain, natural clinical English. No slogans, aphorisms, taglines or clever phrasing. No em dashes (use commas, semicolons or colons). No emojis.
- American spelling. Standard abbreviations are fine (CBC, ESR, CRP, MRI, CT, TSH).
- HTML entities: write `&lt;` and `&gt;` for < and >; `&amp;` for &. Plain words like "over 50,000" are preferred to symbols.
- Only commonly accepted, guideline-standard facts. Do not invent numbers. If you include a specific number or claim you are not certain is standard, append ` ⚠︎` to that cell; do NOT use ⚠︎ on standard, commonly known facts.

## Existing tables (action "extend")
If the brief already has a table that lists first tests (e.g. "clue → diagnosis → first test"), prefer extending it: add a column (e.g. `<th>Confirms, then</th>`) and a matching cell per row, using exact find/replace edits. Each `old` string must be copied exactly from index.html and must occur exactly once inside that brief. Alternatively, if extending is awkward, use "new" and make the new table add what is missing (order and confirmation) without repeating the old one.

## Action "none"
Use only if the topic truly has no diagnostic sequence (pure management, prevention schedule, or the brief is not about diagnosis). Give a one-line reason.

## Output JSON (a list, one object per assigned brief, in the order given)
```json
[
 {"brief":"septic-hip","action":"new",
  "rows":[["CBC, ESR and CRP","First","Count the <b>Kocher</b> predictors ...","3 or more: aspirate"], ...],
  "note":"one line on anything uncertain or any conflict you found in the brief"},
 {"brief":"dvt","action":"extend",
  "edits":[{"old":"<exact text>","new":"<replacement>"}],
  "note":"..."},
 {"brief":"x","action":"none","note":"reason"}
]
```
Validate your JSON parses (python3 -c "import json;json.load(open(PATH))") before finishing. Final reply: one line per brief (id, action, row count), plus any conflicts you noticed in the brief's existing content.
