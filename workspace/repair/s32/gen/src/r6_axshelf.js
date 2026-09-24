window.__axShelf={
  /* Review narrows the page to its fixed set. The sidebar search keeps its
     query and re-lists results inside the set (see 0c). */
  set:function(ids){
    reviewSet=ids||null; closeNav(false); applyShelf(shelf);
  },
  clear:function(){
    reviewSet=null; applyShelf(shelf);
  },
