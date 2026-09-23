"""s12: Aquifer setup pass.
- brief-level data-src="aquifer" on the 12 Aquifer-sourced briefs (11 board-style + shoulder-rom)
- each system gets an Aquifer band after its board-style band; Aquifer briefs move there (ids unchanged)
- nav: "Aquifer" subheader per system, links class "aq"; empty board-style subheaders removed
- system header counts; MSK topic count 23 -> 22
- CSS: Aquifer tokens, badge (source-driven), band, nav, sheet, clue tables, grouped first-test rows
- JS: band counts by source, masthead Aquifer count, sheet carries link classes, empty subheaders hide
bs-puv and bs-leukemia stay board-style: their source items are UWorld (subtitle conflict open with the user)."""
import json,re,sys
sys.path.insert(0,'tools');from axlib import parse_html
src=open('index.html').read();D=parse_html(src);B={b.id:b for b in D.briefs};order=[b.id for b in D.briefs]
edits=[]
AQ=['shoulder-rom','bs-shock','bs-infant-feeding','bs-tanner','bs-ftt','bs-preterm-followup','bs-shunt-timing',
    'bs-nrd','bs-febrile-infant','bs-posterior-fossa','bs-pid','bs-adolescent-vax']
SYS=[(m.start(),m.group(1)) for m in re.finditer(r'<h3 class="system" id="(\w+)"',src)]
def system_of(pos): return [sid for p,sid in SYS if p<pos][-1]
NAME={'msk':'Musculoskeletal &amp; Rheumatology','peds':'Pediatrics','cv':'Cardiovascular','pulm':'Pulmonary',
      'id':'Infectious Disease','neuro':'Neurology &amp; HEENT','obgyn':'Obstetrics &amp; Gynecology','prev':'Preventive Medicine &amp; Ethics'}
NEXT={'msk':'<!-- =================== PEDS','peds':'<!-- =================== CV','cv':'<!-- =================== PULM',
      'pulm':'<!-- =================== GI','id':'<!-- =================== NEURO','neuro':'<!-- =================== DERM',
      'obgyn':'<!-- =================== PREV','prev':'<div style="margin:70px 0 0;padding:22px 0 0;border-top:2px solid var(--rule)'}
groups={}
for bid in AQ: groups.setdefault(system_of(B[bid].raw_start),[]).append(bid)
def band(sid,n):
    return (f'<div class="bsband aqband"><span class="n">{n} brief{"s" if n>1 else ""}</span>'
            f'<span class="lbl">Aquifer &middot; Case-Based Briefs</span><p class="t">{NAME[sid]}</p></div>\n\n')
for sid,ids in groups.items():
    moved=''
    for bid in ids:
        b=B[bid];raw=src[b.raw_start:b.raw_end]
        old=raw+'\n\n' if src[b.raw_end:b.raw_end+2]=='\n\n' else raw
        edits.append({"scope":"page","op":"replace","old":old,"new":"","why":f"move {bid} into the {sid} Aquifer group"})
        opening=re.match(r'<div class="brief[^>]*>',raw).group(0)
        tag=opening[:-1]+' data-src="aquifer"'+(' data-case="FM 25"' if bid=='shoulder-rom' else '')+'>'
        moved+=raw.replace(opening,tag,1)+'\n\n'
    edits.append({"scope":"page","op":"insert_before","anchor":NEXT[sid],"text":band(sid,len(ids))+moved,
                  "why":f"{sid}: Aquifer band after the board-style band"})
# pulmonary board-style band is left empty (bs-nrd was its only brief)
pb=re.search(r'<div class="bsband"><span class="n">1 brief</span><span class="lbl">Board-Style &middot; Next-Step Questions</span><p class="t">Pulmonary</p></div>\n\n',src).group(0)
edits.append({"scope":"page","op":"replace","old":pb,"new":"","why":"pulmonary board-style band is empty after the move"})

