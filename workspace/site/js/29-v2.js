/* Briefs drawn in format v2 (class v2, tools/render_v2.py): drawers, hover reasons, brief links, the phone step strip
   and the practice view switch. The practice questions are the live bank (01-transform mcq, 08-bank-stack): the
   switch above them presses the bank's own view buttons, so answers, progress and review stay the bank's. */
(function(){
  function v2(el){ return el && el.closest && el.closest('.brief.v2'); }
  function scroller(el){
    for(var p = el.parentElement; p && p !== document.body; p = p.parentElement){
      var o = getComputedStyle(p).overflowY; if((o === 'auto' || o === 'scroll') && p.scrollHeight > p.clientHeight) return p;
    }
    return null;
  }
  function viewTop(box){ return box ? box.getBoundingClientRect().top : 0; }

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
      Array.prototype.forEach.call(b.querySelectorAll('.v2r [data-k]'), function(x){ if(x.getBoundingClientRect().top <= line) cur = x.dataset.k; });
      mark(b, cur);
    });
  }
  function go(b, k){
    var t = b.querySelector('.v2r [data-k="' + k + '"]'); if(!t) return;
    var s = b.querySelector('.v2strip'), box = scroller(b), off = (s ? s.getBoundingClientRect().height : 0) + 12;
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

  function built(b){ if(!b.classList.contains('v2')) return; strip(b); practice(b); }

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
