#!/usr/bin/env python3
"""sheets: pack shots.py step images into review or approval sheets (s148 efficiency fix 5; from the s147 and s148
scratch sheets.py).

  python3 tools/spine/sheets.py <shots dir> <out dir> <brief>[,<brief>...] [--steps 1,3,4] [--approval]

Review mode (default), per brief: the phone and phone-study steps are stacked (a 6 px red bar between steps), cut into
1,500 px columns and packed without scaling, up to 5 columns per sheet (<brief>_phone_sheetN.png,
<brief>_phone-study_sheetN.png); the desktop Workup step (step4, step4a, step4b ...) is packed the same way
(<brief>_desktop_workup.png). --steps keeps only those steps in the phone sheets: numbers as shots.py names them
(0 or "header" for the part above step 1, "practice" for the last segment), as review_packet.py --since prints them.
Approval mode (--approval): every step in all four modes, phone, phone-study, desk (1280) and desk-study
(<brief>_<mode>_sheetN.png), for approval.py present. Prints one line per sheet written.
"""
import glob
import os
import re
import sys

# tools/spine/numbers.py shadows the standard numbers module that PIL's PNG plugin imports (via fractions, decimal), so
# this folder leaves the import path before PIL loads (s148 chat 5: the first approval run failed on it)
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.curdir) != _HERE]
from PIL import Image  # noqa: E402
import PIL.PngImagePlugin  # noqa: E402,F401  load the PNG plugin now, while the path is clean
sys.path.append(_HERE)

H, COLS, GAP, BAR = 1500, 5, 14, 6


def stepkey(f):
    m = re.search(r'_step(\d+)([a-z]?)\.png$', f)
    return (int(m.group(1)), m.group(2))


def pick(files, steps):
    """files whose step number is in steps ('header' is 0, 'practice' the highest step number present)"""
    if not steps:
        return files
    top = max((stepkey(f)[0] for f in files), default=0)
    want = {0 if s == 'header' else top if s == 'practice' else int(s) for s in steps}
    return [f for f in files if stepkey(f)[0] in want]


def stack(files):
    ims = [Image.open(f).convert('RGB') for f in files]
    w = max(i.width for i in ims)
    h = sum(i.height for i in ims) + BAR * (len(ims) - 1)
    out = Image.new('RGB', (w, h), 'white')
    y = 0
    for k, i in enumerate(ims):
        out.paste(i, (0, y))
        y += i.height
        if k < len(ims) - 1:
            out.paste(Image.new('RGB', (w, BAR), (220, 30, 30)), (0, y))
            y += BAR
    return out


def columns(img):
    return [img.crop((0, y, img.width, min(y + H, img.height))) for y in range(0, img.height, H)]


def sheet(cols):
    w = sum(c.width for c in cols) + GAP * (len(cols) - 1)
    out = Image.new('RGB', (w, H), (190, 190, 190))
    x = 0
    for c in cols:
        out.paste(c, (x, 0))
        x += c.width + GAP
    return out


def write(files, out, stem):
    if not files:
        print('no images for %s' % stem)
        return []
    cols, done = columns(stack(files)), []
    for n in range(0, len(cols), COLS):
        p = os.path.join(out, '%s_sheet%d.png' % (stem, n // COLS + 1))
        sheet(cols[n:n + COLS]).save(p, optimize=True)
        print(p)
        done.append(p)
    return done


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__.strip().splitlines()[3].strip())
    src, out, ids = argv[0], argv[1], argv[2].split(',')
    steps = argv[argv.index('--steps') + 1].split(',') if '--steps' in argv else None
    os.makedirs(out, exist_ok=True)
    for b in ids:
        def shots(tag):
            return sorted(glob.glob(os.path.join(src, '%s_%s_step*.png' % (b, tag))), key=stepkey)
        if '--approval' in argv:
            for tag, name in (('phone', 'phone'), ('phone-study', 'phone-study'), ('1280', 'desk'), ('1280-study', 'desk-study')):
                write(shots(tag), out, '%s_%s' % (b, name))
            continue
        for tag in ('phone', 'phone-study'):
            write(pick(shots(tag), steps), out, '%s_%s' % (b, tag))
        files = sorted(glob.glob(os.path.join(src, '%s_1280_step4*.png' % b)), key=stepkey)
        if files:
            p = os.path.join(out, '%s_desktop_workup.png' % b)
            sheet(columns(stack(files))).save(p, optimize=True)
            print(p)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
