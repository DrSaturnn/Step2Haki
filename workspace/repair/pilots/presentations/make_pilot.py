"""Pilot (not shipped): Presentations as its own section (Jonathan 2026-11-03: "cant we just remove all duplicated briefs
and keep the same dropdowns? so its just presentations?"; "just having a presentations carry its own order of each
system as sub headers, then having the rest of the systems as normal").
Every brief in the sidebar's Presentations group leaves its system: on the page it moves, byte for byte, into a new
Presentations section after "How to Use This", under a sub-header per system in page order; in the sidebar it is
listed only under Presentations, under the same sub-headers. Every other brief stays where it is. Sidebar order and page
order then agree, so the current brief never switches groups while scrolling. Presentation only: no brief text changes.
Usage: python3 make_pilot.py <live index.html> <out.html>"""
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools'))
from pagelib import read_page, briefs
src, out = sys.argv[1], sys.argv[2]
s = read_page(src)
LABEL = {'msk': 'Musculoskeletal', 'peds': 'Pediatrics', 'cv': 'Cardiovascular', 'pulm': 'Pulmonary',
         'gi': 'GI & Hepatology', 'renal': 'Renal & GU', 'endo': 'Endocrine & Bone', 'heme': 'Hematology',
         'id': 'Infectious Disease', 'neuro': 'Neuro & HEENT', 'derm': 'Dermatology & Wounds', 'obgyn': 'OB / GYN',
         'prev': 'Preventive & Ethics', 'psych': 'Psychiatry & Behavioral Health'}
esc = lambda t: t.replace('&', '&amp;')

# ---- the sidebar's Presentations group
j = s.index('<div id="navlinks">'); k = s.index('</aside>', j); nav = s[j:k]
p0 = nav.index('<div class="sect">Presentations'); p1 = nav.index('<div class="sect">', p0 + 10)
pres_block = nav[p0:p1]
pres = re.findall(r'<a(?: class="[^"]*")? href="#([\w-]+)">', pres_block)
title = {m.group(1): m.group(2) for m in re.finditer(r'<a(?: class="[^"]*")? href="#([\w-]+)">([^<]*)</a>', nav)}

# ---- which page section holds each, in page order
hs = [(m.start(), m.group(1)) for m in re.finditer(r'<h3 class="system" id="([\w-]+)"', s)]
def section(pos):
    cur = None
    for at, hid in hs:
        if at < pos: cur = hid
    return cur
B = briefs(s)
moving = [b for b in B if b.id in set(pres)]
assert len(moving) == len(pres) == 40, (len(moving), len(pres))
groups = []
for b in moving:
    sec = section(b.start)
    if not groups or groups[-1][0] != sec: groups.append((sec, []))
    groups[-1][1].append(b)
assert len({g for g, _ in groups}) == len(groups), 'a system appears twice'

# ---- page: cut the briefs (with the blank lines after them), then add the section before the MSK section
chunks = {b.id: s[b.start:b.end] for b in moving}
for b in sorted(moving, key=lambda x: -x.start):
    e = b.end
    while e < len(s) and s[e] in ' \t\r\n': e += 1
    s = s[:b.start] + s[e:]
anchor = '<!-- =================== MSK =================== -->'
assert s.count(anchor) >= 1   # the live page carries this comment twice above the MSK section; insert above the first
sec = ['<!-- =================== PRESENTATIONS =================== -->',
       '<h3 class="system" id="presentations">Presentations <span class="n">%d complaints</span></h3>' % len(moving),
       '<p class="system-note">Workups that start from the patient\'s complaint, grouped by system.</p>', '']
for g, bs in groups:
    sec.append('<div class="psub" id="pres-%s"><span class="t">%s</span><span class="n">%d</span></div>\n' % (g, esc(LABEL[g]), len(bs)))
    for b in bs:
        sec.append(chunks[b.id] + '\n')
s = s.replace(anchor, '\n'.join(sec) + '\n' + anchor, 1)

# ---- sidebar: Presentations group with system sub-labels; the 40 links leave the system groups
j = s.index('<div id="navlinks">'); k = s.index('</aside>', j); nav = s[j:k]
p0 = nav.index('<div class="sect">Presentations'); p1 = nav.index('<div class="sect">', p0 + 10)
new = '<div class="sect">Presentations <span class="count">%d</span></div>\n' % len(moving)
for g, bs in groups:
    new += '    <div class="navsub">%s</div>\n' % esc(LABEL[g]) + ''.join('    <a href="#%s">%s</a>\n' % (b.id, title[b.id]) for b in bs)
new += '\n    '
rest = nav[p1:]
for i in pres:
    rest, n = re.subn(r'\n[ \t]*<a(?: class="[^"]*")? href="#%s">[^<]*</a>' % re.escape(i), '', rest)
nav = nav[:p0] + new + rest
# each system group's hand-kept count follows its remaining plain links (gate nav-count)
def recount(m):
    body = m.group(3)
    plain = len([1 for t in re.findall(r'<a\b[^>]*>', body) if 'class=' not in t])
    return m.group(1) + str(plain) + m.group(2) + body
def end_of_div(t, i):
    d = 0
    for m in re.finditer(r'<div\b|</div>', t[i:]):
        d += 1 if m.group(0) == '<div' else -1
        if d == 0: return i + m.end()
nl_end = end_of_div(nav, 0)
tail = nav[nl_end:]; nav = nav[:nl_end]
nav = re.sub(r'(<div class="sect">(?:(?!</div>).)*?<span class="count">)\d+(</span></div>)((?:(?!<div class="sect).)*)', recount, nav, flags=re.S) + tail
s = s[:j] + nav + s[k:]

# ---- section tab short name; sub-header style; sub-headers hide with their briefs (shelf, Board-style only, search)
def sub(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80]); s = s.replace(old, new)
sub("var SHORT={msk:'MSK',", "var SHORT={presentations:'CC',msk:'MSK',")
sub('</head>', '''<style id="ax-pres">
/* s161c Presentations section (Jonathan 2026-11-03): a sub-header per system above its complaint briefs */
.psub{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:34px 0 14px;padding:0 4px 8px;border-bottom:1px solid var(--hair)}
.psub .t{font-family:var(--serif);font-size:19px;font-weight:600;color:var(--ink)}
.psub .n{font:700 11.5px/1 var(--sans);color:var(--muted);letter-spacing:.4px}
@media print{.psub{display:none}}
</style>
</head>''')
sub('</body>', '''<script>
/* s161c Presentations sub-headers: shown only while a brief under them is shown; the count is the briefs shown */
(function(){
  function fit(){
    document.querySelectorAll('.psub').forEach(function(h){
      var n = 0, el = h.nextElementSibling;
      while(el && el.classList.contains('brief')){ if(el.style.display !== 'none') n++; el = el.nextElementSibling; }
      h.style.display = n ? '' : 'none'; var c = h.querySelector('.n'); if(c) c.textContent = n;
    });
  }
  document.addEventListener('ax-shelf', fit);
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fit); else fit();
  window.addEventListener('load', fit);
})();
</script>
</body>''')
open(out, 'w', encoding='utf-8').write(s)
print('pilot written', out, '; groups', [(g, len(b)) for g, b in groups])
