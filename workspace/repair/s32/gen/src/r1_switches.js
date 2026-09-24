/* ---------- 0. sidebar mode switches ---------- */
function switches(){
  var nav=document.getElementById('nav'); if(!nav) return;
  var brand=nav.querySelector('.brand');
  var box=document.createElement('div'); box.id='modes';
  box.innerHTML =
    '<button class="bsonly" type="button" aria-pressed="false" title="Show only board-style briefs"><span class="track"><span class="knob"></span></span><span class="nm">BOARD-STYLE ONLY</span></button>'+
    '<button class="study" type="button" aria-pressed="false"><span class="track"><span class="knob"></span></span><span class="nm">STUDY MODE</span></button>'+
    '<button class="flatt" type="button" aria-pressed="false"><span class="track"><span class="knob"></span></span><span class="nm">FLAT THEME</span></button>';
  brand ? brand.after(box) : nav.prepend(box);
  var b=document.body;
  function sync(){
    box.querySelector('.bsonly').setAttribute('aria-pressed',boardOnly?'true':'false');
    box.querySelector('.study').setAttribute('aria-pressed',b.classList.contains('study')?'true':'false');
    box.querySelector('.flatt').setAttribute('aria-pressed',b.classList.contains('flat')?'true':'false');
  }
  if(localStorage.getItem('ax-study')==='1') b.classList.add('study');
  if(localStorage.getItem('ax-flat')==='1') b.classList.add('flat');
  /* Board-style only joins the shelf rule in shelfEligible(); it is a per-viewer
     preference, so it lives in localStorage like the other two switches. */
  box.querySelector('.bsonly').addEventListener('click',function(){
    boardOnly=!boardOnly;
    try{ localStorage.setItem('ax-bsonly',boardOnly?'1':'0'); }catch(e){}
    sync(); applyShelf(shelf);
  });
  box.querySelector('.study').addEventListener('click',function(){
    b.classList.toggle('study'); localStorage.setItem('ax-study',b.classList.contains('study')?'1':'0'); sync();
  });
  box.querySelector('.flatt').addEventListener('click',function(){
    b.classList.toggle('flat'); localStorage.setItem('ax-flat',b.classList.contains('flat')?'1':'0'); sync();
  });
  sync();
  if(!window.__axModeObserver){
    window.__axModeObserver=new MutationObserver(function(){
      sync();
      var mb=document.querySelector('#mbar [data-act="study"]');
      if(mb) mb.setAttribute('aria-pressed',b.classList.contains('study')?'true':'false');
      if(typeof syncMaskRegions==='function') syncMaskRegions();
    });
    window.__axModeObserver.observe(b,{attributes:true,attributeFilter:['class']});
  }
}

