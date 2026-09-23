// Phone screenshot of the Index sheet. Usage: node tools/shot_sheet.js out.png [shelf] [openSystemIndex]
const {chromium}=require('playwright');
(async()=>{
 const out=process.argv[2]||'/tmp/claude-0/sheet.png',shelf=process.argv[3]||'peds',openIdx=process.argv[4];
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
 await p.goto('file://'+process.cwd()+'/index.html?shelf='+shelf);await p.waitForTimeout(700);
 await p.evaluate(()=>{const el=document.getElementById('bs-nrd');if(el)el.scrollIntoView();});
 await p.waitForTimeout(300);
 await p.click('#mbar [data-act="index"]');await p.waitForTimeout(500);
 if(openIdx!==undefined){await p.evaluate(i=>{const d=document.querySelectorAll('#sheet .sheetlist details')[+i];if(d)d.open=true;},openIdx);await p.waitForTimeout(200);}
 await p.screenshot({path:out});console.log(out);
 await b.close();
})();
