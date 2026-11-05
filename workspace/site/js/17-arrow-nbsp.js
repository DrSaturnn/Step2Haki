/* s141 S5 (round 1 display MED, lithium-effects; nephrotic-child LOW): an arrow for a high or low value stays on the line
   of the word it qualifies. Presentation only: the space beside the arrow becomes a no-break space; no text changes. */
(function(){
  "use strict";
  var A = /[↑↓]/;
  function bind(root){
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {acceptNode: function(n){ return A.test(n.nodeValue) ? 1 : 3; }});
    var ns = []; while(w.nextNode()) ns.push(w.currentNode);
    ns.forEach(function(n){
      var v = n.nodeValue
        .replace(/([↑↓]) (?=\S)/g, '$1 ')
        .replace(/(\S) ([↑↓])(?=$|[\s,;:.)])/g, '$1 $2');
      if(/[↑↓] $/.test(v) && n.nextSibling) v = v.slice(0, -1) + ' ';
      if(v !== n.nodeValue) n.nodeValue = v;
    });
  }
  function all(){ document.querySelectorAll('.brief').forEach(bind); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', all); else all();
})();
