import sys,os,json,re,collections
sys.path.insert(0,'tools');sys.path.insert(0,'tools/spine');sys.path.insert(0,'repair/pilots/s167c')
import pagelib,hovers
from prose_lint import text_key, lint_brief
src=sys.argv[1]; dst=sys.argv[2]
h=pagelib.read_page(src)
tot=collections.Counter();edits=[];notes=[];diff=[];lintd=[]
def norm(s): return s
for b in pagelib.briefs(h):
    new,st,nt=hovers.transform(b.inner)
    tot.update(st)
    if new!=b.inner:
        edits.append((b.inner_start,b.inner_end,new))
        if norm(text_key(b.inner))!=norm(text_key(new)): diff.append(b.id)
        if len(lint_brief(b.inner))!=len(lint_brief(new)): lintd.append((b.id,len(lint_brief(b.inner)),len(lint_brief(new))))
        notes+=[(b.id,)+n for n in nt]
pagelib.write_page(dst,pagelib.splice(h,edits))
with open('local/s167c/hover_notes.md','w') as f:
    for n in notes: f.write(' | '.join(n)+'\n')
print(dict(tot),'briefs changed',len(edits),'textkey diffs',diff[:10],len(diff),'lint count diffs',lintd[:8],len(lintd))
