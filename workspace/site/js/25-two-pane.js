/* Two-pane (desktop only, 1101 px and wider). The current brief alone, in screen-tall pages of two columns, read down
   the left column, then the right, then the next page. The brief's own nodes move into the pages and move back when
   the reader returns to Scrolling or opens another brief; the only added text is "<step>, continued" over a part that
   carries on from the column before. A block taller than a third of a column may continue in the next column between
   its rows (a table repeats its header); the question card never splits. Each page ends under its longer column.
   The sidebar collapses to a rail of shelf sections: Expand pushes the brief over (kept until collapsed), a section
   opens its briefs in a panel over the page, Search opens the sidebar over the page.
   Settings: layout ('scroll' or 'two'), twonav ('1' while the sidebar is kept expanded).
   Events: emits nav:ask, nav:search, layout:step; listens to nav:sections, nav:collapse. */
return (function(){
'use strict';
var WIDE = window.matchMedia('(min-width:1101px)');
var root = document.documentElement;
var want = AX.settings.get('layout') === 'two';
var B = null, S = null, rail = null, fly = null, flyFor = null, tip = null, secs = [], ctl = null, offs = [], lastStep = null;
var HEAD = '.bb-bar,.bb-rail,.alias,h4,.sub,nav';
var WHOLE = 'tr,p,dd,dt,h1,h2,h3,h4,h5,h6,caption,thead,.mcq,.mcqwrap,svg,img,canvas,a,b,i,em,strong,span,button,label';   // never cut inside
var GAP = 12, BREAK = 0.3;
var ICON_EXPAND = '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 4h9M2 9h6M2 14h9M12 6.5 15 9l-3 2.5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"></path></svg>';
var ICON_SEARCH = '<svg width="17" height="17" viewBox="0 0 17 17" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.7"></circle><path d="m11 11 4 4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"></path></svg>';
var SHORT = {'Presentations': 'Pres', 'Musculoskeletal': 'MSK', 'Pediatrics': 'Peds', 'Cardiovascular': 'CV', 'Pulmonary': 'Pulm',
  'GI & Hepatology': 'GI', 'Renal & GU': 'Renal', 'Endocrine & Bone': 'Endo', 'Hematology': 'Heme', 'Infectious Disease': 'ID',
  'Neuro & HEENT': 'Neuro', 'Neurology': 'Neuro', 'Dermatology & Wounds': 'Derm', 'Dermatology': 'Derm', 'OB / GYN': 'OB',
  'Obstetrics & Gynecology': 'OB', 'Preventive & Ethics': 'Prev', 'Psychiatry & Behavioral Health': 'Psych',
  'Psychiatry': 'Psych', 'Psych Pharmacology': 'Pharm'};

function el(tag, cls, html){ var e = document.createElement(tag); if(cls) e.className = cls; if(html != null) e.innerHTML = html; return e; }
function txt(n){ return (n && n.textContent || '').replace(/\s+/g, ' ').trim(); }
function each(list, fn){ Array.prototype.forEach.call(list, fn); }
function on(){ return want && WIDE.matches; }
function zoomOf(n){ return (n.getBoundingClientRect().width / n.offsetWidth) || 1; }
function jump(y){ window.scrollTo({top: y, behavior: 'instant'}); }
function barBottom(){ var b = document.getElementById('axbar'); return b && b.offsetParent !== null ? b.getBoundingClientRect().bottom : 16; }

/* ---------- which brief ---------- */
function briefOf(x){ return x && x.closest ? x.closest('main .wrap > .brief') : null; }
function inView(){
  var y = window.innerHeight * 0.32, last = null;
  each(document.querySelectorAll('main .wrap > .brief'), function(b){ if(b.offsetParent !== null && b.getBoundingClientRect().top < y) last = b; });
  return last;
}
function fromHash(){
  var id = location.hash.slice(1); try{ id = decodeURIComponent(id); }catch(e){}
  var t = id ? AX.brief.ensure(id) : null;
  return t ? (t.classList && t.classList.contains('brief') ? t : briefOf(t)) : null;
}

/* ---------- units: the brief's steps (a heading and what follows it), blocks that stand alone, and the practice set ---------- */
function unit(name, cls){ var u = el('section', 'ax2-u' + (cls ? ' ' + cls : '')); u.dataset.name = name || ''; return u; }
function build(){
  if(S || !B) return;
  AX.brief.ensure(B);
  var nodes = Array.prototype.slice.call(B.childNodes), kids = Array.prototype.slice.call(B.children), units = [], end = [], cur = null, prac = null, started = false;
  kids.forEach(function(c){
    if(!started && c.matches(HEAD)) return;
    started = true;
    if(c.matches('.bb-end')){ end.push(c); return; }
    if(c.matches('h5.authored-hdr')){ prac = cur = unit(txt(c), 'ax2-prac'); units.push(prac); }
    else if(!prac && c.matches('h5')){ cur = unit(txt(c).replace(/^\d+\s*/, '')); cur.dataset.hid = c.id || ''; units.push(cur); }
    else if(!cur){ var u = unit(''); u.appendChild(c); units.push(u); return; }
    cur.appendChild(c);
  });
  var flow = el('div', 'ax2-flow');
  B.insertBefore(flow, end[0] || null);
  S = {nodes: nodes, units: units, flow: flow, undo: [], pages: []};
  B.classList.add('ax2-cur');
  root.setAttribute('data-layout', 'two');
  root.classList.toggle('ax2-nav', AX.settings.get('twonav') === '1');
  lay(true);
  setTimeout(function(){ if(S) lay(); }, 700);   // parts that size themselves after they are drawn
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ if(S) lay(); });
}
function unbuild(){
  if(!S) return;
  restore();
  S.nodes.forEach(function(c){ B.appendChild(c); });
  S.flow.remove(); S = null;
  B.classList.remove('ax2-cur');
  root.removeAttribute('data-layout'); root.classList.remove('ax2-nav', 'ax2-over');
  closeFly(); lastStep = null;
}

