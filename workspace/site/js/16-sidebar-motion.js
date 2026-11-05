/* s141: sidebar movement per the Lithium Glance mockup (Jonathan 2026-10-15). Presentation only.
   1. The current step is marked by one lens that glides between steps (the mockup's spring), not a box that jumps.
   2. Steps a brief does not use say so ("Not used"); "Urgent" reads "Urgent risks", as the step heading does.
   3. The sidebar list keeps the current step in view, and on a new brief brings that brief near the top.
   4. The list fades at its top and bottom edges.
   5. Opening the page on a brief's link lands on that brief: the layout scripts reflow the page after the browser's
      first jump to the link, so it is placed again until the reader moves. */
(function(){
  "use strict";
  var WIDE = window.matchMedia('(min-width:1101px)');
  var list = document.getElementById('navlinks');
  if(!list) return;
  function scroller(){
    for(var e = list; e && e !== document.body; e = e.parentElement){
      var o = getComputedStyle(e).overflowY;
      if((o === 'auto' || o === 'scroll') && e.scrollHeight > e.clientHeight + 4) return e;
    }
    return null;
  }
  function dress(rl){
    if(rl.querySelector(':scope > .ax-lens')) return;
    var lens = document.createElement('span'); lens.className = 'ax-lens'; lens.setAttribute('aria-hidden', 'true');
    rl.insertBefore(lens, rl.firstChild);
    rl.querySelectorAll('a').forEach(function(a){
      var t = a.lastChild;
      if(t && t.nodeType === 3 && t.nodeValue === 'Urgent') t.nodeValue = 'Urgent risks';
      if(a.classList.contains('off') && !a.querySelector('.ax-nu')){
        var n = document.createElement('span'); n.className = 'ax-nu'; n.textContent = 'Not used'; a.appendChild(n);
      }
    });
  }
  function keep(el, smooth, top){
    var s = scroller(); if(!s || !el) return;
    var lr = s.getBoundingClientRect(), r = el.getBoundingClientRect();
    if(top){ if(r.top < lr.top + 20 || r.bottom > lr.bottom - 30) s.scrollTo({top: s.scrollTop + r.top - lr.top - 70, behavior: smooth ? 'smooth' : 'auto'}); return; }
    if(r.bottom > lr.bottom - 30 || r.top < lr.top + 20)
      s.scrollTo({top: s.scrollTop + r.top - lr.top - lr.height / 2, behavior: smooth ? 'smooth' : 'auto'});
  }
  var lastRl = null, lastCur = null;
  function place(){
    if(!WIDE.matches || window.AXN) return;   // s143: the axnav component draws the rail
    var rl = list.querySelector('.bb-rail.ax-nr .bb-rl'); if(!rl) return;
    dress(rl);
    var lens = rl.querySelector(':scope > .ax-lens'), a = rl.querySelector('a.cur');
    if(!a){ rl.classList.remove('ax-lensed'); return; }
    if(rl !== lastRl){ rl.classList.remove('ax-glide'); }
    lens.style.transform = 'translateY(' + a.offsetTop + 'px)';
    lens.style.height = a.offsetHeight + 'px'; lens.style.left = a.offsetLeft + 'px'; lens.style.width = a.offsetWidth + 'px'; lens.style.right = 'auto';
    rl.classList.add('ax-lensed');
    if(rl !== lastRl){
      void lens.offsetWidth; rl.classList.add('ax-glide');
      var b = rl.closest('.bb-rail').previousElementSibling;
      keep(b && b.tagName === 'A' ? b : rl, false, true);
    } else if(a !== lastCur) keep(a, true);
    lastRl = rl; lastCur = a;
  }
  var q = 0;
  function kick(){ if(!q) q = requestAnimationFrame(function(){ q = 0; place(); }); }
  new MutationObserver(kick).observe(list, {subtree: true, childList: true, attributes: true, attributeFilter: ['class']});
  window.addEventListener('resize', kick);
  function fade(){ var s = scroller(); document.querySelectorAll('.ax-fade').forEach(function(e){ if(e !== s) e.classList.remove('ax-fade'); }); if(s && WIDE.matches) s.classList.add('ax-fade'); }
  window.addEventListener('load', fade); window.addEventListener('resize', fade);

  /* 5. landing */
  var moved = false;
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function(ev){ window.addEventListener(ev, function(){ moved = true; }, {passive: true, once: true}); });
  function seat(){
    if(moved || window.AXN) return;   // s143: axnav seats the landing
    var id = decodeURIComponent(location.hash.slice(1)); if(!id) return;
    var el = document.getElementById(id); if(!el) return;
    var want = Math.max(parseFloat(getComputedStyle(el).scrollMarginTop) || 0, WIDE.matches ? 88 : 0);   // clear the floating toolbar
    var top = el.getBoundingClientRect().top;
    if(Math.abs(top - want) > 4) window.scrollTo(0, window.scrollY + top - want);
  }
  window.addEventListener('load', function(){ seat(); setTimeout(seat, 250); setTimeout(seat, 900); setTimeout(seat, 1800); kick(); fade(); });
  kick();
})();
