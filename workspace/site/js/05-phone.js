/* Phone layout (below 1100px): the reading header, one brief per screen, and Home as the list of sections.
   The header shows the brief being read, its current step and a Recall switch, with the brief's steps beneath; a step
   is current once its heading passes the reading line (09-brief-bounds). With one brief per screen, a link to a brief
   (its hash) shows that brief alone; Back and Home return to the section list at the place it was left.
   html attributes: ph-layout="long" keeps every brief on one long page; ph-bars="hide" slides the tabs and the
   header's top row away while scrolling down.
   Events: listens to brief:step (the brief being read), phone:home (the Home tab while no screen is open);
   emits nav:open and nav:reveal {id, pres} (Browse at the group holding a brief). */
return (function(){
'use strict';
var NARROW = window.matchMedia('(max-width:1100px)');
var H = document.documentElement, B = document.body;
var SOLO = H.getAttribute('data-ph-layout') !== 'long';
var HIDE = H.getAttribute('data-ph-bars') === 'hide';
var head = null, steps = null, ti = null, sub = null, rec = null;
var shown = null, solo = null, fromHome = false, homeY = 0, lastY = 0, offs = [];

function svg(d, w){ return '<svg viewBox="0 0 24 24" width="' + w + '" height="' + w + '" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">' + d + '</svg>'; }
function reduced(){ return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
function hashId(){ var id = location.hash.slice(1); try{ id = decodeURIComponent(id); }catch(e){} return id; }

/* ---------- the header ---------- */
function makeHead(){
  head = document.createElement('div'); head.id = 'phead';
  head.innerHTML = '<div class="ph-t"><button type="button" class="ph-back" aria-label="Back">' + svg('<path d="M15 5l-7 7 7 7"/>', 24) + '</button>' +
    '<button type="button" class="ph-ti"><b></b><span></span></button>' +
    '<button type="button" class="ph-rec" aria-pressed="false">' + svg('<path d="M2.5 12s3.5-6.5 9.5-6.5S21.5 12 21.5 12s-3.5 6.5-9.5 6.5S2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/>', 16) + '<span>Recall</span></button></div>' +
    '<nav class="ph-steps" aria-label="Steps"></nav>';
  B.appendChild(head);
  steps = head.querySelector('.ph-steps');
  ti = head.querySelector('.ph-ti b'); sub = head.querySelector('.ph-ti span'); rec = head.querySelector('.ph-rec');
  rec.addEventListener('click', function(){
    B.classList.toggle('study');
    AX.settings.set('study', B.classList.contains('study') ? '1' : '0');
    paintRec();
  });
  head.querySelector('.ph-ti').addEventListener('click', function(){ if(shown) shown.go(shown.el); });
  head.querySelector('.ph-back').addEventListener('click', back);
  new MutationObserver(paintRec).observe(B, {attributes: true, attributeFilter: ['class']});
  paintRec();
}
function paintRec(){ if(rec) rec.setAttribute('aria-pressed', B.classList.contains('study') ? 'true' : 'false'); }
function measure(){
  var h = head && head.classList.contains('on') ? head.getBoundingClientRect().height : 0;
  if(h) H.style.setProperty('--ph-h', h.toFixed(0) + 'px');
  H.style.setProperty('--ph-top', (head && head.classList.contains('on') ? Math.max(0, head.getBoundingClientRect().bottom) : 0).toFixed(0) + 'px');
}
function drawSteps(s){
  steps.innerHTML = '';
  var numbered = s.secs.some(function(x){ return x.n; });
  steps.classList.toggle('ph-lab', !numbered);
  s.secs.forEach(function(x, i){
    var b = document.createElement('button'); b.type = 'button';
    b.textContent = numbered ? (x.n || x.l) : x.l;
    b.setAttribute('aria-label', (x.n ? x.n + ' ' : '') + x.l);
    if(numbered && !x.n) b.classList.add('ph-pr');
    if(!x.el){ b.classList.add('off'); b.setAttribute('aria-disabled', 'true'); }
    else b.addEventListener('click', function(){ s.go(x.el); });
    steps.appendChild(b);
  });
}
function paint(s){
  if(!head) return;
  var on = !!s && NARROW.matches && (solo ? s.el === solo : s.past);
  if(!on){ head.classList.remove('on'); head.setAttribute('aria-hidden', 'true'); shown = null; measure(); return; }
  if(!shown || shown.el !== s.el){ ti.textContent = s.title; drawSteps(s); }
  shown = s;
  head.classList.add('on'); head.removeAttribute('aria-hidden');
  var btns = steps.children, x = s.secs[s.cur];
  for(var i = 0; i < btns.length; i++){
    if(i === s.cur) btns[i].setAttribute('aria-current', 'step'); else btns[i].removeAttribute('aria-current');
    btns[i].classList.toggle('done', i < s.cur);
  }
  sub.textContent = x && (s.cur > 0 || s.past) ? (x.n ? x.n + ' · ' : '') + x.l : '';
  if(steps.classList.contains('ph-lab') && btns[s.cur]){
    var c = btns[s.cur], left = c.offsetLeft - (steps.clientWidth - c.offsetWidth) / 2;
    if(Math.abs(steps.scrollLeft - left) > 4) steps.scrollTo({left: Math.max(0, left), behavior: reduced() ? 'auto' : 'smooth'});
  }
  measure();
}

/* ---------- one brief per screen ---------- */
function route(){
  var want = SOLO && NARROW.matches;
  H.classList.toggle('ph-solo', want);
  var b = want ? AX.brief.holder(hashId()) : null;
  if(b && b.closest('main')){
    if(!solo){ homeY = window.pageYOffset || 0; fromHome = routed; }
    if(solo && solo !== b) solo.classList.remove('ph-cur');
    solo = b; b.classList.add('ph-cur'); H.classList.add('ph-open');
  } else if(solo){
    solo.classList.remove('ph-cur'); solo = null; H.classList.remove('ph-open');
    paint(null);
    var y = homeY;
    requestAnimationFrame(function(){ window.scrollTo({top: y, behavior: 'instant'}); });
  }
  routed = true;
}
var routed = false;
function home(){
  if(solo){
    try{ history.pushState(null, '', location.pathname + location.search); }catch(e){ location.hash = ''; }
    route();
  } else window.scrollTo({top: 0, behavior: reduced() ? 'auto' : 'smooth'});
}
function back(){ if(solo && fromHome && history.length > 1) history.back(); else home(); }

/* Home lists the sections: a section, its bands and the Presentations groups open Browse at their group */
function reveal(e){
  if(!SOLO || !NARROW.matches || solo || e.defaultPrevented) return;
  var t = e.target.closest && e.target.closest('main .wrap > :is(.sectwrap,.psub,.bsband)'); if(!t) return;
  if(e.target.closest('a,button,select,input,details')) return;
  var pres = t.classList.contains('psub'), n = t.nextElementSibling;
  while(n && !n.classList.contains('brief')){
    if(n.classList.contains('sectwrap') && n !== t) return;
    if(n.classList.contains('psub')) pres = true;
    n = n.nextElementSibling;
  }
  if(!n) return;
  e.preventDefault();
  AX.emit('nav:open');
  AX.emit('nav:reveal', {id: n.id, pres: pres});
}

/* ---------- scrolling ---------- */
function onScroll(){
  var y = window.pageYOffset || 0;
  if(HIDE){
    if(y > lastY + 6 && y > 120) B.classList.add('ph-down');
    else if(y < lastY - 6) B.classList.remove('ph-down');
  }
  if(Math.abs(y - lastY) > 6) lastY = y;
}

function start(){
  if(head) return;
  if(HIDE) H.classList.add('ph-bars-hide');
  makeHead();
  offs.push(AX.on('brief:step', paint));
  offs.push(AX.on('phone:home', home));
  window.addEventListener('scroll', onScroll, {passive: true});
  document.addEventListener('click', reveal, true);
  measure();
}
window.addEventListener('hashchange', route);
window.addEventListener('popstate', route);
var mqOn = function(){ route(); if(NARROW.matches) start(); else if(head){ head.classList.remove('on'); } };
if(NARROW.addEventListener) NARROW.addEventListener('change', mqOn);
route();
if(NARROW.matches){ if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start(); }

return {teardown: function(){
  window.removeEventListener('hashchange', route); window.removeEventListener('popstate', route);
  window.removeEventListener('scroll', onScroll); document.removeEventListener('click', reveal, true);
  offs.forEach(function(f){ f(); }); offs = [];
  if(head){ head.remove(); head = null; }
  H.classList.remove('ph-solo', 'ph-open', 'ph-bars-hide');
}};
})();
