"""Per-turn token use of a Claude session transcript (main thread only).
Usage: python3 tools/session_usage.py <session.jsonl> [--since YYYY-MM-DDTHH:MM]
Each tool call re-reads the whole context, so cost per turn ~= calls x context size."""
import json,sys
f=sys.argv[1];since=sys.argv[sys.argv.index('--since')+1] if '--since' in sys.argv else ''
turns=[];cur=None
for line in open(f):
    x=json.loads(line)
    if x.get('isSidechain'): continue
    if x.get('type')=='user':
        c=x['message']['content']
        txt=c if isinstance(c,str) else ''.join(p.get('text','') for p in c if isinstance(p,dict) and p.get('type')=='text')
        if txt and not txt.startswith('<') and 'tool_result' not in str(c)[:50]:
            cur={'t':txt[:50].replace('\n',' '),'ts':x.get('timestamp','')[:16],'calls':0,'cr':0,'cw':0,'out':0,'ctx':0};turns.append(cur)
    elif x.get('type')=='assistant' and cur:
        u=x['message'].get('usage') or {}
        cur['calls']+=1;cur['cr']+=u.get('cache_read_input_tokens',0);cur['cw']+=u.get('cache_creation_input_tokens',0)
        cur['out']+=u.get('output_tokens',0);cur['ctx']=max(cur['ctx'],u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0))
T=[t for t in turns if t['calls'] and t['ts']>=since]
for t in T: print(f"{t['ts']} calls {t['calls']:3d} context {t['ctx']//1000:4d}k read {t['cr']/1e6:5.1f}M write {t['cw']/1e3:5.0f}k out {t['out']/1e3:4.0f}k | {t['t']}")
print(f"TOTAL calls {sum(t['calls'] for t in T)} read {sum(t['cr'] for t in T)/1e6:.1f}M write {sum(t['cw'] for t in T)/1e6:.2f}M out {sum(t['out'] for t in T)/1e3:.0f}k")
