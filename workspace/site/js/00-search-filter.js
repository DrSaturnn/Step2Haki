(function(){
  var search=document.getElementById('search');
  var briefs=Array.prototype.slice.call(document.querySelectorAll('.brief'));
  var systems=Array.prototype.slice.call(document.querySelectorAll('h3.system'));
  var links=Array.prototype.slice.call(document.querySelectorAll('#navlinks a'));

  /* Search visibility is composed by shelfInit/applyShelf below.
     The legacy listener used direct style writes and could resurrect
     off-shelf briefs when search was cleared. */
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){
        var id=e.target.id;
        links.forEach(function(a){a.classList.toggle('active',a.getAttribute('href')==='#'+id);});
      }
    });
  },{rootMargin:'-10% 0px -80% 0px'});
  briefs.concat(systems).forEach(function(el){if(el.id)obs.observe(el);});
})();
