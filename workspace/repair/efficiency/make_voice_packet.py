#!/usr/bin/env python3
"""make_voice_packet.py: voice-pass packets for one system section.

  python3 repair/efficiency/make_voice_packet.py <batch> <system id> [--groups N | --per N] [--exclude id,id]
                                                 [--outdir DIR] [--prefix NN]

1. Builds the verify base: index.html plus every repair/<batch>/*.json that is not a voice
   file (name without "voice"), written to scratch/<batch>_base.html, so worker anchors match
   the page as it will be when the voice edits apply.
2. Takes every brief under <h3 class="system" id="<system id>"> in that base (topic, board-style,
   Aquifer), minus --exclude, and splits them into N groups (default 5) of similar HTML size
   (largest first into the lightest group), each group kept in page order; or, with --per N,
   into consecutive page-order packets of N briefs (the last one smaller).
3. Writes <outdir>/packet_<k>.md per group (default outdir repair/<batch>/voice; with --outdir the
   names are packet_<system>_<k>.md): instructions and verify command, RULES_voice.md, the
   replace-only edit format, the worked example, the briefs' HTML. Workers write
   repair/<batch>/<prefix>_voice_<k>.json (default prefix 04; with --outdir
   <prefix>_voice_<system>_<k>.json), which build.py applies after the other batch files.
   Packets quote page HTML only; put them under repair/sources/ when they must stay local.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(WS, 'tools'))
from pagelib import briefs, read_page, text, write_page  # noqa: E402
import apply_edits  # noqa: E402
import json  # noqa: E402

FORMAT = '''One JSON file: `{"edits": [op, op, ...]}`, replace ops only, applied in order:

```json
{"op": "replace", "brief": "<brief id>", "find": "<verbatim snippet of the brief HTML>", "with": "<rewritten HTML>", "note": "why"}
```

- `find` is copied verbatim from the brief HTML below, entities included (`&amp;`, `&middot;`, `&gt;`, `&lt;`), and occurs exactly once inside that brief. Lengthen it with neighbouring text until it is unique.
- `find` must lie inside `.dp`, `.rule`, `.pearls`, `.danger`, `.traps` or the first segment of `p.sub` (before the first `·`). Never inside `.vignette`, a table, `.crit` or the question bank (`ol.bank`); the verifier rejects those.
- Keep every bold clinical term, every number and every `<span class="lbl">...</span>` label exactly (a bold slogan or rhetorical label may be reworded if listed in `"reworded_bold": ["<old bold text>"]` on that op); the only em dash allowed is the structural `<b>Term</b> — definition`.
- One op per block is easiest: `find` = the block's prose (not its opening `<div ...>` tag), `with` = the rewrite.
- Every op carries the claim map (drift protocol in the rules):

```json
{"op": "replace", "brief": "<id>", "find": "...", "with": "...", "note": "why",
 "reworded_bold": ["<old bold slogan or emphasis-only bold, if any>"],
 "claims": [
   {"claim": "<atomic clinical claim from the OLD text>", "to": "<the NEW sentence that carries it, visible text, quoted exactly>"},
   {"claim": "...", "carried_by": "<quoted passage elsewhere in this brief that already states it>"},
   {"claim": "<non-clinical framing only>", "dropped": "<reason>"}],
 "new_claims": [
   {"claim": "<clinical claim in the NEW text>", "from": "<exact claim text of the old claim>"},
   {"claim": "<ACRONYM> stands for <expansion>", "from": "expansion"}]}
```'''


def example():
    """The worked example: before, after, and its full edits entry with the claim map."""
    p = os.path.join(HERE, 'voice_example_infant_stool.json')
    e = json.load(open(p, encoding='utf-8'))['edits'][0]
    return ('Before (visible text):\n\n> %s\n\nAfter:\n\n> %s\n\nSkipped acronym: IgE (immunoglobulin name a learner '
            'expands). The edits entry:\n\n```json\n%s\n```' % (text(e['find']), text(e['with']).replace('\n', ' '),
                                                            json.dumps(e, indent=1, ensure_ascii=False)))


def base_page(batch):
    html = read_page(os.path.join(WS, 'index.html'))
    for f in sorted(glob.glob(os.path.join(WS, 'repair', batch, '*.json'))):
        if 'voice' in os.path.basename(f):
            continue
        html, _ = apply_edits.apply(html, json.load(open(f, encoding='utf-8')))
    os.makedirs(os.path.join(WS, 'scratch'), exist_ok=True)
    out = os.path.join(WS, 'scratch', '%s_base.html' % batch)
    write_page(out, html)
    return html, out


def section_briefs(html, sysid):
    hs = [(m.start(), m.group(1)) for m in re.finditer(r'<h3 class="system" id="([^"]*)"', html)]
    idx = [i for i, h in enumerate(hs) if h[1] == sysid]
    if not idx:
        raise SystemExit('no system header id=%r' % sysid)
    s = hs[idx[0]][0]
    e = hs[idx[0] + 1][0] if idx[0] + 1 < len(hs) else html.find('<script')
    return [b for b in briefs(html) if s < b.start < e]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    batch, sysid = argv[0], argv[1]
    opt = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
    excl = set(opt('--exclude', '').split(',')) - {''}
    prefix = opt('--prefix', '04')
    html, base = base_page(batch)
    bl = [b for b in section_briefs(html, sysid) if b.id not in excl]
    if '--per' in argv:
        per = int(opt('--per'))
        groups = [bl[i:i + per] for i in range(0, len(bl), per)]
        ng = len(groups)
    else:
        ng = int(opt('--groups', 5))
        groups = [[] for _ in range(ng)]
        for b in sorted(bl, key=lambda x: -(x.end - x.start)):
            min(groups, key=lambda g: sum(x.end - x.start for x in g)).append(b)
    rules = open(os.path.join(HERE, 'RULES_voice.md'), encoding='utf-8').read()
    rules = re.sub(r'^# .*\n', '', rules, count=1).strip()
    rules = re.sub(r'^(#{1,4}) ', lambda m: '#' * (len(m.group(1)) + 2) + ' ', rules, flags=re.M)
    named = '--outdir' in argv
    outdir = os.path.join(WS, opt('--outdir')) if named else os.path.join(WS, 'repair', batch, 'voice')
    tag = '%s_%%d' % sysid if named else '%d'
    os.makedirs(outdir, exist_ok=True)
    base_rel = os.path.relpath(base, WS)
    for k, g in enumerate(groups, 1):
        g.sort(key=lambda b: b.start)
        edits = 'repair/%s/%s_voice_%s.json' % (batch, prefix, tag % k)
        cmd = 'python3 tools/verify_edits.py %s %s --voice' % (edits, base_rel)
        parts = ['# Voice packet %d of %d (%s, %s): %s' % (k, ng, batch, sysid, ', '.join(b.id for b in g)),
                 '**Instructions.** Everything you need is in this packet. Do not open index.html, the skill files or other '
                 'packets. Write your edits to `%s`, run `%s` from the workspace folder (Step2Haki/workspace) and loop until it '
                 'prints PASS (add `--report` to read your own claim map). Then reply with the 3 to 5 line report the rules ask for, including any acronym you skipped.' % (edits, cmd),
                 '## Rules\n' + rules,
                 '## Edit format (replace only)\n' + FORMAT,
                 '## Worked example (infant-stool .dp, round 2; passes the verifier)\n' + example(),
                 '## Briefs (%d): current HTML\n' % len(g) + '\n\n'.join(
                     '### `%s`: %s\n\n```html\n%s\n```' % (b.id, b.title, html[b.start:b.end]) for b in g)]
        out = os.path.join(outdir, 'packet_%s.md' % (tag % k))
        body = '\n\n'.join(parts) + '\n'
        open(out, 'w', encoding='utf-8').write(body)
        print('packet %d: %s | %d briefs (%s) | %d chars, ~%d tokens'
              % (k, os.path.relpath(out, WS), len(g), ' '.join(b.id for b in g), len(body), len(body) // 4))
    print('base: %s (index.html + %s non-voice edits) | %d briefs in %s, excluded: %s'
          % (base_rel, batch, len(bl), sysid, ','.join(sorted(excl)) or 'none'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
