"""Build a worker packet: rules + task + source excerpt + the brief's HTML + brief titles.
Usage: python3 repair/efficiency/make_packet.py <task_id> <brief_id> <source.md> "<Qn heading prefix>" "<task line>" <page> <out.md>"""
import sys,re,os
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','tools'));from axlib import parse_html
tid,bid,srcmd,qhead,task,page,out=sys.argv[1:8]
rules=open(os.path.join(os.path.dirname(__file__),'RULES_worker.md')).read()
s=open(srcmd).read();parts=re.split(r'(?m)^## ',s)
q=[p for p in parts if p.startswith(qhead)];assert len(q)==1,(qhead,len(q))
html=open(page,encoding='utf-8').read();D=parse_html(html)
b=[x for x in D.briefs if x.id==bid];assert len(b)==1;brief=html[b[0].raw_start:b[0].raw_end]
titles=[]
for x in D.briefs:
    t=html[x.raw_start:x.raw_end];h=re.search(r'<h4[^>]*>(.*?)</h4>',t,re.S)
    titles.append(f"{x.id} | {re.sub('<[^>]+>','',h.group(1)).strip() if h else ''}")
pk=f"""{rules}

# Task {tid}
{task}
Target brief: `{bid}`. Write your output to /home/claude/bench/out/{tid}_P.json.

# Source question
## {q[0].strip()}

# Brief HTML (current)
```html
{brief}
```

# Brief titles (id | exact title) for Pairs-with sentences
{chr(10).join(titles)}
"""
open(out,'w').write(pk);print(out,len(pk),'chars')
