#!/usr/bin/env python3
"""Offline tests for the 2026-10-12 rules: alias words are not counted against the soft cap (outline_check.strip_aka),
and verify's V1 allowlist reads repair/efficiency/ABBREV.json.

  python3 tools/spine/test_caps_abbrev.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outline_check import strip_aka, strip_collapsed, strip_hover  # noqa: E402
from verify import ACR_OK  # noqa: E402

ok = bad = 0


def expect(name, cond):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', name)


h = '<td>Minimal change disease <span class="aka">(lipoid nephrosis)</span>; protein mainly albumin</td>'
expect('aka words dropped', 'lipoid' not in strip_aka(h) and 'albumin' in strip_aka(h))
expect('two aka spans', strip_aka(h + h).count('lipoid') == 0)
expect('other spans kept', 'keep' in strip_aka('<span class="mask">keep</span>'))
for a in ('CBC', 'BUN', 'US', 'CT', 'MRI', 'BP', 'HR'):
    expect('allowlist has %s' % a, a in ACR_OK)
for a in ('MRV', 'ECG', 'UA', 'FSGS', 'PSGN'):
    expect('allowlist does not have %s' % a, a not in ACR_OK)

# ---- hover bodies are not counted (Jonathan 2026-10-13)
hv = ('<p>keep1 <button class="sp-pop">label</button><span class="sp-pop-b" id="x" hidden><span class="sp-ct">In practice:</span>'
      'gone1 <span class="mask">gone2</span> gone3</span> keep2</p>')
expect('hover body dropped, nested spans included', all(w not in strip_hover(hv) for w in ('gone1', 'gone2', 'gone3', 'In practice')))
expect('text around the hover kept, button label kept', all(w in strip_hover(hv) for w in ('keep1', 'keep2', 'label')))
expect('two hovers both dropped', 'gone' not in strip_hover(hv + hv) and strip_hover(hv + hv).count('keep2') == 2)
expect('no hover: unchanged', strip_hover('<span class="mask">m</span>') == '<span class="mask">m</span>')
expect('words do not run together across a dropped hover', 'keep1' in strip_hover('a<span class="sp-pop-b">x</span>b') or 'a b' in strip_hover('a<span class="sp-pop-b">x</span>b'))


# ---- the collapsed systems panel is not counted; its summary line is (Jonathan 2026-10-13)
sy = ('<p>keep3</p><details class="sp-sys"><summary>What tics do<small>detail</small></summary>'
      '<div class="sp-sysr"><span class="k">gone4</span><span class="f">gone5</span></div></details><p>keep4</p>')
expect('systems panel body dropped', 'gone4' not in strip_collapsed(sy) and 'gone5' not in strip_collapsed(sy))
expect('summary line and text around it kept', all(w in strip_collapsed(sy) for w in ('What tics do', 'keep3', 'keep4')))
expect('other details kept', 'x' in strip_collapsed('<details class="other"><summary>s</summary>x</details>'))

print('test_caps_abbrev: %d passed, %d failed' % (ok, bad))
sys.exit(1 if bad else 0)
