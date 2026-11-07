/* Pilot only: the options group in Settings, the numbered side rail and the differential density variants. */
(function(){
'use strict';
if(!window.matchMedia('(max-width:1100px)').matches || !window.AX) return;
var H = document.documentElement;
function get(k, d){ return H.getAttribute('data-ph-' + k) || d; }
var CH = [
  ['layout', 'Layout', [['solo', 'One brief per screen'], ['long', 'One long page']], get('layout', 'solo')],
  ['bars', 'Bars while reading', [['stay', 'Always shown'], ['hide', 'Hide while scrolling down']], get('bars', 'stay')],
  ['rail', 'Side rail', [['off', 'Off'], ['on', 'Numbered rail, drag to scrub']], get('rail', 'off')],
  ['dx', 'Differential', [['now', 'As now'], ['a', 'A: tighter cards'], ['b', 'B: one card, hairline rows']], get('dx', 'now')]
];
function mount(){
  var s = document.getElementById('axdisp'); if(!s || s.querySelector('.php')) return !!s;
  var box = document.createElement('div'); box.className = 'php';
  box.innerHTML = '<div class="axd-h">Pilot options</div>' + CH.map(function(c){
    return '<div class="php-g"><div class="php-l">' + c[1] + '</div><div class="php-o">' + c[2].map(function(o){
      return '<button type="button" data-k="' + c[0] + '" data-v="' + o[0] + '" aria-pressed="' + (o[0] === c[3]) + '">' + o[1] + '</button>';
    }).join('') + '</div></div>';
  }).join('') + '<p class="php-n">Pilot only. A choice reloads the page.</p>';
  var md = s.querySelector('#modes'); s.insertBefore(box, md ? md.nextSibling : null);
  box.addEventListener('click', function(e){
    var b = e.target.closest('button[data-k]'); if(!b) return;
    e.stopPropagation();
    var o = {}; CH.forEach(function(c){ o[c[0]] = c[3]; }); o[b.dataset.k] = b.dataset.v;
    var ok = false;
    try{ localStorage.setItem('ph-pilot', JSON.stringify(o)); ok = JSON.parse(localStorage.getItem('ph-pilot'))[b.dataset.k] === b.dataset.v; }catch(err){}
    var q = '?' + Object.keys(o).map(function(k){ return 'ph' + k + '=' + o[k]; }).join('&');
    if(ok && !/[?&]ph\w+=/.test(location.search)) location.reload(); else location.href = location.pathname + q + location.hash;
  });
  return true;
}
var n = 0; (function w(){ if(!mount() && ++n < 40) setTimeout(w, 150); })();

/* numbered side rail: shows while scrolling, fades; drag scrubs through the brief; a tap snaps to the nearest stop */
if(get('rail', 'off') !== 'on') return;
var R = document.createElement('div'); R.id = 'phrail'; R.setAttribute('aria-hidden', 'true');
R.innerHTML = '<div class="tk"></div><b class="fl"></b><b class="th"></b><span class="bub"></span>';
document.body.appendChild(R);
var st = null, ticks = [], key = '', fadeT = 0;
function line(){ return Math.max((parseFloat(getComputedStyle(H).getPropertyValue('--ph-top')) || 64) + 8, innerHeight * 0.32); }
AX.on('brief:step', function(s){
  st = s; R.classList.toggle('in', !!s);
  if(!s) return;
  var r = s.el.getBoundingClientRect(), top = r.top + scrollY, hgt = R.clientHeight || 400;
  var k = s.el.id + '|' + Math.round(r.height) + '|' + hgt;
  if(k !== key){
    key = k; var tk = R.querySelector('.tk'); tk.innerHTML = ''; ticks = [];
    var live = s.secs.filter(function(x){ return x.el; });
    var ys = live.map(function(x){ return (x.el.getBoundingClientRect().top + scrollY - top) / r.height * hgt; });
    for(var i = 1; i < ys.length; i++) ys[i] = Math.max(ys[i], ys[i - 1] + 21);
    if(ys.length) ys[ys.length - 1] = Math.min(ys[ys.length - 1], hgt - 10);
    for(var j = ys.length - 2; j >= 0; j--) ys[j] = Math.min(ys[j], ys[j + 1] - 21);
    for(var m = 0; m < ys.length; m++) ys[m] = Math.max(ys[m], 10 + m * 21);
    live.forEach(function(x, i){
      var t = document.createElement('i'); t.style.top = ys[i].toFixed(1) + 'px';
      t.textContent = x.n || ''; if(!x.n) t.className = 'pr';
      tk.appendChild(t); ticks.push({t: t, x: x});
    });
  }
  var cur = s.secs[s.cur];
  ticks.forEach(function(o){ var i = s.secs.indexOf(o.x); o.t.classList.toggle('cur', o.x === cur); o.t.classList.toggle('done', i < s.cur); });
  var f = Math.max(0, Math.min(1, (scrollY + line() - top) / r.height));
  R.querySelector('.fl').style.height = (f * 100).toFixed(2) + '%';
  R.querySelector('.th').style.top = (f * 100).toFixed(2) + '%';
  var bub = R.querySelector('.bub'); bub.style.top = (f * 100).toFixed(2) + '%';
  bub.textContent = cur ? (cur.n ? cur.n + '  ' : '') + cur.l : '';
});
addEventListener('scroll', function(){ R.classList.add('on'); clearTimeout(fadeT); fadeT = setTimeout(function(){ R.classList.remove('on'); }, 1400); }, {passive: true});
var downY = 0, moved = false;
function scrub(e){
  if(!st) return; var rr = R.getBoundingClientRect(), f = Math.max(0, Math.min(1, (e.clientY - rr.top) / rr.height));
  var r = st.el.getBoundingClientRect(); scrollTo({top: r.top + scrollY + f * r.height - line(), behavior: 'instant'});
}
R.addEventListener('pointerdown', function(e){ downY = e.clientY; moved = false; R.classList.add('drag'); R.setPointerCapture(e.pointerId); e.preventDefault(); });
R.addEventListener('pointermove', function(e){ if(!R.classList.contains('drag')) return; if(Math.abs(e.clientY - downY) > 6) moved = true; if(moved) scrub(e); });
R.addEventListener('pointerup', function(e){
  R.classList.remove('drag'); if(moved || !st) return;
  var best = null, bd = 23;
  ticks.forEach(function(o){ var tr = o.t.getBoundingClientRect(), d = Math.abs(e.clientY - (tr.top + tr.height / 2)); if(d < bd){ bd = d; best = o; } });
  if(best) st.go(best.x.el); else scrub(e);
});
R.addEventListener('pointercancel', function(){ R.classList.remove('drag'); });
})();
