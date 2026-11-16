/* ====================== AxBx NBME ======================================
   Everything here is computed from tags on the page; nothing is typed by hand.
   · section-header counts (topics) from the briefs themselves
   · "NBME xN" chip on a brief = distinct NBME ids linked to its questions
   · blueprint panel: briefs and questions per NBME system for the shelf in view
   Source of weights: repair/nbme/outlines.json (NBME content outlines).        */
(function(){
'use strict';
/* one outline per exam. Rows list the exam's own categories; a brief counts in the row of its first data-bp code, or
   in that exam's "Other systems" row. Sources: nbme.org subject exam content outlines (Pediatrics, Psychiatry, Medicine,
   Surgery, Obstetrics & Gynecology, Clinical Neurology, Family Medicine) and usmle.org Step 2 CK content specifications. */
var OUT={"codes": {"gen": "General Principles, Normal Age-Related Findings, Care of the Well Patient", "immune": "Immune System", "heme": "Blood & Lymphoreticular System", "behav": "Behavioral Health", "neuro": "Nervous System & Special Senses", "skin": "Skin & Subcutaneous Tissue", "msk": "Musculoskeletal System", "cv": "Cardiovascular System", "resp": "Respiratory System", "gi": "Gastrointestinal System", "renal": "Renal & Urinary System", "newborn": "Disorders of the Newborn & Congenital Disorders", "preg": "Pregnancy, Childbirth & the Puerperium", "repro_f": "Female Reproductive System & Breast", "repro_m": "Male Reproductive System", "endo": "Endocrine System", "multi": "Multisystem Processes & Disorders", "biostat": "Biostatistics, Epidemiology/Population Health & Medical Literature", "social": "Social Sciences (ethics, consent, physician-patient relationship)"}};
var CODES=OUT.codes;
function R(codes,lo,hi,label){ return {codes:codes.split(' '),r:[lo,hi],label:label||CODES[codes.split(' ')[0]]}; }
function OTHER(lo,hi){ return {codes:[],r:[lo,hi],label:'Other systems, including multisystem processes',rest:1}; }
var DX='dx test stage', MG='next avoid', ALLMG='next avoid screen';
var BP={
 step2:{name:'USMLE Step 2 CK',share:'USMLE share',
  note:'Step 2 CK groups some systems together. Nutrition (15 to 20%) is coded on top of a system, so it has no row here.',
  rows:[R('social',10,15,'Social sciences: legal and ethical issues, professionalism, systems-based practice and patient safety'),
   R('renal repro_f repro_m',7,13,'Renal and urinary system and reproductive systems'),R('cv',6,12),
   R('msk skin',6,12,'Musculoskeletal system and skin'),R('behav',5,10),R('heme immune',5,10,'Blood, lymphoreticular and immune systems'),
   R('gi',5,10),R('neuro',5,10),R('resp',5,10),R('multi',4,8),R('endo',3,7),R('preg',3,7),R('biostat',3,5),
   R('gen',2,4,'Human development, including normal age-related findings and care of the well patient')],
  tasks:[{label:'Diagnosis',r:[16,20],types:'dx stage'},{label:'Laboratory and diagnostic studies',r:[13,17],types:'test'},
   {label:'Management, pharmacotherapy and clinical interventions (combined)',r:[26,38],types:MG},
   {label:'Health maintenance and disease prevention',r:[5,10],types:'screen'},{label:'Prognosis and outcome',r:[5,9],types:''},
   {label:'Systems-based practice, professionalism and practice-based learning (combined)',r:[13,19],types:''}]},
 fm:{name:'Family Medicine',share:'NBME share',
  rows:[R('gen',5,10),R('immune',1,5),R('heme',1,5),R('behav',5,10),R('neuro',1,5),R('skin',3,7),R('msk',5,10),R('cv',5,10),
   R('resp',5,10),R('gi',5,10),R('renal',1,5),R('preg',1,5),R('repro_f',1,5),R('repro_m',1,5),R('endo',5,10),R('multi',1,5),
   R('biostat',1,5),R('social',5,10)],
  tasks:[{label:'Health maintenance',r:[20,25],types:'screen'},{label:'Diagnosis',r:[40,50],types:DX},
   {label:'Pharmacotherapy, intervention and management',r:[25,30],types:MG}]},
 peds:{name:'Pediatrics',share:'NBME share',
  rows:[R('gen',3,7),R('immune',3,7),R('heme',3,7),R('behav',1,5),R('neuro',5,10),R('skin',1,5),R('msk',3,7),R('cv',5,10),
   R('resp',5,10),R('gi',8,12),R('renal',5,10),R('newborn',5,10),R('repro_f',3,7),R('repro_m',1,5),R('endo',5,10),
   R('multi',10,15),R('social',1,5)],
  tasks:[{label:'Applying foundational science',r:[13,17],types:'mech'},{label:'Diagnosis',r:[55,60],types:DX},
   {label:'Health maintenance, pharmacotherapy, intervention and management',r:[20,25],types:ALLMG}]},
 psych:{name:'Psychiatry',share:'NBME share',
  rows:[R('gen',5,10),R('behav',65,70),R('neuro',10,15),OTHER(5,10),R('social',1,5)],
  tasks:[{label:'Diagnosis, including foundational science',r:[65,70],types:DX+' mech'},
   {label:'Pharmacotherapy, intervention and management',r:[30,35],types:ALLMG}]},
 im:{name:'Medicine',share:'NBME share',
  rows:[R('gen',1,5),R('immune',1,5),R('heme',5,10),R('behav',1,5),R('neuro',1,5),R('skin',1,5),R('msk',1,5),R('cv',10,15),
   R('resp',5,10),R('gi',5,10),R('renal',5,10),R('repro_f',1,5),R('repro_m',1,5),R('endo',5,10),R('multi',10,15),
   R('biostat',1,5),R('social',1,5)],
  tasks:[{label:'Applying foundational science',r:[15,20],types:'mech'},{label:'Diagnosis',r:[45,50],types:DX},
   {label:'Health maintenance, pharmacotherapy, intervention and management',r:[25,30],types:ALLMG}]},
 surg:{name:'Surgery',share:'NBME share',
  rows:[R('immune',1,5),R('heme',5,10),R('neuro',5,10),R('skin',1,5),R('msk',3,7),R('cv',10,15),R('resp',8,12),R('gi',20,25),
   R('renal',3,7),R('repro_f',3,7),R('repro_m',1,5),R('endo',3,7),R('multi',5,10),R('social',1,5)],
  tasks:[{label:'Applying foundational science',r:[8,12],types:'mech'},{label:'Diagnosis',r:[50,60],types:DX},
   {label:'Pharmacotherapy, intervention and management',r:[30,35],types:MG}]},
 obgyn:{name:'Obstetrics and Gynecology',share:'NBME share',
  rows:[R('gen',1,5),R('preg',40,45),R('repro_f',40,45),R('endo',1,5),OTHER(5,10),R('social',1,5)],
  tasks:[{label:'Applying foundational science',r:[8,12],types:'mech'},{label:'Diagnosis',r:[45,50],types:DX},
   {label:'Health maintenance, prevention and surveillance',r:[13,17],types:'screen'},
   {label:'Pharmacotherapy, intervention and management',r:[20,25],types:MG}]},
 neurology:{name:'Clinical Neurology',share:'NBME share',
  rows:[R('gen',1,5),R('behav',3,7),R('neuro',60,65),R('msk',10,15),OTHER(15,20),R('social',1,5)],
  tasks:[{label:'Applying foundational science',r:[10,15],types:'mech'},{label:'Diagnosis',r:[55,60],types:DX},
   {label:'Health maintenance, pharmacotherapy, intervention and management',r:[25,30],types:ALLMG}]}
};
var FORMS={'Pediatrics CMS':'NBME Pediatrics CMS'};
function briefsIn(h3){ var a=[],start=h3.closest('.sectwrap')||h3,el=start.nextElementSibling;
  while(el&&!el.classList.contains('sectwrap')&&!(el.tagName==='H3'&&el.classList.contains('system'))){
    if(el.classList.contains('brief')) a.push(el);
    else el.querySelectorAll('.brief').forEach(function(b){a.push(b);});
    el=el.nextElementSibling; }
  return a; }
function kind(b){ return (b.dataset.src==='aquifer'||b.classList.contains('aq'))?'aq':(b.classList.contains('bs')?'bs':'topic'); }
function headerCounts(){
  document.querySelectorAll('h3.system').forEach(function(h){
    var n=h.querySelector('.n'); if(!n) return;
    var c={topic:0,bs:0,aq:0}; briefsIn(h).forEach(function(b){c[kind(b)]++;});
    if(!c.topic&&!c.bs&&!c.aq) return;
    n.textContent=(c.topic+c.bs+c.aq)+' topics';
  });
}
function nbmeIds(root){ var ids={};
  root.querySelectorAll('[data-nbme]').forEach(function(q){ q.getAttribute('data-nbme').split(/\s+/).forEach(function(i){ if(i) ids[i]=1; }); });
  return Object.keys(ids); }
function kidH4(src){ for(var c=src.firstElementChild;c;c=c.nextElementSibling) if(c.tagName==='H4') return c; return null; }
function chips(){
  AX.brief.all().forEach(function(b){
    var src=AX.brief.content(b), h=kidH4(src); if(!h) return;
    var old=h.querySelector('.nbmechip'); if(old) old.remove();
    /* one NBME badge on the title (CSS h4::after); the count shows only when above 1 */
    var n=nbmeIds(src).length;
    b.classList.toggle('nbme-linked',n>0);
    if(n>1) h.setAttribute('data-nbme-n',String(n)); else h.removeAttribute('data-nbme-n');
  });
  labels(document);
  AX.brief.each('nbme-labels',labels);
}
function labels(root){
  root.querySelectorAll('.mcq[data-src="nbme"], .mcq[data-nbme]').forEach(function(m){
    var w=m.querySelector('.why'); if(!w) return;
    var f=m.getAttribute('data-form'); w.setAttribute('data-nbme-label',(f&&FORMS[f])||'NBME form question');
  });
}
function pct(r){ return r?r[0]+'–'+r[1]+'%':'–'; }
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }
function bpRow(cls,name,cells){
  return '<div class="bpr'+(cls?' '+cls:'')+'" role="row"><span class="bn" role="rowheader">'+name+'</span>'+
    cells.map(function(c){ return '<span class="bc" role="cell" data-l="'+c[0]+'">'+c[1]+'</span>'; }).join('')+'</div>';
}
function bpHead(cols){ return '<div class="bpr bphd" role="row">'+cols.map(function(c,i){ return '<span class="'+(i?'bc':'bn')+'" role="columnheader">'+c+'</span>'; }).join('')+'</div>'; }
/* Coverage matrix: one row per row of the shelf's exam outline, with the exam share, the briefs in the row and how many of
   them the person chosen under Review has reviewed at least once. A marked row has no brief yet or sits below its share. */
var LAST=null;
function matrix(){
  if(!LAST) return '';
  var seen=null; try{ seen=window.axRv?window.axRv.seen():null; }catch(e){}
  var tb=0, ts=0;
  var h='<div class="bpmx" role="table" aria-label="Coverage by system, '+esc(LAST.name)+'"><div class="mx-h" role="row"><span role="columnheader">System</span><span role="columnheader">Exam</span><span role="columnheader">Briefs</span><span role="columnheader">Reviewed</span></div>';
  LAST.rows.forEach(function(r){
    var n=r.briefs.length, k=seen?r.briefs.filter(function(id){ return seen.indexOf(id)>-1; }).length:0; tb+=n; ts+=k;
    h+='<div class="mx-r'+(r.gap?' gap':'')+'" role="row"><span class="mx-n" role="rowheader">'+esc(r.label)+'</span><span role="cell">'+pct(r.range)+'</span><span role="cell">'+n+'</span><span role="cell">'+(seen?k+'/'+n:'–')+'</span><i class="mx-b" aria-hidden="true"><b style="width:'+(seen&&n?Math.round(100*k/n):0)+'%"></b></i></div>';
  });
  h+='<div class="mx-r mx-t" role="row"><span class="mx-n" role="rowheader">All rows</span><span role="cell"></span><span role="cell">'+tb+'</span><span role="cell">'+(seen?ts+'/'+tb:'–')+'</span></div>'+
     '<p class="mx-f">'+(seen?'Reviewed counts the briefs taken through Review at least once.':'Choose who is studying, under Review, to fill the Reviewed column.')+' A marked row has no brief yet or sits below its exam range.</p></div>';
  return h;
}
function repaint(){
  var m=matrix(); if(!m) return;
  document.querySelectorAll('.bpmx').forEach(function(n){ var t=document.createElement('div'); t.innerHTML=m; n.replaceWith(t.firstChild); });
}
function blueprint(){
  var host=document.querySelector('#bpview .bptable'); if(!host) return;
  var shelf=(window.axShelf&&window.axShelf())||'step2';
  var O=BP[shelf]||BP.step2;
  var rows=O.rows.map(function(r){ return {r:r,p:0,s:0,q:0,n:0,ids:[]}; });
  var unl={r:{label:'Not in this outline',r:null},p:0,s:0,q:0,n:0,unl:1,ids:[]};
  function rowFor(code){ for(var i=0;i<rows.length;i++) if(rows[i].r.codes.indexOf(code)>-1) return rows[i];
    for(i=0;i<rows.length;i++) if(rows[i].r.rest) return rows[i]; return unl; }
  var tasks=O.tasks.map(function(t){ return {t:t,q:0}; }), tother={}, total=0;
  document.querySelectorAll('.brief').forEach(function(b){
    if(b.style.display==='none') return;
    var bp=(b.getAttribute('data-bp')||'').split(/\s+/); if(!bp[0]||!CODES[bp[0]]) return;
    var row=rowFor(bp[0]); row.p++; if(b.id) row.ids.push(b.id);
    if(bp[1]&&CODES[bp[1]]){ var r2=rowFor(bp[1]); if(r2!==row) r2.s++; }
    var qs=AX.brief.items(b); row.q+=qs.length; row.n+=nbmeIds(AX.brief.content(b)).length;
    qs.forEach(function(m){ var ty=m.type; total++;
      for(var i=0;i<tasks.length;i++) if(tasks[i].t.types && tasks[i].t.types.split(' ').indexOf(ty)>-1){ tasks[i].q++; return; }
      var k=ty==='mech'?'Foundational science (not a listed task on this exam)':ty==='claim'?'Unassigned (claim)':'Other ('+ty+')';
      tother[k]=(tother[k]||0)+1; });
  });
  function share(q){ return total?Math.round(100*q/total)+'%':'–'; }
  var h='<p class="bpnote bpsrc"><b>'+esc(O.name)+'</b> outline. Exam share is the published range.'+(O.note?' '+esc(O.note):'')+'</p>';
  LAST={name:O.name, rows:rows.concat(unl.p?[unl]:[]).map(function(x){ var sh=total?100*x.q/total:0;
    return {label:x.r.label, range:x.r.r||null, briefs:x.ids.slice(), gap:!x.unl&&(x.p===0||!!(total&&x.r.r&&sh<x.r.r[0]))}; })};
  h+=matrix();
  h+='<div class="bpg bptask" role="table" aria-label="Questions by physician task, '+esc(O.name)+'"><div class="bpcap">Questions by physician task</div>'+
     bpHead(['Task',O.share,'Bank share','Questions']);
  tasks.forEach(function(x){ h+=bpRow(x.t.types?'':'bpna',esc(x.t.label),[[O.share,pct(x.t.r)],['Bank share',x.t.types?share(x.q):'–'],['Questions',x.t.types?x.q:'not tagged']]); });
  Object.keys(tother).forEach(function(k){ h+=bpRow('bpna',esc(k),[[O.share,'–'],['Bank share',share(tother[k])],['Questions',tother[k]]]); });
  h+='</div>';
  host.innerHTML=h;
  AX.emit('blueprint:set');
  AX.emit('blueprint:set');
}
function run(){ AX.blueprint={html:matrix, name:function(){ return LAST?LAST.name:''; }};
  headerCounts(); chips(); blueprint();
  document.addEventListener('ax-shelf',function(){ blueprint(); });
  var q=0; AX.on('review:state',function(){ if(!q) q=setTimeout(function(){ q=0; repaint(); },80); }); }
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
})();
