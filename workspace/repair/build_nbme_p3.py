"""NBME phase 3: data-bp on every brief (primary, then optional secondary), attribute-only."""
import csv,json
rows=list(csv.DictReader(open('repair/nbme/blueprint_map.csv')))
edits=[{"scope":"brief:"+r['id'],"op":"set_attr","attr":"data-bp","value":(r['primary']+' '+r['secondary']).strip(),"why":"NBME blueprint system"} for r in rows]
json.dump({"pass":"nbme-p3","date":"2026-09-24","reason":"blueprint tags on all briefs","expected":{},"edits":edits},open('repair/LEDGER-nbme-p3.json','w'),indent=1)
print(len(edits))
