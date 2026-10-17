"""Pilot (not shipped): the live page with A (Presentations group of hubs) and B (Psychiatry disorder-family groups)."""
import re, sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def end_of(start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()

GROUPS = [('Psychosis and mood', ['psychosis-duration', 'voices', 'sz-psychosocial', 'bipolar-mania', 'mdd']),
          ('Anxiety, somatic and sexual', ['panic', 'somatic', 'gppd']),
          ('Cognition, substances and medical causes', ['delirium', 'substance', 'psych-medical']),
          ('Child and adolescent', ['disruptive-behavior']),
          ('Medications', ['ssri-effects', 'antipsych-effects', 'lithium-effects']),
          ('Safety and violence', ['suicide-risk', 'ipv'])]
order = [i for _, ids in GROUPS for i in ids]

# 1. reorder the psych briefs on the page (B)
spans = {}
for i in order:
    m = re.search(r'<div class="brief[^"]*" id="%s"' % re.escape(i), s)
    spans[i] = (m.start(), end_of(m.start()))
lo = min(a for a, b in spans.values()); hi = max(b for a, b in spans.values())
assert sorted(spans.values())[0][0] == lo
body = '\n\n'.join(s[a:b] for a, b in (spans[i] for i in order))
s = s[:lo] + body + s[hi:]

# 2. the sidebar source list
j = s.find('<div id="navlinks">'); k = end_of(j); nav = s[j:k]
link = {m.group(1): m.group(0) for m in re.finditer(r'<a(?: class="[^"]*")? href="#([\w-]+)">[^<]*</a>', nav)}
plain = {m.group(1): '<a href="#%s">%s</a>' % (m.group(1), m.group(2)) for m in re.finditer(r'<a(?: class="[^"]*")? href="#([\w-]+)">([^<]*)</a>', nav)}
# B: Psychiatry links regrouped under sub-labels
p0 = nav.find('<div class="sect">Psychiatry'); p1 = nav.find('</div>', nav.find('</div>', p0) + 6)  # end of sect div
sect_end = nav.find('</div>', p0) + 6
psy = ''.join('\n    <div class="navsub">%s</div>' % name + ''.join('\n    ' + link[i] for i in ids) for name, ids in GROUPS)
rest = nav[sect_end:]
last = rest.rfind('</div>')          # the closing tag of #navlinks
nav = nav[:sect_end] + psy + '\n\n' + rest[last:]
# A: Presentations group first; hubs in system order
hubs = re.findall(r'<div class="brief[^"]*" id="([\w-]+)"[^>]*data-entry="hub"', s) or []
hubs = [m.group(1) for m in re.finditer(r'<div class="brief[^"]*" id="([\w-]+)"([^>]*)>', s) if 'data-entry="hub"' in m.group(2)]
pres = '\n    <div class="sect">Presentations <span class="count">%d</span></div>' % len(hubs) + ''.join('\n    ' + plain[h] for h in hubs)
nav = nav.replace('<div id="navlinks">', '<div id="navlinks">\n' + pres + '\n', 1)
s = s[:j] + nav + s[k:]

# 3. the sidebar component: a hub has two tiles (Presentations and its system). The rail follows the row the reader is in:
#    the tile they clicked, else the tile in the group of the brief they scrolled from, else the system tile.
def sub(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)
sub('var list, groups = [], byId = {}, cur = {brief: null, step: -1}',
    'var tiles = {}, pref = null, curIt = null, list, groups = [], byId = {}, cur = {brief: null, step: -1}')
sub('g.items.push(it); byId[id] = it;', 'g.items.push(it); (tiles[id] = tiles[id] || []).push(it); byId[id] = it;')
sub("""  function setBrief(id){
    var it = byId[id], prev = cur.brief;
    if(prev && byId[prev]) byId[prev].el.removeAttribute('aria-current');
    cur.brief = id; cur.step = -1;
    if(!it){ drawRail(null); return; }
    it.el.setAttribute('aria-current', 'page');""",
"""  function setBrief(id){
    var prev = cur.brief, all = tiles[id] || [], it = null;
    if(prev) (tiles[prev] || []).forEach(function(t){ t.el.removeAttribute('aria-current'); });
    if(pref && pref.id === id){ it = pref; pref = null; }
    else if(curIt){ all.forEach(function(t){ if(t.g === curIt.g) it = t; }); }
    if(!it) it = byId[id];
    cur.brief = id; cur.step = -1; curIt = it || null;
    if(!it){ drawRail(null); return; }
    all.forEach(function(t){ t.el.setAttribute('aria-current', 'page'); });""")
sub("""    else { go(a.dataset.id); }""",
"""    else { var id = a.dataset.id; (tiles[id] || []).forEach(function(t){ if(t.el === a) pref = t; });
      if(cur.brief === id && pref && pref !== curIt){ cur.brief = null; setBrief(id); }
      go(id); }""")

# 4. option: the desktop top bar names the brief before its step
sub("""bar.innerHTML = '<span class="axcur" aria-live="polite"><span class="axcn"></span><span class="axcl"></span></span>""",
    """bar.innerHTML = '<span class="axcur" aria-live="polite"><span class="axbn"></span><span class="axcn"></span><span class="axcl"></span></span>""")
sub("""    cl.textContent = label || 'Step2Haki';""",
"""    cl.textContent = label || 'Step2Haki';
    var bn = bar.querySelector('.axbn'), hh = b ? b.querySelector('h4') : null, nm = hh ? hh.textContent.trim() : '';
    bn.textContent = nm; bn.title = nm; bn.hidden = !nm || nm === label;""")
css = ('<style id="ax-pilot-nav">#axbar .axcur{max-width:520px}'
       '#axbar .axbn{font:600 14px/1.2 var(--sans);color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:240px;'
       'padding-right:12px;margin-right:2px;border-right:1px solid var(--hair)}#axbar .axbn[hidden]{display:none}'
       '@media (min-width:1500px){html{zoom:1.1}}</style>')   # option: 110% on wide desktop windows, 100% below
s = s.replace('</head>', css + '</head>', 1)
s = s.replace('<title>', '<title>PILOT (not live): ', 1)
open(out, 'w', encoding='utf-8').write(s)
print('hubs', hubs); print('psych order', order)
