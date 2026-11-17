/* ====================== AxBx NBME ======================================
   Everything here is computed from tags on the page; nothing is typed by hand.
   · section-header counts (topics) from the briefs themselves
   · "NBME xN" chip on a brief = distinct NBME ids linked to its questions
   · Coverage (drawn on Home): briefs per NBME outline row and questions per physician task for the shelf in view
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
    var c={topic:0,bs:0,aq:0}; briefsIn(h).forEach(function(b){ if(b.style.display!=='none') c[kind(b)]++; });   // the briefs the shelf shows
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
/* Coverage on Home: one card, switched between two tables for the shelf's exam outline.
   By system: one row per outline row, with the exam share, the row's briefs and how many of them the person chosen under
   Review has reviewed (marked as reviewed, or latest review all correct: box 2 or higher). A row with briefs opens in place: counts by state,
   a quiz or a brief review limited to the row, and the row's briefs under the exam outline's subgroups, each subgroup a drop-down with
   its own quiz and review; an outline subgroup with no brief is listed shaded. A brief line carries its state and a Mark as reviewed button with one Undo.
   By task: one row per physician task, with the exam share, the share of the shelf's questions tagged with it and their count.
   A marked row has no brief yet or sits below its exam range. */
var LAST=null, VIEW='sys', OPEN=-1, SUB=-1, UNDO=null, KEEP='';
var CHEV='<svg class="mx-ch" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>';
function review(){ try{ return window.axRv?window.axRv.state():null; }catch(e){ return null; } }
function tally(ids,st){ var c={pass:0,miss:0,fresh:0,due:0,ok:0,n:0};
  ids.forEach(function(id){ var r=st&&st[id]; if(!r){ c.fresh++; return; } if(r.b>=2) c.pass++; else c.miss++; if(r.wait<=0) c.due++; c.ok+=r.ok; c.n+=r.n; });
  return c; }
function when(r){ return r.wait<=0?'due':r.wait+' d'; }
function go(g){ var at=g==null?'':' data-g="'+g+'"';
  return '<div class="mx-go"><button type="button" class="on" data-mx="quiz"'+at+'>Quiz</button><button type="button" data-mx="start"'+at+'>Review briefs</button></div>'; }
