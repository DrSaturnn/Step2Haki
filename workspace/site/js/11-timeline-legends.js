/* Timeline charts as cards (s126): give every row of a keyed timeline chart its own legend, listing only the marks that
   row draws, then hide the shared legend when every row has one. Charts without a legend are left as they are. */
(function(){
  'use strict';
  // mark class on a bar -> legend swatch class
  // mark class on a bar -> legend swatch classes, first one the chart's legend has wins
  var MAP = [['bar inf', ['k-inf']], ['bar only', ['k-only']], ['bar hi', ['k-hi']], ['bar lo', ['k-lo']],
             ['bar c1', ['k-ac', 'k-ps']], ['bar c2', ['k-chr', 'k-ps']], ['bar c3', ['k-chr', 'k-ps']], ['bar exp', ['k-ps']],
             ['mb hi mild', ['k-mild']], ['mb lo opt', ['k-opt']], ['mb hi', ['k-hi']], ['mb lo', ['k-lo']],
             ['pb free', ['k-free']], ['pb', ['k-ps']], ['mb n3', ['k-n3']], ['mb lt', ['k-lt']], ['mb rem', ['k-rem']]];
  function has(el, cls){ return cls.split(' ').every(function(c){ return el.classList.contains(c); }); }
  function run(fig){
    if(fig.classList.contains('lcc') || fig.dataset.rk) return;
    fig.dataset.rk = '1';
    var key = fig.querySelector(':scope > .lc-key'); if(!key) return;
    var items = {};
    key.querySelectorAll('span').forEach(function(s){ var i = s.querySelector('i'); if(i) i.classList.forEach(function(c){ if(c.indexOf('k-') === 0) items[c] = s; }); });
    var rows = fig.querySelectorAll(':scope > .wrows > .wr, :scope > .wrows > .tr'), all = rows.length > 0;
    rows.forEach(function(row){
      var want = [];
      row.querySelectorAll('.bar, .mb, .pb').forEach(function(m){
        for(var j = 0; j < MAP.length; j++){
          if(has(m, MAP[j][0])){ var k = MAP[j][1].filter(function(c){ return items[c]; })[0]; if(k && want.indexOf(k) < 0) want.push(k); break; }
        }
      });
      if(!want.length){ all = false; return; }
      var p = document.createElement('p'); p.className = 'rk'; p.setAttribute('aria-hidden', 'true');
      // keep the shared legend's order
      Object.keys(items).forEach(function(k){ if(want.indexOf(k) >= 0) p.appendChild(items[k].cloneNode(true)); });
      var wb = row.querySelector('.wb') || row;
      var after = wb.querySelector(':scope > .rax') || wb.querySelector('.lanes') || wb.querySelector('.rail');
      if(after && after.parentNode === wb) wb.insertBefore(p, after.nextSibling); else wb.appendChild(p);
    });
    if(all) fig.classList.add('rk-on');
  }
  function init(){ document.querySelectorAll('figure.lcw').forEach(run); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
