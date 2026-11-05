"""s164 item 4: the 6 s163 B4 Recall masks (repair/s163/50_masks.json) that sit in briefs with an outline.json
(kawasaki 3, fap 2, bs-wilson 1) are written into those outlines, so a rebuild from the folder keeps them. Only the
sourced line ({"t", "ids"}) in the Diagnostic criteria step (h n 2) whose text equals the op's pre-mask cell text is
changed, to the op's masked text: the same markup as the page, inside the same t string, so ids and claims are unchanged.
Usage: python3 repair/s164/mask_outlines.py <private clone> [--write]   (reports without --write)"""
import json, os, sys
ROWS = {
    'repair/migration/peds/kawasaki/spine/outline.json': [
        ('Fever <b>5 days</b> or more', 'Fever <span class="mask"><b>5 days</b></span> or more'),
        ('Fever <b>5 days</b> or more plus <b>at least 4</b> criteria',
         'Fever <span class="mask"><b>5 days</b></span> or more plus <b>at least <span class="mask">4</span></b> criteria'),
        ('Fever <b>5 days</b> or more with <b>2 or 3</b> criteria',
         'Fever <span class="mask"><b>5 days</b></span> or more with <span class="mask"><b>2 or 3</b></span> criteria')],
    'repair/migration/gi/fap/spine/outline.json': [
        ('<b>100 or more</b> adenomas, with endoscopy and genetic testing',
         '<b><span class="mask">100</span> or more</b> adenomas, with endoscopy and genetic testing'),
        ('<b>10 to 99</b> adenomas', '<span class="mask"><b>10 to 99</b></span> adenomas')],
    'repair/migration/gi/bs-wilson/spine/outline.json': [
        ('Ceruloplasmin under 5 mg/dL', 'Ceruloplasmin under <span class="mask">5 mg/dL</span>')],
}


def walk(x, step, hits, old, new):
    if isinstance(x, dict):
        if x.get('t') == old and step[0] == 2:
            hits.append(x)
            x['t'] = new
        for v in x.values():
            walk(v, step, hits, old, new)
    elif isinstance(x, list):
        for v in x:
            walk(v, step, hits, old, new)


def main(argv):
    root, write = argv[0], '--write' in argv
    total = 0
    for rel, rows in ROWS.items():
        for base in ('local-only', ''):
            f = os.path.join(root, base, rel)
            if not os.path.exists(f):
                continue
            o = json.load(open(f, encoding='utf-8'))
            for old, new in rows:
                n, cur = 0, None
                for b in o['body']:          # the step a block sits in is the last h block before it
                    if isinstance(b, dict) and b.get('type') == 'h':
                        cur = int(b['n'])
                    hits = []
                    walk(b, [cur], hits, old, new)
                    n += len(hits)
                print('%s: %d x %r' % (os.path.relpath(f, root), n, old[:50]))
                total += n
            if write:
                json.dump(o, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('mask_outlines: %d line(s) %s' % (total, 'written' if write else '(report only)'))


if __name__ == '__main__':
    main(sys.argv[1:])
