/* s136: site layout Phase 1 (claude/pending/S136.md). Presentation only; never adds or removes brief text.
   1. Accent setting (Jonathan 2026-10-14): a reader choice under the theme switches, stored per viewer; Slate default.
      Dark theme (Jonathan 2026-10-14): a switch beside Flat theme, stored per viewer (ax-theme), light by default.
   2. Desktop hovers: open on pointer enter, close on leave, stay open once clicked (a second click closes).
   3. Desktop glass toolbar: the current section's number and name, Read and Study, open or close every panel.
   4. Sidebar systems fold and unfold; the system holding the current brief opens itself. */
(function(){
  "use strict";
  var ACC = [['slate','Slate','#3B5B8C'],['indigo','Indigo','#504ED4'],['purple','Purple','#544AC4'],['navy','Navy','#1E3A8A'],
             ['ocean','Ocean','#1D6A8C'],['plum','Plum','#7A3B8F'],['rose','Rose','#AA2E66'],['graphite','Graphite','#4A5060']];
  var KEY = 'ax-accent';
  function load(){ try { return localStorage.getItem(KEY) || 'slate'; } catch(e){ return 'slate'; } }
  function save(k){ try { localStorage.setItem(KEY, k); } catch(e){} }
  function valid(k){ for(var i = 0; i < ACC.length; i++) if(ACC[i][0] === k) return ACC[i]; return null; }
  var root = document.documentElement;

  /* ---------- 1. accent ----------
     Slate needs nothing (the tokens' default). Another choice is set on the page's regions nearest first, a few per
     frame, then on the root, the same way the flat and study switches restyle (s92): one root-wide change restyled
     every brief at once. */
  var cur = valid(load()) ? load() : 'slate';
  var THEME = 'ax-theme', dark = false;
  try { dark = localStorage.getItem(THEME) === 'dark'; } catch(e){}
  if(cur !== 'slate') root.setAttribute('data-axa', cur);
  if(dark) root.setAttribute('data-theme', 'dark');
  /* Each region carries both attributes while a switch walks the page, so the dark accent rule (which needs both on
     one element or the theme on an ancestor) always matches. */
  function mark(c){
    if(cur === 'slate') c.removeAttribute('data-axa'); else c.setAttribute('data-axa', cur);
    if(dark) c.setAttribute('data-theme', 'dark'); else c.removeAttribute('data-theme');
  }
  function markRoot(){ mark(root); }
  var queue = [], busy = false;
  function regions(){
    var out = [];
    (function walk(el){
      for(var c = el.firstElementChild; c; c = c.nextElementSibling){
        if(c.tagName === 'SCRIPT' || c.tagName === 'STYLE') continue;
        if(c.classList.contains('brief') || !c.querySelector('.brief')) out.push(c); else walk(c);
      }
    })(document.body);
    return out;
  }
  function dist(c){
    var r = c.getBoundingClientRect(), h = window.innerHeight || 800;
    if(!r.width && !r.height) return 1e9;
    return r.bottom < 0 ? -r.bottom : (r.top > h ? r.top - h : 0);
  }
  function step(){
    var n = 0;
    while(queue.length && n < 4){ mark(queue.shift()); n++; }
    if(queue.length){ requestAnimationFrame(step); return; }
    markRoot(); busy = false;
  }
  function walkAll(){
    var rs = regions(), near = [], far = [];
    rs.forEach(function(c){ (dist(c) === 0 ? near : far).push(c); });
    near.forEach(mark);
    far.sort(function(a, b){ return dist(a) - dist(b); });
    queue = far;
    if(!busy){ busy = true; requestAnimationFrame(step); }
  }
  function setAccent(k){
    if(!valid(k) || k === cur) return;
    cur = k; save(k); paintSetting(); walkAll();
  }
  function setDark(on){
    if(on === dark) return;
    dark = on; try { localStorage.setItem(THEME, on ? 'dark' : 'light'); } catch(e){}
    paintSetting(); walkAll();
  }
  var box = null, darkBtn = null;
  function paintSetting(){
    if(!box) return;
    box.querySelectorAll('.axsw').forEach(function(b){ var on = b.getAttribute('data-k') === cur; b.setAttribute('aria-checked', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; });
    var a = valid(cur); box.querySelector('.axan').textContent = a ? a[1] : '';
    if(darkBtn) darkBtn.setAttribute('aria-pressed', dark ? 'true' : 'false');
  }
  function setting(){
    var modes = document.getElementById('modes'); if(!modes || modes.querySelector('.axacc')) return;
    darkBtn = document.createElement('button'); darkBtn.type = 'button'; darkBtn.className = 'dark';
    darkBtn.innerHTML = '<span class="track"><span class="knob"></span></span><span class="nm">DARK THEME</span>';
    var flat = modes.querySelector('.flatt'); if(flat) flat.after(darkBtn); else modes.appendChild(darkBtn);
    darkBtn.addEventListener('click', function(){ setDark(!dark); });
    box = document.createElement('div'); box.className = 'axacc'; box.setAttribute('role', 'radiogroup'); box.setAttribute('aria-label', 'Accent color');
    var h = '<span class="nm">ACCENT</span>';
    ACC.forEach(function(a){ h += '<button type="button" class="axsw" role="radio" data-k="' + a[0] + '" title="' + a[1] + '" aria-label="' + a[1] + '" style="--sw:' + a[2] + '"></button>'; });
    box.innerHTML = h + '<span class="axan"></span>';
    modes.appendChild(box);
    box.addEventListener('click', function(e){ var b = e.target.closest('.axsw'); if(b) setAccent(b.getAttribute('data-k')); });
    box.addEventListener('keydown', function(e){
      var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : (e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0);
      if(!d) return; e.preventDefault();
      var i = 0; ACC.forEach(function(a, j){ if(a[0] === cur) i = j; });
      var k = ACC[(i + d + ACC.length) % ACC.length][0]; setAccent(k);
      var nb = box.querySelector('[data-k="' + k + '"]'); if(nb) nb.focus();
    });
    paintSetting();
  }

  /* ---------- 2. hovers stay open once clicked (desktop) ----------
     The spine script opens a card on pointer enter and closes it on leave; a click on its button closed it. Here a
     click on an open, unpinned card pins it instead; a click on a pinned card's button closes it as before. */
  var fine = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var pinned = null;
  function openCard(){ return document.querySelector('body > .sp-card'); }
  if(fine){
    window.addEventListener('click', function(e){
      var p = e.target.closest && e.target.closest('.sp-pop');
      if(!p){ if(pinned && !(e.target.closest && e.target.closest('.sp-card'))) pinned = null; return; }
      var c = openCard();
      if(c && p.getAttribute('aria-expanded') === 'true' && pinned !== c){ pinned = c; e.preventDefault(); e.stopPropagation(); return; }
      if(!c || p.getAttribute('aria-expanded') !== 'true'){ setTimeout(function(){ pinned = openCard(); }, 0); return; }
      pinned = null;
    }, true);
    function keep(e){ var c = openCard(); if(pinned && c === pinned && (e.target === c || (e.target.closest && e.target.closest('.sp-pop') && e.target.closest('.sp-pop').getAttribute('aria-expanded') === 'true'))) e.stopPropagation(); }
    window.addEventListener('mouseout', keep, true);
    window.addEventListener('mouseleave', keep, true);
    window.addEventListener('mouseover', function(e){
      // pointing at another hover while one is pinned opens that one and releases the pin
      var p = e.target.closest && e.target.closest('.sp-pop');
      if(p && pinned && p.getAttribute('aria-expanded') !== 'true') pinned = null;
    }, true);
  }

  /* ---------- 3. glass toolbar (desktop) ---------- */
  var WIDE = window.matchMedia ? window.matchMedia('(min-width:1101px)') : { matches: true };
  var bar = null, raf = 0;
  function currentBrief(){
    var main = document.querySelector('main'); if(!main) return null;
    var r = main.getBoundingClientRect(), x = Math.max(r.left + 40, Math.min(r.left + r.width / 2, window.innerWidth - 40));
    var el = document.elementFromPoint(x, Math.min(140, window.innerHeight / 3));
    return el && el.closest ? el.closest('main .brief') : null;
  }
  function panels(b){ return b ? Array.prototype.slice.call(b.querySelectorAll('details')) : []; }
  function paintBar(){
    raf = 0; if(!bar || !WIDE.matches) return;
    var b = currentBrief(), n = '', label = '', practice = false;
    if(b){
      var a = b.querySelector('.bb-rl a.cur');
      if(a){
        var nb = a.querySelector('b'); n = nb ? nb.textContent.trim() : '';
        label = (a.textContent || '').replace(n, '').trim(); practice = !n;
      }
      if(!label){ var h = b.querySelector('h4'); label = h ? h.textContent.trim() : ''; }
    }
    var cn = bar.querySelector('.axcn'), cl = bar.querySelector('.axcl');
    cn.textContent = n; cn.hidden = !n && !practice; cn.classList.toggle('p', practice);
    if(practice) cn.textContent = 'P';
    cl.textContent = label || 'Step2Haki';
    var ps = panels(b), all = bar.querySelector('.axall');
    all.hidden = !ps.length;
    var seps = bar.querySelectorAll('.axsep'); if(seps[1]) seps[1].hidden = !ps.length;
    all.textContent = ps.length && ps.every(function(d){ return d.open; }) ? 'Collapse all' : 'Expand all';
    bar.classList.toggle('st', document.body.classList.contains('study'));
    bar.querySelector('[data-m="read"]').setAttribute('aria-pressed', document.body.classList.contains('study') ? 'false' : 'true');
    bar.querySelector('[data-m="study"]').setAttribute('aria-pressed', document.body.classList.contains('study') ? 'true' : 'false');
  }
  var late = 0;
  function kick(){
    if(!raf) raf = requestAnimationFrame(paintBar);
    // the section rail marks its current link in its own frame after a scroll; paint once more after it settles
    clearTimeout(late); late = setTimeout(paintBar, 160);
  }
  function toolbar(){
    if(document.getElementById('axbar')) return;
    var edge = document.createElement('div'); edge.id = 'axedge'; edge.setAttribute('aria-hidden', 'true');
    bar = document.createElement('div'); bar.id = 'axbar'; bar.setAttribute('role', 'toolbar'); bar.setAttribute('aria-label', 'Brief controls');
    bar.innerHTML = '<span class="axcur" aria-live="polite"><span class="axcn"></span><span class="axcl"></span></span><span class="axsep"></span>' +
      '<div class="axseg"><span class="axth" aria-hidden="true"></span><button type="button" data-m="read">Read</button><button type="button" data-m="study">Study</button></div>' +
      '<span class="axsep"></span><button type="button" class="axall">Expand all</button>';
    document.body.appendChild(edge); document.body.appendChild(bar);
    bar.addEventListener('click', function(e){
      var t = e.target.closest('button'); if(!t) return;
      var m = t.getAttribute('data-m');
      if(m){
        var want = m === 'study';
        if(document.body.classList.contains('study') !== want){
          // one code path for the study switch: press the sidebar's own control
          var s = document.querySelector('#modes .study');
          if(s) s.click(); else { document.body.classList.toggle('study', want); try { localStorage.setItem('ax-study', want ? '1' : '0'); } catch(err){} }
        }
      } else if(t.classList.contains('axall')){
        var ps = panels(currentBrief()), open = !ps.every(function(d){ return d.open; });
        ps.forEach(function(d){ d.open = open; });
      }
      kick();
    });
    window.addEventListener('scroll', kick, { passive: true });
    window.addEventListener('resize', kick);
    document.addEventListener('toggle', kick, true);
    new MutationObserver(kick).observe(document.body, { attributes: true, attributeFilter: ['class'] });
    kick();
  }

  /* ---------- 4. sidebar systems fold ---------- */
  function groups(){
    var host = document.getElementById('navlinks'), out = [], g = null;
    if(!host) return out;
    Array.prototype.slice.call(host.children).forEach(function(el){
      if(el.classList.contains('sect')){ g = { head: el, items: [] }; out.push(g); }
      else if(g) g.items.push(el);
    });
    return out;
  }
  function setOpen(g, on){
    g.head.setAttribute('aria-expanded', on ? 'true' : 'false');
    g.items.forEach(function(el){ el.classList.toggle('axsx-c', !on); });
  }
  function fold(){
    var nav = document.getElementById('nav'), gs = groups(); if(!nav || !gs.length) return;
    nav.classList.add('axsx');
    gs.forEach(function(g){
      g.head.setAttribute('role', 'button'); g.head.tabIndex = 0;
      var has = g.items.some(function(el){ return el.classList.contains('active'); });
      setOpen(g, has);
      function flip(){ setOpen(g, g.head.getAttribute('aria-expanded') !== 'true'); }
      g.head.addEventListener('click', flip);
      g.head.addEventListener('keydown', function(e){ if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); flip(); } });
    });
    // the current brief's system opens itself as the reader scrolls into it
    new MutationObserver(function(ms){
      ms.forEach(function(m){
        var a = m.target; if(a.tagName !== 'A' || !a.classList.contains('active') || !a.classList.contains('axsx-c')) return;
        gs.forEach(function(g){ if(g.items.indexOf(a) >= 0) setOpen(g, true); });
      });
    }).observe(document.getElementById('navlinks'), { subtree: true, attributes: true, attributeFilter: ['class'] });
  }

  /* 5. Mnemonic key column fits its widest key (s135 panic display r1 MED: "FEAR" overran the 28 px column on desktop
     and pushed phone text into a narrow column). Only a list with a key wider than one letter changes. */
  function fitMnem(){
    document.querySelectorAll('dl.rows.mnem').forEach(function(dl){
      if(dl.classList.contains('mn-wide')) return;
      var w = 0, n = 0;
      dl.querySelectorAll('dt b.mn').forEach(function(b){ w = Math.max(w, b.scrollWidth || 0); n = Math.max(n, b.textContent.trim().length); });
      var keyOnly = Array.prototype.every.call(dl.querySelectorAll(':scope > dt'), function(dt){
        var b = dt.querySelector('b.mn'); return b && dt.textContent.trim() === b.textContent.trim(); });
      if(keyOnly) dl.classList.add('mn-key');   // phone: the key column shrinks to the key, the text gets the rest
      if(n < 2) return;
      w = Math.max(w, n * 14);
      dl.style.setProperty('--mnw', (Math.ceil(w) + 16) + 'px');
      dl.classList.add('mn-wide');
    });
  }

  function init(){ setting(); toolbar(); fold(); fitMnem(); window.addEventListener('load', fitMnem); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
