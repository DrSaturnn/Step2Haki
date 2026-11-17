// s176h B5: the section card counts follow the shelf. node repair/s176h/counts.js PAGE.html   (from workspace/)
const path=require('path');const {chromium}=require('playwright');const {serve}=require(path.resolve('tools/serve_page'));
(async()=>{const srv=await serve(process.argv[2]);const br=await chromium.launch();let bad=0;
for(const w of [1440,393]){const cx=await br.newContext({viewport:{width:w,height:900}});
await cx.addInitScript(()=>{localStorage.setItem('ax-settings',JSON.stringify({v:1,s:{tour:'1'}}));});
const pg=await cx.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));await pg.goto(srv.url);await pg.waitForTimeout(2500);
const shelves=await pg.evaluate(()=>[...document.querySelectorAll('.masthead .shelfpick [data-shelf]')].map(b=>b.dataset.shelf));
for(const s of shelves){await pg.evaluate(s=>{const b=document.querySelector('.masthead .shelfpick [data-shelf="'+s+'"]');b.click();},s);await pg.waitForTimeout(500);
const rows=await pg.evaluate(()=>[...document.querySelectorAll('main .wrap > .sectwrap')].filter(w=>w.style.display!=='none').map(w=>{const h=w.querySelector('h3.system'),n=h&&h.querySelector('.n');let live=0;for(let x=w.nextElementSibling;x&&!x.classList.contains('sectwrap');x=x.nextElementSibling)if(x.classList.contains('brief')&&x.style.display!=='none')live++;return {id:h&&h.id,txt:n?n.textContent:'',live};}).filter(r=>r.txt));
const wrong=rows.filter(r=>parseInt(r.txt)!==r.live);if(wrong.length)bad++;
console.log((wrong.length?'FAIL ':'PASS ')+w+' '+s+': '+rows.length+' section cards'+(wrong.length?' '+JSON.stringify(wrong):'')+(rows.find(r=>r.id==='presentations')?' (Presentations '+rows.find(r=>r.id==='presentations').txt+')':''));}
if(errs.length){bad++;console.log('FAIL page errors '+errs.join('; '));}await cx.close();}
console.log(bad?bad+' FAILED':'all passed');await br.close();srv.close();})();
