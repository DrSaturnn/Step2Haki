/* s137: site layout Phase 2, display layer (claude/pending/S137.md; Jonathan 2026-10-14 "Display layer").
   Presentation only: never adds, removes or rewords brief content; the brief HTML in the page is unchanged.
   1. Diagnostic workup as Test | Result | Means tables per numbered zone (header cells, row spans, group tints).
   2. Clue table column "Next best step" (Jonathan 2026-10-13; was "Next move").
   3. Mnemonic rows: the key text sits in its own cell beside the tinted capital.
   4. Desktop: the current brief's section steps nest under it in the sidebar (fill-to-current-link rule kept). */
(function(){
  'use strict';
  var WIDE = window.matchMedia ? window.matchMedia('(min-width:1101px)') : { matches: true };

  /* ---------- 1. workup tables ---------- */
  function workups(root){
    (root || document).querySelectorAll('figure.w5a').forEach(function(fig){
      if(fig.classList.contains('ax-w5tab')) return;
      fig.classList.add('ax-w5tab');
      fig.querySelectorAll(':scope > .w5t').forEach(function(t){
        var h = document.createElement('div');
        h.className = 'ax-w5h'; h.setAttribute('aria-hidden', 'true');
        h.innerHTML = '<span>Test</span><span>Result</span><span>Means</span>';
        t.insertBefore(h, t.firstChild);
        var z = 0;
        t.querySelectorAll(':scope > .w5b').forEach(function(b){
          var f = b.nextElementSibling;
          var n = f && f.classList.contains('w5f') ? f.querySelectorAll(':scope > .w5fd').length : 0;
          b.style.setProperty('--axn', String(Math.max(1, n)));
          if(z % 2 === 0){ b.classList.add('ax-z'); if(n) f.classList.add('ax-z'); }
          if(!n) b.classList.add('ax-solo');
          z++;
        });
      });
    });
  }

  /* ---------- 2. "Next best step" ---------- */
  var OLD = 'Next move', NEW = 'Next best step';
  function nextBest(root){
    (root || document).querySelectorAll('.sp-dx th, .sp-dx td[data-label]').forEach(function(c){
      if(c.tagName === 'TH' && c.textContent.trim() === OLD && c.children.length === 0) c.textContent = NEW;
      if(c.getAttribute('data-label') === OLD) c.setAttribute('data-label', NEW);
    });
  }

  /* ---------- 3. mnemonic rows ---------- */
  function mnem(root){
    (root || document).querySelectorAll('dl.rows.mnem').forEach(function(dl){
      dl.classList.add('ax-mn');
      var h = dl.previousElementSibling;
      if(h && h.tagName === 'H5' && !h.classList.contains('tsec')) h.classList.add('ax-mnh');
      else dl.classList.add('ax-mn-solo');
      /* every term is its capital alone (LMNOP): phone keeps letter and description on one row */
      var bare = true;
      dl.querySelectorAll(':scope > dt').forEach(function(dt){ var m = dt.querySelector('b.mn'); if(!m || dt.textContent.trim() !== m.textContent.trim()) bare = false; });
      if(bare) dl.classList.add('ax-mn-bare');
    });
  }

  function all(root){ workups(root); nextBest(root); mnem(root); }

  /* ---------- 4. steps nested in the sidebar ---------- */
  var home = null;   // where the moved rail came from: {rail, parent, next}
  function putBack(){
    if(!home) return;
    if(home.next && home.next.parentNode === home.parent) home.parent.insertBefore(home.rail, home.next);
    else home.parent.appendChild(home.rail);
    home.rail.classList.remove('ax-nr'); home = null;
  }
  function nest(){
    var host = document.getElementById('navlinks');
    if(!host) return;
    document.body.classList.toggle('ax-nest', WIDE.matches);
    if(!WIDE.matches){ putBack(); return; }
    var a = host.querySelector('a.active');
    if(!a){ putBack(); return; }
    var id = (a.getAttribute('href') || '').slice(1), b = id ? document.getElementById(id) : null;
    var rail = b ? b.querySelector(':scope > .bb-rail') : null;
    if(home && home.rail === rail && rail.previousElementSibling === a) return;
    putBack();
    if(!rail) return;
    if(a.classList.contains('axsx-c')){   // its system is folded: open it, as the sidebar does when a brief becomes current
      var h = a.previousElementSibling; while(h && !h.classList.contains('sect')) h = h.previousElementSibling;
      if(h && h.getAttribute('aria-expanded') !== 'true') h.click();
    }
    home = { rail: rail, parent: rail.parentNode, next: rail.nextSibling };
    rail.classList.add('ax-nr');
    a.parentNode.insertBefore(rail, a.nextSibling);
    // keep the current link and its steps in view inside the sidebar's own scroll box only
    var box = host.closest('.navscroll') || (function(el){ while(el && el !== document.body){ var o = getComputedStyle(el).overflowY; if(o === 'auto' || o === 'scroll') return el; el = el.parentElement; } return null; })(host);
    if(box){
      var br = box.getBoundingClientRect(), ar = a.getBoundingClientRect(), rr = rail.getBoundingClientRect();
      if(ar.top < br.top + 8) box.scrollTop += ar.top - br.top - 8;
      else if(rr.bottom > br.bottom - 8) box.scrollTop += Math.min(rr.bottom - br.bottom + 8, ar.top - br.top - 8);
    }
    // the page's rail script sizes the fill from the links' positions on its next frame
    window.dispatchEvent(new Event('scroll'));
  }

  // the toolbar reads the current section from the brief's rail, which may now sit in the sidebar
  window.axRailOf = function(b){ return home && home.parent === b ? home.rail : null; };

  function init(){
    all(document);
    var host = document.getElementById('navlinks');
    if(host) new MutationObserver(function(){ requestAnimationFrame(nest); }).observe(host, { subtree: true, attributes: true, attributeFilter: ['class'] });
    if(WIDE.addEventListener) WIDE.addEventListener('change', nest);
    nest();
    // drawers and hover cards add brief copies to the page: lay them out the same way
    new MutationObserver(function(ms){
      ms.forEach(function(m){ m.addedNodes.forEach(function(n){ if(n.nodeType === 1 && n.querySelector) all(n); }); });
    }).observe(document.body, { childList: true, subtree: true });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
