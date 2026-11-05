"""Pilot (not shipped), s164 item 1: the phone in-brief rail (the sticky bar's section label, its menu and the rail links)
marked one step behind while scrolling. Cause: on phone a step became current only once its heading passed 72 px (under
the sticky bar), while the sidebar index and the desktop rail use a reading line at 32% of the window. A heading in view
below the bar therefore still showed the step before it. Fix: one reading line for both widths, 32% of the window
(never above the bar), so the in-brief rail, the bar label and the sidebar index agree. Presentation only: no text changes.
Usage: python3 make_pilot.py <live index.html> <out.html>
repair/s164/gen_site.py runs this file to collect the same replacements (PAIRS) as replace_global edits."""
import sys
PAIRS = []


def sub(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:80])
    PAIRS.append((old, new))
    return s.replace(old, new)


def apply(s):
    return sub(s,
        "var sth = wide ? Math.max(th + 8, vh * 0.32) : th + 8;   // s141: a step is current once its heading passes 32% of the window on desktop (the Lithium Glance mockup), not 120 px",
        "var sth = Math.max(th + 8, vh * 0.32);   // s141: a step is current once its heading passes 32% of the window (the Lithium Glance mockup), not 120 px; s164: on phone too (was th + 8, under the bar, so a heading in view still showed the step before it), the same line as the sidebar index")


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    s = apply(open(src, encoding='utf-8').read())
    s = s.replace('<title>', '<title>PILOT s164 phone rail: ', 1)
    open(out, 'w', encoding='utf-8').write(s)
    print('pilot written', out, len(PAIRS), 'replacement(s)')
