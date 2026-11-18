const WS='/home/claude/Step2Haki/workspace';const {chromium}=require('playwright');const {serve}=require(WS+'/tools/serve_page');
const [id,W,H,nav]=[process.argv[2]||'hpv',+(process.argv[3]||1512),+(process.argv[4]||945),process.argv[5]==='nav'];
(async()=>{const srv=await serve(process.env.PAGE||WS+'/index.html');const b=await chromium.launch();
const p=await b.newPage({viewport:{width:W,height:H}});await p.addInitScript(()=>localStorage.setItem('ax-settings',JSON.stringify({v:1,s:{tour:'1'}})));
await p.goto(srv.url+'#'+id);await p.waitForTimeout(1800);
await p.evaluate(()=>document.querySelector('#modes .layout button[data-v="two"]').click());await p.waitForTimeout(1500);
if(nav){await p.evaluate(()=>document.querySelector('#ax2rail .ex').click());await p.waitForTimeout(1200);}
console.log(JSON.stringify(await p.evaluate(()=>{const B=document.querySelector('.brief.ax2-cur');const out=[];
 B.querySelectorAll('.ax2-page').forEach((pg,pi)=>{pg.querySelectorAll(':scope > .ax2-cols > .ax2-col').forEach((c,ci)=>{const cr=c.getBoundingClientRect();
  const cs=getComputedStyle(c);
  const units=[...c.children].map(u=>{const rs=[...u.getClientRects()].map(r=>[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]);return {name:u.dataset.name||u.className, rects:rs, kids:[...u.children].slice(0,40).map(k=>{const q=[...k.getClientRects()];return k.tagName.toLowerCase()+'.'+(k.className||'').toString().split(' ')[0]+':'+q.map(r=>Math.round(r.left)+'/'+Math.round(r.top)+'/'+Math.round(r.height)).join('|')})}});
  const bad=units.some(u=>u.rects.some(r=>r[0]>=cr.right-1));
  if(bad) out.push({pi,ci,col:[Math.round(cr.left),Math.round(cr.top),Math.round(cr.right),Math.round(cr.height)],styleH:c.style.height,colcount:cs.columnCount,colw:cs.columnWidth,hold:c.classList.contains('ax2-hold'),units});});});return out;}),null,1));
await b.close();srv.close();})();
