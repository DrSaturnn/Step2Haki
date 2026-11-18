const WS='/home/claude/Step2Haki/workspace';const {chromium}=require('playwright');const {serve}=require(WS+'/tools/serve_page');
const cases=JSON.parse(process.argv[2]);
(async()=>{const srv=await serve(process.env.PAGE||WS+'/index.html');const b=await chromium.launch();
for(const [id,W,H,nav] of cases){
const p=await b.newPage({viewport:{width:W,height:H}});await p.addInitScript(n=>localStorage.setItem('ax-settings',JSON.stringify({v:1,s:{tour:'1'}})));
await p.goto(srv.url+'#'+id);await p.waitForTimeout(1800);
await p.evaluate(()=>document.querySelector('#modes .layout button[data-v="two"]').click());await p.waitForTimeout(1500);
if(nav){await p.evaluate(()=>document.querySelector('#ax2rail .ex').click());await p.waitForTimeout(1500);}
console.log(id,W,H,nav?'nav':'rail',JSON.stringify(await p.evaluate(()=>{const B=document.querySelector('.brief.ax2-cur');const out=[];
 B.querySelectorAll('.ax2-col:not(.ax2-hold)').forEach(c=>{const R=c.getBoundingClientRect().right;[...c.children].forEach(u=>{
   if(![...u.getClientRects()].some(q=>q.left>=R-1))return;
   // deepest element with a rect past R whose parent has rects both sides
   let deep=null;u.querySelectorAll('*').forEach(x=>{const rs=[...x.getClientRects()];if(rs.some(q=>q.width&&q.left>=R-1)&&rs.some(q=>q.width&&q.left<R-1))deep=x;});
   const all=[...u.querySelectorAll('*')].filter(x=>{const rs=[...x.getClientRects()];return rs.length&&rs.every(q=>!q.width||q.left>=R-1)&&!x.parentElement.closest('*')?.matches?.('x')}).slice(0,1);
   out.push({unit:u.dataset.name,opened:u.classList.contains('ax2-open-t'),deep:deep?deep.tagName.toLowerCase()+'.'+(deep.className||'').toString().replace(/ /g,'.')+' '+getComputedStyle(deep).display+' gtc:'+getComputedStyle(deep).gridTemplateColumns:null,firstOut:all[0]?all[0].tagName.toLowerCase()+'.'+(all[0].className||'').toString().split(' ')[0]+' in '+all[0].parentElement.tagName.toLowerCase()+'.'+(all[0].parentElement.className||'').toString().split(' ')[0]:null});});});
 return out;})));
await p.close();}
await b.close();srv.close();})();
