/* Briefs drawn in format v2 (class v2, tools/render_v2.py): drawers, hover reasons, brief links, the phone step strip,
   the practice view switch, and Recall's waits and section Resets. The practice questions are the live bank
   (01-transform mcq, 08-bank-stack): the switch above them presses the bank's own view buttons, so answers, progress
   and review stay the bank's. */
(function(){
  function v2(el){ return el && el.closest && el.closest('.brief.v2'); }
  function scroller(el){
    for(var p = el.parentElement; p && p !== document.body; p = p.parentElement){
      var o = getComputedStyle(p).overflowY; if((o === 'auto' || o === 'scroll') && p.scrollHeight > p.clientHeight) return p;
    }
    return null;
  }
  function viewTop(box){ return box ? box.getBoundingClientRect().top : 0; }
  // the step blocks of a brief (its rail and strip buttons carry the same data-k)
  function steps(b){ return Array.prototype.filter.call(b.querySelectorAll('.v2r [data-k]'), function(x){ return !x.closest('nav.v2rail, .v2strip'); }); }
  function headH(){ return parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--ph-top')) || 0; }

  // the phone step strip: one button per rail step, sticky above the brief; marks the step in view
  function strip(b){
    var rail = b.querySelector('nav.v2rail'); if(!rail || b.querySelector('.ph-s')) return;
    var s = document.createElement('div'); s.className = 'ph-s v2strip';
    Array.prototype.forEach.call(rail.querySelectorAll('button[data-k]'), function(r){
      var n = r.querySelector('i'), btn = document.createElement('button'), num = n ? n.textContent : '';
      btn.type = 'button'; btn.dataset.k = r.dataset.k; if(!num) btn.className = 'pr';
      btn.innerHTML = (num ? '<i>' + num + '</i>' : '') + '<span></span>';
      btn.querySelector('span').textContent = r.textContent.slice(num.length);
      s.appendChild(btn);
    });
    var root = b.querySelector('.v2r'); root.insertBefore(s, root.firstChild);
    mark(b, 'script');
  }
  function mark(b, k){ Array.prototype.forEach.call(b.querySelectorAll('.v2strip button'), function(x){ x.classList.toggle('on', x.dataset.k === k); }); }
  var hold = 0;
  function spy(){
    if(Date.now() < hold) return;
    Array.prototype.forEach.call(document.querySelectorAll('.brief.v2 .v2strip'), function(s){
      if(!s.offsetParent) return;
      var b = s.closest('.brief'), line = s.getBoundingClientRect().bottom + 40, cur = 'script';
      steps(b).forEach(function(x){ if(x.getBoundingClientRect().top <= line) cur = x.dataset.k; });
      mark(b, cur);
    });
  }
  function go(b, k){
    var t = steps(b).filter(function(x){ return x.dataset.k === k; })[0]; if(!t) return;
    var s = b.querySelector('.v2strip'), box = scroller(b), off = (s ? s.getBoundingClientRect().height : 0) + 12 + (box ? 0 : headH());
    hold = Date.now() + 700; mark(b, k);
    var y = t.getBoundingClientRect().top - viewTop(box) - off;
    if(box) box.scrollBy({top: y, behavior: 'smooth'}); else window.scrollBy({top: y, behavior: 'smooth'});
  }

  // the practice view switch draws the bank's mode; the bank's own row of view buttons stays out of sight
  function practice(b){
    var host = b.querySelector('[data-k="prac"]'); if(!host) return;
    var bw = host.querySelector('.bankwrap'); if(!bw) return;
    host.classList.add('v2bank');
    sync(host);
  }
  function sync(host){
    var bw = host.querySelector('.bankwrap'), on = bw && bw.querySelector('.bkmode.on'), v = on ? on.dataset.v : 'stack';
    Array.prototype.forEach.call(host.querySelectorAll('.qv button'), function(x){ x.classList.toggle('on', (x.dataset.v === 'list' ? 'quiz' : x.dataset.v) === v); });
  }

  // each drawer's content sits in one inner box: it slides in as the drawer opens and keeps the space below its last line
  function drawers(b){
    Array.prototype.forEach.call(b.querySelectorAll('.dz > .body'), function(d){
      if(d.children.length === 1 && d.firstElementChild.classList.contains('in')) return;
      var w = document.createElement('div'); w.className = 'in';
      while(d.firstChild) w.appendChild(d.firstChild);
      d.appendChild(w);
    });
  }

  // Recall: an item drawn as waiting on a mask (.rwait[data-wait]) stays blurred and inert until that mask is revealed; a tap
  // on it pulses the mask it waits on. A section with a revealed mask shows its Reset, which masks the section again.
  var RESET = '<svg viewBox="0 0 20 20" width="17" height="17" aria-hidden="true"><path d="M4.6 8.2A6 6 0 1 1 4.4 12" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/><path d="M4.3 3.9v4.6h4.6" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function study(){ return document.body.classList.contains('study'); }
  function keyed(b, k){ return b.querySelector('.mask[data-mk="' + k + '"]'); }
  function shown(m){ return !!m && m.dataset.revealed === '1'; }
  function waits(b){
    var s = study();
    Array.prototype.forEach.call(b.querySelectorAll('.rwait[data-wait]'), function(w){
      var on = s && !shown(keyed(b, w.dataset.wait));
      if(w.classList.contains('wt') !== on) w.classList.toggle('wt', on);
      if(w.inert !== on) w.inert = on;
      if(on) w.setAttribute('aria-hidden', 'true'); else w.removeAttribute('aria-hidden');
    });
    Array.prototype.forEach.call(b.querySelectorAll('.blk > .rcr'), function(r){
      var k = r.parentNode, on = s && !!k.querySelector('.mask[data-revealed="1"]');
      if(k.classList.contains('rvd') !== on) k.classList.toggle('rvd', on);
      r.tabIndex = on ? 0 : -1;
    });
  }
  function resets(b){
    Array.prototype.forEach.call(b.querySelectorAll('.blk'), function(k){
      var h = k.querySelector(':scope > h2.st');
      if(!h || !k.querySelector('.mask') || k.querySelector(':scope > .rcr')) return;
      var r = document.createElement('button'); r.type = 'button'; r.className = 'rcr'; r.tabIndex = -1;
      r.setAttribute('aria-label', 'Reset ' + h.textContent.trim()); r.innerHTML = RESET;
      h.tabIndex = -1; h.insertAdjacentElement('afterend', r);
    });
  }
  function recall(b){
    resets(b); waits(b);
    var q = false;
    new MutationObserver(function(){ if(q) return; q = true; requestAnimationFrame(function(){ q = false; waits(b); }); })
      .observe(b, {subtree: true, attributes: true, attributeFilter: ['data-revealed']});
  }
  function pulse(m){
    if(!m) return;
    m.classList.remove('pz'); void m.offsetWidth; m.classList.add('pz');
    clearTimeout(m._pz); m._pz = setTimeout(function(){ m.classList.remove('pz'); }, 700);
  }
  // a waiting item is inert, so a tap on it lands on the element around it: find the wait under the pointer
  function under(t, e){
    var w = t.closest('.rwait.wt'); if(w) return w;
    return Array.prototype.filter.call(t.querySelectorAll('.rwait.wt'), function(x){
      return Array.prototype.some.call(x.getClientRects(), function(r){ return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom; });
    })[0] || null;
  }
  new MutationObserver(function(){ Array.prototype.forEach.call(document.querySelectorAll('.brief.v2'), function(b){ if(b.querySelector('.v2r')) waits(b); }); })
    .observe(document.body, {attributes: true, attributeFilter: ['class']});
  document.addEventListener('click', function(e){
    var t = e.target; if(!t || !t.closest || !study()) return;
    var b = v2(t); if(!b) return;
    var r = t.closest('.rcr');
    if(r){
      var k = r.parentNode;
      Array.prototype.forEach.call(k.querySelectorAll('.mask'), function(m){ m.dataset.revealed = '0'; });
      AX.emit('masks:sync', k); waits(b);
      k.querySelector(':scope > h2.st').focus();
      return;
    }
    var w = under(t, e); if(w) pulse(keyed(b, w.dataset.wait));
  });

  function built(b){ if(!b.classList.contains('v2')) return; drawers(b); strip(b); practice(b); recall(b); }

  document.addEventListener('click', function(e){
    var t = e.target; if(!t || !t.closest) return;
    var b = v2(t); if(!b) return;
    var q = t.closest('.qv button');
    if(q){
      var host = q.closest('[data-k="prac"]'), want = q.dataset.v === 'list' ? 'quiz' : q.dataset.v;
      var m = host.querySelector('.bankwrap .bkmode[data-v="' + want + '"]');
      if(m) m.click();
      setTimeout(function(){ sync(host); }, 0);
      return;
    }
    var st = t.closest('.v2strip button'); if(st){ go(b, st.dataset.k); return; }
    var d = t.closest('.dz>button'); if(d){ d.parentNode.classList.toggle('open'); return; }
    var lk = t.closest('a.lk[data-to]'); if(lk){ e.preventDefault(); AX.emit('brief:go', lk.getAttribute('data-to')); return; }
    var y = t.closest('.it.ti > .y');
    Array.prototype.forEach.call(b.querySelectorAll('.it.open'), function(i){ if(!y || i !== y.parentNode) i.classList.remove('open'); });
    if(y) y.parentNode.classList.toggle('open');
  });
  document.addEventListener('keydown', function(e){
    var t = e.target;
    if((e.key === 'Enter' || e.key === ' ') && t && t.matches && t.matches('.brief.v2 .it.ti > .y')){ e.preventDefault(); t.parentNode.classList.toggle('open'); }
    if(e.key === 'Escape') Array.prototype.forEach.call(document.querySelectorAll('.brief.v2 .it.open'), function(i){ i.classList.remove('open'); });
  });
  document.addEventListener('scroll', spy, true);

  AX.brief.each('v2', built, true);
})();
