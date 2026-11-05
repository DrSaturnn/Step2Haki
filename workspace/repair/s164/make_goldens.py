"""s164 item 7: frozen goldens for tools/spine/test_outline_check.py under repair/migration/spine/goldens/<brief>/
(local-only; private repo local-only/repair/migration/spine/goldens/). nephrotic-child's folder has had no outline.json
since the s154c delta build, so its golden is outline_before_s154c.json brought to the s163 step order with
migrate_folders.migrate_outline; scfe and copd copy their current outline.json (already s163 order). Each golden keeps the
folder's .json files except 10_*_spine.json (so no tool sees a second folder for the brief) and the old outline_*.json."""
import glob, json, os, shutil, sys
WS = '/home/claude/Step2Haki/workspace'
sys.path.insert(0, os.path.join(WS, 'repair/pilots/criteria-step2'))
sys.path.insert(0, os.path.join(WS, 'tools'))
import migrate_folders as MF
from pagelib import read_page
SRC = {'nephrotic-child': 'repair/migration/peds/NEPH/spine', 'scfe': 'repair/migration/peds/SCFE/spine',
       'copd': 'repair/migration/fm/COPD/spine'}
import subprocess
pre = subprocess.run(['git', '-C', WS, 'show', '6a4eb72~1:workspace/index.html'], capture_output=True, text=True, check=True).stdout   # the page before s163, for its renamed ids
_, renamed = MF.page_heads(pre)
heads, _ = MF.page_heads(read_page(os.path.join(WS, 'index.html')))
for bid, d in SRC.items():
    out = os.path.join(WS, 'repair/migration/spine/goldens', bid)
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(WS, d, '*.json')):
        n = os.path.basename(f)
        if n.startswith('10_') or (n.startswith('outline') and n != 'outline.json'):
            continue
        shutil.copy(f, out)
    if bid == 'nephrotic-child':
        o = json.load(open(os.path.join(WS, d, 'outline_before_s154c.json')))
        log = {'text_hit': 0, 'misses': [], 'residual': []}
        o2, st = MF.migrate_outline(o, [], renamed, heads.get(bid), log)
        print(bid, st)
        o2['golden_note'] = 's164: frozen test golden (outline_before_s154c.json in the s163 step order); not a build source'
        json.dump(o2, open(os.path.join(out, 'outline.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(bid, sorted(os.listdir(out)))