/* ---------- pages ---------- */
function where(e, R){
  var rs = e.getClientRects(), inn = false, out = false;
  for(var i = 0; i < rs.length; i++){ var r = rs[i]; if(!r.width && !r.height) continue; if(r.left >= R - 1) out = true; else inn = true; }
  return out ? (inn ? 'straddle' : 'out') : 'in';
}
function shallow(e){
  var c = e.cloneNode(false); c.removeAttribute('id');
  if(e.matches('figure.w5a')) c.style.counterReset = 'axz ' + e.querySelectorAll(':scope > .w5z').length;   // zone numbers keep counting
  if(e.classList.contains('ax2-u') && e.dataset.name){ var lab = el('p', 'ax2-cont'); lab.textContent = e.dataset.name + ', continued'; c.appendChild(lab); }
  if(e.tagName === 'TABLE'){
    var th = e.querySelector(':scope > thead');
    if(th){ var t2 = th.cloneNode(true); t2.setAttribute('aria-hidden', 'true'); each(t2.querySelectorAll('[id]'), function(x){ x.removeAttribute('id'); }); c.appendChild(t2); }
  }
  return c;
}
// what lies past the column's right edge R moves, inside a copy of each container around it, to the next page.
// ALL: nothing of the box would stay (or only its heading or caption), so the box moves whole
var ALL = {};
var LABEL = 'h5,h6,caption,thead,.ttl,.lbl,.kick,.wg,.w5z,.ax2-cont';
function cut(box, R){
  var kids = Array.prototype.slice.call(box.children);
  for(var i = 0; i < kids.length; i++){
    var w = where(kids[i], R); if(w === 'in') continue;
    var from = i, sub = null;
    if(w === 'straddle' && kids[i].firstElementChild && !kids[i].matches(WHOLE)){ sub = cut(kids[i], R); if(sub && sub !== ALL) from = i + 1; }
    var keep = false;
    for(var q = 0; q < from && !keep; q++) if(!kids[q].matches(LABEL)) keep = true;
    if(!keep && !(sub && sub !== ALL)) return ALL;
    var clone = shallow(box), moved = [];
    box.classList.add('ax2-open-b'); clone.classList.add('ax2-open-t');   // the cut edges read as open
    if(sub && sub !== ALL) clone.appendChild(sub);
    var nodes = Array.prototype.slice.call(box.childNodes), at = from < kids.length ? nodes.indexOf(kids[from]) : nodes.length;
    for(var j = at; j < nodes.length; j++){ clone.appendChild(nodes[j]); moved.push(nodes[j]); }
    S.undo.push({from: box, moved: moved, clone: clone});
    return clone;
  }
  return null;
}
function restore(){
  if(!S) return;
  for(var k = S.undo.length - 1; k >= 0; k--){ var u = S.undo[k]; u.from.classList.remove('ax2-open-b'); u.moved.forEach(function(n){ u.from.appendChild(n); }); if(u.clone.parentNode) u.clone.parentNode.removeChild(u.clone); }
  S.undo = [];
  each(S.flow.querySelectorAll('.ax2-brk'), function(x){ x.classList.remove('ax2-brk'); });
  S.units.forEach(function(u){ S.flow.appendChild(u); });
  each(S.flow.querySelectorAll('.ax2-page'), function(p){ p.remove(); });
}
// a block taller than lim may continue in the next column between its parts; its parts are checked the same way
function breakable(b, k, lim){
  if(b.matches(WHOLE) || b.getBoundingClientRect().height / k <= lim) return;
  b.classList.add('ax2-brk');
  each(b.children, function(c){ breakable(c, k, lim); });
}
// how far down a column its content reaches, in window px
function used(col){
  var top = col.getBoundingClientRect().top, bottom = top;
  each(col.querySelectorAll(':scope > .ax2-u > :not(.ax2-cont)'), function(u){ each(u.getClientRects(), function(r){ if(r.height && r.bottom > bottom) bottom = r.bottom; }); });
  return bottom - top;
}
// the page ends right under its longer column
function fitHeight(L, Rc, k){
  if(L.classList.contains('ax2-hold') || Rc.classList.contains('ax2-hold')){ L.style.height = Rc.style.height = ''; return; }
  var old = L.style.height, h = (Math.max(used(L), used(Rc)) / k + 4) + 'px';
  L.style.height = Rc.style.height = h;
  var bad = false;
  [L, Rc].forEach(function(c){ var R = c.getBoundingClientRect().right; each(c.children, function(u){ if(where(u, R) !== 'in') bad = true; }); });
  if(bad) L.style.height = Rc.style.height = old;
}
// one column: the units go in; what runs past its right edge is cut off and returned for the next column
function fill(col, rest, k, H){
  rest.forEach(function(u){ col.appendChild(u); });
  each(col.querySelectorAll(':scope > .ax2-u:not(.ax2-prac) > *'), function(b){ breakable(b, k, H * BREAK); });
  var R = col.getBoundingClientRect().right, nxt = [], carry = null;
  for(var i = 0; i < rest.length; i++){
    var w = where(rest[i], R); if(w === 'in') continue;
    if(w === 'straddle'){ carry = cut(rest[i], R); if(carry === ALL){ carry = null; nxt = rest.slice(i); } else nxt = rest.slice(i + 1); }
    else nxt = rest.slice(i);
    break;
  }
  nxt.forEach(function(u){ if(u.parentNode === col) col.removeChild(u); });
  return carry ? [carry].concat(nxt) : nxt;
}
// a column where nothing fit (one block taller than a page that cannot be cut) holds the rest at its full length
function hold(col, rest){ rest.forEach(function(u){ col.appendChild(u); }); col.style.height = ''; col.classList.add('ax2-hold'); }
function paginate(){
  restore();
  S.units.forEach(function(u){ u.remove(); });   // out of the flow while the first page is measured
  var f = S.flow, vh = window.innerHeight, barB = barBottom(), rest = S.units.slice(), n = 0, pages = [];
  while(rest.length && n < 60){
    var pg = el('div', 'ax2-page'), cc = el('div', 'ax2-cols'), L = el('div', 'ax2-col'), Rc = el('div', 'ax2-col');
    cc.appendChild(L); cc.appendChild(Rc); pg.appendChild(cc); f.appendChild(pg); pages.push(pg);
    var k = zoomOf(L);
    var top = n ? barB + GAP + 2 * 16 * k : L.getBoundingClientRect().top;   // a later page starts under the toolbar, after the rule above it
    var H = Math.max(320, (vh - top - 20) / k);
    L.style.height = Rc.style.height = H + 'px';
    var left = fill(L, rest, k, H);
    if(left.length && (used(L) < 60 || n >= 59)){ hold(L, left); left = []; }
    rest = left.length ? fill(Rc, left, k, H) : [];
    if(rest.length && (used(Rc) < 60 || n >= 59)){ hold(Rc, rest); rest = []; }
    fitHeight(L, Rc, k);
    n++;
  }
  S.pages = pages;
}

