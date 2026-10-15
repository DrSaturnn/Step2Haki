/* s143: the Lithium Glance mockup's sidebar as one component (Jonathan 2026-10-15). Presentation only: no text is
   invented. The old #navlinks list stays in the page, hidden, because the shelf, Board-style only and search scripts
   write their filters onto it; this list mirrors its visibility and counts and draws the mockup's parts:
   systems that fold (chevron, name, count), brief tiles, and under the current brief its step rail with the fill and
   one lens that glides between steps. A step is current once its heading passes 32% of the window (the mockup's
   rule); a click on a step takes effect at once and the spy waits 0.9 s. The list keeps the current step in view.
   The switches the mockup's sidebar does not carry (shelf, Board-style only, Recall, themes, accent, the change log)
   move into a display sheet behind the round button in the brand row. */
(function(){
  "use strict";
  var nav = document.getElementById('nav'), old = document.getElementById('navlinks');
  if(!nav || !old) return;
  window.AXN = 1;
  var WIDE = window.matchMedia('(min-width:1101px)');
  var SVG_CHEV = '<svg width="8" height="12" viewBox="0 0 9 14" aria-hidden="true"><path d="M2 2l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>';
  var SVG_SRCH = '<svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.8"></circle><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"></path></svg>';
  var SVG_CFG = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4.5h7M12 4.5h2M2 11.5h2M7 11.5h7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><circle cx="10.5" cy="4.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="5.5" cy="11.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';
  function el(tag, cls, html){ var e = document.createElement(tag); if(cls) e.className = cls; if(html != null) e.innerHTML = html; return e; }
  function txt(n){ return (n.textContent || '').replace(/\s+/g, ' ').trim(); }
  function shown(n){ return n && n.style.display !== 'none' && !n.hidden; }

  /* ---------- head: brand row, display button, search pill ---------- */
  function head(){
    var top = document.getElementById('navtop'), brand = nav.querySelector('.brand'), search = document.getElementById('search');
    if(!top) return;
    var h = el('div', 'axn-head');
    var name = brand && brand.querySelector('h1') ? txt(brand.querySelector('h1')) : 'Step2Haki';
    var sub = brand ? Array.prototype.filter.call(brand.querySelectorAll('p'), function(p){ return !p.classList.contains('axbuild'); })[0] : null;
    h.appendChild(el('div', 'axn-mark', 'S2'));
    var t = el('div'); t.appendChild(el('div', 'axn-nm')).textContent = name;
    t.appendChild(el('div', 'axn-sub')).textContent = sub ? txt(sub) : '';
    h.appendChild(t);
    var tools = el('div', 'axn-tools');
    var cfg = el('button', 'axn-cfg', SVG_CFG); cfg.type = 'button'; cfg.id = 'axcfg';
    cfg.setAttribute('aria-label', 'Display settings'); cfg.setAttribute('aria-expanded', 'false'); cfg.setAttribute('aria-controls', 'axdisp');
    tools.appendChild(cfg);
    var x = top.querySelector('.navclose'); if(x) tools.appendChild(x);
    h.appendChild(tools);
    top.insertBefore(h, top.firstChild);
    if(search){
      var pill = el('div', 'axn-srch', SVG_SRCH);
      top.insertBefore(pill, search); pill.appendChild(search);
      var ph = function(){ search.setAttribute('placeholder', 'Search topics, findings, drugs'); };
      ph(); window.addEventListener('load', ph);
      new MutationObserver(function(){ if(search.getAttribute('placeholder') !== 'Search topics, findings, drugs') ph(); }).observe(search, {attributes: true, attributeFilter: ['placeholder']});
    }
    sheet(cfg, brand);
  }

  /* ---------- the display sheet ---------- */
  function sheet(btn, brand){
    var s = el('div'); s.id = 'axdisp'; s.setAttribute('role', 'dialog'); s.setAttribute('aria-label', 'Display settings'); s.tabIndex = -1;
    s.appendChild(el('div', 'axd-h')).textContent = 'Display';
    nav.appendChild(s);
    function fill(){
      var sp = nav.querySelector('#navscroll > .shelfpick'), md = document.getElementById('modes');
      if(sp && sp.parentNode !== s) s.appendChild(sp);
      if(md && md.parentNode !== s) s.appendChild(md);
      var b = brand && brand.querySelector('.axbuild'); if(b && b.parentNode !== s) s.appendChild(b);
      // the switches' labels read as sentences here, like the rest of the sheet (presentation only)
      s.querySelectorAll('#modes .nm').forEach(function(n){ var t = n.textContent; if(t && t === t.toUpperCase()) n.textContent = t.charAt(0) + t.slice(1).toLowerCase(); });
    }
    fill(); window.addEventListener('load', fill);
    function set(on){
      s.classList.toggle('on', on); btn.setAttribute('aria-expanded', on ? 'true' : 'false');
      if(on){ fill(); try{ s.focus({preventScroll: true}); }catch(e){} }
    }
    btn.addEventListener('click', function(e){ e.stopPropagation(); set(!s.classList.contains('on')); });
    document.addEventListener('click', function(e){ if(s.classList.contains('on') && !s.contains(e.target) && e.target !== btn) set(false); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && s.classList.contains('on')){ e.stopPropagation(); set(false); try{ btn.focus(); }catch(x){} } }, true);
    // the change log button lives in the sheet now; opening the log closes the sheet
    s.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('.axlogbtn')) set(false); });
  }

  /* ---------- list ---------- */
  var list, groups = [], byId = {}, cur = {brief: null, step: -1}, rail = null, lock = 0, open = {};
  function build(){
    var host = document.getElementById('navscroll') || old.parentNode;
    list = el('div'); list.id = 'axn'; list.setAttribute('role', 'navigation'); list.setAttribute('aria-label', 'All briefs');
    host.insertBefore(list, old);
    var g = null, box = null;
    Array.prototype.slice.call(old.children).forEach(function(n){
      if(n.classList.contains('sect')){
        var ct = n.querySelector('.count'), name = txt(n).replace(ct ? txt(ct) : '', '').trim();
        var b = el('button', 'axn-sys', SVG_CHEV + '<span class="nm"></span><span class="ct"></span>'); b.type = 'button';
        b.querySelector('.nm').textContent = name; b.querySelector('.ct').textContent = ct ? txt(ct) : '';
        var dz = el('div', 'axn-dz'), dzi = el('div', 'axn-dzi'); box = el('div', 'axn-dzc');
        dzi.appendChild(box); dz.appendChild(dzi); list.appendChild(b); list.appendChild(dz);
        g = {src: n, cnt: ct, btn: b, dz: dz, items: [], name: name};
        groups.push(g);
        b.addEventListener('click', function(gg){ return function(){ fold(gg, gg.btn.getAttribute('aria-expanded') !== 'true', true); }; }(g));
        fold(g, false, false);
      } else if(g && n.classList.contains('navsub')){
        var l = el('div', 'axn-lbl'); l.textContent = txt(n); box.appendChild(l); g.items.push({src: n, el: l});
      } else if(g && n.tagName === 'A' && /^#/.test(n.getAttribute('href') || '')){
        var id = n.getAttribute('href').slice(1);
        var a = el('a', 'axn-b'); a.href = '#' + id; a.textContent = txt(n); a.dataset.id = id;
        box.appendChild(a); var it = {src: n, el: a, id: id, g: g}; g.items.push(it); byId[id] = it;
      }
    });
    list.addEventListener('click', click);
    mirror();
    new MutationObserver(function(){ requestAnimationFrame(mirror); }).observe(old, {subtree: true, attributes: true, attributeFilter: ['style', 'hidden'], childList: true, characterData: true});
  }
  function fold(g, on, anim){
    if(!anim){ list.classList.add('axn-still'); }
    g.btn.setAttribute('aria-expanded', on ? 'true' : 'false'); g.dz.classList.toggle('on', on); open[g.name] = on;
    if(!anim){ void list.offsetHeight; requestAnimationFrame(function(){ list.classList.remove('axn-still'); }); }
  }
  // mirror the filters the old list carries (shelf, Board-style only, search) and its live counts
  function mirror(){
    groups.forEach(function(g){
      g.btn.hidden = !shown(g.src); g.dz.hidden = !shown(g.src);
      if(g.cnt) g.btn.querySelector('.ct').textContent = txt(g.cnt);
      g.items.forEach(function(it){ it.el.hidden = !shown(it.src); });
    });
  }

  /* ---------- the current brief and its steps ---------- */
  function briefs(){ return Array.prototype.filter.call(document.querySelectorAll('main .wrap > .brief'), function(b){ return b.offsetParent !== null; }); }
  function stepsOf(b){
    var r = (window.axRailOf && window.axRailOf(b)) || b.querySelector(':scope > .bb-rail');
    if(!r) return [];
    return Array.prototype.map.call(r.querySelectorAll('.bb-rl a'), function(a){
      var n = a.querySelector('b'), label = '';
      Array.prototype.forEach.call(a.childNodes, function(c){ if(c.nodeType === 3) label += c.nodeValue; });
      label = label.replace(/\s+/g, ' ').trim(); if(label === 'Urgent') label = 'Urgent risks';
      var href = a.getAttribute('href') || '';
      return {n: n ? txt(n) : '', label: label, id: href.charAt(0) === '#' ? href.slice(1) : '', off: a.classList.contains('off') || !href};
    });
  }
  function drawRail(it){
    if(rail){ rail.root.remove(); rail = null; }
    if(!it) return;
    var b = document.getElementById(it.id), steps = b ? stepsOf(b) : [];
    if(!steps.length) return;
    var root = el('div', 'axn-rail'), trk = el('div', 'axn-trk'), fill = el('div', 'axn-fill'), rows = el('div', 'axn-rows'), lens = el('div', 'axn-lens'), rl = el('div', 'axn-rl');
    lens.setAttribute('aria-hidden', 'true'); trk.appendChild(fill); rows.appendChild(lens); rows.appendChild(rl); root.appendChild(trk); root.appendChild(rows);
    var links = steps.map(function(s, i){
      var a = el('a', 'axn-s', '<span class="n"></span><span class="l"></span><span class="u"></span>');
      a.querySelector('.n').textContent = s.n; a.querySelector('.l').textContent = s.label;
      if(s.off){ a.setAttribute('aria-disabled', 'true'); a.querySelector('.u').textContent = 'Not used'; a.tabIndex = -1; }
      else a.href = '#' + s.id;
      a.dataset.i = i; rl.appendChild(a); return a;
    });
    it.el.parentNode.insertBefore(root, it.el.nextSibling);
    rail = {root: root, fill: fill, lens: lens, links: links, steps: steps, id: it.id};
    list.classList.add('axn-still'); paint(); void root.offsetHeight;
    requestAnimationFrame(function(){ list.classList.remove('axn-still'); });
  }
  function paint(){
    if(!rail) return;
    var i = cur.step < 0 ? 0 : cur.step, a = rail.links[i]; if(!a) return;
    rail.links.forEach(function(l, j){ if(j === cur.step) l.setAttribute('aria-current', 'step'); else l.removeAttribute('aria-current'); });
    rail.lens.style.transform = 'translateY(' + a.offsetTop + 'px)';
    rail.fill.style.height = (a.offsetTop + a.offsetHeight) + 'px';
    rail.lens.style.opacity = cur.step < 0 ? '0' : '1';
  }
  function spy(){
    if(Date.now() < lock || document.body.classList.contains('navopen')) return;   // the open phone index fixes the body, so the page reads as scrolled to the top
    var y = window.innerHeight * 0.32, bs = briefs(), b = null;
    for(var i = 0; i < bs.length; i++){ if(bs[i].getBoundingClientRect().top < y) b = bs[i]; else break; }
    if(!b && bs.length) b = bs[0];
    var id = b ? b.id : null, step = -1;
    if(id && (!rail || rail.id !== id)) setBrief(id);
    if(rail){
      rail.steps.forEach(function(s, j){ if(s.off || !s.id) return; var t = document.getElementById(s.id); if(t && t.offsetParent !== null && t.getBoundingClientRect().top < y) step = j; });
      var d = document.scrollingElement || document.documentElement;
      if(d.scrollTop + window.innerHeight >= d.scrollHeight - 4) step = rail.steps.length - 1;
      if(step < 0) step = 0;
    }
    if(step !== cur.step){ cur.step = step; paint(); keep(rail && rail.links[step], true); }
  }
  function setBrief(id){
    var it = byId[id], prev = cur.brief;
    if(prev && byId[prev]) byId[prev].el.removeAttribute('aria-current');
    cur.brief = id; cur.step = -1;
    if(!it){ drawRail(null); return; }
    it.el.setAttribute('aria-current', 'page');
    if(it.g.btn.getAttribute('aria-expanded') !== 'true') fold(it.g, true, false);
    drawRail(it);
    keep(it.el, !!prev, true);
  }
  function scroller(){ var s = document.getElementById('navscroll'); return s && s.scrollHeight > s.clientHeight + 4 ? s : null; }
  // the mockup's rule: a new brief lands 70 px below the list's top; a step outside the band is brought to the middle
  function keep(n, smooth, top){
    var s = scroller(); if(!s || !n || nav.classList.contains('sxon')) return;
    var lr = s.getBoundingClientRect(), r = n.getBoundingClientRect();
    if(!lr.height) return;
    if(top){
      var end = rail ? rail.root.getBoundingClientRect().bottom : r.bottom;
      if(r.top < lr.top + 20 || end > lr.bottom - 30) s.scrollTo({top: s.scrollTop + r.top - lr.top - 70, behavior: smooth ? 'smooth' : 'auto'});
      return;
    }
    if(r.bottom > lr.bottom - 30 || r.top < lr.top + 20) s.scrollTo({top: s.scrollTop + r.top - lr.top - lr.height / 2, behavior: smooth ? 'smooth' : 'auto'});
  }

  /* ---------- going to a brief or a step ---------- */
  var moved = false, seated = null;
  // held until the target has stayed put for 20 frames, the time runs out, the reader moves or a newer link is followed
  function seat(id, until, held){
    var t = document.getElementById(id); if(!t || decodeURIComponent(location.hash.slice(1)) !== id) return;
    var want = WIDE.matches ? (t.classList.contains('brief') ? 0 : 24) : (parseFloat(getComputedStyle(t).scrollMarginTop) || 0);
    var top = t.getBoundingClientRect().top;
    if(Math.abs(top - want) > 2){ held = 0; window.scrollTo({top: window.scrollY + top - want, behavior: 'instant'}); }   // instant: a smooth scroll restarted every frame never arrives
    else held = (held || 0) + 1;
    if(held >= 20) seated = id;
    if(held < 20 && Date.now() < until && !moved) requestAnimationFrame(function(){ seat(id, until, held); });
  }
  function go(id, stepIndex){
    var x = nav.querySelector('.navclose');
    if(document.body.classList.contains('navopen') && x) x.click();
    // the page's own hash handling pins an off-shelf brief, scrolls to it and settles it once lazy briefs above render
    requestAnimationFrame(function(){
      if(location.hash !== '#' + id) location.hash = id;
      else { try{ window.dispatchEvent(new HashChangeEvent('hashchange')); }catch(e){} }
      // briefs above the target render as the page passes them and change height, so the target is seated until it holds
      moved = false; requestAnimationFrame(function(){ seat(id, Date.now() + 1500); });
    });
    if(stepIndex != null){ lock = Date.now() + 900; cur.step = stepIndex; paint(); }
  }
  function click(e){
    var a = e.target.closest && e.target.closest('a'); if(!a || !list.contains(a)) return;
    if(e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault();
    if(a.getAttribute('aria-disabled') === 'true') return;
    if(a.classList.contains('axn-s')) go(a.getAttribute('href').slice(1), +a.dataset.i);
    else { go(a.dataset.id); }
  }

  /* ---------- wiring ---------- */
  var q = 0;
  function kick(){ if(!q) q = requestAnimationFrame(function(){ q = 0; spy(); }); }
  function init(){
    if(!document.getElementById('navtop')) return setTimeout(init, 30);   // the page's nav script builds the head first
    nav.classList.add('axn');
    head(); build();
    if(!document.getElementById('axtopfade')){ var f = el('div'); f.id = 'axtopfade'; f.setAttribute('aria-hidden', 'true'); document.body.appendChild(f); }
    ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function(ev){ window.addEventListener(ev, function(){ moved = true; }, {passive: true}); });
    window.addEventListener('scroll', kick, {passive: true});
    window.addEventListener('resize', function(){ paint(); kick(); });
    // opening the phone index brings the current brief into view
    new MutationObserver(function(){ if(document.body.classList.contains('navopen') && cur.brief && byId[cur.brief]) keep(byId[cur.brief].el, false, true); })
      .observe(document.body, {attributes: true, attributeFilter: ['class']});
    var h = decodeURIComponent(location.hash.slice(1));
    if(h && document.getElementById(h)){ seat(h, Date.now() + 3500); window.addEventListener('load', function(){ if(!moved && seated !== h) seat(h, Date.now() + 1500); }); }
    window.addEventListener('resize', function(){ moved = true; });   // a new window size is the reader's (or a capture's) layout, not a landing
    kick(); window.addEventListener('load', kick);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
