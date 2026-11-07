/* Site layout. Presentation only; never adds or removes brief text.
   1. Accent setting: a reader choice under the theme switches, stored per viewer; Slate default.
      Dark theme: a switch beside Flat theme, stored per viewer, light by default.
   2. Desktop hovers: open on pointer enter, close on leave, stay open once clicked (a second click closes).
   3. Desktop glass toolbar: the current section's number and name, Read and Recall, open or close every panel.
   4. Sidebar systems fold and unfold; the system holding the current brief opens itself. */
(function(){
  "use strict";
  var ACC = [['slate','Slate','#3B5B8C'],['indigo','Indigo','#4A48C6'],['purple','Purple','#544AC4'],['navy','Navy','#1E3A8A'],
             ['ocean','Ocean','#1D6A8C'],['plum','Plum','#7A3B8F'],['rose','Rose','#AA2E66'],['graphite','Graphite','#4A5060']];
  var KEY = 'ax-accent';
  function load(){ return AX.settings.get('accent') || 'slate'; }
  function save(k){ AX.settings.set('accent', k); }
  function valid(k){ for(var i = 0; i < ACC.length; i++) if(ACC[i][0] === k) return ACC[i]; return null; }
  var root = document.documentElement;

  /* ---------- 1. accent ----------
     Slate needs nothing (the tokens' default). Another choice is set on the page's regions nearest first, a few per
     frame, then on the root, the same way the flat and study switches restyle (s92): one root-wide change restyled
     every brief at once. */
  var cur = valid(load()) ? load() : 'slate';
  var THEME = 'ax-theme', dark = false, tint = false;
  var tv = AX.settings.get('theme'); dark = tv === 'dark' || tv === 'tinted'; tint = tv === 'tinted';
  if(cur !== 'slate') root.setAttribute('data-axa', cur);
  if(dark) root.setAttribute('data-theme', 'dark');
  if(tint) root.setAttribute('data-glass', 'tinted');   // tinted glass: dark plus accent-tinted translucent surfaces
  /* Each region carries both attributes while a switch walks the page, so the dark accent rule (which needs both on
     one element or the theme on an ancestor) always matches. */
  function mark(c){
    if(cur === 'slate') c.removeAttribute('data-axa'); else c.setAttribute('data-axa', cur);
    if(dark) c.setAttribute('data-theme', 'dark'); else c.removeAttribute('data-theme');
    if(tint) c.setAttribute('data-glass', 'tinted'); else c.removeAttribute('data-glass');
  }
  function markRoot(){ mark(root); }
  var queue = [], busy = false;
  function regions(){
    var out = [];
    (function walk(el){
      for(var c = el.firstElementChild; c; c = c.nextElementSibling){
        if(c.tagName === 'SCRIPT' || c.tagName === 'STYLE') continue;
        if(c.classList.contains('brief') || !c.querySelector('.brief')) out.push(c); else walk(c);
      }
    })(document.body);
    return out;
  }
  function dist(c){
    var r = c.getBoundingClientRect(), h = window.innerHeight || 800;
    if(!r.width && !r.height) return 1e9;
    return r.bottom < 0 ? -r.bottom : (r.top > h ? r.top - h : 0);
  }
  function step(){
    var n = 0;
    while(queue.length && n < 4){ mark(queue.shift()); n++; }
    if(queue.length){ requestAnimationFrame(step); return; }
    markRoot(); busy = false;
  }
  function walkAll(){
    var rs = regions(), near = [], far = [];
    rs.forEach(function(c){ (dist(c) === 0 ? near : far).push(c); });
    near.forEach(mark);
    far.sort(function(a, b){ return dist(a) - dist(b); });
    queue = far;
    if(!busy){ busy = true; requestAnimationFrame(step); }
  }
  function setAccent(k){
    if(!valid(k) || k === cur) return;
    cur = k; save(k); paintSetting(); walkAll();
  }
  function setTheme(d, t){
    t = d && t;
    if(d === dark && t === tint) return;
    dark = d; tint = t; AX.settings.set('theme', t ? 'tinted' : (d ? 'dark' : 'light'));
    paintSetting(); walkAll();
  }
  function setDark(on){ setTheme(on, on && tint); }
  var box = null, darkBtn = null, tintBtn = null;
  function paintSetting(){
    if(!box) return;
    box.querySelectorAll('.axsw').forEach(function(b){ var on = b.getAttribute('data-k') === cur; b.setAttribute('aria-checked', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; });
    var a = valid(cur); box.querySelector('.axan').textContent = a ? a[1] : '';
    if(darkBtn) darkBtn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    if(tintBtn) tintBtn.setAttribute('aria-pressed', tint ? 'true' : 'false');
  }
  function setting(){
    var modes = document.getElementById('modes'); if(!modes || modes.querySelector('.axacc')) return;
    darkBtn = document.createElement('button'); darkBtn.type = 'button'; darkBtn.className = 'dark';
    darkBtn.innerHTML = '<span class="track"><span class="knob"></span></span><span class="nm">DARK THEME</span>';
    var flat = modes.querySelector('.flatt'); if(flat) flat.after(darkBtn); else modes.appendChild(darkBtn);
    darkBtn.addEventListener('click', function(){ setDark(!dark); });
    tintBtn = document.createElement('button'); tintBtn.type = 'button'; tintBtn.className = 'dark tint';
    tintBtn.innerHTML = '<span class="track"><span class="knob"></span></span><span class="nm">TINTED GLASS</span>';
    darkBtn.after(tintBtn);
    tintBtn.addEventListener('click', function(){ setTheme(true, !tint); });
    box = document.createElement('div'); box.className = 'axacc'; box.setAttribute('role', 'radiogroup'); box.setAttribute('aria-label', 'Accent color');
    var h = '<span class="nm">ACCENT</span>';
    ACC.forEach(function(a){ h += '<button type="button" class="axsw" role="radio" data-k="' + a[0] + '" title="' + a[1] + '" aria-label="' + a[1] + '" style="--sw:' + a[2] + '"></button>'; });
    box.innerHTML = h + '<span class="axan"></span>';
    modes.appendChild(box);
    box.addEventListener('click', function(e){ var b = e.target.closest('.axsw'); if(b) setAccent(b.getAttribute('data-k')); });
    box.addEventListener('keydown', function(e){
      var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : (e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0);
      if(!d) return; e.preventDefault();
      var i = 0; ACC.forEach(function(a, j){ if(a[0] === cur) i = j; });
      var k = ACC[(i + d + ACC.length) % ACC.length][0]; setAccent(k);
      var nb = box.querySelector('[data-k="' + k + '"]'); if(nb) nb.focus();
    });
    paintSetting();
  }

  /* ---------- 2. hovers stay open once clicked (desktop) ----------
     The spine script opens a card on pointer enter and closes it on leave; a click on its button closed it. Here a
     click on an open, unpinned card pins it instead; a click on a pinned card's button closes it as before. */
  var fine = window.matchMedia && window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var pinned = null;
  function openCard(){ return document.querySelector('body > .sp-card'); }
  if(fine){
    window.addEventListener('click', function(e){
      var p = e.target.closest && e.target.closest('.sp-pop');
      if(!p){ if(pinned && !(e.target.closest && e.target.closest('.sp-card'))) pinned = null; return; }
      var c = openCard();
      if(c && p.getAttribute('aria-expanded') === 'true' && pinned !== c){ pinned = c; e.preventDefault(); e.stopPropagation(); return; }
      if(!c || p.getAttribute('aria-expanded') !== 'true'){ setTimeout(function(){ pinned = openCard(); }, 0); return; }
      pinned = null;
    }, true);
    function keep(e){ var c = openCard(); if(pinned && c === pinned && (e.target === c || (e.target.closest && e.target.closest('.sp-pop') && e.target.closest('.sp-pop').getAttribute('aria-expanded') === 'true'))) e.stopPropagation(); }
    window.addEventListener('mouseout', keep, true);
    window.addEventListener('mouseleave', keep, true);
    window.addEventListener('mouseover', function(e){
      // pointing at another hover while one is pinned opens that one and releases the pin
      var p = e.target.closest && e.target.closest('.sp-pop');
      if(p && pinned && p.getAttribute('aria-expanded') !== 'true') pinned = null;
    }, true);
  }

  /* ---------- 3. glass toolbar (desktop) ---------- */
  var WIDE = window.matchMedia ? window.matchMedia('(min-width:1101px)') : { matches: true };
  var bar = null, raf = 0;
  function currentBrief(){
    var main = document.querySelector('main'); if(!main) return null;
    var r = main.getBoundingClientRect(), x = Math.max(r.left + 40, Math.min(r.left + r.width / 2, window.innerWidth - 40));
    var el = document.elementFromPoint(x, Math.min(140, window.innerHeight / 3));
    return el && el.closest ? el.closest('main .brief') : null;
  }
  function panels(b){ return b ? Array.prototype.slice.call(b.querySelectorAll('details')) : []; }
  function paintBar(){
    raf = 0; if(!bar || !WIDE.matches) return;
    var b = currentBrief(), n = '', label = '', practice = false;
    if(b){
      var a = b.querySelector('.bb-rl a.cur') || (window.axRailOf && window.axRailOf(b) ? window.axRailOf(b).querySelector('.bb-rl a.cur') : null);   /* the rail may sit in the sidebar */
      if(a){
        var nb = a.querySelector('b'); n = nb ? nb.textContent.trim() : '';
        label = (a.textContent || '').replace(n, '').trim(); practice = !n;
      }
      if(!label){ var h = b.querySelector('h4'); label = h ? h.textContent.trim() : ''; }
    }
    var cn = bar.querySelector('.axcn'), cl = bar.querySelector('.axcl');
    cn.textContent = n; cn.hidden = !n && !practice; cn.classList.toggle('p', practice);
    if(practice) cn.textContent = 'P';
    cl.textContent = label || 'Step2Haki';
    var bn = bar.querySelector('.axbn'), hh = b ? b.querySelector('h4') : null, nm = hh ? hh.textContent.trim() : '';   
    bn.textContent = nm; bn.title = nm; bn.hidden = !nm || nm === label;
    var ps = panels(b), all = bar.querySelector('.axall');
    all.hidden = !ps.length;
    var seps = bar.querySelectorAll('.axsep'); if(seps[1]) seps[1].hidden = !ps.length;
    all.textContent = ps.length && ps.every(function(d){ return d.open; }) ? 'Collapse all' : 'Expand all';
    bar.classList.toggle('st', document.body.classList.contains('study'));
    bar.querySelector('[data-m="read"]').setAttribute('aria-pressed', document.body.classList.contains('study') ? 'false' : 'true');
    bar.querySelector('[data-m="study"]').setAttribute('aria-pressed', document.body.classList.contains('study') ? 'true' : 'false');
  }
  var late = 0;
  function kick(){
    if(!raf) raf = requestAnimationFrame(paintBar);
    // the section rail marks its current link in its own frame after a scroll; paint once more after it settles
    clearTimeout(late); late = setTimeout(paintBar, 160);
  }
  function toolbar(){
    if(document.getElementById('axbar')) return;
    var edge = document.createElement('div'); edge.id = 'axedge'; edge.setAttribute('aria-hidden', 'true');
    bar = document.createElement('div'); bar.id = 'axbar'; bar.setAttribute('role', 'toolbar'); bar.setAttribute('aria-label', 'Brief controls');
    bar.innerHTML = '<span class="axcur" aria-live="polite"><span class="axbn"></span><span class="axcn"></span><span class="axcl"></span></span><span class="axsep"></span>' +
      '<div class="axseg"><span class="axth" aria-hidden="true"></span><button type="button" data-m="read">Read</button><button type="button" data-m="study">Recall</button></div>' +
      '<span class="axsep"></span><button type="button" class="axall">Expand all</button>';
    document.body.appendChild(edge); document.body.appendChild(bar);
    bar.addEventListener('click', function(e){
      var t = e.target.closest('button'); if(!t) return;
      var m = t.getAttribute('data-m');
      if(m){
        var want = m === 'study';
        if(document.body.classList.contains('study') !== want){
          // one code path for the study switch: press the sidebar's own control
          var s = document.querySelector('#modes .study');
          if(s) s.click(); else { document.body.classList.toggle('study', want); AX.settings.set('study', want ? '1' : '0'); }
        }
      } else if(t.classList.contains('axall')){
        var ps = panels(currentBrief()), open = !ps.every(function(d){ return d.open; });
        ps.forEach(function(d){ d.open = open; });
      }
      kick();
    });
    window.addEventListener('scroll', kick, { passive: true });
    window.addEventListener('resize', kick);
    document.addEventListener('toggle', kick, true);
    new MutationObserver(kick).observe(document.body, { attributes: true, attributeFilter: ['class'] });
    kick();
  }

  /* ---------- 4. sidebar systems fold ---------- */
  function groups(){
    var host = document.getElementById('navlinks'), out = [], g = null;
    if(!host) return out;
    Array.prototype.slice.call(host.children).forEach(function(el){
      if(el.classList.contains('sect')){ g = { head: el, items: [] }; out.push(g); }
      else if(g) g.items.push(el);
    });
    return out;
  }
  function setOpen(g, on){
    g.head.setAttribute('aria-expanded', on ? 'true' : 'false');
    g.items.forEach(function(el){ el.classList.toggle('axsx-c', !on); });
  }
  function fold(){
    var nav = document.getElementById('nav'), gs = groups(); if(!nav || !gs.length) return;
    nav.classList.add('axsx');
    gs.forEach(function(g){
      g.head.setAttribute('role', 'button'); g.head.tabIndex = 0;
      var has = g.items.some(function(el){ return el.classList.contains('active'); });
      setOpen(g, has);
      function flip(){ setOpen(g, g.head.getAttribute('aria-expanded') !== 'true'); }
      g.head.addEventListener('click', flip);
      g.head.addEventListener('keydown', function(e){ if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); flip(); } });
    });
    // the current brief's system opens itself as the reader scrolls into it
    new MutationObserver(function(ms){
      ms.forEach(function(m){
        var a = m.target; if(a.tagName !== 'A' || !a.classList.contains('active') || !a.classList.contains('axsx-c')) return;
        gs.forEach(function(g){ if(g.items.indexOf(a) >= 0) setOpen(g, true); });
      });
    }).observe(document.getElementById('navlinks'), { subtree: true, attributes: true, attributeFilter: ['class'] });
  }

  /* 5. Mnemonic key column fits its widest key, so a long key does not overrun the 28 px column on desktop or push
     phone text into a narrow column. Only a list with a key wider than one letter changes. */
  function fitMnem(root){
    (root && root.querySelectorAll ? root : document).querySelectorAll('dl.rows.mnem').forEach(function(dl){
      if(dl.classList.contains('mn-wide')) return;
      var w = 0, n = 0;
      dl.querySelectorAll('dt b.mn').forEach(function(b){ w = Math.max(w, b.scrollWidth || 0); n = Math.max(n, b.textContent.trim().length); });
      var keyOnly = Array.prototype.every.call(dl.querySelectorAll(':scope > dt'), function(dt){
        var b = dt.querySelector('b.mn'); return b && dt.textContent.trim() === b.textContent.trim(); });
      if(keyOnly) dl.classList.add('mn-key');   // phone: the key column shrinks to the key, the text gets the rest
      if(n < 2) return;
      w = Math.max(w, n * 14);
      dl.style.setProperty('--mnw', (Math.ceil(w) + 16) + 'px');
      dl.classList.add('mn-wide');
    });
  }

  function init(){ setting(); toolbar(); fold(); fitMnem(); AX.brief.each('glance-mnem', fitMnem); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

/* Review in the status bar. A Review pill in the glass toolbar (desktop) and the phone bar's Review button open one
   glass sheet: who is studying (with a passcode pad when the name has a PIN), the 3 briefs the scheduler recommends
   next, Start review and Quiz me instead; no total briefs count. The scheduler, sync and PIN check are the page's own
   (window.axRv, exposed by the review script); this file is presentation only. */
(function(){
  "use strict";
  var sheet = null, pill = null, view = 'auto', pinFor = null, pinVal = '', busy = false, lastFocus = null;
  function R(){ return window.axRv || null; }
  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function phone(){ return window.matchMedia('(max-width:900px)').matches; }

  function paintPill(){
    var r = R(); if(!pill || !r) return;
    var id = r.current(), d = id ? r.due() : 0;
    pill.querySelector('.av').textContent = id ? r.initials(r.nameOf(id)) : '';
    pill.classList.toggle('anon', !id);
    var bd = pill.querySelector('.bd'); bd.textContent = d; bd.hidden = !(id && d);
    pill.setAttribute('aria-label', id ? ('Review: ' + r.nameOf(id) + (d ? ', ' + d + ' due' : '')) : 'Review: sign in');
  }

  var KIND = {due: 'Due', fresh: 'New', later: 'Ahead'};
  function signedInHTML(r, id){
    var pick = r.pick(), d = r.due();
    var h = '<header class="rvh"><span class="av">' + esc(r.initials(r.nameOf(id))) + '</span><div class="who"><b>' + esc(r.nameOf(id)) + '</b>' +
            '<small>' + (d ? (d === 1 ? '1 review due today' : d + ' reviews due today') : 'Nothing due today') + '</small></div>' +
            '<button type="button" class="rvx" data-a="close" aria-label="Close"></button></header>';
    if(pick.length){
      h += '<p class="rvk">Up next</p><ol class="rvl">';
      pick.forEach(function(p, i){
        h += '<li><span class="n">' + (i + 1) + '</span><span class="t">' + esc(p.title) + '</span><span class="tg ' + p.kind + '">' + KIND[p.kind] + '</span></li>';
      });
      h += '</ol><button type="button" class="rvgo" data-a="start">Start review</button>' +
           '<button type="button" class="rvalt" data-a="quiz">Quiz me instead</button>';
    } else {
      h += '<p class="rvnote">No briefs on this shelf yet.</p>';
    }
    h += '<footer class="rvf"><button type="button" data-a="switch">Switch person</button><button type="button" data-a="more">Profile and backup</button></footer>';
    return h;
  }
  function whoHTML(r){
    var ps = r.people();
    var h = '<header class="rvh"><div class="who"><b>Who is studying?</b><small>Progress is saved under your name.</small></div>' +
            '<button type="button" class="rvx" data-a="close" aria-label="Close"></button></header><div class="rvpp">';
    ps.forEach(function(p){
      h += '<button type="button" class="pp" data-a="use" data-id="' + esc(p.id) + '"><span class="av">' + esc(r.initials(p.name)) + '</span><span class="nm">' + esc(p.name) + '</span></button>';
    });
    h += '<button type="button" class="pp add" data-a="new"><span class="av">+</span><span class="nm">New</span></button></div>';
    if(view === 'new'){
      h += '<div class="rvform"><input type="text" id="axrvname" maxlength="28" autocomplete="off" placeholder="Your name or alias" aria-label="Your name or alias">' +
           '<button type="button" class="rvgo" data-a="add">Continue</button></div>';
    }
    h += '<footer class="rvf"><button type="button" data-a="more">Import a code</button></footer>';
    return h;
  }
  var LET = ['', '', 'ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQRS', 'TUV', 'WXYZ'];
  function pinHTML(r){
    var n = Math.max(4, pinVal.length), dots = '';
    for(var i = 0; i < n; i++) dots += '<i' + (i < pinVal.length ? ' class="on"' : '') + '></i>';
    var h = '<header class="rvh center"><span class="av">' + esc(r.initials(r.nameOf(pinFor))) + '</span><div class="who"><b>Enter PIN</b>' +
            '<small>for ' + esc(r.nameOf(pinFor)) + '</small></div></header>' +
            '<div class="rvdots" aria-label="' + pinVal.length + ' digits entered">' + dots + '</div><p class="rverr" aria-live="assertive"></p><div class="rvpad">';
    [1, 2, 3, 4, 5, 6, 7, 8, 9].forEach(function(k){ h += '<button type="button" class="k" data-k="' + k + '"><b>' + k + '</b><small>' + LET[k] + '</small></button>'; });
    h += '<button type="button" class="k txt" data-a="cancel">Cancel</button><button type="button" class="k" data-k="0"><b>0</b><small>&nbsp;</small></button>' +
         '<button type="button" class="k txt" data-a="del" aria-label="Delete">&#9003;</button></div>' +
         '<button type="button" class="rvgo" data-a="pinok"' + (pinVal.length ? '' : ' disabled') + '>OK</button>';
    return h;
  }
  function render(){
    var r = R(); if(!sheet || !r) return;
    var id = r.current(), h;
    if(pinFor) h = pinHTML(r);
    else if(!id || view === 'who' || view === 'new') h = whoHTML(r);
    else h = signedInHTML(r, id);
    sheet.querySelector('.axrv-in').innerHTML = h;
    sheet.classList.toggle('pinv', !!pinFor);
    place(); paintPill();
    var f = sheet.querySelector('#axrvname') || sheet.querySelector('.rvgo:not([disabled])') || sheet.querySelector('.pp');
    if(f && !phone()) try { f.focus({preventScroll: true}); } catch(e){}
  }
  function place(){
    if(!sheet || phone()){ if(sheet){ sheet.style.top = ''; sheet.style.left = ''; } return; }
    var z = parseFloat(getComputedStyle(document.documentElement).zoom) || 1;   // zoomed px in, CSS px out
    var a = pill && pill.offsetParent ? pill.getBoundingClientRect() : null, w = (sheet.offsetWidth || 360) * z;
    var vw = document.documentElement.clientWidth || window.innerWidth;
    var left = a ? Math.min(a.right - w, vw - w - 12) : vw - w - 16, top = a ? a.bottom + 10 : 72;
    sheet.style.left = Math.max(12, left) / z + 'px'; sheet.style.top = top / z + 'px';
  }
  function open(from){
    var r = R(); if(!r) return;
    build(); lastFocus = from || document.activeElement;
    view = 'auto'; pinFor = null; pinVal = '';
    sheet.hidden = false; document.body.classList.add('axrv-open');
    if(pill) pill.setAttribute('aria-expanded', 'true');
    render();
    r.refresh(function(){ if(!sheet.hidden && !pinFor && view === 'auto') render(); });
  }
  function close(){
    if(!sheet || sheet.hidden) return;
    var r = R();
    if(pinFor && r){ r.signOut(); }          // a name with a PIN is not taken without it
    pinFor = null; pinVal = ''; view = 'auto';
    sheet.hidden = true; document.body.classList.remove('axrv-open');
    if(pill) pill.setAttribute('aria-expanded', 'false');
    paintPill();
    if(lastFocus) try { lastFocus.focus({preventScroll: true}); } catch(e){}
  }
  function shake(msg){
    var e = sheet.querySelector('.rverr'); if(e) e.textContent = msg;
    var d = sheet.querySelector('.rvdots'); if(!d) return;
    d.classList.remove('shake'); void d.offsetWidth; d.classList.add('shake');
  }
  function act(a, b){
    var r = R(); if(!r || busy) return;
    if(a === 'close') return close();
    if(a === 'switch'){ view = 'who'; return render(); }
    if(a === 'new'){ view = 'new'; return render(); }
    if(a === 'more'){ var anchor = pill && pill.offsetParent ? pill : document.querySelector('#mbar [data-act="review"]'); close(); return r.open(anchor); }
    if(a === 'start' || a === 'quiz'){ close(); return a === 'start' ? r.start() : r.quiz(); }
    if(a === 'add'){
      var v = sheet.querySelector('#axrvname'); if(!v || !v.value.trim()){ if(v) v.focus(); return; }
      r.add(v.value); view = 'auto'; return render();
    }
    if(a === 'use'){
      var pid = b.getAttribute('data-id'); busy = true; b.classList.add('wait');
      r.use(pid, function(){
        busy = false; view = 'auto';
        if(r.needsPin(pid)){ pinFor = pid; pinVal = ''; }
        render();
      });
      return;
    }
    if(a === 'cancel'){ r.signOut(); pinFor = null; pinVal = ''; view = 'who'; return render(); }
    if(a === 'del'){ pinVal = pinVal.slice(0, -1); return render(); }
    if(a === 'pinok'){
      if(!pinVal) return;
      busy = true; var pid2 = pinFor, val = pinVal;
      sheet.querySelector('.rvgo').textContent = 'Checking';
      r.tryPin(pid2, val, function(ok){
        busy = false;
        if(ok === true){ pinFor = null; pinVal = ''; view = 'auto'; render(); }
        else { pinVal = ''; render(); shake(ok === false ? 'Wrong PIN. Try again.' : 'Could not reach sync. Try again.'); }
      });
    }
  }
  function key(k){
    if(!pinFor || busy || pinVal.length >= 12) return;
    pinVal += k; render();
  }
  function build(){
    if(sheet) return;
    sheet = document.createElement('div'); sheet.id = 'axrv'; sheet.hidden = true;
    sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'false'); sheet.setAttribute('aria-label', 'Review');
    sheet.innerHTML = '<div class="axrv-grab" aria-hidden="true"></div><div class="axrv-in"></div>';
    document.body.appendChild(sheet);
    sheet.addEventListener('click', function(e){
      var b = e.target.closest('button'); if(!b) return;
      if(b.hasAttribute('data-k')) return key(b.getAttribute('data-k'));
      var a = b.getAttribute('data-a'); if(a) act(a, b);
    });
    sheet.addEventListener('keydown', function(e){
      if(e.key === 'Enter' && e.target.id === 'axrvname'){ e.preventDefault(); act('add'); }
    });
    document.addEventListener('keydown', function(e){
      if(!sheet || sheet.hidden) return;
      if(e.key === 'Escape'){ e.stopPropagation(); close(); return; }
      if(pinFor && /^[0-9]$/.test(e.key)){ e.preventDefault(); key(e.key); }
      else if(pinFor && e.key === 'Backspace'){ e.preventDefault(); act('del'); }
      else if(pinFor && e.key === 'Enter'){ e.preventDefault(); act('pinok'); }
    }, true);
    document.addEventListener('mousedown', function(e){
      if(!sheet || sheet.hidden) return;
      if(sheet.contains(e.target) || (pill && pill.contains(e.target)) || (e.target.closest && e.target.closest('#mbar'))) return;
      close();
    });
    window.addEventListener('resize', function(){ if(sheet && !sheet.hidden) place(); });
  }
  function mountPill(){
    var bar = document.getElementById('axbar'); if(!bar || bar.querySelector('.axrvb')) return !!bar;
    var sep = document.createElement('span'); sep.className = 'axsep';
    pill = document.createElement('button'); pill.type = 'button'; pill.className = 'axrvb';
    pill.setAttribute('aria-haspopup', 'dialog'); pill.setAttribute('aria-expanded', 'false'); pill.setAttribute('aria-controls', 'axrv');
    pill.innerHTML = '<span class="av" aria-hidden="true"></span><span class="lb">Review</span><span class="bd" hidden></span>';
    bar.appendChild(sep); bar.appendChild(pill);
    pill.addEventListener('click', function(){ if(sheet && !sheet.hidden) close(); else open(pill); });
    paintPill();
    return true;
  }
  function init(){
    // the phone bar's Review button opens the same sheet (capture: before the page's own panel handler)
    document.addEventListener('click', function(e){
      var b = e.target.closest && e.target.closest('#mbar [data-act="review"]'); if(!b || !R()) return;
      e.preventDefault(); e.stopImmediatePropagation();
      if(sheet && !sheet.hidden) close(); else open(b);
    }, true);
    var tries = 0;
    (function wait(){
      var ok = R() && mountPill();
      if(!ok && ++tries < 60) setTimeout(wait, 250);
      else { paintPill(); setInterval(paintPill, 30000); }
    })();
    document.addEventListener('visibilitychange', function(){ if(!document.hidden) paintPill(); });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
