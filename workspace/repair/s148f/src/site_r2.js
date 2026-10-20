/* s148f site layer (Jonathan 2026-10-19/20): question tiles one size with the mockup's chip row, a Review grouped by
   result, hover cards that animate out as well as in, linked-brief previews with an open icon, and Pairs with as a list.
   Presentation only: no brief text or markup in the page source changes. */
(function(){
  'use strict';
  var fine = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TYPE = { next:'Next step', avoid:'Avoid', dx:'Diagnosis', stage:'Diagnosis', mech:'Mechanism', claim:'Mechanism',
               test:'Workup', screen:'Screening', untyped:'Question' };
  function norm(s){ return (s || '').replace(/\s+/g, ' ').trim(); }
  function key(s){ return norm(s).toLowerCase().replace(/[^a-z0-9 ]/g, ''); }

  /* ---------- 1. question tiles ---------- */
  // banks are measured when they first come near the screen (and again on width change), not all at load
  var io = window.IntersectionObserver ? new IntersectionObserver(function(es){ es.forEach(function(en){
    if(en.isIntersecting){ var t = en.target; t._qxSeen = 1; io.unobserve(t);
      // a lazily rendered brief may still be laying out: measure now and again shortly after, until two runs agree
      (function again(n){ var w = t.querySelector('.mcqwrap'), before = w ? w.style.getPropertyValue('--qx-ho') : '';
        measure(t); var after = w ? w.style.getPropertyValue('--qx-ho') : '';
        if(n > 0 && (!after || after !== before)) setTimeout(function(){ again(n - 1); }, 250); })(8); } }); }, { rootMargin: '600px 0px' }) : null;
  function decorate(bw){
    if(bw._qx) return; bw._qx = 1;
    var qs = Array.prototype.slice.call(bw.querySelectorAll('.mcqwrap > .mcq'));
    qs.forEach(function(q, i){
      if(q.querySelector('.qx-top')) return;
      var qp = q.querySelector('.qp'), t = qp ? qp.dataset.type : 'untyped';
      var top = document.createElement('div'); top.className = 'qx-top';
      var chip = document.createElement('span'); chip.className = 'qx-chip'; chip.textContent = TYPE[t] || 'Question';
      var meta = document.createElement('span'); meta.className = 'qx-meta';
      var no = document.createElement('span'); no.className = 'qx-no'; no.textContent = (i + 1) + ' of ' + qs.length;
      var rv = q.querySelector('.top .rv'); if(rv){ rv.textContent = rv.textContent === 'RESET' ? 'Reset' : 'Reveal'; meta.appendChild(rv); }
      meta.appendChild(no); top.appendChild(chip); top.appendChild(meta);
      q.insertBefore(top, q.firstChild);
      q.dataset.qxN = i + 1;
      // the answer panel sits in a row that can grow smoothly (a hidden element cannot be animated open)
      // the answer line reads "key: reason"; the chain's padding spaces around the key would sit before the colon
      Array.prototype.forEach.call(q.querySelectorAll('.why .chain > .node.dx, .why .chain > .node.act'), function(n){
        var a = n.firstChild, z = n.lastChild;
        if(a && a.nodeType === 3) a.nodeValue = a.nodeValue.replace(/^\s+/, '');
        if(z && z.nodeType === 3) z.nodeValue = z.nodeValue.replace(/\s+$/, '');
      });
      var why = q.querySelector(':scope > .why');
      if(why){ var dz = document.createElement('div'), dzi = document.createElement('div'); dz.className = 'qx-dz'; dzi.className = 'qx-dzi';
        why.parentNode.insertBefore(dz, why); dzi.appendChild(why); dz.appendChild(dzi); }
    });
    var rvw = document.createElement('div'); rvw.className = 'qx-review'; bw.appendChild(rvw);
    // measured when the bank first nears the screen (section wiring) and again when its width changes
    if(window.ResizeObserver){
      var lastW = 0;
      new ResizeObserver(function(){ var w = bw.clientWidth; if(bw._qxSeen && Math.abs(w - lastW) > 1){ lastW = w; measure(bw); } }).observe(bw);
    }
    if(io) io.observe(bw); else { bw._qxSeen = 1; measure(bw); }
    if(bw.classList.contains('review')) renderReview(bw);
  }
  // the tallest card closed (--qx-h) and with its answer open (--qx-ho), measured at the bank's current width
  function measure(bw){
    var wrap = bw.querySelector('.mcqwrap'); if(!wrap || !bw.offsetParent) return false;
    var qs = Array.prototype.slice.call(wrap.querySelectorAll(':scope > .mcq'));
    if(!qs.length) return false;
    wrap.style.removeProperty('--qx-h'); wrap.style.removeProperty('--qx-ho');
    var list = !bw.classList.contains('stack') && !bw.classList.contains('review');
    var colW = list && window.innerWidth > 760 && !bw.closest('.sp-drawer') ? (wrap.clientWidth - 16) / 2 : wrap.clientWidth;
    wrap.classList.add('qx-measure');
    qs.forEach(function(q){ q.style.width = colW + 'px'; });
    var h = 0; qs.forEach(function(q){ h = Math.max(h, q.offsetHeight); });
    wrap.classList.add('qx-open');
    var ho = 0; qs.forEach(function(q){ ho = Math.max(ho, q.offsetHeight); });
    wrap.classList.remove('qx-measure', 'qx-open');
    qs.forEach(function(q){ q.style.width = ''; });
    if(h) wrap.style.setProperty('--qx-h', h + 'px');
    if(ho) wrap.style.setProperty('--qx-ho', ho + 'px');
    if(h > 40) bw._qxM = 1;
    return h > 40;
  }

  /* ---------- 1b. Review grouped by result ---------- */
  function state(q){
    if(!q.classList.contains('done')) return 'open';
    if(q.dataset.qxPick === undefined) return 'seen';
    return q.querySelector('.opts button.wrong') ? 'miss' : 'ok';
  }
  function filterKey(bw){ var b = bw.querySelector('.bkfilter button[aria-pressed="true"]'); return b ? b.dataset.task : 'all'; }
  function txt(el){ return el ? norm(el.textContent) : ''; }
  function renderReview(bw){
    var host = bw.querySelector('.qx-review'); if(!host) return;
    var f = filterKey(bw);
    var qs = Array.prototype.slice.call(bw.querySelectorAll('.mcqwrap > .mcq')).filter(function(q){ return f === 'all' || q.dataset.task === f; });
    var G = { miss:[], ok:[], seen:[], open:[] };
    qs.forEach(function(q){ G[state(q)].push(q); });
    var answered = G.miss.length + G.ok.length;
    host.innerHTML = '';
    var sum = document.createElement('div'); sum.className = 'qx-rsum';
    sum.innerHTML = '<span>Answered <b>' + answered + '</b> of ' + qs.length + '</span>' +
      '<span class="qx-rs-ok"><b>' + G.ok.length + '</b> correct</span><span class="qx-rs-no"><b>' + G.miss.length + '</b> missed</span>' +
      (answered ? '' : '<span class="qx-rhint">Answer questions in Stack or List; missed ones collect at the top here. Each row opens its question.</span>');
    host.appendChild(sum);
    [['miss','Missed'],['ok','Correct'],['seen','Revealed without an answer'],['open','Not yet answered']].forEach(function(g){
      var list = G[g[0]]; if(!list.length) return;
      var box = document.createElement('section'); box.className = 'qx-rg ' + g[0];
      var h = document.createElement('div'); h.className = 'qx-rgh'; h.innerHTML = g[1] + ' <span>' + list.length + '</span>';
      box.appendChild(h);
      list.forEach(function(q){
        var r = document.createElement('button'); r.type = 'button'; r.className = 'qx-rr';
        var right = q.querySelector('.opts button[data-correct="1"]');
        var ansNode = q.querySelector('.why .node.dx'), why = q.querySelector('.why .node.act');
        var ans = right ? txt(right).replace(/^[ABC]\s*/, '') : txt(ansNode);
        var rk = right ? right.querySelector('.k') : null; if(rk) ans = norm(right.textContent.slice(rk.textContent.length));
        var picked = q.querySelector('.opts button.wrong'); var pk = picked ? picked.querySelector('.k') : null;
        var mk = { miss:'✕', ok:'✓', seen:'•', open:'' }[g[0]];
        var html = '<span class="qx-mk" aria-hidden="true">' + mk + '</span><span class="qx-rb"><span class="qx-rt"><span class="qx-chip"></span><span class="qx-no"></span></span>' +
          '<span class="stem qx-rstem"></span><span class="qx-ra"><b></b></span>' + (picked ? '<span class="qx-rc"></span>' : '') + '</span>';
        r.innerHTML = html;
        r.querySelector('.qx-chip').textContent = txt(q.querySelector('.qx-chip'));
        r.querySelector('.qx-no').textContent = 'Question ' + q.dataset.qxN;
        // the whole question, as the live Review shows it: lead line, findings (with the accent bar), vitals and labs
        var st = q.querySelector('.top .stem'), rs = r.querySelector('.qx-rstem');
        if(st) Array.prototype.forEach.call(st.childNodes, function(n){ rs.appendChild(n.cloneNode(true)); });
        r.querySelector('.qx-ra b').textContent = ans;
        if(why){ r.querySelector('.qx-ra').appendChild(document.createTextNode(': ' + txt(why))); }
        if(picked) r.querySelector('.qx-rc').textContent = 'You chose: ' + (pk ? norm(picked.textContent.slice(pk.textContent.length)) : txt(picked));
        r.addEventListener('click', function(){ openInStack(bw, q); });
        box.appendChild(r);
      });
      host.appendChild(box);
    });
  }
  function openInStack(bw, q){
    var st = bw.querySelector('.bkmode[data-v="stack"]'); if(st) st.click();
    var all = bw.querySelector('.bkfilter button[data-task="all"]'); if(all && all.getAttribute('aria-pressed') !== 'true') all.click();
    // step the stack's Back and Next until this card is current (the stack script owns the index)
    var guard = 60, next = bw.querySelector('.bknav [data-sk="1"]'), back = bw.querySelector('.bknav [data-sk="-1"]');
    if(!next || !back) return;
    var qs = Array.prototype.slice.call(bw.querySelectorAll('.mcqwrap > .mcq'));
    var want = qs.indexOf(q);
    while(guard-- > 0){
      var cur = qs.indexOf(bw.querySelector('.mcqwrap > .mcq.sk-cur'));
      if(cur === want || cur < 0) break;
      (cur < want ? next : back).click();
    }
    var top = bw.getBoundingClientRect().top + window.scrollY - 90;
    window.scrollTo({ top: top, behavior: still ? 'auto' : 'smooth' });
  }

  /* ---------- 2. hover cards animate out ---------- */
  var nativeRemove = Element.prototype.remove;
  Element.prototype.remove = function(){
    if(!still && this.classList && this.classList.contains('sp-card') && !this.classList.contains('qx-out') && this.parentNode === document.body && fine){
      var ghost = this.cloneNode(true); ghost.classList.add('qx-out'); ghost.removeAttribute('role'); ghost.setAttribute('aria-hidden', 'true');
      ghost.style.cssText = this.style.cssText; document.body.appendChild(ghost);
      setTimeout(function(){ nativeRemove.call(ghost); }, 380);
    }
    return nativeRemove.call(this);
  };
  // a card placed above its button grows from its lower edge
  new MutationObserver(function(ms){
    ms.forEach(function(m){ Array.prototype.forEach.call(m.addedNodes, function(n){
      if(n.nodeType === 1 && n.classList.contains('sp-card') && !n.classList.contains('qx-out')){
        var o = document.querySelector('.sp-pop[aria-expanded="true"]');
        requestAnimationFrame(function(){ if(o && n.getBoundingClientRect().top < o.getBoundingClientRect().top) n.classList.add('qx-up'); });
      }
    }); });
  }).observe(document.body, { childList: true });

  /* ---------- 3. linked-brief preview ---------- */
  var pv = null, pvFor = null, pvT = 0;
  function closePv(now){
    if(!pv) return; var el = pv; pv = null; if(pvFor) pvFor.removeAttribute('aria-describedby'); pvFor = null;
    if(still || now){ el.remove(); return; }
    el.classList.add('qx-out'); setTimeout(function(){ nativeRemove.call(el); }, 380);
  }
  function openPv(link){
    var id = link.getAttribute('data-brief'), t = document.getElementById(id); if(!t) return;
    if(pvFor === link) return; closePv(true);
    var h = t.querySelector('h4'), q = t.querySelector('.sub .subq');
    pv = document.createElement('div'); pv.className = 'qx-pv'; pv.id = 'qx-pv'; pv.setAttribute('role', 'dialog'); pv.setAttribute('aria-label', 'Linked brief preview');
    pv.innerHTML = '<span class="qx-pk">Linked brief</span><span class="qx-pt"></span>' + (q ? '<span class="qx-pq"></span>' : '') +
      '<button type="button" class="qx-po">Open brief</button>';
    pv.querySelector('.qx-pt').textContent = h ? norm(h.textContent) : norm(link.textContent);
    if(q) pv.querySelector('.qx-pq').textContent = norm(q.textContent);
    pv.querySelector('.qx-po').addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); var l = link; closePv(true); l._qxPass = 1; l.click(); });
    pv.addEventListener('mouseenter', function(){ clearTimeout(pvT); });
    pv.addEventListener('mouseleave', function(){ pvT = setTimeout(function(){ closePv(); }, 200); });
    document.body.appendChild(pv);
    var r = link.getClientRects(); r = r.length ? r[r.length - 1] : link.getBoundingClientRect();
    var z = parseFloat(getComputedStyle(document.documentElement).zoom) || 1, w = pv.offsetWidth * z, hh = pv.offsetHeight * z;
    var left = Math.max(12, Math.min(r.left, window.innerWidth - w - 12));
    var top = r.bottom + 8; if(top + hh > window.innerHeight - 8 && r.top - hh - 8 > 8){ top = r.top - hh - 8; pv.classList.add('qx-up'); }
    pv.style.left = (left + window.scrollX) / z + 'px'; pv.style.top = (top + window.scrollY) / z + 'px';
    pvFor = link; link.setAttribute('aria-describedby', 'qx-pv');
  }
  window.addEventListener('click', function(e){
    var l = e.target.closest && e.target.closest('.sp-drw');
    if(!l){ if(pv && !(e.target.closest && e.target.closest('.qx-pv'))) closePv(); return; }
    if(l._qxPass){ l._qxPass = 0; return; }                   // the preview's Open button: let the drawer open
    if(l.classList.contains('qx-pair') || l.closest('.sp-drawer')){ closePv(true); return; }
    if(fine){ closePv(true); return; }                          // desktop: a click opens the drawer at once
    if(pvFor !== l){ e.preventDefault(); e.stopPropagation(); openPv(l); }   // touch: the first tap previews
    else closePv(true);
  }, true);
  document.addEventListener('mouseover', function(e){
    if(!fine) return; var l = e.target.closest && e.target.closest('.brief .sp-drw:not(.qx-pair)');
    if(l && !l.closest('.sp-drawer')){ clearTimeout(pvT); pvT = setTimeout(function(){ openPv(l); }, 120); }
  });
  document.addEventListener('mouseout', function(e){
    if(!fine) return; var l = e.target.closest && e.target.closest('.brief .sp-drw:not(.qx-pair)');
    if(l){ clearTimeout(pvT); pvT = setTimeout(function(){ if(pv && !pv.matches(':hover')) closePv(); }, 200); }
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && pv){ var f = pvFor; closePv(true); if(f) f.focus(); } });
  window.addEventListener('scroll', function(){ if(pv && !fine) return; if(pv) closePv(); }, { passive: true });

  /* ---------- 3b. Pairs with as a list ---------- */
  var TITLES = null;
  function titles(){
    if(TITLES) return TITLES; TITLES = {};
    Array.prototype.forEach.call(document.querySelectorAll('main .brief[id]'), function(b){ var h = b.querySelector('h4'); if(h) TITLES[key(h.textContent)] = b.id; });
    return TITLES;
  }
  function pairs(pb){
    if(pb._qx) return; pb._qx = 1;
    var lbl = pb.querySelector(':scope > .lbl'); if(!lbl || !/^pairs with$/i.test(norm(lbl.textContent))) return;
    var items = [], cur = null;
    Array.prototype.forEach.call(pb.childNodes, function(n){
      if(n === lbl) return;
      if(n.nodeType === 1 && /^(I|B|EM|A)$/.test(n.tagName)){ cur = { name: norm(n.textContent), why: '', a: n.tagName === 'A' ? n.getAttribute('href') : '' }; items.push(cur); return; }
      if(cur) cur.why += n.textContent; else if(norm(n.textContent)) items.bad = 1;
    });
    if(!items.length || items.bad) return;
    var T = titles(), list = document.createElement('div'); list.className = 'qx-pl';
    items.forEach(function(it){
      var why = norm(it.why).replace(/^[:–—-]\s*/, '').replace(/[.;]\s*$/, '');
      var id = it.a && it.a.charAt(0) === '#' ? it.a.slice(1) : T[key(it.name)];
      var row = document.createElement(id ? 'button' : 'div');
      row.className = id ? 'sp-drw qx-pair' : 'qx-pair qx-nolink';
      if(id){ row.type = 'button'; row.setAttribute('data-brief', id); }
      row.innerHTML = '<span><span class="qx-pn"></span>' + (why ? '<span class="qx-pd"></span>' : '') + '</span>';
      row.querySelector('.qx-pn').textContent = it.name;
      if(why) row.querySelector('.qx-pd').textContent = why;
      list.appendChild(row);
    });
    var src = document.createElement('span'); src.className = 'qx-src';           // the original sentence stays for search and print
    while(lbl.nextSibling) src.appendChild(lbl.nextSibling);
    pb.appendChild(list); pb.appendChild(src); pb.classList.add('qx-pairs');
  }

  /* ---------- 4. hover and link buttons inside text wrap with the sentence ----------
     A <button> is laid out as one unbreakable box even when styled inline, so a long hover label inside a cell or a
     sentence jumped to its own line and stood as a block (tics, phone). Inside text it becomes a span with the button
     role, the same classes, attributes and keyboard behavior; the hover and drawer scripts find it by class. */
  function inlineButtons(root){
    Array.prototype.forEach.call(root.querySelectorAll('.brief :is(td, p, li, dd, .sp-f, .sp-note) :is(button.sp-pop, button.sp-drw):not(.qx-pair)'), function(b){
      var s = document.createElement('span');
      Array.prototype.forEach.call(b.attributes, function(a){ if(a.name !== 'type') s.setAttribute(a.name, a.value); });
      s.setAttribute('role', 'button'); s.tabIndex = 0; s.classList.add('qx-ib');
      while(b.firstChild) s.appendChild(b.firstChild);
      b.parentNode.replaceChild(s, b);
    });
  }
  document.addEventListener('keydown', function(e){
    if((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('qx-ib')){ e.preventDefault(); e.target.click(); }
  });

  /* ---------- wiring ---------- */
  function scan(root){
    inlineButtons(root || document);
    Array.prototype.forEach.call((root || document).querySelectorAll('.bankwrap'), decorate);
    Array.prototype.forEach.call((root || document).querySelectorAll('.brief .pearls'), pairs);
  }
  // a bank reached by a jump (the section rail, a link) may be touched before its first measurement has run
  document.addEventListener('pointerdown', function(e){
    var bw = e.target.closest && e.target.closest('.bankwrap'); if(bw && !bw._qxM){ bw._qxSeen = 1; measure(bw); }
  }, true);
  document.addEventListener('click', function(e){
    var o = e.target.closest && e.target.closest('.mcq .opts button');
    if(o){ var q = o.closest('.mcq'); if(!q.classList.contains('done') && !o.disabled) q.dataset.qxPick = o.dataset.optionId || '1'; }
    var rv = e.target.closest && e.target.closest('.mcq .rv');
    if(rv){ var q2 = rv.closest('.mcq'); if(q2.classList.contains('done')) delete q2.dataset.qxPick; }
    // the bank script writes REVEAL or RESET after any answer or reveal: keep the chip row's sentence case
    var q3 = e.target.closest && e.target.closest('.mcq');
    if(q3) setTimeout(function(){ var r3 = q3.querySelector('.qx-top .rv'); if(r3) r3.textContent = q3.classList.contains('done') ? 'Reset' : 'Reveal'; }, 0);
    var ba = e.target.closest && e.target.closest('.bkall');
    if(ba){ var b0 = ba.closest('.bankwrap'); setTimeout(function(){ Array.prototype.forEach.call(b0.querySelectorAll('.mcq'), function(x){
      if(!x.classList.contains('done')) delete x.dataset.qxPick; var r2 = x.querySelector('.qx-top .rv'); if(r2) r2.textContent = x.classList.contains('done') ? 'Reset' : 'Reveal'; }); }, 0); }
  }, true);
  document.addEventListener('click', function(e){
    var bm = e.target.closest && e.target.closest('.bkmode, .bkfilter button');
    var bw = e.target.closest && e.target.closest('.bankwrap'); if(!bw) return;
    setTimeout(function(){ if(bm) measure(bw); if(bw.classList.contains('review')) renderReview(bw); }, 0);
  });
  function boot(){ scan(document); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  // banks and briefs that render later (lazy sections, the drawer) are decorated when they appear
  new MutationObserver(function(ms){
    for(var i = 0; i < ms.length; i++){ var a = ms[i].addedNodes;
      for(var j = 0; j < a.length; j++){ var n = a[j]; if(n.nodeType === 1 && (n.matches('.bankwrap, .sp-drawer, .brief') || n.querySelector && n.querySelector('.bankwrap, .pearls'))) { scan(n.parentNode || document); } } }
  }).observe(document.body, { childList: true, subtree: true });
})();
