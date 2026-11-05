window.NBV={"CODES": {"gen": "General principles and well care", "immune": "Immune", "heme": "Blood and lymphoreticular", "behav": "Behavioral health", "neuro": "Nervous system", "skin": "Skin", "msk": "Musculoskeletal", "cv": "Cardiovascular", "resp": "Respiratory", "gi": "Gastrointestinal", "renal": "Renal and urinary", "newborn": "Newborn and congenital", "preg": "Pregnancy", "repro_f": "Female reproductive", "repro_m": "Male reproductive", "endo": "Endocrine", "multi": "Multisystem (drugs, toxins, infection)", "biostat": "Biostatistics", "social": "Ethics and law"}, "FORMS": {"f6": "Psychiatry CMS Form 6 (inferred)", "pf": "Psychiatry form (name not given)", "pc": "Pediatrics CMS (form not given)", "o": "Other"}, "SHELVES": {"psych": "Psychiatry", "peds": "Pediatrics", "fm": "Family medicine", "im": "Internal medicine", "obgyn": "Obstetrics and gynecology", "surg": "Surgery", "neuro": "Neurology"}, "ITEMS": [{"id": "psych-cms-3a30eb", "q": "SSRI discontinuation", "b": "ssri-effects", "x": "decoy", "xc": ["multi", "preg", "neuro"], "n": "Influenza, pregnancy and migraine offered beside SSRI discontinuation"}, {"id": "psych-cms-fc4577", "q": "Narcolepsy", "b": "peds-sleep", "x": "key", "xc": ["neuro"], "n": "Sleep medicine"}, {"id": "psych-cms-5d383d", "q": "Cholinergic blockade from sleep aids", "b": "tca-tox", "x": "key", "xc": ["multi"], "n": "Pharmacology"}, {"id": "psych-cms-d434f3", "q": "Thiazide raised lithium", "b": "lithium-effects", "x": "key", "xc": ["renal"], "n": "Renal drug interaction"}, {"id": "psych-cms-695a21", "q": "Intubate after failed naloxone", "b": "toxidrome", "x": "key", "xc": ["resp"], "n": "Critical care"}, {"id": "psych-cms-5887c8", "q": "Proxy chose comfort care: food by mouth", "b": "capacity", "x": "key", "xc": ["social"], "n": "Ethics"}, {"id": "psych-cms-c01111", "q": "Valproate pancreatitis", "b": "bipolar-mania", "x": "key", "xc": ["gi"], "n": "Gastrointestinal adverse effect"}, {"id": "psych-cms-24fc10", "q": "Delirium tremens, alcohol unnamed", "b": "substance", "x": "decoy", "xc": ["endo"], "n": "Hypercalcemia offered beside delirium tremens"}, {"id": "psych-cms-6edb85", "q": "Chronic schizophrenia in an older adult", "b": "psychosis-duration", "x": "decoy", "xc": ["multi"], "n": "Psychotic disorder due to a general medical condition offered"}]};
/* s154g view C: "NBME presentations", built at load from the page itself (call 10): framing blocks (div.nbq and
   pp-b[data-nbme]), linked practice items (li or .mcq[data-nbme]), NBME descriptions ([data-nbme-src]) and cross-domain
   tags ([data-xdom]), plus the static table of logged CMS items whose key or decoy crosses a domain. */
