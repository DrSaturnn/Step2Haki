import json,sys
sys.path.insert(0,'tools');import axlib
L=json.load(open(sys.argv[1]));f='index.html';src=open(f,encoding='utf-8').read();orig=src
import re as _re
# pre-write guards: every new item/brief id must be absent before anything is written
_new=[x for ed in L['edits'] for x in _re.findall(r'<li [^>]*data-item-id="([^"]+)"',ed.get('text','')+ed.get('new',''))]
_have=set(_re.findall(r'<li [^>]*data-item-id="([^"]+)"',src))
# ids leaving the page in this ledger (replaced or moved) may reappear once in the new text
_repl={x for ed in L['edits'] if ed['op']=='replace' for x in _re.findall(r'<li [^>]*data-item-id="([^"]+)"',ed.get('old',''))}
_moved_briefs={x for ed in L['edits'] if ed['op']=='replace' for x in _re.findall(r'<div class="brief[^"]*" id="([^"]+)"',ed.get('old',''))}
assert len(_new)==len(set(_new)),'duplicate id inside this ledger'
_clash=[x for x in _new if x in _have and x not in _repl];assert not _clash,('id already on page',_clash)
for bid in _re.findall(r'<div class="brief[^"]*" id="([^"]+)"',''.join(ed.get('text','') for ed in L['edits'])):
    assert bid in _moved_briefs or f'id="{bid}"' not in src,('brief id exists',bid)
def span(s,bid):
    b=[x for x in axlib.parse_html(s).briefs if x.id==bid];assert len(b)==1,bid;return b[0].raw_start,b[0].raw_end
for ed in L['edits']:
    sc=ed.get('scope','brief:'+L.get('brief',''))
    s,e=(0,len(src)) if sc=='page' else span(src,sc.split(':',1)[1])
    body=src[s:e]
    if ed['op']=='replace':
        assert body.count(ed['old'])==1,(sc,ed['old'][:60],body.count(ed['old']));body=body.replace(ed['old'],ed['new'])
    elif ed['op']=='insert_before_end':
        assert body.endswith('</div>'),sc;body=body[:-6]+ed['text']+'</div>'
    elif ed['op']=='set_attr':
        # attribute-only edit on one opening tag: an item (by data-item-id) or the brief div itself
        if 'item' in ed: pat=r'<li [^>]*data-item-id="%s"[^>]*>'%_re.escape(ed['item'])
        else: pat=r'<div class="brief[^"]*" id="%s"[^>]*>'%_re.escape(sc.split(':',1)[1])
        tags=_re.findall(pat,body);assert len(tags)==1,(sc,ed.get('item'),len(tags))
        tag=tags[0];a=ed['attr'];v=ed['value'].replace('&','&amp;').replace('"','&quot;')
        if _re.search(r'\s%s="[^"]*"'%_re.escape(a),tag): nt=_re.sub(r'(\s%s=")[^"]*(")'%_re.escape(a),lambda m:m.group(1)+v+m.group(2),tag,count=1)
        else: nt=tag[:-1]+f' {a}="{v}">'
        body=body.replace(tag,nt,1)
    elif ed['op'] in('insert_after','insert_before'):
        assert body.count(ed['anchor'])==1,(sc,ed['anchor'],body.count(ed['anchor']))
        i=body.index(ed['anchor'])+(len(ed['anchor']) if ed['op']=='insert_after' else 0);body=body[:i]+ed['text']+body[i:]
    src=src[:s]+body+src[e:]
assert src.count('<div')-src.count('</div')==orig.count('<div')-orig.count('</div')
assert src.count('<B>')==orig.count('<B>')
open(f,'w',encoding='utf-8').write(src);print('applied',len(L['edits']),'edits')
import subprocess;r=subprocess.run([sys.executable,'tools/gate.py',f],capture_output=True,text=True);print(r.stdout.strip().splitlines()[0])
if r.returncode: print(r.stdout);sys.exit('GATE FAILED after write; revert with git checkout index.html')
