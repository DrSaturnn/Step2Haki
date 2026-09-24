# Voice packet 4 of 5 (s30, gi): peutz-jeghers, rlq-pain, neonatal-jaundice, bs-umbilical

**Instructions.** Everything you need is in this packet. Do not open index.html, the skill files or other packets. Write your edits to `repair/s30/04_voice_4.json`, run `python3 tools/verify_edits.py repair/s30/04_voice_4.json scratch/s30_base.html --voice` from the workspace folder (Step2Haki/workspace) and loop until it prints PASS (add `--report` to read your own claim map). Then reply with the 3 to 5 line report the rules ask for, including any acronym you skipped.

## Rules
**Task:** rewrite prose in plain, clear, concise clinical voice. Same facts, same meaning, same keyed logic. Shorter is better.

**Scope:** `.dp`, `.rule`, `.pearls`, `.danger`, `.traps` text, and `p.sub` first segment only. Do not touch: `.vignette`, bank items (`ol.bank` and its `li`), tables, `.crit`, ids, attributes, `data-*`.

**Remove:**
- slogans and aphorisms;
- personification ("the urine is the decider", "the phone call is the decoy");
- paired contrasts written for rhythm ("X names the panel, Y names the disease");
- dramatic openers and closers ("The fever is not incidental", "never after it", "everything", "the whole question");
- rhetorical framing about the question itself ("the trap is", "this question tests") unless it is in `.traps`, where one plain sentence per trap is fine;
- filler transitions;
- em dashes in prose.

**Keep:**
- every clinical fact, number, cutoff and named test;
- every bold clinical term (you may reword around it, not drop or rename it). A bold span that is itself a slogan, a full-sentence aphorism or a rhetorical label may be reworded: list its old text in the op as `"reworded_bold": ["<old bold text>"]` (the verifier accepts only declared removals). Keep the rewrite bold if it still carries the key idea;
- standard clinical phrases such as "until proven otherwise";
- the "·" row separators and "`<b>Term</b> — definition`" structure where they already exist (that " — " is structural, the only em dash allowed);
- `.rule` starts with its existing label markup; other block labels (`<span class="lbl">`) stay unless the label itself is a slogan or rhetorical label, in which case reword it and list the old text in `"reworded_label": ["<old label>"]`.

**Model (approved by Jonathan):**
- Before: The phone call is the decoy and the urine is the decider. Every option is on the newborn screen, so a positive screen eliminates nothing. What separates them is that this infant has conjugated hyperbilirubinemia, a large liver, and a non-glucose reducing sugar in the urine after ten days of milk feeds. That triad is galactose-1-phosphate accumulating in a GALT-deficient liver: classic galactosemia. The fever is not incidental. Galactosemia predisposes to Escherichia coli sepsis, and a febrile 10-day-old is septic until cultured — the sepsis workup runs in parallel with the metabolic answer, never after it.
- After: Conjugated hyperbilirubinemia, a large liver, and a non-glucose reducing sugar in the urine after ten days of milk feeds indicate classic galactosemia (GALT deficiency; galactose-1-phosphate accumulates in the liver). Galactosemia predisposes to Escherichia coli sepsis, so start the sepsis workup and antibiotics while stopping lactose.
- Subtitle before: The screen names the panel, the presentation names the disease · handoff · conjugated, big liver, reducing sugar
- Subtitle after: Sick neonate with a positive newborn screen · conjugated jaundice, hepatomegaly, urine reducing sugar

**Learned from GI review:**
- Never state that a test excludes what the brief says needs a different test.
- Keep hedges and quantifiers that set strength ("rather than presumed", "any one of", "until").
- Restate stem facts only as the vignette gives them.
- Pairs-with claims about coverage must match the page.
- Strip internal and workflow text (batch notes, ledger, candidate, verified).
- Reread every changed sentence for grammar.

