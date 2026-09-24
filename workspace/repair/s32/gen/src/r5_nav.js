/* ---------- 0b. one sidebar: fixed on desktop, off-canvas on phones ----------
   Desktop keeps the fixed sidebar. Below 980px the same sidebar slides in from
   the left over a dimmed page, opened by the bar's Index button and closed by
   its X, a tap on the backdrop, Escape or choosing a link. Search is pinned at
   the top and the list scrolls beneath it. While open, the panel's height
   follows window.visualViewport, so the search field and its results stay
   above the iOS keyboard. No edge swipe: Safari owns that gesture for Back. */
var NAV_NARROW='(max-width:980px)';
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
  if(sc && act && act.style.display!=='none' && !sxQuery()){
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
  x.setAttribute('aria-label','Close index'); x.innerHTML='<span aria-hidden="true">✕</span>';
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
    '<button type="button" data-act="study" aria-pressed="false"><span>Study</span></button>'+
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
  if(!/[À-ɏ]/.test(l)) return l;
  return l.replace(/[À-ÖØ-öø-ɏ]/g,function(c){
    var d=c.normalize ? c.normalize('NFD').charAt(0) : c; return /[a-z]/.test(d) ? d : c;
  });
}
function sxQNorm(s){ return sxNorm(s).replace(/[^a-z0-9À-ÖØ-öø-ɏͰ-Ͽ]+/g,' ').trim(); }
function sxAl(c){ return (c>=97&&c<=122)||(c>=48&&c<=57)||(c>=65&&c<=90)||(c>=0xc0&&c<=0x24f&&c!==0xd7&&c!==0xf7)||(c>=0x370&&c<=0x3ff); }
function sxQuery(){ var i=document.getElementById('search'); return i ? norm(i.value) : ''; }
function sxNow(){ return (window.performance && performance.now) ? performance.now() : Date.now(); }
function sxEsc(s){ return s.replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

var SX_SKIP=/(^|\s)(lbl|mask-toggle|k|rv|qp|bktools|scalepeek|availability|reviewwrap|rvmark|cue|arw)(\s|$)/;
var SX_MASK=/(^|\s)(mask|why)(\s|$)/;
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
/* One bank item: stem, then the options joined with " · ", then the answer
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
    s=s.split(/\s+[\u2014\u2013]\s+|:/)[0].trim();   /* "Neonatal conjunctivitis — a practical..." -> its name */
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
    pre=pre.slice(Math.max(pre.lastIndexOf(','),pre.lastIndexOf(';'),pre.lastIndexOf(':'),pre.lastIndexOf('.'),pre.lastIndexOf('('),pre.lastIndexOf('·'))+1);
    var w=sxQNorm(pre).split(' ');
    for(var n=1;n<=Math.min(w.length,a.length+2);n++){
      var ph=w.slice(w.length-n).join(' ');
      if(ph.charAt(0)===a.charAt(0) && sxSubseq(a,ph.replace(/ /g,''))){ if(ph!==a) sxGroup([a,ph]); break; }
    }
  }
}
function sxBuildOne(b,di){
  if(!b.id) return;
  var h=b.querySelector(':scope > h4');
  var rec={b:b,id:b.id,di:di,title:h ? norm(h.textContent) : b.id,sub:'',blocks:[],all:''};
  var add=function(k){
    var parts=[], vis=[]; sxWalk(k,function(t,n,m){ parts.push(t); if(!m) vis.push(t); });
    k.raw=parts.join('').replace(/\s+/g,' ').trim();
    if(k.bank>-1) k.stemEnd=vis.join('').replace(/\s+/g,' ').trim().length;   /* the answer chain comes last */
    if(k.raw) rec.blocks.push(k);
  };
  for(var c=b.firstElementChild;c;c=c.nextElementSibling){
    if(c.classList.contains('bankwrap')){
      Array.prototype.forEach.call(c.querySelectorAll('.mcqwrap > .mcq'),function(m,i){
        var k=sxBlk(m,'Question',3); k.bank=i; add(k);
      });
      continue;
    }
    if(c.classList.contains('rvmark')) continue;
    var L=sxLabel(c); if(!L) continue;
    var k=sxBlk(c,L[0],L[1]); add(k);
    if(L[1]===1 && !rec.sub) rec.sub=k.raw;
  }
  var parts=[];
  rec.blocks.forEach(function(k){ k.n=sxNorm(k.raw); parts.push(k.n); sxPairs(k.raw); });
  rec.all=parts.join('\n');
  SX.briefs.push(rec);
}
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
  var loc=sxLocate(k,first), masked=!!(loc && loc.masked), inAnswer=false;
  /* A bank item's answer stays hidden until the reader answers it, in any
     mode, so a hit there shows the stem instead of spoiling the key. */
  if(masked && k.bank>-1){ first=0; masked=false; inAnswer=true; }
  var raw=k.raw, L=raw.length, a=Math.max(0,first-42), b;
  if(a>0){ var sp=raw.indexOf(' ',a); a=(sp>-1 && sp<first) ? sp+1 : a; }
  b=Math.min(L,a+150);
  if(b<L){ var sp2=raw.lastIndexOf(' ',b); if(sp2>first) b=sp2; }
  if(k.bank>-1 && k.stemEnd && first<k.stemEnd) b=Math.min(b,k.stemEnd);   /* never run on into the answer chain */
  return {answer:inAnswer, html:(a>0?'…':'')+sxHl(raw,k.n,a,b,terms)+(b<L?'…':''), masked:masked};
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
  requestAnimationFrame(function(){
    var rc=tgt.getBoundingClientRect(), vh=window.innerHeight||document.documentElement.clientHeight;
    var y=(window.pageYOffset||0)+rc.top-(rc.height<vh*0.6 ? (vh-rc.height)/2 : 76);
    try{ window.scrollTo({top:Math.max(0,y),behavior:reduce?'auto':'smooth'}); }catch(e){ window.scrollTo(0,Math.max(0,y)); }
    el.classList.remove('sxflash'); void el.offsetWidth; el.classList.add('sxflash');
    clearTimeout(el._sxT); el._sxT=setTimeout(function(){ el.classList.remove('sxflash'); },2100);
  });
}
function sxWire(){
  var input=document.getElementById('search'), res=document.getElementById('sxres');
  if(!input || !res) return;
  input.setAttribute('placeholder','Search all '+document.querySelectorAll('.brief').length+' briefs…');
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

