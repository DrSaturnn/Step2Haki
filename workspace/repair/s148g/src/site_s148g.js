/* s148g site layer (Jonathan 2026-10-20; claude/pending/SITE_S148G.md): hover cards float on touch as on desktop, and a
   linked brief opens as a panel grown from its link (desktop) or a near-full-screen sheet grown from the tapped link (phone),
   replacing the right-hand 520 px panel. The per-choice reasons, the card sizing, the First step split and the timeline
   tile are in the page script (mcq), the s148f script and the styles. Presentation only: no brief text changes. */
(function(){
  'use strict';
  var fine = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nativeRemove = Element.prototype.remove;
  function zoom(){ return parseFloat(getComputedStyle(document.documentElement).zoom) || 1; }

  /* ---------- 1. hover cards on touch: the desktop card and motion, opened by a tap ---------- */
  var tc = null, tOwner = null;
  function bodyOf(btn){
    var n = btn.nextElementSibling;
    if(n && n.classList.contains('sp-pop-b')) return n;
    return document.getElementById(btn.getAttribute('aria-controls'));
  }
  function tClose(anim){
    if(!tc) return; var c = tc; tc = null;
    if(tOwner){ tOwner.setAttribute('aria-expanded', 'false'); tOwner.classList.remove('qx-on'); tOwner = null; }
    if(still || !anim){ nativeRemove.call(c); return; }
    c.classList.add('qx-out'); setTimeout(function(){ nativeRemove.call(c); }, 380);
  }
  // the line box of the term nearest the tap (a term can wrap over two lines)
  function termRect(btn, y){
    var rs = btn.getClientRects(), best = null, d = 1e9;
    for(var i = 0; i < rs.length; i++){ var r = rs[i], dd = (y == null) ? i : Math.abs((r.top + r.bottom) / 2 - y); if(dd < d){ d = dd; best = r; } }
    return best || btn.getBoundingClientRect();
  }
  function tOpen(btn, y){
    var body = bodyOf(btn); if(!body) return;
    tClose(false);
    var z = zoom();
    var c = document.createElement('div'); c.className = 'sp-card qx-tc'; c.setAttribute('role', 'dialog');
    c.setAttribute('aria-label', (btn.textContent || '').replace(/\s+/g, ' ').trim());
    c.innerHTML = body.innerHTML;
    document.body.appendChild(c);
    var r = termRect(btn, y), w = Math.min(380, window.innerWidth - 24);
    c.style.width = (w / z) + 'px';
    var left = Math.max(12, Math.min(r.left, window.innerWidth - w - 12));
    var h = c.offsetHeight * z, below = r.bottom + 8, up = below + h > window.innerHeight - 8 && r.top - h - 8 > 8;
    var top = up ? r.top - h - 8 : below;
    // the card grows from the term: its origin sits under (or over) the tapped word
    var ox = Math.max(14, Math.min(r.left + Math.min(r.width, 60) / 2 - left, w - 14));
    c.style.transformOrigin = (ox / z) + 'px ' + (up ? '100%' : '0');
    if(up) c.classList.add('qx-up');
    c.style.left = (left + window.scrollX) / z + 'px'; c.style.top = (top + window.scrollY) / z + 'px';
    tc = c; tOwner = btn; btn.setAttribute('aria-expanded', 'true'); btn.classList.add('qx-on');
  }
  if(!fine){
    // window capture runs before the spine script's document listener, so the old inline tray never opens
    window.addEventListener('click', function(e){
      var p = e.target.closest && e.target.closest('.sp-pop');
      if(p && !p.closest('.sp-card')){
        e.preventDefault(); e.stopPropagation();
        if(tOwner === p) tClose(true); else tOpen(p, e.clientY);
        return;
      }
      if(tc && !(e.target.closest && e.target.closest('.qx-tc'))) tClose(true);
    }, true);
    // a card left behind by a scrolling panel or table would float loose: close it; the page's own scroll carries it
    document.addEventListener('scroll', function(e){ if(tc && e.target !== document && !(e.target.closest && e.target.closest('.qx-tc'))) tClose(true); }, true);
    window.addEventListener('resize', function(){ tClose(false); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') tClose(true); });
  }

  /* ---------- 2. linked brief: a panel anchored to its link ---------- */
  var root = document.documentElement, from = null, link = null;
  function anchored(){ return !document.body.classList.contains('qx-rhp'); }
  // set the panel's place before the spine script builds it (document capture runs after this window capture)
  function place(l){
    var z = zoom(), vw = window.innerWidth, vh = window.innerHeight;
    link = l;
    if(vw <= 640) return;                                   // phone: a fixed near-full-screen sheet (styles)
    var r = l.getBoundingClientRect();
    var need = Math.min(vh * 0.62, 560);
    if(vh - r.bottom - 34 < need){                          // too little room under the link: bring it up first
      var dy = r.top - Math.max(96, vh * 0.14);
      window.scrollBy({ top: dy, behavior: 'instant' }); if(from) from = { left: from.left, top: from.top - dy, width: from.width, height: from.height };
      r = l.getBoundingClientRect();
    }
    var w = Math.min(720, vw - 32), left = Math.max(16, Math.min(r.left - 18, vw - w - 16));
    var top = Math.min(r.bottom + 10, vh - need - 24), h = vh - top - 24;
    root.style.setProperty('--qx-dl', left / z + 'px'); root.style.setProperty('--qx-dt', top / z + 'px');
    root.style.setProperty('--qx-dw', w / z + 'px'); root.style.setProperty('--qx-dh', h / z + 'px');
  }
  window.addEventListener('click', function(e){
    var po = e.target.closest && e.target.closest('.qx-pv .qx-po');
    if(po){ var b = po.closest('.qx-pv').getBoundingClientRect(); from = { left: b.left, top: b.top, width: b.width, height: b.height }; return; }
    var l = e.target.closest && e.target.closest('.sp-drw');
    if(!l || l.closest('.sp-drawer')) { from = null; return; }
    if(anchored()) place(l);
  }, true);
  function flip(el, r){
    var d = el.getBoundingClientRect(); if(!r || !r.width || !d.width) return false;
    el.style.transformOrigin = '0 0';
    el.style.transform = 'translate(' + (r.left - d.left) + 'px,' + (r.top - d.top) + 'px) scale(' + (r.width / d.width) + ',' + (r.height / d.height) + ')';
    return true;
  }
  new MutationObserver(function(ms){
    ms.forEach(function(m){ Array.prototype.forEach.call(m.addedNodes, function(n){
      if(n.nodeType !== 1 || !n.classList.contains('sp-drawer')) return;
      if(!anchored()){ n.classList.add('qx-rh'); from = null; return; }
      n.classList.add('qx-anc'); var src = from, lk = link; from = null; n._qxLink = lk;
      if(lk) lk.classList.add('qx-lk');
      if(still) return;
      if(fine && window.innerWidth > 640){
        // the spine script grows the panel from the link; opened from the preview, it grows from the preview card instead
        if(src && n.classList.contains('sp-g')){
          var t = n.style.transition; n.style.transition = 'none'; n.style.transform = '';
          flip(n, src); n.style.borderRadius = '20px'; n.getBoundingClientRect(); n.style.transition = t;
        }
        return;
      }
      // touch: grow from the tapped link (or the preview card) to the sheet
      var r = src || (lk && lk.getBoundingClientRect());
      n.classList.add('qx-g0');
      if(flip(n, r)){ n.style.borderRadius = '18px'; n.getBoundingClientRect(); }
      n.classList.add('qx-g');
      requestAnimationFrame(function(){ n.style.transform = ''; n.style.borderRadius = ''; n.classList.remove('qx-g0'); });
    }); });
  }).observe(document.body, { childList: true });
  // Close (and the scrim) shrinks the touch sheet back into its link; desktop already shrinks it (spine script)
  Element.prototype.remove = function(){
    var el = this;
    if(el.classList && el.classList.contains('sp-drawer') && el._qxLink) el._qxLink.classList.remove('qx-lk');
    if(!still && !fine && el.classList && el.parentNode === document.body && !el._qxGone &&
       (el.classList.contains('qx-anc') || (el.classList.contains('sp-scrim') && document.querySelector('body > .sp-drawer.qx-anc')))){
      el._qxGone = 1; el.style.pointerEvents = 'none';
      if(el.classList.contains('sp-scrim')){ el.style.transition = 'opacity .3s ease'; el.style.opacity = '0'; setTimeout(function(){ nativeRemove.call(el); }, 320); return; }
      var lk = el._qxLink, r = lk && document.body.contains(lk) ? lk.getBoundingClientRect() : null;
      el.classList.add('qx-g', 'qx-g0');
      if(r && r.width) flip(el, r); else el.style.transform = 'translateY(40px) scale(.96)';
      el.style.opacity = '0';
      setTimeout(function(){ nativeRemove.call(el); }, 420);
      return;
    }
    return nativeRemove.apply(el, arguments);
  };
})();
