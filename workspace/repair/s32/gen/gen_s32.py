#!/usr/bin/env python3
"""Generate repair/s32/*.json (replace_global ops) from the current index.html.
Every find is sliced verbatim from the page between asserted-unique markers."""
import json, os, re, sys
WS='/home/claude/Step2Haki/workspace'
SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)),'src')
page=open(os.path.join(WS,'index.html'),encoding='utf-8').read()

def uniq(s):
    n=page.count(s); assert n==1, (n, s[:80]); return page.index(s)
def region(start, end, incl_end=False):
    a=uniq(start); b=page.index(end, a)
    assert page.count(end, a, b+len(end))==1
    return page[a:b+len(end)] if incl_end else page[a:b]
def jsesc(s):
    return ''.join(c if ord(c)<128 else '\\u%04x'%ord(c) for c in s)
def src(name, js=True):
    t=open(os.path.join(SRC,name),encoding='utf-8').read()
    return jsesc(t) if js else t
def op(find, with_):
    uniq(find); return {"op":"replace_global","find":find,"with":with_}

# ---------------- CSS
css=[]
navrule=re.search(r'#nav\{position:fixed;top:0;left:0;width:var\(--sidebar\);height:100vh;[^}]*\}',page).group(0)
css.append(op(navrule, '#nav{position:fixed;top:0;left:0;width:var(--sidebar);height:100vh;background:#17171C;color:#fff;display:flex;flex-direction:column;overflow:hidden;padding:22px 0 0;z-index:50}'))
srule=re.search(r'#search\{width:calc\(100% - 36px\);[^}]*\}',page).group(0)
assert 'font-size:13.5px' in srule
css.append(op(srule, srule.replace('font-size:13.5px','font-size:16px').replace('margin:0 18px 14px','margin:0 18px 14px;display:block')))
css.append(op('  #nav{position:static;width:100%;height:auto}\n', ''))
css.append(op('#mbar,#sheet{display:none}\n@media (max-width:980px){\n  #nav{display:none}\n', '#mbar{display:none}\n@media (max-width:980px){\n'))
f=region('  /* the bar sits under the sheet, so the sheet carries its own close control */', '@media print{ #mbar,#sheet{display:none!important} }', True)
assert f.count('\n}\n@media print')==1 and f.endswith('\n}\n@media print{ #mbar,#sheet{display:none!important} }')
css.append(op(f, '}\n@media print{ #mbar{display:none!important} }'))
f=region('/* Index sheet, pass 2.', '/* ---------- PHONE: tables restack as one card per row')
assert all(k in f for k in ['.sheetin','.sheetlist a.here']) and '.tw' not in f
css.append(op(f, ''))
css.append(op('  .sheetin .shelfpick{margin:0 0 12px}\n', ''))
nb=re.search(r'\.nbmetog\{[^}]*\}\n\.nbmetog\.on\{[^}]*\}\n',page).group(0)
css.append(op(nb, ''))
f=region('@media (max-width:980px){\n  .sheetlist a.aq{', '  .sheetlist .msub.aq{color:var(--aquifer)}\n}\n', True)
css.append(op(f, ''))
css.append(op('body.flat .sheetlist details,body.flat .sheetin,body.flat #mbar{', 'body.flat #mbar{'))
css.append(op('@media (max-width:900px){\n  #rvlaunch{display:none}\n', '@media (max-width:900px){\n'))
st=page.index('</style>'); assert page.count('</style>')==1
tail=page[st-160:st+len('</style>')]
cssnew=src('css_new.css', js=False)
css.append(op(tail, page[st-160:st].rstrip('\n')+'\n'+cssnew.strip('\n').join(['\n','\n'])+'</style>'))

# ---------------- transform (script 2)
tr=[]
tr.append(op(region('/* ---------- 0. sidebar mode switches ---------- */','/* ---------- 0a. shelf selector'), src('r1_switches.js')))
tr.append(op(region("var shelf='step2';\nvar reviewSet=null;","function shelfPicker(kind){"), src('r2_vars.js')))
tr.append(op(region("  document.querySelectorAll('#nav a[href^=\"#\"], #sheet .sheetlist a[href^=\"#\"]')","  var meta=document.querySelector('.masthead .meta');"), src('r3_navcounts.js')))
v="(SHELVES.filter(function(x){return x[0]===s;})[0]||['','Step 2'])[1]+'</b></span>';"
tr.append(op(v, "(SHELVES.filter(function(x){return x[0]===s;})[0]||['','Step 2'])[1]+'</b>'+(boardOnly&&!reviewSet?' &middot; board-style only':'')+'</span>';"))
tr.append(op(region("function shelfInit(){","/* ---------- 0b. phone navigation"), src('r4_shelfinit.js')))
tr.append(op(region("/* ---------- 0b. phone navigation","/* ---------- 1. section headers"), src('r5_nav.js')))
tr.append(op(region("window.__axShelf={\n  set:function(ids){","  active:function(){ return !!reviewSet; },"), src('r6_axshelf.js')))

# ---------------- review module (script 3)
rv=[]
old=region("  /* Directly beneath the shelf selector:", "  var lau=buildLauncher('side');")
rv.append(op(old, "  /* Beneath the shelf selector and the three switches: what you choose\n     before you read sits together, and Review is the larger control. */\n  var sp=document.querySelector('#nav #modes')||document.querySelector('#nav .shelfpick');\n"))
h="  window.addEventListener('hashchange',function(){ setTimeout(paintChip,0); });\n"
rv.append(op(h, h+"  /* shelf, Board-style only and review all re-run applyShelf, which announces itself */\n  document.addEventListener('ax-shelf',function(){ setTimeout(paintChip,0); });\n"))

# ---------------- NBME script (script 4): the NBME-tested filter is retired
nb=[]
nb.append(op("   · NBME-tested filter (joins the shelf rule; an active review keeps its set)\n", ""))
t=region("function toggles(){", "function pct(r){")
nb.append(op(t, ""))
nb.append(op("function run(){ headerCounts(); chips(); toggles(); blueprint();", "function run(){ headerCounts(); chips(); blueprint();"))

out=os.path.join(WS,'repair','s32'); os.makedirs(out,exist_ok=True)
for name,ops in [('10_css.json',css),('20_transform.json',tr),('30_review.json',rv),('40_nbme.json',nb)]:
    json.dump({"edits":ops},open(os.path.join(out,name),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print(name,len(ops))
