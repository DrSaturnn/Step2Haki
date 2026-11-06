/* Workup 5a connectors: start each finding's connector 6 px after the end of its first line. */
(function(){
  'use strict';
  function place(root){
    (root || document).querySelectorAll('.w5a .w5fd').forEach(function(fd){
      var t = fd.querySelector('.t'), ld = fd.querySelector('.ld'); if(!t || !ld) return;
      if(!document.createRange) return;
      var r = document.createRange(); if(typeof r.getClientRects !== 'function') return;   /* CSS fallback: connector from the column edge */
      r.selectNodeContents(t);
      var rects = r.getClientRects(); if(!rects || !rects.length) return;
      var first = rects[0], box = fd.getBoundingClientRect();
      for(var i = 1; i < rects.length; i++){ if(Math.abs(rects[i].top - first.top) < 2 && rects[i].right > first.right) first = rects[i]; }
      fd.style.setProperty('--ld', Math.round(first.right - box.left + 6) + 'px');
    });
  }
  /* Study mode: findings under a band wait until that band's test is revealed. */
  function gate(root){
    var study = document.body.classList.contains('study');
    (root || document).querySelectorAll('.w5a .w5b').forEach(function(b){
      var f = b.nextElementSibling; if(!f || !f.classList.contains('w5f')) return;
      var m = b.querySelector('.w5om'), wait = study && !(m && m.dataset.revealed === '1');
      if(f.classList.contains('w5-wait') !== wait) f.classList.toggle('w5-wait', wait);
      if(f.inert !== wait) f.inert = wait;
      if(wait) f.setAttribute('aria-hidden', 'true'); else f.removeAttribute('aria-hidden');
    });
  }
  var queued = false;
  function soon(){ if(queued) return; queued = true; requestAnimationFrame(function(){ queued = false; place(); gate(); }); }
  function init(){
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(soon);
    window.addEventListener('resize', soon);
    var ro = window.ResizeObserver ? new ResizeObserver(soon) : null;
    new MutationObserver(soon).observe(document.body, { attributes: true, attributeFilter: ['class'] });
    AX.brief.each('workup-connectors', function(b){
      place(b); gate(b);
      b.querySelectorAll('.w5a').forEach(function(f){
        if(ro) ro.observe(f);
        new MutationObserver(soon).observe(f, { subtree: true, attributes: true, attributeFilter: ['data-revealed'] });
      });
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
