/* Builds briefs on demand: those within about 1.5 screens of the viewport, the target of the address hash, the target
   of an in-page link before the browser jumps to it, and every brief before printing. Unbuilt briefs hold an estimated
   height (--axh). A brief built wholly above the viewport keeps the reader's place. Every brief is built at once when
   IntersectionObserver is missing, in jsdom, or with ?axall in the address. Built briefs render only near the screen
   (content-visibility). */
"use strict";
var root = document.documentElement, B = AX.brief;
var anchorNative = !!(window.CSS && CSS.supports && CSS.supports('overflow-anchor', 'auto'));
var eager = !window.IntersectionObserver || /jsdom/i.test(navigator.userAgent) || /[?&]axall\b/.test(location.search);

function estimate(){
  var w = Math.max(320, Math.min(root.clientWidth || 1024, 1600));
  var k = w <= 640 ? 0.95 : w <= 1100 ? 0.55 : 0.36;
  B.pending().forEach(function(b){
    var n = B.content(b).textContent.length;
    b.style.setProperty('--axh', Math.max(400, Math.round(n * k)) + 'px');
  });
}

function build(b){
  if(B.isBuilt(b)) return;
  var r = b.getBoundingClientRect(), above = r.bottom <= 0 && !anchorNative;
  B.build(b);
  b.style.removeProperty('--axh');
  if(above){ var d = b.getBoundingClientRect().height - r.height; if(d) window.scrollBy(0, d); }
}

var io = null, paused = false;
function observe(){
  io = new IntersectionObserver(function(es){
    if(paused) return;
    es.forEach(function(e){ if(e.isIntersecting){ io.unobserve(e.target); build(e.target); } });
  }, { rootMargin: '150% 0px 150% 0px' });
  B.pending().forEach(function(b){ io.observe(b); });
}
AX.on('brief:built', function(b){ if(io) io.unobserve(b); });

function hashId(){ var h = (location.hash || '').slice(1); try{ return decodeURIComponent(h); }catch(e){ return h; } }
function target(){ var id = hashId(); return id ? document.getElementById(id) : null; }

var timer = null;
function settle(){
  clearInterval(timer);
  var el = target(); if(!el) return;
  var last = -1, n = 0;
  timer = setInterval(function(){
    var y = window.pageYOffset || 0;
    if(y === last){
      clearInterval(timer);
      if(el.offsetParent === null) return;
      var top = el.getBoundingClientRect().top;
      if(top < -4 || top > 60) el.scrollIntoView({ block: 'start' });
    }
    last = y; if(++n > 40) clearInterval(timer);
  }, 120);
}
function goHash(){
  var id = hashId(); if(!id) return;
  var had = document.getElementById(id);
  var b = B.holder(id); if(!b) return;
  build(b);
  var el = document.getElementById(id);
  if(el && !had) el.scrollIntoView({ block: 'start' });
  settle();
}

/* brief:reveal {y, smooth}: scroll to y() (a page offset the caller measures). Briefs passed on the way are not built
   until the scroll stops, so their estimated heights hold and y() stays valid; then the briefs near the destination
   build and the page is placed at y() again until it holds. Input from the reader ends the correction. */
var revealN = 0;
function stopReveal(){ revealN++; }
['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function(t){ window.addEventListener(t, stopReveal, { passive: true, capture: true }); });
function reveal(o){
  var my = ++revealN, last = -1, still = 0, ticks = 0;
  function place(){ window.scrollTo({ top: o.y(), behavior: 'instant' }); }
  function resume(){
    paused = false;
    if(io){ io.disconnect(); observe(); }
    var n = 0;
    var t = setInterval(function(){
      if(my !== revealN || ++n > 12){ clearInterval(t); return; }
      if(Math.abs(o.y() - (window.pageYOffset || 0)) > 4) place();
    }, 100);
  }
  if(!io){ o.smooth ? window.scrollTo({ top: o.y(), behavior: 'smooth' }) : place(); return; }
  paused = true;
  window.scrollTo({ top: o.y(), behavior: o.smooth ? 'smooth' : 'instant' });
  var w = setInterval(function(){
    var y = window.pageYOffset || 0;
    still = y === last ? still + 1 : 0; last = y;
    if(my !== revealN || still >= 2 || ++ticks > 40){ clearInterval(w); resume(); }
  }, 80);
}
AX.on('brief:reveal', reveal);

document.addEventListener('click', function(e){
  var a = e.target.closest && e.target.closest('a[href^="#"]'); if(!a) return;
  var id = a.getAttribute('href').slice(1); try{ id = decodeURIComponent(id); }catch(x){}
  var b = id && B.holder(id); if(b) build(b);
}, true);
window.addEventListener('hashchange', function(){ goHash(); });
window.addEventListener('beforeprint', function(){ B.buildAll(); });

function start(){
  if('contentVisibility' in root.style) root.classList.add('cv');
  if(eager){ B.buildAll(); return; }
  estimate();
  goHash();
  observe();
}
if(document.readyState === 'complete') start(); else window.addEventListener('load', function(){ setTimeout(start, 0); });
