/* Version label and update check. ship.sh stamps <meta name="ax-build"> and writes version.json beside the page;
   when a newer build is live, a bar offers a refresh, so a phone or a home-screen copy never sits on an old version.
   A page served by the offline worker (24-offline) waits for site:ready, the newer build saved by the worker, before
   offering, and Refresh emits site:apply; each check emits net:status (false when the server could not be reached). */
(function(){
"use strict";
var meta=document.querySelector('meta[name="ax-build"]'); if(!meta) return;
var parts=(meta.getAttribute('content')||'').split('|'), BUILD=parts[0]||'', DAY=parts[1]||'';
function fmt(d){ var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(d); if(!m) return d;
  return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][+m[2]-1]+' '+(+m[3])+', '+m[1]; }
function vfmt(n){ n=String(n); while(n.length<3) n='0'+n; return 'v0.'+n; }
var NUM=BUILD.replace(/^s0*/,''), VER=/^\d+$/.test(NUM)?vfmt(NUM):BUILD;
var label=(DAY?fmt(DAY)+' · ':'')+VER;
function openLog(){
  if(document.querySelector('.axlog-scrim')) return;
  var data=[]; try{ data=JSON.parse((document.getElementById('axlog')||{}).textContent||'[]'); }catch(e){}
  var prev=document.activeElement, scrim=document.createElement('div'); scrim.className='axlog-scrim';
  var box=document.createElement('div'); box.className='axlog'; box.setAttribute('role','dialog'); box.setAttribute('aria-modal','true'); box.setAttribute('aria-label','Change log');
  box.innerHTML='<header><h2>Change log</h2><button type="button">Close</button></header><div class="axlog-filter"><button type="button" aria-pressed="false" data-f="all">All versions</button><button type="button" aria-pressed="false" data-f="merges">Merged briefs</button></div><div class="axlog-body"></div>';
  var body=box.querySelector('.axlog-body');
  function el(tag,cls,txt){ var x=document.createElement(tag); if(cls) x.className=cls; if(txt!=null) x.textContent=txt; return x; }
  function render(f){
    body.innerHTML='';
    Array.prototype.forEach.call(box.querySelectorAll('.axlog-filter button'),function(b){ b.setAttribute('aria-pressed',b.getAttribute('data-f')===f?'true':'false'); });
    data.forEach(function(e){
      if(f==='merges' && !(e.merges&&e.merges.length)) return;
      var v=el('div','axlog-v'+(vfmt(e.v)===VER?' cur':'')), h=el('div','axlog-h');
      h.appendChild(el('b',null,vfmt(e.v))); h.appendChild(el('span',null,fmt(e.date))); v.appendChild(h);
      if(e.note) v.appendChild(el('p',null,e.note));
      if(e.merges&&e.merges.length){ var ul=el('ul');
        e.merges.forEach(function(m){ var li=el('li'); li.appendChild(el('span','new',m.new));
          li.appendChild(el('span','old','from: '+m.old.join(' · '))); ul.appendChild(li); });
        v.appendChild(ul); }
      body.appendChild(v);
    });
    if(!body.firstChild) body.appendChild(el('p',null,'No entries.'));
  }
  Array.prototype.forEach.call(box.querySelectorAll('.axlog-filter button'),function(b){ b.addEventListener('click',function(){ render(b.getAttribute('data-f')); }); });
  function close(){ scrim.remove(); document.removeEventListener('keydown',key); if(prev&&prev.focus) prev.focus(); }
  function key(ev){ if(ev.key==='Escape') close(); }
  box.querySelector('header button').addEventListener('click',close);
  scrim.addEventListener('click',function(ev){ if(ev.target===scrim) close(); });
  document.addEventListener('keydown',key);
  scrim.appendChild(box); document.body.appendChild(scrim); render('merges'); box.querySelector('header button').focus();
}
function logButton(){ var b=document.createElement('button'); b.type='button'; b.className='axlogbtn'; b.textContent=label; b.title='Open the change log'; b.addEventListener('click',openLog); return b; }
function show(){
  var mm=document.querySelector('.masthead .meta');
  if(mm){ var sp=Array.prototype.find.call(mm.querySelectorAll('span'),function(x){ return /Last updated/.test(x.textContent); });
    if(!sp){ sp=document.createElement('span'); mm.appendChild(sp); }
    sp.className='axbuild'; sp.textContent='Updated '; sp.appendChild(logButton()); }
  var br=document.querySelector('#nav .brand');
  if(br && !br.querySelector('.axbuild')){ var p=document.createElement('p'); p.className='axbuild'; p.textContent='Updated '; p.appendChild(logButton()); br.appendChild(p); }
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',show); else show();
if(/jsdom/i.test(navigator.userAgent) || !window.fetch || !BUILD || BUILD==='dev') return;
var last=0, bar=null;
function reloadTo(b){
  var u=new URL(location.href); u.searchParams.set('v',b); location.replace(u.toString());
}
function controlled(){ return !!(navigator.serviceWorker && navigator.serviceWorker.controller); }
function offer(apply){
  if(bar) return;
  bar=document.createElement('div'); bar.className='axupdate'; bar.setAttribute('role','status');
  bar.innerHTML='<span>A newer version is available.</span><button type="button">Refresh</button>';
  bar.querySelector('button').addEventListener('click',apply);
  document.body.appendChild(bar);
}
AX.on('site:ready',function(){ offer(function(){ AX.emit('site:apply'); }); });
function check(){
  if(document.visibilityState==='hidden' || Date.now()-last<120000) return;
  last=Date.now();
  fetch('version.json?t='+last,{cache:'no-store'}).then(function(r){ AX.emit('net:status',true); return r.ok?r.json():null; },
      function(){ AX.emit('net:status',false); return null; })
    .then(function(v){
      if(!v || !v.build || v.build===BUILD) return;
      if(controlled()) AX.emit('site:newer',v.build); else offer(function(){ reloadTo(v.build); });
    }).catch(function(){});
}
setTimeout(check,4000);
document.addEventListener('visibilitychange',function(){ if(document.visibilityState==='visible') check(); });
window.addEventListener('pageshow',function(e){ if(e.persisted){ last=0; check(); } });
window.addEventListener('online',function(){ last=0; check(); });
})();
