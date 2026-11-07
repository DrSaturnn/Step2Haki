/* Presentations sub-headers: shown only while a brief under them is shown; the count is the briefs shown */
(function(){
  function fit(){
    document.querySelectorAll('.psub').forEach(function(h){
      var n = 0, el = h.nextElementSibling;
      while(el && el.classList.contains('brief')){ if(el.style.display !== 'none') n++; el = el.nextElementSibling; }
      h.style.display = n ? '' : 'none'; var c = h.querySelector('.n'); if(c) c.textContent = n;
    });
  }
  document.addEventListener('ax-shelf', fit);
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fit); else fit();
  window.addEventListener('load', fit);
})();
