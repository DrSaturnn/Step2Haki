// rail at 1512 x 945 and 1280 x 800: fit, current tile, track; then Display settings from the rail
const WS='/home/claude/Step2Haki/workspace';const {chromium}=require('playwright');const {serve}=require(WS+'/tools/serve_page');
(async()=>{const srv=await serve(process.env.PAGE||WS+'/index.html');const b=await chromium.launch();
for(const [W,H] of [[1512,945],[1280,800]]){
const p=await b.newPage({viewport:{width:W,height:H}});await p.addInitScript(()=>localStorage.setItem('ax-settings',JSON.stringify({v:1,s:{tour:'1'}})));
await p.goto(srv.url+'#mdd');await p.waitForTimeout(1800);
await p.evaluate(()=>document.querySelector('#modes .layout button[data-v="two"]').click());await p.waitForTimeout(1500);
await p.evaluate(()=>window.scrollBy(0,innerHeight*1.2));await p.waitForTimeout(600);
console.log(W,H,JSON.stringify(await p.evaluate(()=>{const r=document.getElementById('ax2rail');return {need:r.scrollHeight,have:r.clientHeight,tiles:[...r.querySelectorAll('.sec')].map(x=>x.textContent).join(' '),home:(r.querySelector('.sec.home')||{}).textContent,at:r.style.getPropertyValue('--ax2-at')}})));
await p.screenshot({path:'/home/claude/s172b_work/rail_'+H+'.png',clip:{x:0,y:0,width:700,height:H}});
if(H===945){await p.click('#ax2rail .cfg');await p.waitForTimeout(800);
 console.log('sheet',JSON.stringify(await p.evaluate(()=>{const s=document.getElementById('axdisp');const r=s&&s.getBoundingClientRect();return s?{on:s.classList.contains('on'),x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),vis:getComputedStyle(s).visibility}:null})));
 await p.screenshot({path:'/home/claude/s172b_work/rail_cfg.png',clip:{x:0,y:0,width:900,height:H}});}
await p.close();}
await b.close();srv.close();})();
