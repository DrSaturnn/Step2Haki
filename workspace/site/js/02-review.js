/* ====================== AxBx REVIEW ======================================
   Spaced review over the whole library, with named profiles.

   Storage is localStorage and nothing else — there is no server, so:
     · each browser already has its own store (two people on two laptops are
       separate without doing anything);
     · profiles exist for the cases that isn't enough — a shared machine, or
       one person keeping a Peds track apart from a Step 2 track;
     · a phone is a different computer, which is what the export code is for;
     · clearing site data is deletion, and the export code is the only backup.

   Scheduling is Leitner at the BRIEF level (five boxes, 1/3/7/16/35 days).
   Each review samples three items from a due brief's bank: all three right
   moves it up a box, any miss drops it to box 1. Sampling three of a ten-item
   bank is deliberate — it is the bank, not the item, that has to be known.  */
(function(){
'use strict';

var NS='ax-rev', DAY=864e5;
var BOXES=[0,1,3,7,16,35];      /* index = box number */
var PER_SESSION=3, PER_BRIEF=3;   /* 3 briefs a session */

function today(){ return Math.floor(Date.now()/DAY); }
function store(){ try{ return window.localStorage; }catch(e){ return null; } }
function get(k,d){ var s=store(); if(!s) return d;
  try{ var v=s.getItem(k); return v==null?d:JSON.parse(v); }catch(e){ return d; } }
function set(k,v){ var s=store(); if(!s) return false;
  try{ s.setItem(k,JSON.stringify(v)); return true; }catch(e){ return false; } }
function drop(k){ var s=store(); if(!s) return; try{ s.removeItem(k); }catch(e){} }
function el(t,c,h){ var n=document.createElement(t); if(c) n.className=c;
  if(h!=null) n.innerHTML=h; return n; }
function shuffle(a){ for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1));
  var t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
function esc(s){ return String(s).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

/* ---------- profiles ---------- */
function profiles(){ var p=get(NS+'-profiles',[]); return Array.isArray(p)?p:[]; }
function putProfiles(p){ return set(NS+'-profiles',p); }
function activeId(){ return get(NS+'-active',null); }
/* Who this machine has actually been used by, most recent first. The roster
   may carry fifty names; this is the two or three that belong here. */
function recents(){ var r=get(NS+'-recent',[]); return Array.isArray(r)?r:[]; }
function touchRecent(id){
  if(!id) return;
  var r=recents().filter(function(x){ return x!==id; });
  r.unshift(id); set(NS+'-recent', r.slice(0,6));
}
/* A roster suggestion becomes ours the moment someone here picks it. */
function claim(id){
  var p=profiles(), hit=0;
  p.forEach(function(x){ if(x.id===id && x.remote){ delete x.remote; hit=1; } });
  if(hit) putProfiles(p);
}
function mineOnly(){ return profiles().filter(function(p){ return !p.remote; }); }
function setActive(id){ set(NS+'-active',id); if(id){ claim(id); touchRecent(id); } }
/* '' is the sentinel for "stepped aside on purpose"; a missing key means
   nobody has chosen yet and current() may adopt this machine's last user. */
function signOut(){ set(NS+'-active',''); }
function addProfile(name){
  name=String(name||'').trim().replace(/\s+/g,' ').slice(0,28) || 'Guest';
  var p=profiles(), id='p'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);
  p.push({id:id,name:name,made:today()}); putProfiles(p); setActive(id); return id;
}
function renameProfile(id,name){
  name=String(name||'').trim().slice(0,28); if(!name) return;
  var p=profiles(); p.forEach(function(x){ if(x.id===id) x.name=name; }); putProfiles(p);
}
/* Deliberately returns null rather than conjuring a profile: the library is
   readable without naming yourself, and the panel only asks when you review. */
function current(){
  var id=activeId(), p=profiles();
  if(id && p.some(function(x){ return x.id===id; })) return id;
  if(id==='') return null;          /* signed out deliberately — do not re-adopt */
  /* Deliberately will NOT fall back onto a name that only arrived from the
     shared roster: a fresh device must ask who you are, not guess. */
  var mine=mineOnly(), r=recents(), i;
  for(i=0;i<r.length;i++)
    if(mine.some(function(x){ return x.id===r[i]; })){ set(NS+'-active',r[i]); return r[i]; }
  if(mine.length){ set(NS+'-active',mine[0].id); return mine[0].id; }
  return null;
}
function nameOf(id){ var f=profiles().filter(function(x){ return x.id===id; })[0];
  return f?f.name:'Guest'; }
function initials(n){ n=String(n||'?').trim();
  var parts=n.split(/\s+/); return ((parts[0]||'?')[0]+(parts[1]?parts[1][0]:'')).toUpperCase(); }

function dataOf(id){
  var d=get(NS+'-d-'+id,null);
  if(!d||typeof d!=='object'||Array.isArray(d)) d={v:1,box:{},runs:0,last:null};
  if(!d.box||typeof d.box!=='object') d.box={};
  return d;
}
function putData(id,d){ return set(NS+'-d-'+id,d); }

/* ---------- what is due ----------
   Enumerated from the DOM every time, so briefs added later are picked up
   with no migration, and the active shelf decides the pool. */
function unavailableCount(){
  var n=0;
  document.querySelectorAll('.brief').forEach(function(b){
    if(!window.__axShelf.eligible(b.id)) return;
    if(!AX.brief.isBuilt(b)){ AX.brief.items(b).forEach(function(x){ if(x.status && x.status!=='ready') n++; }); return; }
    b.querySelectorAll('.mcq').forEach(function(m){
      if(m.dataset.itemStatus && m.dataset.itemStatus!=='ready') n++;
    });
  });
  return n;
}
function availabilityText(){
  var n=unavailableCount();
  return n ? n+' question'+(n===1?'':'s')+' on this shelf need source details and are unavailable for scored practice.' : '';
}
function builtItems(b){
  var items=[],totalItems=0;
  Array.prototype.forEach.call(b.querySelectorAll('.mcq'),function(m){
    if(m.dataset.a==='-1') return;
    totalItems++;
    if(!m.dataset.itemStatus || m.dataset.itemStatus==='ready') items.push(m);
  });
  return {items:items,totalItems:totalItems};
}
function pool(){
  var out=[];
  Array.prototype.forEach.call(document.querySelectorAll('.brief'),function(b){
    if(!b.id || !window.__axShelf || !window.__axShelf.eligible(b.id)) return;
    var h=AX.brief.content(b).querySelector('h4'), title=h?h.textContent.trim():b.id;
    if(!AX.brief.isBuilt(b)){
      var st=AX.brief.items(b), ready=st.filter(function(x){ return !x.status || x.status==='ready'; }).length;
      if(!ready) return;
      out.push({id:b.id,title:title,totalItems:st.length,get items(){ AX.brief.ensure(b); return builtItems(b).items; }});
      return;
    }
    var r=builtItems(b);
    if(!r.items.length) return;
    out.push({id:b.id,title:title,items:r.items,totalItems:r.totalItems});
  });
  return out;
}
function split(id){
  var d=dataOf(id), t=today(), fresh=[], due=[], later=[];
  pool().forEach(function(b){
    var r=d.box[b.id];
    if(!r) fresh.push(b);
    else if(r.due<=t) due.push({b:b,over:t-r.due});
    else later.push({b:b,wait:r.due-t});
  });
  due.sort(function(x,y){ return y.over-x.over; });
  later.sort(function(x,y){ return x.wait-y.wait; });
  return {fresh:fresh,due:due,later:later,data:d};
}
/* the sheet shows the briefs a session will review before it starts; buildSession then reviews exactly those */
var PREPICK=null;
function previewPick(id){
  var s=split(id), pick=[], kind=[];
  var due=s.due.map(function(x){ return x.b; }), fresh=shuffle(s.fresh.slice()), later=s.later.map(function(x){ return x.b; });
  while(pick.length<PER_SESSION && due.length)   { pick.push(due.shift()); kind.push('due'); }
  while(pick.length<PER_SESSION && fresh.length) { pick.push(fresh.shift()); kind.push('fresh'); }
  while(pick.length<PER_SESSION && later.length) { pick.push(later.shift()); kind.push('later'); }
  PREPICK={id:id, list:pick};
  return pick.map(function(b,i){ return {id:b.id, title:b.title, kind:kind[i]}; });
}
function buildSession(id){
  var s=split(id), pick=[];
  var due=s.due.map(function(x){ return x.b; });
  var fresh=shuffle(s.fresh.slice());
  var later=s.later.map(function(x){ return x.b; });
  if(PREPICK && PREPICK.id===id){ pick=PREPICK.list.slice(); PREPICK=null; } else {
  while(pick.length<PER_SESSION && due.length)   pick.push(due.shift());
  while(pick.length<PER_SESSION && fresh.length) pick.push(fresh.shift());
  while(pick.length<PER_SESSION && later.length) pick.push(later.shift());   /* studying ahead */
  }
  var q=[];
  pick.forEach(function(b){
    var take=shuffle(b.items.slice()).slice(0,PER_BRIEF);
    b.want=Math.min(PER_BRIEF,b.totalItems); /* quarantine cannot lower the required sample */
    take.forEach(function(m){ q.push({brief:b,mcq:m}); });
  });
  return {briefs:pick,queue:shuffle(q)};   /* interleaved, never blocked by brief */
}

/* ---------- export / import ----------
   AXBX2 is schedule-only and delta-encoded: id:box:daysFromExportDay, with the
   export day carried once in the header so dates rebuild absolutely rather
   than relative to the importing device's clock. The v1 JSON form ran to 9,474
   characters on a fully worked library, which nobody is going to move between
   devices. Lifetime hit counts stay local — nothing reads them, and they are
   what made the old code big.                                              */
function exportCode(id){
  var d=dataOf(id), t=today(), parts=[];
  Object.keys(d.box).forEach(function(k){
    var r=d.box[k];
    if(!r || !(r.b>=1 && r.b<=5)) return;
    parts.push(k+':'+r.b+':'+(r.due-t));
  });
  return 'AXBX2.'+encodeURIComponent(nameOf(id))+'|'+t+'|'+parts.join(',');
}
/* Ids that no longer exist on the page are dropped rather than carried as
   dead weight, so a rename or a retired brief cannot inflate the counts. */
function knownIds(){
  var s={};
  Array.prototype.forEach.call(document.querySelectorAll('.brief'),function(b){
    if(b.id) s[b.id]=1;
  });
  return s;
}
function decodeCode(code){
  code=String(code||'').trim().replace(/\s+/g,'');
  var known=knownIds(), box={}, n=0, nm='Imported', ep=today();
  if(code.indexOf('AXBX2.')===0){
    var body=code.slice(6), a=body.indexOf('|'), b2=body.indexOf('|',a+1);
    if(a<0||b2<0) throw new Error('The code is incomplete – it is missing a section.');
    try{ nm=decodeURIComponent(body.slice(0,a))||'Imported'; }catch(e){ nm='Imported'; }
    ep=parseInt(body.slice(a+1,b2),10);
    if(!isFinite(ep)) throw new Error('The code is damaged.');
    body.slice(b2+1).split(',').forEach(function(s){
      if(!s) return;
      var p=s.split(':');
      if(p.length<3) return;
      var bx=parseInt(p[1],10), dd=parseInt(p[2],10);
      if(!known[p[0]] || !(bx>=1&&bx<=5) || !isFinite(dd)) return;
      box[p[0]]={b:bx,due:ep+dd,ok:0,n:0}; n++;
    });
  } else if(code.indexOf('AXBX1.')===0){          /* the original JSON form */
    var q=JSON.parse(decodeURIComponent(escape(atob(code.slice(6)))));
    if(!q||!q.d||!q.d.box) throw new Error('The code is incomplete.');
    nm=q.n||'Imported';
    Object.keys(q.d.box).forEach(function(k){
      if(!known[k]) return; box[k]=q.d.box[k]; n++;
    });
  } else {
    throw new Error('That is not an AxBx code – it should start with AXBX2.');
  }
  if(!n) throw new Error('No progress in that code matched anything on this page.');
  return {name:nm,box:box,count:n};
}
function uniqueName(want){
  want=String(want||'Imported').trim()||'Imported';
  var name=want, k=2;
  while(profiles().some(function(x){ return x.name.toLowerCase()===name.toLowerCase(); }))
    name=want+' ('+(k++)+')';
  return name;
}
function importCode(code){
  var p=decodeCode(code);
  var id=addProfile(uniqueName(p.name));
  putData(id,{v:1,box:p.box,runs:0,last:today()});
  return id;
}
/* The day a brief was last reviewed is recoverable — due minus its box's
   interval — so two devices can be reconciled per brief on real evidence
   instead of a guess. Whichever side studied a brief more recently wins. */
function mergeBox(targetId, box){
  var mine=dataOf(targetId), added=0, taken=0, kept=0;
  Object.keys(box||{}).forEach(function(k){
    var theirs=box[k], ours=mine.box[k];
    if(!theirs || !(theirs.b>=1&&theirs.b<=5)) return;
    if(!ours){ mine.box[k]={b:theirs.b,due:theirs.due,ok:theirs.ok||0,n:theirs.n||0}; added++; return; }
    var ourDay   = ours.due   - (BOXES[ours.b]  ||0);
    var theirDay = theirs.due - (BOXES[theirs.b]||0);
    /* Same rule as the server (api/progress.js): later review wins, and an
       equally-recent tie goes to the LOWER box. The two must agree exactly or
       a push and a pull would disagree about the same pair of records. */
    if(theirDay>ourDay || (theirDay===ourDay && theirs.b<ours.b)){
      mine.box[k]={b:theirs.b,due:theirs.due,ok:ours.ok||0,n:ours.n||0}; /* local counts survive */
      taken++;
    } else kept++;
  });
  putData(targetId,mine);
  return {added:added,taken:taken,kept:kept};
}
function mergeCode(targetId, code){
  var p=decodeCode(code), r=mergeBox(targetId,p.box);
  r.total=p.count; return r;
}

/* ---------- server sync ----------------------------------------------
   localStorage stays the working copy; the server is only a sync layer.
   Every call is best-effort and time-boxed — if the API is missing, the
   store is down, or you are on a ward with no signal, the page keeps
   working from local storage and simply says so. Nothing here is allowed
   to block or break a review already in progress.                     */
var SYNC={url:'/api/progress', state:'unknown', at:0, note:''};

function api(method, qs, body){
  if(typeof fetch!=='function') return Promise.reject(new Error('no fetch'));
  try{ return apiCall(method,qs,body); }catch(e){ return Promise.reject(e); }
}
function apiCall(method, qs, body){
  var ctl = (typeof AbortController!=='undefined') ? new AbortController() : null;
  var t = setTimeout(function(){ if(ctl) ctl.abort(); }, 6000);
  var opt={method:method, headers:{'Content-Type':'application/json'}};
  if(ctl) opt.signal=ctl.signal;
  if(body) opt.body=JSON.stringify(body);
  return fetch(SYNC.url+(qs||''),opt).then(function(r){
    return r.json().catch(function(){ return {}; }).then(function(j){
      return {status:r.status, body:j};
    });
  }).then(function(res){ clearTimeout(t); return res; },
          function(err){ clearTimeout(t); throw err; });
}
function mark(state,note){ SYNC.state=state; SYNC.note=note||''; SYNC.at=Date.now(); }

/* Names other people have used on this link, so a new device offers them
   instead of making you retype a name exactly. */
function syncRoster(then){
  api('GET','').then(function(r){
    if(r.status!==200 || !r.body || !r.body.names){ mark('off', (r.body&&r.body.error)||''); return; }
    var have={}; profiles().forEach(function(p){ have[p.name.toLowerCase()]=1; });
    var list=profiles(), added=0;
    r.body.names.forEach(function(n){
      if(!n || have[String(n).toLowerCase()]) return;
      list.push({id:'p'+Date.now().toString(36)+Math.random().toString(36).slice(2,6),
                 name:String(n).slice(0,28), made:today(), remote:1});
      added++;
    });
    if(added) putProfiles(list);
    mark('on');
    if(then) then(added);
  }).catch(function(){ mark('off'); if(then) then(0); });
}
function syncPull(id, then){
  if(!id) return then&&then(null);
  api('GET','?name='+encodeURIComponent(nameOf(id))).then(function(r){
    if(r.status!==200 || !r.body){ mark('off',(r.body&&r.body.error)||''); return then&&then(null); }
    if(!r.body.found){
      /* The store does not know this profile. If this device still holds a
         schedule, the store was wiped or rebuilt — say so and offer to put it
         back, rather than reporting "synced" over an empty server. */
      var localCount=Object.keys(dataOf(id).box||{}).length;
      mark(localCount?'restore':'on', localCount?String(localCount):'');
      return then&&then({found:false,localCount:localCount});
    }
    var res=mergeBox(id, r.body.data && r.body.data.box);
    if(r.body.hasPin) setPinKnown(id,true);
    mark('on');
    paintBadge();
    if(then) then(res);
  }).catch(function(){ mark('off'); if(then) then(null); });
}
function syncPush(id, then){
  if(!id) return then&&then(null);
  var d=dataOf(id);
  api('POST','',{name:nameOf(id), pin:pinOf(id)||'', data:{box:d.box, runs:d.runs||0, last:d.last||0}})
    .then(function(r){
      if(r.status===403){ mark('pin', r.body&&r.body.error); return then&&then({needPin:true}); }
      if(r.status===429){ mark('off', r.body&&r.body.error); return then&&then({full:true}); }
      if(r.status!==200){ mark('off',(r.body&&r.body.error)||''); return then&&then(null); }
      /* The server merges on write and returns the result; adopting it is what
         stops this device pushing a stale view again next time. */
      if(r.body && r.body.data) mergeBox(id, r.body.data.box);
      mark('on'); paintBadge(); if(then) then({ok:true});
    }).catch(function(){ mark('off'); if(then) then(null); });
}
function pinOf(id){
  var f=profiles().filter(function(x){ return x.id===id; })[0];
  return f && f.pin ? f.pin : '';
}
function setPin(id,pin){
  var l=profiles(); l.forEach(function(x){ if(x.id===id) x.pin=String(pin||'').slice(0,12); });
  putProfiles(l);
}
function setPinKnown(id,v){
  var l=profiles(); l.forEach(function(x){ if(x.id===id) x.hasPin=!!v; });
  putProfiles(l);
}
function delProfile(id){
  var l=profiles().filter(function(x){ return x.id!==id; });
  putProfiles(l);
  drop(NS+'-d-'+id);
  set(NS+'-recent', recents().filter(function(x){ return x!==id; }));
  /* Let current() decide who is next — it knows which names are ours. Drop
     the key rather than blanking it, or removal would read as a sign-out. */
  if(activeId()===id) drop(NS+'-active');
}
function syncRemove(id, then){
  var nm=nameOf(id), pin=pinOf(id);
  api('DELETE','?name='+encodeURIComponent(nm)+(pin?'&pin='+encodeURIComponent(pin):''))
    .then(function(r){
      if(r.status===403){ mark('pin', r.body&&r.body.error); return then&&then({needPin:true}); }
      if(r.status!==200){ mark('off',(r.body&&r.body.error)||''); return then&&then(null); }
      mark('on'); if(then) then({ok:true});
    }).catch(function(){ mark('off'); if(then) then(null); });
}

function syncLine(){
  if(SYNC.state==='on')  return '<p class="sync ok">Synced across your devices.</p>';
  if(SYNC.state==='pin') return '<p class="sync bad">'+esc(SYNC.note||'This name has a PIN.')+'</p>';
  if(SYNC.state==='restore') return '<p class="sync bad">The sync store has no copy of this '+
      'profile &ndash; this device still holds '+esc(SYNC.note)+'.</p>'+
      '<button class="go alt" data-act="dorestore" type="button">Restore it to sync</button>';
  if(SYNC.state==='off') return '<p class="sync">Saved on this device only'+
      (SYNC.note?' &ndash; '+esc(SYNC.note):' &ndash; sync unreachable')+'.</p>';
  return '';
}

/* ---------- the launcher + panel ---------- */
var anchorEl=null, panel, lastFocus=null, sessionFocus=null;

function dueFor(id){ var s=split(id); return s.due.length+s.fresh.length; }
function paintBadge(){
  var bdg=document.querySelector('#mbar [data-act="review"] .bdg');
  if(bdg){ var id=current(), rd=id?split(id).due.length:0; bdg.textContent=rd; bdg.setAttribute('data-n', rd?'1':'0'); }   /* scheduled reviews only, never the shelf total */
}
/* The panel opens from the Review sheet's "Profile and backup" (14-glance.js), anchored on the toolbar's Review pill, or
   the phone bar's Review button. */
function trigger(){
  var a=document.querySelector('#axbar .axrvb'); if(a && a.offsetParent) return a;
  return document.querySelector('#mbar [data-act="review"]');
}
function panelOpen(){ return panel && !panel.hidden; }
function openPanel(anchor){
  if(!panel) buildPanel();
  lastFocus=anchor||document.activeElement;
  anchorEl=anchor||trigger()||null;
  renderPanel();
  /* Refresh in the background — the panel is usable immediately and
     re-renders only if the server actually had something newer. */
  syncRoster(function(){
    syncPull(current(), function(){ if(panelOpen()) renderPanel(); });
  });
  panel.hidden=false;
  place(anchor);
  var f=panel.querySelector('select,input,button.go,button.mini');
  if(f) try{ f.focus({preventScroll:true}); }catch(e){ f.focus(); }
}
function closePanel(){
  if(!panel||panel.hidden) return;
  panel.hidden=true;
  if(lastFocus) try{ lastFocus.focus({preventScroll:true}); }catch(e){}
  lastFocus=null;
}
function place(anchor){
  anchor = anchor || anchorEl || trigger();
  if(!anchor || !panel) return;
  if(window.matchMedia('(max-width:900px)').matches){ panel.style.top=''; panel.style.left=''; return; }
  var r=anchor.getBoundingClientRect(), z=parseFloat(getComputedStyle(document.documentElement).zoom)||1;   /* zoomed px in, CSS px out */
  var pw=(panel.offsetWidth||330)*z, ph=(panel.offsetHeight||420)*z;
  var vw=document.documentElement.clientWidth||window.innerWidth;
  var vh=window.innerHeight, M=12, left, top;
  if(anchor.closest && anchor.closest('#axbar')){
    /* the toolbar's Review pill: the panel takes the Review sheet's place, its right edge under the pill's */
    left=r.right-pw; top=r.bottom+10;
  } else if(r.width>420){
    /* a wide anchor — the masthead bar — reads as a header: the panel belongs
       under its left edge, not off the end of it. */
    left=r.left; top=r.bottom+10;
    if(top+ph+M>vh){
      /* no room beneath: flip above the bar rather than clamping down over the
         control that was just clicked. */
      var above=r.top-10-ph;
      top = above>=M ? above : Math.max(M, vh-ph-M);
    }
  } else {
    /* a narrow anchor — the sidebar tile — takes the panel alongside, flipping
       to its other side when the window runs out. */
    left=r.right+14; top=r.top;
    if(left+pw+M>vw && r.left-pw-14>=M) left=r.left-pw-14;
  }
  panel.style.left=Math.max(M, Math.min(left, vw-pw-M))/z+'px';
  panel.style.top =Math.max(M, Math.min(top,  vh-ph-M))/z+'px';
}

function buildPanel(){
  panel=el('div'); panel.id='rvpanel'; panel.hidden=true;
  panel.setAttribute('role','dialog');
  panel.setAttribute('aria-modal','false');        /* a popover, not a wall */
  panel.setAttribute('aria-label','Review and profiles');
  document.body.appendChild(panel);

  /* dismissals: click away (the Review pill included: it opens the sheet instead), Escape, the × */
  document.addEventListener('mousedown',function(e){
    if(!panelOpen()) return;
    if(panel.contains(e.target)) return;
    if(e.target.closest && e.target.closest('#mbar')) return;
    closePanel();
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape' && panelOpen()){ e.stopPropagation(); closePanel(); }
  });
  window.addEventListener('resize',function(){ if(panelOpen()) place(); });
}

/* The new-name form, also reachable behind "Someone else". */
function newNameHTML(){
  var h='', rem=profiles().filter(function(p){ return p.remote; });
  if(rem.length){
    h+='<div class="row"><select id="rvpick" aria-label="Existing name">'+
       '<option value="">A name already in use…</option>';
    rem.forEach(function(p){ h+='<option value="'+esc(p.id)+'">'+esc(p.name)+'</option>'; });
    h+='</select><button class="mini" data-act="usepick" type="button">Use</button></div>';
  }
  h+='<div class="row"><input type="text" id="rvnew" placeholder="'+
     (rem.length?'Or a new name or alias':'Your name or alias')+
     '" maxlength="28" autocomplete="off"></div>'+
     '<div class="row"><input type="text" id="rvnewpin" placeholder="PIN (optional)" maxlength="12" inputmode="numeric" autocomplete="off">'+
     '<button class="mini" data-act="add" type="button">Add</button></div>';
  return h;
}
/* Signed out: lead with the people who actually study on this machine. */
function signedOutHTML(){
  var mine=mineOnly(), r=recents(), q=[];
  r.forEach(function(rid){
    var f=mine.filter(function(x){ return x.id===rid; })[0];
    if(f && q.length<4) q.push(f);
  });
  mine.forEach(function(p){
    if(q.length<4 && !q.some(function(x){ return x.id===p.id; })) q.push(p);
  });
  if(!q.length){
    return newNameHTML()+
           '<div class="rvl rows"><button class="row-b" data-act="showimp" type="button">Import a code</button></div>';
  }
  var h='<p class="rvk">Pick up where you left off</p><div class="rvl rows">';
  q.forEach(function(p){
    var d=dueFor(p.id);
    h+='<button class="row-b whob" type="button" data-act="use" data-id="'+esc(p.id)+'">'+
       '<span class="av">'+esc(initials(p.name))+'</span>'+
       '<span class="nm">'+esc(p.name)+'</span>'+
       '<span class="due" data-n="'+(d?'1':'0')+'">'+d+'</span></button>';
  });
  h+='</div><div class="rvl rows">'+
     '<button class="row-b" data-act="other" type="button">Someone else</button>'+
     '<button class="row-b" data-act="showimp" type="button">Import a code</button>'+
     '</div>';
  return h;
}
/* A PIN is not a password, but a name that carries one cannot be written back
   to without it. Ask at claim time rather than letting the first save fail. */
function askPinIfNeeded(id){
  var p=profiles().filter(function(x){ return x.id===id; })[0];
  if(!p || !p.hasPin || p.pin) return;
  var io=panel && panel.querySelector('#rvio'); if(!io) return;
  io.innerHTML='<p class="note" style="margin-top:10px">This name has a PIN. Enter it so '+
    'this device can save back to it.</p>'+
    '<div class="row"><input type="text" id="rvpin" maxlength="12" inputmode="numeric" '+
    'autocomplete="off" placeholder="PIN">'+
    '<button class="mini" data-act="dopin" type="button">Save</button></div>';
  var f=io.querySelector('#rvpin'); if(f) f.focus();
  place();
}

function renderPanel(){
  var id=current(), list=profiles();
  var h;

  if(!id){
    h='<header class="rvh"><div class="who"><b>Who is studying?</b><small>Progress is saved under your name.</small></div>'+
      '<button class="rvx x" type="button" aria-label="Close"></button></header>'+
      signedOutHTML()+
      syncLine();   /* a first-time user must be told if sync is not working */
  } else {
    var s=split(id), t=today();
    var d=s.data, n=s.due.length+s.fresh.length, due=s.due.length;
    var learned=Object.keys(d.box).length;
    var mature=Object.keys(d.box).filter(function(k){ return d.box[k].b>=4; }).length;
    h='<header class="rvh"><span class="av">'+esc(initials(nameOf(id)))+'</span><div class="who"><b>'+esc(nameOf(id))+'</b>'+
      '<small>'+(due ? (due===1 ? '1 review due today' : due+' reviews due today') : 'Nothing due today')+'</small></div>'+
      '<button class="rvx x" type="button" aria-label="Close"></button></header>';
    h+='<p class="rvk">Progress</p><div class="rvl stats">'+
       '<div><b>'+n+'</b><span>Due</span></div>'+
       '<div><b>'+learned+'</b><span>Seen</span></div>'+
       '<div><b>'+mature+'</b><span>Solid</span></div>'+
       '<div><b>'+pool().length+'</b><span>On shelf</span></div>';
    var counts=[0,0,0,0,0];
    Object.keys(d.box).forEach(function(k){ var b=d.box[k].b; if(b>=1&&b<=5) counts[b-1]++; });
    var tot=pool().length||1;
    h+='<div class="boxes" aria-hidden="true">';
    counts.forEach(function(c){ h+='<i><b style="width:'+Math.round(100*c/tot)+'%"></b></i>'; });
    h+='</div></div>';
    h+=syncLine();      /* sync state leads: it is what you need to know first */
    h+='<button class="rvgo go" data-act="start" type="button"'+(n||s.later.length?'':' disabled')+'>'+
       (n? 'Review '+Math.min(PER_SESSION,n)+' briefs' : 'Nothing due, read ahead')+'</button>';
    h+='<button class="rvalt go alt" data-act="quiz" type="button"'+(n||s.later.length?'':' disabled')+'>'+
       'Quiz me, up to '+(PER_SESSION*PER_BRIEF)+' questions</button>';
    if(availabilityText()) h+='<p class="msg availability">'+esc(availabilityText())+'</p>';
    h+='<p class="rvk">Profile</p><div class="rvl rows">'+
       '<button class="row-b" data-act="rename" type="button">Rename</button>'+
       '<button class="row-b" data-act="pin" type="button">'+(pinOf(id)?'Change PIN':'Set PIN')+'</button>'+
       '<button class="row-b" data-act="new" type="button">Add a person</button>'+
       '<button class="row-b warn" data-act="reset" type="button">Start over</button>'+
       '<button class="row-b warn" data-act="remove" type="button">Remove</button>'+
       '</div>';
    /* Backup is no longer how progress travels between devices — sync is. It
       stays because it is the only copy that exists outside the store, so it
       reads as insurance now rather than as transport. */
    h+='<p class="rvk">Backup</p><div class="rvl rows">'+
       '<button class="row-b" data-act="showexp" type="button">Backup code</button>'+
       '<button class="row-b" data-act="showimp" type="button">Restore from a code</button>'+
       '</div>';
  }
  h+='<div id="rvio"></div>';
  h+='<footer class="rvf"><button type="button" data-act="'+(id?'signout':'less')+'">'+(id?'Switch person':'Back')+'</button>'+
     (id?'<button type="button" data-act="less">Fewer options</button>':'')+'</footer>';
  panel.innerHTML=h;
  paintBadge();

  panel.onclick=function(e){
    var b=e.target.closest('button'); if(!b) return;
    var a=b.dataset.act;
    if(b.classList.contains('x')) return closePanel();
    if(a==='use'||a==='usepick'){
      var pid = (a==='use') ? b.dataset.id
              : ((panel.querySelector('#rvpick')||{}).value||'');
      if(!pid) return;
      setActive(pid);
      renderPanel(); place();
      syncPull(pid,function(){
        if(!panelOpen()) return;
        renderPanel(); place();
        askPinIfNeeded(pid);
      });
      return;
    }
    if(a==='other'){
      panel.querySelector('#rvio').innerHTML='<div style="margin-top:10px">'+newNameHTML()+'</div>';
      var f0=panel.querySelector('#rvnew'); if(f0) f0.focus();
      place(); return;
    }
    if(a==='signout'||a==='less'){ closePanel(); AX.emit('review:sheet', a==='signout'?'who':'auto'); return; }
    if(a==='add'){
      var v=panel.querySelector('#rvnew'), vp=panel.querySelector('#rvnewpin');
      var nid2=addProfile(v?v.value:'');
      if(vp && vp.value.trim()) setPin(nid2, vp.value);
      renderPanel(); place();
      syncPull(nid2,function(){ if(panelOpen()){ renderPanel(); place(); } });
      return;
    }
    if(a==='new'||a==='rename'){
      /* inline, not window.prompt(): a native dialog looks wrong against this
         page and is suppressed outright in some embedded contexts. */
      var ren=(a==='rename'), cur0=current();
      panel.querySelector('#rvio').innerHTML=
        '<div class="row" style="margin-top:10px">'+
        '<input type="text" id="rvname" maxlength="28" autocomplete="off" placeholder="Name or alias" value="'+
        (ren?esc(nameOf(cur0)):'')+'">'+
        '<button class="mini" data-act="'+(ren?'dorename':'doadd')+'" type="button">'+(ren?'Save':'Add')+'</button>'+
        '</div>';
      var f=panel.querySelector('#rvname'); f.focus(); f.select(); place(); return;
    }
    if(a==='doadd'){
      addProfile(panel.querySelector('#rvname').value); renderPanel(); place(); return;
    }
    if(a==='dorename'){
      renameProfile(current(), panel.querySelector('#rvname').value); renderPanel(); place(); return;
    }
    if(a==='pin'){
      panel.querySelector('#rvio').innerHTML=
        '<div class="row" style="margin-top:10px">'+
        '<input type="text" id="rvpin" maxlength="12" autocomplete="off" inputmode="numeric" '+
        'placeholder="A few digits" value="'+esc(pinOf(current()))+'">'+
        '<button class="mini" data-act="dopin" type="button">Save</button></div>'+
        '<p class="note" style="margin-top:8px">Not a password. It only stops someone '+
        'typing your name on another device and overwriting your schedule by accident. '+
        'Leave it empty for none.</p>';
      panel.querySelector('#rvpin').focus(); place(); return;
    }
    if(a==='dopin'){
      setPin(current(), panel.querySelector('#rvpin').value);
      syncPush(current(), function(r){
        renderPanel(); place();
        var s=panel.querySelector('#rvio');
        if(s) s.innerHTML = (r&&r.needPin)
          ? '<p class="msg bad">That PIN does not match the one already on this name.</p>'
          : '<p class="msg">Saved.</p>';
      });
      return;
    }
    if(a==='dorestore'){
      syncPush(current(), function(r){
        renderPanel(); place();
        var s5=panel.querySelector('#rvio');
        if(s5) s5.innerHTML = (r&&r.ok)
          ? '<p class="msg">Restored from this device.</p>'
          : '<p class="msg bad">Could not reach sync. Your copy here is untouched.</p>';
      });
      return;
    }
    if(a==='reset'){
      var rid=current(); if(!rid) return;
      var seen=Object.keys(dataOf(rid).box||{}).length;
      panel.querySelector('#rvio').innerHTML=
        '<p class="note" style="margin-top:10px">Clear the schedule for <b>'+esc(nameOf(rid))+
        '</b>? '+(seen? seen+' brief'+(seen===1?'':'s')+' would go back to unseen and everything '
        : 'Everything ')+'becomes due again. The name, the PIN and any other profile stay. '+
        'Copy the code first if you might want this back &ndash; there is no undo.</p>'+
        '<textarea class="code" readonly>'+esc(exportCode(rid))+'</textarea>'+
        '<div class="row" style="margin-top:8px">'+
        '<button class="mini" data-act="doreset" type="button">Start over</button>'+
        '</div><p class="msg" id="rvmsg" hidden></p>';
      place(); return;
    }
    if(a==='doreset'){
      var zid=current(); if(!zid) return;
      putData(zid,{v:1,box:{},runs:0,last:null});
      paintBadge();
      /* The store merges on write and never truncates, so an empty push would
         leave the old schedule sitting there. Drop the record, then re-create
         it empty — which also keeps the name on the roster. */
      syncRemove(zid,function(r1){
        if(r1&&r1.needPin){
          renderPanel(); place();
          var m1=panel.querySelector('#rvio');
          if(m1) m1.innerHTML='<p class="msg bad">Cleared on this device. The store '+
            'kept its copy because this name has a PIN &ndash; set the matching PIN, then start over again.</p>';
          return;
        }
        syncPush(zid,function(){
          renderPanel(); place();
          var m2=panel.querySelector('#rvio');
          if(m2) m2.innerHTML='<p class="msg">Cleared. Everything is due again.</p>'+
            '<p class="note" style="margin-top:6px">If another device still holds the old '+
            'schedule, it will sync back the next time that device opens the page &ndash; '+
            'start over there too.</p>';
        });
      });
      return;
    }
    if(a==='remove'){
      var cur2=current(); if(!cur2) return;
      /* The export code is offered first: removal is the one action here that
         cannot be undone, and a schedule is weeks of work. */
      panel.querySelector('#rvio').innerHTML=
        '<p class="note" style="margin-top:10px">Remove <b>'+esc(nameOf(cur2))+'</b>? '+
        'This clears the profile from this browser. Copy the code first if you '+
        'might want it back &ndash; there is no undo.</p>'+
        '<textarea class="code" readonly>'+esc(exportCode(cur2))+'</textarea>'+
        '<div class="row" style="margin-top:8px">'+
        '<button class="mini" data-act="dorm" type="button">Remove here</button>'+
        '<button class="mini" data-act="dormall" type="button">Remove everywhere</button>'+
        '</div><p class="msg" id="rvmsg" hidden></p>';
      place(); return;
    }
    if(a==='dorm'){
      delProfile(current()); renderPanel(); place();
      var s3=panel.querySelector('#rvio');
      if(s3) s3.innerHTML='<p class="msg">Removed from this device.</p>';
      return;
    }
    if(a==='dormall'){
      var gone=current();
      syncRemove(gone,function(r){
        var mm2=panel.querySelector('#rvmsg');
        if(r&&r.needPin){
          if(mm2){ mm2.hidden=false; mm2.className='msg bad';
                   mm2.textContent='That name has a PIN. Set the matching PIN first, then remove.'; }
          return;
        }
        delProfile(gone); renderPanel(); place();
        var s4=panel.querySelector('#rvio');
        if(s4) s4.innerHTML='<p class="msg">'+(r&&r.ok
          ? 'Removed from this device and from the shared list.'
          : 'Removed here. The shared list could not be reached, so the name may still appear elsewhere.')+'</p>';
      });
      return;
    }
    if(a==='showexp'){
      var code=exportCode(current());
      panel.querySelector('#rvio').innerHTML=
        '<textarea class="code" readonly aria-label="Your backup code">'+esc(code)+'</textarea>'+
        '<p class="msg">Keep this somewhere. Your devices sync on their own, so this '+
        'is not how progress travels &ndash; it is the only copy that exists outside the '+
        'sync store, and the only way back if that store is ever lost.</p>';
      var ta=panel.querySelector('.code'); ta.focus(); ta.select(); place(); return;
    }
    if(a==='showimp'){
      var list2=profiles(), mg='';
      if(list2.length){
        mg='<div class="row" style="margin-top:8px"><select id="rvmto" aria-label="Merge into">';
        list2.forEach(function(x){
          mg+='<option value="'+esc(x.id)+'"'+(x.id===current()?' selected':'')+'>'+esc(x.name)+'</option>';
        });
        mg+='</select><button class="mini" data-act="domerge" type="button">Merge</button></div>';
      }
      panel.querySelector('#rvio').innerHTML=
        '<textarea class="code" id="rvcode" placeholder="Paste an AXBX2… code" aria-label="Paste a code"></textarea>'+
        mg+
        '<div class="row" style="margin-top:8px"><button class="mini" data-act="doimp" type="button">Or import as a new profile</button></div>'+
        '<p class="msg" id="rvmsg" hidden></p>';
      panel.querySelector('#rvcode').focus(); place(); return;
    }
    if(a==='domerge'){
      var mm=panel.querySelector('#rvmsg');
      try{
        var tgt=panel.querySelector('#rvmto').value;
        var r=mergeCode(tgt, panel.querySelector('#rvcode').value);
        setActive(tgt); renderPanel(); place();
        var slot2=panel.querySelector('#rvio');
        if(slot2) slot2.innerHTML='<p class="msg">Merged into “'+esc(nameOf(tgt))+'”. '+
          r.added+' new, '+r.taken+' updated from the other device, '+r.kept+' already newer here.</p>';
      }catch(err2){
        if(mm){ mm.hidden=false; mm.className='msg bad'; mm.textContent=err2.message||'That code could not be read.'; }
      }
      return;
    }
    if(a==='doimp'){
      var m=panel.querySelector('#rvmsg');
      try{
        var nid=importCode(panel.querySelector('#rvcode').value);
        setActive(nid); renderPanel(); place();
        var m2=panel.querySelector('#rvio');
        if(m2) m2.innerHTML='<p class="msg">Imported as “'+esc(nameOf(nid))+'”.</p>';
      }catch(err){
        if(m){ m.hidden=false; m.className='msg bad'; m.textContent=err.message||'That code could not be read.'; }
      }
      return;
    }
    if(a==='start'||a==='quiz'){
      var who=current();
      if(!who){
        var v2=panel.querySelector('#rvnew');
        who=addProfile(v2?v2.value:'Guest');
      }
      closePanel();
      (a==='quiz'?startQuiz:startReview)(who);
      return;
    }
  };
  panel.onchange=function(e){
    if(e.target.id==='rvsel'){
      setActive(e.target.value); renderPanel(); place();
      syncPull(current(), function(){ if(panelOpen()){ renderPanel(); place(); } });
    }
  };
  panel.onkeydown=function(e){
    if(e.key!=='Enter') return;
    if(e.target.id==='rvnew'){
      e.preventDefault(); addProfile(e.target.value); renderPanel(); place();
    } else if(e.target.id==='rvname'){
      e.preventDefault();
      var btn=panel.querySelector('[data-act="doadd"],[data-act="dorename"]');
      if(btn) btn.click();
    }
  };
}

/* ================= REVIEW: five full briefs, in the page =================
   Review is reading, not answering. It narrows the page to the five briefs
   the schedule picked and leaves everything else exactly as authored — the
   criteria tiles still mask, the scale peeks still expand, the figures still
   open, and each brief keeps its own bank with its Review/Quiz chips. Study
   mode is the page's own masking switch, surfaced in the review bar because
   masking and revealing IS the review.
   Nothing is cloned: everything downstream of brief visibility is derived by
   applyShelf, which review hooks rather than reimplements.               */
var rev=null, bar=null;

function startReview(who){
  if(!window.__axShelf){ return startQuiz(who); }      /* transform too old */
  var built=buildSession(who);
  if(!built.briefs.length){
    openPanel(trigger());
    var s0=panel.querySelector('#rvio');
    if(s0) s0.innerHTML='<p class="msg bad">This shelf has no briefs to review.</p>';
    return;
  }
  var set={}; built.briefs.forEach(function(b){ set[b.id]=1; });
  rev={who:who, briefs:built.briefs, marks:{},
       priorStudy:document.body.classList.contains('study')};
  window.__axShelf.set(set);
  document.body.classList.add('reviewing','study');
  AX.settings.set('study','1');
  buildBar(); paintBar();
  built.briefs.forEach(function(b){ addMark(b); });
  window.scrollTo({top:0});
}

function buildBar(){
  if(bar){ bar.hidden=false; return; }
  bar=el('div'); bar.id='rvbar';
  bar.innerHTML=
    '<span class="who"></span>'+
    '<span class="ct"></span>'+
    '<button class="sm" type="button" aria-pressed="true">'+
      '<span class="track"><span class="knob"></span></span>Recall mode</button>'+
    '<button class="fin" type="button">Finish</button>';
  document.body.appendChild(bar);
  bar.querySelector('.sm').addEventListener('click',function(){
    var on=document.body.classList.toggle('study');
    AX.settings.set('study',on?'1':'0');
    paintBar();
  });
  bar.querySelector('.fin').addEventListener('click',function(){ endReview(true); });
}
function paintBar(){
  if(!bar||!rev) return;
  var done=Object.keys(rev.marks).length, n=rev.briefs.length;
  bar.querySelector('.who').textContent=nameOf(rev.who);
  bar.querySelector('.ct').textContent=n+' brief'+(n===1?'':'s')+' \u00b7 '+done+' marked';
  var on=document.body.classList.contains('study');
  var sm=bar.querySelector('.sm');
  sm.classList.toggle('on',on); sm.setAttribute('aria-pressed',on?'true':'false');
  bar.querySelector('.fin').textContent = done ? ('Finish \u2013 '+done+' scored') : 'End review';
}
/* The mark strip sits at the end of the brief it scores, so you rate it where
   you finished reading rather than hunting for a control at the top. */
function addMark(b){
  var node=AX.brief.ensure(b.id); if(!node) return;
  var old=node.querySelector('.rvmark'); if(old) old.parentNode.removeChild(old);
  var m=el('div','rvmark',
    '<span class="q">Did you have this one?</span>'+
    '<button type="button" data-v="ok">Knew it</button>'+
    '<button type="button" data-v="no">Needs work</button>');
  node.appendChild(m);
  m.addEventListener('click',function(e){
    var btn=e.target.closest('button'); if(!btn||!rev) return;
    /* Undo is handled here, in the one delegated listener. Giving the undo
       button its own listener left this one to fire too, which stored "undo"
       as the mark — so an undone brief silently scored as a miss. */
    if(btn.dataset.v==='undo'){ delete rev.marks[b.id]; addMark(b); paintBar(); return; }
    rev.marks[b.id]=btn.dataset.v;
    m.className='rvmark done '+btn.dataset.v;
    m.innerHTML='<span class="q">'+(btn.dataset.v==='ok'
        ? 'Marked known \u2013 it moves up a box.'
        : 'Marked for more work \u2013 back to box 1.')+'</span>'+
      '<button type="button" data-v="undo">Change</button>';
    paintBar();
    var idx=rev.briefs.indexOf(b), nx=rev.briefs[idx+1];
    if(nx){ var el2=AX.brief.ensure(nx.id);
            if(el2) el2.scrollIntoView({behavior:(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)?'auto':'smooth',block:'start'}); }
    else if(bar) bar.querySelector('.fin').focus({preventScroll:true});
  });
}
function endReview(save){
  if(!rev) return;
  var moves=[];
  if(save){
    var d=dataOf(rev.who), t=today();
    rev.briefs.forEach(function(b){
      var mk=rev.marks[b.id];
      if(!mk) return;                       /* unmarked briefs are left alone */
      var prev=d.box[b.id]?d.box[b.id].b:0;
      var nb = (mk==='ok') ? Math.min(5,Math.max(1,prev)+1) : 1;
      var was=d.box[b.id]||{ok:0,n:0};
      d.box[b.id]={b:nb,due:t+BOXES[nb],ok:was.ok||0,n:was.n||0};
      moves.push({title:b.title,to:nb,up:mk==='ok'});
    });
    d.runs=(d.runs||0)+1; d.last=t; putData(rev.who,d);
    syncPush(rev.who);
  }
  document.querySelectorAll('.rvmark').forEach(function(x){ x.parentNode.removeChild(x); });
  if(!rev.priorStudy){
    document.body.classList.remove('study');
    AX.settings.set('study','0');
  }
  document.body.classList.remove('reviewing');
  if(bar) bar.hidden=true;
  window.__axShelf.clear();
  rev=null; paintBadge();
  window.scrollTo({top:0});
  if(save && moves.length){ openPanel(trigger());
    var slot=panel.querySelector('#rvio');
    if(slot) slot.innerHTML='<p class="msg">'+moves.length+' brief'+(moves.length===1?'':'s')+
      ' scored \u2013 '+moves.filter(function(m){return m.up;}).length+' moved up.</p>';
  }
}

/* ---------- the quiz overlay (cold retrieval, no context) ---------- */
var sess=null, box=null;

function startQuiz(who){
  sessionFocus=document.activeElement;
  var built=buildSession(who);
  if(!built.queue.length){
    openPanel(trigger());
    var slot=panel.querySelector('#rvio');
    if(slot) slot.innerHTML='<p class="msg bad">This shelf has no quiz items yet. '+
      'Switch to Step 2 for the pooled view. '+esc(availabilityText())+'</p>';
    return;
  }
  sess={who:who,queue:built.queue,briefs:built.briefs,i:0,result:{},answered:false,seen:[],priorStudy:document.body.classList.contains('study')};
  built.briefs.forEach(function(b){ sess.result[b.id]={ok:0,n:0}; });
  if(!box) buildSessionShell();
  AX.emit('layout:hold', true);
  setStudy(true);   /* briefs opened beside the quiz start in Recall; the switch over the brief turns it off */
  box.hidden=false;
  document.body.classList.add('rvopen');
  renderCard();
}
function setStudy(on){
  document.body.classList.toggle('study',on);
  AX.settings.set('study',on?'1':'0');
  var rc=box && box.querySelector('.rvq-pane .rc'); if(rc) rc.setAttribute('aria-pressed',on?'true':'false');
}
function endSession(save){
  if(save && sess) grade(sess.who,sess.briefs,sess.result);
  if(sess) setStudy(sess.priorStudy);
  sess=null;
  closeSource();
  if(box){
    var c=box.querySelector('.sh .confirm'); if(c) c.parentNode.removeChild(c);
    box.hidden=true;
  }
  document.body.classList.remove('rvopen');
  AX.emit('layout:hold', false);
  paintBadge();
  if(sessionFocus && sessionFocus.isConnected) try{ sessionFocus.focus({preventScroll:true}); }catch(e){}
  sessionFocus=null;
}
function grade(who,briefs,result){
  var d=dataOf(who), t=today(), moves=[];
  briefs.forEach(function(b){
    var r=result[b.id]||{ok:0,n:0};
    var want=b.want||PER_BRIEF;
    if(r.n<want){ moves.push({id:b.id,title:b.title,skipped:true,ok:r.ok,n:r.n,want:want}); return; }
    var prev=d.box[b.id]?d.box[b.id].b:0;
    var clean=(r.ok===r.n);
    var nb=clean ? Math.min(5,Math.max(1,prev)+1) : 1;
    var was=d.box[b.id]||{ok:0,n:0};
    d.box[b.id]={b:nb,due:t+BOXES[nb],ok:(was.ok||0)+r.ok,n:(was.n||0)+r.n};
    moves.push({id:b.id,title:b.title,from:prev,to:nb,ok:r.ok,n:r.n,clean:clean});
  });
  d.runs=(d.runs||0)+1; d.last=t;
  putData(who,d);
  syncPush(who);
  return moves;
}

/* The quiz sits beside the sidebar on the page's own background, in two columns on a wide screen: the question on
   the left, the right column empty until a brief opens there (its source link, a sidebar tile or a link inside the
   brief). The brief's own node moves into the right column and back to its place when the column closes or the quiz
   ends. Narrower screens show one column at a time; the Brief tab switches between them. */
var pane=null, paneBody=null, paneTitle=null, paneHold=null, paneBrief=null;
function briefFor(id){
  var t=id && document.getElementById(id); if(!t) return null;
  if(t.classList.contains('brief')) return {brief:t, at:null};
  var b=t.closest && t.closest('.brief'); return b ? {brief:b, at:t} : null;
}
/* the page's mode carriers (01-transform axm-flat, axm-study) sit on the outermost element without a brief: when a brief
   moves into the column the quiz frame stops being one, and becomes one again when it leaves */
function carry(n, on){ ['flat','study'].forEach(function(m){ n.classList.toggle('axm-'+m, !!on && document.body.classList.contains(m)); }); }
function autoBrief(){ return AX.settings.get('quizbrief')!=='0'; }
function openSource(id, quiet){
  if(AX.brief.ensure(id)===null && !document.getElementById(id)) return false;
  var f=briefFor(id); if(!f) return false;
  if(paneBrief!==f.brief){
    closeSource();
    paneHold=document.createComment('rv-pane'); f.brief.parentNode.insertBefore(paneHold,f.brief);
    paneBrief=f.brief; paneBrief.dataset.rvDisplay=paneBrief.style.display; paneBrief.style.display='';
    carry(box,false); paneBody.appendChild(paneBrief); carry(paneBrief,true);
    var h=paneBrief.querySelector(':scope > h4'); paneTitle.textContent=h?h.textContent.replace(/\s+/g,' ').trim():'';
  }
  box.classList.add('has-brief');
  if(f.at) f.at.scrollIntoView({block:'start'}); else paneBody.scrollTop=0;
  return true;
}
function closeSource(){
  if(paneBrief && paneHold && paneHold.parentNode){
    paneBrief.style.display=paneBrief.dataset.rvDisplay||''; delete paneBrief.dataset.rvDisplay;
    paneHold.parentNode.replaceChild(paneBrief,paneHold);
  }
  paneBrief=null; paneHold=null;
  if(box) carry(box,true);
  if(paneTitle) paneTitle.textContent='';
  if(box) box.classList.remove('has-brief');
}
function wide(){ return window.matchMedia('(min-width:1101px)').matches; }
/* The Brief tab, top right of the quiz, is the one control for the brief. On a wide screen it shows or hides the right
   column (setting quizbrief, on by default): while it is on, a question's brief opens there once the question is
   answered, and a new question starts with the column empty. On a narrower screen it switches between the answered
   question and its brief. */
function paintTab(){
  if(!box) return;
  var on=wide() ? autoBrief() : !!paneBrief;
  box.classList.toggle('pane-on', wide() && autoBrief());
  bt.setAttribute('aria-pressed', on?'true':'false');
  bt.disabled = !wide() && !(sess && sess.answered) && !paneBrief;
}
var bt=null;
function tabClick(){
  if(!sess) return;
  var cur=sess.queue[sess.i].brief.id;
  if(wide()){
    var on=!autoBrief(); AX.settings.set('quizbrief', on?'1':'0');
    if(!on) closeSource(); else if(sess.answered) openSource(cur, true);
  } else if(paneBrief){ closeSource(); }
  else if(sess.answered){ openSource(cur, true); }
  paintTab();
}
function buildSessionShell(){
  box=el('div'); box.id='rvsession'; box.hidden=true;
  box.innerHTML=
    '<button class="bt" type="button" aria-pressed="true" aria-controls="rvq-pane">'+
    '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 3.2c1.9-.8 4-.8 6 .6 2-1.4 4.1-1.4 6-.6v9.4c-1.9-.8-4-.8-6 .6-2-1.4-4.1-1.4-6-.6zM8 3.8v9.4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'+
    '<span>Brief</span></button>'+
    '<div class="rvq"><section class="rvq-main"><div class="sh">'+
    '<span class="who"></span>'+
    '<span class="prog"><b style="width:0%"></b></span>'+
    '<span class="ct"></span>'+
    '<button class="x" type="button" aria-label="End review">✕</button></div>'+
    '<div class="sb"><div class="sw"></div></div></section>'+
    '<section class="rvq-pane" id="rvq-pane" aria-label="Brief"><div class="ph">'+
    '<b class="t"></b>'+
    '<button class="rc" type="button" aria-pressed="true"><span class="track"><span class="knob"></span></span>Recall</button>'+
    '</div>'+
    '<div class="pb"></div></section></div>';
  document.body.appendChild(box);
  pane=box.querySelector('.rvq-pane'); paneBody=pane.querySelector('.pb'); paneTitle=pane.querySelector('.t');
  bt=box.querySelector('.bt');
  bt.addEventListener('click',tabClick);
  pane.querySelector('.rc').addEventListener('click',function(){ setStudy(!document.body.classList.contains('study')); });
  window.matchMedia('(min-width:1101px)').addEventListener('change',function(){ if(sess) paintTab(); });
  /* while the quiz is open, a link to a brief anywhere on the page opens that brief in the right column */
  document.addEventListener('click',function(e){
    if(!sess||!box||box.hidden||e.defaultPrevented||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button) return;
    var a=e.target.closest && e.target.closest('a[href^="#"]'); if(!a) return;
    var id=a.getAttribute('href').slice(1); try{ id=decodeURIComponent(id); }catch(x){}
    if(!id || !(AX.brief.ensure(id)||briefFor(id))) return;
    e.preventDefault(); e.stopPropagation();
    var x=document.body.classList.contains('navopen') && document.querySelector('#nav .navclose'); if(x) x.click();   /* the phone index closes as it does for a page jump */
    if(wide() && !autoBrief()) AX.settings.set('quizbrief','1');   /* a brief asked for by name shows the column */
    openSource(id, true); paintTab();
  },true);
  box.querySelector('.x').addEventListener('click',askEnd);
  document.addEventListener('keydown',function(e){
    if(!sess||!box||box.hidden) return;
    if(e.key==='Escape'){ e.preventDefault(); if(paneBrief && !wide()){ closeSource(); paintTab(); } else askEnd(); return; }
    if(pane && pane.contains(document.activeElement)) return;   /* keys typed while reading the brief stay with the brief */
    if(e.key==='ArrowLeft'){ var pv=box.querySelector('.pv'); if(pv){ e.preventDefault(); pv.click(); } return; }
    if(!sess.answered){
      var k=({'1':0,'2':1,'3':2,'a':0,'b':1,'c':2})[e.key.toLowerCase()];
      if(k!=null){ var bs=box.querySelectorAll('.opts button'); if(bs[k]){ e.preventDefault(); bs[k].click(); } }
    } else if(e.key==='Enter'||e.key===' '){
      var nx=box.querySelector('.nx'); if(nx){ e.preventDefault(); nx.click(); }
    }
  });
}

/* Leaving early is offered inline, in the page's own voice, rather than
   through a native confirm() — and it scores what was actually finished
   instead of throwing the session away. */
function askEnd(){
  if(!sess) return endSession(false);
  var sh=box.querySelector('.sh');
  if(sh.querySelector('.confirm')) return;
  var c=el('span','confirm',
    '<span class="q">End review?</span>'+
    '<button class="yes" type="button">End</button>'+
    '<button class="no" type="button">Keep going</button>');
  sh.appendChild(c);
  c.querySelector('.yes').addEventListener('click',function(){ endSession(true); });
  c.querySelector('.no').addEventListener('click',function(){
    c.parentNode.removeChild(c);
    var f=box.querySelector('.nx')||box.querySelector('.opts button');
    if(f) f.focus({preventScroll:true});
  });
  c.querySelector('.yes').focus({preventScroll:true});
}

function card(entry){
  var src=entry.mcq;
  var originalStem=src.querySelector('.stem');
  var stem=originalStem?originalStem.cloneNode(true):null;
  /* Remove teaching emphasis, retaining notation, images and actual case facts. */
  if(stem) stem.querySelectorAll('b,strong,em,i,mark').forEach(function(n){
    var parent=n.parentNode; while(n.firstChild) parent.insertBefore(n.firstChild,n); parent.removeChild(n);
  });
  var qp=src.querySelector('.qp');
  var btns=Array.prototype.slice.call(src.querySelectorAll('.opts button'));
  var ai=parseInt(src.dataset.a,10);
  var correctId=src.dataset.correctOptionId||'';
  var opts=btns.map(function(b,i){
    var c=b.cloneNode(true), k=c.querySelector('.k'); if(k) k.parentNode.removeChild(k);
    var rz=c.querySelector('.qx-rsn'), rw=rz?rz.textContent.trim():''; if(rz) rz.parentNode.removeChild(rz);
    var optionId=b.dataset.optionId||'';
    return {optionId:optionId,text:c.textContent.trim(),rw:rw,right:correctId?optionId===correctId:i===ai};
  });
  shuffle(opts);                      /* re-shuffled each session, identity stays attached */
  var why=src.querySelector('.why');
  return {itemId:src.dataset.itemId||'',itemVersion:src.dataset.itemVersion||'',
          itemStatus:src.dataset.itemStatus||'',correctOptionId:correctId,
          stem:stem?stem.innerHTML:'', qp:qp?qp.textContent:'',
          opts:opts, why:why?why.innerHTML:''};
}


/* A question seen earlier in the session comes back as it was: the same choice order and, once answered, its marks and
   explanation; an answer is scored once and cannot be changed. */
function renderCard(){
  var e=sess.queue[sess.i], sw=box.querySelector('.sw');
  var seen=sess.seen[sess.i]||(sess.seen[sess.i]={c:card(e),pick:null});
  var c=seen.c;
  sess.answered=seen.pick!==null;
  closeSource(); paintTab();
  box.querySelector('.who').textContent=nameOf(sess.who);
  box.querySelector('.ct').textContent=(sess.i+1)+' / '+sess.queue.length;
  box.querySelector('.prog b').style.width=Math.round(100*sess.i/sess.queue.length)+'%';
  var h=(availabilityText()?'<p class="availability">'+esc(availabilityText())+'</p>':'')+
        '<p class="stem">'+c.stem+'</p>'+
        '<p class="qp">'+esc(c.qp)+'</p><div class="opts">';
  c.opts.forEach(function(o,i){
    h+='<button type="button" data-option-id="'+esc(o.optionId)+'" data-r="'+(o.right?1:0)+'"><span class="k">'+'ABC'[i]+'</span>'+(o.rw?'<span class="qx-ol">'+esc(o.text)+'<span class="qx-rsn">'+esc(o.rw)+'</span></span>':esc(o.text))+'</button>';
  });
  h+='</div><div class="slot"></div><div class="qnav">'+
     (sess.i?'<button class="pv" type="button">Previous</button>':'')+'</div>';
  sw.dataset.itemId=c.itemId;
  sw.dataset.itemVersion=c.itemVersion;
  sw.dataset.itemStatus=c.itemStatus;
  sw.dataset.correctOptionId=c.correctOptionId;
  sw.innerHTML=h;
  box.querySelector('.sb').scrollTop=0;
  var pv=sw.querySelector('.pv'); if(pv) pv.onclick=function(){ sess.i--; renderCard(); };

  function show(b){
    Array.prototype.forEach.call(sw.querySelectorAll('.opts button'),function(x){
      x.disabled=true;
      if(x.dataset.r==='1') x.classList.add('ok');
      else if(x===b) x.classList.add('no');
    });
    var last=sess.i>=sess.queue.length-1;
    sw.querySelector('.slot').innerHTML=
      '<p class="src">'+esc(e.brief.title)+'</p>'+
      '<div class="why">'+c.why+'</div>';
    if(autoBrief() && wide()) openSource(e.brief.id, true);
    paintTab();
    var nx=el('button','nx',last?'Finish':'Next'); nx.type='button';
    sw.querySelector('.qnav').appendChild(nx);
    nx.onclick=function(){
      if(last){ finish(); }
      else { sess.i++; renderCard(); }
    };
    return nx;
  }
  if(sess.answered){
    var was=Array.prototype.filter.call(sw.querySelectorAll('.opts button'),function(x){ return x.dataset.optionId===seen.pick.id && Array.prototype.indexOf.call(x.parentNode.children,x)===seen.pick.i; })[0];
    show(was).focus({preventScroll:true});
    return;
  }
  sw.querySelector('.opts').onclick=function(ev){
    var b=ev.target.closest('button'); if(!b||sess.answered) return;
    sess.answered=true;
    seen.pick={id:b.dataset.optionId, i:Array.prototype.indexOf.call(b.parentNode.children,b)};
    var right=b.dataset.r==='1';
    var r=sess.result[e.brief.id]; r.n++; if(right) r.ok++;
    show(b).focus({preventScroll:true});
  };
  var first=sw.querySelector('.opts button'); if(first) first.focus({preventScroll:true});
}

function finish(){
  var moves=grade(sess.who,sess.briefs,sess.result);
  var tot=0,ok=0;
  Object.keys(sess.result).forEach(function(k){ tot+=sess.result[k].n; ok+=sess.result[k].ok; });
  box.querySelector('.prog b').style.width='100%';
  box.querySelector('.ct').textContent=sess.queue.length+' / '+sess.queue.length;
  var h='<div class="done"><h2>'+ok+' of '+tot+'</h2>'+
        '<p class="sub">A brief moves up only when its required sample is complete and correct. '+
        'A missing source item never lowers that requirement; incomplete samples keep their schedule.</p><table>';
  moves.forEach(function(m){
    h+='<tr><td class="t">'+esc(m.title)+'<br><a class="jump" href="#'+esc(m.id)+'">open the brief</a></td>';
    if(m.skipped){
      h+='<td class="r">'+m.ok+'/'+m.want+'<br><span class="mv sk">not finished</span><br>'+
         '<span style="font-size:10.5px">schedule unchanged; required sample incomplete</span></td></tr>';
      return;
    }
    var when=BOXES[m.to];
    h+='<td class="r">'+m.ok+'/'+m.n+'<br><span class="mv '+(m.clean?'up':'dn')+'">'+
       (m.clean ? 'box '+m.to : (m.from ? 'back to box 1' : 'stays at box 1'))+'</span><br>'+
       '<span style="font-size:10.5px">in '+when+(when===1?' day':' days')+'</span></td></tr>';
  });
  h+='</table><button class="nx" type="button" data-act="close">Done</button></div>';
  var sw=box.querySelector('.sw'); sw.innerHTML=h;
  box.querySelector('.sb').scrollTop=0;
  sw.querySelector('.nx').focus({preventScroll:true});
  sw.querySelector('.nx').onclick=function(){ endSession(false); };
  sess.briefs=[];                 /* already graded; closing must not double-score */
  sess.result={};
}

/* ---------- mount ---------- */
function boot(){
  if(!document.querySelector('.brief')) return;
  buildPanel();
  /* phone: a fourth bar button opens the same panel */
  var bar=document.getElementById('mbar');
  if(bar){
    var b=el('button'); b.type='button'; b.dataset.act='review';
    b.innerHTML='<span>Review<i class="bdg" data-n="0">0</i></span>';
    var top=bar.querySelector('[data-act="top"]');
    bar.insertBefore(b, top||null);
    b.addEventListener('click',function(){ panelOpen()?closePanel():openPanel(b); });
  }
  paintBadge();
  try{ syncRoster(function(){ paintBadge(); }); }catch(e){ mark('off'); }
  /* the status-bar Review sheet drives this scheduler through window.axRv */
  window.axRv={
    current:current, nameOf:nameOf, initials:initials,
    due:function(){ var id=current(); return id?split(id).due.length:0; },   /* scheduled reviews only, never the shelf total */
    pick:function(){ var id=current(); return id?previewPick(id):[]; },
    people:function(){
      var mine=mineOnly(), out=[];
      recents().forEach(function(rid){ var f=mine.filter(function(x){ return x.id===rid; })[0]; if(f) out.push(f); });
      mine.concat(profiles().filter(function(p){ return p.remote; })).forEach(function(p){
        if(out.length<6 && !out.some(function(x){ return x.id===p.id; })) out.push(p); });
      return out.slice(0,6);
    },
    refresh:function(then){ syncRoster(function(){ syncPull(current(), function(){ paintBadge(); if(then) then(); }); }); },
    use:function(pid,then){ setActive(pid); paintBadge(); syncPull(pid,function(){ paintBadge(); if(then) then(); }); },
    needsPin:function(pid){ var p=profiles().filter(function(x){ return x.id===pid; })[0]; return !!(p && p.hasPin && !p.pin); },
    tryPin:function(pid,pin,then){
      setPin(pid,pin);
      syncPush(pid,function(r){
        if(r && r.ok) return then(true);
        setPin(pid,'');
        then(r && r.needPin ? false : null);
      });
    },
    start:function(){ var w=current(); if(w) startReview(w); },
    quiz:function(){ var w=current(); if(w) startQuiz(w); },
    signOut:function(){ signOut(); paintBadge(); },
    add:function(name){ var id=addProfile(name); paintBadge(); return id; },
    open:function(anchor){ openPanel(anchor); }
  };

  /* The shelf changes the pool, so the due count has to follow it. Event-driven,
     never a timer: a poll that outlives the page it serves is a leak, and the
     shelf only ever changes through a click or the hash. */
  document.addEventListener('click',function(e){
    if(e.target.closest && e.target.closest('.shelfpick')) setTimeout(paintBadge,0);
  });
  window.addEventListener('hashchange',function(){ setTimeout(paintBadge,0); });
  /* shelf, Board-style only and review all re-run applyShelf, which announces itself */
  document.addEventListener('ax-shelf',function(){ setTimeout(paintBadge,0); });
  window.addEventListener('storage',function(e){
    if(e.key && e.key.indexOf('ax-')===0) paintBadge();     /* another tab */
  });

  window.__axRev={profiles:profiles,current:current,split:split,pool:pool,
                 startReview:startReview,endReview:endReview,startQuiz:startQuiz,
                 exportCode:exportCode,importCode:importCode,mergeCode:mergeCode,
                 mergeBox:mergeBox,syncRoster:syncRoster,syncPull:syncPull,syncPush:syncPush,
                 SYNC:SYNC,setPin:setPin,pinOf:pinOf,
                 decodeCode:decodeCode,dataOf:dataOf,putData:putData,
                 openPanel:function(){ openPanel(trigger()); },closePanel:closePanel,
                 recents:recents,signOut:signOut,mineOnly:mineOnly,setActive:setActive,
                 BOXES:BOXES};
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
else boot();
})();