# ---- nav
n0=src.index('<div id="navlinks">')+len('<div id="navlinks">');n1=src.index('\n  </div>\n</aside>')
nav=src[n0:n1];lines=nav.split('\n')
out=[];blocks=[];cur=None
for ln in lines:
    if 'class="sect"' in ln:
        cur=[ln];blocks.append(cur)
    elif cur is None: out.append(ln)
    else: cur.append(ln)
newnav=out[:]
for blk in blocks:
    aq_lines=[];keep=[]
    for ln in blk:
        m=re.search(r'href="#([\w-]+)"',ln)
        if m and m.group(1) in AQ:
            text=re.search(r'>([^<]*)</a>',ln).group(1)
            aq_lines.append(f'    <a class="aq" href="#{m.group(1)}">{text}</a>')
        else: keep.append(ln)
    # drop an empty board-style subheader
    k2=[]
    for i,ln in enumerate(keep):
        if 'class="navsub"' in ln and not any('class="bs"' in x for x in keep[i+1:] if 'class="sect"' not in x):
            continue
        k2.append(ln)
    if aq_lines:
        # insert after the last link of the block (before trailing blank lines)
        j=max(i for i,x in enumerate(k2) if '<a ' in x)
        k2=k2[:j+1]+['    <div class="navsub aq">Aquifer</div>']+aq_lines+k2[j+1:]
    newnav+=k2
newnav='\n'.join(newnav).replace('<div class="sect">Musculoskeletal <span class="count">23</span></div>','<div class="sect">Musculoskeletal <span class="count">22</span></div>')
assert newnav!=nav
edits.append({"scope":"page","op":"replace","old":nav,"new":newnav,"why":"nav: Aquifer subheaders; empty board-style subheader removed"})

# ---- system header counts
AQC='<span style="color:#1F6A7E">'
def hdr(sid,topics,bs,aq):
    m=re.search(rf'<h3 class="system" id="{sid}">(.*?)</h3>',src).group(0)
    name=re.match(rf'<h3 class="system" id="{sid}">([^<]*)',m).group(1)
    parts=f'{topics} topics'+(f' <span style="color:#9A5B0E">+ {bs} board-style</span>' if bs else '')+(f' {AQC}+ {aq} Aquifer</span>' if aq else '')
    edits.append({"scope":"page","op":"replace","old":m,"new":f'<h3 class="system" id="{sid}">{name}<span class="n">{parts}</span></h3>',"why":f"{sid} header counts"})
for sid,t,bs,aq in [('msk',22,4,1),('peds',5,1,5),('cv',15,1,1),('pulm',14,0,1),('id',10,3,1),('neuro',12,3,1),('obgyn',10,2,1),('prev',5,1,1)]:
    hdr(sid,t,bs,aq)

