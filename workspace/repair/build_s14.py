"""s14: drop caution flags from standard facts added in s08 (rlq-pain); keep short grid labels on one line."""
import json
edits=[]
for frag in ['antibiotics (azithromycin) shorten illness and spread ⚠︎','because treatment otherwise prolongs carriage ⚠︎',
             'supportive unless bacteremic or immunocompromised ⚠︎','oral vancomycin or fidaximicin ⚠︎']:
    edits.append({"scope":"brief:rlq-pain","op":"replace","old":frag,"new":frag[:-3],"why":"standard fact, user: no flag on verified common knowledge"})
edits.append({"scope":"page","op":"replace",
 "old":"      blk.appendChild(dl);\n    } else {\n      var ul=document.createElement('ul'); ul.className='facts';",
 "new":"      markShortRows(dl);\n      blk.appendChild(dl);\n    } else {\n      var ul=document.createElement('ul'); ul.className='facts';","why":"short-label grids"})
edits.append({"scope":"page","op":"replace",
 "old":"    if(ul.id) dl.id=ul.id;\n    ul.parentNode.replaceChild(dl,ul);",
 "new":"    if(ul.id) dl.id=ul.id;\n    markShortRows(dl);\n    ul.parentNode.replaceChild(dl,ul);","why":"short-label grids"})
edits.append({"scope":"page","op":"replace",
 "old":"function restore(blk,holder){ while(holder.firstChild) blk.appendChild(holder.firstChild); }",
 "new":"""function restore(blk,holder){ while(holder.firstChild) blk.appendChild(holder.firstChild); }
/* A grid whose labels are all short gets a label column of up to a third of the width.
   With plain auto sizing, a long right-hand column squeezes the label track to its
   narrowest word and "Versus ITP" stacks one word per line. Sentence-length labels
   keep the old sizing. */
function markShortRows(dl){
  var dts=Array.prototype.slice.call(dl.children).filter(function(x){return x.tagName==='DT';});
  if(dts.length && dts.every(function(dt){ return dt.textContent.trim().length<=34; })) dl.classList.add('rows-short');
}""","why":"short-label grids"})
edits.append({"scope":"page","op":"insert_before","anchor":"/* ---------- AQUIFER: source-driven badge, band, nav ---------- */",
 "text":"@media (min-width:981px){ .rows.rows-short{grid-template-columns:fit-content(34%) minmax(0,1fr)} }\n","why":"short-label grids"})
json.dump({"pass":"s14","date":"2026-09-23","reason":"drop flags on standard facts (s08); short grid labels stay on one line","expected":{"mcq_delta":0},"edits":edits},open('repair/LEDGER-s14.json','w'),indent=1,ensure_ascii=False)
print(len(edits))
