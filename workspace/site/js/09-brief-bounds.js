/* Brief boundaries. Builds, for every brief: a sticky section rail (>1100px) and an end cap; below 1100px it reports the
   brief being read and its current section as brief:step {el, title, secs, cur, p, past} for the phone header (05-phone).
   Sections: spine briefs follow their stepper (absent steps greyed); other briefs use their section headings, after an Overview
   entry for the top of the brief. Built at load from the page itself; nothing is stored. Drawer clones strip both (spine.js). */
(function(){
  'use strict';
  var WIDE = window.matchMedia('(min-width:1101px)');
  var briefs = [], byId = {}, live = new Set(), active = null, raf = 0;

  function txt(n){ return (n ? n.textContent : '').replace(/\s+/g, ' ').trim(); }
  function sectionsOf(b){
    var out = [], step = b.querySelector('.sp-step');
    if(step){
      step.querySelectorAll('a').forEach(function(a){
        var n = txt(a.querySelector('b')), l = txt(a.querySelector('span')) || txt(a);
        if(a.classList.contains('off')){ out.push({n:n, l:l, el:null}); return; }
        var id = (a.getAttribute('href') || '').slice(1), el = id && document.getElementById(id);
        if(el && b.contains(el)) out.push({n:n, l:l, el:el});
      });
      return out;
    }
    out.push({n:'', l:'Overview', el:b});
    b.querySelectorAll('h5.tsec, h5.authored-hdr').forEach(function(h, i){
      if(h.closest('.sp-drawer')) return;
      if(!h.id) h.id = b.id + '-bb' + i;
      out.push({n:'', l:txt(h), el:h});
    });
    return out;
  }
  function go(el){
    if(el) AX.brief.ensure(el);
    if(!el) return;
    el.scrollIntoView({behavior: 'smooth', block: 'start'});
    if(el.id) history.replaceState(null, '', '#' + el.id);
  }
  function nextVisible(b){
    var all = document.querySelectorAll('main .brief[id]'), i = Array.prototype.indexOf.call(all, b.el);
    for(var j = i + 1; j < all.length; j++){
      if(all[j].style.display === 'none' || (WIDE.matches && all[j].offsetParent === null)) continue;
      if(byId[all[j].id]) return byId[all[j].id];
      var h = AX.brief.content(all[j]).querySelector('h4');
      return {el: all[j], title: h ? txt(h) : all[j].id};
    }
    return null;
  }

  function build(b){
    var h4 = b.querySelector('h4'); if(!h4) return null;
    var title = txt(h4), secs = sectionsOf(b), rec = {el:b, h4:h4, title:title, secs:secs, cur:-1};
    // rail
    var rail = document.createElement('nav'); rail.className = 'bb-rail'; rail.setAttribute('aria-label', 'Sections of ' + title);
    rail.innerHTML = '<p class="bb-rt"></p><div class="bb-rl"><span class="bb-fill"></span></div>';
    rail.querySelector('.bb-rt').textContent = title;
    var rl = rail.querySelector('.bb-rl');
    secs.forEach(function(s){
      var a = document.createElement('a');
      if(s.el){ a.href = '#' + s.el.id; a.addEventListener('click', function(e){ e.preventDefault(); go(s.el); }); }
      else { a.className = 'off'; a.setAttribute('aria-disabled', 'true'); }
      if(s.n){ var nb = document.createElement('b'); nb.textContent = s.n; a.appendChild(nb); }
      a.appendChild(document.createTextNode(s.l)); rl.appendChild(a);
    });
    b.insertBefore(rail, b.firstChild);
    b.classList.add('bb-r');
    // end cap
    var end = document.createElement('div'); end.className = 'bb-end';
    end.innerHTML = '<span class="bb-el">End of <b></b></span><span class="bb-go"><button type="button" class="bb-top">Back to top ↑</button><a class="bb-next" href="#">Next: <b></b> →</a></span>';
    end.querySelector('.bb-el b').textContent = title;
    end.querySelector('.bb-top').addEventListener('click', function(){ go(b); });
    var nx = end.querySelector('.bb-next');
    // desktop scrolls to the next brief; on phones the link's hash opens it (05-phone)
    nx.addEventListener('click', function(e){ if(!WIDE.matches) return; e.preventDefault(); var n = nextVisible(rec); if(n) go(n.el); });
    b.appendChild(end);
    rec.rail = rail; rec.fill = rail.querySelector('.bb-fill'); rec.links = [].slice.call(rl.querySelectorAll('a')); rec.next = nx;
    return rec;
  }
  function railFit(rec){ rec.rail.style.marginBottom = (-rec.rail.offsetHeight) + 'px'; }
  /* the rail fill ends at the highlighted section's link (Jonathan 2026-10-13, tics rail as the model), not at the
     brief's scroll height: sections differ in length while the links are evenly spaced, so a height-based fill
     disagreed with the highlight */
  function fillTo(rec, cur){
    var rl = rec.fill.parentNode, r0 = rl.getBoundingClientRect(), a = rec.links[cur];
    if(!a) return;
    var off = rec.fill.getBoundingClientRect().top - r0.top;   // the fill starts a few px down its track
    rec.fill.style.height = Math.max(0, a.getBoundingClientRect().bottom - r0.top - off).toFixed(1) + 'px';
  }

  function update(){
    raf = 0;
    var vh = window.innerHeight, wide = WIDE.matches, th = wide ? 120 : (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--ph-top')) || 64), pick = null;
    live.forEach(function(rec){
      var r = rec.el.getBoundingClientRect();
      if(r.top <= th && r.bottom > th) pick = rec;
    });
    active = pick;
    if(!pick){ if(!wide) AX.emit('brief:step', null); return; }
    var r = pick.el.getBoundingClientRect();
    var p = Math.max(0, Math.min(1, (vh - r.top) / r.height));
    // current section: the last one whose heading has reached the threshold
    var cur = 0;
    var sth = Math.max(th + 8, vh * 0.32);   // s141: a step is current once its heading passes 32% of the window (the Lithium Glance mockup), not 120 px; s164: on phone too (was th + 8, under the bar, so a heading in view still showed the step before it), the same line as the sidebar index
    pick.secs.forEach(function(s, i){ if(s.el && s.el !== pick.el && s.el.getBoundingClientRect().top <= sth) cur = i; });
    if(pick.secs[0] && !pick.secs[0].el){ /* spine brief whose first step is absent: never */ }
    if(wide) fillTo(pick, cur);
    if(cur !== pick.cur){
      pick.cur = cur;
      pick.links.forEach(function(a, i){ a.classList.toggle('cur', i === cur); });
    }
    var n = nextVisible(pick);
    if(n){ pick.next.hidden = false; pick.next.querySelector('b').textContent = n.title; pick.next.setAttribute('href', '#' + n.el.id); } else pick.next.hidden = true;
    if(!wide) AX.emit('brief:step', {el: pick.el, title: pick.title, secs: pick.secs, cur: cur, p: p, past: pick.h4.getBoundingClientRect().bottom < 0, go: go});
  }
  function kick(){ if(!raf) raf = requestAnimationFrame(update); }

  function init(){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ var rec = byId[e.target.id]; if(!rec) return; if(e.isIntersecting) live.add(rec); else live.delete(rec); });
      kick();
    }, {rootMargin: '0px'});
    AX.brief.each('brief-bounds', function(b){
      if(!b.id || !b.closest('main') || b.querySelector(':scope > .bb-rail')) return;
      var rec = build(b); if(!rec) return;
      briefs.push(rec); byId[b.id] = rec;
      io.observe(rec.el); if(WIDE.matches) railFit(rec);
      kick();
    });
    window.addEventListener('scroll', kick, {passive: true});
    window.addEventListener('resize', function(){ briefs.forEach(function(rec){ rec.rail.style.marginBottom = ''; if(WIDE.matches) railFit(rec); }); kick(); });
    kick();
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(init, 0); });
  else setTimeout(init, 0);
})();
