/* Browse on phones as a drawer. The sidebar slides in from the left and the page slides aside with it (layout/sidebar.css,
   layout/phone.css). This module adds the dimmed strip over the page, which closes the drawer on a tap, and the swipe:
   to the right on the page opens, to the left closes; the drawer follows the finger and settles by position or speed.
   A swipe that starts in the left 20 px is left to the browser's Back gesture, and one that starts inside an element that
   scrolls sideways is left to that element.
   Events: emits nav:open and nav:close. */
return (function(){
'use strict';
var NARROW = window.matchMedia('(max-width:1100px)');
var B = document.body, nav = document.getElementById('nav'), main = document.querySelector('main');
if(!nav || !main) return null;
var sc = document.createElement('div'); sc.id = 'phscrim'; sc.setAttribute('aria-hidden', 'true'); B.appendChild(sc);
function close(){ AX.emit('nav:close'); }
sc.addEventListener('click', close);
var g = null;
function width(){ return Math.min(window.innerWidth * 0.86, 340); }
function movers(){ return [main, document.getElementById('phead'), document.getElementById('phbar')].filter(Boolean); }
function sideScroller(el){
  for(; el && el !== B; el = el.parentElement){
    if(el.scrollWidth > el.clientWidth + 4){ var o = getComputedStyle(el).overflowX; if(o === 'auto' || o === 'scroll') return true; }
  }
  return false;
}
function set(f){
  nav.style.transition = 'none'; nav.style.visibility = 'visible'; nav.style.transform = 'translateX(' + ((f - 1) * 104).toFixed(2) + '%)';
  sc.style.transition = 'none'; sc.style.opacity = f.toFixed(3); sc.style.left = (f * g.w).toFixed(1) + 'px';
  var x = 'translateX(' + (f * g.w).toFixed(1) + 'px)';
  movers().forEach(function(e){ if(e.id === 'phead' && !e.classList.contains('on')) return; e.style.transition = 'none'; e.style.transform = x; });
}
function clear(){
  [nav, sc].concat(movers()).forEach(function(e){ e.style.transition = ''; e.style.transform = ''; e.style.visibility = ''; e.style.opacity = ''; e.style.left = ''; });
}
function start(e){
  g = null;
  if(!NARROW.matches || e.touches.length !== 1 || B.classList.contains('navset')) return;
  var t = e.touches[0], open = B.classList.contains('navopen');
  if(!open){
    if(t.clientX < 20 || e.target.closest('#mbar,#phead,#phbar,#rvpanel,#rvsession,#axtour,input,select,textarea') || sideScroller(e.target)) return;
  } else if(!e.target.closest('#nav,#phscrim')) return;
  g = {x: t.clientX, y: t.clientY, open: open, lock: false, f: open ? 1 : 0, w: width(), t: Date.now(), lx: t.clientX, v: 0};
}
function move(e){
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
}
function end(){
  if(!g || !g.lock){ g = null; return; }
  var want = g.v > 0.35 ? true : g.v < -0.35 ? false : g.f > 0.5, was = g.open; g = null;
  nav.getBoundingClientRect();
  clear();
  if(want && !was) AX.emit('nav:open'); else if(!want && was) close();
}
document.addEventListener('touchstart', start, {passive: true});
document.addEventListener('touchmove', move, {passive: false});
document.addEventListener('touchend', end); document.addEventListener('touchcancel', end);

return {teardown: function(){
  document.removeEventListener('touchstart', start); document.removeEventListener('touchmove', move);
  document.removeEventListener('touchend', end); document.removeEventListener('touchcancel', end);
  sc.remove();
}};
})();
