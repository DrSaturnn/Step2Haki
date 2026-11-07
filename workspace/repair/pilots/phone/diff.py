"""diff: python3 diff.py OUTDIR; counts pixels that differ between each a_<state>.png and b_<state>.png."""
import glob, os, sys
from PIL import Image, ImageChops
d = sys.argv[1]
for a in sorted(glob.glob(os.path.join(d, 'a_*.png'))):
    b = a.replace('/a_', '/b_')
    x, y = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
    m = ImageChops.difference(x, y).convert('L').point(lambda v: 255 if v > 8 else 0)
    print(os.path.basename(a)[2:-4], 'pixels differing:', sum(1 for v in m.getdata() if v))
