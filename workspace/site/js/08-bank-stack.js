/* s116: practice questions as an overlapped stack with back and next (Jonathan 2026-10-07). The question cards are not
   moved or rebuilt: the stack only marks one card current, so answers, filters, study mode and progress keep working. */
(function(){
  function cards(bw){ return Array.prototype.slice.call(bw.querySelectorAll('.mcqwrap > .mcq')).filter(function(q){ return !q.hidden; }); }
  function nav(bw){
    var n = bw.querySelector('.bknav'); if(n) return n;
    var w = bw.querySelector('.mcqwrap'); if(!w) return null;
    n = document.createElement('div'); n.className = 'bknav';
    n.innerHTML = '<button type="button" data-sk="-1" aria-label="Previous question">&lsaquo; Back</button><span class="bkn" aria-live="polite"></span><button type="button" data-sk="1" aria-label="Next question">Next &rsaquo;</button>';
    w.insertAdjacentElement('afterend', n); return n;
  }
  function show(bw, i, dir){
    var cs = cards(bw), n = nav(bw); if(!n) return;
    Array.prototype.forEach.call(bw.querySelectorAll('.mcqwrap > .mcq.sk-cur'), function(q){ q.classList.remove('sk-cur','sk-in-f','sk-in-b'); });
    if(!cs.length){ n.querySelector('.bkn').textContent = ''; return; }
    i = Math.max(0, Math.min(cs.length - 1, i)); bw._sk = i;
    var c = cs[i]; c.classList.add('sk-cur'); if(dir) c.classList.add(dir > 0 ? 'sk-in-f' : 'sk-in-b');
    bw.querySelector('.mcqwrap').setAttribute('data-more', String(Math.min(2, cs.length - 1 - i)));
    n.querySelector('.bkn').textContent = (i + 1) + ' of ' + cs.length;
    n.querySelector('[data-sk="-1"]').disabled = i === 0;
    var nx = n.querySelector('[data-sk="1"]'); nx.disabled = i === cs.length - 1;
    nx.classList.toggle('next-ready', c.classList.contains('done') && i < cs.length - 1);
  }
  // one toolbar: the three views as one segmented control, the task filter as a second, side by side
  function toolbar(bw){
    var tools = bw.querySelector('.bktools'); if(!tools || tools.querySelector('.bkseg')) return;
    var seg = document.createElement('span'); seg.className = 'bkseg'; seg.setAttribute('role','group'); seg.setAttribute('aria-label','Question view');
    Array.prototype.forEach.call(tools.querySelectorAll('.bkmode'), function(b){ seg.appendChild(b); });
    tools.insertBefore(seg, tools.firstChild);
    var f = bw.querySelector('.bkfilter');
    if(f){ f.classList.add('bkseg'); tools.insertBefore(f, tools.querySelector('.bkall')); }
  }
  function init(){
    AX.brief.each('bank-stack', function(b){ Array.prototype.forEach.call(b.querySelectorAll('.bankwrap'), function(bw){ toolbar(bw); show(bw, 0); }); });
  }
  document.addEventListener('click', function(e){
    var t = e.target; if(!t || !t.closest) return;
    var nb = t.closest('.bknav button');
    if(nb){ var bw = nb.closest('.bankwrap'), d = parseInt(nb.getAttribute('data-sk'), 10); show(bw, (bw._sk || 0) + d, d); return; }
    var bw2 = t.closest('.bankwrap'); if(!bw2) return;
    if(t.closest('.bkfilter') || t.closest('.bkmode')){ setTimeout(function(){ show(bw2, 0); }, 0); return; }
    if(t.closest('.mcq')) setTimeout(function(){ show(bw2, bw2._sk || 0); }, 0);
  });
  document.addEventListener('keydown', function(e){
    if(e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    var a = document.activeElement; if(!a || !a.closest || /INPUT|TEXTAREA|SELECT/.test(a.tagName)) return;
    var bw = a.closest('.bankwrap.stack'); if(!bw) return;
    var d = e.key === 'ArrowRight' ? 1 : -1; show(bw, (bw._sk || 0) + d, d); e.preventDefault();
  });
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(init, 0); });
  else setTimeout(init, 0);
})();
