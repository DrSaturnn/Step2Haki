/* The address bar should always describe what is on screen, so a copied
   URL reproduces it for someone else. */
function syncShelfUrl(s){
  if(!history.replaceState) return;
  try{
    var u=new URL(location.href);
    u.searchParams.set('shelf', s);
    history.replaceState(null, '', u.pathname + u.search + u.hash);
  }catch(e){}
}
function shelfInit(){
  var m=document.querySelector('.masthead .wrap')||document.querySelector('.masthead');
  if(m) m.appendChild(shelfPicker());
  var nav=document.getElementById('modes');
  if(nav) nav.parentNode.insertBefore(shelfPicker('select'), nav);

  document.addEventListener('click',function(e){
    var b=e.target.closest && e.target.closest('.shelfpick button[data-shelf]');
    if(!b || b.disabled || shelfPending(b.dataset.shelf)) return;
    applyShelf(b.dataset.shelf);
    syncShelfUrl(b.dataset.shelf);
  });
  document.addEventListener('change',function(e){
    var sel=e.target;
    if(!sel.classList || !sel.classList.contains('shelfsel')) return;
    if(shelfPending(sel.value)){ sel.value=shelf; return; }
    applyShelf(sel.value);
    syncShelfUrl(sel.value);
  });

  function valid(s){
    return !!s && !shelfPending(s) && SHELVES.some(function(x){ return x[0]===s; });
  }

  /* Precedence: an explicit ?shelf= in the link, then the reader's own last
     choice, then Step 2. The link wins so a shared URL is predictable for
     whoever opens it, whatever shelf they normally study on. */
  var q=(location.search.match(/[?&]shelf=(\w+)/)||[])[1];
  var saved=null;
  try{ saved=localStorage.getItem('ax-shelf'); }catch(e){}
  var start = valid(q) ? q : (valid(saved) ? saved : 'step2');
  applyShelf(start);
  if(!valid(q)) syncShelfUrl(start);

  /* The browser resolves #hash at parse time, before the shelf filter has
     run, so a link into a filtered brief lands nowhere. Re-run the scroll
     once the layout is settled, and again whenever the hash changes. */
  function gotoHash(smooth){
    var id=pinnedId(); if(!id) return;
    var el=document.getElementById(id);
    if(!el || el.style.display==='none'){
      if(reviewSet && !reviewSet[id]) setSearchMessage(false,true);
      return;
    }
    try{ el.scrollIntoView({behavior: smooth && !(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches) ? 'smooth' : 'auto', block:'start'}); }
    catch(e){ el.scrollIntoView(); }
  }
  if(pinnedId()) setTimeout(function(){ gotoHash(false); }, 60);
  window.addEventListener('hashchange', function(){
    applyShelf(shelf);   /* re-pins for the new hash, un-pins the old one */
    gotoHash(true);
  });
}

