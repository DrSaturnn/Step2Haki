/* =====================================================================
   AxBx transform — presentation only.
   Restructures the existing DOM at load. Never invents or removes text:
   every operation moves nodes or wraps them. A content-invariance check
   at the end compares the visible text before and after.
   ===================================================================== */
(function(){
"use strict";

/* The word-count self-check forces a full layout of the page twice (about 1.7 s on a laptop, longer on a phone),
   so it runs only under the ship check (jsdom) or with ?axcheck in the URL. */
var VERIFY = /jsdom/i.test(navigator.userAgent) || /[?&]axcheck\b/.test(location.search);
var BEFORE = (VERIFY && document.body) ? norm(document.body.innerText) : "";
function norm(s){ return (s||"").replace(/\s+/g," ").trim(); }

/* ---------- 0. sidebar mode switches ---------- */
function switches(){
  var nav=document.getElementById('nav'); if(!nav) return;
  var brand=nav.querySelector('.brand');
  var box=document.createElement('div'); box.id='modes';
  box.innerHTML =
    '<button class="bsonly" type="button" aria-pressed="false" title="Show only board-style briefs"><span class="track"><span class="knob"></span></span><span class="nm">BOARD-STYLE ONLY</span></button>'+
    '<button class="study" type="button" aria-pressed="false"><span class="track"><span class="knob"></span></span><span class="nm">RECALL MODE</span></button>'+
    '<button class="flatt" type="button" aria-pressed="false"><span class="track"><span class="knob"></span></span><span class="nm">FLAT THEME</span></button>';
  brand ? brand.after(box) : nav.prepend(box);
  var b=document.body;
  function sync(){
    box.querySelector('.bsonly').setAttribute('aria-pressed',boardOnly?'true':'false');
    box.querySelector('.study').setAttribute('aria-pressed',b.classList.contains('study')?'true':'false');
    box.querySelector('.flatt').setAttribute('aria-pressed',b.classList.contains('flat')?'true':'false');
  }
  if(localStorage.getItem('ax-study')==='1') b.classList.add('study');
  if(localStorage.getItem('ax-flat')!=='0') b.classList.add('flat');   // s161b r3: flat is the default
  /* Board-style only joins the shelf rule in shelfEligible(); it lasts for this visit only (not saved). */
  box.querySelector('.bsonly').addEventListener('click',function(){
    boardOnly=!boardOnly;
    sync(); keepPlace(function(){ applyShelf(shelf); });
  });
  box.querySelector('.study').addEventListener('click',function(){
    b.classList.toggle('study'); localStorage.setItem('ax-study',b.classList.contains('study')?'1':'0'); sync();
  });
  box.querySelector('.flatt').addEventListener('click',function(){
    b.classList.toggle('flat'); localStorage.setItem('ax-flat',b.classList.contains('flat')?'1':'0'); sync();
  });
  sync();
  if(!window.__axModeObserver){
    window.__axModeObserver=new MutationObserver(function(){
      sync();
      var mb=document.querySelector('#mbar [data-act="study"]');
      if(mb) mb.setAttribute('aria-pressed',b.classList.contains('study')?'true':'false');
      axmSync(false);
    });
    window.__axModeObserver.observe(b,{attributes:true,attributeFilter:['class']});
  }
  axmWatch();
}

/* ---------- 0b. mode carriers (s92) ----------------------------------
   Flat and study styling hangs on per-region classes (axm-flat, axm-study),
   not on body. A switch restyles the regions on or near the screen at once
   and the rest four per frame, nearest first. A body-wide class change made
   the browser restyle every brief at once (about 45,000 elements for flat),
   which froze Safari and slower machines in both directions.            */
var axmQ=[], axmRaf=0, axmLast='';
function axmCarriers(){
  var out=[];
  (function walk(el){
    for(var c=el.firstElementChild;c;c=c.nextElementSibling){
      if(c.tagName==='SCRIPT'||c.tagName==='STYLE') continue;
      if(c.classList.contains('brief')||!c.querySelector('.brief')) out.push(c); else walk(c);
    }
  })(document.body);
  return out;
}
function axmApply(c){
  var b=document.body, study=false;
  ['flat','study'].forEach(function(m){
    var on=b.classList.contains(m);
    if(c.classList.contains('axm-'+m)!==on){ c.classList.toggle('axm-'+m,on); if(m==='study') study=true; }
  });
  if(study) syncMaskRegions(c);
}
function axmDist(c){
  var r=c.getBoundingClientRect(), h=window.innerHeight||800;
  if(!r.width&&!r.height) return 1e9;
  return r.bottom<0?-r.bottom:(r.top>h?r.top-h:0);
}
/* next frame, or after 60 ms where frames are paused or throttled, whichever comes first */
function axmKick(){
  var done=false; axmRaf=1;
  function go(){ if(done) return; done=true; axmStep(); }
  requestAnimationFrame(go); setTimeout(go,60);
}
function axmStep(){
  axmRaf=0; if(!axmQ.length) return;
  axmQ.splice(0,4).forEach(axmApply);
  if(axmQ.length) axmKick();
}
function axmSync(now){
  var b=document.body, key=(b.classList.contains('flat')?'f':'')+(b.classList.contains('study')?'s':'');
  if(!now&&key===axmLast) return; axmLast=key;
  /* distances are read once, before any class changes, so the queue never forces a layout */
  var all=axmCarriers(), h=window.innerHeight||800, near=[], rest=[];
  all.forEach(function(c){ var d=now?0:axmDist(c); if(d<h) near.push(c); else rest.push([d,c]); });
  near.forEach(axmApply);
  rest.sort(function(x,y){ return x[0]-y[0]; });
  axmQ=rest.map(function(x){ return x[1]; }); if(axmQ.length&&!axmRaf) axmKick();
}
function axmWatch(){
  axmSync(true);
  if(window.__axmChildObserver) return;
  window.__axmChildObserver=new MutationObserver(function(list){
    list.forEach(function(r){ Array.prototype.forEach.call(r.addedNodes,function(n){ if(n.nodeType===1&&n.tagName!=='SCRIPT'&&n.tagName!=='STYLE'&&(n.classList.contains('brief')||!n.querySelector('.brief'))) axmApply(n); }); });
  });
  window.__axmChildObserver.observe(document.body,{childList:true});
}

/* ---------- 0a. shelf selector --------------------------------------
   One document, four views. Briefs carry data-shelf; selecting a shelf
   hides the rest and rebuilds the index, masthead counts and section
   headers to match, so a shelf never advertises content it isn't showing.
   Step 2 is the pooled default. ?shelf=peds deep-links a shelf.       */
/* [id, label, pending] — pending shelves render greyed and unclickable.
   Remove the trailing 1 when a shelf is written; nothing else changes. */
var SHELVES=[['step2','Step 2'],['fm','Family Med'],['peds','Pediatrics'],['psych','Psych'],
             ['im','Medicine',1],['surg','Surgery',1],['obgyn','OB/GYN',1],
             ['neurology','Neurology',1]];
function shelfPending(s){
  for(var i=0;i<SHELVES.length;i++) if(SHELVES[i][0]===s) return !!SHELVES[i][2];
  return false;
}
var shelf='step2';
var reviewSet=null;   /* fixed brief IDs while an active review is running */
/* Search no longer filters the page: it lists results in the sidebar (see 0c).
   searchTerm stays empty so applyShelf's composition is unchanged. */
var searchTerm='';
var boardOnly=false;
/* BOARD-STYLE ONLY starts off on every visit (Jonathan 2026-10-01: a remembered switch hid whole shelves on one device). */
try{ localStorage.removeItem('ax-bsonly'); }catch(e){}

/* Board-style = the set the title badge calls Board (or UWorld): .brief.bs
   without an Aquifer source, the same split the masthead counts use. */
function isBoardStyle(b){
  return b.classList.contains('bs') && b.getAttribute('data-src')!=='aquifer';
}
function shelfEligible(b,s){
  if(!b || !b.id) return false;
  if(reviewSet) return !!reviewSet[b.id];
  if(boardOnly && !isBoardStyle(b)) return false;
  if(s==='step2') return true;
  return (b.getAttribute('data-shelf')||'').split(/\s+/).indexOf(s)>-1;
}
function desktopMatch(b){
  return !searchTerm || (b.textContent||'').toLowerCase().indexOf(searchTerm)>-1;
}
function setSearchMessage(visible,reviewBlocked){
  var n=document.getElementById('noresults'); if(!n) return;
  if(reviewBlocked){ n.textContent='This brief is outside the active review.'; n.style.display='block'; return; }
  n.textContent='No briefs match that search.';
  n.style.display=(searchTerm&&!visible)?'block':'none';
}

function shelfPicker(kind){
  var w=document.createElement('div'); w.className='shelfpick';
  var lbl=document.createElement('span'); lbl.className='lbl'; lbl.textContent='Shelf';
  w.appendChild(lbl);

  /* The sidebar is 286px wide and the list only grows, so it gets a real
     <select>: it scales to any number of shelves and renders the pending ones
     as disabled options without any styling of our own. */
  if(kind==='select'){
    w.className='shelfpick assel';
    var sel=document.createElement('select');
    sel.className='shelfsel'; sel.setAttribute('aria-label','Shelf');
    SHELVES.forEach(function(s){
      var o=document.createElement('option');
      o.value=s[0]; o.textContent=s[1]+(s[2]?'  \u2013  soon':'');
      if(s[2]) o.disabled=true;
      sel.appendChild(o);
    });
    w.appendChild(sel);
    return w;
  }

  var g=document.createElement('div'); g.className='seg';
  SHELVES.forEach(function(s){
    var b=document.createElement('button'); b.dataset.shelf=s[0];
    b.textContent=s[1];
    if(s[2]){
      b.disabled=true; b.className='soon';
      b.title=s[1]+' – not written yet';
      var i=document.createElement('i'); i.textContent='soon'; b.appendChild(i);
    }
    g.appendChild(b);
  });
  w.appendChild(g);
  return w;
}

/* A deep link may target a brief the active shelf filters out. Rather than
   widening the shelf (which would silently change what the reader asked for)
   or dropping them on a blank page, that one brief is pinned visible for as
   long as the hash points at it. Everything downstream — section headers,
   band counts, sidebar links, masthead totals — reads style.display, so the
   pin has to be applied here or the page would contradict itself. */
function pinnedId(){
  var id=(location.hash||'').replace(/^#/,'');
  if(!id) return null;
  var el=document.getElementById(id);
  return (el && el.classList.contains('brief')) ? id : null;
}
/* s92: a filter switch (shelf, Board-style only) keeps the reader's place: the brief at the top of the
   screen stays where it was, or, if it is filtered out, the next shown brief takes its spot. */
var placeMemo=null;
function jump(dy){ if(dy) window.scrollBy({top:dy,left:0,behavior:'instant'}); }
function keepPlace(fn){
  var all=Array.prototype.slice.call(document.querySelectorAll('.brief')), anchor=null, top=0;
  for(var i=0;i<all.length;i++){ if(all[i].style.display==='none') continue; var r=all[i].getBoundingClientRect(); if(r.bottom>0){ anchor=i; top=r.top; break; } }
  /* switching back without scrolling in between returns to the brief you started from */
  var memo=(placeMemo&&anchor!==null&&all[anchor].id===placeMemo.landed)?placeMemo:null;
  fn();
  placeMemo=null;
  if(anchor===null||window.pageYOffset<1) return;
  var back=memo&&document.getElementById(memo.id);
  if(back&&back.style.display!=='none'){ jump(back.getBoundingClientRect().top-memo.top); return; }
  for(var j=anchor;j<all.length;j++){
    if(all[j].style.display!=='none'){
      jump(all[j].getBoundingClientRect().top-(j===anchor?top:Math.max(top,0)));
      placeMemo={id:(memo?memo.id:all[anchor].id),top:(memo?memo.top:top),landed:all[j].id};
      return;
    }
  }
}
function applyShelf(s){
  shelf=s;
  try{ localStorage.setItem('ax-shelf',s); }catch(e){}
  var pin=pinnedId(), visible=0;
  document.querySelectorAll('.brief').forEach(function(b){
    var eligible=shelfEligible(b,s), on=eligible;
    /* Browsing may pin one explicit off-shelf hash. Review membership is fixed. */
    if(!reviewSet&&b.id===pin) on=true;
    if(on&&searchTerm&&!(!reviewSet&&b.id===pin)) on=desktopMatch(b);
    if(b.style.display!==(on?'':'none')) b.style.display=on?'':'none';
    b.classList.toggle('pinned',!!(!reviewSet&&b.id===pin&&!eligible));
    if(on) visible++;
  });
  var liveSystems=0;
  document.querySelectorAll('.sectwrap').forEach(function(sw){
    var n=0,total=0,el=sw.nextElementSibling;
    while(el&&!el.classList.contains('sectwrap')){
      if(el.classList.contains('brief')){total++;if(el.style.display!=='none')n++;}
      el=el.nextElementSibling;
    }
    /* a system section with no briefs yet stays hidden; front matter (h3 without a count) stays shown */
    var swd=(n||(total===0&&!sw.querySelector('h3.system .n')))?'':'none'; if(sw.style.display!==swd) sw.style.display=swd; if(sw.dataset.count!==String(n)) sw.dataset.count=n;
    if(total>0&&n) liveSystems++;
  });
  document.querySelectorAll('.bsband').forEach(function(bb){
    var n=0,el=bb.nextElementSibling,aq=bb.classList.contains('aqband');
    while(el&&el.classList.contains('brief')){
      if((aq?el.dataset.src==='aquifer':el.classList.contains('bs'))&&el.style.display!=='none')n++;
      el=el.nextElementSibling;
    }
    bb.style.display=n?'':'none';
    var c=bb.querySelector('.n'); if(c)c.textContent=n+(n===1?' brief':' briefs');
  });
  document.querySelectorAll('#navlinks a[href^="#"]').forEach(function(a){
    var t=document.getElementById(a.getAttribute('href').slice(1));
    var eligible=!!(t&&(!t.classList.contains('brief')||t.style.display!=='none'));
    if(a.dataset.eligible!==(eligible?'1':'0')) a.dataset.eligible=eligible?'1':'0';
    if(a.style.display!==(eligible?'':'none')) a.style.display=eligible?'':'none';
  });
  /* Each system group shows how many of its links are live under the current
     shelf, Board-style only and review filters, so the index never advertises
     briefs it is hiding. */
  var navHost=document.getElementById('navlinks');
  if(navHost){
    var group=null,live=0,sub=null,subLive=0;
    function closeSub(){ if(sub)sub.style.display=subLive?'':'none'; sub=null; subLive=0; }
    function closeGroup(){
      if(!group) return;
      group.style.display=live?'':'none';
      var gc=group.querySelector('.count'); if(gc) gc.textContent=live;
    }
    Array.prototype.slice.call(navHost.children).forEach(function(el){
      if(el.classList.contains('sect')){
        closeSub(); closeGroup();
        group=el;live=0;
      }else if(el.tagName==='A'&&el.style.display!=='none'){live++;subLive++;}
      else if(el.classList.contains('navsub')){ closeSub(); sub=el; }
    });
    closeSub(); closeGroup();
  }
  var meta=document.querySelector('.masthead .meta');
  if(meta){
    var bs=0,aq=0;
    document.querySelectorAll('.brief').forEach(function(b){
      if(b.style.display==='none')return;
      if(b.dataset.src==='aquifer')aq++; else if(b.classList.contains('bs'))bs++;
    });
    meta.innerHTML='<span><b>'+(visible-bs-aq)+'</b> topics</span>'+
      '<span><b>'+bs+'</b> board-style</span>'+(aq?'<span><b>'+aq+'</b> Aquifer</span>':'')+'<span><b>'+liveSystems+'</b> systems</span>'+
      '<span><b>10</b> named trap species</span><span>Viewing <b>'+
      (SHELVES.filter(function(x){return x[0]===s;})[0]||['','Step 2'])[1]+'</b>'+(boardOnly&&!reviewSet?' &middot; board-style only':'')+'</span>';
  }
  document.querySelectorAll('.shelfpick button').forEach(function(b){b.classList.toggle('on',b.dataset.shelf===s);});
  document.querySelectorAll('.shelfsel').forEach(function(sel){if(sel.value!==s)sel.value=s;});
  setSearchMessage(visible,!!(reviewSet&&pin&&!reviewSet[pin]));
  try{ document.dispatchEvent(new CustomEvent('ax-shelf',{detail:{shelf:s,visible:visible}})); }catch(e){}
}
window.axApplyShelf=function(){ applyShelf(shelf); };
window.axShelf=function(){ return shelf; };

/* The address bar should always describe what is on screen, so a copied
   URL reproduces it for someone else. */
/* s113: switching shelf releases a pin the new shelf does not include. Without this a stale #brief in the
   address bar kept that brief, its system section and its sidebar link on every shelf you switched to. */
function unpinOffShelf(s){
  var id=pinnedId(); if(!id||reviewSet) return;
  if(shelfEligible(document.getElementById(id),s)) return;
  try{ var u=new URL(location.href); history.replaceState(null,'',u.pathname+u.search); }catch(e){}
}
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
    unpinOffShelf(b.dataset.shelf); keepPlace(function(){ applyShelf(b.dataset.shelf); });
    syncShelfUrl(b.dataset.shelf);
  });
  document.addEventListener('change',function(e){
    var sel=e.target;
    if(!sel.classList || !sel.classList.contains('shelfsel')) return;
    if(shelfPending(sel.value)){ sel.value=shelf; return; }
    unpinOffShelf(sel.value); keepPlace(function(){ applyShelf(sel.value); });
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
    gotoHash(!window.AXN);   // s143: an instant jump; axnav then seats the target while lazy briefs above it render
  });
}

