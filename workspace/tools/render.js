const {JSDOM,VirtualConsole}=require('jsdom');const fs=require('fs');
const f=process.argv[2]||'index.html';const html=fs.readFileSync(f,'utf8');
const vc=new VirtualConsole();const logs=[];vc.on('log',m=>logs.push(String(m)));vc.on('jsdomError',e=>logs.push('ERR '+e.message));
const dom=new JSDOM(html,{runScripts:'dangerously',url:'http://localhost/',pretendToBeVisual:true,virtualConsole:vc,
 beforeParse(w){w.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}};w.scrollTo=()=>{};w.matchMedia=w.matchMedia||(()=>({matches:false,addListener(){},removeListener(){},addEventListener(){},removeEventListener(){}}));}});
dom.window.addEventListener('load',()=>setTimeout(()=>{const d=dom.window.document,$=s=>d.querySelectorAll(s).length;
 const mcqs=[...d.querySelectorAll('.mcq')];const cnt={};mcqs.forEach(m=>{const k=m.querySelectorAll('.opts button').length;cnt[k]=(cnt[k]||0)+1});console.error('optcounts',JSON.stringify(cnt));const bad=mcqs.filter(m=>m.querySelectorAll('.opts button').length!==3).length;
 const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);const dup=ids.filter((x,i)=>ids.indexOf(x)!==i);
 const dead=[...d.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(h=>h&&!d.getElementById(h));
 console.log(JSON.stringify({briefs:$('.brief'),bankwrap:$('.bankwrap'),mcq:mcqs.length,malformedMcq:bad,vignetteMask:$('.vignette .mask'),vignettes:$('.vignette'),axCheck:dom.window.__axCheck,dupIds:[...new Set(dup)].slice(0,10),dead:[...new Set(dead)].slice(0,10),errs:logs.filter(l=>l.startsWith('ERR')).slice(0,5),axlog:logs.filter(l=>l.includes('[ax]'))}));process.exit(0)},1500));
