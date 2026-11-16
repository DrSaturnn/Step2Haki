#!/usr/bin/env python3
"""r2_manual.py: lead edits for round 2 pairs the applier could not place or the lead reworded (s170 chat 5)."""
import json, subprocess, sys
OP = '<span class="op op-a" role="img" aria-label="leads to"></span>'
EDITS = [  # (brief, receipt key, old, new, expected count)
 ('pc-ssri', 'read:1', '<b>Hyponatremia</b>, often from the', '<b>Hyponatremia</b>: often from the', 1),
 ('pc-ssri', 'read:3 (lead wording: no comma restatement)', 'Full dose: 6 weeks before considering a change',
  'Full dose: up to 6 weeks before considering a change', 1),
 ('mdd', 'acc:1', '<p class="sp-note">None of these findings is diagnostic alone.</p>',
  '<p class="sp-note">These findings never make the diagnosis.</p>', 1),
 ('mdd', 'acc:2 (lead wording)', 'Medical illness to exclude: hypothyroidism', 'Medical illness to exclude: e.g., hypothyroidism', 1),
 ('mdd', 'flags:1 MED cut', 'adverse effect or discontinuation; discontinuation can mimic relapse.',
  'adverse effect or discontinuation.', 1),
 ('pc-antidep', 'acc:1 (lead wording)', 'avoid it with <b>seizure disorder</b> or <b>bulimia or anorexia</b>',
  'avoid it with <b>seizure disorder</b> and with current or past <b>bulimia or anorexia</b>', 1),
 ('pc-antidep', 'acc:2 (lead wording: two lines kept)', '<span class="sp-l">Mirtazapine also blocks serotonin 2 and 3 receptors</span>',
  '<span class="sp-l">Mirtazapine: blocks alpha-2 and serotonin 2 and 3 receptors</span>', 1),
 ('pc-antidep', 'read:3', '<span class="sp-l">Painful or not, stop the drug</span><span class="sp-l sp-la">' + OP + ' seek emergency care at once</span>',
  '<span class="sp-l">Painful or not: stop the drug and seek emergency care at once</span>', 1),
 ('pc-tca', 'acc:1', '<b>Fatal at relatively low doses</b>', '<b>Can be fatal at relatively low doses</b>', 1),
 ('pc-tca', 'read:1', 'Tricyclics: block <b>muscarinic</b>, <b>alpha-1</b> and <b>histamine H1</b> receptors besides reuptake',
  'Tricyclics: block reuptake and <b>muscarinic</b>, <b>alpha-1</b> and <b>histamine H1</b> receptors', 1),
 ('voices', 'read:1 (read:2 skipped: the cell label stays)', '<span class="sp-l">Odd beliefs short of delusions',
  '<span class="sp-l">Schizotypal: odd beliefs short of delusions', 1),
 ('pc-snri', 'acc:1 both lines', 'Onset: within days of an abrupt stop', 'Onset: typically within days of an abrupt stop', 2),
 ('pc-snri', 'flags:1 (lead wording: one fact)', 'Discontinuation syndrome: can mimic depressive relapse or influenza',
  'Discontinuation syndrome: can mimic influenza', 1),
]
apply = '--apply' in sys.argv
docs = {}
bad = 0
for b, key, old, new, want in EDITS:
    if b not in docs:
        f = subprocess.run([sys.executable, 'tools/spine/folder_of.py', b], capture_output=True, text=True).stdout.split('\t')[1].strip()
        p = f + '/rewrite_s170/rewrite_s170.json'
        docs[b] = (p, json.load(open(p)))
    p, d = docs[b]
    rows = d['units'] + d.get('raw', [])
    n = sum(r['new'].count(old) for r in rows)
    if n != want:
        print(f'{b} {key}: found {n}, want {want}'); bad += 1; continue
    for r in rows: r['new'] = r['new'].replace(old, new)
if bad: sys.exit(f'r2_manual: {bad} edit(s) not placed; nothing written')
if apply:
    for p, d in docs.values(): open(p, 'w').write(json.dumps(d, indent=1, ensure_ascii=False) + '\n')
print(f"r2_manual: {len(EDITS)} edits placed; {'written' if apply else 'dry run'}")
