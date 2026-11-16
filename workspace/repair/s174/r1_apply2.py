#!/usr/bin/env python3
"""s174 round 1 replacement pairs, second pass: pairs written without {{}} ("N. old: X" / "new: Y") or inline
("old {{X}} new {{Y}}"). Applies a pair to rewrite_s174.json when X occurs once in one changed entry (raw text or with
HTML entities decoded); skips a pair whose new text is already present. Writes local/s174/r1_pairs2.md."""
import glob, html, json, re, subprocess
WS = '/home/claude/Step2Haki/workspace'
PAT = [re.compile(r'^\s*\d+\.\s*old:\s*\{?\{?(.+?)\}?\}?\s*\n\s*new:\s*\{?\{?(.+?)\}?\}?\s*$', re.M),
       re.compile(r'old \{\{(.+?)\}\} new \{\{(.+?)\}\}')]
pairs, rows, left = {}, [], []
for rp in sorted(glob.glob(WS + '/repair/efficiency/lanes/s174/r1/lane_*/receipt.md')):
    for sec in re.split(r'^=== ', open(rp).read(), flags=re.M)[1:]:
        head = sec.split('\n', 1)[0].split()
        for p in PAT:
            for m in p.finditer(sec):
                pairs.setdefault(head[0], []).append((head[1] if len(head) > 1 else '?', m.group(1).strip(), m.group(2).strip()))
for bid, ps in pairs.items():
    fo = subprocess.run(['python3', WS + '/tools/spine/folder_of.py', bid], capture_output=True, text=True).stdout.split()[-1]
    p = '%s/%s/rewrite_s174/rewrite_s174.json' % (WS, fo)
    rw = json.load(open(p))
    ents = rw.get('units', []) + rw.get('raw', [])
    seen = set()
    for part, old, new in ps:
        if (old, new) in seen:
            continue
        seen.add((old, new))
        if any(new in html.unescape(e.get('new', '')) for e in ents) and not any(old in html.unescape(e.get('new', '')) for e in ents if old not in new):
            rows.append('- %s %s: already ({{%s}})' % (bid, part, new[:60])); continue
        done = False
        for e in ents:
            s = e.get('new', '')
            for o in (old, html.escape(old, quote=False).replace("'", '&#x27;'), old.replace('->', '&rarr;')):
                if s.count(o) == 1:
                    e['new'] = s.replace(o, new); done = True; break
            if done:
                break
        (rows if done else left).append('- %s %s: %s {{%s}} -> {{%s}}' % (bid, part, 'applied' if done else 'LEFT', old, new))
    json.dump(rw, open(p, 'w'), ensure_ascii=False, indent=1)
open(WS + '/local/s174/r1_pairs2.md', 'w').write('# r1 pairs, pass 2\n\n' + '\n'.join(rows) + '\n\n## Left\n' + '\n'.join(left) + '\n')
print('applied %d, already %d, left %d' % (sum('applied' in r for r in rows), sum('already' in r for r in rows), len(left)))
