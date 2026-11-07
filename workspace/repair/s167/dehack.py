#!/usr/bin/env python3
"""dehack.py: s167 step 3, the specificity workarounds and !important that the layers make unnecessary.

1. `html:is([data-theme],:not([data-theme])) ` is removed from every selector in site/css (it outranked the old theme
   rules, which are now custom-property tokens in the last layer).
2. `!important` is removed from every declaration in site/css, except: layout/print.css (print overrides the inline
   styles of the screen view), the prefers-reduced-motion block, and the declarations kept in KEEP below with a reason.
A rule whose removal changed a computed style (tools/ui_check.js run) or that beats an inline style a script writes is
listed in KEEP as (file, selector text as it stands after step 1, property, reason); it keeps its !important or, with
property '(hack)', its workaround prefix.

  python3 repair/s167/dehack.py [--dry]     writes site/css and local/s167/dehack_changes.txt
"""
import glob, os, re, sys

WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSS = os.path.join(WS, 'site', 'css')
HACK = 'html:is([data-theme],:not([data-theme])) '
SKIP_FILES = {'layout/print.css'}

# (file, selector after step 1, property or '(hack)', reason)
KEEP = [
    ('components/bank.css', '.bankwrap .mcqwrap.qx-measure > .mcq .qx-rsn', 'display',
     'measure state: body .bankwrap .mcq.qx-hr.done .opts button .qx-rsn (0,6,2) outranks it; answered cards measured taller'),
    ('layout/sidebar.css', '#axn.axn-still .axn-dz,#axn.axn-still .axn-dzc,#axn.axn-still .axn-sys svg,#axn.axn-still .axn-fill,#axn.axn-still .axn-lens', 'transition',
     'still state: #axn .axn-dz:not(.on) .axn-dzc (1,3,0) outranks it; inactive zones animate on a still jump'),
    ('layout/sidebar.css', '#axn [hidden]', 'display',
     '#axn a.axn-b{display:flex} (1,1,1) outranks it; links the shelf filter hides would show'),
    # chunk 13: parity c4 vs base_fix (ui_check), each the winning rule on the base page that lost after the dehack
    ('components/brief.css', 'body .brief > h4::after', '(hack)', '.brief.nbme-linked > h4::after (0,2,2) set vertical-align 5px on linked headers (base 14px, phone 7px)', 13),
    ('components/brief.css', 'body .brief .dp .lbl', '(hack)', 'html:not([data-theme=dark]) .dp > span.lbl (0,3,2) set the accent color on the first-step labels (base var(--confirm))', 13),
    ('components/brief.css', 'body .brief .nbh', '(hack)', '.pearls.nbq .nbh (0,3,0) set 10px uppercase 800 on NBME pearl heads (base 13px, 700, no transform)', 13),
    ('components/hovercard.css', 'body .brief.sp .sp-pop-b', '(hack:font-size)', '.brief.sp .sp-thr span (0,3,1) set 13.5px on thread popover bodies (base 15px)', 13),
    ('components/table.css', 'body .brief .tw td:first-child', '(hack)', '.brief.sp .sp-dx td:first-child 650 and the phone .cluet 400 and .tierT 800 rules outranked the 700 first column', 13),
    ('components/brief.css', '.k-mild', 'width', 'figure.lcw:not(.lcc) .rk i and .lc-key i (14px, 15px) widened the mild key swatch (base 9px)', 13),
    ('components/mnemonic.css', '.brief dl.rows.mnem.ax-mn.ax-mn-bare', 'grid-template-columns', 'phone: .ax-mn.mn-key:not(.mn-wide) 56px column outranked the bare mnemonic 44px', 13),
    ('components/nbme.css', '.brief:has(li[data-nbme],.mcq[data-nbme]) > h4::after', 'content', '.brief.bs[data-nid]:not([data-src=aquifer]) > h4::after wrote UWorld on NBME-linked bs headers', 13),
    ('components/nbme.css', '.brief.nbme-linked > h4[data-nbme-n]::after', 'content', 'same: UWorld replaced NBME x n', 13),
    ('components/table.css', '.tw tbody.grp tr', 'background', 'phone: body .axm-flat .tw tbody tr background-color painted group rows (base none)', 13),
    ('components/table.css', '.tw tbody td:has(> span:only-child:empty)', 'display', 'phone: .tw table.dense ... td display flow-root showed empty cells (base none)', 13),
    ('components/table.css', 'html[data-theme="dark"][data-glass="tinted"] .tw tbody tr', 'background', 'tinted: the zebra and phone card rules outranked the tinted row tint', 13),
    ('components/table.css', '[data-theme="dark"] .tw table.cluet tbody tr', 'background', 'phone tinted: with the tinted row tint important again, the dark clue-table rows need theirs to stay clear', 13),
    ('components/table.css', '[data-theme="dark"] .tw tbody.grp tr', 'background', 'same, group rows', 13),
    ('components/bank.css', 'html[data-theme="dark"][data-glass="tinted"] .brief .mcq button', 'background-image', 'tinted: the answer-option hover rule replaced the tinted gradient with none', 13),
]


def keep(rel, sel, prop):
    return any(k[0] == rel and k[1] == sel and k[2] == prop for k in KEEP)


def split_decls(body):
    out, depth, cur = [], 0, ''
    for ch in body:
        depth += ch == '('
        depth -= ch == ')'
        if ch == ';' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def main(a):
    changes, n_hack, n_imp, kept = [], 0, 0, 0
    for f in sorted(glob.glob(os.path.join(CSS, '**', '*.css'), recursive=True)):
        rel = os.path.relpath(f, CSS)
        src = open(f, encoding='utf-8').read()
        out, in_rm = [], False
        for ln in src.splitlines(True):
            if 'reduced-motion' in ln and ln.lstrip().startswith('@media'):
                in_rm = True
            m = re.match(r'^([^{}@]*)\{(.*)\}(\s*)$', ln)
            if in_rm and ln.strip() == '}':
                in_rm = False
            if not m or rel in SKIP_FILES:
                out.append(ln); continue
            sel, body, tail = m.groups()
            new_sel = sel
            if HACK in sel:
                stripped = sel.replace(HACK, '')
                if keep(rel, stripped, '(hack)'):
                    kept += 1
                else:
                    new_sel = stripped; n_hack += sel.count(HACK)
                    changes.append('%s: hack  %s' % (rel, stripped[:150]))
            decls = split_decls(body)
            for i, d in enumerate(decls):
                if '!important' not in d or ':' not in d or in_rm:
                    continue
                prop = d.split(':', 1)[0].strip()
                if keep(rel, new_sel if new_sel == sel.replace(HACK, '') else sel.replace(HACK, ''), prop):
                    kept += 1; continue
                decls[i] = re.sub(r'\s*!important', '', d); n_imp += 1
                changes.append('%s: important  %s { %s }' % (rel, sel.replace(HACK, '')[:120], prop))
            out.append(new_sel + '{' + ';'.join(decls) + '}' + tail)
        new = ''.join(out)
        if new != src and '--dry' not in a:
            open(f, 'w', encoding='utf-8').write(new)
    os.makedirs(os.path.join(WS, 'local', 's167'), exist_ok=True)
    open(os.path.join(WS, 'local', 's167', 'dehack_changes.txt'), 'w').write('\n'.join(changes) + '\n')
    print('dehack: hack prefixes removed', n_hack, '; !important removed', n_imp, '; kept', kept, '(KEEP %d)' % len(KEEP))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
