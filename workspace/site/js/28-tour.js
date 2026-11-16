/* The welcome card. It opens once for a reader who arrives at the starting screen with no saved reading or review data,
   and again whenever tour:open is emitted. Every way out (the close button, Skip, the primary button, Esc, a tap on the
   backdrop, a swipe down on the phone sheet) records the card as seen in the reader settings (tour).
   While the card is open the rest of the page is inert and focus stays inside the card.
   Events: listens to tour:open. */
return (function(){
'use strict';
var VERSION = '1';
var NARROW = window.matchMedia('(max-width:1100px)');
var B = document.body;
var COPY = {
  title: 'Welcome to Step2Haki',
  line: 'Board briefs for Step 2 CK and the shelf exams. Each brief teaches one decision the exam tests, then checks it with practice questions.',
  rows: ['Pick a shelf.', 'Find a topic by system or by complaint.', 'Read the steps in order, then answer the questions.'],
  note: 'Progress saves in this browser. No account needed.',
  go: 'Take the tour', skip: 'Skip'
};
var SVG_X = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8"/></svg>';
var root = null, scrim = null, card = null, isOpen = false, back = null, held = [], hideT = 0, drag = null;

function el(tag, cls, html){ var e = document.createElement(tag); if(cls) e.className = cls; if(html) e.innerHTML = html; return e; }
function seen(){ return AX.settings.get('tour') !== null; }
function returning(){
  try{
    var ls = window.localStorage;
    if(ls.getItem('ax-recent')) return true;
    for(var i = 0; i < ls.length; i++) if((ls.key(i) || '').indexOf('ax-rev') === 0) return true;
  }catch(e){}
  return false;
}
function onBrief(){
  var id = decodeURIComponent((location.hash || '').slice(1)), t = id && document.getElementById(id);
  return !!(t && t.closest('.brief'));
}

function build(){
  root = el('div'); root.id = 'axtour';
  scrim = root.appendChild(el('div', 'tr-scrim'));
  card = root.appendChild(el('div', 'tr-card'));
  card.setAttribute('role', 'dialog'); card.setAttribute('aria-modal', 'true'); card.setAttribute('aria-labelledby', 'axtour-h'); card.tabIndex = -1;
  card.appendChild(el('div', 'tr-grab')).setAttribute('aria-hidden', 'true');
  var x = card.appendChild(el('button', 'tr-x', SVG_X)); x.type = 'button'; x.setAttribute('aria-label', 'Close');
  card.appendChild(el('div', 'tr-mark')).textContent = 'S2';
  var h = card.appendChild(el('h2', 'tr-h')); h.id = 'axtour-h'; h.textContent = COPY.title;
  card.appendChild(el('p', 'tr-p')).textContent = COPY.line;
  var ol = card.appendChild(el('ol', 'tr-rows'));
  COPY.rows.forEach(function(t, i){
    var li = ol.appendChild(el('li'));
    var n = li.appendChild(el('span', 'n')); n.textContent = i + 1; n.setAttribute('aria-hidden', 'true');
    li.appendChild(el('span', 't')).textContent = t;
  });
  card.appendChild(el('p', 'tr-f')).textContent = COPY.note;
  var go = card.appendChild(el('button', 'tr-go')); go.type = 'button'; go.textContent = COPY.go;
  var skip = card.appendChild(el('button', 'tr-skip')); skip.type = 'button'; skip.textContent = COPY.skip;
  [x, go, skip].forEach(function(b){ b.addEventListener('click', close); });
  scrim.addEventListener('click', close);
  scrim.addEventListener('wheel', function(e){ e.preventDefault(); }, {passive: false});
  card.addEventListener('touchstart', dragStart, {passive: true});
  card.addEventListener('touchmove', dragMove, {passive: false});
  card.addEventListener('touchend', dragEnd); card.addEventListener('touchcancel', dragEnd);
  B.appendChild(root);
}

/* the rest of the page takes no focus and no pointer while the card is open */
function hold(on){
  if(on){
    held = Array.prototype.filter.call(B.children, function(c){ return c !== root && !c.inert; });
    held.forEach(function(c){ c.inert = true; });
  } else { held.forEach(function(c){ c.inert = false; }); held = []; }
}
function open(){
  if(isOpen) return;
  if(!root) build();
  clearTimeout(hideT); isOpen = true;
  back = document.activeElement;
  root.classList.add('on'); hold(true);
  root.getBoundingClientRect();
  root.classList.add('in');
  try{ card.focus({preventScroll: true}); }catch(e){}
}
function close(){
  if(!isOpen) return;
  isOpen = false; AX.settings.set('tour', VERSION);
  root.classList.remove('in'); hold(false);
  hideT = setTimeout(function(){ root.classList.remove('on'); clearDrag(); }, 520);
  if(back && back.focus && B.contains(back)) try{ back.focus({preventScroll: true}); }catch(e){}
  back = null;
}
function key(e){
  if(!isOpen) return;
  if(e.key === 'Escape'){ e.preventDefault(); e.stopPropagation(); close(); return; }
  if(e.key !== 'Tab') return;
  var f = card.querySelectorAll('button'), first = f[0], end = f[f.length - 1], a = document.activeElement;
  if(e.shiftKey && (a === first || a === card)){ e.preventDefault(); end.focus(); }
  else if(!e.shiftKey && a === end){ e.preventDefault(); first.focus(); }
}

/* the phone sheet follows a downward drag and closes past 30% of its height or on a fast flick */
function clearDrag(){ card.style.transition = ''; card.style.transform = ''; scrim.style.transition = ''; scrim.style.opacity = ''; }
function dragStart(e){
  drag = null;
  if(!NARROW.matches || !isOpen || e.touches.length !== 1 || card.scrollTop > 0) return;
  var t = e.touches[0];
  drag = {x: t.clientX, y: t.clientY, lock: false, d: 0, h: card.offsetHeight, t: Date.now(), ly: t.clientY, v: 0};
}
function dragMove(e){
  if(!drag) return;
  var t = e.touches[0], dx = t.clientX - drag.x, dy = t.clientY - drag.y;
  if(!drag.lock){
    if(dy < -6 || Math.abs(dx) > Math.abs(dy) + 6){ drag = null; return; }
    if(dy < 8) return;
    drag.lock = true;
  }
  if(e.cancelable) e.preventDefault();
  var now = Date.now(); drag.v = (t.clientY - drag.ly) / Math.max(1, now - drag.t); drag.ly = t.clientY; drag.t = now;
  drag.d = Math.max(0, dy);
  card.style.transition = 'none'; card.style.transform = 'translateY(' + drag.d.toFixed(1) + 'px)';
  scrim.style.transition = 'none'; scrim.style.opacity = Math.max(0, 1 - drag.d / drag.h).toFixed(3);
}
function dragEnd(){
  if(!drag || !drag.lock){ drag = null; return; }
  var shut = drag.v > 0.5 || drag.d > drag.h * 0.3; drag = null;
  card.getBoundingClientRect();
  clearDrag();
  if(shut) close();
}

document.addEventListener('keydown', key, true);
var offOpen = AX.on('tour:open', open);
var firstT = 0;
function first(){ if(!seen() && !returning() && !onBrief()) firstT = setTimeout(open, 450); }
if(document.readyState === 'complete') first(); else window.addEventListener('load', first);

return {teardown: function(){
  clearTimeout(firstT); clearTimeout(hideT);
  document.removeEventListener('keydown', key, true); window.removeEventListener('load', first);
  offOpen(); hold(false); if(root) root.remove();
}};
})();