# ---- CSS
CSS=r'''
/* ---------- AQUIFER: source-driven badge, band, nav ---------- */
:root{--aquifer:#1F6A7E;--aquifer-bg:#E2EDF0}
.brief[data-src="aquifer"] > h4::after{content:"Aquifer";display:inline-block;vertical-align:5px;margin-left:10px;font-family:var(--sans);font-size:9px;font-weight:800;letter-spacing:1px;color:var(--aquifer);background:linear-gradient(145deg,#E7F0F2 0%,#DDE9EC 52%,#D3E2E6 100%);padding:5px 9px;border-radius:var(--r-chip);box-shadow:var(--ec)}
.brief[data-src="aquifer"] h5{color:var(--aquifer)}
.aqband{background:linear-gradient(145deg,#DCE8EB 0%,var(--aquifer-bg) 48%,#EEF5F6 100%)}
.aqband .lbl,.aqband .n{color:var(--aquifer)}
body.flat .aqband{background:var(--aquifer-bg);background-image:none}
#nav .navsub.aq{color:#86BFCD}
#nav a.aq{padding-left:30px;font-size:12.6px}
@media (max-width:980px){
  .sheetlist a.aq{padding-left:26px;color:var(--aquifer)}
  .sheetlist .msub.aq{color:var(--aquifer)}
}
/* clue tables: plain clue, emphasized pointer */
table.cluet tbody td:first-child{font-weight:400;color:var(--ink-2);width:46%}
@media (max-width:640px){
  .tw table.cluet tbody td:first-child{font-family:var(--sans);font-size:14px;font-weight:400;color:var(--ink-2);border-bottom:none;padding:0 0 2px;margin:0;width:100%}
  .tw table.cluet tbody td:not(:first-child)::before{content:"\2192  ";display:inline;font-size:14px;letter-spacing:0;text-transform:none;font-weight:400;color:var(--faint)}
  .tw table.cluet tbody td{padding:2px 0}
  .tw table.cluet tbody{background:linear-gradient(145deg,#F4F5F5 0%,#EEF0F0 55%,#E9EBEB 100%);border-radius:14px;box-shadow:var(--e2);overflow:hidden;margin:0 0 4px}
  .tw table.cluet tbody tr{background:none!important;box-shadow:none;border-radius:0;margin:0;padding:11px 15px}
  .tw table.cluet tbody tr+tr{border-top:1px solid rgba(24,28,30,.08)}
}
/* the first test's outcomes: one branch point, read as one unit */
.tw tbody.grp td{background:rgba(84,74,196,.045)}
.tw tbody.grp tr:nth-child(even){background:none}
.tw tbody.grp tr td:first-child{box-shadow:inset 3px 0 0 rgba(84,74,196,.5)}
.tw tbody.grp tr:last-child td{border-bottom:1px solid rgba(84,74,196,.22)}
@media (max-width:640px){
  .tw tbody.grp{background:linear-gradient(145deg,#F2F1FA 0%,#EDECF7 60%,#E9E8F4 100%);border-radius:14px;box-shadow:var(--e2),inset 0 0 0 1.5px rgba(84,74,196,.22);overflow:hidden;margin:0 0 11px}
  .tw tbody.grp tr{background:none!important;box-shadow:none;border-radius:0;margin:0;padding:10px 15px}
  .tw tbody.grp tr+tr{border-top:1px solid rgba(84,74,196,.14)}
  .tw tbody.grp td{background:none;border:none}
  .tw tbody.grp tr td:first-child{box-shadow:none}
  .tw tbody.grp td:nth-child(3)::before{content:none}
  .tw tbody.grp td:nth-child(4)::before{content:"\2192  ";display:inline;font-size:14px;letter-spacing:0;text-transform:none;font-weight:400;color:var(--faint)}
  .tw tbody.grp td:nth-child(3),.tw tbody.grp td:nth-child(4){padding:2px 0}
  .tw tbody.grp tr:first-child td:nth-child(3){padding-top:8px}
  .tw tbody.grp tr:last-child td{border-bottom:none}
  .tw tbody.grp tr:first-child td:first-child{border-bottom:1px solid rgba(84,74,196,.16)}
}
'''
edits.append({"scope":"page","op":"insert_before","anchor":"</style>\n</head>","text":CSS,"why":"Aquifer CSS"})

# ---- JS
def js(old,new,why): edits.append({"scope":"page","op":"replace","old":old,"new":new,"why":why})
js("""    var n=0,el=bb.nextElementSibling;
    while(el&&el.classList.contains('brief')){
      if(el.classList.contains('bs')&&el.style.display!=='none')n++;""",
   """    var n=0,el=bb.nextElementSibling,aq=bb.classList.contains('aqband');
    while(el&&el.classList.contains('brief')){
      if((aq?el.dataset.src==='aquifer':el.classList.contains('bs'))&&el.style.display!=='none')n++;""","bands count by source")
