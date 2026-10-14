# Receipt format (part: display, site review s136)

Write one file, receipt.md, in your lane:

    part: display
    scope: s136 site layout Phase 1, brief <id> (site review; not a brief receipt)
    Verdict: PASS | FAIL
    Findings
    1. [HIGH|MED|LOW] <screenshot file>, <where>: <what is wrong>. Fix: <what to change>.
    ...
    Checked and fine:
    - <one line per scope item you checked and found delivered>

- `Verdict: PASS`: no HIGH or MED findings (LOW findings may be listed).
- `Verdict: FAIL`: any HIGH or MED stands.
- Judge only what the screenshots show. If a screenshot cannot settle a point, say so as a finding, LOW, with what
  shot would settle it.
- No emojis and no em dashes.
