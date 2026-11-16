"""Review page 2 (tour stop 1): one HTML file with the stop_shots.js screenshots inlined.
Usage: python3 review2.py <shots dir> <out html>"""
import base64, io, os, sys
from PIL import Image
shots, out = sys.argv[1], sys.argv[2]
def img(name, w):
    im = Image.open(os.path.join(shots, name)).convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=86)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def fig(name, w, cap, cls=''):
    return '<figure class="%s"><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (cls, img(name, w), cap, cap)
phones = [('stop1_p375_light.png', '375 x 667'), ('stop1_p393_light.png', '393 x 852'), ('stop1_p430_light.png', '430 x 932')]
desks = [('stop1_d1101_light.png', '1101 x 800'), ('stop1_d1280_light.png', '1280 x 720'), ('stop1_d1440_light.png', '1440 x 900')]
html = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Step2Haki tour stop 1: review 2</title>
<style>
:root{--bg:#F4F4F7;--card:#FFFFFF;--ink:#15151B;--mut:#5C6070;--hair:#E1E2E8;--acc:#3A5A8C}
@media (prefers-color-scheme:dark){:root{--bg:#101114;--card:#1A1B20;--ink:#F1F1F4;--mut:#A0A4B2;--hair:#2B2D35;--acc:#9DB7E0}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
main{max-width:1120px;margin:0 auto;padding:32px 20px 64px}
h1{font-size:28px;letter-spacing:-.02em;margin:0 0 6px}h2{font-size:19px;margin:36px 0 10px;letter-spacing:-.01em}
p{margin:0 0 10px;max-width:74ch}.sub{color:var(--mut)}
.box{background:var(--card);border:1px solid var(--hair);border-radius:16px;padding:16px 18px;margin:14px 0}
ol,ul{margin:0;padding-left:22px}li{margin:4px 0;max-width:74ch}
.row{display:grid;gap:16px;margin:12px 0}.r3{grid-template-columns:repeat(3,1fr)}.r2{grid-template-columns:repeat(2,1fr)}
figure{margin:0;background:var(--card);border:1px solid var(--hair);border-radius:14px;overflow:hidden}
figure img{display:block;width:100%;height:auto}figcaption{padding:8px 12px;font-size:13px;color:var(--mut);border-top:1px solid var(--hair)}
.wide figure{margin:0 0 16px}
table{border-collapse:collapse;width:100%;font-size:14.5px}th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--hair);vertical-align:top}th{color:var(--mut);font-weight:600}
@media (max-width:760px){.r3{grid-template-columns:1fr 1fr}.r2{grid-template-columns:1fr}}
</style></head><body><main>
<h1>Tour stop 1: review 2</h1>
<p class="sub">Batch s176f, step 3. Built on branch wip/s176f. Nothing is shipped; the live page is unchanged.</p>
<div class="box"><p><b>Decision needed.</b> Approve the stop design below, or name changes. Step 4 then builds stops 2 to 4 in this design and wires the Settings replay row and the direct-link pill.</p>
<p><b>Try it.</b> The pilot artifact (Step2Haki Welcome Card Pilot) now runs this build. Press "Take the tour" on the card. The top button "Pilot: show the welcome card" reopens the card.</p></div>

<h2>Phones</h2>
<p>The ring surrounds the top bar (search and the shelf menu). The text sits in a panel 8 px above the tab capsule. The panel is 152 px tall at all three sizes, under the 200 px budget, with no scrolling.</p>
<div class="row r3">''' + ''.join(fig(n, 430, c) for n, c in phones) + '''</div>

<h2>Desktop</h2>
<p>The ring surrounds the sidebar search and the shelf card. The popover (320 x 152) opens to the right of the sidebar at x 334 with a pointer toward the ring.</p>
<div class="wide">''' + ''.join(fig(n, 1280, c) for n, c in desks) + '''</div>

<h2>Dark and tinted</h2>
<div class="row r2">''' + fig('stop1_p393_dark.png', 430, 'Phone 393 x 852, dark') + fig('stop1_p393_tinted.png', 430, 'Phone 393 x 852, tinted') + '''</div>
<div class="wide">''' + fig('stop1_d1280_dark.png', 1280, 'Desktop 1280 x 720, dark') + fig('stop1_d1280_tinted.png', 1280, 'Desktop 1280 x 720, tinted') + '''</div>

<h2>Behavior in this build</h2>
<ul>
<li>"Take the tour" on the card opens stop 1 and records the tour as seen.</li>
<li>Exits from a stop: the close button, Esc, and a swipe down on the phone panel (past 30% of its height, or a fast flick).</li>
<li>A tap on the dimmed page or on the highlighted element does nothing (open call 4, option a). The page stays inert during a stop.</li>
<li>The ring and the panel re-measure on resize, rotation, scroll, pinch zoom and any size change of the target. Tested: desktop resize, crossing 1100 px mid-stop, phone rotation mid-stop.</li>
<li>When the tagged element is missing, the same text shows as a centered card over the blurred backdrop, with no ring.</li>
<li>Reduced motion: the ring and the panel appear in place with no timed move.</li>
<li>"Next" closes the tour in this build, because stops 2 to 4 arrive in step 4. The Back button exists and stays hidden on stop 1.</li>
</ul>
<p>Check results: stop_check.js 55 of 55 pass; card_check.js 36 of 36 pass; ui_lint page counts equal the baseline; ui_lint site PASS.</p>

<h2>Built differently from the plan</h2>
<table><tr><th>Item</th><th>Plan</th><th>Built</th><th>Reason</th></tr>
<tr><td>Backdrop during a stop</td><td>Dimmed page with a 20 px blur</td><td>Dimmed page, no blur. Light theme dim 46%, dark 62%</td><td>A blur layer cannot leave a sharp opening for the target, and the reader needs to see the page around the ring to place it. The card keeps the blur.</td></tr>
<tr><td>Phone panel width</td><td>Docked above the capsule</td><td>Same, capped at 480 px wide and centered between 500 and 1100 px</td><td>Matches the cap on the welcome sheet at tablet widths.</td></tr>
<tr><td>Progress dots</td><td>Four dots, current in the accent color</td><td>Same, and the current dot is 18 px wide</td><td>The current step reads at a glance without a counter.</td></tr>
<tr><td>Desktop popover</td><td>Popover beside the element</td><td>Same, with a 14 px pointer on the edge facing the ring</td><td>Ties the text to the ring when the two are 14 px apart.</td></tr>
<tr><td>Phone ring</td><td>#phbar</td><td>The ring is inset 4 px from the screen edges</td><td>#phbar spans the full width, and a ring at the edge would be cut off.</td></tr>
</table>

<h2>Review 1 items still open</h2>
<p>The message that started this chat named no changes to the welcome card, so the card is unchanged from review 1. The four differences listed there (floating phone sheet with four rounded corners, 480 px cap, spring curves, no timed move under reduced motion) stand until reversed. Copy edits for the card and for stop 1 can be given with this review (open call 6).</p>

<h2>Copy on stop 1</h2>
<p><b>Search and shelf.</b> Search any topic, finding or drug. The shelf menu limits every list to one exam.</p>
</main></body></html>'''
open(out, 'w', encoding='utf-8').write(html)
print('review', out, len(html))
