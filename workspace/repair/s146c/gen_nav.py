#!/usr/bin/env python3
"""s146c (site layer, Jonathan 2026-10-17): writes repair/s146c/40_nav.json from the live page.
A Presentations group of hubs first in the sidebar; Psychiatry briefs regrouped in six disorder families (sidebar
sub-labels and page order); the sidebar rail follows the row the reader is in; the desktop top bar names the brief
before its step; 110% scale on windows 1500 px and wider. Pilot: repair/pilots/nav/make_pilot.py (same changes)."""
import json, os, re, sys
WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import read_page, briefs
s = read_page(os.path.join(WS, 'index.html'))
E = []
GROUPS = [('Psychosis and mood', ['psychosis-duration', 'voices', 'sz-psychosocial', 'bipolar-mania', 'mdd']),
          ('Anxiety, somatic and sexual', ['panic', 'somatic', 'gppd']),
          ('Cognition, substances and medical causes', ['delirium', 'substance', 'psych-medical']),
          ('Child and adolescent', ['disruptive-behavior']),
          ('Medications', ['ssri-effects', 'antipsych-effects', 'lithium-effects']),
          ('Safety and violence', ['suicide-risk', 'ipv'])]
order = [i for _, ids in GROUPS for i in ids]
for a, b in zip(order, order[1:]):
    E.append({'op': 'move_brief', 'brief': b, 'after': a, 'note': 'Psychiatry page order by disorder family'})
# sidebar list
j = s.find('<div id="navlinks">'); nav = s[j:s.find('</aside>', j)]
link = {m.group(1): m.group(0) for m in re.finditer(r'<a(?: class="[^"]*")? href="#([\w-]+)">[^<]*</a>', nav)}
title = {m.group(1): m.group(2) for m in re.finditer(r'<a(?: class="[^"]*")? href="#([\w-]+)">([^<]*)</a>', nav)}
hubs = [b.id for b in briefs(s) if b.attrs.get('data-entry') == 'hub']
pres = '<div id="navlinks">\n\n    <div class="sect">Presentations <span class="count">%d</span></div>\n' % len(hubs) + \
       ''.join('    <a href="#%s">%s</a>\n' % (h, title[h]) for h in hubs)
assert s.count('<div id="navlinks">\n') == 1
E.append({'op': 'replace_global', 'find': '<div id="navlinks">\n', 'with': pres, 'note': 'Presentations group: every hub'})
p0 = nav.find('<div class="sect">Psychiatry'); p1 = nav.find(link['suicide-risk']) + len(link['suicide-risk'])
old = nav[p0:p1]
head = old[:old.find('</div>') + 6]
new = head + ''.join('\n    <div class="navsub">%s</div>' % g + ''.join('\n    ' + link[i] for i in ids) for g, ids in GROUPS)
E.append({'op': 'replace_global', 'find': old, 'with': new, 'note': 'Psychiatry sidebar: six disorder-family groups'})
# sidebar component (axnav): two tiles per hub; the rail follows the row the reader is in
R = [('var list, groups = [], byId = {}, cur = {brief: null, step: -1}',
      'var tiles = {}, pref = null, curIt = null, list, groups = [], byId = {}, cur = {brief: null, step: -1}'),
     ('g.items.push(it); byId[id] = it;', 'g.items.push(it); (tiles[id] = tiles[id] || []).push(it); byId[id] = it;'),
     ("""  function setBrief(id){
    var it = byId[id], prev = cur.brief;
    if(prev && byId[prev]) byId[prev].el.removeAttribute('aria-current');
    cur.brief = id; cur.step = -1;
    if(!it){ drawRail(null); return; }
    it.el.setAttribute('aria-current', 'page');""",
      """  function setBrief(id){   // s146c: a hub has two tiles; the rail follows the tile clicked, else the row scrolled from, else the system tile
    var prev = cur.brief, all = tiles[id] || [], it = null;
    if(prev) (tiles[prev] || []).forEach(function(t){ t.el.removeAttribute('aria-current'); });
    if(pref && pref.id === id){ it = pref; pref = null; }
    else if(curIt){ all.forEach(function(t){ if(t.g === curIt.g) it = t; }); }
    if(!it) it = byId[id];
    cur.brief = id; cur.step = -1; curIt = it || null;
    if(!it){ drawRail(null); return; }
    all.forEach(function(t){ t.el.setAttribute('aria-current', 'page'); });"""),
     ("""    else { go(a.dataset.id); }""",
      """    else { var id = a.dataset.id; (tiles[id] || []).forEach(function(t){ if(t.el === a) pref = t; });
      if(cur.brief === id && pref && pref !== curIt){ cur.brief = null; setBrief(id); }
      go(id); }"""),
     # desktop top bar: the brief name before its step
     ("""bar.innerHTML = '<span class="axcur" aria-live="polite"><span class="axcn"></span><span class="axcl"></span></span>""",
      """bar.innerHTML = '<span class="axcur" aria-live="polite"><span class="axbn"></span><span class="axcn"></span><span class="axcl"></span></span>"""),
     ("""    cl.textContent = label || 'Step2Haki';""",
      """    cl.textContent = label || 'Step2Haki';
    var bn = bar.querySelector('.axbn'), hh = b ? b.querySelector('h4') : null, nm = hh ? hh.textContent.trim() : '';   // s146c
    bn.textContent = nm; bn.title = nm; bn.hidden = !nm || nm === label;"""),
     ('</head>', '<style id="ax-s146c">\n/* s146c: brief name in the desktop top bar; 110% scale on windows 1500 px and wider (Jonathan 2026-10-17) */\n'
      '#axbar .axcur{max-width:520px}\n#axbar .axbn{font:600 14px/1.2 var(--sans);color:var(--muted);white-space:nowrap;overflow:hidden;'
      'text-overflow:ellipsis;max-width:240px;padding-right:12px;margin-right:2px;border-right:1px solid var(--hair)}\n'
      '#axbar .axbn[hidden]{display:none}\n@media (min-width:1500px){html{zoom:1.1}}\n</style>\n</head>')]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    E.append({'op': 'replace_global', 'find': a, 'with': b})
json.dump({'edits': E}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '40_nav.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(E), 'edits; hubs', hubs)
