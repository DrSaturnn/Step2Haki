/* Index button (s47): on phones and tablets the index opens from a frosted pill at the top left, which hides while
   the page scrolls and while the index is open; the bottom bar keeps Study, Review and Top. */
(function(){
"use strict";
function init(){
  var bar=document.getElementById('mbar'), ib=bar && bar.querySelector('[data-act="index"]');
  if(!ib || document.getElementById('navtab')) return;
  var t=document.createElement('button'); t.type='button'; t.id='navtab';
  t.setAttribute('aria-controls','nav'); t.setAttribute('aria-expanded','false'); t.setAttribute('aria-label','Open index');
  t.innerHTML='<span>Index</span>';
  t.addEventListener('click',function(){ ib.click(); });
  document.body.appendChild(t);
  function sync(){ var o=document.body.classList.contains('navopen');
    t.setAttribute('aria-expanded',o?'true':'false'); t.setAttribute('aria-label',o?'Close index':'Open index');
    t.querySelector('span').textContent=o?'Close':'Index'; }
  new MutationObserver(sync).observe(document.body,{attributes:true,attributeFilter:['class']});
  /* hide while the page scrolls; back once scrolling stops (s47) */
  var to; window.addEventListener('scroll',function(){ t.classList.add('hid'); clearTimeout(to); to=setTimeout(function(){ t.classList.remove('hid'); },350); },{passive:true});
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){ setTimeout(init,0); }); else setTimeout(init,0);
})();
