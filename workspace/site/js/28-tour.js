/* The welcome card and the tour stops. The card opens once for a reader who arrives at the starting screen with no saved
   reading or review data, and again whenever tour:open is emitted. Its primary button starts the stops: one ring moves to
   the elements tagged data-tour for the stop, and the stop text sits in a panel above the tab capsule on phones and in a
   popover beside the ring on desktop. A stop stores no position; it measures its tagged elements when shown and again on
   resize, scroll, zoom and any size change of a target. A stop with no visible target shows its text as a centered card.
   Stops 1 and 2 need the phone starting screen and stop 3 needs an open brief, so the tour moves there first: stop 3
   opens the brief the reader was in, or the first brief the sidebar lists. A first visit ends inside that brief; a replay
   returns the reader to where the tour started. On the last stop the ring moves from the bar to the settings control.
   A reader who first arrives on a direct link to a brief gets a small pill that offers the tour.
   The display sheet's Help group holds the replay control, which emits tour:open.
   Every way out (the close buttons, Skip, Esc, a tap on the card's backdrop, a swipe down on the phone sheet or panel)
   records the tour as seen in the reader settings (tour). While the tour is open the rest of the page is inert and
   focus stays inside the card or the panel.
   Events: listens to tour:open. */
return (function(){
'use strict';
var VERSION = '1';
var NARROW = window.matchMedia('(max-width:1100px)');
var B = document.body;
var COPY = {
  title: 'Welcome to Step2Haki',
  line: 'Board briefs for Step 2 CK and the shelf exams. Each brief teaches one decision the exam tests, then checks it with practice questions.',
  rows: ['Pick a shelf.', 'Find a topic by system or by complaint.', 'Read the steps in order, then answer the questions.'],
  note: 'Progress saves in this browser. No account needed.',
  go: 'Take the tour', skip: 'Skip', next: 'Next', done: 'Done', back: 'Back'
};
var STOPS = [
  {tag: 'find', home: true, title: 'Search and shelf', text: 'Search any topic, finding or drug. The shelf menu limits every list to one exam.'},
  {tag: 'browse', home: true, title: 'Browse', text: 'By system lists topics by organ system. By complaint lists workups that start from the presenting complaint.'},
  {tag: 'brief', brief: true, title: 'Inside a brief', text: 'Steps 1 to 8 run from presentation to follow-up. A number jumps to its step. Practice opens the questions. Recall hides answers until tapped.'},
  {tag: 'bar', then: 'replay', title: 'Tabs', wideTitle: 'Toolbar',
    text: 'Home, Browse, Review and Settings stay at the bottom of every screen. This tutorial replays from Settings.',
    wideText: 'Read and Recall switch the study mode. Review schedules what to see again. This tutorial replays from the settings button.'}
];
var PILL = 'New here? Take the tour';
var DOTS = STOPS.length, PAD = 6, GAP = 14, EDGE = 16;
var SVG_X = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8"/></svg>';
var root = null, scrim = null, card = null, ring = null, panel = null, isOpen = false, mode = 'card', at = 0, back = null, held = [], hideT = 0, drag = null, raf = 0, ro = null, watched = [], ringTag = '', thenT = 0, pollT = 0, seq = 0, replay = false, was = null, pill = null, rpT = 0;

function el(tag, cls, html){ var e = document.createElement(tag); if(cls) e.className = cls; if(html) e.innerHTML = html; return e; }
function seen(){ return AX.settings.get('tour') !== null; }
function returning(){
  try{
    var ls = window.localStorage;
    if(ls.getItem('ax-recent')) return true;
    for(var i = 0; i < ls.length; i++) if((ls.key(i) || '').indexOf('ax-rev') === 0) return true;
  }catch(e){}
  return false;
}
function briefAt(hash){
  var id = decodeURIComponent((hash || '').slice(1)), t = id && document.getElementById(id);
  return !!(t && t.closest('.brief'));
}
function onBrief(){ return briefAt(location.hash); }
function starter(){
  var a = Array.prototype.filter.call(document.querySelectorAll('#nav a.axn-b[href^="#"]'), function(x){ return x.getClientRects().length; })[0];
  return a ? a.getAttribute('href') : '';
}
/* move the page to the screen a stop needs, and remember where the tour started */
function prep(s){
  var need = (s.home && NARROW.matches && onBrief()) ? 'home' : (s.brief && !onBrief()) ? 'brief' : '';
  if(!need) return;
  if(!was) was = {hash: location.hash, y: window.scrollY};
  if(need === 'home'){ AX.emit('phone:home'); return; }
  var h = briefAt(was.hash) ? was.hash : starter();
  if(h){ location.hash = h; setTimeout(function(){ window.dispatchEvent(new Event('scroll')); }, 60); }
}
function restore(){
  var w = was; was = null;
  if(!w || !replay || location.hash === w.hash) return;
  if(w.hash) location.hash = w.hash;
  else if(NARROW.matches) AX.emit('phone:home');
  else history.replaceState(null, '', location.pathname + location.search);
  if(!NARROW.matches) window.scrollTo(0, w.y);
}

function build(){
  root = el('div'); root.id = 'axtour';
  scrim = root.appendChild(el('div', 'tr-scrim'));
  card = root.appendChild(el('div', 'tr-card'));
  card.setAttribute('role', 'dialog'); card.setAttribute('aria-modal', 'true'); card.setAttribute('aria-labelledby', 'axtour-h'); card.tabIndex = -1;
  card.appendChild(el('div', 'tr-grab')).setAttribute('aria-hidden', 'true');
  var x = card.appendChild(el('button', 'tr-x', SVG_X)); x.type = 'button'; x.setAttribute('aria-label', 'Close');
  card.appendChild(el('div', 'tr-mark')).textContent = 'S2';
  var h = card.appendChild(el('h2', 'tr-h')); h.id = 'axtour-h'; h.textContent = COPY.title;
  card.appendChild(el('p', 'tr-p')).textContent = COPY.line;
  var ol = card.appendChild(el('ol', 'tr-rows'));
  COPY.rows.forEach(function(t, i){
    var li = ol.appendChild(el('li'));
    var n = li.appendChild(el('span', 'n')); n.textContent = i + 1; n.setAttribute('aria-hidden', 'true');
    li.appendChild(el('span', 't')).textContent = t;
  });
  card.appendChild(el('p', 'tr-f')).textContent = COPY.note;
  var go = card.appendChild(el('button', 'tr-go')); go.type = 'button'; go.textContent = COPY.go;
  var skip = card.appendChild(el('button', 'tr-skip')); skip.type = 'button'; skip.textContent = COPY.skip;
  [x, skip].forEach(function(b){ b.addEventListener('click', close); });
  go.addEventListener('click', function(){ stop(0); });
  scrim.addEventListener('click', function(){ if(mode === 'card') close(); });
  root.addEventListener('mousedown', function(e){ if(!e.target.closest('.tr-card,.tr-panel')) e.preventDefault(); });
  root.addEventListener('wheel', function(e){ if(!e.target.closest('.tr-card')) e.preventDefault(); }, {passive: false});
  ring = root.appendChild(el('div', 'tr-ring')); ring.setAttribute('aria-hidden', 'true');
  panel = root.appendChild(el('div', 'tr-panel'));
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'true'); panel.setAttribute('aria-labelledby', 'axtour-sh'); panel.tabIndex = -1; panel.inert = true;
  panel.appendChild(el('div', 'tr-grab')).setAttribute('aria-hidden', 'true');
  var sx = panel.appendChild(el('button', 'tr-x', SVG_X)); sx.type = 'button'; sx.setAttribute('aria-label', 'Close');
  panel.appendChild(el('h2', 'tr-sh')).id = 'axtour-sh';
  panel.appendChild(el('p', 'tr-sp'));
  var foot = panel.appendChild(el('div', 'tr-foot')), dots = foot.appendChild(el('div', 'tr-dots'));
  dots.setAttribute('role', 'img');
  for(var d = 0; d < DOTS; d++) dots.appendChild(el('i'));
  var bk = foot.appendChild(el('button', 'tr-back')); bk.type = 'button'; bk.textContent = COPY.back;
  var nx = foot.appendChild(el('button', 'tr-next')); nx.type = 'button';
  sx.addEventListener('click', close);
  bk.addEventListener('click', function(){ if(at > 0) stop(at - 1); });
  nx.addEventListener('click', function(){ if(at < STOPS.length - 1) stop(at + 1); else close(); });
  [card, panel].forEach(function(s){
    s.addEventListener('touchstart', dragStart, {passive: true});
    s.addEventListener('touchmove', dragMove, {passive: false});
    s.addEventListener('touchend', dragEnd); s.addEventListener('touchcancel', dragEnd);
  });
  B.appendChild(root);
}
function sheet(){ return mode === 'card' ? card : panel; }
function shade(){ return mode === 'card' ? scrim : ring; }
function setMode(m){ mode = m; root.setAttribute('data-m', m); card.inert = m !== 'card'; panel.inert = m !== 'stop'; }

/* the visible elements tagged for a stop, and the one box around them */
function tagged(tag){
  return Array.prototype.filter.call(document.querySelectorAll('[data-tour~="' + tag + '"]'), function(e){
    var r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden' && r.right > 0 && r.left < window.innerWidth;
  });
}
function targets(tag){
  return tagged(tag).filter(function(e){ var r = e.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; });
}
function box(els){
  var l = Infinity, t = Infinity, r = -Infinity, b = -Infinity;
  els.forEach(function(e){ var q = e.getBoundingClientRect(); l = Math.min(l, q.left); t = Math.min(t, q.top); r = Math.max(r, q.right); b = Math.max(b, q.bottom); });
  var vw = window.innerWidth, vh = window.innerHeight;
  l = Math.max(4, l - PAD); t = Math.max(4, t - PAD); r = Math.min(vw - 4, r + PAD); b = Math.min(vh - 4, b + PAD);
  return {l: l, t: t, w: r - l, h: b - t};
}
function watch(els){
  if(!ro) return;
  watched.forEach(function(e){ ro.unobserve(e); }); watched = els; els.forEach(function(e){ ro.observe(e); });
}
function px(n){ return Math.round(n) + 'px'; }
function place(){
  raf = 0;
  if(!isOpen || mode !== 'stop') return;
  var st = STOPS[at], els = targets(ringTag), base = ringTag === st.tag ? els : targets(st.tag), vw = window.innerWidth, vh = window.innerHeight, ps = panel.style;
  watch(els);
  root.classList.toggle('lost', !els.length);
  ps.left = ps.top = ps.bottom = ''; ps.removeProperty('--tr-ay');
  if(!els.length) return;
  var b = box(els), rs = ring.style;
  if(NARROW.matches){
    var bar = document.getElementById('mbar'), br = bar && bar.getBoundingClientRect();
    if(br && br.height && br.top > vh / 2){
      var a = base.length ? box(base) : b, edge = a.t > vh / 2 && a.t < br.top && a.t + a.h > br.top ? a.t : br.top;
      ps.bottom = px(vh - edge + 8);
    }
    var lim = panel.getBoundingClientRect().top - 8;
    if(b.t + 40 < lim) b.h = Math.min(b.h, lim - b.t);
  } else {
    var c = base.length ? box(base) : b, pw = panel.offsetWidth, ph = panel.offsetHeight, x, y, side;
    if(c.l + c.w + GAP + pw <= vw - EDGE){ side = 'r'; x = c.l + c.w + GAP; y = c.t + c.h / 2 - ph / 2; }
    else { side = 'b'; x = c.l + c.w - pw; y = c.t + c.h + GAP; }
    x = Math.max(EDGE, Math.min(x, vw - pw - EDGE)); y = Math.max(EDGE, Math.min(y, vh - ph - EDGE));
    ps.left = px(x); ps.top = px(y);
    root.setAttribute('data-side', side);
    if(side === 'r') ps.setProperty('--tr-ay', px(Math.max(22, Math.min(c.t + c.h / 2 - y, ph - 22))));
    else ps.setProperty('--tr-ay', px(Math.max(22, Math.min(c.l + c.w / 2 - x, pw - 22))));
  }
  rs.left = px(b.l); rs.top = px(b.t); rs.width = px(b.w); rs.height = px(b.h);
}
function queue(){ if(isOpen && mode === 'stop' && !raf) raf = requestAnimationFrame(place); }
function render(){
  var s = STOPS[at], wide = !NARROW.matches;
  panel.querySelector('.tr-sh').textContent = (wide && s.wideTitle) || s.title;
  panel.querySelector('.tr-sp').textContent = (wide && s.wideText) || s.text;
  panel.querySelector('.tr-back').hidden = at === 0;
  panel.querySelector('.tr-next').textContent = at === DOTS - 1 ? COPY.done : COPY.next;
  var dots = panel.querySelector('.tr-dots');
  dots.setAttribute('aria-label', 'Step ' + (at + 1) + ' of ' + DOTS);
  Array.prototype.forEach.call(dots.children, function(d, k){ d.classList.toggle('on', k === at); });
}
/* a stop shows once its target is on screen; a target that never appears shows the text as a centered card */
function stop(i){
  var s = STOPS[i], from = mode, me = ++seq;
  AX.settings.set('tour', VERSION);
  clearTimeout(thenT); clearTimeout(pollT);
  prep(s);
  (function wait(n){
    if(me !== seq || !isOpen) return;
    var els = targets(s.tag);
    if(!els.length){
      var off = tagged(s.tag)[0];
      if(off) off.scrollIntoView({block: 'center'});
      if(n < 20){ if(from === 'stop') root.classList.add('wait'); pollT = setTimeout(function(){ wait(n + 1); }, 80); return; }
    }
    at = i; ringTag = s.tag; render();
    root.classList.remove('wait', 'far');
    if(from === 'card'){ ring.style.transition = 'none'; panel.style.transition = 'none'; }
    setMode('stop'); place();
    if(from === 'card'){ root.getBoundingClientRect(); ring.style.transition = ''; panel.style.transition = ''; root.classList.add('go'); }
    try{ panel.focus({preventScroll: true}); }catch(e){}
    if(s.then) thenT = setTimeout(function(){ if(me !== seq || !isOpen || !targets(s.then).length) return; ringTag = s.then; root.classList.add('far'); place(); }, 1800);
  })(0);
}
function relay(){ if(isOpen && mode === 'stop') stop(at); }

/* the rest of the page takes no focus and no pointer while the card is open */
function hold(on){
  if(on){
    held = Array.prototype.filter.call(B.children, function(c){ return c !== root && !c.inert; });
    held.forEach(function(c){ c.inert = true; });
  } else { held.forEach(function(c){ c.inert = false; }); held = []; }
}
function open(again){
  if(isOpen) return;
  replay = again === true; was = null; unpill();
  if(!root) build();
  clearTimeout(hideT); isOpen = true;
  back = document.activeElement;
  root.classList.remove('go', 'lost', 'wait', 'far'); setMode('card');
  root.classList.add('on'); hold(true);
  root.getBoundingClientRect();
  root.classList.add('in');
  try{ card.focus({preventScroll: true}); }catch(e){}
}
function close(){
  if(!isOpen) return;
  isOpen = false; AX.settings.set('tour', VERSION);
  seq++; clearTimeout(thenT); clearTimeout(pollT);
  root.classList.remove('in', 'go'); hold(false); watch([]); restore();
  hideT = setTimeout(function(){ root.classList.remove('on'); clearDrag(); }, 520);
  if(back && back.focus && B.contains(back)) try{ back.focus({preventScroll: true}); }catch(e){}
  back = null;
}
function key(e){
  if(!isOpen) return;
  if(e.key === 'Escape'){ e.preventDefault(); e.stopPropagation(); close(); return; }
  if(e.key !== 'Tab') return;
  var sh = sheet(), f = sh.querySelectorAll('button:not([hidden])'), first = f[0], end = f[f.length - 1], a = document.activeElement;
  if(e.shiftKey && (a === first || a === sh)){ e.preventDefault(); end.focus(); }
  else if(!e.shiftKey && a === end){ e.preventDefault(); first.focus(); }
}

/* the phone sheet or panel follows a downward drag and closes past 30% of its height or on a fast flick */
function clearDrag(){ [card, panel, scrim, ring].forEach(function(e){ e.style.transition = ''; e.style.opacity = ''; }); card.style.transform = ''; panel.style.transform = ''; }
function dragStart(e){
  drag = null;
  if(!NARROW.matches || !isOpen || e.touches.length !== 1 || sheet().scrollTop > 0) return;
  var t = e.touches[0];
  drag = {x: t.clientX, y: t.clientY, lock: false, d: 0, el: sheet(), sh: shade(), h: sheet().offsetHeight, t: Date.now(), ly: t.clientY, v: 0};
}
function dragMove(e){
  if(!drag) return;
  var t = e.touches[0], dx = t.clientX - drag.x, dy = t.clientY - drag.y;
  if(!drag.lock){
    if(dy < -6 || Math.abs(dx) > Math.abs(dy) + 6){ drag = null; return; }
    if(dy < 8) return;
    drag.lock = true;
  }
  if(e.cancelable) e.preventDefault();
  var now = Date.now(); drag.v = (t.clientY - drag.ly) / Math.max(1, now - drag.t); drag.ly = t.clientY; drag.t = now;
  drag.d = Math.max(0, dy);
  drag.el.style.transition = 'none'; drag.el.style.transform = 'translateY(' + drag.d.toFixed(1) + 'px)';
  drag.sh.style.transition = 'none'; drag.sh.style.opacity = Math.max(0, 1 - drag.d / drag.h).toFixed(3);
}
function dragEnd(){
  if(!drag || !drag.lock){ drag = null; return; }
  var shut = drag.v > 0.5 || drag.d > drag.h * 0.3, e = drag.el; drag = null;
  e.getBoundingClientRect();
  clearDrag();
  if(shut) close();
}

document.addEventListener('keydown', key, true);
if(window.ResizeObserver) ro = new ResizeObserver(queue);
window.addEventListener('resize', queue); window.addEventListener('scroll', queue, true); window.addEventListener('orientationchange', queue);
if(window.visualViewport){ window.visualViewport.addEventListener('resize', queue); window.visualViewport.addEventListener('scroll', queue); }
if(NARROW.addEventListener) NARROW.addEventListener('change', relay);
/* a replay closes the display sheet first */
var offOpen = AX.on('tour:open', function(){
  var sheetOn = B.classList.contains('navset') || !!document.querySelector('#axdisp.on');
  if(B.classList.contains('navset')) AX.emit('nav:close'); else if(sheetOn) AX.emit('settings:set', false);
  clearTimeout(rpT); rpT = setTimeout(function(){ open(true); }, sheetOn ? 320 : 0);
});

/* a first arrival on a direct link to a brief: a pill that offers the tour, for that visit */
function unpill(){ if(pill){ pill.remove(); pill = null; } }
function showPill(){
  pill = el('div'); pill.id = 'axtourpill';
  var go = pill.appendChild(el('button', 'tp-go')); go.type = 'button'; go.textContent = PILL;
  var x = pill.appendChild(el('button', 'tp-x', SVG_X)); x.type = 'button'; x.setAttribute('aria-label', 'Dismiss');
  go.addEventListener('click', function(){ open(false); });
  x.addEventListener('click', function(){ AX.settings.set('tour', VERSION); unpill(); });
  B.appendChild(pill); pill.getBoundingClientRect(); pill.classList.add('in');
}

var firstT = 0;
function first(){
  if(seen() || returning()) return;
  firstT = setTimeout(function(){ if(onBrief()) showPill(); else open(false); }, 450);
}
if(document.readyState === 'complete') first(); else window.addEventListener('load', first);

return {teardown: function(){
  clearTimeout(firstT); clearTimeout(hideT); clearTimeout(thenT); clearTimeout(pollT); clearTimeout(rpT); seq++; unpill();
  cancelAnimationFrame(raf); if(ro) ro.disconnect();
  document.removeEventListener('keydown', key, true); window.removeEventListener('load', first);
  window.removeEventListener('resize', queue); window.removeEventListener('scroll', queue, true); window.removeEventListener('orientationchange', queue);
  if(window.visualViewport){ window.visualViewport.removeEventListener('resize', queue); window.visualViewport.removeEventListener('scroll', queue); }
  if(NARROW.removeEventListener) NARROW.removeEventListener('change', relay);
  offOpen(); hold(false); if(root) root.remove();
}};
})();
