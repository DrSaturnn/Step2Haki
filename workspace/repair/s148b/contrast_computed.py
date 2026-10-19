#!/usr/bin/env python3
"""s148b computed-contrast cross-check (no screenshots): for every text node in the given briefs, the text color
(alpha composited) against the first opaque background found up its ancestor chain (a gradient counts by its first
stop; a translucent fill is composited over what lies beneath). Need 4.5:1, or 3:1 at 24 px or 18.66 px bold.
Masked study text and SVG are skipped. Complements legib_audit, whose tall-element capture can catch the page
mid-reflow.

  python3 repair/s148b/contrast_computed.py <page.html> <brief,...> [--themes light,dark,tinted] [--accents a,b]
                                            [--widths 1180,390] [--modes sculpted,flat]
"""
import sys
from playwright.sync_api import sync_playwright

JS = r"""(bids)=>{
const P=c=>{const m=c&&c.match(/rgba?\(([^)]+)\)/);if(m){const v=m[1].split(/[ ,/]+/).filter(Boolean).map(Number);return [v[0],v[1],v[2],v.length>3?v[3]:1]}
 const s=c&&c.match(/color\(srgb ([^)]+)\)/);if(s){const v=s[1].split(/[ /]+/).filter(Boolean).map(Number);return [v[0]*255,v[1]*255,v[2]*255,v.length>3?v[3]:1]}return null};
const L=c=>{const f=x=>{x/=255;return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4)};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])};
const over=(a,b)=>[a[0]*a[3]+b[0]*(1-a[3]),a[1]*a[3]+b[1]*(1-a[3]),a[2]*a[3]+b[2]*(1-a[3]),1];
const bgOf=el=>{const st=[];for(let e=el;e;e=e.parentElement){const cs=getComputedStyle(e);let c=P(cs.backgroundColor);
  if(cs.backgroundImage&&/gradient/.test(cs.backgroundImage)){const g=cs.backgroundImage.match(/(rgba?\([^)]+\)|color\(srgb [^)]+\))/);if(g)c=P(g[1])}
  if(c&&c[3]>0){st.push(c);if(c[3]>=.999)break}}
  let b=[255,255,255,1];const root=P(getComputedStyle(document.documentElement).backgroundColor);if(root&&root[3]>0)b=root;
  for(let i=st.length-1;i>=0;i--)b=over(st[i],b);return b};
const out=[];
for(const id of bids){const B=document.getElementById(id);if(!B)continue;const w=document.createTreeWalker(B,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.textContent.trim();if(t.length<2)continue;const el=n.parentElement;if(!el||el.closest('svg,.bb-rail,.bb-bar'))continue;
  if(el.closest('details:not([open])')&&!el.closest('summary'))continue;
  const cs=getComputedStyle(el);if(cs.display==='none'||cs.visibility==='hidden')continue;
  if(el.closest('.mask:not(.shown)')&&document.body.classList.contains('study'))continue;
  let op=1;for(let e=el;e;e=e.parentElement)op*=parseFloat(getComputedStyle(e).opacity||'1');
  const r=el.getBoundingClientRect();if(r.width<2||r.height<4)continue;
  let fg=P(cs.color);if(!fg)continue;fg=[fg[0],fg[1],fg[2],fg[3]*op];
  const bg=bgOf(el);const f=over(fg,bg);const a=L(f),b=L(bg);const cr=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  const fs=parseFloat(cs.fontSize),fw=parseInt(cs.fontWeight);const need=(fs>=24||(fw>=700&&fs>=18.66))?3:4.5;
  if(cr<need)out.push([id,el.tagName.toLowerCase()+'.'+[...el.classList].join('.'),Math.round(cr*100)/100,need,t.slice(0,40)])}}
return out}"""


def opt(a, k, d):
    return a[a.index(k) + 1] if k in a else d


def main(a):
    page, bids = a[0], a[1].split(',')
    themes = opt(a, '--themes', 'light,dark,tinted').split(',')
    accents = opt(a, '--accents', '').split(',') if '--accents' in a else ['']
    widths = [int(w) for w in opt(a, '--widths', '1180,390').split(',')]
    modes = opt(a, '--modes', 'sculpted,flat,study').split(',')
    total = 0
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for th in themes:
            for ac in accents:
                for w in widths:
                    for m in modes:
                        c = b.new_context(viewport={'width': w, 'height': 900})
                        c.add_init_script("try{localStorage.setItem('ax-flat','%s');localStorage.setItem('ax-study','%s');%s%s}catch(e){}" % (
                            '1' if m == 'flat' else '0', '1' if m == 'study' else '0',
                            "localStorage.setItem('ax-theme','%s');" % th if th != 'light' else '',
                            "localStorage.setItem('ax-accent','%s');" % ac if ac else ''))
                        p = c.new_page(); p.goto('file://' + page); p.wait_for_timeout(1500)
                        p.add_style_tag(content='*{content-visibility:visible!important}'); p.wait_for_timeout(300)
                        bad = p.evaluate(JS, bids)
                        total += len(bad)
                        print('%-6s %-8s %4d %-8s below %d %s' % (th, ac or '-', w, m, len(bad), bad[:5]))
                        c.close()
    print('contrast_computed: %d below' % total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