/* ---------- 0b. one sidebar: fixed on desktop, off-canvas on phones ----------
   Desktop keeps the fixed sidebar. Below 1100px the same sidebar slides in from
   the left over a dimmed page, opened by the bar's Index button and closed by
   its X, a tap on the backdrop, Escape or choosing a link. Search is pinned at
   the top and the list scrolls beneath it. While open, the panel's height
   follows window.visualViewport, so the search field and its results stay
   above the iOS keyboard. No edge swipe: Safari owns that gesture for Back. */
var NAV_NARROW='(max-width:1100px)';
var navEl=null, navBar=null, navScrim=null, navOpen=false, navInvoker=null, navScrollY=0;
function navNarrow(){ return !!(window.matchMedia && window.matchMedia(NAV_NARROW).matches); }
function navFit(){
  var vv=window.visualViewport;
  if(!navEl) return;
  if(!navOpen || !vv){
    navEl.classList.remove('vvfit'); navEl.style.removeProperty('--vvh'); navEl.style.removeProperty('--vvt'); return;
  }
  navEl.style.setProperty('--vvh', Math.round(vv.height)+'px');
  navEl.style.setProperty('--vvt', Math.round(vv.offsetTop)+'px');
  navEl.classList.add('vvfit');
}
function navInert(on){
  var main=document.querySelector('main');
  [main, navBar].forEach(function(x){ if(!x) return; try{ x.inert=on; }catch(e){} if(on) x.setAttribute('aria-hidden','true'); else x.removeAttribute('aria-hidden'); });
}
function openNav(){
  if(navOpen || !navEl || !navNarrow()) return;
  navInvoker=document.activeElement;
  navOpen=true;
  navScrollY=window.pageYOffset||document.documentElement.scrollTop||0;
  /* Lock the page behind the panel. overflow:hidden alone does not stop iOS
     from scrolling the body, so the body is pinned in place and restored. */
  var bs=document.body.style;
  bs.position='fixed'; bs.top=(-navScrollY)+'px'; bs.left='0'; bs.right='0'; bs.width='100%';
  document.body.classList.add('navopen');
  navEl.setAttribute('role','dialog'); navEl.setAttribute('aria-modal','true');
  var ib=navBar && navBar.querySelector('[data-act="index"]'); if(ib) ib.setAttribute('aria-expanded','true');
  navInert(true);
  if(window.visualViewport){
    window.visualViewport.addEventListener('resize',navFit);
    window.visualViewport.addEventListener('scroll',navFit);
  }
  navFit();
  /* open on the brief being read */
  var sc=document.getElementById('navscroll'), act=navEl.querySelector('#navlinks a.active');
  if(sc && act && act.style.display!=='none' && !sxQuery() && !window.AXN){
    var off=act.getBoundingClientRect().top-sc.getBoundingClientRect().top+sc.scrollTop;
    sc.scrollTop=Math.max(0, off-sc.clientHeight/3);
  }
  /* On touch, focusing the field would raise the keyboard over the list, so
     focus goes to the close button; with a pointer it goes to the search. */
  var coarse=window.matchMedia && window.matchMedia('(pointer:coarse)').matches;
  var f=coarse ? navEl.querySelector('.navclose') : document.getElementById('search');
  if(f) try{ f.focus({preventScroll:true}); }catch(e){ f.focus(); }
}
function closeNav(restoreFocus){
  if(!navOpen) return;
  navOpen=false;
  if(window.visualViewport){
    window.visualViewport.removeEventListener('resize',navFit);
    window.visualViewport.removeEventListener('scroll',navFit);
  }
  navFit();
  document.body.classList.remove('navopen');
  var bs=document.body.style; bs.position=''; bs.top=''; bs.left=''; bs.right=''; bs.width='';
  var de=document.documentElement, sb=de.style.scrollBehavior;
  de.style.scrollBehavior='auto'; window.scrollTo(0,navScrollY); de.style.scrollBehavior=sb;
  navEl.removeAttribute('role'); navEl.removeAttribute('aria-modal');
  var ib=navBar && navBar.querySelector('[data-act="index"]'); if(ib) ib.setAttribute('aria-expanded','false');
  navInert(false);
  if(restoreFocus!==false){
    var back=(navInvoker && navInvoker.isConnected && !navEl.contains(navInvoker)) ? navInvoker : ib;
    if(back) try{ back.focus({preventScroll:true}); }catch(e){}
  } else if(ib && navEl.contains(document.activeElement)){
    try{ ib.focus({preventScroll:true}); }catch(e){}
  }
  navInvoker=null;
}
function mobileNav(){
  var nav=document.getElementById('nav'); if(!nav) return;
  navEl=nav;
  nav.setAttribute('aria-label','Index and search');

  /* Pinned head (brand, close, search) above one scrolling body (shelf,
     switches, review, then the systems list or the search results). */
  var top=document.createElement('div'); top.id='navtop';
  var body=document.createElement('div'); body.id='navscroll';
  var brand=nav.querySelector('.brand'), search=document.getElementById('search');
  var x=document.createElement('button'); x.type='button'; x.className='navclose';
  x.setAttribute('aria-label','Close index'); x.innerHTML='<span aria-hidden="true">\u2715</span>';
  Array.prototype.slice.call(nav.childNodes).forEach(function(n){ if(n!==brand && n!==search) body.appendChild(n); });
  if(brand) top.appendChild(brand);
  top.appendChild(x);
  if(search) top.appendChild(search);
  nav.appendChild(top); nav.appendChild(body);
  var res=document.createElement('div'); res.id='sxres'; res.hidden=true;
  res.innerHTML='<p class="sxstat" role="status" aria-live="polite"></p><ol class="sxlist" aria-label="Search results"></ol><div class="sxfoot"></div>';
  var links=document.getElementById('navlinks');
  if(links && links.parentNode===body) body.insertBefore(res,links); else body.appendChild(res);

  var bar=document.createElement('nav'); bar.id='mbar'; bar.setAttribute('aria-label','Page tools');
  bar.innerHTML =
    '<button type="button" data-act="index" aria-expanded="false" aria-controls="nav"><span>Index</span></button>'+
    '<button type="button" data-act="study" aria-pressed="false"><span>Recall</span></button>'+
    '<button type="button" data-act="top"><span>Top</span></button>';
  var scrim=document.createElement('div'); scrim.id='navscrim';
  document.body.appendChild(scrim);
  document.body.appendChild(bar);
  navBar=bar; navScrim=scrim;
  var mobileStudy=bar.querySelector('[data-act="study"]');
  if(mobileStudy) mobileStudy.setAttribute('aria-pressed',document.body.classList.contains('study')?'true':'false');

  bar.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    var a=b.dataset.act;
    if(a==='index'){ navOpen?closeNav():openNav(); }
    if(a==='study'){
      document.body.classList.toggle('study');
      try{ localStorage.setItem('ax-study',document.body.classList.contains('study')?'1':'0'); }catch(err){}
      b.setAttribute('aria-pressed',document.body.classList.contains('study')?'true':'false');
    }
    if(a==='top'){ closeNav(); window.scrollTo({top:0,behavior:(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)?'auto':'smooth'}); }
  });
  scrim.addEventListener('click',function(){ closeNav(); });
  x.addEventListener('click',function(){ closeNav(); });
  /* choosing an index link closes the panel; the browser then follows the hash */
  nav.addEventListener('click',function(e){
    var a=e.target.closest && e.target.closest('#navlinks a[href^="#"]');
    if(a && navOpen) closeNav(false);
  });
  document.addEventListener('keydown',function(e){
    if(!navOpen) return;
    var rp=document.getElementById('rvpanel'); if(rp && !rp.hidden) return;   /* the review popover handles its own keys */
    if(e.key==='Escape'){ e.preventDefault(); closeNav(); return; }
    if(e.key!=='Tab') return;
    var f=Array.prototype.filter.call(nav.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])'),function(el){
      return !el.disabled && el.getClientRects().length;
    });
    if(!f.length) return;
    var first=f[0], last=f[f.length-1];
    if(e.shiftKey && (document.activeElement===first || !nav.contains(document.activeElement))){ e.preventDefault(); last.focus(); }
    else if(!e.shiftKey && (document.activeElement===last || !nav.contains(document.activeElement))){ e.preventDefault(); first.focus(); }
  });
  if(window.matchMedia){
    var mq=window.matchMedia(NAV_NARROW), onMq=function(){ if(!mq.matches) closeNav(false); };
    if(mq.addEventListener) mq.addEventListener('change',onMq); else if(mq.addListener) mq.addListener(onMq);
  }
  sxWire();
}

