/* s84: render only the briefs near the screen (content-visibility). Each brief keeps its measured height as a
   placeholder so jumps land where they did before; a jump is re-checked once scrolling stops, in case a brief
   above it changed height on the way. Width changes re-measure. */
(function(){
"use strict";
var root=document.documentElement;
if(!('contentVisibility' in root.style)) return;
function measure(){
  root.classList.remove('cv');
  Array.prototype.forEach.call(document.querySelectorAll('.brief'),function(b){
    var h=b.offsetHeight; if(h>0) b.style.containIntrinsicSize='auto '+h+'px';
  });
  root.classList.add('cv');
}
function target(){
  var id=''; try{ id=decodeURIComponent((location.hash||'').slice(1)); }catch(e){ id=(location.hash||'').slice(1); }
  return id ? document.getElementById(id) : null;
}
var timer=null;
function settle(){
  clearInterval(timer);
  var el=target(); if(!el) return;
  var last=-1, n=0;
  timer=setInterval(function(){
    var y=window.pageYOffset||0;
    if(y===last){
      clearInterval(timer);
      if(el.offsetParent===null) return;
      var top=el.getBoundingClientRect().top;
      if(top<-4 || top>60) el.scrollIntoView({block:'start'});
    }
    last=y; if(++n>40) clearInterval(timer);
  },120);
}
function start(){ requestAnimationFrame(function(){ measure(); }); }
if(document.readyState==='complete') start(); else window.addEventListener('load',start);
window.addEventListener('hashchange',function(){ setTimeout(settle,30); });
var w=window.innerWidth, rt=null;
window.addEventListener('resize',function(){
  if(window.innerWidth===w) return; w=window.innerWidth;
  clearTimeout(rt); rt=setTimeout(measure,400);
});
})();