(function(){
'use strict';
var D=window.NBV||{}, CODES=D.CODES||{}, SHELVES=D.SHELVES||{}, FORMS=D.FORMS||{}, ITEMS=D.ITEMS||[];
var STEPS={1:'Illness script',2:'Diagnostic criteria',3:'Urgent risks',4:'Differential',5:'Workup',6:'Severity',7:'Treatment',8:'Follow-up'};
var TYPES=[['desc','Descriptions'],['frame','NBME framing'],['linked','Linked items'],['item','Cross-domain items']];
var TL={desc:'Description',frame:'NBME framing',linked:'Linked practice item',item:'Item',xrow:'Cross-domain row'};
var ORDER={desc:0,item:1,xrow:2,frame:3,linked:4};
var st={sh:'all',f:'all',sy:'all',x:'all',xd:'all',t:{desc:1,frame:1,linked:1,item:1}};
var E=null;
function lab(c){return CODES[c]||c;}
function txt(n){return n?(n.textContent||'').replace(/\s+/g,' ').trim():'';}
function el(t,c,s){var e=document.createElement(t); if(c) e.className=c; if(s!=null) e.textContent=s; return e;}
function form(id){return /^psych-cms/.test(id)?'f6':/^psych-form/.test(id)?'pf':/^peds-cms/.test(id)?'pc':'o';}
function clean(n,drop){ // text of n without the given descendants (hover bodies, nested descriptions)
  if(!n) return ''; var c=n.cloneNode(true); c.querySelectorAll(drop).forEach(function(x){x.remove();}); return txt(c);
}
function step(n,b){
  var s=n.closest('[id]'); while(s && s!==b){ var m=/-(s(\d)|dx|mx)$/.exec(s.id); if(m) return {id:s.id,n:m[2]||(m[1]==='dx'?'4':'7')}; s=s.parentElement&&s.parentElement.closest('[id]'); }
  return null;
}
function base(n,t){
  var b=n.closest('.brief'); if(!b) return null;
  var x=n.closest('[data-xdom]'), sp=step(n,b);
  return {t:t,b:b.id,bt:txt(b.querySelector('h4')),sh:(b.getAttribute('data-shelf')||'').split(/\s+/).filter(Boolean),
    sy:(b.getAttribute('data-bp')||'').split(/\s+/).filter(Boolean).slice(0,1),f:'o',
    x:x?x.getAttribute('data-xdom-kind'):null,xc:x?x.getAttribute('data-xdom').split(/\s+/):[],
    href:'#'+(sp?sp.id:b.id),w:sp?('step '+sp.n+' · '+STEPS[sp.n]):'',q:'',m:'',id:''};
}
function collect(){
  var out=[], seen={};
  function add(e){ if(e && e.q){ var k=e.t+'|'+e.b+'|'+e.id+'|'+e.q; if(!seen[k]){ seen[k]=1; out.push(e); } } }
  document.querySelectorAll('.brief [data-nbme-src]').forEach(function(n){
    var e=base(n,'desc'); if(!e) return; e.id=n.getAttribute('data-nbme-src'); e.f=form(e.id);
    if(n.classList.contains('nbd-h')){ var lb=n.querySelector('b'); e.m=txt(lb).replace(/:$/,''); e.q=clean(n,'b'); }
    else { e.q=txt(n.classList.contains('nbd-w')?(n.querySelector('.nbd')||n):n).replace(/^\(|\)$/g,'');
      var k=n.closest('.nbd-w'); k=k&&k.querySelector('.nbd-k'); if(k) e.m=txt(k);
      else { var row=n.closest('tr,.sp-row'), cell=row&&(row.querySelector('.sp-f')||row.querySelector('td'));
        if(cell) e.m=clean(cell,'.nbd-w,.sp-pop-b,.sp-pop,.sp-src'); } }
    add(e);
  });
  document.querySelectorAll('.brief div.nbq[data-nbme], .brief .pp-b[data-nbme]').forEach(function(n){
    var e=base(n,'frame'); if(!e) return; e.id=n.getAttribute('data-nbme'); e.f=form(e.id);
    e.q=txt(n.querySelector('.sl')); e.m=n.classList.contains('pp-b')?clean(n.querySelector('.pp-off'),'.sp-pop,.sp-pop-b'):txt(n.querySelector('.nbask'));
    add(e);
  });
  document.querySelectorAll('.brief li[data-nbme], .brief .mcq[data-nbme]').forEach(function(n){
    if(n.closest('.nbq')) return;
    var e=base(n,'linked'); if(!e) return; e.id=n.getAttribute('data-nbme'); e.f=form(e.id);
    e.q=n.getAttribute('data-lead-in')||txt(n.querySelector('.qp'))||'Practice item';
    var k=/(?:&rarr;|→)\s*<b>([\s\S]*?)<\/b>/.exec(n.innerHTML); if(k){ var d=document.createElement('div'); d.innerHTML=k[1]; e.m='Key: '+txt(d); }
    add(e);
  });
  document.querySelectorAll('.brief tr[data-xdom], .brief .sp-row[data-xdom], .brief li[data-xdom], .brief .mcq[data-xdom]').forEach(function(n){
    if(n.querySelector('[data-nbme-src]')) return;
    var e=base(n,'xrow'); if(!e) return;
    if(n.matches('li,.mcq')){ e.q=n.getAttribute('data-lead-in')||txt(n.querySelector('.qp'))||'Practice item'; e.m='Practice item'; }
    else e.q=clean(n.querySelector('.sp-f')||n.querySelector('td'),'.sp-pop-b,.sp-pop,.nbd-w');
    add(e);
  });
  var bt={}; document.querySelectorAll('.brief[id]').forEach(function(b){ bt[b.id]=b; });
  ITEMS.forEach(function(it){
    var b=it.b&&bt[it.b];
    out.push({t:'item',b:b?it.b:'',bt:b?txt(b.querySelector('h4')):'',sh:['psych'],sy:b?(b.getAttribute('data-bp')||'').split(/\s+/).slice(0,1):['behav'],
      f:form(it.id),x:it.x,xc:it.xc,href:'#'+it.b,w:'',q:it.q,m:it.n,id:it.id});
  });
  return out.sort(function(a,b){
    var sa=a.sh.indexOf('psych')>=0?0:1, sb=b.sh.indexOf('psych')>=0?0:1; if(sa!==sb) return sa-sb;
    var ta=a.bt||'~', tb=b.bt||'~'; if(ta!==tb) return ta<tb?-1:1; return ORDER[a.t]-ORDER[b.t];});
}
function card(e){
  var li=el('li','nbv-e'); li.setAttribute('data-t',e.t); if(e.id) li.setAttribute('data-nbme-ref',e.id);
  var top=el('div','nbv-top'); top.appendChild(el('span','nbv-t',TL[e.t]));
  if(e.x) top.appendChild(el('span','nbv-x '+e.x,(e.x==='key'?'Answer in another domain: ':'Decoy from another domain: ')+e.xc.map(lab).join(', ')));
  li.appendChild(top); li.appendChild(el('p','nbv-q',e.q));
  if(e.m) li.appendChild(el('p','nbv-m',e.m));
  var l=el('p','nbv-l');
  if(e.b){ var a=el('a','',e.bt); a.href=e.href; l.appendChild(a); if(e.w) l.appendChild(el('span','',' · '+e.w)); }
  else l.appendChild(el('span','','No home brief yet'));
  li.appendChild(l); return li;
}
function match(e){
  if(st.sh!=='all' && e.sh.indexOf(st.sh)<0) return false;
  if(st.f!=='all' && e.f!==st.f) return false;
  if(st.sy!=='all' && e.sy.indexOf(st.sy)<0) return false;
  if(st.x==='any' && !e.x) return false;
  if((st.x==='key'||st.x==='decoy') && e.x!==st.x) return false;
  if(st.x!=='all' && st.xd!=='all' && e.xc.indexOf(st.xd)<0) return false;
  return !!st.t[e.t==='xrow'?'item':e.t];
}
function chipRow(box,k,opts,multi){
  box.innerHTML='';
  opts.forEach(function(o){
    var b=el('button','nbv-c',o[1]); b.type='button';
    b.setAttribute('aria-pressed',(multi?!!st.t[o[0]]:st[k]===o[0])?'true':'false');
    b.addEventListener('click',function(){
      if(multi) st.t[o[0]]=st.t[o[0]]?0:1; else { st[k]=o[0]; if(k==='x' && o[0]==='all') st.xd='all'; }
      draw();
    });
    box.appendChild(b);
  });
}
function opts(sel,all,keys,cur){
  sel.innerHTML=''; var o=el('option','',all); o.value='all'; sel.appendChild(o);
  keys.sort(function(a,b){return lab(a)<lab(b)?-1:1;}).forEach(function(c){ var x=el('option','',lab(c)); x.value=c; if(cur===c) x.selected=true; sel.appendChild(x); });
}
function draw(){
  var v=document.getElementById('nbme-view'); if(!v) return;
  if(!E) E=collect();
  var shs={}, fs={}, sys={}, xds={};
  E.forEach(function(e){ e.sh.forEach(function(x){shs[x]=1;}); fs[e.f]=1; e.sy.forEach(function(x){sys[x]=1;}); e.xc.forEach(function(x){xds[x]=1;}); });
  chipRow(v.querySelector('[data-k="sh"]'),'sh',[['all','All']].concat(Object.keys(SHELVES).filter(function(k){return shs[k];}).map(function(k){return [k,SHELVES[k]];})));
  chipRow(v.querySelector('[data-k="f"]'),'f',[['all','All']].concat(Object.keys(FORMS).filter(function(k){return fs[k];}).map(function(k){return [k,FORMS[k]];})));
  var xb=v.querySelector('[data-k="x"]');
  chipRow(xb,'x',[['all','All'],['any','Either kind'],['key','Answer in another domain'],['decoy','Decoy from another domain']]);
  if(st.x!=='all'){
    var wrap=el('div','nbv-sel'), s2=el('select'); s2.setAttribute('aria-label','Domain');
    opts(s2,'Every domain',Object.keys(xds),st.xd); s2.addEventListener('change',function(){st.xd=s2.value; draw();});
    wrap.appendChild(s2); xb.appendChild(wrap);
  }
  var sel=v.querySelector('select[data-k="sy"]'); opts(sel,'Every system',Object.keys(sys),st.sy);
  sel.onchange=function(){st.sy=sel.value; draw();};
  chipRow(v.querySelector('[data-k="t"]'),'t',TYPES,true);
  var list=v.querySelector('.nbv-list'); list.innerHTML='';
  var shown=E.filter(match);
  shown.forEach(function(e){list.appendChild(card(e));});
  if(!shown.length) list.appendChild(el('li','nbv-empty','Nothing logged matches these filters.'));
  v.querySelector('.nbv-n').textContent=shown.length+' of '+E.length+' shown';
}
function boot(){
  var v=document.getElementById('nbme-view'); if(!v) return;
  var d=v.closest('details');
  if(d && !d.open){ d.addEventListener('toggle',function once(){ if(d.open){ d.removeEventListener('toggle',once); draw(); } }); }
  else draw();
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){ setTimeout(boot,0); }); else setTimeout(boot,0);
})();