/* ---------- frame: where the brief starts, how wide the title may run ---------- */
function frame(){
  var m = document.querySelector('main'), mz = m ? zoomOf(m) : 1;
  var left = 0, nav = document.getElementById('nav');
  if(root.classList.contains('ax2-nav') && nav){
    left = ((parseFloat(getComputedStyle(nav).left) || 16) + nav.offsetWidth) * zoomOf(nav);
  } else if(rail) left = (parseFloat(getComputedStyle(rail).left) + rail.offsetWidth) * zoomOf(rail);
  root.style.setProperty('--ax2-left', ((left + 28) / mz) + 'px');
  var bar = document.getElementById('axbar'), h = B.querySelector(':scope > h4');
  if(bar && h){ var room = bar.getBoundingClientRect().left - h.getBoundingClientRect().left - 24; root.style.setProperty('--ax2-tw', (room > 240 ? room / zoomOf(h) : 2000) + 'px'); }
}

function lay(first){
  if(!S) return;
  var pi = first ? 0 : pageInView();
  jump(0);
  frame(); paginate();
  if(pi > 0 && S.pages[pi]) seatPage(S.pages[pi]); else jump(0);
  mark();
}
function pageInView(){
  if(!S) return 0;
  var y = barBottom() + 40, at = 0;
  S.pages.forEach(function(p, i){ if(p.getBoundingClientRect().top <= y) at = i; });
  return at;
}
function seatPage(p){ jump(window.scrollY + p.getBoundingClientRect().top - (barBottom() + GAP)); }

