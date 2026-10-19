#!/usr/bin/env python3
"""s148b onset timeline sweep (SITE_BODY_GLANCE.md, Decided D, check 5).

  python3 repair/s148b/onset_sweep.py <page.html> [--widths 1440,1024,820,400] [--out report.json]

For every onset timeline and course track (figure.sp-on) on the page, at each width, in light, dark and study modes:
  text   every text line of a card lies inside that card (1 px tolerance);
  cards  no two cards overlap;
  leader no leader line crosses a card other than its own (events at the same time share one line).
Prints one line per brief and mode with its counts and exits 1 on any failure."""
import json, sys
from playwright.sync_api import sync_playwright

JS = r"""()=>{
const out=[];const inside=(r,c)=>r.left>=c.left-1&&r.right<=c.right+1&&r.top>=c.top-1&&r.bottom<=c.bottom+1;
const hit=(a,b)=>Math.min(a.right,b.right)-Math.max(a.left,b.left)>0.5&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>0.5;
for(const fig of document.querySelectorAll('.brief figure.sp-on')){
 const B=fig.closest('.brief');const f=fig.querySelector('.sp-on-f');
 const lis=[...fig.querySelectorAll('.sp-on-ev > li, .sp-trk > li')];
 const r={brief:B.id,kind:f?'onset':'course',list:fig.classList.contains('sp-on-list'),js:!!(f&&f.classList.contains('sp-on-js')),text:0,cards:0,leader:0,n:lis.length,bad:[]};
 const cards=lis.map(li=>{const d=f?li.firstElementChild:li;return d});
 const rects=cards.map(d=>d.getBoundingClientRect());
 cards.forEach((d,i)=>{const w=document.createTreeWalker(d,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;
   const rg=document.createRange();rg.selectNodeContents(n);for(const q of rg.getClientRects()){if(q.width<1)continue;if(!inside(q,rects[i])){r.text++;r.bad.push('text '+i+' '+n.textContent.trim().slice(0,30));break}}}});
 const floating=f&&getComputedStyle(cards[0]).position==='absolute';
 if(floating){
  for(let i=0;i<rects.length;i++)for(let j=i+1;j<rects.length;j++)if(hit(rects[i],rects[j])){r.cards++;r.bad.push('cards '+i+'x'+j)}
  const fr=f.getBoundingClientRect();
  const xs=lis.map(li=>li.getBoundingClientRect().left);
  lis.forEach((li,i)=>{const s=getComputedStyle(li,'::before');const x=xs[i];const h=parseFloat(s.height)||0;const bot=fr.bottom-parseFloat(s.bottom);
   const L={left:x-1,right:x+1,top:bot-h,bottom:bot};rects.forEach((c,j)=>{if(j!==i&&Math.abs(xs[j]-x)>=2&&hit(L,c)){r.leader++;r.bad.push('leader '+i+'>'+j)}})});
 }
 out.push(r)}
return out}"""


def main(argv):
    page = argv[0]
    widths = [int(w) for w in (argv[argv.index('--widths') + 1] if '--widths' in argv else '1440,1024,820,400').split(',')]
    fails, rows = 0, []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for width in widths:
            for mode in ('light', 'dark', 'study'):
                init = "try{localStorage.setItem('ax-flat','0');localStorage.setItem('ax-study','%s')%s}catch(e){}" % (
                    '1' if mode == 'study' else '0', ";localStorage.setItem('ax-theme','dark')" if mode == 'dark' else '')
                c = b.new_context(viewport={'width': width, 'height': 1000})
                c.add_init_script(init)
                p = c.new_page()
                p.goto('file://' + page)
                p.wait_for_timeout(1500)
                p.evaluate("()=>{const s=document.createElement('style');s.textContent='*{content-visibility:visible!important}';document.head.appendChild(s);if(window.axOnset)window.axOnset()}")
                p.wait_for_timeout(400)
                for r in p.evaluate(JS):
                    r.update(width=width, mode=mode)
                    rows.append(r)
                    bad = r['text'] + r['cards'] + r['leader']
                    fails += bad > 0
                    print('%5d %-5s %-18s %-6s %s%s n=%d text=%d cards=%d leader=%d %s' % (
                        width, mode, r['brief'], r['kind'], 'list ' if r['list'] else '', 'placed' if r['js'] else '',
                        r['n'], r['text'], r['cards'], r['leader'], '; '.join(r['bad'][:4])))
                c.close()
    if '--out' in argv:
        json.dump(rows, open(argv[argv.index('--out') + 1], 'w'), indent=1)
    print('onset sweep: %d figure-mode rows, %d with a failure' % (len(rows), fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
