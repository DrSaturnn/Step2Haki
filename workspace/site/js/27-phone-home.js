/* Home on phones. A fixed bar (title, shelf selector, profile, search) over: Continue (the last briefs read), Review, one
   Browse card switched between By system and By complaint, the Coverage matrix, then the page's own guides. Every row is
   read from the page at each draw: the shelf buttons, the section cards with the briefs the shelf shows, the Presentations
   groups. A row dispatches a click on the section card it stands for, so Browse opens at that group; nothing here names a
   shelf or a system. The last four briefs read are kept in localStorage (ax-recent).
   Events: listens to brief:step, phone:home, blueprint:set, review:state; emits nav:open. */
return (function(){
'use strict';
var NARROW = window.matchMedia('(max-width:1100px)');
var H = document.documentElement, B = document.body;
var mw = document.querySelector('main .masthead .wrap'); if(!mw) return null;
var box = null, bar = null, foot = null, seg = 'sys', offs = [], timer = 0;
var CHEV = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>';
var UPDOWN = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 9.5l5-5 5 5M7 14.5l5 5 5-5"/></svg>';
var PERSON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><circle cx="12" cy="8.2" r="4.2"/><path d="M3.8 20.5c.7-4.2 4.1-6.6 8.2-6.6s7.5 2.4 8.2 6.6z"/></svg>';
var LENS = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>';

function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
function off(e){ return e.style.display === 'none'; }
function recent(){ try{ var r = JSON.parse(localStorage.getItem('ax-recent') || '[]'); return Array.isArray(r) ? r : []; }catch(e){ return []; } }
function remember(st){
  if(!st || !st.el || !st.el.id) return;
  var x = st.secs[st.cur] || {}, r = recent().filter(function(o){ return o.id !== st.el.id; });
  r.unshift({id: st.el.id, t: st.title, n: x.n || '', l: x.l || '', h: x.el && x.el.id ? x.el.id : st.el.id});
  try{ localStorage.setItem('ax-recent', JSON.stringify(r.slice(0, 4))); }catch(e){}
}
function read(){
  var meta = [].map.call(document.querySelectorAll('.masthead .meta > span'), function(s){ return s.textContent.trim(); });
  var shelves = [].map.call(document.querySelectorAll('.masthead .shelfpick [data-shelf]'), function(b){
    return {id: b.dataset.shelf, on: b.classList.contains('on'), soon: b.classList.contains('soon'), t: (b.firstChild && b.firstChild.textContent || b.textContent).trim()}; });
  var secs = [].filter.call(document.querySelectorAll('main .wrap > .sectwrap'), function(w){ return !off(w); }).map(function(w){
    var h = w.querySelector('h3.system'), n = h && h.querySelector('.n');
    var t = h ? [].map.call(h.childNodes, function(c){ return c === n ? '' : c.textContent; }).join('').trim() : '';
    var live = 0, x = w.nextElementSibling;
    for(; x && !x.classList.contains('sectwrap'); x = x.nextElementSibling) if(x.classList.contains('brief') && !off(x)) live++;
    return {el: w, id: h ? h.id : '', t: t, n: live}; });
  var groups = [].filter.call(document.querySelectorAll('main .wrap > .psub'), function(p){ return !off(p); }).map(function(p){
    return {el: p, t: (p.querySelector('.t') || p).textContent.trim(), n: (p.querySelector('.n') || {}).textContent || ''}; });
  var pres = secs.filter(function(s){ return s.id === 'presentations'; })[0] || null;
  var due = 0, me = '';
  try{ due = window.axRv.due() || 0; var id = window.axRv.current(); if(id) me = window.axRv.initials(window.axRv.nameOf(id)) || ''; }catch(e){}
  return {meta: meta, shelves: shelves, cur: shelves.filter(function(s){ return s.on; })[0] || {t: ''}, groups: pres ? groups : [],
    sys: secs.filter(function(s){ return s !== pres && s.n; }), due: due, me: me};
}
function draw(){
  if(!box) return;
  var d = read(), els = [];
  function ref(el){ els.push(el); return ' data-i="' + (els.length - 1) + '"'; }
  function row(o){ return '<button type="button" class="hh-r"' + ref(o.el) + '><span>' + esc(o.t) + '</span><span class="hh-b">' + esc(o.n) + '</span><span class="hh-ch">' + CHEV + '</span></button>'; }
  bar.innerHTML = '<div class="hh-top"><button type="button" class="hh-ttl" data-do="top">Step2Haki</button><label class="hh-shelf"><span>' + esc(d.cur.t) + '</span>' + UPDOWN +
    '<select aria-label="Shelf">' + d.shelves.map(function(s){ return '<option value="' + esc(s.id) + '"' + (s.on ? ' selected' : '') + (s.soon ? ' disabled' : '') + '>' + esc(s.t) + (s.soon ? ' (soon)' : '') + '</option>'; }).join('') + '</select></label>' +
    '<button type="button" class="hh-me" data-do="review" aria-label="Review and profiles">' + (d.me ? esc(d.me) : PERSON) + '</button></div>' +
    '<button type="button" class="hh-s" data-do="search">' + LENS + '<span>Search topics, findings, drugs</span></button>';
  var rc = recent().filter(function(o){ var el = document.getElementById(o.id); return el && !off(el); });
  var hasCc = d.groups.length > 0, view = hasCc && (seg === 'cc' || !d.sys.length) ? 'cc' : 'sys', h = '';
  if(rc.length){
    h += '<div class="hh-card hh-list"><button type="button" class="hh-c" data-do="go" data-h="' + esc(rc[0].h) + '"><span class="hh-cx"><em>Continue</em><b>' + esc(rc[0].t) + '</b>' +
      (rc[0].l ? '<i>' + esc((rc[0].n ? rc[0].n + ' · ' : '') + rc[0].l) + '</i>' : '') + '</span><span class="hh-play">' + CHEV + '</span></button>' +
      rc.slice(1, 3).map(function(o){ return '<button type="button" class="hh-r" data-do="go" data-h="' + esc(o.id) + '"><span>' + esc(o.t) + '</span><span class="hh-ch">' + CHEV + '</span></button>'; }).join('') + '</div>';
  }
  h += '<button type="button" class="hh-card hh-rv" data-do="review"><span class="hh-cx"><b>Review</b><i>' +
    (d.me ? (d.due ? d.due + ' due in ' + esc(d.cur.t) : 'Nothing due in ' + esc(d.cur.t)) : 'Choose who is studying to schedule reviews') + '</i></span><span class="hh-pill' + (d.me && d.due ? ' on' : '') + '">' + (d.me ? (d.due ? 'Start' : 'Open') : 'Set up') + '</span></button>';
  h += '<div class="hh-h"><h2>Browse</h2><span>' + esc(d.meta.slice(0, 2).join(' · ')) + '</span></div><div class="hh-card hh-list" data-tour="browse">' +
    (d.sys.length && hasCc ? '<div class="hh-seg" role="group" aria-label="Browse by"><button type="button" data-do="seg" data-v="sys" aria-pressed="' + (view === 'sys') + '">By system</button><button type="button" data-do="seg" data-v="cc" aria-pressed="' + (view === 'cc') + '">By complaint</button></div>' : '') +
    (!d.sys.length && !hasCc ? '<p class="hh-none">No topics in ' + esc(d.cur.t) + ' yet.</p>' : '') +
    (view === 'cc' ? d.groups : d.sys).map(row).join('') + '</div>';
  var mx = AX.blueprint ? AX.blueprint.html() : '';
  if(mx) h += '<div class="hh-h"><h2>Coverage</h2><span>' + esc(AX.blueprint.name()) + '</span></div>' + mx;
  h += '<div class="hh-h"><h2>Guides</h2></div>';
  box.innerHTML = h; box._els = els;
  foot.textContent = [d.meta[4], d.meta[2]].filter(Boolean).join(' · ');
  var r = mw.getBoundingClientRect();
  if(r.width) H.style.setProperty('--phbar-x', Math.max(12, Math.round(r.left + parseFloat(getComputedStyle(mw).paddingLeft || 0))) + 'px');
  var sm = bar.classList.contains('sm'); bar.classList.remove('sm');
  var bh = bar.getBoundingClientRect().height; if(bh) H.style.setProperty('--phbar-h', Math.round(bh) + 'px');
  if(sm) bar.classList.add('sm');
}
function later(ms){ clearTimeout(timer); timer = setTimeout(function(){ if(!H.classList.contains('ph-open')) draw(); }, ms || 40); }
function onClick(e){
  var b = e.target.closest('button'); if(!b || !(box.contains(b) || bar.contains(b))) return;
  var act = b.dataset['do'];
  if(act === 'top'){ window.scrollTo({top: 0, behavior: 'smooth'}); return; }
  if(act === 'seg'){ seg = b.dataset.v; draw(); return; }
  if(act === 'go'){ location.hash = '#' + b.dataset.h; return; }
  if(act === 'search'){ AX.emit('nav:open'); var q = document.querySelector('#nav input[type="search"], #nav #search, #nav .axn-srch input'); if(q) q.focus(); return; }
  if(act === 'review'){ var r = document.querySelector('#mbar [data-act="review"]'); if(r) r.click(); return; }
  var el = box._els && box._els[+b.dataset.i]; if(el) el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
}
function onChange(e){
  if(e.target.tagName !== 'SELECT' || !bar.contains(e.target)) return;
  var b = document.querySelector('.masthead .shelfpick [data-shelf="' + e.target.value + '"]'); if(b) b.click();
  later(60);
}
function onScroll(){ if(bar) bar.classList.toggle('sm', (window.pageYOffset || 0) > 24); }
function onShelf(){ later(40); }
function start(){
  if(box || !NARROW.matches) return;
  box = document.createElement('div'); box.id = 'phhome'; mw.insertBefore(box, mw.firstChild);
  bar = document.createElement('div'); bar.id = 'phbar'; bar.setAttribute('data-tour', 'find'); B.appendChild(bar);
  foot = document.createElement('button'); foot.type = 'button'; foot.id = 'phfoot';
  var tail = document.querySelectorAll('main .wrap'); tail[tail.length - 1].appendChild(foot);
  foot.addEventListener('click', function(){ var l = document.querySelector('.masthead .axlogbtn'); if(l) l.click(); });
  H.classList.add('ph-home');
  document.addEventListener('click', onClick); document.addEventListener('change', onChange);
  window.addEventListener('scroll', onScroll, {passive: true});
  document.addEventListener('ax-shelf', onShelf);
  window.addEventListener('hashchange', onShelf); window.addEventListener('popstate', onShelf);
  offs.push(AX.on('brief:step', remember), AX.on('phone:home', onShelf), AX.on('blueprint:set', onShelf), AX.on('review:state', onShelf));
  draw(); later(1200);
}
if(NARROW.addEventListener) NARROW.addEventListener('change', start);
if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();

return {teardown: function(){
  clearTimeout(timer);
  document.removeEventListener('click', onClick); document.removeEventListener('change', onChange);
  window.removeEventListener('scroll', onScroll); document.removeEventListener('ax-shelf', onShelf);
  window.removeEventListener('hashchange', onShelf); window.removeEventListener('popstate', onShelf);
  offs.forEach(function(f){ f(); }); offs = [];
  [box, bar, foot].forEach(function(e){ if(e) e.remove(); }); box = bar = foot = null;
  H.classList.remove('ph-home');
}};
})();
