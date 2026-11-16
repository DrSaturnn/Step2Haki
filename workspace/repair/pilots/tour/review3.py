"""Review page 3 (the whole tour and the resize and zoom pass): one HTML file with the tour_check.js and
resize_shots.js screenshots inlined.
Usage: python3 review3.py <tour_check shots dir> <resize_shots dir> <out html>"""
import base64, io, os, sys
from PIL import Image
tour, rs, out = sys.argv[1], sys.argv[2], sys.argv[3]
def img(d, name, w):
    im = Image.open(os.path.join(d, name + '.png')).convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=84)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def fig(d, name, w, cap):
    return '<figure><img src="%s" alt="%s"><figcaption>%s</figcaption></figure>' % (img(d, name, w), cap, cap)
def row(cls, items, d, w):
    return '<div class="row %s">' % cls + ''.join(fig(d, n, w, c) for n, c in items) + '</div>'
P = 'tour_375x667_'; D = 'tour_1101x800_'
html = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Step2Haki tour: review 3</title>
<style>
:root{--bg:#F4F4F7;--card:#FFFFFF;--ink:#15151B;--mut:#5C6070;--hair:#E1E2E8;--acc:#3A5A8C}
@media (prefers-color-scheme:dark){:root{--bg:#101114;--card:#1A1B20;--ink:#F1F1F4;--mut:#A0A4B2;--hair:#2B2D35;--acc:#9DB7E0}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
main{max-width:1120px;margin:0 auto;padding:32px 20px 64px}
h1{font-size:28px;letter-spacing:-.02em;margin:0 0 6px}h2{font-size:19px;margin:36px 0 10px;letter-spacing:-.01em}
p{margin:0 0 10px;max-width:74ch}.sub{color:var(--mut)}
.box{background:var(--card);border:1px solid var(--hair);border-radius:16px;padding:16px 18px;margin:14px 0}
ol,ul{margin:0;padding-left:22px}li{margin:4px 0;max-width:74ch}
.row{display:grid;gap:14px;margin:12px 0}.r5{grid-template-columns:repeat(5,1fr)}.r4{grid-template-columns:repeat(4,1fr)}.r3{grid-template-columns:repeat(3,1fr)}.r2{grid-template-columns:repeat(2,1fr)}
figure{margin:0;background:var(--card);border:1px solid var(--hair);border-radius:14px;overflow:hidden}
figure img{display:block;width:100%;height:auto}figcaption{padding:8px 12px;font-size:13px;color:var(--mut);border-top:1px solid var(--hair)}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14.5px}th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--hair);vertical-align:top}th{color:var(--mut);font-weight:600}
@media (max-width:760px){.r5,.r4{grid-template-columns:1fr 1fr}.r3{grid-template-columns:1fr 1fr}.r2{grid-template-columns:1fr}}
</style></head><body><main>
<h1>Welcome tour: review 3</h1>
<p class="sub">Batch s176f, steps 4 and 5. Built on branch wip/s176f. Nothing is shipped; the live page is unchanged.</p>
<div class="box"><p><b>Decision needed.</b> Approve the four stops, the Help row, the direct-link pill and the resize behavior below, or name changes. Copy edits for any stop can be given here. After approval, step 6 adds the tour check to the ship checks, writes the records and presents the gate result for "ship".</p>
<p><b>Try it.</b> The pilot artifact (Step2Haki Welcome Card Pilot) runs this build. The top button "Pilot: show the welcome card" reopens the card.</p></div>

<h2>Phone, 375 x 667</h2>
<p>Stops 1 and 2 run on the starting screen. Stop 3 opens the first brief the shelf lists. On stop 4 the ring starts on the tab capsule and moves to the Settings tab after 1.8 seconds. The panel is 152 to 173 px tall, under the 200 px budget, with no scrolling.</p>
''' + row('r5', [(P + '1', 'Stop 1: Search and shelf'), (P + '2', 'Stop 2: Browse'), (P + '3', 'Stop 3: Inside a brief'), (P + '4', 'Stop 4: Tabs'), (P + '4b', 'Stop 4 after 1.8 s: Settings tab')], tour, 375) + '''

