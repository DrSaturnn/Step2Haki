import json,re,sys
sys.path.insert(0,'tools');from axlib import parse_html
s=open('index.html').read();d=parse_html(s);B={b.id:s[b.raw_start:b.raw_end] for b in d.briefs}
edits=[]
def tag(bid,pos,val,why):
    li=re.findall(r'<li [^>]*>',B[bid])[pos-1]
    assert 'data-src' not in li and B[bid].count(li)==1,(bid,pos)
    edits.append({"scope":"brief:"+bid,"op":"replace","old":li,"new":li.replace('<li ',f'<li data-src="{val}" ',1),"why":why})
tag('shoulder-rom',1,'aquifer',"case item of Aquifer FM 25 (named in the subtitle); metadata only, no version bump")
for i in range(2,8): tag('shoulder-rom',i,'authored',"variants written around the Aquifer case")
for i in (5,12,13): tag('bs-nrd',i,'authored',"later addendum item never tagged")
for i in (10,11,12): tag('bs-preterm-followup',i,'authored',"later addendum item never tagged")
json.dump({"pass":"s11","date":"2026-09-23","reason":"source-tag gaps: shoulder-rom case item, six untagged addendum items","expected":{"mcq_delta":0},"edits":edits},open('repair/LEDGER-s11.json','w'),indent=1)
print(len(edits))
