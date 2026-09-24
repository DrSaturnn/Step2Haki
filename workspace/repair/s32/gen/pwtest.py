import json, os, sys
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else '/mnt/user-data/outputs/s32'
os.makedirs(OUT, exist_ok=True)
URL = 'file://' + PAGE
res = {}
errs = []
def ck(name, cond, info=''):
    res[name] = bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name + ('  ' + str(info) if info else ''))

PHONE = dict(viewport={'width': 390, 'height': 844}, device_scale_factor=3, is_mobile=True, has_touch=True,
             user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')

with sync_playwright() as p:
    b = p.chromium.launch()
    # ---------------- phone
    c = b.new_context(**PHONE)
    pg = c.new_page(); pg.on('pageerror', lambda e: errs.append('phone: ' + str(e)))
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.screenshot(path=OUT + '/phone-closed.png')
    ck('phone: nav off-canvas when closed', pg.evaluate("getComputedStyle(document.getElementById('nav')).visibility") == 'hidden')
    ck('phone: bottom sheet removed', pg.evaluate("!document.getElementById('sheet') && !document.getElementById('msearch')"))
    ck('no NBME-tested controls', pg.evaluate("document.querySelectorAll('.nbmetog').length===0 && !/NBME-tested/.test(document.body.innerText)"))
    pg.tap('#mbar [data-act="index"]'); pg.wait_for_timeout(500)
    st = pg.evaluate("""()=>{var n=document.getElementById('nav'),r=n.getBoundingClientRect(),ib=document.querySelector('#mbar [data-act=index]');
      return {vis:getComputedStyle(n).visibility,left:r.left,w:r.width,h:r.height,role:n.getAttribute('role'),modal:n.getAttribute('aria-modal'),
      exp:ib.getAttribute('aria-expanded'),focusIn:n.contains(document.activeElement),bodyFixed:getComputedStyle(document.body).position,
      mainInert:document.querySelector('main').inert,order:Array.from(document.getElementById('navscroll').children).map(e=>e.id||e.className),
      fs:getComputedStyle(document.getElementById('search')).fontSize,label:n.getAttribute('aria-label')}}""")
    ck('phone: panel opens full height from left', st['vis'] == 'visible' and abs(st['left']) < 1 and st['h'] >= 840, st)
    ck('phone: aria dialog/modal/expanded + focus inside + scroll lock', st['role'] == 'dialog' and st['modal'] == 'true' and st['exp'] == 'true' and st['focusIn'] and st['bodyFixed'] == 'fixed' and st['mainInert'])
    ck('sidebar order: shelf, toggles, review, results, systems', st['order'][:5] == ['shelfpick assel', 'modes', 'rvlaunch', 'sxres', 'navlinks'], st['order'])
    ck('search input >= 16px', float(st['fs'][:-2]) >= 16, st['fs'])
    pg.screenshot(path=OUT + '/phone-sidebar.png')
    # Escape closes and returns focus
    pg.keyboard.press('Escape'); pg.wait_for_timeout(350)
    ck('phone: Escape closes, focus back on Index button', pg.evaluate("!document.body.classList.contains('navopen') && document.activeElement===document.querySelector('#mbar [data-act=index]') && document.body.style.position===''"))
    # backdrop closes
    pg.tap('#mbar [data-act="index"]'); pg.wait_for_timeout(400)
    pg.mouse.click(380, 300); pg.wait_for_timeout(350)
    ck('phone: backdrop tap closes', pg.evaluate("!document.body.classList.contains('navopen')"))
    # choosing a link closes and navigates
    pg.tap('#mbar [data-act="index"]'); pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('#navlinks a[href=\"#limp\"]').scrollIntoView({block:'center'})")
    pg.tap('#navlinks a[href="#limp"]'); pg.wait_for_timeout(900)
    lk = pg.evaluate("({open:document.body.classList.contains('navopen'),hash:location.hash,top:Math.round(document.getElementById('limp').getBoundingClientRect().top)})")
    ck('phone: link closes panel and lands on brief', not lk['open'] and lk['hash'] == '#limp' and abs(lk['top']) < 60, lk)
    # search
    pg.tap('#mbar [data-act="index"]'); pg.wait_for_timeout(400)
    pg.tap('#search'); pg.keyboard.type('pyloric stenosis'); pg.wait_for_timeout(400)
    rs = pg.evaluate("""()=>Array.from(document.querySelectorAll('#sxres a.sxhit')).map(a=>[a.getAttribute('href'),a.querySelector('.b').textContent,a.querySelector('.s')?a.querySelector('.s').textContent.slice(0,80):''])""")
    ids = [r[0] for r in rs]
    ck('search "pyloric stenosis" finds neonatal-bowel, bs-tef, bs-puv, redeye', all('#' + x in ids for x in ['neonatal-bowel', 'bs-tef', 'bs-puv', 'redeye']), rs[:8])
    ck('results replace systems list; controls hidden on phone', pg.evaluate("getComputedStyle(document.getElementById('navlinks')).display==='none' && getComputedStyle(document.getElementById('modes')).display==='none'"))
    pg.screenshot(path=OUT + '/phone-search-pyloric.png')
    first = ids[0]
    pg.tap('#sxres a.sxhit >> nth=0'); pg.wait_for_timeout(750)
    ld = pg.evaluate("""()=>{var f=document.querySelector('.sxflash');if(!f)return null;var r=f.getBoundingClientRect();
      return {open:document.body.classList.contains('navopen'),hash:location.hash,cls:f.className,top:r.top,bottom:r.bottom,inBrief:f.closest('.brief').id}}""")
    ck('tap result: panel closes, block flashes in view', ld and not ld['open'] and ld['hash'] == first and ld['inBrief'] == first[1:] and ld['top'] < 844 and ld['bottom'] > 0, ld)
    pg.screenshot(path=OUT + '/phone-result-landed.png')
    pg.wait_for_timeout(1600)
    ck('flash clears after ~2 s', pg.evaluate("!document.querySelector('.sxflash')"))
    # study mode: landing does not unmask
    pg.evaluate("document.body.classList.add('study')"); pg.wait_for_timeout(100)
    shown_before = pg.evaluate("document.querySelectorAll('.mask.shown').length")
    pg.tap('#mbar [data-act="index"]'); pg.wait_for_timeout(400)
    pg.fill('#search', 'kocher'); pg.wait_for_timeout(400)
    pg.tap('#sxres a.sxhit >> nth=0'); pg.wait_for_timeout(600)
    ck('study mode: landing unmasks nothing', pg.evaluate("document.querySelectorAll('.mask.shown').length") == shown_before)
    pg.evaluate("document.body.classList.remove('study')")
    # keyboard simulation
    pg.tap('#mbar [data-act="index"]'); pg.wait_for_timeout(400)
    pg.fill('#search', ''); pg.tap('#search'); pg.keyboard.type('pyloric'); pg.wait_for_timeout(300)
    pg.set_viewport_size({'width': 390, 'height': 480}); pg.wait_for_timeout(500)
    kb = pg.evaluate("""()=>{var s=document.getElementById('search').getBoundingClientRect(),n=document.getElementById('nav').getBoundingClientRect(),a=document.querySelector('#sxres a.sxhit');var ar=a?a.getBoundingClientRect():null;
      return {vvh:window.visualViewport.height,navH:n.height,searchBottom:s.bottom,firstResultBottom:ar?ar.bottom:null}}""")
    ck('keyboard sim: panel follows visualViewport, field and first result visible', kb['navH'] <= kb['vvh'] + 1 and kb['searchBottom'] < 480 and kb['firstResultBottom'] and kb['firstResultBottom'] < 480, kb)
    pg.screenshot(path=OUT + '/phone-keyboard-sim.png')
    pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(300)
    # Board-style only
    pg.fill('#search', ''); pg.wait_for_timeout(300)
    pg.evaluate("history.replaceState(null,'',location.pathname+location.search); window.axApplyShelf()")
    pg.tap('#modes .bsonly'); pg.wait_for_timeout(300)
    bo = pg.evaluate("""()=>{var vis=Array.from(document.querySelectorAll('.brief')).filter(b=>b.style.display!=='none');
      return {n:vis.length,allBs:vis.every(b=>b.classList.contains('bs')&&b.dataset.src!=='aquifer'),meta:document.querySelector('.masthead .meta').textContent,
      pressed:document.querySelector('#modes .bsonly').getAttribute('aria-pressed'),ls:localStorage.getItem('ax-bsonly'),
      navLinks:Array.from(document.querySelectorAll('#navlinks a')).filter(a=>a.style.display!=='none').length,
      counts:Array.from(document.querySelectorAll('#navlinks .sect')).filter(s=>s.style.display!=='none').map(s=>+s.querySelector('.count').textContent).reduce((x,y)=>x+y,0)}}""")
    ck('Board-style only shows only board-style briefs; counts agree', bo['allBs'] and bo['n'] > 0 and bo['n'] == bo['navLinks'] == bo['counts'] and bo['meta'].startswith('0 topics') and bo['pressed'] == 'true' and bo['ls'] == '1', bo)
    pg.evaluate("document.getElementById('navscroll').scrollTop=0")
    pg.screenshot(path=OUT + '/phone-boardstyle-on.png')
    pg.reload(); pg.wait_for_timeout(900)
    ck('Board-style only persists across reload', pg.evaluate("document.querySelector('#modes .bsonly').getAttribute('aria-pressed')==='true' && Array.from(document.querySelectorAll('.brief')).filter(b=>b.style.display!=='none').every(b=>b.classList.contains('bs'))"))
    pg.evaluate("document.querySelector('#modes .bsonly').click()")
    ck('Board-style off restores all 207', pg.evaluate("Array.from(document.querySelectorAll('.brief')).filter(b=>b.style.display!=='none').length") == 207)
    c.close()

    # ---------------- desktop
    c = b.new_context(viewport={'width': 1440, 'height': 900})
    pg = c.new_page(); pg.on('pageerror', lambda e: errs.append('desktop: ' + str(e)))
    pg.goto(URL); pg.wait_for_timeout(900)
    d = pg.evaluate("({mbar:getComputedStyle(document.getElementById('mbar')).display,nav:getComputedStyle(document.getElementById('nav')).visibility,close:getComputedStyle(document.querySelector('.navclose')).display,mcq:document.querySelectorAll('.mcq').length,ax:window.__axCheck})")
    ck('desktop: fixed sidebar, no phone chrome', d['mbar'] == 'none' and d['nav'] == 'visible' and d['close'] == 'none', d)
    ck('MCQ generation intact (2014)', d['mcq'] == 2014 and d['ax']['mcq'] == 2014)
    pg.screenshot(path=OUT + '/desktop-sidebar.png')
    pg.click('#search'); pg.keyboard.type('pyloric stenosis'); pg.wait_for_timeout(400)
    dr = pg.evaluate("Array.from(document.querySelectorAll('#sxres a.sxhit')).map(a=>a.getAttribute('href'))")
    ck('desktop: same result list', all('#' + x in dr for x in ['neonatal-bowel', 'bs-tef', 'bs-puv', 'redeye']) and pg.evaluate("getComputedStyle(document.getElementById('modes')).display!=='none'"), dr[:6])
    pg.screenshot(path=OUT + '/desktop-search.png')
    pg.keyboard.press('Enter'); pg.wait_for_timeout(800)
    ck('desktop: Enter opens first result', pg.evaluate("location.hash") == dr[0])
    # other shelves line
    pg.select_option('#nav .shelfsel', 'fm'); pg.wait_for_timeout(300)
    more = pg.evaluate("(document.querySelector('#sxres .sxmore')||{}).textContent||''")
    stat = pg.evaluate("document.querySelector('#sxres .sxstat').textContent")
    ck('shelf respected + "N more in other shelves"', 'more in other shelves' in more or 'No matches' in stat, [stat, more])
    if more:
        pg.click('#sxres .sxmore'); pg.wait_for_timeout(300)
        ck('"more" switches shelf to Step 2 and URL', pg.evaluate("window.axShelf()==='step2' && /shelf=step2/.test(location.search)"))
    pg.fill('#search', 'zzqxnomatch'); pg.wait_for_timeout(300)
    ck('empty state', pg.evaluate("document.querySelector('#sxres .sxstat').textContent") == 'No matches in Step 2.')
    pg.fill('#search', 'ihps'); pg.wait_for_timeout(300)
    ck('alias IHPS -> pyloric stenosis', '#neonatal-bowel' in pg.evaluate("Array.from(document.querySelectorAll('#sxres a.sxhit')).map(a=>a.getAttribute('href'))"))
    pg.fill('#search', 'stenosis pyloric'); pg.wait_for_timeout(300)
    ck('any word order', '#bs-tef' in pg.evaluate("Array.from(document.querySelectorAll('#sxres a.sxhit')).map(a=>a.getAttribute('href'))"))
    pg.fill('#search', 'alpha fetoprotein'); pg.wait_for_timeout(300)
    ck('page acronym pair (AFP)', pg.evaluate("window.__axSearch.search('afp').hits.length") > 0 and pg.evaluate("window.__axSearch.search('alpha fetoprotein').hits.length") >= pg.evaluate("window.__axSearch.search('afp').hits.length") - 0)
    pg.fill('#search', '')
    # shelf URL, deep link pin, review, flat
    pg.goto(URL + '?shelf=peds#bs-tef'); pg.wait_for_timeout(1000)
    dl = pg.evaluate("({s:window.axShelf(),top:Math.round(document.getElementById('bs-tef').getBoundingClientRect().top),vis:document.getElementById('bs-tef').style.display})")
    ck('?shelf=peds + #deep link', dl['s'] == 'peds' and dl['vis'] == '' and abs(dl['top']) < 80, dl)
    pg.goto(URL + '?shelf=fm#bs-tef'); pg.wait_for_timeout(1000)
    ck('deep link pins an off-shelf brief', pg.evaluate("document.getElementById('bs-tef').classList.contains('pinned') && document.getElementById('bs-tef').style.display===''"))
    pg.goto(URL + '?shelf=step2'); pg.wait_for_timeout(900)
    ck('review card in sidebar under switches', pg.evaluate("document.getElementById('modes').nextElementSibling.id==='rvlaunch'"))
    ck('review module loaded', pg.evaluate("!!window.__axRev && typeof window.__axRev.pool==='function' && window.__axRev.pool().length>0"))
    pg.click('#modes .flatt'); pg.wait_for_timeout(200)
    ck('flat theme toggles', pg.evaluate("document.body.classList.contains('flat') && localStorage.getItem('ax-flat')==='1'"))
    pg.click('#modes .flatt')
    pg.click('#modes .study'); pg.wait_for_timeout(200)
    ck('study mode masks', pg.evaluate("document.body.classList.contains('study') && getComputedStyle(document.querySelector('.mask-region')).filter.indexOf('blur')>-1"))
    pg.click('#modes .study')
    c.close()

    # ---------------- timings, phone profile with 4x CPU throttling
    c = b.new_context(**PHONE)
    pg = c.new_page()
    cdp = c.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
    pg.goto(URL); pg.wait_for_function("window.__axSearch && window.__axSearch.stats().built", timeout=30000)
    stt = pg.evaluate("window.__axSearch.stats()")
    q = pg.evaluate("""()=>{var o={};['pyloric stenosis','kawasaki','ihps','a','chest pain fever'].forEach(function(q){var t=performance.now();for(var i=0;i<5;i++)window.__axSearch.search(q);o[q]=Math.round((performance.now()-t)/5*10)/10;});
      document.getElementById('search').value='pyloric stenosis';var t2=performance.now();window.__axSearch.render();o.render_pyloric=Math.round((performance.now()-t2)*10)/10;return o;}""")
    print('TIMING 4x throttle: build %s ms work (%s ms wall, %s idle slices) over %s briefs, %s synonym groups; query ms %s' % (stt['buildMs'], stt.get('wallMs'), stt.get('slices'), stt['briefs'], stt['groups'], json.dumps(q)))
    res['timing'] = {'build': stt, 'query': q}
    c.close()
    b.close()
print('page errors:', errs)
print('SUMMARY', sum(1 for k, v in res.items() if v is True), 'pass /', sum(1 for k, v in res.items() if isinstance(v, bool)))
