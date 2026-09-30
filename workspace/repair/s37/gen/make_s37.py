#!/usr/bin/env python3
"""make_s37.py: writes repair/s37/*.json. Psych goes live for Jonathan's review (2026-09-30, his approval):
s36 page setup (psych shelf, section, Type C CSS, hide-empty-section fix), 9 psych briefs, Kawasaki migration.
Replayable: python3 repair/s37/gen/make_s37.py <psych drafts dir>  (brief sources: <dir>/<P1..N6>/brief.html)."""
import json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE); WS = os.path.dirname(os.path.dirname(B))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import read_page, brief_by_id
SRC = sys.argv[1]

def dump(name, edits):
    with open(os.path.join(B, name), 'w', encoding='utf-8') as f:
        json.dump({'edits': edits}, f, indent=1, ensure_ascii=False); f.write('\n')

# 10-30: s36 setup regenerated from the current tools/typec/typec.css, plus the hide-empty-section fix
subprocess.run([sys.executable, os.path.join(WS, 'repair', 's36', 'gen', 'make_s36.py')], check=True)
for f in ('10_shelf_psych.json', '20_section_psych.json', '30_typec_setup.json'):
    shutil.copy(os.path.join(WS, 'repair', 's36', f), os.path.join(B, f))
shutil.copy(os.path.join(WS, 'repair', 's36', 'proposed', '25_hide_empty_section.json'), os.path.join(B, '25_hide_empty_section.json'))

def crit_rows(h):
    # the page's columnizer grids a criteria tile only when its items read "<b>Term</b> &ndash; definition" (render
    # not-gridded); the drafts wrote "<b>Term:</b> definition". Markup only: the colon becomes the en dash separator.
    def fix(m):
        return re.sub(r'<b>([^<]+?):</b>\s*', r'<b>\1</b> &ndash; ', m.group(0))
    return re.sub(r'<div class="crit[^"]*"[^>]*>(?:(?!</div>).)*</div>', fix, h, flags=re.S)

# 40: psych briefs, in teaching order
ORDER = ['P1', 'N1', 'N3', 'N2', 'N5', 'N4', 'P2', 'P3', 'N6']
briefs = []
for d in ORDER:
    h = crit_rows(open(os.path.join(SRC, d, 'brief.html'), encoding='utf-8').read().strip())
    bid = re.search(r'<div class="brief[^"]*" id="([^"]+)"', h).group(1)
    h4 = re.sub(r'<[^>]+>', '', re.search(r'<h4[^>]*>(.*?)</h4>', h, re.S).group(1))
    short = re.sub(r'\s*\([^)]*\)', '', h4.split(':')[0]).strip()
    briefs.append((bid, h, short))
NOTE = '<p class="system-note">Mood, anxiety, psychotic, substance use and behavioral topics.</p>\n'
SECT = '    <div class="sect">Psychiatry &amp; Behavioral Health <span class="count">0</span></div>'
ed = [
 {'op': 'replace_global', 'find': '<span class="n">0 topics</span></h3>\n' + NOTE,
  'with': '<span class="n">%d topics</span></h3>\n' % len(briefs) + NOTE + '\n' + briefs[0][1] + '\n'},
 {'op': 'replace_global', 'find': SECT,
  'with': SECT.replace('>0<', '>1<') + '\n    <a href="#%s">%s</a>' % (briefs[0][0], briefs[0][2])},
]
for (pid, _, _), (bid, h, short) in zip(briefs, briefs[1:]):
    ed.append({'op': 'new_brief', 'after': pid, 'html': h, 'nav': {'after_link': pid, 'title': short}})
dump('40_psych_briefs.json', ed)

# 50: Kawasaki migration (reviewer-accepted candidate; same id and title, 10 carried items + 3 new)
page = read_page(os.path.join(WS, 'index.html'))
b = brief_by_id(page, 'kawasaki')
new = crit_rows(open(os.path.join(WS, 'repair', 'migration', 'kawasaki', 'brief.html'), encoding='utf-8').read().strip())
dump('50_kawasaki_typec.json', [{'op': 'replace_brief', 'brief': 'kawasaki', 'html': new,
    'ledger': 'repair/migration/kawasaki/claim_map.json (local-only)', 'note': 'Type C migration, reviewer-accepted (R11 to R14)'}])
print('s37:', [x[0] for x in briefs], '+ kawasaki')
