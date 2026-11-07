/* Workup stages as headed cards: move each stage label into its card as the card's header. Stages without a card
   keep their label where it is. Runs once at load; nothing is stored. */
(function(){
  'use strict';
  function init(){ AX.brief.each('workup-headed-cards', cards); }
  function cards(b){
    b.querySelectorAll('figure.lcp .pt').forEach(function(pt){
      var w = pt.querySelector(':scope > .when'), t = pt.querySelector(':scope > .tile');
      if(w && t) t.insertBefore(w, t.firstChild);
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
