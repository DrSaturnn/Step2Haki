"""Rank existing questions that may test the same decision as a new NBME (or UWorld) question.
Usage: python3 tools/nbme_match.py "<key>" "<stem text>" [--top 10]
Scores: key similarity (token overlap with the item's key or its distractors) and stem word overlap.
It proposes candidates only; a person confirms the match."""
import sys,re,html
sys.path.insert(0,'tools');import axlib
key,stem=sys.argv[1],sys.argv[2];top=int(sys.argv[sys.argv.index('--top')+1]) if '--top' in sys.argv else 10
STOP=set('a an the of and or with in on to for is was has had his her he she this that at by from as be are were who which after before over under yo old year years month months day days'.split())
tok=lambda t:{w for w in re.findall(r'[a-z0-9]+',html.unescape(re.sub('<[^>]+>','',t or '')).lower()) if w not in STOP and len(w)>2}
src=open('index.html',encoding='utf-8').read();doc=axlib.parse_html(src)
K,S=tok(key),tok(stem);res=[]
spans=[(b.raw_start,b.raw_end,b.id) for b in doc.briefs]
for m in re.finditer(r'<li data-type="(\w+)"([^>]*)>(.*?)</li>',src,re.S):
    a=dict(re.findall(r'(data-[\w-]+)="([^"]*)"',m.group(2)));parts=re.split(r'\s*(?:→|&rarr;)\s*',m.group(3))
    ik=tok(parts[1] if len(parts)>1 else '');opts=ik|tok(a.get('data-d1'))|tok(a.get('data-d2'))
    ks=len(K&ik)/max(1,len(K|ik));ko=len(K&opts)/max(1,len(K))
    ss=len(S&tok(parts[0]))/max(1,len(S))
    score=round(0.5*ks+0.2*ko+0.3*ss,3)
    if score>0.15:
        b=next((x[2] for x in spans if x[0]<=m.start()<x[1]),'?')
        res.append((score,b,a.get('data-item-id'),m.group(1),re.sub('<[^>]+>','',parts[1] if len(parts)>1 else '')[:60],re.sub('<[^>]+>','',parts[0])[:90]))
for r in sorted(res,reverse=True)[:top]: print(*r,sep=' | ')
