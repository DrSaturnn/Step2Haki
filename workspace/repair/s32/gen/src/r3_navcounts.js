  document.querySelectorAll('#navlinks a[href^="#"]').forEach(function(a){
    var t=document.getElementById(a.getAttribute('href').slice(1));
    var eligible=!!(t&&(!t.classList.contains('brief')||t.style.display!=='none'));
    a.dataset.eligible=eligible?'1':'0';
    a.style.display=eligible?'':'none';
  });
  /* Each system group shows how many of its links are live under the current
     shelf, Board-style only and review filters, so the index never advertises
     briefs it is hiding. */
  var navHost=document.getElementById('navlinks');
  if(navHost){
    var group=null,live=0,sub=null,subLive=0;
    function closeSub(){ if(sub)sub.style.display=subLive?'':'none'; sub=null; subLive=0; }
    function closeGroup(){
      if(!group) return;
      group.style.display=live?'':'none';
      var gc=group.querySelector('.count'); if(gc) gc.textContent=live;
    }
    Array.prototype.slice.call(navHost.children).forEach(function(el){
      if(el.classList.contains('sect')){
        closeSub(); closeGroup();
        group=el;live=0;
      }else if(el.tagName==='A'&&el.style.display!=='none'){live++;subLive++;}
      else if(el.classList.contains('navsub')){ closeSub(); sub=el; }
    });
    closeSub(); closeGroup();
  }
