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

# 3. the sidebar component: a brief may have two tiles (Presentations and its system); both mark current
old = 'g.items.push(it); byId[id] = it;'
new = 'g.items.push(it); if(byId[id]){ (byId[id].dup = byId[id].dup || []).push(it); } else byId[id] = it;'
assert s.count(old) == 1; s = s.replace(old, new)
old = "if(prev && byId[prev]) byId[prev].el.removeAttribute('aria-current');"
new = "if(prev && byId[prev]){ byId[prev].el.removeAttribute('aria-current'); (byId[prev].dup || []).forEach(function(d){ d.el.removeAttribute('aria-current'); }); }"
assert s.count(old) == 1; s = s.replace(old, new)
old = "it.el.setAttribute('aria-current', 'page');"
new = "it.el.setAttribute('aria-current', 'page'); (it.dup || []).forEach(function(d){ d.el.setAttribute('aria-current', 'page'); });"
assert s.count(old) == 1; s = s.replace(old, new)
s = s.replace('<title>', '<title>PILOT (not live): ', 1)
open(out, 'w', encoding='utf-8').write(s)
print('hubs', hubs); print('psych order', order)
