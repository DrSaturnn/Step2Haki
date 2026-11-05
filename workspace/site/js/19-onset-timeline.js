/* s148b: onset timeline placement (Jonathan 2026-10-18, "the timeline boxes should adapt to fit all text within it";
   claude/pending/SITE_BODY_GLANCE.md, Decided D). After layout and on every resize: walk the events left to right and put
   each card on the lowest tier where it overlaps no card (8 px gap), its leader line crosses no card below it, and it
   covers no leader line from above; each tier sits on the tallest card below it and the chart height follows. If the
   cards cannot fit at a width, the figure takes the phone list layout. Phone and study mode keep their list layouts. */
(function(){
  var GAP = 8, BASE = 48, AXIS = 31, MAXT = 5, PAD = 4, LEAD = 4, WIDTHS = [280, 240, 210, 180];
  var phone = window.matchMedia('(max-width:640px)');
  function reset(f){
    var fig = f.closest('figure.sp-on');
    if(fig) fig.classList.remove('sp-on-list');
    f.classList.remove('sp-on-js'); f.style.height = ''; f.style.removeProperty('--cmw');
    f.querySelectorAll('.sp-on-ev > li').forEach(function(li){
      ['--cx', '--cb', '--lh'].forEach(function(k){ li.style.removeProperty(k); });
    });
  }
  // a search over tiers and left edges, events taken left to right, nearest the preferred spot first: a card overlaps no
  // card on its tier (8 px gap); its own leader line stays inside it, 12 px in from each side; its leader crosses no card
  // below it and it covers no leader line from a card above (events at the same time share one line); null if none fits
  function layout(items, W){
    var placed = [], nodes = 0;
    items.forEach(function(it){ it.pref = it.al === 'r' ? it.x - it.w : it.al === 'c' ? it.x - it.w / 2 : it.x - 14; });
    function same(a, b){ return Math.abs(a.x - b.x) < 2; }
    function ok(it, t, L){
      var R = L + it.w;
      return placed.every(function(o){
        if(o.t === t) return R + GAP <= o.L || o.R + GAP <= L;
        if(same(o, it)) return true;
        if(o.t < t) return it.x < o.L - LEAD || it.x > o.R + LEAD;
        return o.x < L - LEAD || o.x > R + LEAD;
      });
    }
    function go(i){
      if(i === items.length) return true;
      if(++nodes > 20000) return false;
      var it = items[i];
      if(!it.w || it.w > W) return false;
      var lo = Math.max(0, it.x - it.w + 12), hi = Math.min(W - it.w, it.x - 12);
      if(lo > hi) return false;
      var cand = [it.pref, lo, hi];
      placed.forEach(function(o){ cand.push(o.L - GAP - it.w, o.R + GAP, o.x - LEAD - it.w, o.x + LEAD + 0.5); });
      items.slice(i + 1).forEach(function(o){ cand.push(o.x - LEAD - 0.5 - it.w); });   // room for later leader lines
      cand = cand.map(function(L){ return Math.max(lo, Math.min(hi, L)); })
        .sort(function(a, b){ return Math.abs(a - it.pref) - Math.abs(b - it.pref); })
        .filter(function(L, k, A){ return A.indexOf(L) === k; });
      for(var t = 0; t < MAXT; t++){
        for(var c = 0; c < cand.length; c++){
          if(!ok(it, t, cand[c])) continue;
          it.t = t; it.L = cand[c]; it.R = cand[c] + it.w; placed.push(it);
          if(go(i + 1)) return true;
          placed.pop();
        }
      }
      return false;
    }
    if(!go(0)) return null;
    var tiers = [];
    items.forEach(function(o){ (tiers[o.t] = tiers[o.t] || []).push(o); });
    return tiers;
  }
  function place(f){
    var W = f.clientWidth;
    if(!W) return;                 // not laid out (hidden, or mid-capture): keep the last placement
    reset(f);
    f._w = W;
    if(phone.matches || document.body.classList.contains('study')) return;
    var fig = f.closest('figure.sp-on'), tiers = null, items = [];
    for(var m = 0; !tiers && m < WIDTHS.length; m++){   // narrower cards, more lines, before giving up the chart
      f.style.setProperty('--cmw', WIDTHS[m] + 'px');
      items = [].map.call(f.querySelectorAll('.sp-on-ev > li'), function(li){
        var d = li.firstElementChild;
        return {li: li, w: d ? d.offsetWidth : 0, h: d ? d.offsetHeight : 0,
                x: (parseFloat(li.style.getPropertyValue('--x')) || 0) / 100 * W,
                al: li.classList.contains('a-r') ? 'r' : li.classList.contains('a-c') ? 'c' : 'l'};
      }).sort(function(a, b){ return a.x - b.x; });
      tiers = layout(items, W);
    }
    if(!tiers){ f.style.removeProperty('--cmw'); if(fig) fig.classList.add('sp-on-list'); return; }
    var bottom = [], b = BASE;
    for(var k = 0; k < tiers.length; k++){
      tiers[k] = tiers[k] || [];
      bottom[k] = b;
      b += Math.max.apply(null, tiers[k].map(function(o){ return o.h; }).concat([0])) + GAP;
    }
    items.forEach(function(o){
      var cb = bottom[o.t];
      o.li.style.setProperty('--cx', (o.L - o.x) + 'px');
      o.li.style.setProperty('--cb', cb + 'px');
      o.li.style.setProperty('--lh', (cb - AXIS + 6) + 'px');
    });
    f.classList.add('sp-on-js');
    f.style.height = (b - GAP + PAD) + 'px';
  }
  function all(root){ (root || document).querySelectorAll('.sp-on-f').forEach(place); }
  var ro = window.ResizeObserver ? new ResizeObserver(function(es){
    es.forEach(function(e){ var f = e.target; if(f.clientWidth && f.clientWidth !== f._w) place(f); });
  }) : null;
  function watch(root){ (root || document).querySelectorAll('.sp-on-f').forEach(function(f){ if(ro && !f._ro){ f._ro = 1; ro.observe(f); } }); }
  function start(){
    all(); watch();
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ all(); });
    var study = document.body.classList.contains('study');
    new MutationObserver(function(){     // study mode on or off (a class on body only)
      var s = document.body.classList.contains('study');
      if(s !== study){ study = s; all(); }
    }).observe(document.body, {attributes: true, attributeFilter: ['class']});
    new MutationObserver(function(ms){   // a drawer that brings a brief in
      ms.forEach(function(m){
        m.addedNodes.forEach(function(n){
          if(n.nodeType === 1 && (n.matches('.sp-on-f') || n.querySelector('.sp-on-f'))){ var r = n.parentNode || n; watch(r); all(r); }
        });
      });
    }).observe(document.body, {childList: true, subtree: true});
  }
  window.axOnset = all;
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
