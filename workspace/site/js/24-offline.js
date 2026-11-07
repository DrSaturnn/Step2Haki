/* Offline use. Registers sw.js (the worker the build writes beside the page), shows a note while the device has no
   connection, and hands a newer build from the worker to the update bar.
   Events: listens to site:newer (version.json names a newer build: ask the worker to fetch it), site:apply (the reader
   chose Refresh: the waiting worker takes over, then the page reloads) and net:status (false when a request to the
   server failed); emits site:ready (a newer build is saved and waiting). */
return (function(){
"use strict";
var meta=document.querySelector('meta[name="ax-build"]');
var parts=((meta&&meta.getAttribute('content'))||'').split('|'), BUILD=parts[0]||'', DAY=parts[1]||'';
var SW=navigator.serviceWorker;
var local=/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
var usable=!!SW && (location.protocol==='https:' || (location.protocol==='http:' && local)) &&
  !/jsdom/i.test(navigator.userAgent) && BUILD && BUILD!=='dev' && !/[?&]axall\b/.test(location.search);
var reg=null, note=null, failed=false, reloading=false, offs=[];

function day(d){ var m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(d); if(!m) return d;
  return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][+m[2]-1]+' '+(+m[3])+', '+m[1]; }
function text(){
  if(SW && SW.controller) return 'Offline: saved copy from '+day(DAY);
  return 'Offline: no saved copy on this device';
}
function render(){
  var off=navigator.onLine===false || failed;
  if(!off){ if(note){ note.classList.remove('on'); note.setAttribute('aria-hidden','true'); } return; }
  if(!note){ note=document.createElement('div'); note.className='axoffline'; note.setAttribute('role','status'); document.body.appendChild(note); }
  note.textContent=text(); note.removeAttribute('aria-hidden');
  requestAnimationFrame(function(){ note.classList.add('on'); });
}
function online(){ failed=false; render(); }
function offline(){ render(); }
window.addEventListener('online',online); window.addEventListener('offline',offline);
offs.push(AX.on('net:status',function(ok){ failed=!ok; render(); }));
render();

function waiting(r){
  if(r.waiting && SW.controller) AX.emit('site:ready',{});
}
function watch(r){
  waiting(r);
  r.addEventListener('updatefound',function(){
    var w=r.installing; if(!w) return;
    w.addEventListener('statechange',function(){ if(w.state==='installed') waiting(r); });
  });
}
function start(){
  SW.register('sw.js',{updateViaCache:'none'}).then(function(r){ reg=r; watch(r); render(); }).catch(function(){});
  SW.addEventListener('controllerchange',function(){
    if(reloading){ location.reload(); return; }
    render();
  });
}
if(usable){
  offs.push(AX.on('site:newer',function(){ if(reg) reg.update().catch(function(){}); }));
  offs.push(AX.on('site:apply',function(){
    if(reg && reg.waiting){ reloading=true; reg.waiting.postMessage({type:'activate'}); }
    else location.reload();
  }));
  var go=function(){ if(window.requestIdleCallback) requestIdleCallback(start,{timeout:5000}); else setTimeout(start,1500); };
  if(document.readyState==='complete') go(); else window.addEventListener('load',go,{once:true});
}

return {teardown:function(){
  window.removeEventListener('online',online); window.removeEventListener('offline',offline);
  offs.forEach(function(f){ f(); }); offs=[];
  if(note){ note.remove(); note=null; }
}};
})();
