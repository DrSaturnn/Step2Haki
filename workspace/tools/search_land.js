#!/usr/bin/env node
// search_land: press Enter on each query in the search box and report where the page lands (s164c).
//
//   node tools/search_land.js PAGE QUERY [QUERY ...] [--phone]
//
// Per query, from the top of the page: the first hit (brief id, whether it was unbuilt, block label), then after the
// scroll settles: whether the brief is built, the flashed block's top in the viewport, the address hash, and how many
// briefs are still unbuilt. A good landing puts the flashed block inside the viewport.
'use strict';
const { chromium } = require('playwright');
const path=require('path');
(async()=>{
  const argv=process.argv.slice(2), phone=argv.includes('--phone'), [page,...qs]=argv.filter(a=>a!=='--phone');
  const b=await chromium.launch(); const p=await (await b.newContext({viewport:phone?{width:390,height:844}:{width:1512,height:945}, hasTouch:phone})).newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+path.resolve(page),{waitUntil:'load'}); await p.waitForTimeout(1200);
  for(const q of qs){
    await p.evaluate(()=>window.scrollTo({top:0,behavior:'instant'})); await p.waitForTimeout(1500);
    const top=await p.evaluate(q=>{ const h=window.__axSearch.search(q).hits[0]; return h? {id:h.r.id,lazy:!!h.r.lazy,label:h.r.blocks[h.best.bi].label}:null; },q);
    await p.evaluate(()=>{ document.querySelectorAll('[data-sxt]').forEach(e=>e.removeAttribute('data-sxt')); if(!window.__mo){ window.__mo=new MutationObserver(ms=>ms.forEach(m=>{ if(m.target.classList&&m.target.classList.contains('sxflash')) m.target.setAttribute('data-sxt','1'); })); __mo.observe(document.body,{subtree:true,attributes:true,attributeFilter:['class']}); } });
    if(phone && !(await p.isVisible('#search'))){ await p.click('#navtab'); await p.waitForTimeout(600); }   // the phone search sits in the navigation panel
    await p.fill('#search',q); await p.press('#search','Enter'); await p.waitForTimeout(4500);
    const r=await p.evaluate(id=>{ const b=document.getElementById(id); const f=document.querySelector('[data-sxt]');
      const rc=f&&f.getBoundingClientRect(); return {built:!b.querySelector(':scope > template.axl'), flashIn: f? b.contains(f):null, flashTop: rc? Math.round(rc.top):null, vh:innerHeight, hash:location.hash, unbuilt:document.querySelectorAll('.brief > template.axl').length}; },top.id);
    console.log(q, JSON.stringify(top), JSON.stringify(r));
  }
  console.log('errors',errs.length, errs.slice(0,3)); await b.close();
})();