/* the step at the top of the page in view: the sidebar's step rail marks it */
function mark(){
  if(!S || !S.pages.length) return;
  var p = S.pages[pageInView()], u = p && p.querySelector('.ax2-u'), id = null;
  for(var x = u; x && !id; x = x.nextElementSibling) if(x.classList.contains('ax2-u')) id = x.dataset.hid || null;
  if(id !== lastStep){ lastStep = id; AX.emit('layout:step', id); }
}

/* where a link lands: the page that holds the target, under the toolbar; the brief's own top for the brief or page 1 */
AX.setLanding(function(t){
  if(!S || !B.contains(t) && t !== B) return null;
  var p = t === B ? null : t.closest('.ax2-page');
  if(!p || p === S.pages[0]) return {el: B, top: 0};
  return {el: p, top: barBottom() + GAP};
});

/* ---------- the rail ---------- */
function makeRail(){
  if(rail) return;
  rail = el('nav'); rail.id = 'ax2rail'; rail.setAttribute('aria-label', 'Sidebar, collapsed');
  document.body.appendChild(rail);
  tip = el('div'); tip.id = 'ax2tip'; tip.hidden = true; tip.setAttribute('role', 'tooltip'); document.body.appendChild(tip);
  function show(b){
    var t = b && b.getAttribute('data-tip'); if(!t || (fly && flyFor === b)){ tip.hidden = true; return; }
    var z = zoomOf(rail), r = b.getBoundingClientRect();
    tip.textContent = t; tip.style.top = ((r.top + r.height / 2) / z) + 'px'; tip.hidden = false;
  }
  rail.addEventListener('mouseover', function(e){ show(e.target.closest('button')); });
  rail.addEventListener('mouseleave', function(){ tip.hidden = true; });
  rail.addEventListener('focusin', function(e){ show(e.target.closest('button')); });
  rail.addEventListener('focusout', function(){ tip.hidden = true; });
  rail.addEventListener('click', function(e){
    var b = e.target.closest('button'); if(!b) return;
    tip.hidden = true;
    if(b.classList.contains('ex')) expand(true);
    else if(b.classList.contains('sr')) over();
    else if(b.classList.contains('sec')) openFly(b);
  });
  drawRail();
}
function drawRail(){
  if(!rail) return;
  rail.innerHTML = '<button type="button" class="ex tool" aria-label="Expand sidebar" data-tip="Expand sidebar">' + ICON_EXPAND + '</button>' +
                   '<button type="button" class="sr" aria-label="Search" data-tip="Search">' + ICON_SEARCH + '</button><span class="hr" aria-hidden="true"></span>';
  secs.forEach(function(sc, i){
    var b = el('button', 'sec'); b.type = 'button'; b.dataset.i = i;
    b.textContent = SHORT[sc.name] || sc.name.split(/[\s&\/]+/)[0].slice(0, 5);
    b.setAttribute('data-tip', sc.name + (sc.count ? '  ·  ' + sc.count : ''));
    b.setAttribute('aria-label', sc.name); b.setAttribute('aria-haspopup', 'dialog'); b.setAttribute('aria-expanded', 'false');
    rail.appendChild(b);
  });
  paintRail();
}
// the current brief's home section: the first section listing it, Presentations last
function paintRail(){
  if(!rail || !B) return;
  var home = -1;
  secs.forEach(function(sc, i){ if(home < 0 && sc.name !== 'Presentations' && sc.items.some(function(it){ return it.id === B.id; })) home = i; });
  if(home < 0) secs.forEach(function(sc, i){ if(home < 0 && sc.items.some(function(it){ return it.id === B.id; })) home = i; });
  each(rail.querySelectorAll('.sec'), function(b){ b.classList.toggle('home', +b.dataset.i === home); });
}
function openFly(b){
  var sc = secs[+b.dataset.i]; if(!sc) return;
  if(flyFor === b){ closeFly(); return; }
  closeFly();
  fly = el('div'); fly.id = 'ax2fly'; fly.setAttribute('role', 'dialog'); fly.setAttribute('aria-label', sc.name);
  var head = el('div', 'fh'); head.appendChild(el('b')).textContent = sc.name; head.appendChild(el('span')).textContent = sc.count ? sc.count + ' briefs' : '';
  fly.appendChild(head);
  var body = el('div', 'fb');
  sc.items.forEach(function(it){
    if(it.sub){ body.appendChild(el('div', 'fl')).textContent = it.sub; return; }
    var a = el('a', 'fi'); a.href = '#' + it.id; a.textContent = it.label;
    if(B && it.id === B.id) a.setAttribute('aria-current', 'page');
    body.appendChild(a);
  });
  fly.appendChild(body); document.body.appendChild(fly);
  var z = zoomOf(fly), r = b.getBoundingClientRect(), vh = window.innerHeight / z;
  fly.style.top = Math.max(16, Math.min(r.top / z - 10, vh - 16 - Math.min(fly.offsetHeight, vh - 32))) + 'px';
  flyFor = b; b.setAttribute('aria-expanded', 'true'); b.classList.add('open');
  fly.addEventListener('click', function(e){ if(e.target.closest('a.fi')) setTimeout(closeFly, 0); });
  var cur = fly.querySelector('[aria-current]'); (cur || fly.querySelector('a.fi') || fly).focus && setTimeout(function(){ try{ (cur || fly.querySelector('a.fi')).focus({preventScroll: false}); }catch(e){} }, 0);
}
function closeFly(){
  if(fly){ fly.remove(); fly = null; }
  if(flyFor){ flyFor.setAttribute('aria-expanded', 'false'); flyFor.classList.remove('open'); flyFor = null; }
}
// Expand: the sidebar stays beside the brief, which moves over and lays out again once the sidebar has slid in
function expand(v){
  root.classList.toggle('ax2-nav', !!v); root.classList.remove('ax2-over'); closeFly();
  AX.settings.set('twonav', v ? '1' : '0');
  if(S){ lay(); setTimeout(function(){ if(S) lay(); }, 480); }
}
function over(){ closeFly(); root.classList.add('ax2-over'); AX.emit('nav:search'); }