function briefs(r,idx,st){
  var list=idx.map(function(i){ var id=r.briefs[i], x=st&&st[id], held=UNDO&&UNDO.id===id;   /* a line just marked keeps its place until the next action */
    return {id:id,i:i,x:x,k:held?(UNDO.was?0:1):!x?1:x.wait<=0?0:2,w:held||!x?0:x.wait}; });
  if(st) list.sort(function(p,q){ return p.k-q.k||p.w-q.w||p.i-q.i; });
  return '<div class="mx-l">'+list.map(function(o){
    var x=o.x, cls=!st?'':!x?' new':x.b>=2?' pass':' miss', undo=UNDO&&UNDO.id===o.id;
    return '<div class="mx-i'+cls+'"><a href="#'+esc(o.id)+'">'+esc(r.titles[o.i])+'</a>'+
      (st?(x&&x.n?'<span class="mx-q">'+x.ok+'/'+x.n+'</span>':'')+'<span class="mx-w">'+(!x?'New':(x.b>=2?'Reviewed':'Missed')+' · '+when(x))+'</span>'+
        (undo?'<button type="button" class="mx-u" data-mx="undo" data-id="'+esc(o.id)+'">Undo</button>':
         (!x||x.b<2||x.wait<=0?'<button type="button" class="mx-u" data-mx="mark" data-id="'+esc(o.id)+'">Mark as reviewed</button>':'')):'')+'</div>'; }).join('')+'</div>';
}
function detail(r,st){
  var c=tally(r.briefs,st), h='';
  if(st){
    h+='<div class="mx-s">'+[['Reviewed',c.pass],['Missed',c.miss],['New',c.fresh],['Due',c.due]].map(function(x){ return '<span><b>'+x[1]+'</b>'+x[0]+'</span>'; }).join('')+'</div>'+
       (c.n?'<p class="mx-a">Answers correct: '+c.ok+' of '+c.n+'</p>':'')+go();
  } else {
    h+='<div class="mx-go"><p>Progress and row quizzes: available after a profile is chosen.</p><button type="button" class="on" data-do="review">Set up</button></div>';
  }
  if(r.groups.filter(function(g){ return g.idx.length; }).length<2&&r.groups.length<2) return h+briefs(r,r.briefs.map(function(_,i){ return i; }),st);
  h+='<div class="mx-gs">';
  var sys='';
  r.groups.forEach(function(g,j){
    if(g.sys!==sys){ sys=g.sys; if(sys) h+='<div class="mx-sh">'+esc(sys)+'</div>'; }
    if(!g.idx.length){ h+='<div class="mx-g none"><span>'+esc(g.label)+'</span><span class="mx-gn">No brief yet</span></div>'; return; }
    var ids=g.idx.map(function(i){ return r.briefs[i]; }), k=tally(ids,st).pass, open=j===SUB;
    h+='<div class="mx-g'+(open?' open':'')+(st&&k===ids.length?' full':'')+'"><button type="button" class="mx-gh" data-mx="sub" data-g="'+j+'" aria-expanded="'+open+'"><span>'+esc(g.label)+'</span><span class="mx-gn">'+(st?k+'/'+ids.length:ids.length)+'</span>'+CHEV+'</button>'+
      (open?(st&&ids.length>1?go(j):'')+briefs(r,g.idx,st):'')+'</div>';
  });
  return h+'</div>';
}
function sysTable(){
  var st=review(), tb=0, tp=0;
  var h='<div class="mx-h" role="row"><span role="columnheader">System</span><span role="columnheader">Exam</span><span role="columnheader">Briefs</span><span role="columnheader">Reviewed</span><span></span></div>';
  LAST.rows.forEach(function(r,i){
    var n=r.briefs.length, c=tally(r.briefs,st), k=c.pass, open=i===OPEN&&n>0; tb+=n; tp+=k;
    h+='<div class="mx-r'+(r.gap?' gap':'')+(st&&n&&k===n?' full':'')+(open?' open':'')+'" role="row"><span class="mx-n" role="rowheader">'+
      (n?'<button type="button" class="mx-o" data-mx="row" data-i="'+i+'" aria-expanded="'+open+'">'+esc(r.label)+'</button>':esc(r.label))+'</span>'+
      '<span role="cell">'+pct(r.range)+'</span><span role="cell">'+n+'</span><span role="cell">'+(st&&n?k+'/'+n:'–')+'</span>'+(n?CHEV:'<span></span>')+
      '<i class="mx-b" aria-hidden="true"><b style="width:'+(st&&n?Math.round(100*k/n):0)+'%"></b><b class="s" style="width:'+(st&&n?Math.round(100*c.miss/n):0)+'%"></b></i></div>';
    if(open) h+='<div class="mx-d" role="row"><div role="cell">'+detail(r,st)+'</div></div>';
  });
  return h+'<div class="mx-r mx-t" role="row"><span class="mx-n" role="rowheader">All rows</span><span role="cell"></span><span role="cell">'+tb+'</span><span role="cell">'+(st?tp+'/'+tb:'–')+'</span><span></span></div></div>'+
    '<p class="mx-f">'+(st?'Reviewed: briefs marked as reviewed, or whose latest review was all correct.':'Reviewed: filled after a profile is chosen under Review.')+' Marked row: no brief yet, or question share below the exam range.'+(LAST.note?' '+esc(LAST.note):'')+'</p>';
}
function taskTable(){
  var h='<div class="mx-h" role="row"><span role="columnheader">Task</span><span role="columnheader">Exam</span><span role="columnheader">Bank</span><span role="columnheader">Questions</span></div>';
  LAST.tasks.forEach(function(t){
    h+='<div class="mx-r mx-k'+(t.gap?' gap':'')+(t.na?' na':'')+'" role="row"><span class="mx-n" role="rowheader">'+esc(t.label)+'</span><span role="cell">'+pct(t.range)+'</span><span role="cell">'+t.share+'</span><span role="cell">'+t.q+'</span></div>';
  });
  return h+'<div class="mx-r mx-t" role="row"><span class="mx-n" role="rowheader">All tasks</span><span role="cell"></span><span role="cell"></span><span role="cell">'+LAST.total+'</span></div></div>'+
    '<p class="mx-f">Bank: share of the shelf’s questions tagged with the task. Marked row: bank share below the exam range.</p>';
}
function matrix(){
  if(!LAST) return '';
  var task=VIEW==='task';
  return '<div class="bpmx'+(task?' tk':'')+'">'+
    '<div class="mx-seg" role="group" aria-label="Coverage by"><button type="button" data-mx="view" data-v="sys" aria-pressed="'+!task+'">By system</button><button type="button" data-mx="view" data-v="task" aria-pressed="'+task+'">By task</button></div>'+
    '<div role="table" aria-label="Coverage by '+(task?'physician task':'system')+', '+esc(LAST.name)+'">'+(task?taskTable():sysTable())+'</div>';
}
function repaint(focus){
  var m=matrix(); if(!m) return;
  document.querySelectorAll('.bpmx').forEach(function(n){ var t=document.createElement('div'); t.innerHTML=m; n.replaceWith(t.firstChild); });
  if(focus){ var f=document.querySelector(focus); if(f) f.focus({preventScroll:true}); }
}
function onClick(e){
  var b=e.target.closest&&e.target.closest('.bpmx [data-mx]'); if(!b||!LAST) return;
  var a=b.getAttribute('data-mx'), r=LAST.rows[OPEN], g=b.getAttribute('data-g'), id=b.getAttribute('data-id'), R=window.axRv;
  if(a==='view'){ VIEW=b.getAttribute('data-v'); repaint('.bpmx .mx-seg [aria-pressed="true"]'); return; }
  if(a==='row'){ var i=+b.getAttribute('data-i'); OPEN=OPEN===i?-1:i; SUB=-1; UNDO=null; repaint('.bpmx .mx-o[data-i="'+i+'"]'); return; }
  if(a==='sub'){ SUB=SUB===+g?-1:+g; repaint('.bpmx .mx-gh[data-g="'+g+'"]'); return; }
  if(!r||!R) return;
  if(a==='mark'){ var m=R.mark(id); if(m){ UNDO={id:id,was:m.was}; repaint(KEEP='.bpmx [data-mx="undo"]'); } return; }
  if(a==='undo'&&UNDO&&UNDO.id===id){ var w=UNDO.was; UNDO=null; R.put(id,w); repaint(KEEP='.bpmx [data-mx="mark"][data-id="'+id+'"]'); return; }
  if(a==='quiz'||a==='start'){ UNDO=null; R[a](g==null?r.briefs.slice():r.groups[+g].idx.map(function(i){ return r.briefs[i]; })); }
}
/* Subgroups of a row. SB.S: the Step 2 outline's headings per system code, in outline order (a third item marks a heading
   that exists only on a shelf's list). SB.L: each shelf's own list, for the systems its outline subdivides (key, and that
   shelf's label when it differs). A brief's data-bps tag names its heading; "a+b" uses b on a shelf whose list has b.
   A heading with no brief is kept, with an empty idx, on Step 2 for every heading of the row's own codes and on a shelf
   only for the headings of that shelf's list; it is drawn shaded, with no button. A row that spans several codes carries
   the system's short name on each group (sys), drawn once as a sub-header. Briefs with no tag sit under Other topics. */