/* ---------- 0c. full-text search (one index for desktop and phone) ----------
   Built once from each brief's visible text, block by block (title, subtitle,
   decision point, criteria, tables, pearls, rule, traps, bank items, vignette).
   Case, accents and punctuation are normalized; every query word must occur in
   the brief (any order, word-start match). Ranking: the block that holds the
   most query words, then title > subtitle > decision point > the rest, then
   hit count. Results list in the sidebar in place of the systems list and
   respect the shelf, Board-style only and an active review. */
var SX={built:false, briefs:[], groups:[], gmap:{}, oneway:{}, buildMs:0, queryMs:0, hits:[], timer:null, cap:60};
/* Small hand map; "ACRONYM (expansion)" pairs on the page are added at build.
   A leading ~ marks a one-way alias: typing it finds the group, but the group
   does not widen to it (HPS is also the Heart Protection Study). */
var SX_ALIASES=[
  ['ihps','~hps','pyloric stenosis','hypertrophic pyloric stenosis','infantile hypertrophic pyloric stenosis','pyloric','pyloromyotomy'],
  ['tef','tracheoesophageal fistula','esophageal atresia'],
  ['puv','posterior urethral valves'],
  ['vur','vesicoureteral reflux'],
  ['uti','urinary tract infection'],
  ['nec','necrotizing enterocolitis'],
  ['gerd','gastroesophageal reflux'],
  ['dka','diabetic ketoacidosis'],
  ['ddh','developmental dysplasia of the hip','hip dysplasia'],
  ['scfe','slipped capital femoral epiphysis'],
  ['jia','juvenile idiopathic arthritis'],
  ['itp','immune thrombocytopenia','immune thrombocytopenic purpura'],
  ['hsp','henoch schonlein purpura','iga vasculitis'],
  ['rsv','respiratory syncytial virus'],
  ['kawasaki','mucocutaneous lymph node syndrome'],
  ['ekg','ecg','electrocardiogram','electrocardiography'],
  ['cxr','chest x ray','chest radiograph'],
  ['mi','myocardial infarction'],
  ['copd','chronic obstructive pulmonary disease'],
  ['sids','sudden infant death'],
  ['adhd','attention deficit'],
  ['ibd','inflammatory bowel disease']
];
/* Case and accents fold one character to one character, so an offset in the
   folded text is an offset in the visible text. Punctuation is not rewritten
   in the index (that pass is the expensive one); matching treats any
   character that is not a letter or digit as a word boundary instead. */
