// Screenshot a selector at phone and desktop widths. Usage: node tools/shot.js "<css selector>" [outprefix]
const {chromium}=require('playwright');
(async()=>{
 const sel=process.argv[2]||'.traps',pre=process.argv[3]||'/tmp/claude-0/shot';
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 for(const [w,n] of [[390,'phone'],[1100,'desk']]){
  const p=await b.newPage({viewport:{width:w,height:900},deviceScaleFactor:2});
  await p.goto('file://'+process.cwd()+'/index.html');await p.waitForTimeout(800);
  const el=await p.$(sel);await el.scrollIntoViewIfNeeded();
  await el.screenshot({path:`${pre}_${n}.png`});console.log(`${pre}_${n}.png`);
 }
 await b.close();
})();