/* ---------- the Layout choice in the display sheet ---------- */
function control(){
  var modes = document.getElementById('modes');
  if(!modes){ setTimeout(control, 60); return; }
  if(ctl) return;
  ctl = AX.ui.seg('Layout', [['scroll', 'Scrolling'], ['two', 'Two-pane']], want ? 'two' : 'scroll', function(v){ set(v === 'two'); });
  ctl.classList.add('layout'); ctl.dataset.g = 'layout'; ctl.dataset.o = '1';
  modes.appendChild(ctl);
}
function set(v){
  if(v === want) return;
  want = v; AX.settings.set('layout', v ? 'two' : 'scroll');
  apply(true);
}
function apply(byReader){
  if(on()){
    if(!S){ makeRail(); B = fromHash() || inView() || document.querySelector('main .wrap > .brief'); build(); }
  } else if(S){
    var b = B; unbuild();
    if(byReader && b) requestAnimationFrame(function(){ b.scrollIntoView({block: 'start'}); });
  }
}
function show(b){
  if(!b || b === B) return;
  if(S) unbuild();
  B = b; build(); paintRail();
}

/* ---------- wiring ---------- */
offs.push(AX.on('nav:sections', function(list){ secs = list || []; drawRail(); }));
offs.push(AX.on('nav:collapse', function(){ expand(false); }));
function onHash(){
  if(!on()) return;
  var b = fromHash();
  root.classList.remove('ax2-over'); closeFly();
  if(b && b !== B) show(b);
}
var rq = 0, rt = null, lw = window.innerWidth, lh = window.innerHeight;
function onScroll(){ if(S && !rq) rq = requestAnimationFrame(function(){ rq = 0; mark(); }); }
function onResize(e){
  if(!e.isTrusted || (window.innerWidth === lw && window.innerHeight === lh)) return;
  lw = window.innerWidth; lh = window.innerHeight;
  clearTimeout(rt); rt = setTimeout(function(){ if(!WIDE.matches){ if(S) unbuild(); return; } if(!S) apply(); else lay(); }, 200);
}
function relay(){ if(S){ clearTimeout(rt); rt = setTimeout(lay, 150); } }
function onToggle(e){ if(S && S.flow.contains(e.target)) relay(); }
function onDown(e){
  if(fly && !fly.contains(e.target) && !(rail && rail.contains(e.target))) closeFly();
  if(root.classList.contains('ax2-over')){ var nav = document.getElementById('nav'); if(nav && !nav.contains(e.target) && !(rail && rail.contains(e.target))) root.classList.remove('ax2-over'); }
}
function onKey(e){
  if(e.key !== 'Escape') return;
  if(fly){ var b = flyFor; closeFly(); if(b) b.focus(); }
  else if(root.classList.contains('ax2-over')) root.classList.remove('ax2-over');
}
// Recall and Flat change heights; other classes on the body (open panels, the phone index) do not
function modes(c){ return /(^|\s)study(\s|$)/.test(c) + ',' + /(^|\s)flat(\s|$)/.test(c); }
var mo = new MutationObserver(function(rs){ if(rs.some(function(r){ return modes(r.oldValue || '') !== modes(document.body.className); })) relay(); });
function start(){
  control(); AX.emit('nav:ask');
  if(on()) apply();
  mo.observe(document.body, {attributes: true, attributeFilter: ['class'], attributeOldValue: true});
}
window.addEventListener('hashchange', onHash);
window.addEventListener('scroll', onScroll, {passive: true});
window.addEventListener('resize', onResize);
document.addEventListener('toggle', onToggle, true);
document.addEventListener('mousedown', onDown, true);
document.addEventListener('keydown', onKey);
if(WIDE.addEventListener) WIDE.addEventListener('change', function(){ apply(); });
if(document.readyState === 'complete') start(); else window.addEventListener('load', start, {once: true});

return {teardown: function(){
  if(S) unbuild();
  window.removeEventListener('hashchange', onHash); window.removeEventListener('scroll', onScroll); window.removeEventListener('resize', onResize);
  document.removeEventListener('toggle', onToggle, true); document.removeEventListener('mousedown', onDown, true); document.removeEventListener('keydown', onKey);
  mo.disconnect(); offs.forEach(function(f){ f(); }); offs = [];
  if(rail){ rail.remove(); rail = null; } if(tip){ tip.remove(); tip = null; }
}, on: on};
})();
