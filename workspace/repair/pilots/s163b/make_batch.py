#!/usr/bin/env python3
"""s163b generator (site layer plus tools, open-work cleanup; Jonathan 2026-11-05). Reads the live working page and
writes repair/s163b/10_site.json: replace_global ops only (page chrome: CSS and page script; no brief markup).

  python3 repair/pilots/s163b/make_batch.py [page]      (default workspace/index.html)

I1  in-brief rail: on a phone a step is current once its heading passes 32% of the window, as on desktop and in the
    sidebar (was 72 px, so the in-brief rail read one step behind the sidebar).
I2  drawer preview: a Differential row naming one row of the linked brief's step-2 window figure (figure.lcw) shows
    that row (title, window, bar, axis) as the criteria tile.
I3  drawer preview matcher: word forms (urinary tract infection = UTI, posttraumatic stress disorder = PTSD, major
    depressive disorder = depressive = depression, tuberculous = tuberculosis).
I4  system headings ("17 topics + 3 board-style") count the briefs shown, as the sidebar does.
I5  change log dialog and review panel fit the window under the 110% zoom of windows 1500 px and wider (the desktop
    drawer already divides by the zoom).
I6  window chart bars one step lighter (top tier --psy-e, middle tier between --psy2 and --psy-e).
I7  Pairs with list: shelf labels (Part I, Part II, Aquifer) before a title are dropped from the list rows, and an
    emphasized word that names no brief stays in the row's reason (an "Ask:" question, a bolded term) instead of
    becoming a row of its own. The original sentence stays in .qx-src.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PAGE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WS, 'index.html')
OUT = os.path.join(WS, 'repair', 's163b', '10_site.json')
h = open(PAGE, encoding='utf-8').read()


def between(a, b):
    i = h.index(a)
    j = h.index(b, i)
    return h[i:j]


ops = []


def op(find, new, note):
    assert h.count(find) == 1, (note, h.count(find), find[:80])
    ops.append({'op': 'replace_global', 'find': find, 'with': new, 'note': 's163b ' + note})


# ---- I1
op('var sth = wide ? Math.max(th + 8, vh * 0.32) : th + 8;',
   'var sth = Math.max(th + 8, vh * 0.32);   // s163b: the phone too, so the in-brief rail agrees with the sidebar (was th + 8 on a phone: one step behind)',
   'I1 phone in-brief rail reading line')

# ---- I4
op("function applyShelf(s){",
   """/* s163b (Jonathan 2026-11-05, "system heading counts made live"): one counter for the system headings. It counts the
   briefs each section shows, under the shelf, Board-style only, review and search filters, as the sidebar counts do
   (headerCounts counted every brief once at load, and wrote "topics" over Presentations' "complaints" and Psych
   Pharmacology's "18 of 18 class cards"). The form is read once from the heading as written: "N complaints" counts
   every brief; "N topics" splits topics, board-style and Aquifer; any other wording is left as written. On window,
   since this script is wrapped and headerCounts lives in another. */
