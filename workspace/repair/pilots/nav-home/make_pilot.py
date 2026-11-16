"""Pilot (not shipped), s161b candidate: one home per brief in the sidebar (2026-11-03).
A brief listed under Presentations and under its system has one home, its system tile: the step rail always sits there and
only that tile is current. The Presentations tile is marked (a dot), never current. A group the sidebar opened itself
closes when the reader moves to a brief in another group, with the list held still. The old s141 nesting stops moving the
brief's rail into the hidden old list once the s143 sidebar is on the page. Presentation only: no text changes.
Usage: python3 make_pilot.py <live index.html> <out.html>
repair/s161b/gen_nav_home.py runs this file to collect the same replacements (PAIRS) as replace_global edits."""
import sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
PAIRS = []

def sub(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)
    PAIRS.append((old, new))

# 1. the rail always follows the home tile (byId keeps the last tile, the system one; Presentations-only briefs keep theirs)
sub("""  function setBrief(id){   // s146c: a hub has two tiles; the rail follows the tile clicked, else the row scrolled from, else the system tile
    var prev = cur.brief, all = tiles[id] || [], it = null;
    if(prev) (tiles[prev] || []).forEach(function(t){ t.el.removeAttribute('aria-current'); });
    if(pref && pref.id === id){ it = pref; pref = null; }
    else if(curIt){ all.forEach(function(t){ if(t.g === curIt.g) it = t; }); }
    if(!it) it = byId[id];
    cur.brief = id; cur.step = -1; curIt = it || null;
    if(!it){ drawRail(null); return; }
    all.forEach(function(t){ t.el.setAttribute('aria-current', 'page'); });
    if(it.g.btn.getAttribute('aria-expanded') !== 'true') fold(it.g, true, false);
    drawRail(it);
    keep(it.el, !!prev, true);
  }""",
"""  function setBrief(id){   // s161b (2026-11-03): the rail always sits under the home tile (the system tile; a
                           // Presentations-only brief's home is its Presentations tile); the other tile is marked, never current (was s146c: the
                           // rail followed the tile clicked or the row scrolled from, so it hopped between groups and depended on scroll direction)
    var prev = cur.brief, all = tiles[id] || [], it = byId[id] || null, s = scroller();
    if(prev) (tiles[prev] || []).forEach(function(t){ t.el.removeAttribute('aria-current'); t.el.removeAttribute('data-also'); });
    cur.brief = id; cur.step = -1; curIt = it;
    if(!it){ drawRail(null); return; }
    all.forEach(function(t){ if(t === it) t.el.setAttribute('aria-current', 'page'); else { t.el.setAttribute('data-also', ''); if(stay) stay = t.el; } });
    if(it.g.btn.getAttribute('aria-expanded') !== 'true'){ fold(it.g, true, false); it.g.auto = true; }
    drawRail(it);
    // a group the sidebar opened itself closes once the current brief lives elsewhere; the list is held still while it closes
    groups.forEach(function(g){
      if(!g.auto || g === it.g) return;
      var at = stay || it.el, y0 = at.getBoundingClientRect().top;
      fold(g, false, false); g.auto = false;
      if(s) s.scrollTop += at.getBoundingClientRect().top - y0;
    });
    keep(it.el, !!prev, true);
  }""")

# 2. a group the reader folds or unfolds by hand is theirs: the sidebar never closes it
sub("b.addEventListener('click', function(gg){ return function(){ fold(gg, gg.btn.getAttribute('aria-expanded') !== 'true', true); }; }(g));",
    "b.addEventListener('click', function(gg){ return function(){ gg.auto = false; fold(gg, gg.btn.getAttribute('aria-expanded') !== 'true', true); }; }(g));")

# 3. a click on either tile goes to the brief; the rail stays home
sub("""    else { var id = a.dataset.id; (tiles[id] || []).forEach(function(t){ if(t.el === a) pref = t; });
      if(cur.brief === id && pref && pref !== curIt){ cur.brief = null; setBrief(id); }
      go(id); }""",
"""    else { var id = a.dataset.id;
      stay = byId[id] && byId[id].el !== a ? a : null;   // s161b r2: a click in Presentations keeps the sidebar there
      if(cur.brief === id && byId[id]) keep(byId[id].el, true, true);   // s161b: already current, so bring its home tile (or, browsing, this tile) into view
      go(id); }""")

# 4. the marked (second) tile
sub("""#axn a.axn-b[aria-current="page"]{""",
"""#axn a.axn-b[data-also]{position:relative;font-weight:600}
#axn a.axn-b[data-also]::before{content:"";position:absolute;left:17px;top:50%;width:6px;height:6px;margin-top:-3px;border-radius:50%;background:var(--accent)}
#axn a.axn-b[aria-current="page"]{""")

# 5. the s141 nesting no longer moves the brief's rail into the hidden old list once the s143 sidebar is on
sub("""    document.body.classList.toggle('ax-nest', WIDE.matches);
    if(!WIDE.matches){ putBack(); return; }""",
"""    document.body.classList.toggle('ax-nest', WIDE.matches);
    if(!WIDE.matches || window.AXN){ putBack(); return; }   // s161b: the s143 sidebar draws its own rail""")


