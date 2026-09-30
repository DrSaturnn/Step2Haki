#!/usr/bin/env python3
"""make_s36.py: writes repair/s36/*.json (page setup: psych shelf + section, Type C CSS and transform patch).
Replayable: python3 repair/s36/gen/make_s36.py  (reads tools/typec/typec.css; writes the edits files only)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
B = os.path.dirname(HERE)

def dump(name, edits):
    with open(os.path.join(B, name), 'w', encoding='utf-8') as f:
        json.dump({'edits': edits}, f, indent=1, ensure_ascii=False)
        f.write('\n')

# 10: psych shelf goes live (third shelf after fm and peds; was a pending 'Psychiatry' placeholder)
dump('10_shelf_psych.json', [
 {'op': 'replace_global',
  'find': "var SHELVES=[['step2','Step 2'],['fm','Family Med'],['peds','Pediatrics'],\n"
          "             ['im','Medicine',1],['surg','Surgery',1],['obgyn','OB/GYN',1],\n"
          "             ['psych','Psychiatry',1],['neurology','Neurology',1]];",
  'with': "var SHELVES=[['step2','Step 2'],['fm','Family Med'],['peds','Pediatrics'],['psych','Psych'],\n"
          "             ['im','Medicine',1],['surg','Surgery',1],['obgyn','OB/GYN',1],\n"
          "             ['neurology','Neurology',1]];"},
 {'op': 'replace_global', 'find': '   One document, three views.', 'with': '   One document, four views.'},
])

# 20: Psychiatry & Behavioral Health section (id psych), nav group, SHORT tab label
SECTION = ('\n<!-- =================== PSYCH =================== -->\n'
           '<h3 class="system" id="psych">Psychiatry &amp; Behavioral Health <span class="n">0 topics</span></h3>\n'
           '<p class="system-note">Mood, anxiety, psychotic, substance use and behavioral topics.</p>\n')
PROV = '\n<div style="margin:70px 0 0;padding:22px 0 0;border-top:2px solid var(--rule)'
NAV_END = '    <a class="aq" href="#bs-adolescent-vax">Adolescent Immunization</a>\n  </div>\n</aside>'
dump('20_section_psych.json', [
 {'op': 'replace_global', 'find': PROV, 'with': SECTION + PROV},
 {'op': 'replace_global', 'find': NAV_END,
  'with': '    <a class="aq" href="#bs-adolescent-vax">Adolescent Immunization</a>\n    \n'
          '    <div class="sect">Psychiatry &amp; Behavioral Health <span class="count">0</span></div>\n  </div>\n</aside>'},
 {'op': 'replace_global', 'find': "obgyn:'OBGYN',prev:'PREV',strategy:'START',heme:'HEME'};",
  'with': "obgyn:'OBGYN',prev:'PREV',strategy:'START',heme:'HEME',psych:'PSYCH'};"},
])

# 30: one-time Type C setup: typec.css at the end of the main <style>, and the mnemonics() patch
css = open(os.path.join(WS, 'tools', 'typec', 'typec.css'), encoding='utf-8').read().rstrip('\n')
STYLE_END = '  #nav.sxon #navscroll > .shelfpick,#nav.sxon #modes,#nav.sxon #rvlaunch{display:none}\n}\n</style>'
T0 = "    if(hits.length < Math.ceil(lis.length*0.7) || lis.length<2) return;\n    var dl=document.createElement('dl'); dl.className='rows';"
dump('30_typec_setup.json', [
 {'op': 'replace_global', 'find': STYLE_END, 'with': STYLE_END[:-len('</style>')] + css + '\n</style>'},
 {'op': 'replace_global', 'find': T0, 'with': T0 + "\n    if(ul.classList.contains('mnem')) dl.classList.add('mnem');"},
])
print('wrote', sorted(x for x in os.listdir(B) if x.endswith('.json')))
