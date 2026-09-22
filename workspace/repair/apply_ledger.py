import json,sys
sys.path.insert(0,'tools');import axlib
L=json.load(open(sys.argv[1]));f='index.html';src=open(f,encoding='utf-8').read();orig=src
def span(s,bid):
    b=[x for x in axlib.parse_html(s).briefs if x.id==bid];assert len(b)==1,bid;return b[0].raw_start,b[0].raw_end
for ed in L['edits']:
    sc=ed.get('scope','brief:'+L.get('brief',''))
    s,e=(0,len(src)) if sc=='page' else span(src,sc.split(':',1)[1])
    body=src[s:e]
    if ed['op']=='replace':
        assert body.count(ed['old'])==1,(sc,ed['old'][:60],body.count(ed['old']));body=body.replace(ed['old'],ed['new'])
    elif ed['op'] in('insert_after','insert_before'):
        assert body.count(ed['anchor'])==1,(sc,ed['anchor'],body.count(ed['anchor']))
        i=body.index(ed['anchor'])+(len(ed['anchor']) if ed['op']=='insert_after' else 0);body=body[:i]+ed['text']+body[i:]
    src=src[:s]+body+src[e:]
assert src.count('<div')-src.count('</div')==orig.count('<div')-orig.count('</div')
assert src.count('<B>')==orig.count('<B>')
open(f,'w',encoding='utf-8').write(src);print('applied',len(L['edits']),'edits')