<h2>Desktop, 1101 x 800</h2>
<p>The popover opens to the right of the sidebar for stops 1 to 3 and below the toolbar for stop 4. On stop 4 the ring moves from the toolbar to the settings button.</p>
''' + row('r2', [(D + '1', 'Stop 1: Search and shelf'), (D + '2', 'Stop 2: Browse'), (D + '3', 'Stop 3: Inside a brief'), (D + '4b', 'Stop 4 after 1.8 s: settings button')], tour, 1101) + '''

<h2>Replay row and direct-link pill</h2>
<p>"Replay tutorial" sits in a new last group, Help, in the display sheet. A first visit that lands on a direct link to a brief gets the pill; the tour and the close button both mark the tutorial as seen.</p>
''' + row('r4', [('help_phone', 'Phone: Settings, Help group'), ('pill_phone', 'Phone: pill under the brief header')], tour, 393) + row('r2', [('help_desktop', 'Desktop: display sheet, Help group'), ('pill_desktop', 'Desktop: pill at the bottom right')], tour, 1280) + '''

<h2>Resize and zoom pass</h2>
<p>resize_shots.js runs five cases and measures the ring, the panel and the target in each: 86 of 86 checks pass.</p>
<h3>1. Phone rotated mid-stop (393 x 852 to 852 x 393)</h3>
<p>The ring and the panel follow the rotation at stops 1, 2 and 3, and return to the portrait layout when the phone rotates back.</p>
''' + row('r3', [('rotate_1_land', 'Stop 1, landscape'), ('rotate_2_land', 'Stop 2, landscape: panel at the top'), ('rotate_3_land', 'Stop 3, landscape')], rs, 852) + '''
<h3>2. Window crossing 1100 px mid-stop (1280 to 900 wide and back)</h3>
<p>The stop restarts in the other layout with the same step and text. Stop 4 switches between the Toolbar text and the Tabs text.</p>
''' + row('r2', [('cross_2_900', 'Stop 2 at 900 wide'), ('cross_4_900b', 'Stop 4 at 900 wide'), ('cross_2_1280', 'Stop 2 back at 1280 wide'), ('cross_4_1280b', 'Stop 4 back at 1280 wide')], rs, 1000) + '''
<h3>3. Browser zoom 200% (a 1280 x 720 window becomes 640 x 360)</h3>
<p>The page uses the phone layout at this width. Every stop keeps its ring on the target and its text on screen with no scrolling.</p>
''' + row('r2', [('zoom200_1', 'Stop 1'), ('zoom200_2', 'Stop 2: panel at the top'), ('zoom200_3', 'Stop 3'), ('zoom200_4', 'Stop 4')], rs, 960) + '''
<h3>4. Pinch zoom 2x at stop 1</h3>
<p>The ring stays on the top bar. The panel stays at the bottom of the page layout, so a reader who pinches in at the top of the screen pans down or pinches out to reach Next and the close button. This matches how Safari treats any fixed sheet under pinch zoom. Left as built; an option is listed under open items.</p>
''' + row('r4', [('pinch_1_zoomed', 'Pinched to 2x, top left of the page'), ('pinch_1_back', 'Back at 1x')], rs, 393) + '''
<h3>5. Removed tag at stop 2</h3>
<p>With the Browse tag removed from the page, stop 2 shows its text as a centered card over the blurred backdrop with no ring. Next then reaches stop 3 on its target.</p>
''' + row('r2', [('lost_2_phone', 'Phone'), ('lost_2_desktop', 'Desktop')], rs, 900) + '''

<h2>Changed in step 5</h2>
<p>One defect was found and fixed. On a short phone-layout screen (a phone in landscape, or a desktop window at 200% zoom) the Browse card at stop 2 sat under the tab capsule with 31 px in view. The panel now docks at the top of the screen when the bottom position would leave under 64 px of the target in view, and the page scrolls the target into the space between the panel and the capsule (112 px in view at 640 x 360, 145 px at 852 x 393). Tall phone screens are unchanged.</p>

