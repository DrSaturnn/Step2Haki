/* s136: Review in the status bar (Jonathan 2026-10-14: "reinvent the brief review and login with pin using the same apple
   ios 27 stylized look and put it on the top status bar"; "very quick to jump into the 3 most recommended reviews rather
   than 5"; "Do not include the total briefs count"). A Review pill in the glass toolbar (desktop) and the phone bar's
   Review button open one glass sheet: who is studying (with a passcode pad when the name has a PIN), the 3 briefs the
   scheduler recommends next, Start review and Quiz me instead. The scheduler, sync and PIN check are the page's own
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
    var a = pill && pill.offsetParent ? pill.getBoundingClientRect() : null, w = sheet.offsetWidth || 360;
    var vw = document.documentElement.clientWidth || window.innerWidth;
    var left = a ? Math.min(a.right - w, vw - w - 12) : vw - w - 16, top = a ? a.bottom + 10 : 72;
    sheet.style.left = Math.max(12, left) + 'px'; sheet.style.top = top + 'px';
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
