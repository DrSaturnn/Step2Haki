/* Decision spine v2 (claude/SPINE_SPEC.md).
   Popovers: mechanisms and "why order it" notes. Desktop (fine pointer): hover or click opens a card. Touch: tap opens the
   same text inline under the whole line.
   Drawers: the reasoning moves into another brief. The drawer shows that whole brief, cloned, minus its practice questions.
   Any link inside a drawer closes it and jumps to the real brief, so a drawer never opens another drawer (Jonathan 2026-10-07). */
(function(){
  var fine = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var card = null, owner = null, hideT = null;
  function bodyOf(btn){
    var n = btn.nextElementSibling;
    if(n && n.classList.contains('sp-pop-b')) return n;
    return document.getElementById(btn.getAttribute('aria-controls'));
  }
  function closeCard(){ if(card){ card.remove(); card = null; } if(owner){ owner.setAttribute('aria-expanded','false'); owner = null; } }
  function openCard(btn){
    var body = bodyOf(btn); if(!body) return;
    if(!fine){
      // inside a sentence, open under the whole line; a standalone button opens in place, inside its own row
      var line = btn.closest('.sp-f, .sp-note, p, td, .sp-chips');
      if(line){
        var tray = line.nextElementSibling;
        if(!tray || !tray.classList.contains('sp-tray')){ tray = document.createElement('div'); tray.className = 'sp-tray'; line.insertAdjacentElement('afterend', tray); }
        if(body.parentNode !== tray) tray.appendChild(body);
      }
      var show = body.hidden; body.hidden = !show; btn.setAttribute('aria-expanded', show ? 'true' : 'false'); return;
    }
    closeCard();
    var z = parseFloat(getComputedStyle(document.documentElement).zoom) || 1;   // s147: html zoom 1.1 at 1500 px and wider; rects and scroll are zoomed px, CSS lengths are not
    card = document.createElement('div'); card.className = 'sp-card'; card.setAttribute('role','tooltip'); card.innerHTML = body.innerHTML;
    document.body.appendChild(card);
    var r = btn.getBoundingClientRect(), w = Math.min(380, window.innerWidth - 24);
    card.style.width = (w / z) + 'px';
    card.style.left = Math.max(12, Math.min(r.left + window.scrollX, window.scrollX + window.innerWidth - w - 12)) / z + 'px';
    var below = r.bottom + 8, h = card.offsetHeight * z;
    var top = (below + h > window.innerHeight - 8 && r.top - h - 8 > 8) ? r.top - h - 8 : below;
    card.style.top = (top + window.scrollY) / z + 'px';
    owner = btn; btn.setAttribute('aria-expanded','true');
    card.addEventListener('mouseenter', function(){ clearTimeout(hideT); });
    card.addEventListener('mouseleave', function(){ hideT = setTimeout(closeCard, 180); });
  }
  var scrim = null, drawer = null, lastBtn = null;
  // desktop: the drawer grows out of the button that opened it and shrinks back into it (spring-like ease)
  var motion = fine && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  function toButton(el, btn){
    var r = btn.getBoundingClientRect(), d = el.getBoundingClientRect();
    if(!r.width || !d.width) return false;
    el.style.transformOrigin = '0 0';
    el.style.transform = 'translate(' + (r.left - d.left) + 'px,' + (r.top - d.top) + 'px) scale(' + (r.width / d.width) + ',' + (r.height / d.height) + ')';
    el.style.borderRadius = '40px';
    return true;
  }
  function closeDrawer(){
    if(!drawer) return;
    var dr = drawer, sc = scrim, btn = lastBtn; drawer = scrim = null; lastBtn = null;
    document.documentElement.style.overflow = '';
    function done(){ dr.remove(); sc.remove(); }
    if(motion && btn && document.body.contains(btn) && dr.classList.contains('sp-g')){
      dr.classList.add('sp-g0'); sc.classList.add('sp-g0');
      if(toButton(dr, btn)){ dr.style.opacity = '0.4'; setTimeout(done, 420); } else done();
    } else done();
    if(btn) btn.focus();
  }
  function jump(id){ closeDrawer(); var t = AX.brief.ensure(id); if(t){ location.hash = id; } }
  function openDrawer(btn){
    var target = AX.brief.ensure(btn.getAttribute('data-brief')); if(!target) return;
    closeCard(); closeDrawer();
    var c = target.cloneNode(true);
    // practice questions stay on the page: cut from the bank (and its "Practice" heading) to the end
    var bank = c.querySelector('.bankwrap, ol.bank');
    if(bank){
      var top = bank; while(top.parentNode && top.parentNode !== c) top = top.parentNode;
      var prev = top.previousElementSibling;
      if(prev && prev.tagName === 'H5' && /practice/i.test(prev.textContent)) prev.remove();
      while(top.nextSibling) top.nextSibling.remove();
      top.remove();
    }
    c.querySelectorAll('.sp-step, .bb-bar, .bb-rail, .bb-end').forEach(function(n){ n.remove(); });
    c.classList.remove('bb-r');
    c.querySelectorAll('[id]').forEach(function(n){ n.removeAttribute('id'); });
    c.removeAttribute('id'); c.hidden = false; c.style.display = 'block';
    scrim = document.createElement('div'); scrim.className = 'sp-scrim';
    drawer = document.createElement('aside'); drawer.className = 'sp-drawer'; drawer.setAttribute('role','dialog'); drawer.setAttribute('aria-modal','true');
    var title = target.querySelector('h4'); drawer.setAttribute('aria-label', title ? title.textContent : 'Linked brief');
    var bar = document.createElement('div'); bar.className = 'sp-dbar';
    var meta = document.createElement('span'); meta.className = 'sp-dmeta'; meta.textContent = 'Linked brief';
    var close = document.createElement('button'); close.type = 'button'; close.className = 'sp-dclose'; close.textContent = 'Close';
    bar.appendChild(meta); bar.appendChild(close); drawer.appendChild(bar); drawer.appendChild(c);
    var pr = document.createElement('div'); pr.className = 'sp-dpractice';
    pr.innerHTML = '<span>Practice questions are on the full brief.</span>';
    var go = document.createElement('a'); go.className = 'sp-dopen'; go.href = '#' + target.id; go.textContent = 'Open the full brief';
    pr.appendChild(go); drawer.appendChild(pr);
    document.body.appendChild(scrim); document.body.appendChild(drawer);
    document.documentElement.style.overflow = 'hidden';
    if(motion && window.innerWidth > 640){
      drawer.classList.add('sp-g0'); scrim.classList.add('sp-g0');
      if(toButton(drawer, btn)){
        drawer.getBoundingClientRect();
        drawer.classList.add('sp-g');
        requestAnimationFrame(function(){ if(!drawer) return; drawer.style.transform = ''; drawer.style.borderRadius = ''; drawer.classList.remove('sp-g0'); scrim.classList.remove('sp-g0'); });
      } else { drawer.classList.remove('sp-g0'); scrim.classList.remove('sp-g0'); }
    }
    lastBtn = btn; close.focus();
    close.addEventListener('click', closeDrawer); scrim.addEventListener('click', closeDrawer);
  }
  document.addEventListener('click', function(e){
    var inDrawer = drawer && drawer.contains(e.target);
    if(inDrawer){
      // links never nest: anything that would open another brief closes the drawer and jumps instead
      var d2 = e.target.closest('.sp-drw');
      if(d2){ e.preventDefault(); e.stopPropagation(); lastBtn = null; jump(d2.getAttribute('data-brief')); return; }
      var a = e.target.closest('a[href^="#"]');
      if(a){ e.preventDefault(); e.stopPropagation(); lastBtn = null; jump(a.getAttribute('href').slice(1)); return; }
    }
    var p = e.target.closest && e.target.closest('.sp-pop');
    if(p){ e.preventDefault(); if(fine && owner === p){ closeCard(); } else { openCard(p); } return; }
    var d = e.target.closest && e.target.closest('.sp-drw');
    if(d){ e.preventDefault(); openDrawer(d); return; }
    if(card && !(e.target.closest && e.target.closest('.sp-card'))) closeCard();
  }, true);
  document.addEventListener('mouseover', function(e){
    if(!fine) return; var p = e.target.closest && e.target.closest('.sp-pop');
    if(p){ clearTimeout(hideT); if(owner !== p) openCard(p); }
  });
  document.addEventListener('mouseout', function(e){
    if(!fine) return; var p = e.target.closest && e.target.closest('.sp-pop');
    if(p && owner === p){ hideT = setTimeout(function(){ if(card && !card.matches(':hover')) closeCard(); }, 180); }
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ closeCard(); closeDrawer(); } });
})();
