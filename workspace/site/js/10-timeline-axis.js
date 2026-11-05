/* Timeline axis labels (s124). Greedy two-line layout for every .rax: each label stays on line 1 if it clears the label
   before it (and the end arrow), else drops to line 2, else hides. Re-runs whenever an axis changes width (panels opening,
   drawers, resizes). Nothing is stored. */
(function(){
  'use strict';
  var GAP = 6;
  function fit(ax){
    var w = ax.clientWidth; if(!w) return;
    var spans = [].slice.call(ax.querySelectorAll(':scope > span'));
    spans.forEach(function(s){ s.classList.remove('lo', 'gone'); });
    ax.classList.remove('fit2');
    var base = ax.getBoundingClientRect().left, em = ax.querySelector(':scope > em');
    var stop = em ? em.getBoundingClientRect().left - base - GAP : w;
    var end = [-1e9, -1e9], two = false;
    spans.forEach(function(s){
      var r = s.getBoundingClientRect(), L = r.left - base, R = r.right - base;
      if(L >= end[0] + GAP && R <= stop){ end[0] = R; }
      else if(L >= end[1] + GAP){ s.classList.add('lo'); end[1] = R; two = true; }
      else { s.classList.add('gone'); }
    });
    if(two) ax.classList.add('fit2');
  }
  var ro = ('ResizeObserver' in window) ? new ResizeObserver(function(es){ es.forEach(function(e){ fit(e.target); }); }) : null;
  var seen = new WeakSet();
  function watch(root){
    (root.querySelectorAll ? root.querySelectorAll('.rax') : []).forEach(function(ax){
      if(seen.has(ax)) return; seen.add(ax);
      if(ro) ro.observe(ax); else fit(ax);
    });
  }
  function init(){
    watch(document);
    new MutationObserver(function(ms){ ms.forEach(function(m){ m.addedNodes.forEach(function(n){ if(n.nodeType === 1) watch(n.matches && n.matches('.rax') ? n.parentNode : n); }); }); })
      .observe(document.body, {childList: true, subtree: true});
    if(!ro) window.addEventListener('resize', function(){ document.querySelectorAll('.rax').forEach(fit); });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
