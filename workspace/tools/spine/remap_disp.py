#!/usr/bin/env python3
"""remap_disp: re-derive covered:S### ids after a build edit (runbook S1 card checklist; moved from the s148 scratch
tools into the repo, s148 efficiency fix 5).

  python3 remap_disp.py <brief folder> <old claim_map.json>

Each covered id is mapped by its old claim text to the new claim with the same text, else the closest text (ratio >= 0.6,
reported), else dropped (reported). Writes cards_disposition.json in place and prints what changed.
"""
#!/usr/bin/env python3
import difflib
import json
import os
import re
import sys


def texts(cm):
    return {c['id']: (c.get('new_text') or c.get('text') or '') for c in cm['claims']}


def main(folder, old_path):
    old = texts(json.load(open(old_path)))
    new = texts(json.load(open(os.path.join(folder, 'claim_map.json'))))
    by_text = {}
    for i, t in new.items():
        by_text.setdefault(t, i)
    dp = os.path.join(folder, 'cards_disposition.json')
    disp = json.load(open(dp))
    changed = 0
    for k, v in disp.items():
        if not v.startswith('covered:'):
            continue
        m = re.match(r'covered:((?:S\d{3},?)+)(.*)$', v)
        note = m.group(2) if m else ''
        ids = []
        for i in (m.group(1).strip(',').split(',') if m else v[8:].split(',')):
            t = old.get(i)
            if t is None:
                print('unknown old id', k, i)
                continue
            if t in by_text:
                ids.append(by_text[t])
                continue
            best = max(new.items(), key=lambda kv: difflib.SequenceMatcher(None, t, kv[1]).ratio())
            r = difflib.SequenceMatcher(None, t, best[1]).ratio()
            if r >= 0.6:
                ids.append(best[0])
                print('fuzzy %s %s -> %s (%.2f): %s' % (k, i, best[0], r, best[1][:90]))
            else:
                print('DROPPED %s %s: %s' % (k, i, t[:90]))
        ids = sorted(set(ids))
        nv = 'covered:' + ','.join(ids) + note if ids else v
        if not ids:
            print('NO CLAIM LEFT for', k, '(kept old value; fix by hand)')
        if nv != v:
            changed += 1
            disp[k] = nv
    json.dump(disp, open(dp, 'w'), indent=1, ensure_ascii=False)
    print('remap_disp: %d disposition(s) changed' % changed)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
