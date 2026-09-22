import json,sys,hashlib
sys.path.insert(0,'tools');import axlib
L=json.load(open(sys.argv[1]));f='index.html';src=open(f,encoding='utf-8').read()
doc=axlib.parse_html(src);b=[x for x in doc.briefs if x.id==L['brief']];assert len(b)==1
s,e=b[0].raw_start,b[0].raw_end;body=src[s:e]
for ed in L['edits']:
    if ed['op']=='replace':
        assert body.count(ed['old'])==1,(ed['id'],body.count(ed['old']));body=body.replace(ed['old'],ed['new'])
    elif ed['op']=='insert_after':
        assert body.count(ed['anchor'])==1,ed['id'];i=body.index(ed['anchor'])+len(ed['anchor']);body=body[:i]+ed['text']+body[i:]
out=src[:s]+body+src[e:]
assert out.count('<div')-out.count('</div')==src.count('<div')-src.count('</div')
assert out.count('<B>')==src.count('<B>')
open(f,'w',encoding='utf-8').write(out);print('applied',len(L['edits']),'edits; bytes',len(src),'->',len(out))