var SB={"S":{"gen":[["child","Infancy and childhood (0 to 12 years)"],["adol","Adolescence (13 to 17 years)"],["adult","Adulthood (18 to 64 years)"],["older","Older adulthood (65 years and older)"]],"behav":[["normal","Normal processes",1],["psychotic","Psychotic disorders"],["anxiety","Anxiety disorders"],["mood","Mood disorders"],["somatic","Somatic symptoms and related disorders"],["factitious","Factitious disorders"],["eating","Eating and impulse-control disorders"],["child","Childhood-onset disorders"],["personality","Personality disorders"],["psychosocial","Psychosocial disorders/behaviors"],["sexual","Sexual disorders and gender dysphoria"],["substance","Substance use disorders"],["drugs","Adverse drug effects",1]],"cv":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["rhythm","Dysrhythmias"],["hf","Heart failure"],["ihd","Ischemic heart disease"],["myo","Myocardial diseases"],["peri","Pericardial diseases"],["valv","Valvular heart disease"],["hypo","Hypotension"],["htn","Hypertension"],["lipid","Dyslipidemia"],["vasc","Vascular disorders"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"msk":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["degen","Degenerative and metabolic disorders"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"newborn":[["nb","Newborn (birth to 4 weeks of age)"],["cong","Congenital disorders"]],"social":[["comm","Communication and interpersonal skills"],["ethics","Medical ethics and jurisprudence"],["sbp","Systems-based practice and patient safety"],["policy","Health care policy and economics"]],"preg":[["prenatal","Prenatal care"],["ob","Obstetric complications"],["labor","Labor and delivery"],["puerp","Puerperium"],["newborn","Newborn (birth to 4 weeks of age)"],["drugs","Adverse drug effects"],["systemic","Systemic disorders affecting pregnancy"]],"repro_m":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["metab","Metabolic and regulatory disorders"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"endo":[["dm","Diabetes mellitus"],["thyroid","Thyroid disorders"],["parathyroid","Parathyroid disorders"],["adrenal","Adrenal disorders"],["pituitary","Pituitary disorders"],["hypothal","Hypothalamic endocrine disorders"],["men","Multiple endocrine neoplasia"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"immune":[["immdef","Immunodeficiency disorders"],["hiv","HIV/AIDS"],["immmed","Immunologically mediated disorders"],["drugs","Adverse drug effects"]],"repro_f":[["breast","Breast"],["female","Infection, immunology and inflammation"],["fneo","Neoplasms"],["fert","Fertility and infertility"],["meno","Menopause"],["menstr","Menstrual and endocrine disorders"],["sexual","Sexual dysfunction"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"skin":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["integ","Hair, nail and gland disorders"],["oral","Oral disease"],["pigment","Pigmentation disorders"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"heme":[["infl","Infection and immunology"],["neo","Neoplasms"],["anemia","Anemia, cytopenias and polycythemia"],["coag","Coagulation disorders"],["trauma","Traumatic, mechanical and vascular disorders"],["drugs","Adverse drug effects"]],"gi":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["signs","Signs, symptoms and ill-defined disorders"],["oral","Oral cavity, salivary gland and esophageal disorders"],["bowel","Stomach, intestinal and anorectal disorders"],["liver","Liver and biliary disorders"],["panc","Pancreatic disorders"],["periton","Peritoneal disorders"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"neuro":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["cva","Cerebrovascular disease"],["spine","Spine, spinal cord and nerve root disorders"],["nerves","Cranial and peripheral nerve disorders"],["pain","Neurologic pain syndromes"],["degen","Degenerative disorders/amnestic syndromes"],["global","Global cerebral dysfunction"],["nm","Neuromuscular disorders"],["move","Movement disorders"],["metab","Metabolic disorders"],["parox","Paroxysmal disorders"],["sleep","Sleep disorders"],["trauma","Traumatic disorders and increased intracranial pressure"],["cong","Congenital disorders"],["drugs","Adverse drug effects"],["eye","Eye and eyelid disorders"],["ear","Ear disorders"]],"renal":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["urine","Abnormalities of urine/urination"],["metab","Metabolic and regulatory disorders"],["vasc","Vascular disorders"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"resp":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms"],["obstr","Obstructive airway disease"],["restr","Pneumoconiosis, fibrosing and restrictive disorders"],["fail","Respiratory failure and pulmonary vascular disorders"],["metab","Metabolic, regulatory and structural disorders"],["pleura","Pleural, mediastinal and chest wall disorders"],["trauma","Traumatic and mechanical disorders"],["cong","Congenital disorders"],["drugs","Adverse drug effects"]],"multi":[["infl","Infection, immunology and inflammation"],["neo","Neoplasms and related disorders"],["signs","Signs, symptoms and ill-defined disorders"],["nutr","Nutrition"],["tox","Toxins and environmental extremes"],["bites","Venomous bites and stings"],["fluid","Fluid, electrolyte and acid-base disorders"],["abuse","Abuse"],["trauma","Multiple trauma"],["shock","Shock"],["genetic","Genetic, metabolic and developmental disorders"],["drugs","Adverse drug effects"]]},"L":{"peds":{"repro_f":[["female","Infection, immunology and inflammation"],["menstr"]]},"fm":{"social":[["comm"],["ethics"],["sbp"]]},"psych":{"behav":[["normal"],["psychotic"],["anxiety"],["mood"],["somatic"],["factitious"],["eating"],["child"],["personality"],["psychosocial"],["substance"],["drugs"]],"social":[["comm"],["ethics"]]}},"N":{"gen":"General","immune":"Immune","heme":"Blood","behav":"Behavioral","neuro":"Nervous","skin":"Skin","msk":"Musculoskeletal","cv":"Cardiovascular","resp":"Respiratory","gi":"Gastrointestinal","renal":"Renal","newborn":"Newborn","preg":"Pregnancy","repro_f":"Female reproductive","repro_m":"Male reproductive","endo":"Endocrine","multi":"Multisystem","biostat":"Biostatistics","social":"Social sciences"}};
function groupsOf(codes,subs,own,shelf){ var seen=[], g=[], used={}, lists=SB.L[shelf]||{};
  codes.forEach(function(c){ if(seen.indexOf(c)<0) seen.push(c); });
  var many=seen.length>1||own.length>1, order=own.filter(function(c){ return SB.S[c]; }).concat(seen.filter(function(c){ return own.indexOf(c)<0; }));
  function has(L,k){ return !!L&&L.some(function(x){ return x[0]===k; }); }
  var key=codes.map(function(c,i){ var t=(subs[i]||'').split('+'); return t[1]&&has(lists[c],t[1])?t[1]:t[0]; });
  order.forEach(function(c){ var L=lists[c]; (SB.S[c]||[]).forEach(function(h){
    var idx=[]; codes.forEach(function(x,i){ if(x===c&&key[i]===h[0]){ idx.push(i); used[i]=1; } });
    var mine=L?L.filter(function(x){ return x[0]===h[0]; })[0]:null, empty=own.indexOf(c)>-1&&(shelf==='step2'?!h[2]:!!mine);
    if(idx.length||empty) g.push({label:(mine&&mine[1])||h[1],sys:many?SB.N[c]:'',idx:idx}); }); });
  var other=codes.map(function(_,i){ return i; }).filter(function(i){ return !used[i]; });
  if(other.length) g.push({label:'Other topics',sys:'',idx:other});
  return g; }
function blueprint(){
  var shelf=(window.axShelf&&window.axShelf())||'step2';
  var O=BP[shelf]||BP.step2;
  var rows=O.rows.map(function(r){ return {r:r,p:0,s:0,q:0,n:0,ids:[],ts:[],cs:[],ss:[]}; });
  var unl={r:{label:'Not in this outline',r:null},p:0,s:0,q:0,n:0,unl:1,ids:[],ts:[],cs:[],ss:[]};
  function rowFor(code){ for(var i=0;i<rows.length;i++) if(rows[i].r.codes.indexOf(code)>-1) return rows[i];
    for(i=0;i<rows.length;i++) if(rows[i].r.rest) return rows[i]; return unl; }
  var tasks=O.tasks.map(function(t){ return {t:t,q:0}; }), tother={}, total=0;
  document.querySelectorAll('.brief').forEach(function(b){
    if(b.style.display==='none') return;
    var bp=(b.getAttribute('data-bp')||'').split(/\s+/); if(!bp[0]||!CODES[bp[0]]) return;
    var row=rowFor(bp[0]); row.p++;
    if(b.id){ var h4=kidH4(AX.brief.content(b)); row.ids.push(b.id); row.ts.push(h4?h4.textContent.replace(/\s+/g,' ').trim():b.id); row.cs.push(bp[0]); row.ss.push(b.getAttribute('data-bps')||''); }
    if(bp[1]&&CODES[bp[1]]){ var r2=rowFor(bp[1]); if(r2!==row) r2.s++; }
    var qs=AX.brief.items(b); row.q+=qs.length; row.n+=nbmeIds(AX.brief.content(b)).length;
    qs.forEach(function(m){ var ty=m.type; total++;
      for(var i=0;i<tasks.length;i++) if(tasks[i].t.types && tasks[i].t.types.split(' ').indexOf(ty)>-1){ tasks[i].q++; return; }
      var k=ty==='mech'?'Foundational science (not a listed task on this exam)':ty==='claim'?'Unassigned (claim)':'Other ('+ty+')';
      tother[k]=(tother[k]||0)+1; });
  });
  function share(q){ return total?Math.round(100*q/total)+'%':'–'; }
  if(!LAST||LAST.shelf!==shelf){ OPEN=-1; SUB=-1; UNDO=null; }
  LAST={shelf:shelf, name:O.name, note:O.note||'', total:total, rows:rows.concat(unl.p?[unl]:[]).map(function(x){ var sh=total?100*x.q/total:0;
    return {label:x.r.label, range:x.r.r||null, briefs:x.ids.slice(), titles:x.ts.slice(), groups:groupsOf(x.cs,x.ss,x.r.codes||[],shelf), gap:!x.unl&&(x.p===0||!!(total&&x.r.r&&sh<x.r.r[0]))}; }),
    tasks:tasks.map(function(x){ var on=!!x.t.types; return {label:x.t.label, range:x.t.r, share:on?share(x.q):'–', q:on?x.q:'not tagged', na:!on, gap:on&&!!total&&100*x.q/total<x.t.r[0]}; })
      .concat(Object.keys(tother).map(function(k){ return {label:k, range:null, share:share(tother[k]), q:tother[k], na:true, gap:false}; }))};
  AX.emit('blueprint:set');
}
function run(){ AX.blueprint={html:matrix, name:function(){ return LAST?LAST.name:''; }};
  headerCounts(); chips(); blueprint();
  document.addEventListener('ax-shelf',function(){ headerCounts(); blueprint(); });
  document.addEventListener('click',onClick);
  var q=0; AX.on('review:state',function(){ if(!q) q=setTimeout(function(){ q=0; repaint(KEEP); KEEP=''; },80); }); }
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
})();
