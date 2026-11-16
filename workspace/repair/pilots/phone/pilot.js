/* Pilot only: the options group in Settings, the numbered side rail and the differential density variants. */
(function(){
'use strict';
if(!window.matchMedia('(max-width:1100px)').matches || !window.AX) return;
var H = document.documentElement;
function get(k, d){ return H.getAttribute('data-ph-' + k) || d; }
var CH = [
  ['layout', 'Layout', [['solo', 'One brief per screen'], ['long', 'One long page']], get('layout', 'solo')],
  ['bars', 'Bars while reading', [['stay', 'Always shown'], ['hide', 'Hide while scrolling down']], get('bars', 'stay')],
  ['rail', 'Side rail', [['off', 'Off'], ['on', 'Numbered rail, drag to scrub']], get('rail', 'off')],
  ['dx', 'Differential', [['now', 'As now'], ['a', 'A: tighter cards'], ['b', 'B: one card, hairline rows']], get('dx', 'now')],
  ['nav', 'Browse opens as (r5)', [['drawer', 'Side drawer over the page'], ['push', 'Side drawer, page slides aside'], ['screen', 'Full screen (r3)']], get('nav', 'drawer')],
  ['surf', 'Surface (r5, light only)', [['axbx', 'AxBx deck'], ['axbx24', 'AxBx deck, 24 px corners'], ['now', 'Sculpted (now)']], get('surf', 'axbx')],
  ['home', 'Home (r4)', [['tiles', 'Tiles'], ['list', 'List (r3)']], get('home', 'tiles')],
  ['tabs', 'Tab bar (r4)', [['dock', 'Docked (r3)'], ['float', 'Floating capsule']], get('tabs', 'dock')]
];
if(!H.getAttribute('data-ph-nav')) H.setAttribute('data-ph-nav', 'drawer');
if(!H.getAttribute('data-ph-home')) H.setAttribute('data-ph-home', 'tiles');
if(!H.getAttribute('data-ph-surf')) H.setAttribute('data-ph-surf', 'axbx');
function mount(){
  var s = document.getElementById('axdisp'); if(!s || s.querySelector('.php')) return !!s;
  var box = document.createElement('div'); box.className = 'php';
  box.innerHTML = '<div class="axd-h">Pilot options</div>' + CH.map(function(c){
    return '<div class="php-g"><div class="php-l">' + c[1] + '</div><div class="php-o">' + c[2].map(function(o){
      return '<button type="button" data-k="' + c[0] + '" data-v="' + o[0] + '" aria-pressed="' + (o[0] === c[3]) + '">' + o[1] + '</button>';
    }).join('') + '</div></div>';
  }).join('') + '<p class="php-n">Pilot only. A choice reloads the page.</p>';
  var md = s.querySelector('#modes'); s.insertBefore(box, md ? md.nextSibling : null);
  box.addEventListener('click', function(e){
    var b = e.target.closest('button[data-k]'); if(!b) return;
    e.stopPropagation();
    var o = {}; CH.forEach(function(c){ o[c[0]] = c[3]; }); o[b.dataset.k] = b.dataset.v;
    var ok = false;
    try{ localStorage.setItem('ph-pilot', JSON.stringify(o)); ok = JSON.parse(localStorage.getItem('ph-pilot'))[b.dataset.k] === b.dataset.v; }catch(err){}
    var q = '?' + Object.keys(o).map(function(k){ return 'ph' + k + '=' + o[k]; }).join('&');
    if(ok && !/[?&]ph\w+=/.test(location.search)) location.reload(); else location.href = location.pathname + q + location.hash;
  });
  return true;
}
var n = 0; (function w(){ if(!mount() && ++n < 40) setTimeout(w, 150); })();

/* r5 Browse as a side drawer: the sidebar slides in from the left over the page (drawer) or the page slides aside with
   it (push). It opens from the Browse tab or a swipe to the right on the page, and closes from the Browse tab, a tap on
   the dimmed page, or a swipe to the left. A swipe that starts in the left 20 px is left to Safari's Back gesture, and
   one that starts inside a table or figure that scrolls sideways is left to that element. */
(function(){
  var mode = get('nav', 'drawer'); if(mode === 'screen') return;
  var nav = document.getElementById('nav'), B = document.body; if(!nav) return;
  var sc = document.createElement('div'); sc.id = 'phscrim'; sc.setAttribute('aria-hidden', 'true'); B.appendChild(sc);
  sc.addEventListener('click', function(){ AX.emit('nav:close'); });
  var main = document.querySelector('main'), g = null;
  function isOpen(){ return B.classList.contains('navopen'); }
  function dw(){ return nav.getBoundingClientRect().width || Math.min(innerWidth * 0.86, 340); }
  function sideScroller(el){
    for(; el && el !== B; el = el.parentElement){
      if(el.scrollWidth > el.clientWidth + 4){ var o = getComputedStyle(el).overflowX; if(o === 'auto' || o === 'scroll') return true; }
    }
    return false;
  }
  function set(f){
    nav.style.transition = 'none'; nav.style.visibility = 'visible'; nav.style.transform = 'translateX(' + ((f - 1) * 104).toFixed(2) + '%)';
    sc.style.transition = 'none'; sc.style.opacity = f.toFixed(3);
    if(mode === 'push'){ var x = 'translateX(' + (f * g.w).toFixed(1) + 'px)'; main.style.transition = 'none'; main.style.transform = x; var h = document.getElementById('phead'); if(h && h.classList.contains('on')){ h.style.transition = 'none'; h.style.transform = x; } }
  }
  function clear(){
    [nav, sc, main, document.getElementById('phead')].forEach(function(e){ if(e){ e.style.transition = ''; e.style.transform = ''; e.style.visibility = ''; e.style.opacity = ''; } });
  }
  document.addEventListener('touchstart', function(e){
    g = null;
    if(e.touches.length !== 1 || B.classList.contains('navset')) return;
    var t = e.touches[0], open = isOpen();
    if(!open){
      if(t.clientX < 20 || e.target.closest('#mbar,#phead,#rvpanel,#rvsession,input,select,textarea,.hh-row') || sideScroller(e.target)) return;
    } else if(!e.target.closest('#nav,#phscrim')) return;
    g = {x: t.clientX, y: t.clientY, open: open, lock: false, f: open ? 1 : 0, w: open ? dw() : Math.min(innerWidth * 0.86, 340), t: Date.now(), lx: t.clientX, v: 0};
  }, {passive: true});
  document.addEventListener('touchmove', function(e){
    if(!g) return;
    var t = e.touches[0], dx = t.clientX - g.x, dy = t.clientY - g.y;
    if(!g.lock){
      if(Math.abs(dy) > 10 && Math.abs(dy) >= Math.abs(dx)){ g = null; return; }
      if(Math.abs(dx) < 12 || Math.abs(dx) < 1.6 * Math.abs(dy)) return;
      if(g.open ? dx > 0 : dx < 0){ g = null; return; }
      g.lock = true;
    }
    if(e.cancelable) e.preventDefault();
    var now = Date.now(); g.v = (t.clientX - g.lx) / Math.max(1, now - g.t); g.lx = t.clientX; g.t = now;
    g.f = Math.max(0, Math.min(1, (g.open ? g.w + dx : dx) / g.w));
    set(g.f);
  }, {passive: false});
  function end(){
    if(!g || !g.lock){ g = null; return; }
    var want = g.v > 0.35 ? true : g.v < -0.35 ? false : g.f > 0.5, was = g.open; g = null;
    nav.getBoundingClientRect();
    clear();
    if(want && !was) AX.emit('nav:open'); else if(!want && was) AX.emit('nav:close');
  }
  document.addEventListener('touchend', end); document.addEventListener('touchcancel', end);
})();

/* r4 Home as tiles (after the iOS Fitness Summary and Sharing screens): a large title with the profile button, a Review
   card, the Presentations groups as a row of cards, the systems as a two-column grid. Every tile is built from the
   page's own section cards and opens what they open; nothing is stored. */
(function(){
  if(get('home', 'tiles') !== 'tiles' || get('layout', 'solo') === 'long') return;
  var mw = document.querySelector('main .masthead .wrap'); if(!mw) return;
  var box = document.createElement('div'); box.id = 'phhome'; mw.insertBefore(box, mw.firstChild);
  var CHEV = '<i class="hh-go" aria-hidden="true"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></i>';
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  function off(e){ return e.style.display === 'none'; }
  function draw(){
    var meta = [].map.call(document.querySelectorAll('.masthead .meta > span'), function(s){ return s.textContent.trim(); });
    var shelves = [].map.call(document.querySelectorAll('.masthead .shelfpick [data-shelf]'), function(b){
      return {id: b.dataset.shelf, on: b.classList.contains('on'), soon: b.classList.contains('soon'), t: (b.firstChild && b.firstChild.textContent || b.textContent).trim()}; });
    var cur = shelves.filter(function(s){ return s.on; })[0] || {t: ''};
    var due = 0, me = '';
    try{ due = window.axRv.due() || 0; var id = window.axRv.current(); if(id) me = window.axRv.initials(window.axRv.nameOf(id)) || ''; }catch(e){}
    var secs = [].filter.call(document.querySelectorAll('main .wrap > .sectwrap'), function(w){ return !off(w); }).map(function(w){
      var h = w.querySelector('h3.system'), n = h && h.querySelector('.n');
      var t = h ? [].map.call(h.childNodes, function(c){ return c === n ? '' : c.textContent; }).join('').trim() : '';
      return {el: w, id: h ? h.id : '', t: t, n: n ? parseInt(n.textContent, 10) || 0 : null, num: (w.querySelector('.tab b') || {}).textContent || '', code: (w.querySelector('.tab i') || {}).textContent || ''}; });
    var groups = [].filter.call(document.querySelectorAll('main .wrap > .psub'), function(p){ return !off(p); }).map(function(p){
      return {el: p, t: (p.querySelector('.t') || p).textContent.trim(), n: (p.querySelector('.n') || {}).textContent || ''}; });
    var pres = secs.filter(function(s){ return s.id === 'presentations'; })[0];
    var guide = secs.filter(function(s){ return s.n === null; });
    var sys = secs.filter(function(s){ return s !== pres && s.n !== null; });
    var els = [];
    function ref(el){ els.push(el); return ' data-i="' + (els.length - 1) + '"'; }
    var h = '<div class="hh-top"><h1>Step2Haki</h1><button type="button" class="hh-me" data-do="review" aria-label="Review and profiles">' +
      (me ? esc(me) : '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><circle cx="12" cy="8.2" r="4.2"/><path d="M3.8 20.5c.7-4.2 4.1-6.6 8.2-6.6s7.500 2.400 8.2 6.600z"/></svg>') + '</button></div>' +
      '<div class="hh-sub"><span>' + esc(meta.slice(0, 2).join(' · ')) + '</span><label class="hh-shelf"><span>' + esc(cur.t) + '</span><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 9.500l5-5 5 5M7 14.500l5 5 5-5"/></svg>' +
      '<select aria-label="Shelf">' + shelves.map(function(s){ return '<option value="' + s.id + '"' + (s.on ? ' selected' : '') + (s.soon ? ' disabled' : '') + '>' + esc(s.t) + (s.soon ? ' (soon)' : '') + '</option>'; }).join('') + '</select></label></div>' +
      '<button type="button" class="hh-card hh-hero" data-do="review"><span class="hh-ct">Review' + CHEV + '</span><span class="hh-hr"><span class="hh-big"><b>' + due + '</b><em>due</em></span>' +
      '<span class="hh-ms"><span><i>Shelf</i><b>' + esc(cur.t) + '</b></span>' + meta.slice(0, 2).map(function(m){ var p = /^(\S+)\s+(.*)$/.exec(m) || [0, m, '']; return '<span><i>' + esc(p[2].charAt(0).toUpperCase() + p[2].slice(1)) + '</i><b>' + esc(p[1]) + '</b></span>'; }).join('') + '</span></span></button>';
    if(pres && groups.length){
      h += '<div class="hh-h"><h2>Presentations</h2><span>' + pres.n + ' topics, by complaint</span></div><div class="hh-row">' + groups.map(function(g){
        return '<button type="button" class="hh-card hh-g"' + ref(g.el) + '><span class="hh-ct">' + esc(g.t) + '</span><span class="hh-n"><b>' + esc(g.n) + '</b><em>' + (g.n === '1' ? 'topic' : 'topics') + '</em></span></button>'; }).join('') + '</div>';
    }
    h += '<div class="hh-h"><h2>Systems</h2><span>' + sys.length + ' in ' + esc(cur.t) + '</span></div><div class="hh-grid">' + sys.map(function(s){
      return '<button type="button" class="hh-card hh-t"' + ref(s.el) + '><span class="hh-ct">' + esc(s.t) + CHEV + '</span><span class="hh-n"><b>' + s.n + '</b><em>' + (s.n === 1 ? 'topic' : 'topics') + '</em></span><span class="hh-f">' + esc(s.code || s.num) + '</span></button>'; }).join('') + '</div>';
    if(guide.length){
      h += '<div class="hh-h"><h2>Guides</h2></div>' + guide.map(function(s){ return '<button type="button" class="hh-card hh-l"' + ref(s.el) + '><span class="hh-ct">' + esc(s.t) + CHEV + '</span></button>'; }).join('');
    }
    box.innerHTML = h; box._els = els;
  }
  box.addEventListener('click', function(e){
    var b = e.target.closest('button'); if(!b) return;
    if(b.dataset['do'] === 'review'){ var r = document.querySelector('#mbar [data-act="review"]'); if(r) r.click(); return; }
    var el = box._els && box._els[+b.dataset.i]; if(el) el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
  });
  box.addEventListener('change', function(e){
    if(e.target.tagName !== 'SELECT') return;
    var b = document.querySelector('.masthead .shelfpick [data-shelf="' + e.target.value + '"]'); if(b) b.click();
    setTimeout(draw, 60);
  });
  draw(); setTimeout(draw, 1200);
  document.addEventListener('ax-shelf', function(){ setTimeout(draw, 30); });
})();

/* numbered side rail: shows while scrolling, fades; drag scrubs through the brief; a tap snaps to the nearest stop */
if(get('rail', 'off') !== 'on') return;
var R = document.createElement('div'); R.id = 'phrail'; R.setAttribute('aria-hidden', 'true');
R.innerHTML = '<div class="tk"></div><b class="fl"></b><b class="th"></b><span class="bub"></span>';
document.body.appendChild(R);
var st = null, ticks = [], key = '', fadeT = 0;
function line(){ return Math.max((parseFloat(getComputedStyle(H).getPropertyValue('--ph-top')) || 64) + 8, innerHeight * 0.32); }
AX.on('brief:step', function(s){
  st = s; R.classList.toggle('in', !!s);
  if(!s) return;
  var r = s.el.getBoundingClientRect(), top = r.top + scrollY, hgt = R.clientHeight || 400;
  var k = s.el.id + '|' + Math.round(r.height) + '|' + hgt;
  if(k !== key){
    key = k; var tk = R.querySelector('.tk'); tk.innerHTML = ''; ticks = [];
    var live = s.secs.filter(function(x){ return x.el; });
    var ys = live.map(function(x){ return (x.el.getBoundingClientRect().top + scrollY - top) / r.height * hgt; });
    for(var i = 1; i < ys.length; i++) ys[i] = Math.max(ys[i], ys[i - 1] + 21);
    if(ys.length) ys[ys.length - 1] = Math.min(ys[ys.length - 1], hgt - 10);
    for(var j = ys.length - 2; j >= 0; j--) ys[j] = Math.min(ys[j], ys[j + 1] - 21);
    for(var m = 0; m < ys.length; m++) ys[m] = Math.max(ys[m], 10 + m * 21);
    live.forEach(function(x, i){
      var t = document.createElement('i'); t.style.top = ys[i].toFixed(1) + 'px';
      t.textContent = x.n || ''; if(!x.n) t.className = 'pr';
      tk.appendChild(t); ticks.push({t: t, x: x});
    });
  }
  var cur = s.secs[s.cur];
  ticks.forEach(function(o){ var i = s.secs.indexOf(o.x); o.t.classList.toggle('cur', o.x === cur); o.t.classList.toggle('done', i < s.cur); });
  var f = Math.max(0, Math.min(1, (scrollY + line() - top) / r.height));
  R.querySelector('.fl').style.height = (f * 100).toFixed(2) + '%';
  R.querySelector('.th').style.top = (f * 100).toFixed(2) + '%';
  var bub = R.querySelector('.bub'); bub.style.top = (f * 100).toFixed(2) + '%';
  bub.textContent = cur ? (cur.n ? cur.n + '  ' : '') + cur.l : '';
});
addEventListener('scroll', function(){ R.classList.add('on'); clearTimeout(fadeT); fadeT = setTimeout(function(){ R.classList.remove('on'); }, 1400); }, {passive: true});
var downY = 0, moved = false;
function scrub(e){
  if(!st) return; var rr = R.getBoundingClientRect(), f = Math.max(0, Math.min(1, (e.clientY - rr.top) / rr.height));
  var r = st.el.getBoundingClientRect(); scrollTo({top: r.top + scrollY + f * r.height - line(), behavior: 'instant'});
}
R.addEventListener('pointerdown', function(e){ downY = e.clientY; moved = false; R.classList.add('drag'); R.setPointerCapture(e.pointerId); e.preventDefault(); });
R.addEventListener('pointermove', function(e){ if(!R.classList.contains('drag')) return; if(Math.abs(e.clientY - downY) > 6) moved = true; if(moved) scrub(e); });
R.addEventListener('pointerup', function(e){
  R.classList.remove('drag'); if(moved || !st) return;
  var best = null, bd = 23;
  ticks.forEach(function(o){ var tr = o.t.getBoundingClientRect(), d = Math.abs(e.clientY - (tr.top + tr.height / 2)); if(d < bd){ bd = d; best = o; } });
  if(best) st.go(best.x.el); else scrub(e);
});
R.addEventListener('pointercancel', function(){ R.classList.remove('drag'); });
})();