# 6. r2 (2026-11-03): browsing from Presentations keeps the sidebar on
#    Presentations. A click on a Presentations tile sets stay; while it is set the sidebar never scrolls toward the home
#    rail, and it follows the current brief's Presentations tile (the dot) when there is one. A click on a system tile or
#    a step ends it. The rail stays home under the system tile throughout.
sub("var tiles = {}, pref = null, curIt = null,", "var tiles = {}, pref = null, curIt = null, stay = null,")
sub("""  function keep(n, smooth, top){
    var s = scroller(); if(!s || !n || nav.classList.contains('sxon')) return;""",
"""  function keep(n, smooth, top){
    if(stay){ if(!top) return; n = stay; }   // s161b r2: browsing Presentations, follow its tile, not the rail
    var s = scroller(); if(!s || !n || nav.classList.contains('sxon')) return;""")
sub("""    if(a.classList.contains('axn-s')) go(a.getAttribute('href').slice(1), +a.dataset.i);""",
"""    if(a.classList.contains('axn-s')){ stay = null; go(a.getAttribute('href').slice(1), +a.dataset.i); }""")

# 7. r5 (2026-11-03; r4's subtitle
#    switcher: "no it should be more obvious tbf"): a shelf card sits between the brand row and the search, always shown:
#    an accent book icon, a small "Shelf" label over the shelf name in bold, and a chevron. The page's shelf <select> lies
#    invisibly over the card, so the system picker opens and every shelf script keeps working. It leaves the sheet.
#    r6 ("search bar should be on top"): the card sits under the search pill.
sub("""  /* ---------- the display sheet ---------- */""",
"""  /* s161b r5: the shelf card; the shelf <select> lies invisibly over it */
  var SVG_SHELF = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 2.5v9.5M6 2.5v9.5M9.2 3.2l2.6 8.8M1.5 14h13" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"></path></svg>';
  var SVG_DOWN = '<svg width="12" height="8" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg>';
  function shelfCard(before, sel){   // before: the search pill, which stays on top
    var row = el('div', 'axn-shelfrow');
    row.appendChild(el('span', 'ic', SVG_SHELF));
    var t = el('span', 'tx'); t.appendChild(el('span', 'k')).textContent = 'Shelf'; var v = t.appendChild(el('span', 'v')); row.appendChild(t);
    row.appendChild(el('span', 'ch', SVG_DOWN)); row.appendChild(sel);
    before.parentNode.insertBefore(row, before.nextSibling);   // r6: under the search
    function show(){ var o = sel.options[sel.selectedIndex]; v.textContent = o ? txt(o).replace(/\\s+\\u2013\\s+soon$/, '') : 'Step 2'; }
    sel.addEventListener('change', function(){ setTimeout(show, 0); });
    document.addEventListener('ax-shelf', show); show();
  }

  /* ---------- the display sheet ---------- */""")
sub("""      if(sp && sp.parentNode !== s) s.appendChild(sp);""",
"""      var pl = nav.querySelector('.axn-srch'), ss = sp && sp.querySelector('select');   // s161b r5: the shelf picker is a card under the search, not a sheet row
      if(ss && pl && !nav.querySelector('.axn-shelfrow')) shelfCard(pl, ss);""")
sub("""#nav.axn .axn-sub{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}""",
"""#nav.axn .axn-sub{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#nav.axn{--axn-shelf-line:rgba(24,28,30,.09)}
[data-theme="dark"] #nav.axn{--axn-shelf-line:rgba(255,255,255,.09)}
#nav.axn .axn-shelfrow{position:relative;display:grid;grid-template-columns:32px minmax(0,1fr) auto;align-items:center;gap:10px;margin:0 14px 10px;padding:7px 14px 7px 7px;border-radius:14px;background:var(--axn-tile);box-shadow:0 1px 3px rgba(0,0,0,.08),inset 0 0 0 1px var(--axn-shelf-line);cursor:pointer;transition:box-shadow .2s ease}
#nav.axn .axn-shelfrow:hover{box-shadow:0 2px 8px rgba(0,0,0,.10),inset 0 0 0 1px rgba(var(--acc-rgb),.35)}
#nav.axn .axn-shelfrow:focus-within{box-shadow:0 1px 3px rgba(0,0,0,.08),inset 0 0 0 1.5px rgba(var(--acc-rgb),.6)}
#nav.axn .axn-shelfrow .ic{display:flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:10px;background:rgba(var(--acc-rgb),.14);color:var(--accent)}
#nav.axn .axn-shelfrow .tx{display:flex;flex-direction:column;gap:1px;min-width:0}
#nav.axn .axn-shelfrow .k{font:600 10.5px/1.2 var(--sans);letter-spacing:.7px;text-transform:uppercase;color:var(--axn-mute)}
#nav.axn .axn-shelfrow .v{font:700 15px/1.25 var(--sans);color:var(--axn-ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#nav.axn .axn-shelfrow .ch{display:flex;color:var(--axn-mute)}
#nav.axn .axn-shelfrow select{position:absolute;inset:0;width:100%;height:100%;margin:0;padding:0;border:0;border-radius:14px;opacity:0;cursor:pointer;font-size:16px;-webkit-appearance:none;appearance:none;background:none;box-shadow:none}""")

# 8. r3 (2026-11-03): the flat theme is on unless the reader has
#    turned it off (a stored '0' keeps sculpted).
sub("""  if(localStorage.getItem('ax-flat')==='1') b.classList.add('flat');""",
"""  if(localStorage.getItem('ax-flat')!=='0') b.classList.add('flat');   // s161b r3: flat is the default""")
open(out, 'w', encoding='utf-8').write(s)
print('pilot written', out)