**Round 2 (after Jonathan's review of the live GI sample; no drift is the top priority):**
- One idea per sentence, about 25 words at most. Split arrow chains: at most one → per sentence. Where a block lists parallel items (for example three benign complaints), a "·"-separated row list is allowed in `.dp`, `.pearls`, `.danger` and `.rule`.
- No framing or meta sentences. Nothing that talks about the answer, the tier, the finding, the question, the stem or the decision instead of stating the clinical fact. "X and Y set the answer", "Two mimics change the tier" and "Parental distress is not a finding" become what to do, e.g. "Reassure; a thriving infant needs no formula change, suppository or stool workup."
- Acronyms: at first use within each block, bold the acronym and write it out in parentheses, unbolded: `<b>FPIES</b> (food protein-induced enterocolitis syndrome)`. Later uses in the same block stay plain. Common units and immunoglobulin names (IgE, IgA) count as acronyms only if a learner might not expand them; list every acronym you skip in your report. Do not create a "`<b>Term</b> — definition`" pattern by accident (never follow the bold acronym with " — ").
- Remove emphasis bold on non-terms (for example a bold "and"), and declare it in `reworded_bold`.
- The approved galactosemia `.dp` text stays unless it breaks a rule above.

**Drift protocol (mandatory; the verifier checks it):** every replace op carries a claim map.
- `"claims"`: every atomic clinical claim in the OLD text, one short sentence each, with exactly one of:
  `"to"`: the NEW sentence that now carries it, quoted exactly as visible text (tags stripped); or
  `"carried_by"`: a quoted passage elsewhere in the same brief (another block, a table cell or a bank item) that already states it; or
  `"dropped"`: the reason, allowed only for non-clinical framing. A dropped claim may not contain a number, drug, test or cutoff.
- `"new_claims"`: every clinical claim in the NEW text, each with `"from"`: the exact `"claim"` text of the old claim it came from, or `"expansion"` for a written-out acronym (the expansion must be the standard one).
- The verifier fails an op with no claims list, an unmapped claim, a quote that is not in the new brief, a new claim without `"from"` (or with a `"from"` that matches no old claim), or a dropped claim carrying clinical content. `--report` prints old text, new text and the claim map for the reviewer.

If a block is already plain, leave it. If you are unsure a rewrite keeps the meaning, leave it and list it.

**Output:** edits JSON (replace ops, anchors unique within the brief) and a report of 3 to 5 lines: blocks changed, blocks left, anything uncertain.

## Edit format (replace only)
One JSON file: `{"edits": [op, op, ...]}`, replace ops only, applied in order:

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
```

## Worked example (infant-stool .dp, round 2; passes the verifier)
Before (visible text):

> Three benign stool complaints present in a thriving, well-appearing infant or child with alarmed parents; the stool and the timing set the answer. Straining and screaming for minutes, then a normal soft stool, under 9 months, is infant dyschezia → reassurance only. Painless blood-streaked stools in a well infant under 6 months is food protein-induced allergic proctocolitis → eliminate cow's milk and soy from the maternal diet, or use an extensively hydrolyzed formula. Watery diarrhea and bloating after dairy is reintroduced following gastroenteritis is secondary lactase deficiency → temporary lactose avoidance, no workup. Two mimics change the tier, and both are ill-appearing: FPIES (profuse vomiting and lethargy 1–4 h after the trigger, non-IgE) needs fluids, and IgE-mediated allergy (urticaria, wheeze, anaphylaxis within minutes) needs epinephrine. Parental distress is not a finding; a thriving infant does not need a formula change, a suppository, or a stool workup.

After:

> These three benign stool complaints occur in a thriving, well-appearing infant or child whose parents are worried. Straining and screaming for minutes, followed by a normal soft stool in an infant under 9 months, is infant dyschezia → reassurance only. Painless blood-streaked stools in a well infant under 6 months are food protein-induced allergic proctocolitis. Treat it by removing cow's milk and soy from the maternal diet, or by using an extensively hydrolyzed formula. Watery diarrhea and bloating after dairy is reintroduced following gastroenteritis are secondary lactase deficiency → temporary lactose avoidance, with no workup. Two mimics present with an ill-appearing infant. FPIES (food protein-induced enterocolitis syndrome) causes profuse vomiting and lethargy 1–4 h after the trigger; it is non-IgE and needs fluids. IgE-mediated allergy causes urticaria, wheeze or anaphylaxis within minutes and needs epinephrine. Reassure the parents; a thriving infant needs no formula change, suppository or stool workup.

Skipped acronym: IgE (immunoglobulin name a learner expands). The edits entry:

```json
{
 "op": "replace",
 "brief": "infant-stool",
 "find": "<p>Three benign stool complaints present in a <b>thriving, well-appearing</b> infant or child with alarmed parents; the <b>stool</b> and the <b>timing</b> set the answer. Straining and screaming for minutes, then a <b>normal soft stool</b>, under 9 months, is <b>infant dyschezia</b> → reassurance only. <b>Painless blood-streaked stools</b> in a well infant under 6 months is <b>food protein-induced allergic proctocolitis</b> → eliminate cow's milk and soy from the maternal diet, or use an extensively hydrolyzed formula. Watery diarrhea and bloating <b>after dairy is reintroduced</b> following gastroenteritis is <b>secondary lactase deficiency</b> → temporary lactose avoidance, no workup.</p>\n<p>Two mimics change the tier, and both are <b>ill-appearing</b>: <b>FPIES</b> (profuse vomiting and lethargy 1–4 h after the trigger, non-IgE) needs fluids, and <b>IgE-mediated</b> allergy (urticaria, wheeze, anaphylaxis within minutes) needs epinephrine. Parental distress is not a finding; a thriving infant does not need a formula change, a suppository, or a stool workup.</p>",
 "with": "<p>These three benign stool complaints occur in a <b>thriving, well-appearing</b> infant or child whose parents are worried. Straining and screaming for minutes, followed by a <b>normal soft stool</b> in an infant under 9 months, is <b>infant dyschezia</b> → reassurance only. <b>Painless blood-streaked stools</b> in a well infant under 6 months are <b>food protein-induced allergic proctocolitis</b>. Treat it by removing cow's milk and soy from the maternal diet, or by using an extensively hydrolyzed formula. Watery diarrhea and bloating <b>after dairy is reintroduced</b> following gastroenteritis are <b>secondary lactase deficiency</b> → temporary lactose avoidance, with no workup.</p>\n<p>Two mimics present with an <b>ill-appearing</b> infant. <b>FPIES</b> (food protein-induced enterocolitis syndrome) causes profuse vomiting and lethargy 1–4 h after the trigger; it is non-IgE and needs fluids. <b>IgE-mediated</b> allergy causes urticaria, wheeze or anaphylaxis within minutes and needs epinephrine. Reassure the parents; a thriving infant needs no formula change, suppository or stool workup.</p>",
 "note": "round 2 worked example: .dp",
 "reworded_bold": [
  "stool",
  "timing"
 ],
 "claims": [
  {
   "claim": "The three stool complaints are benign.",
   "to": "These three benign stool complaints occur in a thriving, well-appearing infant or child whose parents are worried."
  },
  {
   "claim": "They occur in a thriving, well-appearing infant or child.",
   "to": "These three benign stool complaints occur in a thriving, well-appearing infant or child whose parents are worried."
  },
  {
   "claim": "The parents are alarmed.",
   "to": "These three benign stool complaints occur in a thriving, well-appearing infant or child whose parents are worried."
  },
  {
   "claim": "The stool and the timing set the answer.",
   "dropped": "framing about the answer; the stool and timing details are stated in each of the next sentences"
  },
  {
   "claim": "Straining and screaming for minutes, then a normal soft stool, under 9 months, is infant dyschezia.",
   "to": "Straining and screaming for minutes, followed by a normal soft stool in an infant under 9 months, is infant dyschezia → reassurance only."
  },
  {
   "claim": "Infant dyschezia needs reassurance only.",
   "to": "Straining and screaming for minutes, followed by a normal soft stool in an infant under 9 months, is infant dyschezia → reassurance only."
  },
  {
   "claim": "Painless blood-streaked stools in a well infant under 6 months are food protein-induced allergic proctocolitis.",
   "to": "Painless blood-streaked stools in a well infant under 6 months are food protein-induced allergic proctocolitis."
  },
  {
   "claim": "Proctocolitis is treated by eliminating cow's milk and soy from the maternal diet, or with an extensively hydrolyzed formula.",
   "to": "Treat it by removing cow's milk and soy from the maternal diet, or by using an extensively hydrolyzed formula."
  },
  {
   "claim": "Watery diarrhea and bloating after dairy is reintroduced following gastroenteritis is secondary lactase deficiency.",
   "to": "Watery diarrhea and bloating after dairy is reintroduced following gastroenteritis are secondary lactase deficiency → temporary lactose avoidance, with no workup."
  },
  {
   "claim": "Secondary lactase deficiency needs temporary lactose avoidance and no workup.",
   "to": "Watery diarrhea and bloating after dairy is reintroduced following gastroenteritis are secondary lactase deficiency → temporary lactose avoidance, with no workup."
  },
  {
   "claim": "Two mimics change the tier.",
   "dropped": "framing about the tier; the two mimics and their treatments are stated next"
  },
  {
   "claim": "Both mimics are ill-appearing.",
   "to": "Two mimics present with an ill-appearing infant."
  },
  {
   "claim": "FPIES gives profuse vomiting and lethargy 1–4 h after the trigger.",
   "to": "FPIES (food protein-induced enterocolitis syndrome) causes profuse vomiting and lethargy 1–4 h after the trigger; it is non-IgE and needs fluids."
  },
  {
   "claim": "FPIES is non-IgE.",
   "to": "FPIES (food protein-induced enterocolitis syndrome) causes profuse vomiting and lethargy 1–4 h after the trigger; it is non-IgE and needs fluids."
  },
  {
   "claim": "FPIES needs fluids.",
   "to": "FPIES (food protein-induced enterocolitis syndrome) causes profuse vomiting and lethargy 1–4 h after the trigger; it is non-IgE and needs fluids."
  },
  {
   "claim": "IgE-mediated allergy gives urticaria, wheeze or anaphylaxis within minutes.",
   "to": "IgE-mediated allergy causes urticaria, wheeze or anaphylaxis within minutes and needs epinephrine."
  },
  {
   "claim": "IgE-mediated allergy needs epinephrine.",
   "to": "IgE-mediated allergy causes urticaria, wheeze or anaphylaxis within minutes and needs epinephrine."
  },
  {
   "claim": "Parental distress is not a finding.",
   "to": "Reassure the parents; a thriving infant needs no formula change, suppository or stool workup."
  },
  {
   "claim": "A thriving infant does not need a formula change, a suppository, or a stool workup.",
   "to": "Reassure the parents; a thriving infant needs no formula change, suppository or stool workup."
  }
 ],
 "new_claims": [
  {
   "claim": "The three stool complaints are benign and occur in a thriving, well-appearing infant or child with worried parents.",
   "from": "The three stool complaints are benign."
  },
  {
   "claim": "Straining and screaming for minutes, then a normal soft stool, under 9 months, is infant dyschezia.",
   "from": "Straining and screaming for minutes, then a normal soft stool, under 9 months, is infant dyschezia."
  },
  {
   "claim": "Infant dyschezia needs reassurance only.",
   "from": "Infant dyschezia needs reassurance only."
  },
  {
   "claim": "Painless blood-streaked stools in a well infant under 6 months are food protein-induced allergic proctocolitis.",
   "from": "Painless blood-streaked stools in a well infant under 6 months are food protein-induced allergic proctocolitis."
  },
  {
   "claim": "Treat proctocolitis by removing cow's milk and soy from the maternal diet, or with an extensively hydrolyzed formula.",
   "from": "Proctocolitis is treated by eliminating cow's milk and soy from the maternal diet, or with an extensively hydrolyzed formula."
  },
  {
   "claim": "Watery diarrhea and bloating after dairy is reintroduced following gastroenteritis are secondary lactase deficiency.",
   "from": "Watery diarrhea and bloating after dairy is reintroduced following gastroenteritis is secondary lactase deficiency."
  },
  {
   "claim": "Secondary lactase deficiency needs temporary lactose avoidance and no workup.",
   "from": "Secondary lactase deficiency needs temporary lactose avoidance and no workup."
  },
  {
   "claim": "Two mimics present with an ill-appearing infant.",
   "from": "Both mimics are ill-appearing."
  },
  {
   "claim": "FPIES stands for food protein-induced enterocolitis syndrome.",
   "from": "expansion"
  },
  {
   "claim": "FPIES causes profuse vomiting and lethargy 1–4 h after the trigger.",
   "from": "FPIES gives profuse vomiting and lethargy 1–4 h after the trigger."
  },
  {
   "claim": "FPIES is non-IgE and needs fluids.",
   "from": "FPIES is non-IgE."
  },
  {
   "claim": "IgE-mediated allergy causes urticaria, wheeze or anaphylaxis within minutes and needs epinephrine.",
   "from": "IgE-mediated allergy gives urticaria, wheeze or anaphylaxis within minutes."
  },
  {
   "claim": "Reassure the parents.",
   "from": "Parental distress is not a finding."
  },
  {
   "claim": "A thriving infant needs no formula change, suppository or stool workup.",
   "from": "A thriving infant does not need a formula change, a suppository, or a stool workup."
  }
 ]
}
```

## Briefs (4): current HTML
### `peutz-jeghers`: Peutz-Jeghers Syndrome

```html
<div class="brief" id="peutz-jeghers" data-shelf="peds fm" data-nid="1482886927273 1482886932317" data-bp="gi">
<h4>Peutz-Jeghers Syndrome</h4>
<p class="sub">Macules on the lips, polyps in the gut &middot; the exam finding that redirects the workup</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 13-year-old girl, 2 months of fatigue worse after walking to class; menarche at 12, regular 28-day cycles, menses 6&ndash;7 days with cramping; well-balanced diet, no medications &middot; <b>Exam</b> &mdash; pale conjunctivae; <b>a few brown macules on the lips and buccal mucosa</b>; abdomen soft, no organomegaly &middot; <b>Labs</b> &mdash; haemoglobin <b>8.4</b>, MCV <b>70</b>, platelets and leukocytes normal &middot; <b>Q</b> &mdash; the best next step; options spanned ACTH stimulation, bone marrow evaluation, iron with oral contraception, lead level and upper and lower endoscopy</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>A 13-year-old with six-day menses and microcytic anaemia suggests menstrual iron deficiency, but <b>brown macules on the lips and buccal mucosa</b> are the mucocutaneous marker of <b>Peutz-Jeghers syndrome</b>. The anaemia is then occult bleeding from hamartomatous polyps, not menstrual loss. The next step is <b>upper and lower endoscopy</b>.</p>
<p>Iron and an oral contraceptive treat the anaemia but leave the syndrome undiagnosed.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Peutz-Jeghers</b> &mdash; autosomal dominant, tumour-suppressor mutation, with mucocutaneous pigmented macules and two or more gastrointestinal hamartomatous polyps &middot; <b>Macule distribution</b> &mdash; lips, buccal mucosa, palms and soles &middot; <b>Polyp complications</b> &mdash; obstruction or intussusception, anaemia from bleeding, rectal prolapse &middot; <b>Cancer risk</b> &mdash; gastrointestinal, breast and genital tract &middot; <b>Surveillance</b> &mdash; annual haemoglobin plus upper and lower endoscopy</div>
<table data-mask="last">
<caption>Pigmentation plus anaemia &mdash; the differential<span class="cap-sub">where the pigment is decides</span></caption>
<thead><tr><th>Diagnosis</th><th>The pigment</th><th>The anaemia</th><th>What to do</th></tr></thead>
<tbody>
<tr><td><b>Peutz-Jeghers</b></td><td><b>Discrete brown macules</b> on lips, buccal mucosa, palms and soles</td><td>Microcytic, from occult polyp bleeding</td><td>Upper and lower endoscopy; genetic testing</td></tr>
<tr><td>Primary adrenal insufficiency</td><td><b>Diffuse</b> hyperpigmentation, worst on pressure and sun-exposed areas</td><td>Usually normocytic if present</td><td>ACTH stimulation test</td></tr>
<tr><td>Lead poisoning</td><td><b>Blue gingival line</b> at the tooth margin</td><td>Microcytic with basophilic stippling</td><td>Blood lead level</td></tr>
<tr><td>Menstrual iron deficiency</td><td>None</td><td>Microcytic, from heavy or prolonged menses</td><td>Iron; hormonal control if bleeding is heavy</td></tr>
<tr><td>Marrow failure or malignancy</td><td>None</td><td>Usually normocytic, with other cytopenias</td><td>Bone marrow evaluation</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>CBC with MCV</td><td>First</td><td>Microcytic anemia, other cell lines <b>normal</b></td><td>Iron deficiency from blood loss, not marrow failure</td></tr>
<tr><td>Upper and lower endoscopy with polyp biopsy</td><td>Confirms</td><td>Two or more <b>hamartomatous</b> polyps</td><td>Peutz-Jeghers with the mucocutaneous macules; the polyps are the bleeding source</td></tr>
<tr><td>STK11 genetic testing</td><td>Confirms</td><td><b>STK11</b> mutation</td><td>Autosomal dominant: test first-degree relatives</td></tr>
<tr><td>Annual hemoglobin with periodic upper and lower endoscopy</td><td>Screen</td><td>New <b>anemia</b> or polyps</td><td>Lifelong surveillance, plus breast and genital tract cancer screening</td></tr>
<tr><td>ACTH stimulation test or lead level</td><td>Skip</td><td>Pigment is <b>discrete</b> macules on lips and buccal mucosa</td><td>Wrong distribution for Addison disease (diffuse) or lead (gingival line)</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="next" data-d1="Iron therapy and oral contraception only" data-d2="Lead level" data-src="uworld" data-item-id="q_ee9358efb98dc94119ee" data-item-version="1" data-item-status="ready" data-key-id="o_f4cf55085de3d6051d81" data-d1-id="o_673d62a1979d52f8f448" data-d2-id="o_c9aa24af1f1ed78dedce">13 year old with fatigue, pale conjunctivae, haemoglobin 8.4 with MCV 70, and brown macules on the lips and buccal mucosa &rarr; <b>Upper and lower endoscopy</b> &rarr; Peutz-Jeghers &mdash; the macules convert an iron-deficiency workup into a polyposis one</li>
<li data-type="dx" data-d1="Familial adenomatous polyposis" data-d2="Addison disease" data-src="uworld" data-item-id="q_e3f050dd7f5ec502aefe" data-item-version="1" data-item-status="ready" data-key-id="o_657fb0dd4c230dae5072" data-d1-id="o_f37ee85c203d35900287" data-d2-id="o_cb1101c7e02c6552cc9e">Adolescent with hyperpigmented macules on lips, buccal mucosa and palms, and recurrent abdominal pain from intussusception &rarr; <b>Peutz-Jeghers syndrome</b> &rarr; Hamartomatous polyps, autosomal dominant</li>
<li data-type="mech" data-d1="Autoimmune destruction of parietal cells" data-d2="Impaired iron absorption in the duodenum" data-src="uworld" data-item-id="q_c8b53b5face81d662d7d" data-item-version="1" data-item-status="ready" data-key-id="o_a31391c3a163214bdeda" data-d1-id="o_a4581a6a3dfdd186b7e1" data-d2-id="o_6fc4a94e92e86942c3e2">How Peutz-Jeghers polyps produce a microcytic anaemia &rarr; <b>Chronic occult blood loss from the polyps</b> &rarr; Iron deficiency, not marrow failure &mdash; the MCV is the clue</li>
<li data-type="screen" data-d1="Colonoscopy only, starting at age 50" data-d2="Annual abdominal ultrasonography" data-src="uworld" data-item-id="q_61789b9eedb055588a80" data-item-version="2" data-item-status="ready" data-key-id="o_589896208dac2dd84ad5" data-d1-id="o_ace8457aabc75e956323" data-d2-id="o_e23635fda12837fdc3f2" data-lead-in="Which of the following is the most appropriate surveillance?">Patient with established Peutz-Jeghers syndrome &rarr; <b>Annual haemoglobin with periodic upper and lower endoscopy</b> &rarr; Plus awareness of breast and genital tract risk</li>
<li data-type="dx" data-d1="Peutz-Jeghers syndrome" data-d2="Lead poisoning" data-src="uworld" data-item-id="q_5a2b077a40b6cf04c3cc" data-item-version="1" data-item-status="ready" data-key-id="o_591fec5e0acf9c0490df" data-d1-id="o_61dd9d948cbd2ad5e1a3" data-d2-id="o_ddd12afbf848a4d79c8a">Adolescent with fatigue, generalised hyperpigmentation worst over elbows and knees, anorexia and weight loss &rarr; <b>Primary adrenal insufficiency</b> &rarr; Diffuse pigmentation in sun- and pressure-exposed areas, not discrete macules</li>
<li data-type="dx" data-d1="Peutz-Jeghers syndrome" data-d2="Iron deficiency from menorrhagia" data-src="uworld" data-item-id="q_e9c2a8c363fd27f18265" data-item-version="1" data-item-status="ready" data-key-id="o_2d0a59a28e81b30b70a8" data-d1-id="o_ffb5ca8e08be9372eefd" data-d2-id="o_77b8ab3375e90c71221c">Child with microcytic anaemia and a blue line along the gingival margin &rarr; <b>Lead poisoning</b> &rarr; Gingival lead lines, not mucosal macules</li>
<li data-type="avoid" data-d1="Upper and lower endoscopy" data-d2="Genetic testing for the family" data-src="uworld" data-item-id="q_0a5c7897d4e545a48267" data-item-version="1" data-item-status="ready" data-key-id="o_7b7132c9e7ab75c7bfe7" data-d1-id="o_3b5f1db1db4b4d1a454c" data-d2-id="o_7f301b0fbc4ae995e2cc">Adolescent girl with microcytic anaemia, regular 6-day menses and oral pigmented macules; which management is inadequate &rarr; <b>Iron and oral contraception alone</b> &rarr; It treats the anaemia and ignores the syndrome causing it</li>
</ol>
<div class="danger"><span class="lbl">Gates</span> <b>Microcytic anaemia in an adolescent girl is not automatically menstrual</b> &mdash; check the mouth, palms and family history &middot; <b>Intussusception in an older child</b> has a lead point until proven otherwise; a hamartoma can be one &middot; Cancer risk includes breast and genital tract, so surveillance is lifelong &middot; Normal platelet and leukocyte counts argue against marrow failure</div>
<div class="pearls"><span class="lbl">Pearls</span> The macules can fade in adulthood but the polyp risk persists, so a normal skin examination in a parent does not exclude the family history &middot; <b>Hamartomatous</b>, not adenomatous, which is why the cancer risk is broader than colon alone &middot; MCV separates the bleeding causes from the marrow causes before any imaging &middot; Perioral pigmentation with intussusception in a child is the classic presentation</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Familial Adenomatous Polyposis</b> covers the adenomatous syndromes and colectomy timing; this brief covers the hamartomatous one. Ask: where exactly is the pigment, and what is the MCV?</div>
<div class="rule"><span class="lbl">Transferable rule</span> When one finding does not fit an otherwise ordinary explanation, that finding usually determines the diagnosis.</div>
<div class="traps">
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">An adolescent girl with menses and microcytic anaemia suggests menstrual iron deficiency until the oral macules are noted.</span></div>
<div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Addison disease and lead poisoning also cause pigmentation, but in a different distribution.</span></div>
</div>
</div>
```

### `rlq-pain`: Right Lower Quadrant Pain

```html
<div class="brief" id="rlq-pain" data-shelf="fm peds" data-nid="1506285146600" data-bp="gi">
<h4>Right Lower Quadrant Pain</h4>
<p class="sub">appendix, ileocecum, or neither &middot; Is there profuse mucoid diarrhea, and is there a sick contact?</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 17 yo, migratory periumbilical to right lower quadrant pain, 12 mucoid stools in 24 hours, fever, sibling with the same illness &middot; <b>Q</b> &mdash; the most likely diagnosis; options spanned Campylobacter infection, acute appendicitis and Escherichia coli O157:H7 infection</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Fever, right lower quadrant tenderness, and a neutrophil-predominant leukocytosis occur in both appendicitis and ileocecitis and do not discriminate. Two findings that appendicitis does not explain are <b>twelve mucus-containing loose stools in 24 hours</b> and a <b>brother with the same illness</b>. Both fit <b>infectious ileocecitis</b> (pseudoappendicitis) from organisms with an ileocecal predilection, <i>Campylobacter jejuni</i> and <i>Yersinia enterocolitica</i>. The migratory periumbilical-to-right-lower-quadrant pain also fits: <i>Campylobacter</i> may infect the jejunum first and then spread to the ileum and cecum.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Infectious ileocecitis (pseudoappendicitis)</b> &mdash; right lower quadrant pain from acute ileocecitis caused by organisms with an ileocecal predilection, specifically <b><i>Yersinia enterocolitica</b></i> and <b><i>Campylobacter jejuni</b></i> &middot; <b>The discriminating symptom</b> &mdash; profuse watery or <b>mucoid</b> diarrhea, which acute appendicitis is not classically associated with &middot; <b>The imaging tell</b> &mdash; ileocecal inflammation and mesenteric lymphadenopathy <b>with sparing of the appendix</b> &middot; <b>When <i>Campylobacter</i> earns antibiotics</b> &mdash; duration beyond 7 days, bloody stools, high fevers, or a patient who is pregnant, immunocompromised, or elderly</div>
<div class="pearls"><span class="lbl">Pertinent positives &amp; negatives</span> <b>Twelve mucus-containing stools in 24 hours</b> &mdash; profuse mucoid diarrhea, not a feature of appendicitis &middot; <b>A brother with the same illness, now improving</b> &mdash; a shared exposure, which appendicitis does not explain; the sibling's course fits a self-limited enteritis &middot; <b>Migratory periumbilical → right lower quadrant pain</b> &mdash; classic for appendicitis, but also explained by jejunal-then-ileocecal spread of <i>Campylobacter</i> &middot; <b>Right lower quadrant tenderness without rebound or rigidity</b> &mdash; no peritonitis; this argues against an advanced or perforated appendix without excluding an early one &middot; <b>Fever 38.8 °C with WBC 13,700 and 80% neutrophils</b> &mdash; present in both diagnoses; does not discriminate &middot; <b>Mucus in the stool</b> &mdash; argues against norovirus, whose stools are watery without mucus &middot; <b>No hematochezia in the patient, with fever above 38.5 °C</b> &mdash; argues against <i>E. coli</i> O157:H7, which usually brings hematochezia within 1–3 days and rarely high fever &middot; <b>Age 17</b> &mdash; diverticulitis is exceedingly rare at this age</div>
<table data-mask="3">
<caption>Right lower quadrant pain in a young patient — the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th><th>Excluded here by</th></tr></thead>
<tbody>
<tr><td><b>Infectious ileocecitis</b> — <i>Campylobacter</i>, <i>Yersinia</i></td><td>Undercooked poultry or a sick contact; ileocecal predilection; fever with mucoid or bloody diarrhea</td><td><b>Profuse mucoid diarrhea with right lower quadrant pain</b>; imaging spares the appendix</td><td>— (the answer)</td></tr>
<tr><td>Acute appendicitis</td><td>Luminal obstruction; migratory periumbilical to right lower quadrant pain, anorexia, vomiting</td><td><b>Little or no diarrhea</b>, progressive localized peritonitis, no sick contacts</td><td>Twelve mucoid stools and an affected sibling</td></tr>
<tr><td><i>E. coli</i> O157:H7</td><td>Shiga toxin colitis; undercooked beef or a point-source outbreak</td><td><b>Hematochezia within 1–3 days</b> and fever above 38.5 °C is rare</td><td>The patient has no bloody stools and a temperature of 38.8 °C</td></tr>
<tr><td>Norovirus</td><td>Common-source outbreak; prominent vomiting</td><td><b>Watery stools without mucus</b>, normal white blood cell count</td><td>Mucoid stools with a neutrophilic leukocytosis</td></tr>
<tr><td>Cecal diverticulitis</td><td>Right-sided diverticular inflammation</td><td>Right lower quadrant pain and fever <b>in an adult</b>; mild or no diarrhea</td><td>Exceedingly rare at 17; profuse mucoid diarrhea</td></tr>
<tr><td>Crohn ileitis ⚠︎</td><td>Chronic transmural ileal inflammation</td><td><b>Weeks to months</b> of pain, weight loss, perianal disease</td><td>Three days of illness with a sick contact</td></tr>
</tbody></table>
<div class="danger"><span class="lbl">Management, in one line</span> <i>Campylobacter</i> is treated <b>supportively</b> because it is usually self-limited within seven days; antibiotics are reserved for the severe or high-risk cases listed above, and <b>surgery is not required</b> in infectious ileocecitis <i>(all in-context)</i>.</div>
<div class="pearls"><span class="lbl">Decision spine</span> <b>Is there diarrhea, and how much?</b> &mdash; Twelve mucoid stools → argues against appendicitis &middot; <b>Is there a sick contact?</b> &mdash; A brother with the same illness → an infectious exposure, not a luminal obstruction &middot; <b>Are there peritoneal signs?</b> &mdash; No rebound, no rigidity → not a surgical abdomen at this moment &middot; <b>What is the stool like?</b> &mdash; Mucoid, with or without blood → invasive bacterial rather than viral &middot; <b>Which organisms live at the ileocecum?</b> &mdash; <i>Campylobacter</i> and <i>Yersinia</i></div>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>CBC</td><td>First</td><td>Neutrophil-predominant <b>leukocytosis</b></td><td>Shared by appendicitis and ileocecitis; decides nothing</td></tr>
</tbody>
<tbody class="grp">
<tr><td>Ultrasound or CT of the abdomen</td><td>By branch</td><td>Ileocecal inflammation with a <b>spared appendix</b></td><td>Infectious ileocecitis: supportive care, no surgery</td></tr>
<tr><td></td><td></td><td><b>Inflamed</b> appendix</td><td>Acute appendicitis: surgical consultation</td></tr>
</tbody>
<tbody>
<tr><td>Stool culture or PCR</td><td>Confirms</td><td><b>Campylobacter</b> or Yersinia</td><td>Names the organism; a susceptibility panel alone is not a reason to treat</td></tr>
<tr><td>Colonoscopy with ileal intubation</td><td>By branch</td><td><b>Chronic</b> ileal inflammation on biopsy</td><td>Crohn ileitis: months of pain, weight loss, perianal disease</td></tr>
<tr><td>Diagnostic laparoscopy</td><td>Skip</td><td>Invasive when <b>imaging</b> can decide</td><td>Image first when the examination leaves the diagnosis unclear</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="dx" data-d1="Acute appendicitis" data-d2="Escherichia coli O157:H7 infection" data-item-id="q_2084b43af50a5525afa6" data-item-version="1" data-item-status="ready" data-key-id="o_6ce0247055375049b304" data-d1-id="o_86776ffc075854379f04" data-d2-id="o_6023bb5b94e753e99e65">17 yo with migratory periumbilical to right lower quadrant pain, 12 mucoid stools in 24 hours, fever, and a sibling with the same illness &rarr; <b>Campylobacter infection</b> &rarr; Infectious ileocecitis</li>
<li data-type="next" data-d1="Appendectomy" data-d2="Empiric ciprofloxacin on presentation" data-item-id="q_c4e6b08e6f8650429bf4" data-item-version="2" data-item-status="ready" data-key-id="o_34421ae4e2ee5de78614" data-d1-id="o_3d755c30b2b353668bd0" data-d2-id="o_b415f4892ff452348e88">A hemodynamically stable 17-year-old with migratory periumbilical-to-right-lower-quadrant pain, 12 mucoid stools in 24 hours, fever, and a sibling with the same illness has had 3 days of symptoms without bloody stools. &rarr; <b>Supportive care with stool studies</b> &rarr; Usually self-limited within 7 days</li>
<li data-type="next" data-d1="Continue supportive care alone" data-d2="Urgent colectomy" data-item-id="q_a16d32168d8253779248" data-item-version="2" data-item-status="ready" data-key-id="o_5b281fcc5b12540a9fd3" data-d1-id="o_c0f1dc47ab6f5924a654" data-d2-id="o_b417404355955eab896d">A 17-year-old with migratory periumbilical-to-right-lower-quadrant pain, 12 mucoid stools in 24 hours, fever, and a sibling with the same illness now presents on day 9 with bloody stools and fever to 39.5 °C. &rarr; <b>Start antimicrobial therapy</b> &rarr; A high-risk criterion is met</li>
<li data-type="next" data-d1="Stool studies with supportive care" data-d2="Outpatient antibiotics and reassessment in 48 hours" data-item-id="q_6d05d3039eac5223abbb" data-item-version="1" data-item-status="ready" data-key-id="o_b18cc96ff2e75661ba22" data-d1-id="o_7ff8c0c031b15541af63" data-d2-id="o_1c6aab4b0e8a5c25ac29">17 yo with right lower quadrant pain, anorexia and vomiting but no diarrhea, with rebound tenderness &rarr; <b>Surgical consultation for appendectomy</b> &rarr; The classic script without the stool</li>
<li data-type="next" data-d1="Immediate diagnostic laparoscopy" data-d2="Discharge with symptomatic treatment" data-item-id="q_abe495f14e0150a09426" data-item-version="1" data-item-status="ready" data-key-id="o_2ac1c0e7ab4954329df2" data-d1-id="o_ae5edc2b44995a41bec3" data-d2-id="o_8c38a23e220a55d6b786">17 yo with right lower quadrant pain and diarrhea in whom the diagnosis remains unclear after examination &rarr; <b>Cross-sectional imaging of the abdomen</b> &rarr; Ileocecal inflammation with a spared appendix</li>
<li data-type="next" data-d1="Stool culture and supportive care" data-d2="Appendectomy" data-item-id="q_2b77ff64ccf6572d82a1" data-item-version="1" data-item-status="ready" data-key-id="o_33d0a9b441965467b6aa" data-d1-id="o_81e6c47c95a05b728dd7" data-d2-id="o_51ae6a78d02a50658421">16 yo with months of right lower quadrant pain, weight loss and a perianal fistula &rarr; <b>Colonoscopy with ileal intubation</b> &rarr; Crohn ileitis</li>
<li data-type="dx" data-d1="Campylobacter infection" data-d2="Acute appendicitis" data-item-id="q_82ce085a31485431a3cd" data-item-version="1" data-item-status="ready" data-key-id="o_064aa2ce303755cba871" data-d1-id="o_884471f9d4225df6bd6b" data-d2-id="o_c285769b1f575e69a5dc">6 yo with severe crampy abdominal pain and grossly bloody stools, temperature 37.6 C, after a family cookout &rarr; <b>Escherichia coli O157:H7 infection</b> &rarr; Hematochezia early, high fever rare</li>
<li data-type="avoid" data-d1="Intravenous fluid resuscitation" data-d2="Serial monitoring of hemoglobin and platelet count" data-item-id="q_62c095fb7f2b5781ac0e" data-item-version="1" data-item-status="ready" data-key-id="o_91ccfeafc47d5fca9df4" data-d1-id="o_2ca0a0e449c958fcb7dc" data-d2-id="o_a6aef911adce5d6f9432">That 6 year old with suspected Shiga toxin producing E coli; which intervention should be withheld &rarr; <b>Empiric antibiotics</b> &rarr; Risk of precipitating hemolytic uremic syndrome</li>
<li data-type="mech" data-d1="Reactive arthritis" data-d2="Transverse myelitis" data-item-id="q_b808cebcd78f5597987a" data-item-version="1" data-item-status="ready" data-key-id="o_d483d5200caa58048ec6" data-d1-id="o_2154e25b8e035f9c8c78" data-d2-id="o_0608aef047da5d079b85">Three weeks after a Campylobacter enteritis, ascending symmetric weakness with areflexia &rarr; <b>Guillain-Barre syndrome</b> &rarr; The classic post-infectious sequela</li>
<li data-type="mech" data-d1="Guillain-Barre syndrome" data-d2="Septic arthritis" data-item-id="q_2abf625294055b6bbfed" data-item-version="1" data-item-status="ready" data-key-id="o_14d7230d3f31577e8278" data-d1-id="o_66fe7f7cbbbd5872976c" data-d2-id="o_d22526f43d7353bb8fff">Two weeks after a Campylobacter enteritis, asymmetric oligoarthritis with conjunctivitis and urethritis &rarr; <b>Reactive arthritis</b> &rarr; The second named sequela</li>
<li data-type="next" data-src="uworld" data-nid="1575404882954 1580504776948" data-d1="Amoxicillin per susceptibility" data-d2="Doxycycline" data-item-id="q_313f717cd94898dbb098" data-item-version="1" data-item-status="ready" data-key-id="o_6942446271398990c022" data-d1-id="o_04110531e3b2e9f53882" data-d2-id="o_eb860d9a46d1d7192182" data-lead-in="Which is the most appropriate treatment for this patient&#x27;s condition?">5 yo M, 4 days of mucoid diarrhea after a low-grade fever that has resolved, still 5 or 6 stools a day, well hydrated, afebrile, guaiac negative; stool culture grows Campylobacter coli, ciprofloxacin resistant, ampicillin and tetracycline sensitive &rarr; <b>Symptomatic care only</b> &rarr; mild and self-limited; the susceptibility panel is not an indication</li>
<li data-type="next" data-src="authored" data-d1="Doxycycline" data-d2="Levofloxacin" data-item-id="q_142d4dd2a8394fae6600" data-item-version="1" data-item-status="ready" data-key-id="o_8c6465fe8bb8c563f134" data-d1-id="o_5694b0f693d78e3fcd52" data-d2-id="o_bbc54a3fa037b06b9841">6 yo with Campylobacter coli enteritis now on day 9 with bloody stools; ciprofloxacin resistant, erythromycin intermediate, ampicillin and tetracycline sensitive &rarr; <b>Amoxicillin</b> &rarr; sensitive, and safe under 8</li>
<li data-type="next" data-src="authored" data-d1="Symptomatic care only" data-d2="Loperamide" data-item-id="q_1970422a7c65d91e039b" data-item-version="1" data-item-status="ready" data-key-id="o_bd207742b89e974e4ed8" data-d1-id="o_8a964327b3c79726b499" data-d2-id="o_8d5e433d18503f816303">4 yo in day care with high fever, bloody diarrhea and a brief generalized seizure; stool grows Shigella &rarr; <b>Azithromycin</b> &rarr; treating shortens illness and spread</li>
</ol>
<div class="danger"><span class="lbl">Decoy note</span> The brother's illness supports an infectious cause, but his <i>bloody</i> stools may prompt a diagnosis of Shiga toxin <i>E. coli</i> in a patient with no blood in his own stool. A contact's findings describe the exposure, not this patient's phenotype. The migratory pain is also explained by <i>Campylobacter</i> spread, so it does not confirm appendicitis.</div>
<div class="pearls"><span class="lbl">Bacterial diarrhea: who gets antibiotics</span> <b>Campylobacter</b> &mdash; self-limited within about a week; supportive care. Treat only for symptoms beyond 7 days, bloody stools, high fever, or pregnancy, immunocompromise or old age; choose by susceptibility &middot; <b>The culture trap</b> &mdash; a positive culture with a susceptibility panel is not an indication; culture exists for protracted or severe illness and for outbreak control in day care and nursing homes &middot; <b>Shiga toxin-producing E. coli</b> &mdash; bloody diarrhea with little fever; never give antibiotics, which raise the risk of hemolytic uremic syndrome &middot; <b>Shigella</b> &mdash; high fever, bloody diarrhea, sometimes a febrile seizure; antibiotics (azithromycin) shorten illness and spread &middot; <b>Nontyphoidal Salmonella</b> &mdash; supportive in a healthy child; treat infants under 3 months, sickle cell disease, immunocompromise or bacteremia, because treatment otherwise prolongs carriage &middot; <b>Yersinia</b> &mdash; pseudoappendicitis like Campylobacter; supportive unless bacteremic or immunocompromised &middot; <b>Clostridioides difficile</b> &mdash; recent antibiotics; oral vancomycin or fidaximicin &middot; <b>Doxycycline under 8</b> &mdash; avoided when another agent covers the organism, for tooth staining</div>
<div class="pearls"><span class="lbl">Pearls</span> Appendicitis does not cause twelve mucoid stools or a sick sibling; ileocecal Campylobacter or Yersinia explains both. &middot; Profuse watery-then-mucoid diarrhea or a sick contact alone should prompt reconsideration of appendicitis before surgery. &middot; <i>Campylobacter</i> and <i>Yersinia</i> have an ileocecal predilection and mimic appendicitis; imaging shows ileocecal inflammation and mesenteric adenopathy with a <b>normal appendix</b>. &middot; <i>Campylobacter</i> may infect the jejunum before the ileum and cecum, so the pain can migrate as in appendicitis. &middot; The two tested sequelae of <i>Campylobacter</i> are <b>Guillain-Barré syndrome</b> and <b>reactive arthritis</b>. &middot; Antibiotics are for illness beyond seven days, bloody stools, high fevers, or pregnancy, immunocompromise, or advanced age; otherwise the treatment is supportive. &middot; Antibiotics are withheld for Shiga toxin <i>E. coli</i> ⚠︎, so invasive bacterial diarrheas do not share one management rule.</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part II <b>NSAID Prerenal AKI in a Child</b> has the Shiga toxin and hemolytic uremic syndrome row from the renal side, where the <i>E. coli</i> O157:H7 branch of this differential ends. Ask: <i>whose stool was bloody, and how many days into the illness?</i> Part I <b>Anemia with Thrombocytopenia</b> covers hemolytic uremic syndrome, which follows Shiga toxin-producing <i>E. coli</i>, not <i>Campylobacter</i>. Part II <b>Foodborne Diarrhea: Source and Organism</b> covers the organism by exposure: what did the patient eat, and when?</div>
<div class="rule"><span class="lbl">Transferable rule</span> When a presentation fits a textbook script, look for the finding the script <b>cannot</b> explain, such as a symptom the disease does not produce or an exposure it cannot have.</div>
<div class="traps"><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Acute appendicitis &mdash; Appendicitis is not associated with profuse watery then mucoid diarrhea, and it cannot explain a sibling with the same illness; there are no peritoneal signs</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy"><i>E. coli</i> O157:H7 &mdash; Hematochezia appears in the patient within 1–3 days, and fever above 38.5 °C rarely occurs; the bloody stools are the brother's, not this patient's</span></div><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Norovirus &mdash; Norovirus gives <b>watery</b> stools without mucus, a normal white blood cell count, and prominent vomiting</span></div><div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Cecal diverticulitis &mdash; It is exceedingly rare in children and adolescents, and it does not produce profuse mucoid diarrhea</span></div><div class="trapline"><span class="pill p-test">Test-overrides-findings</span><span class="trapwhy">A susceptibility panel invites treatment, but a mild, improving, afebrile child is treated by the clinical picture, not the culture report.</span></div></div>
</div>
```

### `neonatal-jaundice`: Neonatal Jaundice

```html
<div class="brief" id="neonatal-jaundice" data-shelf="fm peds" data-nid="1482976984253 1486591392171 1512679081304 1517959834181 1555449924265" data-bp="newborn gi">
<h4>Neonatal Jaundice</h4>
<p class="sub">Timing, direct fraction and Coombs &middot; NBME peds &middot; which mechanism, and does it need light</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 4-day-old term M, uncomplicated pregnancy and delivery, Apgars 10 and 10, breast-feeding without difficulty, <b>eight wet diapers daily</b>, alert and afebrile &middot; <b>Labs</b> &mdash; total bilirubin <b>11 mg/dL</b> &middot; <b>Q</b> &mdash; the most likely underlying cause; options spanned cholestasis, enterohepatic circulation, conjugation-enzyme activity, albumin binding and ligandin</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Physiologic jaundice is a <b>conjugation</b> problem. The newborn breaks down fetal hemoglobin quickly while hepatic <b>UDP-glucuronosyltransferase</b> is still immature, so unconjugated bilirubin accumulates. A well infant, feeding and voiding normally, jaundiced on day 4 at 11 mg/dL has physiologic jaundice.</p>
<p>Each wrong option is a <b>real mechanism stated in the wrong direction or the wrong compartment</b>. Ligandin is <b>low</b> at birth. Enterohepatic circulation is <b>increased</b> in the newborn. Cholestasis produces a <b>direct</b> hyperbilirubinemia, which this infant does not have. Albumin displacement requires a displacing drug.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Physiologic</b> &mdash; begins after 24 hours, peaks around day 3 to 5, predominantly indirect, resolving by 1 to 2 weeks &middot; <b>Pathologic</b> &mdash; jaundice within the first 24 hours, any raised direct fraction, or persistence beyond 2 weeks &middot; <b>Jaundice threshold</b> &mdash; clinically apparent above about 5 mg/dL &middot; <b>Physiologic ceiling</b> &mdash; peak around 14 to 15 mg/dL, indirect over 90% &middot; <b>Exchange range</b> &mdash; generally above 20 mg/dL; kernicterus risk rises at 25 to 30 mg/dL</div>
<table>
<caption>Neonatal jaundice &mdash; the mechanisms<span class="cap-sub">timing and the direct fraction separate them</span></caption>
<thead><tr><th>Cause</th><th>When</th><th>Key discriminator</th><th>What to do</th></tr></thead>
<tbody>
<tr><td><b>Physiologic</b></td><td>After 24 h, peak day 3&ndash;5</td><td>Well infant, feeding and voiding normally; indirect</td><td>Nothing but time</td></tr>
<tr><td>Suboptimal-intake (breast-feeding) jaundice</td><td>Day 3&ndash;5</td><td><b>Weight loss and few wet diapers</b>; increased enterohepatic reabsorption</td><td>Feed more often, lactation support</td></tr>
<tr><td>Breast-milk jaundice</td><td>Day 7 onward, <b>peaks around 2 weeks</b>, can persist weeks</td><td><b>Thriving</b> infant, indirect, gaining well; normal GGT, normal stools; milk beta-glucuronidase deconjugates bilirubin and increases enterohepatic circulation</td><td>Continue breast-feeding</td></tr>
<tr><td>ABO or Rh hemolytic disease</td><td>Often within 24 h</td><td><b>Coombs positive</b>; mother O or Rh-negative; indirect, <b>high reticulocytes</b></td><td>Phototherapy; exchange above threshold</td></tr>
<tr><td>G6PD deficiency <span class="tag t-em">Can&#39;t miss</span></td><td>Variable, can be abrupt</td><td>Indirect with anemia and <b>high reticulocytes</b>, often an oxidant trigger</td><td>Remove trigger; phototherapy</td></tr>
<tr><td>Biliary atresia <span class="tag t-em">Can&#39;t miss</span></td><td>Well at birth; jaundice and hepatomegaly at <b>2 to 8 weeks</b></td><td><b>Raised direct fraction</b> with <b>high GGT and ALP</b>, transaminases normal or mildly high, <b>normal reticulocytes</b>; acholic stools, dark urine; ultrasound shows a small or absent gallbladder and a <b>triangular cord sign</b></td><td>Intraoperative cholangiogram (or liver biopsy) confirms; <b>Kasai</b> hepatoportoenterostomy before about 60 days; most eventually need a liver transplant</td></tr>
<tr><td>Progressive familial intrahepatic cholestasis</td><td>Infancy</td><td>Direct hyperbilirubinemia with a <b>normal GGT</b>; gallbladder present</td><td>Specialist evaluation</td></tr>
<tr><td>Hemophagocytic lymphohistiocytosis</td><td>Infancy, acute</td><td><b>Febrile and ill</b>; direct bilirubin and GGT high with <b>cytopenias and low reticulocytes</b>; normal gallbladder</td><td>Urgent hematology evaluation</td></tr>
<tr><td>Crigler-Najjar / Gilbert</td><td>Persistent indirect</td><td>The same enzyme, absent or reduced rather than immature</td><td>Depends on type</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody class="grp">
<tr><td>Total and direct bilirubin</td><td>First</td><td><b>Indirect</b>, after 24 hours, well infant</td><td>Physiologic or intake-related; plot on an hour-specific chart for phototherapy</td></tr>
<tr><td></td><td></td><td><b>Direct</b> fraction raised</td><td>Never physiologic: cholestasis workup; check the direct fraction in any infant still jaundiced past 2 weeks</td></tr>
</tbody>
<tbody>
<tr><td>Blood type and direct Coombs test</td><td>By branch</td><td><b>Coombs positive</b>, mother group O or Rh-negative</td><td>Isoimmune hemolysis: phototherapy, exchange above threshold</td></tr>
<tr><td>CBC, smear, reticulocyte count and G6PD</td><td>By branch</td><td><b>Anemia</b> with Coombs-negative hemolysis</td><td>G6PD deficiency or spherocytosis</td></tr>
<tr><td>Liver panel with GGT</td><td>By branch</td><td><b>High GGT and ALP</b>, transaminases normal or mildly high</td><td>Bile duct injury: biliary atresia; a <b>normal GGT</b> with a direct hyperbilirubinemia points to PFIC</td></tr>
<tr><td>Abdominal ultrasound</td><td>Next</td><td>Small or absent gallbladder, <b>triangular cord sign</b></td><td>Supports biliary atresia</td></tr>
<tr><td>Intraoperative cholangiogram (or liver biopsy), after ultrasound and HIDA</td><td>Confirms</td><td><b>No</b> contrast reaches the bowel; biopsy shows duct proliferation and fibrosis</td><td>Biliary atresia: Kasai before about 60 days; most eventually need a liver transplant</td></tr>
<tr><td>Hepatic ultrasound or serum albumin</td><td>Skip</td><td>Cannot show <b>hemolysis</b> or immature conjugation</td><td>Jaundice under 24 hours needs bilirubin fractions and a Coombs</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="mech" data-d1="Decreased enterohepatic circulation of bilirubin" data-d2="Increased hepatocyte ligandin concentration" data-src="authored" data-item-id="q_4e69aac28fcf549afe6e" data-item-version="1" data-item-status="ready" data-key-id="o_9876c69b2ba074f1b523" data-d1-id="o_f944086fb5103c608882" data-d2-id="o_c8db40dd8cc14d3eaf26">4 day old M, term, breast-feeding well with eight wet diapers, alert and afebrile, total bilirubin 11 mg/dL &rarr; <b>Immature UDP-glucuronosyltransferase activity</b> &rarr; Physiologic jaundice &mdash; conjugation lags the fetal hemoglobin load</li>
<li data-type="next" data-d1="Exchange transfusion" data-d2="Restriction of breast-feeding" data-src="authored" data-item-id="q_c5b948d9253906aa4201" data-item-version="1" data-item-status="ready" data-key-id="o_95128b8ac62b8a2d13a9" data-d1-id="o_d34acc2268f746ab3122" data-d2-id="o_65dee1319b214d4d6c87">2 day old F, jaundice to the chest, total bilirubin 19 with direct 0.6, Coombs positive, infant blood group B and mother group O &rarr; <b>Phototherapy</b> &rarr; ABO incompatibility &mdash; below the exchange range</li>
<li data-type="dx" data-d1="Breast-milk jaundice" data-d2="Biliary atresia" data-src="authored" data-item-id="q_ed3d5ff447cc34d96b29" data-item-version="1" data-item-status="ready" data-key-id="o_67e65c9ef90c1c56c117" data-d1-id="o_18b055129737a8509d8b" data-d2-id="o_59de846e011929be5f54">Day 4, exclusively breast-fed, 11% below birth weight, three wet diapers, indirect hyperbilirubinemia &rarr; <b>Suboptimal-intake jaundice</b> &rarr; Also called breast-feeding jaundice &mdash; too little milk, not the milk itself</li>
<li data-type="dx" data-d1="Suboptimal-intake jaundice" data-d2="Congenital hypothyroidism" data-src="authored" data-item-id="q_90c7f5ce1579adea3b72" data-item-version="1" data-item-status="ready" data-key-id="o_65e57556ac834306003d" data-d1-id="o_da637a2251d1966e34f7" data-d2-id="o_fac82459dae8649282b9">Thriving 3 week old, exclusively breast-fed, gaining well, persistent indirect hyperbilirubinemia, normal direct fraction &rarr; <b>Breast-milk jaundice</b> &rarr; Late, well-grown, indirect &mdash; continue feeding</li>
<li data-type="dx" data-d1="Physiologic jaundice" data-d2="Breast-milk jaundice" data-src="authored" data-item-id="q_f914c13631b93692dcad" data-item-version="1" data-item-status="ready" data-key-id="o_f2f8929625892e9ababf" data-d1-id="o_227ecc6e5b5798f6c257" data-d2-id="o_6f6429b6ac3b9abdc1e1">6 week old with jaundice, acholic stools and a direct bilirubin of 5 mg/dL &rarr; <b>Biliary atresia</b> &rarr; A direct fraction is never physiologic</li>
<li data-type="mech" data-d1="Reduced hepatic conjugation capacity" data-d2="Displacement of bilirubin from albumin" data-src="authored" data-item-id="q_c0dfa7c97c1600f1b04e" data-item-version="1" data-item-status="ready" data-key-id="o_987fc1de76df88f4319b" data-d1-id="o_7b87f7746a324f278e18" data-d2-id="o_d09dc340fedd9b234ee6">Why dehydration in the first week worsens an indirect hyperbilirubinaemia &rarr; <b>Increased enterohepatic reabsorption</b> &rarr; Slow gut transit lets intestinal bilirubin return to the circulation</li>
<li data-type="test" data-d1="Hepatic ultrasonography" data-d2="Serum albumin concentration" data-src="authored" data-item-id="q_3b84f5c6443921e09e97" data-item-version="2" data-item-status="ready" data-key-id="o_e626e65b5225c88ccd82" data-d1-id="o_79bb76df111d830bbb69" data-d2-id="o_984cb869487c63e8e71f" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">Term newborn jaundiced at 14 hours of life &rarr; <b>Total and direct bilirubin with a Coombs test</b> &rarr; Onset inside 24 hours is pathologic until proven otherwise</li>
<li data-type="avoid" data-d1="Lactation support with more frequent feeds" data-d2="Phototherapy if the level crosses threshold" data-src="authored" data-item-id="q_995ec81369106a952f4e" data-item-version="1" data-item-status="ready" data-key-id="o_e2c089ebe7fea5d29d21" data-d1-id="o_879fdd925d2269db5fb1" data-d2-id="o_f6958897e96cad972ceb">Well term newborn with suboptimal-intake jaundice on day 4; which management is inappropriate &rarr; <b>Stopping breast-feeding</b> &rarr; Feed more often, not less &mdash; milk intake drives bilirubin out</li>
<li data-type="mech" data-d1="Inhibition of glucuronosyltransferase" data-d2="Increased haem oxygenase activity" data-src="authored" data-item-id="q_e3d808bf1661371049fc" data-item-version="1" data-item-status="ready" data-key-id="o_2a73eceb14d40a639d6b" data-d1-id="o_2e23dd71f7ac82c12243" data-d2-id="o_fb44aff4d79a15fc04b9">Which mechanism makes a sulfonamide dangerous in a jaundiced newborn &rarr; <b>Displacement of bilirubin from albumin</b> &rarr; Free bilirubin crosses into the basal ganglia</li>
<li data-type="test" data-src="uworld" data-nid="1482976984253 1486591392171 1512679081304 1517959834181 1555449924265" data-d1="Direct bilirubin high, GGT normal, reticulocyte count normal" data-d2="Direct bilirubin normal, GGT normal, reticulocyte count high" data-item-id="q_8f4f13f378a0151b32dd" data-item-version="1" data-item-status="ready" data-key-id="o_7f8066670fd7e08d68ce" data-d1-id="o_0ba2fbb3864b44b36dc1" data-d2-id="o_0c3a1f78099da0c4d0c3" data-lead-in="Which of the following laboratory patterns is most likely to be present in this patient?">4-week-old term boy, exclusively breastfed, with weeks of progressive yellowing of the eyes and now jaundice of the face and chest; stools have become fewer and paler; weight at the 25th percentile; afebrile and well-appearing; soft abdomen with an enlarged liver; total bilirubin 12.5 mg/dL; ultrasound shows hepatomegaly and no visible gallbladder &rarr; <b>Direct bilirubin high, GGT high, reticulocyte count normal</b> &rarr; Biliary atresia; intraoperative cholangiography, then Kasai hepatoportoenterostomy</li>
<li data-type="test" data-src="authored" data-d1="Transcutaneous bilirubin measurement" data-d2="Blood type and direct Coombs test" data-item-id="q_5374e158190b467a7a54" data-item-version="1" data-item-status="ready" data-key-id="o_f6c0c3011d05aebc8f0a" data-d1-id="o_3c2092ffca563a9094c0" data-d2-id="o_4ff9ace2534f98e1413f" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">3-week-old term girl, exclusively breastfed, still jaundiced to the chest at a routine visit; gaining weight well, yellow stools and pale urine; exam otherwise normal &rarr; <b>Serum total and direct bilirubin</b> &rarr; Jaundice past 2 weeks needs a direct fraction; indirect in a thriving infant is breast-milk jaundice</li>
<li data-type="next" data-src="authored" data-d1="Primary liver transplantation" data-d2="Ursodeoxycholic acid and fat-soluble vitamins" data-item-id="q_f61faf557c39ed95a92a" data-item-version="1" data-item-status="ready" data-key-id="o_31c11bcf9c0c66eb7dfe" data-d1-id="o_433ca0389cbf9ca6062d" data-d2-id="o_497bdd90b911ad320ed2">6-week-old term boy with jaundice since 3 weeks of age, clay-colored stools and dark urine; direct bilirubin 6 mg/dL, GGT high; ultrasound shows a small gallbladder and a triangular cord sign; intraoperative cholangiogram shows no contrast entering the duodenum &rarr; <b>Kasai hepatoportoenterostomy</b> &rarr; Biliary atresia; best done early, and most eventually need a liver transplant</li>
</ol>
<div class="danger"><span class="lbl">Exit ramps and gates</span> <b>Under 24 hours</b> &mdash; never physiologic; send bilirubin with a direct fraction and a Coombs &middot; <b>Any direct fraction</b> &mdash; not physiologic; consider obstruction or infection &middot; <b>Beyond 2 weeks</b> &mdash; check the direct fraction and the stool color before reassuring &middot; <b>Phototherapy versus exchange</b> &mdash; phototherapy first; exchange transfusion is for the severe range or signs of encephalopathy, not a level near threshold &middot; <b>Feeding</b> &mdash; jaundice is almost never a reason to stop breast-feeding; more milk increases bilirubin excretion through the gut</div>
<div class="pearls"><span class="lbl">Pearls</span> The newborn gut reabsorbs bilirubin, so anything that slows transit raises the indirect fraction &middot; <b>Suboptimal-intake versus breast-milk jaundice</b> &mdash; suboptimal intake is a hungry infant losing weight in the first week; breast-milk jaundice is a thriving infant still jaundiced in the second week &middot; Ligandin and glucuronosyltransferase are both <b>low</b> at birth &middot; Sulfonamides and ceftriaxone displace bilirubin from albumin, so they are avoided in jaundiced newborns &middot; A raised direct fraction makes newborn jaundice urgent</div>
<div class="pearls"><span class="lbl">Direct bilirubin, GGT, reticulocytes</span> Read the three together &middot; <b>Direct high, GGT high, retics normal</b>: duct obstruction, biliary atresia in a well infant with pale stools &middot; <b>Direct high, GGT normal</b>: PFIC &middot; <b>Direct and GGT high, retics low, cytopenias</b>: HLH in a febrile, ill infant &middot; <b>Indirect, retics high</b>: hemolysis &middot; <b>Indirect, everything else normal</b>: breast-milk jaundice in a thriving infant &middot; An <b>exclusively breastfed</b> infant can still have biliary atresia; pale stools and a direct fraction decide it</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part II <b>The Sick Jaundiced Neonate with a Positive Screen</b> covers the unwell infant with a metabolic cause; this brief covers the well one. Part I <b>Cholestasis &amp; the LFT Patterns</b> covers the direct-fraction workup. Ask: is the infant well, and is any of it direct?</div>
<div class="rule"><span class="lbl">Transferable rule</span> When every option names a real mechanism, check which direction each one moves in this patient before choosing.</div>
<div class="traps">
<div class="trapline"><span class="pill p-unchecked">Unchecked attribute</span><span class="trapwhy">Ligandin and enterohepatic circulation are real mechanisms, but the options state them in the wrong direction.</span></div>
<div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Exchange transfusion offered when the level is high but still in the phototherapy range.</span></div>
<div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Cholestasis causes a direct hyperbilirubinemia; this infant's is indirect.</span></div>
<div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">A direct hyperbilirubinemia with a normal GGT is PFIC; pale stools and an absent gallbladder mean bile duct destruction, which raises the GGT.</span></div>
<div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">HLH also raises direct bilirubin and GGT, but with fever, an ill infant and marrow failure lowering the reticulocytes; this infant is afebrile and well.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Exclusive breastfeeding suggests breast-milk jaundice, but that is indirect, peaks around 2 weeks and leaves the stools yellow and the gallbladder normal.</span></div>
</div>
</div>
```

### `bs-umbilical`: Umbilical Findings in a Newborn

```html
<div class="brief bs" id="bs-umbilical" data-shelf="peds" data-nid="1486596683598 1539170358295 1557079212053" data-bp="newborn">
<h4>Umbilical Findings in a Newborn</h4>
<p class="sub">Skin-covered and reducible · is there skin over it, and how big and how old is it?</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 4-hour-old boy, 38 wk, 3.6 kg, mother 18 with no prenatal care, normal vitals; <b>soft, nontender, skin-covered 1.4 cm bulge</b> just below the umbilical stump that <b>enlarges with crying and reduces</b> with gentle pressure &middot; <b>Q</b> &mdash; the most appropriate next step for the mass; options spanned observation, abdominal ultrasound, karyotype, immediate surgery and topical silver nitrate</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>A <b>skin-covered, soft, reducible</b> bulge that grows with crying is a congenital umbilical hernia: the fascial ring around the umbilicus has not closed yet. It is common in healthy newborns, incarceration is very rare, and small hernias usually close on their own, so a well infant needs <b>observation only</b>. The diagnosis is clinical; no imaging or genetic test is needed.</p>
<p>The cutoffs decide when observation ends: a defect <b>over 1.5 cm</b> is less likely to close, persistence to <b>about age 5</b> earns elective repair, and <b>incarceration</b> earns repair at any age. The exception is <b>no skin</b>: bowel in a membranous sac (omphalocele) or bare bowel beside the cord (gastroschisis) goes to surgery right after birth.</p>
</div>
<div class="crit"><span class="lbl">Decision cutoffs</span> <b>Skin-covered, soft, reducible</b>: observe &middot; <b>Defect over 1.5 cm</b>: spontaneous closure less likely; keep following &middot; <b>Still present at about age 5</b>: elective surgical repair &middot; <b>Incarcerated</b> (firm, tender, irreducible or discolored, with vomiting): urgent repair at any age &middot; <b>No skin over the bowel</b>: gastroschisis or omphalocele, surgery at birth</div>
<table data-mask="3">
<caption>Umbilical findings in a newborn: the differential</caption>
<thead><tr><th>Finding</th><th>Illness script</th><th>The NBME tell</th><th>Next step</th></tr></thead>
<tbody>
<tr><td><b>Umbilical hernia</b></td><td>Unclosed fascial ring; more frequent with Down syndrome, hypothyroidism, Beckwith-Wiedemann and Ehlers-Danlos</td><td><b>Skin-covered</b>, soft, reducible, grows with crying</td><td>Observe; repair about age 5 if persistent, sooner if incarcerated</td></tr>
<tr><td>Umbilical granuloma</td><td>Excess granulation tissue at the base after the cord separates</td><td><b>Moist, red, friable nub</b> that appears after the cord falls off</td><td>Topical silver nitrate</td></tr>
<tr><td>Patent urachus or omphalomesenteric duct</td><td>Persistent tract to the bladder (urachus) or the ileum (omphalomesenteric duct)</td><td><b>Drainage</b>: urine-like fluid from a urachus, stool or mucus from the duct</td><td>Ultrasound, then surgical excision</td></tr>
<tr><td>Omphalocele</td><td>Midline defect at the umbilical ring; bowel, often liver, herniates into the base of the cord</td><td><b>Membranous sac</b> with the cord inserting on it</td><td>Surgery at birth; karyotype and echocardiogram for associated anomalies</td></tr>
<tr><td>Gastroschisis</td><td>Full-thickness wall defect, usually right of the umbilicus; usually isolated</td><td><b>Bare bowel, no sac</b>, beside a normally inserted cord</td><td>Cover the bowel, decompress, immediate surgery</td></tr>
</tbody>
</table>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="next" data-src="uworld" data-nid="1486596683598 1539170358295 1557079212053" data-d1="Abdominal ultrasound" data-d2="Immediate surgical repair" data-item-id="q_3848a74bbe5788ec0cd2" data-item-version="1" data-item-status="ready" data-key-id="o_527087a0ed16fdcc69df" data-d1-id="o_78507dbcc8fa94330eb8" data-d2-id="o_19eed6a440d9eb816b0f" data-lead-in="Which of the following is the most appropriate next step in management of the mass?">4-hour-old boy born at 38 weeks to a mother without prenatal care, well-appearing, with a soft, nontender, skin-covered 1.4 cm bulge just below the umbilical stump that enlarges with crying and reduces with gentle pressure &rarr; <b>Observation only</b> &rarr; Congenital umbilical hernia</li>
<li data-type="next" data-src="authored" data-d1="Reassurance and reexamination in 2 years" data-d2="Abdominal ultrasound" data-item-id="q_9fc1e6fd6f179968b014" data-item-version="1" data-item-status="ready" data-key-id="o_82075efe42ad0f93ccc3" data-d1-id="o_a25c8062370dfb88b1e8" data-d2-id="o_7ceed528dffb6f45ec46">5-year-old girl, well, with a soft, reducible, skin-covered umbilical bulge present since birth that has not decreased in size; defect about 2 cm; no pain or vomiting &rarr; <b>Elective surgical repair</b> &rarr; Persistent umbilical hernia</li>
<li data-type="next" data-src="authored" data-d1="Observation and reexamination in 1 week" data-d2="Elective repair at about age 5" data-item-id="q_ef47cdcba6bd7ec534de" data-item-version="1" data-item-status="ready" data-key-id="o_ab166e20363490ac0ea6" data-d1-id="o_1f86be6f94cfffc7a27d" data-d2-id="o_5eed675e94cffc8f5749">8-month-old boy with a known umbilical hernia that is now firm, tender, discolored and cannot be reduced; he has vomited three times &rarr; <b>Urgent surgical repair</b> &rarr; Incarcerated umbilical hernia</li>
<li data-type="next" data-src="authored" data-d1="Surgical excision of the umbilical tissue" data-d2="Observation only" data-item-id="q_24ecf611fbdfd4b46fb0" data-item-version="1" data-item-status="ready" data-key-id="o_3d4db4e41b4ffee387cc" data-d1-id="o_102f179958151a089427" data-d2-id="o_f5cd8cb1405eb3851263">12-day-old girl whose cord fell off 4 days ago, now with a 4 mm moist, red, friable, pedunculated nub at the umbilical base with slight serous drainage; afebrile, no surrounding erythema &rarr; <b>Topical silver nitrate</b> &rarr; Umbilical granuloma</li>
<li data-type="dx" data-src="authored" data-d1="Patent omphalomesenteric duct" data-d2="Umbilical granuloma" data-item-id="q_a570b49ecd39020bb0cc" data-item-version="1" data-item-status="ready" data-key-id="o_a6cb115834892b8603ca" data-d1-id="o_27b33dbf548ff6c33a51" data-d2-id="o_85cfde372fef7fd091a4">3-week-old boy with clear, urine-like fluid leaking from the umbilicus that increases when he cries or strains; the skin around the umbilicus is normal &rarr; <b>Patent urachus</b> &rarr; Ultrasound, then surgical excision</li>
<li data-type="next" data-src="authored" data-d1="Karyotype and echocardiogram before any repair" data-d2="Observation with repair at about age 5" data-item-id="q_8762dc7594a29f979c2d" data-item-version="1" data-item-status="ready" data-key-id="o_ee6a2690c7cd799bbd74" data-d1-id="o_b7d80aa79b7f1e3f0834" data-d2-id="o_547548cfe07f33c6cb27">Term newborn with loops of bare, edematous bowel protruding through a defect to the right of a normally inserted umbilical cord, with no covering membrane; vital signs stable &rarr; <b>Cover the bowel and arrange immediate surgery</b> &rarr; Gastroschisis</li>
<li data-type="test" data-src="authored" data-d1="Serum TSH and free T4" data-d2="No further evaluation is needed" data-item-id="q_099f35c5a2bab69de8ce" data-item-version="1" data-item-status="ready" data-key-id="o_553a8e35e2a561b0c340" data-d1-id="o_2ae6b6f0bfbc942072f8" data-d2-id="o_1baadd44b574be176474" data-lead-in="In addition to surgical repair, which of the following evaluations is most appropriate?">Term newborn with a 5 cm midline membrane-covered sac containing bowel and liver at the base of the umbilical cord, with the cord inserting on the sac &rarr; <b>Karyotype and echocardiogram</b> &rarr; Omphalocele</li>
<li data-type="test" data-src="authored" data-d1="Karyotype" data-d2="Abdominal ultrasound" data-item-id="q_7e472e5bd7e09a357f4d" data-item-version="1" data-item-status="ready" data-key-id="o_e96f74a21f611f533a88" data-d1-id="o_8159cde4a1c5839bea1f" data-d2-id="o_8448eeae6df3b6c58f05" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">7-week-old girl born at home without newborn screening, with a reducible skin-covered umbilical hernia, persistent jaundice, a large tongue, poor tone, constipation and a wide posterior fontanelle &rarr; <b>Serum TSH and free T4</b> &rarr; Congenital hypothyroidism</li>
</ol>
<div class="danger"><span class="lbl">Abdominal wall defect at delivery</span> Exposed bowel loses heat and fluid: cover it with a <b>sterile moist dressing or bowel bag</b>, place a nasogastric tube, give IV fluids and keep the infant warm, then <b>immediate surgery</b>. An omphalocele also gets a <b>karyotype and echocardiogram</b>, because trisomy 13 and 18, Beckwith-Wiedemann and heart defects travel with it; gastroschisis usually travels alone.</div>
<div class="pearls"><span class="lbl">Pearls</span> An umbilical hernia with prolonged jaundice, macroglossia, hypotonia, constipation or a large fontanelle is a reason to check <b>TSH</b>, because congenital hypothyroidism is the treatable association &middot; Karyotype is for Down features or an omphalocele, never for an isolated hernia in a normal infant &middot; Silver nitrate is the treatment for a granuloma; an umbilical lesion that keeps draining urine or stool is a remnant tract and needs imaging and excision</div>
<div class="pearls"><span class="lbl">Pairs with</span> <b>Congenital Hypothyroidism</b>: an umbilical hernia is one of its soft signs; ask: is there jaundice, macroglossia or a large fontanelle beside the hernia? <b>Tracheoesophageal Fistula with Esophageal Atresia</b>: after any structural defect, screen for the anomalies that occur with it (VACTERL there, karyotype and echocardiogram for an omphalocele).</div>
<div class="rule"><span class="lbl">Transferable rule</span> For a newborn umbilical finding, ask first whether skin covers it: skin-covered and reducible means observe, with repair set by the cutoffs (still present at about age 5, or incarcerated at any age), while bowel without skin goes to surgery at birth.</div>
<div class="traps"><div class="trapline"><span class="pill p-seq">Redundant workup</span><span class="trapwhy">Abdominal ultrasound adds nothing to a clinical diagnosis; it is for an acquired hernia in an older child or adult.</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Immediate surgery belongs to gastroschisis and omphalocele, where no skin covers the bowel.</span></div><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">A young mother without prenatal care invites a genetic workup, but karyotype is for Down features or an omphalocele, and this infant has neither.</span></div><div class="trapline"><span class="pill p-mirror">Mirror twin</span><span class="trapwhy">Silver nitrate treats an umbilical granuloma, the moist red nub that appears after the cord falls off, not a skin-covered bulge at 4 hours.</span></div></div>
</div>
```