js("""    var bs=0;
    document.querySelectorAll('.brief.bs').forEach(function(b){if(b.style.display!=='none')bs++;});
    meta.innerHTML='<span><b>'+(visible-bs)+'</b> topics</span>'+
      '<span><b>'+bs+'</b> board-style</span><span><b>'+liveSystems+'</b> systems</span>'+""",
   """    var bs=0,aq=0;
    document.querySelectorAll('.brief').forEach(function(b){
      if(b.style.display==='none')return;
      if(b.dataset.src==='aquifer')aq++; else if(b.classList.contains('bs'))bs++;
    });
    meta.innerHTML='<span><b>'+(visible-bs-aq)+'</b> topics</span>'+
      '<span><b>'+bs+'</b> board-style</span>'+(aq?'<span><b>'+aq+'</b> Aquifer</span>':'')+'<span><b>'+liveSystems+'</b> systems</span>'+""","masthead Aquifer count")
js("""    var group=null,live=0;
    Array.prototype.slice.call(navHost.children).forEach(function(el){
      if(el.classList.contains('sect')){
        if(group)group.style.display=live?'':'none';
        group=el;live=0;
      }else if(el.tagName==='A'&&el.style.display!=='none')live++;
      else if(el.classList.contains('navsub'))el.style.display='';
    });
    if(group)group.style.display=live?'':'none';""",
   """    var group=null,live=0,sub=null,subLive=0;
    function closeSub(){ if(sub)sub.style.display=subLive?'':'none'; sub=null; subLive=0; }
    Array.prototype.slice.call(navHost.children).forEach(function(el){
      if(el.classList.contains('sect')){
        closeSub();
        if(group)group.style.display=live?'':'none';
        group=el;live=0;
      }else if(el.tagName==='A'&&el.style.display!=='none'){live++;subLive++;}
      else if(el.classList.contains('navsub')){ closeSub(); sub=el; }
    });
    closeSub();
    if(group)group.style.display=live?'':'none';""","nav subheaders hide when their group is empty")
js("""    d.querySelectorAll('.msub').forEach(function(x){ x.style.display=mobileIndexQuery?'none':''; });""",
   """    d.querySelectorAll('.msub').forEach(function(x){
      if(mobileIndexQuery){ x.style.display='none'; return; }
      var n=0,el=x.nextElementSibling;
      while(el&&!el.classList.contains('msub')){ if(el.tagName==='A'&&el.style.display!=='none')n++; el=el.nextElementSibling; }
      x.style.display=n?'':'none';
    });""","sheet subheaders hide when their group is empty")
js("""      cur.items.push({href:el.getAttribute('href'), text:norm(el.textContent), bs:el.classList.contains('bs')});""",
   """      cur.items.push({href:el.getAttribute('href'), text:norm(el.textContent), cls:el.classList.contains('aq')?'aq':(el.classList.contains('bs')?'bs':'')});""","sheet carries link class")
js("""      cur.items.push({sub:norm(el.textContent)});""","""      cur.items.push({sub:norm(el.textContent), aq:el.classList.contains('aq')});""","sheet carries subheader class")
js("""      if(it.sub){ var h=document.createElement('div'); h.className='msub'; h.textContent=it.sub; d.appendChild(h); return; }""",
   """      if(it.sub){ var h=document.createElement('div'); h.className='msub'+(it.aq?' aq':''); h.textContent=it.sub; d.appendChild(h); return; }""","sheet subheader class")
js("""      if(it.bs) a.className='bs';""","""      if(it.cls) a.className=it.cls;""","sheet link class")

json.dump({"pass":"s12","date":"2026-09-23","reason":"Aquifer setup: source-driven badge, Aquifer bands and nav groups, counts, CSS and JS for Aquifer briefs.","expected":{"mcq_delta":0},"edits":edits},open('repair/LEDGER-s12.json','w'),indent=1,ensure_ascii=False)
print(len(edits),'edits;',{k:len(v) for k,v in groups.items()})
