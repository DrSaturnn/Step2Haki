"""Mechanical check of a Task A backfill draft before review.
Usage: python3 tools/verify_edits.py <draft.json> [--page <index.html>] [--nids "<nid nid ...>"]
Builds the ledger exactly as the batch builder does, applies it to a scratch copy of the page, runs the gate,
and reports each failure with the fix. Exit 0 = mechanically clean (judgment review still required)."""
import json,sys,os,re,shutil,subprocess,tempfile,html
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(HERE)
args=sys.argv[1:];draft=args[0]
page=args[args.index('--page')+1] if '--page' in args else os.path.join(ROOT,'index.html')
want_nids=set(args[args.index('--nids')+1].split()) if '--nids' in args else set()
sys.path.insert(0,HERE);from idgen import item_id,option_id
e=lambda s:html.escape(s,quote=True);errs=[];notes=[]
try: data=json.load(open(draft));data=data if isinstance(data,list) else [data]
except Exception as x: print('FAIL json:',x);sys.exit(1)
TYPES={'next','dx','test','mech','avoid','screen','stage','claim'}
EM='—'
def li(it):
    b,t=it['brief'],it['type'];q=item_id(b,t,it['key'],it['stem'])
    k,o1,o2=option_id(q,'key',it['key']),option_id(q,'d1',it['d1']),option_id(q,'d2',it['d2'])
    nid=it.get('nid');lead=it.get('lead')
    return (f'<li data-type="{t}" data-src="{it.get("src") or "authored"}"'+(f' data-nid="{nid}"' if nid else '')+
            f' data-d1="{e(it["d1"])}" data-d2="{e(it["d2"])}" data-item-id="{q}" data-item-version="1" data-item-status="ready" '
            f'data-key-id="{k}" data-d1-id="{o1}" data-d2-id="{o2}"'+(f' data-lead-in="{e(lead)}"' if lead else '')+
            f'>{e(it["stem"])} &rarr; <b>{e(it["key"])}</b> &rarr; {e(it["companion"])}</li>\n')
edits=[];newitems=0;src_items=[]
for o in data:
    for ed in o.get('edits',[]):
        txt=(ed.get('text') or '')+(ed.get('new') or '')
        if EM in txt: errs.append(f"em dash character in new text ({ed.get('why','')[:40]}): use a colon or comma; &mdash; only as a label separator")
        if '<li' in txt: errs.append('an edit inserts <li>: put questions in items, not edits')
        edits.append(ed)
    by={}
    for it in o.get('items',[]):
        miss=[k for k in ('brief','type','stem','key','companion','d1','d2') if not it.get(k)]
        if miss: errs.append(f"item missing {miss}: {it.get('stem','')[:50]}");continue
        if it['type'] not in TYPES: errs.append(f"bad type {it['type']}")
        opts=[x.strip().lower() for x in (it['key'],it['d1'],it['d2'])]
        if len(set(opts))<3: errs.append(f"options not distinct: {it['key']}")
        for k in ('stem','key','companion','d1','d2'):
            if EM in it[k] or '<' in it[k]: errs.append(f"item field {k} has an em dash or HTML: {it[k][:40]}")
        if len(it['key'])>max(len(it['d1']),len(it['d2']))+12: notes.append(f"answer cue: key much longer than distractors: {it['key']}")
        if it.get('src')=='uworld': src_items.append(it)
        by.setdefault(it['brief'],[]).append(li(it));newitems+=1
    for b,lis in by.items(): edits.append({"scope":"brief:"+b,"op":"insert_before","anchor":"</ol>","text":''.join(lis),"why":"items"})
if not src_items: errs.append('no source item (src "uworld")')
for it in src_items:
    got=set((it.get('nid') or '').split())
    if want_nids and got!=want_nids: errs.append(f"source item nids {sorted(got)} != expected {sorted(want_nids)}")
if not 2<=newitems<=4: notes.append(f"{newitems} new items (spec asks 2 to 4 per brief)")
tmp=tempfile.mkdtemp();shutil.copy(page,os.path.join(tmp,'index.html'))
shutil.copytree(HERE,os.path.join(tmp,'tools'));os.makedirs(os.path.join(tmp,'repair'))
shutil.copy(os.path.join(ROOT,'repair','apply_ledger.py'),os.path.join(tmp,'repair'))
json.dump({"pass":"verify","edits":edits},open(os.path.join(tmp,'L.json'),'w'))
before=subprocess.run([sys.executable,'tools/gate.py','index.html'],cwd=tmp,capture_output=True,text=True).stdout
r=subprocess.run([sys.executable,'repair/apply_ledger.py','L.json'],cwd=tmp,capture_output=True,text=True)
if r.returncode: errs.append('ledger did not apply: '+(r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ['?'])[-1][:300])
else:
    after=subprocess.run([sys.executable,'tools/gate.py','index.html'],cwd=tmp,capture_output=True,text=True).stdout
    nb=len(re.findall(r'^NEAR',before,re.M));na=len(re.findall(r'^NEAR',after,re.M))
    if na>nb: errs.append(f"new near-duplicate question(s): {na-nb}")
    if 'FAIL' in after: errs.append('gate: '+[l for l in after.splitlines() if l.startswith('FAIL')][0][:200])
shutil.rmtree(tmp,ignore_errors=True)
for n in notes: print('NOTE',n)
for x in errs: print('FAIL',x)
print('CLEAN' if not errs else f'{len(errs)} failure(s)', f'| edits {len(edits)-len([1 for o in data for _ in [0] if o.get("items")])} items {newitems}')
sys.exit(1 if errs else 0)
