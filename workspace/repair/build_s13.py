"""s13: the first Aquifer symptom-workup brief, aq-bruising (Aquifer Pediatrics 21), into Hematology.
Brief HTML comes from repair/pilot_peds21.py (B3, rev 2); shelf widened to fm peds."""
import json,subprocess,sys
subprocess.run([sys.executable,'repair/pilot_peds21.py'],check=True,capture_output=True)
brief=open('/tmp/claude-0/briefB3.html').read()
brief=brief.replace('<div class="brief aq" id="aq-bruising" data-shelf="peds"','<div class="brief aq" id="aq-bruising" data-shelf="fm peds"',1)
assert brief.count('id="aq-bruising"')==1 and 'data-shelf="fm peds"' in brief
edits=[]
band=('<div class="bsband aqband"><span class="n">1 brief</span><span class="lbl">Aquifer &middot; Case-Based Briefs</span>'
      '<p class="t">Hematology</p></div>\n\n')
edits.append({"scope":"page","op":"insert_before","anchor":"<!-- =================== ID","text":band+brief+"\n\n\n",
              "why":"new Aquifer symptom-workup brief (Aquifer Pediatrics 21); owns IgA vasculitis, previously pending"})
edits.append({"scope":"page","op":"insert_after","anchor":'    <a class="bs" href="#bs-sickle-trait">Sickle Trait vs Disease</a>',
              "text":'\n    <div class="navsub aq">Aquifer</div>\n    <a class="aq" href="#aq-bruising">Bruising and Purpura</a>',"why":"nav"})
edits.append({"scope":"page","op":"replace",
  "old":'<h3 class="system" id="heme">Hematology <span class="n">6 topics <span style="color:#9A5B0E">+ 3 board-style</span></span></h3>',
  "new":'<h3 class="system" id="heme">Hematology <span class="n">6 topics <span style="color:#9A5B0E">+ 3 board-style</span> <span style="color:#1F6A7E">+ 1 Aquifer</span></span></h3>',
  "why":"heme header counts"})
edits.append({"scope":"brief:anemia-thrombocytopenia","op":"replace",
  "old":"where hemolysis arrives with a normal platelet count and an antibody rather than a clot.</div>",
  "new":"where hemolysis arrives with a normal platelet count and an antibody rather than a clot. Aquifer <b>Bruising and Purpura in a Child</b> starts one step earlier, from the bruise, and sorts it by the platelet count.</div>",
  "why":"reverse link"})
edits.append({"scope":"brief:bs-leukemia","op":"replace",
  "old":"owns the benign nocturnal limb pain whose normal examination excludes this diagnosis.</div>",
  "new":"owns the benign nocturnal limb pain whose normal examination excludes this diagnosis. Aquifer <b>Bruising and Purpura in a Child</b> places leukemia among the other causes of bruising in a child.</div>",
  "why":"reverse link"})
edits.append({"scope":"brief:hematuria","op":"replace",
  "old":"is the urine showing red cells and casts, or protein alone?</div>",
  "new":"is the urine showing red cells and casts, or protein alone? Aquifer <b>Bruising and Purpura in a Child</b> sends the renal involvement of IgA vasculitis here.</div>",
  "why":"reverse link"})
json.dump({"pass":"s13","date":"2026-09-23","reason":"First Aquifer symptom-workup brief: aq-bruising (Pediatrics 21).","expected":{"mcq_delta":17},"edits":edits},
          open('repair/LEDGER-s13.json','w'),indent=1,ensure_ascii=False)
print(len(edits))