<h2>Built differently from the plan</h2>
<div class="tw"><table><tr><th>Item</th><th>Plan</th><th>Built</th><th>Status</th></tr>
<tr><td>Phone welcome sheet</td><td>Sheet attached to the bottom edge, top corners rounded</td><td>Floats 10 px from the sides and the bottom, four 28 px corners</td><td>Accepted in review 2</td></tr>
<tr><td>Sheet and panel width</td><td>Full width</td><td>Capped at 480 px between 500 and 1100 px</td><td>Accepted in review 2</td></tr>
<tr><td>Motion</td><td>One cubic-bezier curve</td><td>The site's spring tokens</td><td>Accepted in review 2</td></tr>
<tr><td>Reduced motion</td><td>120 ms fade</td><td>No timed move</td><td>Accepted in review 2</td></tr>
<tr><td>Backdrop during a stop</td><td>Dim with blur</td><td>Dim, no blur; the card keeps the blur</td><td>Accepted in review 2</td></tr>
<tr><td>Current dot</td><td>Accent color</td><td>Accent color and 18 px wide</td><td>Accepted in review 2</td></tr>
<tr><td>Desktop popover</td><td>Popover beside the element</td><td>Adds a 14 px pointer</td><td>Accepted in review 2</td></tr>
<tr><td>Phone ring</td><td>On the element</td><td>Inset 4 px from the screen edges</td><td>Accepted in review 2</td></tr>
<tr><td>Stop 4</td><td>The bar, "ending on the Settings tab"</td><td>One stop; the ring moves from the bar to the settings control after 1.8 s</td><td>New in step 4</td></tr>
<tr><td>Replay control</td><td>Added by the tour module</td><td>Built where the display sheet builds its other controls</td><td>New in step 4</td></tr>
<tr><td>Replay or pill tour started inside a brief, phones</td><td>Not specified</td><td>Stops 1 and 2 show the starting screen; stop 3 returns to that brief</td><td>New in step 4</td></tr>
<tr><td>Phone Browse target</td><td>The segment control with the first rows</td><td>The whole Browse card, cut 8 px above the panel</td><td>New in step 4</td></tr>
<tr><td>Short screens</td><td>Panel always above the tab capsule</td><td>Panel docks at the top when under 64 px of the target would show</td><td>New in step 5</td></tr>
</table></div>

<h2>Open items</h2>
<ul>
<li>Pinch zoom: the panel could follow the pinched view. At 2x on a phone the visible area is 197 px wide and the panel is 365 px wide, so the panel would need to shrink to half size. Recommendation: keep the current behavior.</li>
<li>Copy (open call 6): the text of every stop is below and can be edited in this review.</li>
</ul>

<h2>Copy</h2>
<div class="tw"><table><tr><th>Stop</th><th>Title</th><th>Text</th></tr>
<tr><td>1</td><td>Search and shelf</td><td>Search any topic, finding or drug. The shelf menu limits every list to one exam.</td></tr>
<tr><td>2</td><td>Browse</td><td>By system lists topics by organ system. By complaint lists workups that start from the presenting complaint.</td></tr>
<tr><td>3</td><td>Inside a brief</td><td>Steps 1 to 8 run from presentation to follow-up. A number jumps to its step. Practice opens the questions. Recall hides answers until tapped.</td></tr>
<tr><td>4, phones</td><td>Tabs</td><td>Home, Browse, Review and Settings stay at the bottom of every screen. This tutorial replays from Settings.</td></tr>
<tr><td>4, desktop</td><td>Toolbar</td><td>Read and Recall switch the study mode. Review schedules what to see again. This tutorial replays from the settings button.</td></tr>
<tr><td>Pill</td><td></td><td>New here? Take the tour</td></tr>
</table></div>

<h2>Checks</h2>
<p>tour_check.js 104 of 104, stop_check.js 53 of 53, card_check.js 36 of 36, resize_shots.js 86 of 86. ui_lint page counts are at the baseline and the site lint passes.</p>
</main></body></html>'''
html = html.replace('<h3>', '<h3 style="font-size:16px;margin:22px 0 6px">')
open(out, 'w', encoding='utf-8').write(html)
print('review', out, len(html))
