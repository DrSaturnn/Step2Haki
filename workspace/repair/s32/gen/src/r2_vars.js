var shelf='step2';
var reviewSet=null;   /* fixed brief IDs while an active review is running */
/* Search no longer filters the page: it lists results in the sidebar (see 0c).
   searchTerm stays empty so applyShelf's composition is unchanged. */
var searchTerm='';
var boardOnly=false;
try{ boardOnly=localStorage.getItem('ax-bsonly')==='1'; }catch(e){}

/* Board-style = the set the title badge calls Board (or UWorld): .brief.bs
   without an Aquifer source, the same split the masthead counts use. */
function isBoardStyle(b){
  return b.classList.contains('bs') && b.getAttribute('data-src')!=='aquifer';
}
function shelfEligible(b,s){
  if(!b || !b.id) return false;
  if(reviewSet) return !!reviewSet[b.id];
  if(boardOnly && !isBoardStyle(b)) return false;
  if(s==='step2') return true;
  return (b.getAttribute('data-shelf')||'').split(/\s+/).indexOf(s)>-1;
}
function desktopMatch(b){
  return !searchTerm || (b.textContent||'').toLowerCase().indexOf(searchTerm)>-1;
}
function setSearchMessage(visible,reviewBlocked){
  var n=document.getElementById('noresults'); if(!n) return;
  if(reviewBlocked){ n.textContent='This brief is outside the active review.'; n.style.display='block'; return; }
  n.textContent='No briefs match that search.';
  n.style.display=(searchTerm&&!visible)?'block':'none';
}