function sxNorm(s){
  var l=s.toLowerCase();
  if(l.length!==s.length){ l=''; for(var i=0;i<s.length;i++){ l+=s.charAt(i).toLowerCase().charAt(0); } }
  if(!/[\u00c0-\u024f]/.test(l)) return l;
  return l.replace(/[\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u024f]/g,function(c){
    var d=c.normalize ? c.normalize('NFD').charAt(0) : c; return /[a-z]/.test(d) ? d : c;
  });
}
function sxQNorm(s){ return sxNorm(s).replace(/[^a-z0-9\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u024f\u0370-\u03ff]+/g,' ').trim(); }
function sxAl(c){ return (c>=97&&c<=122)||(c>=48&&c<=57)||(c>=65&&c<=90)||(c>=0xc0&&c<=0x24f&&c!==0xd7&&c!==0xf7)||(c>=0x370&&c<=0x3ff); }
function sxQuery(){ var i=document.getElementById('search'); return i ? norm(i.value) : ''; }
function sxNow(){ return (window.performance && performance.now) ? performance.now() : Date.now(); }
function sxEsc(s){ return s.replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

var SX_SKIP=/(^|\s)(lbl|mask-toggle|k|rv|qp|bktools|bkfilter|scalepeek|availability|reviewwrap|rvmark|cue|arw)(\s|$)/;
var SX_MASK=/(^|\s)(mask|why)(\s|$)/;
/* brief navigation added at build (bounds bar, rail, end line): not brief text, and absent from a template copy */
var SX_CHROME=/(^|\s)(bb-bar|bb-rail|bb-end)(\s|$)/;
var SX_BRKT={DIV:1,P:1,LI:1,DT:1,DD:1,TD:1,TH:1,TR:1,BR:1,H4:1,H5:1,H6:1,UL:1,OL:1,DL:1,TABLE:1,CAPTION:1,THEAD:1,TBODY:1,BUTTON:1,text:1};
function sxBlk(el,label,rank){ return {el:el,label:label,rank:rank,raw:'',n:'',bank:-1}; }
/* One traversal, used twice: at build (to collect text) and at lookup (to find
   the node and mask state behind a character offset). emit(text,node,masked). */
function sxTrav(root,masked,emit){
  for(var n=root.firstChild;n;n=n.nextSibling){
    var t=n.nodeType;
    if(t===3){ emit(n.nodeValue,n,masked); continue; }
    if(t!==1) continue;
    var tg=n.tagName; if(tg==='SCRIPT' || tg==='STYLE') continue;
    var cn=n.className, m=masked; if(typeof cn!=='string') cn=n.getAttribute('class')||'';
    if(cn){ if(SX_SKIP.test(cn)) continue; if(!m && SX_MASK.test(cn)) m=true; }
    var brk=SX_BRKT[tg]===1;
    if(brk) emit(' ',null,m);
    sxTrav(n,m,emit);
    if(brk) emit(' ',null,m);
  }
}
/* One bank item: stem, then the options joined with " \u00b7 ", then the answer
   chain (answer side, so it counts as masked). A chain node that repeats the
   stem or an option label is skipped, so no label appears twice. */
var SX_SEP=' \u00b7 ';
function sxBankTrav(m,emit){
  var seen={}, key=function(el){ return norm(el.textContent).toLowerCase(); };
  var st=m.querySelector(':scope > .top .stem'); if(st) seen[key(st)]=1;
  for(var c=m.firstElementChild;c;c=c.nextElementSibling){
    var cn=c.getAttribute('class')||'';
    if(/(^|\s)opts(\s|$)/.test(cn)){
      for(var o=c.firstElementChild;o;o=o.nextElementSibling){
        var kk=o.querySelector('.k'), ok=norm(o.textContent.slice(kk ? kk.textContent.length : 0)).toLowerCase();
        if(!ok || seen[ok]) continue; seen[ok]=1;
        emit(SX_SEP,null,false); sxTrav(o,false,emit);
      }
      continue;
    }
    if(/(^|\s)why(\s|$)/.test(cn)){
      var ch=c.querySelector('.chain');
      if(!ch){ emit(SX_SEP,null,true); sxTrav(c,true,emit); continue; }
      for(var nd=ch.firstElementChild;nd;nd=nd.nextElementSibling){
        if(/(^|\s)arw(\s|$)/.test(nd.getAttribute('class')||'')) continue;
        var nk=key(nd); if(!nk || seen[nk]) continue; seen[nk]=1;
        emit(SX_SEP,null,true); sxTrav(nd,true,emit);
      }
      continue;
    }
    if(SX_SKIP.test(cn)) continue;
    emit(' ',null,false); sxTrav(c,false,emit);
  }
}
function sxWalk(k,emit){ if(k.bank>-1) sxBankTrav(k.el,emit); else sxTrav(k.el,false,emit); }
/* raw = the pieces joined, whitespace collapsed, trimmed; sxLocate replays the
   same collapse to map a raw offset back to its text node. */
function sxLocate(k,off){
  var pos=0, sp=true, hit=null, WS=/\s/;
  try{
    sxWalk(k,function(text,node,masked){
      if(hit) throw 0;
      for(var i=0;i<text.length;i++){
        if(WS.test(text.charAt(i))){ if(!sp){ sp=true; pos++; } }
        else { if(pos>=off){ hit={node:node,masked:masked}; throw 0; } sp=false; pos++; }
      }
    });
  }catch(e){ if(e!==0) throw e; }
  return hit;
}
function sxLabel(el){
  var cl=el.classList, t=el.tagName;
  if(t==='H4') return ['Title',0];
  if(cl.contains('sub')) return ['Subtitle',1];
  if(cl.contains('dp')) return ['Decision point',2];
  if(cl.contains('vignette')) return ['Source vignette',3];
  if(cl.contains('crit')) return ['Criteria',3];
  if(cl.contains('tw') || t==='TABLE') return ['Table',3];
  if(cl.contains('rule')) return ['Rule',3];
  if(cl.contains('traps')) return ['Traps',3];
  if(cl.contains('figure')) return ['Figure',3];
  if(cl.contains('pearls') || cl.contains('danger')){
    var l=el.querySelector(':scope > .lbl'), s=l ? norm(l.textContent) : '';
    s=s.split(/\s+[\u2014\u2013]\s+|:/)[0].trim();   /* "Neonatal conjunctivitis \u2013 a practical..." -> its name */
    if(s.length>30) s=s.slice(0,29)+'\u2026';
    return [s || (cl.contains('pearls') ? 'Pearls' : 'Caution'),3];
  }
  if(t==='H5') return cl.contains('authored-hdr') ? null : ['Heading',3];
  return ['Text',3];
}
function sxGroup(phrases){
  var g=-1;
  phrases=phrases.map(function(p){ if(p.charAt(0)==='~'){ p=p.slice(1); SX.oneway[p]=1; } return p; });
  phrases.forEach(function(p){ if(g<0 && SX.gmap[p]!==undefined) g=SX.gmap[p]; });
  if(g<0){ g=SX.groups.length; SX.groups.push([]); }
  phrases.forEach(function(p){
    if(!p || SX.gmap[p]!==undefined || SX.groups[g].length>=14) return;
    SX.gmap[p]=g; SX.groups[g].push(p);
  });
}
function sxSubseq(acr,phrase){
  var i=0; for(var j=0;j<phrase.length && i<acr.length;j++) if(phrase.charAt(j)===acr.charAt(i)) i++;
  return i===acr.length;
}
/* "AFP (alpha-fetoprotein)" and "alpha-fetoprotein (AFP)": the expansion must
   start with the acronym's first letter and contain its letters in order. */
function sxPairs(raw){
  var m, re=/\b([A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*?)(s?) \(([^()]{3,70})\)/g;
  while((m=re.exec(raw))){
    var acr=m[1].toLowerCase(), exp=sxQNorm(m[3]);
    if(acr.length<2 || acr.length>8 || /[,;:]/.test(m[3])) continue;
    var ew=exp.split(' ');
    if(ew.length>acr.length+3 || exp.charAt(0)!==acr.charAt(0) || !sxSubseq(acr,exp.replace(/ /g,''))) continue;
    sxGroup([acr,exp]);
  }
  var r2=/\(([A-Z][A-Za-z0-9]*[A-Z0-9])s?\)/g;
  while((m=r2.exec(raw))){
    var a=m[1].toLowerCase(); if(a.length<2 || a.length>8 || !/[a-z]/.test(a)) continue;
    var pre=raw.slice(Math.max(0,m.index-90),m.index);
    pre=pre.slice(Math.max(pre.lastIndexOf(','),pre.lastIndexOf(';'),pre.lastIndexOf(':'),pre.lastIndexOf('.'),pre.lastIndexOf('('),pre.lastIndexOf('\u00b7'))+1);
    var w=sxQNorm(pre).split(' ');
    for(var n=1;n<=Math.min(w.length,a.length+2);n++){
      var ph=w.slice(w.length-n).join(' ');
      if(ph.charAt(0)===a.charAt(0) && sxSubseq(a,ph.replace(/ /g,''))){ if(ph!==a) sxGroup([a,ph]); break; }
    }
  }
}
/* One brief's record. A built brief is read from the page. An unbuilt brief is read from a detached copy of its
   template run through every per-brief pass (AX.brief.copy), as a build runs them, so the text, block labels and
   masks match the built brief; the copy is dropped and each block keeps its masked ranges (k.mr) for snippets. On brief:built the
   record is read again from the page. */
function sxRecord(b,di){
  var root=b, lazy=!AX.brief.isBuilt(b);
  if(lazy){
    var keep=window.__ax; root=AX.brief.copy(b); window.__ax=keep;
  }
  var h=null; for(var e=root.firstElementChild;e;e=e.nextElementSibling) if(e.tagName==='H4'){ h=e; break; }
  var rec={b:b,id:b.id,di:di,lazy:lazy,title:h ? norm(h.textContent) : b.id,sub:'',blocks:[],all:''};
  var add=function(k){
    var parts=[], vis=[], mr=[], pos=0, sp=true, WS=/\s/;
    sxWalk(k,function(t,n,m){
      parts.push(t); if(!m) vis.push(t);
      if(!lazy) return;
      for(var i=0;i<t.length;i++){
        if(WS.test(t.charAt(i))){ if(!sp){ sp=true; pos++; } continue; }
        if(m){ var last=mr[mr.length-1]; if(last && last[1]===pos) last[1]++; else mr.push([pos,pos+1]); }
        sp=false; pos++;
      }
    });
    k.raw=parts.join('').replace(/\s+/g,' ').trim();
    if(k.bank>-1) k.stemEnd=vis.join('').replace(/\s+/g,' ').trim().length;   /* the answer chain comes last */
    if(lazy){ k.mr=mr; k.el=null; }
    if(k.raw) rec.blocks.push(k);
  };
  for(var c=root.firstElementChild;c;c=c.nextElementSibling){
    if(c.classList.contains('bankwrap')){
      Array.prototype.forEach.call(c.querySelectorAll('.mcqwrap > .mcq'),function(m,i){
        var k=sxBlk(m,'Question',3); k.bank=i; add(k);
      });
      continue;
    }
    if(c.classList.contains('rvmark') || SX_CHROME.test(c.className)) continue;
    var L=sxLabel(c); if(!L) continue;
    var k=sxBlk(c,L[0],L[1]); add(k);
    if(L[1]===1 && !rec.sub) rec.sub=k.raw;
  }
  var parts=[];
  rec.blocks.forEach(function(k){ k.n=sxNorm(k.raw); parts.push(k.n); sxPairs(k.raw); });
  rec.all=parts.join('\n');
  return rec;
}
function sxBuildOne(b,di){ if(b.id) SX.briefs.push(sxRecord(b,di)); }
/* masked state at a raw offset for a record read from a template copy: the first character at or after it */
function sxMaskedAt(k,off){
  var p=off; while(p<k.raw.length && k.raw.charAt(p)===' ') p++;
  for(var i=0;i<k.mr.length;i++){ if(p<k.mr[i][0]) break; if(p<k.mr[i][1]) return true; }
  return false;
}
AX.on('brief:built',function(b){
  for(var i=0;i<SX.briefs.length;i++) if(SX.briefs[i].b===b){ if(SX.briefs[i].lazy) SX.briefs[i]=sxRecord(b,SX.briefs[i].di); return; }
});
/* Built in idle slices after load so it never blocks a tap; a query that
   arrives first finishes the build on the spot. */
function sxBuild(deadline){
  if(SX.built) return;
  if(!SX.list){ SX.list=document.querySelectorAll('.brief'); SX.next=0; SX.work=0; SX.t0=sxNow(); SX_ALIASES.forEach(function(g){ sxGroup(g.map(function(p){ return (p.charAt(0)==='~'?'~':'')+sxQNorm(p); })); }); }
  var t0=sxNow();
  while(SX.next<SX.list.length){
    sxBuildOne(SX.list[SX.next],SX.next); SX.next++;
    if(deadline && (deadline.didTimeout ? sxNow()-t0>12 : deadline.timeRemaining()<2)) break;
  }
  SX.work+=sxNow()-t0; SX.slices=(SX.slices||0)+1;
  if(SX.next>=SX.list.length){ SX.built=true; SX.buildMs=Math.round(SX.work); SX.wallMs=Math.round(sxNow()-SX.t0); }
  else sxIdle();
}
function sxIdle(){
  if(window.requestIdleCallback) requestIdleCallback(sxBuild,{timeout:1500});
  else setTimeout(function(){ var t=sxNow(); sxBuild({didTimeout:false,timeRemaining:function(){ return 12-(sxNow()-t); }}); },40);
}
/* query -> terms; each term is a set of alternatives, and a brief must match
   every term. Typed words match at a word start (words of one or two letters
   whole); alias phrases match whole and in order. */
function sxTerms(q){
  var w=sxQNorm(q).split(' ').filter(Boolean), terms=[];
  for(var i=0;i<w.length;){
    var took=0;
    for(var k=Math.min(5,w.length-i);k>=1 && !took;k--){
      var ph=w.slice(i,i+k).join(' '), g=SX.gmap[ph];
      if(g===undefined) continue;
      var alts=[{words:w.slice(i,i+k)}];
      SX.groups[g].forEach(function(p){ if(p!==ph && !SX.oneway[p]) alts.push({phrase:p}); });
      terms.push(alts); took=k;
    }
    if(!took){ terms.push([{words:[w[i]]}]); took=1; }
    i+=took;
  }
  return terms;
}
/* next match of w at or after `from` that starts a word; exact also needs it to
   end one. Words of one or two letters always match whole. Returns index or -1. */
function sxFind(s,w,from,exact){
  if(w.length<=2) exact=true;
  var p=s.indexOf(w,from);
  while(p>-1){
    if((p===0 || !sxAl(s.charCodeAt(p-1))) && (!exact || !sxAl(s.charCodeAt(p+w.length)))) return p;
    p=s.indexOf(w,p+1);
  }
  return -1;
}
/* a phrase: its words in order, separated by anything that is not a letter or
   digit ("alpha fetoprotein" finds "alpha-fetoprotein"). Returns end or -1. */
function sxPhraseEnd(s,p,words){
  var pos=p;
  for(var i=0;i<words.length;i++){
    if(i){ var j=pos; while(j<s.length && !sxAl(s.charCodeAt(j))) j++; if(j===pos) return -1; pos=j; }
    if(s.substr(pos,words[i].length)!==words[i]) return -1;
    pos+=words[i].length;
  }
  return sxAl(s.charCodeAt(pos)) ? -1 : pos;
}
function sxPhraseFind(s,words,from){
  var p=sxFind(s,words[0],from,words.length===1);
  while(p>-1){ var e=sxPhraseEnd(s,p,words); if(e>-1) return [p,e]; p=sxFind(s,words[0],p+1,words.length===1); }
  return null;
}
function sxCountWord(s,w,cap,out){
  var n=0, p=sxFind(s,w,0,false);
  while(p>-1 && n<cap){ if(out.first<0 || p<out.first) out.first=p; n++; p=sxFind(s,w,p+1,false); }
  return n;
}
function sxCountPhrase(s,words,cap,out){
  var n=0, m=sxPhraseFind(s,words,0);
  while(m && n<cap){ if(out.first<0 || m[0]<out.first) out.first=m[0]; n++; m=sxPhraseFind(s,words,m[1]); }
  return n;
}
function sxAltHits(s,alt,cap,out){
  if(alt.phrase) return sxCountPhrase(s,alt.pw||(alt.pw=alt.phrase.split(' ')),cap,out);
  var tot=0, tmp={first:-1};
  for(var i=0;i<alt.words.length;i++){
    var c=sxCountWord(s,alt.words[i],cap,tmp); if(!c) return 0; tot+=c;
  }
  if(tmp.first>-1 && (out.first<0 || tmp.first<out.first)) out.first=tmp.first;
  return tot;
}
function sxTermHits(s,alts,cap,out){
  var t=0, own={first:-1}, alias={first:-1};
  for(var i=0;i<alts.length;i++) t+=sxAltHits(s,alts[i],cap,i===0?own:alias);
  var f=own.first>-1 ? own.first : alias.first;
  if(f>-1 && (out.first<0 || f<out.first)) out.first=f;
  return t;
}
function sxInShelf(b){ return shelfEligible(b,shelf); }
function sxSearch(q){
  sxBuild();
  var t0=sxNow(), terms=sxTerms(q), hits=[], other=0;
  if(!terms.length) return {hits:hits,other:0,ms:0};
  SX.briefs.forEach(function(r){
    var inShelf=sxInShelf(r.b);
    if(!inShelf && (reviewSet || !shelfEligible(r.b,'step2'))) return;
    for(var i=0;i<terms.length;i++) if(!sxTermHits(r.all,terms[i],1,{first:-1})) return;
    if(!inShelf){ other++; return; }
    var best=null, total=0;
    r.blocks.forEach(function(k,bi){
      var m=0, h=0, out={first:-1};
      for(var i=0;i<terms.length;i++){ var c=sxTermHits(k.n,terms[i],40,out); if(c){ m++; h+=c; } }
      if(!m) return;
      total+=h;
      if(!best || m>best.m || (m===best.m && (k.rank<best.rank || (k.rank===best.rank && h>best.h))))
        best={bi:bi,m:m,rank:k.rank,h:h,first:out.first};
    });
    if(best) hits.push({r:r,best:best,total:total});
  });
  hits.sort(function(a,b){
    return (b.best.m-a.best.m) || (a.best.rank-b.best.rank) || (b.total-a.total) || (a.r.di-b.r.di);
  });
  SX.queryMs=Math.round((sxNow()-t0)*10)/10;
  return {hits:hits,other:other,terms:terms,ms:SX.queryMs};
}
/* spans to highlight: every query word (to the end of its word) or alias
   phrase that starts inside [a,b) of the folded text n */
function sxMarks(n,a,b,terms){
  var spans=[];
  terms.forEach(function(alts){ alts.forEach(function(alt){
    if(alt.phrase){
      var pw=alt.pw||(alt.pw=alt.phrase.split(' ')), m=sxPhraseFind(n,pw,a);
      while(m && m[0]<b){ spans.push(m); m=sxPhraseFind(n,pw,m[1]); }
      return;
    }
    alt.words.forEach(function(w){
      var p=sxFind(n,w,a,false);
      while(p>-1 && p<b){
        var e=p+w.length; while(e<n.length && sxAl(n.charCodeAt(e))) e++;
        spans.push([p,e]); p=sxFind(n,w,p+1,false);
      }
    });
  }); });
  spans.sort(function(x,y){ return x[0]-y[0]; });
  return spans;
}
function sxHl(raw,n,a,b,terms){
  var spans=sxMarks(n,a,b,terms), out='', at=a;
  spans.forEach(function(sp){
    var s=Math.max(sp[0],at), e=Math.min(sp[1],b); if(e<=s) return;
    out+=sxEsc(raw.slice(at,s))+'<mark>'+sxEsc(raw.slice(s,e))+'</mark>'; at=e;
  });
  return out+sxEsc(raw.slice(at,b));
}
function sxSnippet(k,first,terms){
  var masked=k.el ? !!((sxLocate(k,first)||{}).masked) : sxMaskedAt(k,first), inAnswer=false;
  /* A bank item's answer stays hidden until the reader answers it, in any
     mode, so a hit there shows the stem instead of spoiling the key. */
  if(masked && k.bank>-1){ first=0; masked=false; inAnswer=true; }
  var raw=k.raw, L=raw.length, a=Math.max(0,first-42), b;
  if(a>0){ var sp=raw.indexOf(' ',a); a=(sp>-1 && sp<first) ? sp+1 : a; }
  b=Math.min(L,a+150);
  if(b<L){ var sp2=raw.lastIndexOf(' ',b); if(sp2>first) b=sp2; }
  if(k.bank>-1 && k.stemEnd && first<k.stemEnd) b=Math.min(b,k.stemEnd);   /* never run on into the answer chain */
  return {answer:inAnswer, html:(a>0?'\u2026':'')+sxHl(raw,k.n,a,b,terms)+(b<L?'\u2026':''), masked:masked};
}
function sxShelfName(){
  if(reviewSet) return 'the active review';
  return (SHELVES.filter(function(x){ return x[0]===shelf; })[0]||['','Step 2'])[1];
}
function sxRender(){
  var input=document.getElementById('search'), res=document.getElementById('sxres'), nav=navEl;
  if(!input || !res || !nav) return;
  var q=norm(input.value);
  if(!q){ res.hidden=true; nav.classList.remove('sxon'); SX.hits=[]; return; }
  var out=sxSearch(q), hits=out.hits, list=res.querySelector('.sxlist'), stat=res.querySelector('.sxstat'), foot=res.querySelector('.sxfoot');
  SX.hits=hits;
  var scope=sxShelfName()+(boardOnly && !reviewSet ? ', board-style only' : '');
  stat.innerHTML=hits.length ? ('<b>'+hits.length+'</b> '+(hits.length===1?'brief':'briefs')+' in '+sxEsc(scope))
                             : ('No matches in '+sxEsc(scope)+'.');
  var h='';
  hits.slice(0,SX.cap).forEach(function(x,i){
    var r=x.r, k=r.blocks[x.best.bi], label=k.label, snip;
    if(k.rank===0){
      var tn=sxNorm(r.title);
      snip={html:sxEsc(r.sub||''),masked:false};
      var th=sxHl(r.title,tn,0,r.title.length,out.terms);
      h+='<li><a class="sxhit" href="#'+sxEsc(r.id)+'" data-i="'+i+'"><span class="t">'+th+'</span><span class="b">Title</span>'+(snip.html?'<span class="s">'+snip.html+'</span>':'')+'</a></li>';
      return;
    }
    snip=sxSnippet(k,x.best.first,out.terms);
    var tn2=sxNorm(r.title);
    h+='<li><a class="sxhit" href="#'+sxEsc(r.id)+'" data-i="'+i+'"><span class="t">'+sxHl(r.title,tn2,0,r.title.length,out.terms)+'</span>'+
       '<span class="b">'+sxEsc(label+(snip.answer?', in the answer':''))+'</span><span class="s'+(snip.masked?' sxm':'')+'">'+snip.html+'</span></a></li>';
  });
  list.innerHTML=h;
  var f='';
  if(hits.length>SX.cap) f+='<p class="sxcap">Showing the first '+SX.cap+' of '+hits.length+'. Add a word to narrow.</p>';
  if(out.other) f+='<button type="button" class="sxmore">'+out.other+' more in other shelves</button>';
  foot.innerHTML=f;
  res.hidden=false; nav.classList.add('sxon');
}
function sxSchedule(){
  clearTimeout(SX.timer);
  SX.timer=setTimeout(sxRender,120);
}
/* Open the brief, scroll to the block that matched and flash it. Study-mode
   masks are left exactly as they were. */
function sxLand(x){
  if(x.r.lazy){
    /* build the brief, then search again so the hit points at the page */
    var id=x.r.id; AX.brief.ensure(x.r.b);
    var again=sxSearch(sxQuery()).hits.filter(function(h){ return h.r.id===id; })[0];
    var rb=SX.briefs.filter(function(r){ return r.id===id; })[0];
    x=again || {r:rb,best:{bi:0,first:-1}};
    if(!x.r || x.r.lazy || !x.r.blocks.length) return;
  }
  var r=x.r, k=r.blocks[x.best.bi], el=k.el;
  if(navOpen) closeNav(false);
  try{ if(history.replaceState) history.replaceState(null,'','#'+r.id); }catch(e){}
  applyShelf(shelf);
  if(k.bank>-1){
    var bw=el.closest('.bankwrap');
    if(bw && bw.classList.contains('review')){ var rr=bw.querySelectorAll('.reviewwrap > .rrow')[k.bank]; if(rr) el=rr; }
  }
  var tgt=el;
  if(k.rank>0 && x.best.first>-1 && el===k.el){
    var loc=sxLocate(k,x.best.first), node=loc && loc.node;
    var p=node && node.parentElement;
    while(p && p!==el && !p.getClientRects().length) p=p.parentElement;
    if(p && el.contains(p) && /^(TD|TH|LI|DD|DT|P|DIV|SPAN|B|I)$/.test(p.tagName)){
      while(p!==el && /^(SPAN|B|I|A)$/.test(p.tagName)) p=p.parentElement;
      tgt=p;
    }
  }
  var reduce=window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var y=function(){
    var rc=tgt.getBoundingClientRect(), vh=window.innerHeight||document.documentElement.clientHeight;
    return Math.max(0,(window.pageYOffset||0)+rc.top-(rc.height<vh*0.6 ? (vh-rc.height)/2 : 76));
  };
  requestAnimationFrame(function(){
    AX.emit('brief:reveal',{y:y,smooth:!reduce});
    el.classList.remove('sxflash'); void el.offsetWidth; el.classList.add('sxflash');
    clearTimeout(el._sxT); el._sxT=setTimeout(function(){ el.classList.remove('sxflash'); },2100);
  });
}
function sxWire(){
  var input=document.getElementById('search'), res=document.getElementById('sxres');
  if(!input || !res) return;
  input.setAttribute('placeholder','Search all '+document.querySelectorAll('.brief').length+' briefs\u2026');
  input.setAttribute('aria-label','Search all briefs');
  input.setAttribute('aria-controls','sxres');
  input.setAttribute('enterkeyhint','search');
  input.setAttribute('autocapitalize','off'); input.setAttribute('autocorrect','off'); input.setAttribute('spellcheck','false');
  input.addEventListener('input',sxSchedule);
  input.addEventListener('keydown',function(e){
    if(e.key==='Enter'){ e.preventDefault(); clearTimeout(SX.timer); sxRender(); if(SX.hits.length) sxLand(SX.hits[0]); }
    else if(e.key==='ArrowDown'){ var a=res.querySelector('a.sxhit'); if(a){ e.preventDefault(); a.focus(); } }
    else if(e.key==='Escape' && input.value && !navOpen){ input.value=''; sxRender(); }
  });
  res.addEventListener('click',function(e){
    var more=e.target.closest && e.target.closest('.sxmore');
    if(more){ applyShelf('step2'); syncShelfUrl('step2'); return; }
    var a=e.target.closest && e.target.closest('a.sxhit'); if(!a) return;
    e.preventDefault();
    var x=SX.hits[parseInt(a.getAttribute('data-i'),10)]; if(x) sxLand(x);
  });
  document.addEventListener('ax-shelf',function(){ if(sxQuery()) sxRender(); });
  /* build while the reader is still looking at the masthead */
  sxIdle();
  window.__axSearch={build:sxBuild,search:function(q){ return sxSearch(q); },render:sxRender,
    stats:function(){ return {built:SX.built,buildMs:SX.buildMs,wallMs:SX.wallMs,slices:SX.slices,queryMs:SX.queryMs,briefs:SX.briefs.length,groups:SX.groups.length}; }};
}

/* ---------- 1. section headers get a protruding numbered tab ---------- */
var SHORT={presentations:'CC',msk:'MSK',peds:'PEDS',cv:'CV',pulm:'PULM',gi:'GI',renal:'RENAL',endo:'ENDO',
           id:'ID',neuro:'NEURO',derm:'DERM',obgyn:'OBGYN',prev:'PREV',strategy:'START',heme:'HEME',psych:'PSYCH'};
function sections(){
  var n=0;
  document.querySelectorAll('h3.system').forEach(function(h){
    n++;
    var note=h.nextElementSibling && h.nextElementSibling.classList.contains('system-note') ? h.nextElementSibling : null;
    var wrap=document.createElement('div'); wrap.className='sectwrap';
    var card=document.createElement('div'); card.className='sectcard';
    var tab=document.createElement('div'); tab.className='tab';
    tab.innerHTML='<b>'+String(n).padStart(2,'0')+'</b><i>'+(SHORT[h.id]||'')+'</i>';
    h.parentNode.insertBefore(wrap,h);
    wrap.appendChild(tab); wrap.appendChild(card);
    card.appendChild(h); if(note) card.appendChild(note);
  });
}

/* ---------- 2. tables become raised cards; tier tables tagged ---------- */
function tables(R){
  (R||document).querySelectorAll('table').forEach(function(t){
    /* labelling must happen even for tables authored pre-wrapped in .tw —
       otherwise their cells lose their column headers on phones */
    var wrapped = t.parentNode.classList && t.parentNode.classList.contains('tw');
    var th=Array.prototype.slice.call(t.querySelectorAll('thead th'));
    if(th.length && /^tier/i.test(th[0].textContent.trim())) t.classList.add('tierT');
    /* Carry each column's header onto its cells. On phones the table
       restacks into one card per row and these become the micro-labels,
       so the row keeps its meaning without horizontal scrolling — which
       otherwise pushes the first column (the diagnosis) off screen. */
    var heads=th.map(function(x){ return norm(x.textContent); });
    t.querySelectorAll('tbody tr').forEach(function(tr){
      Array.prototype.slice.call(tr.children).forEach(function(td,i){
        if(heads[i]) td.setAttribute('data-label',heads[i]);
      });
    });
    t.querySelectorAll('tbody tr').forEach(function(tr){
      if(tr.querySelector('.t-em')) tr.classList.add('em');
    });
    if(wrapped) return;
    var w=document.createElement('div'); w.className='tw';
    t.parentNode.insertBefore(w,t); w.appendChild(t);
  });
}

/* ---------- 3. columnize ·-separated and Term — definition blocks ------
   Two shapes appear in these blocks:
     (a) "<b>Term</b> – definition · <b>Term</b> – definition"
     (b) "fact · fact · fact"
   (a) becomes an aligned dt/dd grid; (b) becomes a bulleted fact list.
   Splitting is done on a cloned fragment so inline markup survives.     */
function splitTop(node, ch){
  var parts=[], cur=document.createDocumentFragment();
  node.childNodes.forEach ? null : null;
  Array.prototype.slice.call(node.childNodes).forEach(function(n){
    if(n.nodeType===3 && n.nodeValue.indexOf(ch)>-1){
      var bits=n.nodeValue.split(ch);
      bits.forEach(function(b,i){
        if(i>0){ parts.push(cur); cur=document.createDocumentFragment(); }
        if(b) cur.appendChild(document.createTextNode(b));
      });
    } else cur.appendChild(n.cloneNode(true));
  });
  parts.push(cur);
  return parts.filter(function(f){ return norm(f.textContent).length; });
}
function fragHasLeadingBoldDash(f){
  var first=null;
  for(var i=0;i<f.childNodes.length;i++){
    var n=f.childNodes[i];
    if(n.nodeType===3 && !n.nodeValue.trim()) continue;
    first=n; break;
  }
  if(!first || first.nodeType!==1 || !/^(B|STRONG)$/.test(first.tagName)) return false;
  return /\s[—–]\s/.test(f.textContent);
}
function columnize(R){
  (R||document).querySelectorAll('.pearls,.danger,.dp,.rule,.crit,.vignette').forEach(function(blk){
    var lbl=blk.querySelector(':scope > .lbl');
    // only operate on the block's own inline content, not nested tables/lists
    if(blk.querySelector('table,ol,ul,dl')) return;
    var holder=document.createElement('div');
    Array.prototype.slice.call(blk.childNodes).forEach(function(n){
      if(n===lbl) return; holder.appendChild(n);
    });
    if(holder.textContent.indexOf('·')<0){ blk.appendChild(holder.firstChild?frag(holder):document.createTextNode('')); return restore(blk,holder); }
    var parts=splitTop(holder,'·');
    if(parts.length<2){ return restore(blk,holder); }
    var termish=parts.filter(fragHasLeadingBoldDash).length;
    if(termish >= Math.ceil(parts.length*0.6)){
      var dl=document.createElement('dl'); dl.className='rows';
      parts.forEach(function(f){
        var txt=f.textContent, m=txt.match(/\s[—–]\s/);
        if(!m){ var dt0=document.createElement('dt'); dt0.appendChild(f); dl.appendChild(dt0);
                dl.appendChild(document.createElement('dd')); return; }
        var idx=txt.indexOf(m[0]);
        var walker=splitAtOffset(f, idx, m[0].length);
        var dt=document.createElement('dt'); dt.appendChild(walker[0]);
        var dd=document.createElement('dd'); var sp=document.createElement('span');
        sp.className = blk.classList.contains('vignette') ? 'nomask' : 'mask';
        sp.appendChild(walker[1]); dd.appendChild(sp);
        dl.appendChild(dt); dl.appendChild(dd);
      });
      markShortRows(dl);
      blk.appendChild(dl);
    } else {
      var ul=document.createElement('ul'); ul.className='facts';
      parts.forEach(function(f){ var li=document.createElement('li'); li.appendChild(f); ul.appendChild(li); });
      blk.appendChild(ul);
    }
  });
}
function restore(blk,holder){ while(holder.firstChild) blk.appendChild(holder.firstChild); }
/* A grid whose labels are all short gets a label column of up to a third of the width.
   With plain auto sizing, a long right-hand column squeezes the label track to its
   narrowest word and "Versus ITP" stacks one word per line. Sentence-length labels
   keep the old sizing. */
function markShortRows(dl){
  var dts=Array.prototype.slice.call(dl.children).filter(function(x){return x.tagName==='DT';});
  if(dts.length && dts.every(function(dt){ return dt.textContent.trim().length<=34; })) dl.classList.add('rows-short');
}
function frag(h){ var f=document.createDocumentFragment(); while(h.firstChild) f.appendChild(h.firstChild); return f; }
/* split a fragment's flat text at an offset, preserving element nodes */
function splitAtOffset(f, idx, sepLen){
  var a=document.createDocumentFragment(), b=document.createDocumentFragment(), seen=0, done=false;
  Array.prototype.slice.call(f.childNodes).forEach(function(n){
    var len=n.textContent.length;
    if(done){ b.appendChild(n); return; }
    if(seen+len <= idx){ a.appendChild(n); seen+=len; return; }
    if(n.nodeType===3){
      var cut=idx-seen;
      if(cut>0) a.appendChild(document.createTextNode(n.nodeValue.slice(0,cut)));
      var rest=n.nodeValue.slice(cut+sepLen);
      if(rest) b.appendChild(document.createTextNode(rest));
      done=true; return;
    }
    a.appendChild(n); seen+=len;
  });
  return [a,b];
}

/* ---------- 4. mnemonic lines: "Term – definition" -> aligned rows ---- */
function mnemonics(R){
  (R||document).querySelectorAll('ul.plain').forEach(function(ul){
    var lis=Array.prototype.slice.call(ul.children);
    var hits=lis.filter(function(li){ return /\s[—–]\s/.test(li.textContent); });
    if(hits.length < Math.ceil(lis.length*0.7) || lis.length<2) return;
    var dl=document.createElement('dl'); dl.className='rows';
    if(ul.classList.contains('mnem')) dl.classList.add('mnem');
    lis.forEach(function(li){
      var txt=li.textContent, m=txt.match(/\s[—–]\s/);
      var f=document.createDocumentFragment();
      while(li.firstChild) f.appendChild(li.firstChild);
      if(!m){ var d=document.createElement('dt'); d.appendChild(f); dl.appendChild(d); dl.appendChild(document.createElement('dd')); return; }
      var pr=splitAtOffset(f, txt.indexOf(m[0]), m[0].length);
      var dt=document.createElement('dt'); dt.appendChild(pr[0]);
      var dd=document.createElement('dd'); var sp=document.createElement('span'); sp.className='mask';
      sp.appendChild(pr[1]); dd.appendChild(sp);
      dl.appendChild(dt); dl.appendChild(dd);
    });
    if(ul.id) dl.id=ul.id;
    markShortRows(dl);
    ul.parentNode.replaceChild(dl,ul);
  });
}

/* ---------- 5. study-mode masks on tables and rules ------------------
   Only columns that are demonstrably the answer get masked:
     · first header "Tier"            -> mask column 2 (the intervention)
     · last header names a verdict    -> mask last column
     · explicit data-mask attribute   -> obey it (hand-tagged tables)
   Anything else is left alone rather than guessed at.                  */
var VERDICT=/tell|kills|interpret|next step|treatment|management|action|diagnosis|first test|discriminator|what to do|it selects|consequence|move/i;
var maskSeq=0;
function syncMaskRegions(root){
  /* s92: scoped to one region when given, and writes only what changed */
  var study=document.body.classList.contains('study');
  (root||document).querySelectorAll('.mask[data-disclosure]').forEach(function(mask){
    var btn=mask.querySelector('.mask-toggle'), region=mask.querySelector('.mask-region');
    if(!btn||!region) return;
    var open=!study || mask.dataset.revealed==='1', shown=mask.dataset.revealed==='1';
    if(region.hidden) region.hidden=false;
    var ah=open?'false':'true'; if(region.getAttribute('aria-hidden')!==ah) region.setAttribute('aria-hidden',ah);
    if(region.inert!==!open) region.inert=!open;
    if(mask.classList.contains('shown')!==shown) mask.classList.toggle('shown',shown);
    var ae=open?'true':'false'; if(btn.getAttribute('aria-expanded')!==ae) btn.setAttribute('aria-expanded',ae);
    var tx=open?'Hide answer':'Reveal answer'; if(btn.textContent!==tx) btn.textContent=tx;
  });
}
function makeMaskDisclosure(mask){
  if(mask.dataset.disclosure==='1') return;
  if(mask.closest('.vignette')) return;
  var btn=document.createElement('button'); btn.type='button'; btn.className='mask-toggle';
  btn.setAttribute('aria-expanded','false'); btn.textContent='Reveal answer';
  var region=document.createElement('span'); region.className='mask-region';
  region.id='ax-mask-region-'+(++maskSeq);
  while(mask.firstChild) region.appendChild(mask.firstChild);
  mask.dataset.disclosure='1'; mask.appendChild(btn); mask.appendChild(region);
  btn.setAttribute('aria-controls',region.id);
}
function masks(R){ var D=R||document;
  D.querySelectorAll('table').forEach(function(t){
    var hs=Array.prototype.slice.call(t.querySelectorAll('thead th'));
    if(!hs.length) return;
    var col=null, explicit=t.getAttribute('data-mask');
    if(explicit==='none') return;
    else if(explicit) col=(explicit==='last')?hs.length-1:(parseInt(explicit,10)-1);
    else if(/^tier/i.test(hs[0].textContent.trim())) col=1;
    else if(VERDICT.test(hs[hs.length-1].textContent)) col=hs.length-1;
    if(col===null||col<0||col>=hs.length) return;
    t.querySelectorAll('tbody tr').forEach(function(tr){
      var td=tr.children[col]; if(!td||!norm(td.textContent)) return;
      if(td.querySelector('.mask')) return;
      var sp=document.createElement('span'); sp.className='mask';
      while(td.firstChild) sp.appendChild(td.firstChild);
      td.appendChild(sp);
    });
  });
  D.querySelectorAll('.rule').forEach(function(r){
    var lbl=r.querySelector(':scope > .lbl');
    if(r.querySelector('.mask')) return;
    var sp=document.createElement('span'); sp.className='mask';
    Array.prototype.slice.call(r.childNodes).forEach(function(n){ if(n!==lbl) sp.appendChild(n); });
    r.appendChild(sp);
  });
  D.querySelectorAll('.brief.sp .dp .bl > li, .brief.sp .sp-pause').forEach(function(el){ /* s135: study mode masks the bottom line and the pause point in every spine brief (Jonathan 2026-10-13: "Mask both") */
    if(el.querySelector('.mask')) return;
    var lead=el.classList.contains('sp-pause')?el.querySelector(':scope > b'):null;
    var sp=document.createElement('span'); sp.className='mask';
    Array.prototype.slice.call(el.childNodes).forEach(function(n){ if(n!==lead) sp.appendChild(n); });
    el.appendChild(sp);
  });
  D.querySelectorAll('.mask').forEach(makeMaskDisclosure);
  if(!window.__axMaskClick){
    document.addEventListener('click',function(e){
      if(!document.body.classList.contains('study')) return;
      var mask=e.target.closest?e.target.closest('.mask'):null; if(!mask) return;
      var btn=e.target.closest('.mask-toggle');
      if(!btn && e.target.closest('a,button,input,select,textarea,summary')) return;
      mask.dataset.revealed=mask.dataset.revealed==='1'?'0':'1'; syncMaskRegions(mask.parentNode);
    });
    window.__axMaskClick=true;
  }
  if(!window.__axMaskObserver){
    window.__axMaskObserver=new MutationObserver(function(){
      /* s84: only when study mode itself flips, not on every body class change */
      var s=document.body.classList.contains('study');
      /* s92: the mode carriers (axmApply) now resync each region's masks as it switches */
      if(s===window.__axLastStudy) return; window.__axLastStudy=s;
    });
    window.__axLastStudy=document.body.classList.contains('study');
    window.__axMaskObserver.observe(document.body,{attributes:true,attributeFilter:['class']});
  }
  syncMaskRegions(R);
}

/* ---------- 6. scenario bank -> MCQ ---------------------------------
   Item shape is "stem -> answer" or "stem -> diagnosis -> action".
   Distractors are pulled from the SAME brief: first-column entries of
   its tables, i.e. entities the brief has already discriminated. If two
   usable siblings can't be found, the item stays a reveal-only row
   rather than shipping a fabricated option.                            */
function briefEntities(brief){
  var out=[];
  brief.querySelectorAll('table tbody tr').forEach(function(tr){
    var td=tr.children[0]; if(!td) return;
    var s=norm(td.textContent).replace(/\s*\(.*?\)\s*/g,' ').replace(/\s+/g,' ').trim();
    s=s.replace(/\s*[—–-]\s*.*$/,'');
    if(s.length>2 && s.length<48 && !/^\d/.test(s) && !/^(tier|1|2|3)$/i.test(s)) out.push(s);
  });
  return out;
}
/* S04: display the complete authored label after the same whitespace
   normalization used by the source parser. Clinical qualifiers, punctuation,
   negations, and compound actions remain part of the selectable option. */
function titleCaseKeep(s){ return norm(s); }
function shortLabel(s){ return norm(s); }
/* Question prompt per bank item type (board-brief Rule 13). The type is
   carried on the <li> as data-type. Untyped legacy items get a NEUTRAL
   prompt: many of them are keyed on an action, so a diagnosis default
   would mislabel the question. Type them as they are touched. */
function mcq(R){
  var made=0, kept=0;
  (R||document).querySelectorAll('ol.bank').forEach(function(ol){
    var brief=ol.closest('.brief'); if(!brief) return;
    var pool=briefEntities(brief);
    var wrapAll=document.createElement('div');
    Array.prototype.slice.call(ol.children).forEach(function(li){
      /* split on the fragment, not the string, so <b> emphasis survives */
      var tmp=document.createElement('div');
      while(li.firstChild) tmp.appendChild(li.firstChild);
      var segs=splitTop(tmp,'→');
      if(segs.length<2){ kept++; wrapAll.appendChild(revealFrag(segs)); return; }
      var stemF=segs[0], ansF=segs[1];
      var actF=null;
      if(segs.length>2){
        actF=document.createDocumentFragment();
        for(var s=2;s<segs.length;s++){
          if(s>2) actF.appendChild(document.createTextNode(' → '));
          actF.appendChild(segs[s]);
        }
      }
      var stem=norm(stemF.textContent);
      var answer=norm(ansF.textContent);
      /* Distractors are HAND-AUTHORED only, carried on the <li> as
         data-d1/data-d2. Optional data-label-* values are explicit authored
         display overrides; otherwise the complete source strings are used. */
      var d1=norm(li.getAttribute('data-label-d1')||li.getAttribute('data-d1')||'');
      var d2=norm(li.getAttribute('data-label-d2')||li.getAttribute('data-d2')||'');
      var authoredAnswer=norm(li.getAttribute('data-label-answer')||answer);
      var cands=[];
      if(d1&&d2) cands=[d1,d2];
      /* Only items without an authored pair remain reveal-only. */
      if(cands.length<2){
        kept++; wrapAll.appendChild(revealFrag([stemF,ansF].concat(actF?[actF]:[]))); return;
      }
      var itemId=li.getAttribute('data-item-id')||('legacy-'+brief.id+'-'+made);
      var optionDefs=[
        {id:li.getAttribute('data-key-id')||itemId+'-answer',label:authoredAnswer},
        {id:li.getAttribute('data-d1-id')||itemId+'-d1',label:d1},
        {id:li.getAttribute('data-d2-id')||itemId+'-d2',label:d2}
      ];
      var order=[0,1,2]; shuffle(order);
      var ansIdx=order.indexOf(0);
      var box=document.createElement('div'); box.className='mcq'; box.dataset.a=ansIdx;
      box.dataset.itemId=itemId;
      box.dataset.itemVersion=li.getAttribute('data-item-version')||'';
      box.dataset.itemStatus=li.getAttribute('data-item-status')||'';
      ['data-src','data-nid','data-form','data-nbme','data-xdom','data-xdom-kind'].forEach(function(k){ if(li.hasAttribute(k)) box.setAttribute(k,li.getAttribute(k)); });
      box.dataset.correctOptionId=optionDefs[0].id;
      var top=document.createElement('div'); top.className='top';
      var p=document.createElement('p'); p.className='stem'; p.appendChild(stemF.cloneNode(true));
      var rv=document.createElement('span'); rv.className='rv'; rv.textContent='REVEAL';
      top.appendChild(p); top.appendChild(rv); box.appendChild(top);
      var qt=(li.getAttribute('data-type')||'').toLowerCase();
      var qp=document.createElement('p'); qp.className='qp'; qp.dataset.type=AX.brief.qtype(qt);
      qp.textContent=li.getAttribute('data-lead-in')||AX.brief.prompt(qt); box.appendChild(qp);
      if(li.hasAttribute('data-objective')) box.dataset.objective=li.getAttribute('data-objective');
      var o=document.createElement('div'); o.className='opts';
      /* Option labels render as PLAIN TEXT. The keyed answer carries <b>
         from the source chain while distractors do not, so preserving its
         markup made the bold option the answer every time. Emphasis is
         kept in the stem, the chain and the explanation, where the answer
         is already revealed. */
      order.forEach(function(oi,i){
        var b=document.createElement('button');
        b.innerHTML='<span class="k">'+'ABC'[i]+'</span>';
        b.dataset.optionId=optionDefs[oi].id;
        b.dataset.correct=oi===0?'1':'0';
        b.appendChild(document.createTextNode(optionDefs[oi].label));
        /* s148g: the choice's one-line reason, shown under it once the answer is revealed (Jonathan 2026-10-20) */
        var rsn=norm(li.getAttribute(['data-key-why','data-d1-why','data-d2-why'][oi])||'');
        if(rsn){ var rs=document.createElement('span'); rs.className='qx-rsn'; rs.textContent=rsn; b.appendChild(rs); box.classList.add('qx-hr'); }
        o.appendChild(b);
      });
      box.appendChild(o);
      var why=document.createElement('div'); why.className='why';
      var chain=document.createElement('div'); chain.className='chain';
      chain.appendChild(nodeF(stemF.cloneNode(true),''));
      chain.appendChild(arw());
      chain.appendChild(nodeF(ansF.cloneNode(true),'dx'));
      if(actF){ chain.appendChild(arw()); chain.appendChild(nodeF(actF.cloneNode(true),'act')); }
      why.appendChild(chain);
      box.appendChild(why);
      wrapAll.appendChild(box); made++;
    });
    var h=document.createElement('div'); h.className='mcqwrap';
    while(wrapAll.firstChild) h.appendChild(wrapAll.firstChild);
    var bw=document.createElement('div'); bw.className='bankwrap';
    var tools=document.createElement('div'); tools.className='bktools';
    tools.innerHTML='<button class="bkmode" data-v="stack">Stack</button>'+
                    '<button class="bkmode" data-v="quiz">List</button>'+
                    '<button class="bkmode" data-v="review">Review</button>'+
                    '<button class="bkall">Reveal all</button>';
    var rw=document.createElement('div'); rw.className='reviewwrap';
    Array.prototype.slice.call(h.children).forEach(function(q){
      var row=document.createElement('div'); row.className='rrow';
      var ch=q.querySelector('.why .chain');
      if(ch){ ch=ch.cloneNode(true);
        if(q.dataset.a==='-1'){
          var st=q.querySelector('.stem');
          if(st){ var sn=document.createElement('span'); sn.className='node';
            sn.innerHTML=st.innerHTML;
            if(ch.firstChild){ ch.insertBefore(arw(),ch.firstChild); ch.insertBefore(sn,ch.firstChild); }
            else ch.appendChild(sn);
          }
        }
        row.appendChild(ch);
      }
      rw.appendChild(row);
    });
    bw.appendChild(tools); bw.appendChild(h); bw.appendChild(rw); addFilter(bw);
    var pref='stack';
    try{ var sv=localStorage.getItem('ax-bankview'); if(sv==='review') pref='review'; else if(sv==='list') pref='quiz'; }catch(err){}
    if(pref==='review') bw.classList.add('review');
    if(pref==='stack') bw.classList.add('stack');
    bw.querySelector('.bkmode[data-v="'+pref+'"]').classList.add('on');
    ol.parentNode.replaceChild(bw,ol);
  });
  var T=window.__ax||{made:0,kept:0}; window.__ax={made:T.made+made,kept:T.kept+kept};   /* totals over every build */
}
/* reveal-only fallback, markup preserved */
function revealFrag(segs){
  var d=document.createElement('div'); d.className='mcq'; d.dataset.a='-1';
  var t=document.createElement('div'); t.className='top';
  var p=document.createElement('p'); p.className='stem';
  p.appendChild(segs[0].cloneNode(true));
  t.appendChild(p);
  var rv=document.createElement('span'); rv.className='rv'; rv.textContent='REVEAL';
  t.appendChild(rv); d.appendChild(t);
  var w=document.createElement('div'); w.className='why';
  var chain=document.createElement('div'); chain.className='chain';
  for(var i=1;i<segs.length;i++){
    if(i>1) chain.appendChild(arw());
    chain.appendChild(nodeF(segs[i].cloneNode(true), i===1?'dx':'act'));
  }
  if(segs.length<2) chain.appendChild(nodeF(segs[0].cloneNode(true),''));
  w.appendChild(chain); d.appendChild(w);
  return d;
}
function nodeF(f,c){ var s=document.createElement('span'); s.className='node'+(c?' '+c:''); s.appendChild(f); return s; }
function arw(){ var s=document.createElement('span'); s.className='arw'; s.textContent='→'; return s; }
/* Task-type filter (s76): chips by what a question asks (Diagnosis, Workup, Next step, Mechanism), never by its answer.
   The lead-in already states the task, so a chip reveals nothing. Shown when a bank has 2 or more task groups. */
var TASKGROUP={dx:'dx',stage:'dx',test:'wk',screen:'wk',next:'mx',avoid:'mx',mech:'me',claim:'me'};
var TASKLABEL=[['dx','Diagnosis'],['wk','Workup'],['mx','Next step'],['me','Mechanism']];
function addFilter(bw){
  var qs=Array.prototype.slice.call(bw.querySelectorAll('.mcqwrap > .mcq')), rows=Array.prototype.slice.call(bw.querySelectorAll('.reviewwrap > .rrow'));
  var n={}, tagged=0;
  qs.forEach(function(q,i){ var qp=q.querySelector('.qp'), g=TASKGROUP[qp?qp.dataset.type:'']||'';
    q.dataset.task=g; if(rows[i]) rows[i].dataset.task=g; if(g){ n[g]=(n[g]||0)+1; tagged++; } });
  var groups=TASKLABEL.filter(function(x){ return n[x[0]]; });
  if(groups.length<2) return;
  var f=document.createElement('div'); f.className='bkfilter'; f.setAttribute('role','group'); f.setAttribute('aria-label','Filter questions by task');
  function chip(key,label,count){ var b=document.createElement('button'); b.type='button'; b.dataset.task=key; b.setAttribute('aria-pressed',key==='all'?'true':'false');
    b.appendChild(document.createTextNode(label)); var c=document.createElement('span'); c.textContent=count; b.appendChild(c); f.appendChild(b); }
  chip('all','All',qs.length);
  groups.forEach(function(x){ chip(x[0],x[1],n[x[0]]); });
  f.addEventListener('click',function(e){ var b=e.target.closest('button'); if(!b) return; var k=b.dataset.task;
    Array.prototype.forEach.call(f.querySelectorAll('button'),function(x){ x.setAttribute('aria-pressed',x===b?'true':'false'); });
    qs.concat(rows).forEach(function(el){ el.hidden=!(k==='all'||el.dataset.task===k); });
    var ba=bw.querySelector('.bkall'); if(ba){ var vis=qs.filter(function(q){ return !q.hidden; });
      ba.textContent=vis.length&&vis.every(function(q){ return q.classList.contains('done'); })?'Reset all':'Reveal all'; } });
  var tools=bw.querySelector('.bktools'); tools.parentNode.insertBefore(f,tools.nextSibling);
}
function shuffle(a){ for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var t=a[i];a[i]=a[j];a[j]=t; } }

/* ---------- 7. interaction ---------- */
var whySeq=0;   /* ids stay unique across briefs built at different times */
function accessibilityEnhance(R){
  (R||document).querySelectorAll('.mcq').forEach(function(q){
    var rv=q.querySelector('.rv'), why=q.querySelector('.why');
    if(!why) return;
    if(!why.id) why.id='ax-mcq-why-'+(++whySeq);
    why.hidden=!q.classList.contains('done');
    if(rv){
      if(rv.tagName!=='BUTTON'){ var b=document.createElement('button'); b.type='button'; b.className=rv.className; b.textContent=rv.textContent; rv.parentNode.replaceChild(b,rv); rv=b; }
      rv.setAttribute('aria-controls',why.id); rv.setAttribute('aria-expanded',q.classList.contains('done')?'true':'false');
    }
  });
}

function setMcqReveal(q,show){
  q.classList.toggle('done',show);
  var ans=parseInt(q.dataset.a,10), opts=Array.prototype.slice.call(q.querySelectorAll('.opts button'));
  opts.forEach(function(b,i){ b.classList.remove('right','wrong'); if(show&&ans>=0&&i===ans)b.classList.add('right'); });
  var rv=q.querySelector('.rv'), why=q.querySelector('.why');
  if(why) why.hidden=!show;
  if(rv){ rv.textContent=show?'RESET':'REVEAL'; rv.setAttribute('aria-expanded',show?'true':'false'); }
}
function wire(){
  document.addEventListener('click',function(e){
    var bm=e.target.closest? e.target.closest('.bkmode') : null;
    if(bm){ var bwEl=bm.closest('.bankwrap'), v=bm.dataset.v;
      bwEl.classList.toggle('review',v==='review'); bwEl.classList.toggle('stack',v==='stack');
      Array.prototype.slice.call(bwEl.querySelectorAll('.bkmode')).forEach(function(x){x.classList.toggle('on',x===bm);});
      try{ localStorage.setItem('ax-bankview',v==='quiz'?'list':v); }catch(err){} return;
    }
    var ba=e.target.closest? e.target.closest('.bkall') : null;
    if(ba){ var bw2=ba.closest('.bankwrap'), qs=Array.prototype.slice.call(bw2.querySelectorAll('.mcq')).filter(function(x){ return !x.hidden; });
      var anyOpen=qs.some(function(x){return !x.classList.contains('done');}); qs.forEach(function(x){setMcqReveal(x,anyOpen);});
      ba.textContent=anyOpen?'Reset all':'Reveal all'; return;
    }
    var q=e.target.closest? e.target.closest('.mcq') : null; if(!q) return;
    var rv=e.target.closest('.rv');
    if(rv){ setMcqReveal(q,!q.classList.contains('done')); return; }
    var b=e.target.closest('.opts button'); if(!b||q.classList.contains('done')) return;
    var opts=Array.prototype.slice.call(q.querySelectorAll('.opts button')), i=opts.indexOf(b), ans=parseInt(q.dataset.a,10);
    if(i<0) return; setMcqReveal(q,true); if(ans>=0&&i!==ans)b.classList.add('wrong');
  });
}

/* ---------- run ---------- */
var scalePeekSeq=0, activeScaleButton=null;
function scalepeeks(R){
  (R||document).querySelectorAll('.scaleref').forEach(function(old){
    if(old.tagName==='BUTTON') return;
    var b=document.createElement('button'); b.type='button'; b.className='scaleref';
    b.setAttribute('data-scale',old.getAttribute('data-scale')||''); b.innerHTML=old.innerHTML;
    b.setAttribute('aria-expanded','false');
    var sourceId=old.getAttribute('data-scale'); if(sourceId) b.setAttribute('aria-controls',sourceId);
    old.parentNode.replaceChild(b,old);
  });
  if(R) return;
  document.addEventListener('click',function(e){
    var r=e.target.closest? e.target.closest('.scaleref') : null; if(!r) return;
    var pk=r._peek;
    if(!pk){
      var tgt=document.getElementById(r.getAttribute('data-scale')); if(!tgt) return;
      pk=document.createElement('div'); pk.className='scalepeek'; pk.hidden=true;
      pk.id='ax-scale-peek-'+(++scalePeekSeq); pk.setAttribute('role','region'); pk.setAttribute('aria-label','Scale reference');
      var cl=tgt.cloneNode(true), ids={};
      if(cl.id){ var rootId=cl.id; ids[rootId]=rootId+'-peek-'+scalePeekSeq; cl.id=ids[rootId]; }
      cl.querySelectorAll('[id]').forEach(function(n){ var oldId=n.id; var next=oldId+'-peek-'+scalePeekSeq; ids[oldId]=next; n.id=next; });
      cl.querySelectorAll('[aria-controls]').forEach(function(n){ var target=ids[n.getAttribute('aria-controls')]; if(target) n.setAttribute('aria-controls',target); });
      pk.appendChild(cl);
      var host=r.closest('.crit,.dp,.danger,.pearls,.rule,.vignette,td,li')||r.parentNode;
      host.appendChild(pk); r._peek=pk; r.setAttribute('aria-controls',pk.id); activeScaleButton=r;
    }
    var show=pk.hidden; pk.hidden=!show; r.classList.toggle('open',show); r.setAttribute('aria-expanded',show?'true':'false');
    if(show) activeScaleButton=r;
    else { r.focus({preventScroll:true}); activeScaleButton=null; }
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape' && activeScaleButton){ e.preventDefault(); e.stopImmediatePropagation();
      var r=activeScaleButton, pk=r._peek; if(pk){pk.hidden=true; r.classList.remove('open'); r.setAttribute('aria-expanded','false'); r.focus({preventScroll:true});} activeScaleButton=null;
    }
  });
}
function unavailableInline(R){
  (R||document).querySelectorAll('.mcq').forEach(function(q){
    if(!q.dataset.itemStatus || q.dataset.itemStatus==='ready') return;
    var note=document.createElement('p'); note.className='availability';
    note.textContent='Reference only: source details are missing. This item is excluded from scored practice.';
    q.insertBefore(note,q.firstChild);
    q.querySelectorAll('.opts button').forEach(function(b){ b.disabled=true; });
  });
}
var xrefMap=null;
function xrefs(R){
  var map={};
  if(!xrefMap){ xrefMap={};
    AX.brief.all().forEach(function(b){
      var h=AX.brief.content(b).querySelector('h4'); if(!h||!b.id) return;
      xrefMap[norm(h.textContent).toLowerCase().replace(/[^a-z0-9 ]/g,'')]=b.id;
    });
  }
  map=xrefMap;
  (R||document).querySelectorAll('.pearls').forEach(function(pb){
    if(!/pairs with/i.test(pb.textContent)) return;
    pb.querySelectorAll('b').forEach(function(b){
      if(b.closest('a')) return;
      var k=norm(b.textContent).toLowerCase().replace(/[^a-z0-9 ]/g,'');
      var id=map[k]; if(!id) return;
      var a=document.createElement('a'); a.className='xref'; a.href='#'+id;
      b.parentNode.insertBefore(a,b); a.appendChild(b);
    });
  });
}
var figureSeq=0;
function figures(R){
  (R||document).querySelectorAll('.figure').forEach(function(fig){
    var cap=fig.querySelector(':scope > .figcap'), body=fig.querySelector(':scope > .figbody');
    if(!cap||!body) return;
    if(cap.tagName!=='BUTTON'){
      var button=document.createElement('button'); button.type='button'; button.className=cap.className; button.innerHTML=cap.innerHTML;
      cap.parentNode.replaceChild(button,cap); cap=button;
    }
    if(!body.id) body.id='ax-figure-body-'+(++figureSeq);
    var open=fig.getAttribute('data-open')==='1'; body.hidden=!open; cap.classList.toggle('open',open);
    cap.setAttribute('aria-expanded',open?'true':'false'); cap.setAttribute('aria-controls',body.id);
    var cue=cap.querySelector('.cue'); if(cue) cue.textContent=open?'hide':'show';
    cap.addEventListener('click',function(){
      var show=body.hidden; body.hidden=!show; cap.classList.toggle('open',show); cap.setAttribute('aria-expanded',show?'true':'false');
      if(cue) cue.textContent=show?'hide':'show';
    });
  });
}
function transformBrief(b){ columnize(b); mnemonics(b); tables(b); masks(b); mcq(b); accessibilityEnhance(b); unavailableInline(b); xrefs(b); scalepeeks(b); figures(b); }
  function run(){
  switches(); mobileNav(); sections(); columnize(); mnemonics(); tables(); masks(); mcq(); accessibilityEnhance(); unavailableInline(); xrefs(); scalepeeks(); figures(); wire(); shelfInit();
  AX.brief.each('transform',transformBrief);
  var AFTER=VERIFY?norm(document.body.innerText):"";
  var addedUI=/STUDY MODE|RECALL MODE|FLAT THEME|REVEAL|From this brief|Distractors are entities/;
  var a=BEFORE.split(' ').filter(Boolean).length;
  var b=AFTER.split(' ').filter(Boolean).length;
  console.log('[ax] words before',a,'after',b,'| mcq',window.__ax.made,'reveal-only',window.__ax.kept);
  window.__axCheck={before:a,after:b,get mcq(){ return (window.__ax||{}).made||0; },get reveal(){ return (window.__ax||{}).kept||0; }};
}
window.__axShelf={
  /* Review narrows the page to its fixed set. The sidebar search keeps its
     query and re-lists results inside the set (see 0c). */
  set:function(ids){
    reviewSet=ids||null; closeNav(false); applyShelf(shelf);
  },
  clear:function(){
    reviewSet=null; applyShelf(shelf);
  },
  active:function(){ return !!reviewSet; },
  eligible:function(id){
    var b=document.getElementById(id);
    return !!(b && shelfEligible(b,shelf));
  }
};
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
})();