window.axSysHeads=function(){
  document.querySelectorAll('h3.system').forEach(function(h){
    var n=h.querySelector('.n'); if(!n) return;
    if(!n.dataset.axForm){ var t=n.firstChild, m=t&&t.nodeType===3&&/^\\s*\\d+ (topic|complaint)s?\\b/.exec(t.nodeValue); n.dataset.axForm=m?m[1]:'fixed'; }
    if(n.dataset.axForm==='fixed') return;
    var c={topic:0,bs:0,aq:0}, sw=h.closest('.sectwrap')||h, el=sw.nextElementSibling;
    function add(b){ if(b.style.display==='none') return; c[(b.dataset.src==='aquifer'||b.classList.contains('aq'))?'aq':(b.classList.contains('bs')?'bs':'topic')]++; }
    while(el&&!el.classList.contains('sectwrap')&&!(el.tagName==='H3'&&el.classList.contains('system'))){
      if(el.classList.contains('brief')) add(el); else el.querySelectorAll('.brief').forEach(add);
      el=el.nextElementSibling;
    }
    var all=c.topic+c.bs+c.aq, out;
    if(n.dataset.axForm==='complaint') out=all+' complaint'+(all===1?'':'s');
    else out=c.topic+' topic'+(c.topic===1?'':'s')+(c.bs?' <span style="color:#9A5B0E">+ '+c.bs+' board-style</span>':'')+(c.aq?' <span style="color:#1F6A7E">+ '+c.aq+' Aquifer</span>':'');
    if(n.innerHTML!==out) n.innerHTML=out;
  });
};
function applyShelf(s){""", 'I4 live system heading counts (counter)')
op("  document.querySelectorAll('.bsband').forEach(function(bb){",
   "  window.axSysHeads();   // s163b: system headings follow the filters, as the sidebar does\n  document.querySelectorAll('.bsband').forEach(function(bb){",
   'I4 live system heading counts (on every filter change)')
op("function headerCounts(){",
   "function headerCounts(){\n  if(window.axSysHeads) return window.axSysHeads();   // s163b: one counter (axSysHeads, beside applyShelf)",
   'I4 live system heading counts (load)')

# ---- I5, I6 (CSS)
op('</head>', '''<style id="ax-s163b">
/* s163b I5: the change log and the review panel fit the window under the 110% zoom of windows 1500 px and wider
   (s146c zoom; the s161d sidebar fix by insets); their max-height was 100vh based and grew with the zoom */
@media (min-width:1500px){.axlog{max-height:calc((100vh - 48px) / 1.1)}#axrv{max-height:calc((100vh - 96px) / 1.1)}}
/* s163b I6: window chart bars one step lighter, so every tier reads pastel (STANDING: softer, pastel-leaning chart
   colors; s159 display review of pc-maoi); text and legend tokens unchanged */
.lcw .bar.c2,[data-theme="dark"] .lcw .bar.c2{background:color-mix(in srgb,var(--psy2) 45%,var(--psy-e))}
.lcw .bar.c3,[data-theme="dark"] .lcw .bar.c3{background:var(--psy-e)}
/* s163b I2: a window row in the drawer preview's criteria tile stacks (name and window above the bar) at every width,
   as on a phone; the desktop two-column row does not fit the 340 px tile */
.qx-pv .qx-pc figure.lcw .wax{grid-template-columns:1fr}.qx-pv .qx-pc figure.lcw .wsp{display:none}
.qx-pv .qx-pc figure.lcw .wr{display:block}
</style>
</head>''', 'I5 zoom-safe panels, I6 window chart palette')

# ---- I3
op('  function pvToks(s){\n    var o = [];\n    norm(s).toLowerCase()',
   '''  /* s163b I3: word forms the matcher should treat as one (a row says "UTI", the brief "Urinary Tract Infection") */
  var PV_SYN = [[/\\burinary tract infections?\\b/g, 'uti'], [/\\bpost-?traumatic stress disorder\\b/g, 'ptsd'],
    [/\\bmajor depressive disorder\\b/g, 'depression'], [/\\bdepressive\\b/g, 'depression'], [/\\btuberculous\\b/g, 'tuberculosis']];
  function pvSyn(s){ PV_SYN.forEach(function(p){ s = s.replace(p[0], p[1]); }); return s; }
  function pvToks(s){
    var o = [];
    pvSyn(norm(s).toLowerCase())''', 'I3 matcher word forms')

# ---- I2
old = between('  function pvCrit(link, t){', '  function pvTile(n){')
assert old.count("Array.prototype.forEach.call(t.querySelectorAll('h5.tsec, div.crit, div.sp-dx'), function(n){") == 1
new = old.replace("    var on = false, bl = [];", "    var on = false, bl = [], wins = [];") \
    .replace("Array.prototype.forEach.call(t.querySelectorAll('h5.tsec, div.crit, div.sp-dx'), function(n){\n"
             "      if(n.tagName === 'H5') on = n === h; else if(on && !n.parentElement.closest('div.crit, div.sp-dx')) bl.push(n);",
             "Array.prototype.forEach.call(t.querySelectorAll('h5.tsec, div.crit, div.sp-dx, figure.lcw'), function(n){\n"
             "      if(n.tagName === 'H5') on = n === h;\n"
             "      else if(on && !n.parentElement.closest('div.crit, div.sp-dx, figure.lcw')) (n.tagName === 'FIGURE' ? wins : bl).push(n);") \
    .replace("    if(!bl.length) return null;", "    if(!bl.length && !wins.length) return null;") \
    .replace("    var tt = pvToks(",
             "    /* s163b I2: a window figure's row that names the row's diagnosis in full (a broader row such as \"Psychotic\n"
             "       disorder\" names none, so it gets no tile) */\n"
             "    for(var f = 0; f < wins.length; f++){\n"
             "      var wr = wins[f].querySelectorAll('li.wr');\n"
             "      for(var r = 0; r < wr.length; r++){ var nm = wr[r].querySelector('.nm'); if(nm && pvIn(pvToks(pvTxt(nm).replace(/\\([^)]*\\)/g, ' ')), all)) return {fig: wins[f], row: wr[r]}; }\n"
             "    }\n"
             "    var tt = pvToks(") \
    .replace("return pvIn(tt, all) || pvIn(core, tt) ? bl[0] : null;", "return bl.length && (pvIn(tt, all) || pvIn(core, tt)) ? bl[0] : null;")
assert new.count('wins') >= 5 and 'bl.length && (pvIn' in new
op(old, new, 'I2 window figure rows in the preview (match)')
op('    var c = n.cloneNode(true);',
   '''    var c = n.fig ? pvWin(n) : n.cloneNode(true);''', 'I2 window figure rows in the preview (tile)')
op('  function pvTile(n){',
   '''  // s163b I2: a name's text without the Recall reveal button's label
  function pvTxt(n){ var c = n.cloneNode(true); c.querySelectorAll('.mask-toggle').forEach(function(x){ x.remove(); }); return norm(c.textContent); }
  // s163b I2: the window figure cut to its title and the one row the Differential row names
  function pvWin(m){
    var c = m.fig.cloneNode(true), k = Array.prototype.indexOf.call(m.fig.querySelectorAll('li.wr'), m.row);
    Array.prototype.forEach.call(c.querySelectorAll('li.wr'), function(r, j){ if(j !== k) r.remove(); });
    Array.prototype.forEach.call(c.querySelectorAll('li.wg, figcaption, .lc-key'), function(x){ x.remove(); });
    return c;
  }
  function pvTile(n){''', 'I2 window figure rows in the preview (cut)')

# ---- I7
old = between('  function pairs(pb){', '    if(!items.length || items.bad) return;')
assert old.count("if(n.nodeType === 1 && /^(I|B|EM|A)$/.test(n.tagName)){") == 1
new = old.replace("    var items = [], cur = null;",
                  "    var items = [], cur = null, lead = '', T0 = titles();\n"
                  "    /* s163b I7: a shelf label before a title (Part I, Part II, Aquifer) is not part of a row, and an emphasized\n"
                  "       word that names no brief (an \"Ask:\" question, a bolded term) stays in the row's reason */\n"
                  "    var SHELF = /(^|[\\s.;,])(?:Part I{1,2}|Aquifer)\\s*$/, CONJ = /(,\\s*|\\s+)(?:and|or)\\s*$/;") \
    .replace("      if(n.nodeType === 1 && /^(I|B|EM|A)$/.test(n.tagName)){ cur = {",
             "      if(n.nodeType === 1 && /^(I|B|EM|A)$/.test(n.tagName)){\n"
             "        if(cur && n.tagName !== 'A' && !T0[key(n.textContent)]){ cur.why += n.textContent; return; }\n"
             "        if(cur) cur.why = cur.why.replace(SHELF, '$1').replace(CONJ, '');\n"
             "        else if(lead && !norm(lead.replace(SHELF, ''))) lead = '';\n"
             "        cur = {") \
    .replace("      if(cur) cur.why += n.textContent; else if(norm(n.textContent)) items.bad = 1;",
             "      if(cur) cur.why += n.textContent; else lead += n.textContent;")
new = new.rstrip('\n') + "\n    if(norm(lead)) items.bad = 1;\n"
assert 'T0[key(' in new and 'lead += n.textContent' in new
op(old, new, 'I7 Pairs with rows')

json.dump({'edits': ops}, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
open(OUT, 'a').write('\n')
print('s163b make_batch: %d ops -> %s' % (len(ops), os.path.relpath(OUT, WS)))
