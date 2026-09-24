# Voice packet 3 of 5 (s30, gi): zenker, feeding-refusal, peds-constipation, bs-tef

**Instructions.** Everything you need is in this packet. Do not open index.html, the skill files or other packets. Write your edits to `repair/s30/04_voice_3.json`, run `python3 tools/verify_edits.py repair/s30/04_voice_3.json scratch/s30_base.html --voice` from the workspace folder (Step2Haki/workspace) and loop until it prints PASS (add `--report` to read your own claim map). Then reply with the 3 to 5 line report the rules ask for, including any acronym you skipped.

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
### `zenker`: Zenker Diverticulum

```html
<div class="brief" id="zenker" data-shelf="fm" data-bp="gi">
<h4>Zenker Diverticulum</h4>
<p class="sub">Regurgitation of undigested food in an old man · the swallow study comes before any scope or tube</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 74 yo M, months of dysphagia, regurgitates undigested food hours after meals, halitosis, gurgling in the neck on swallowing, weight stable &middot; <b>Q</b> &mdash; the most likely diagnosis; options spanned Zenker diverticulum, achalasia and esophageal squamous cell carcinoma</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>An <b>elderly man</b> with dysphagia, <b>regurgitation of undigested food</b>, <b>halitosis</b>, and a <b>gurgling</b> sound in the neck has a Zenker diverticulum: a pulsion pouch through the weak posterior hypopharyngeal wall because the <b>cricopharyngeus fails to relax</b>. Order a <b>barium esophagram first</b>; a blind endoscope or nasogastric tube can enter the pouch and <b>perforate</b> it.</p>
<p>Once the esophagram shows the pouch, treatment is <b>cricopharyngeal myotomy</b> (with or without diverticulectomy). The main complication is <b>aspiration pneumonia</b>.</p></div>
<table>
<caption>Dysphagia in an adult — the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th></tr></thead>
<tbody>
<tr><td><b>Zenker diverticulum</b></td><td>Elderly man; cricopharyngeal dysfunction; food pools in a posterior pharyngeal pouch</td><td><b>Regurgitation of undigested food, halitosis, neck gurgling</b>; esophagram before scope</td></tr>
<tr><td>Achalasia</td><td>Loss of myenteric inhibitory neurons; middle age; dysphagia to <b>solids and liquids from the start</b></td><td><b>Bird's beak</b> on esophagram; manometry confirms absent peristalsis and a non-relaxing LES</td></tr>
<tr><td>Esophageal cancer <span class="tag t-em">Can't miss</span></td><td>Smoker or drinker (SCC) or long-standing reflux (adenocarcinoma); progressive solid then liquid dysphagia</td><td><b>Weight loss</b> with progressive solid-food dysphagia; endoscopy with biopsy</td></tr>
<tr><td>Schatzki ring / peptic stricture</td><td>Distal mucosal ring or reflux scar; intermittent solid-food dysphagia</td><td><b>Episodic impaction with meat or bread</b>, no weight loss; dilation</td></tr>
<tr><td>Oropharyngeal (neurologic) dysphagia</td><td>Stroke, Parkinson disease, myasthenia; trouble <b>initiating</b> the swallow</td><td><b>Coughing or choking at the start of the swallow</b>, nasal regurgitation; videofluoroscopy and speech therapy</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody class="grp">
<tr><td>Barium esophagram</td><td>First</td><td>Posterior <b>pouch</b> above the cricopharyngeus</td><td>Zenker diverticulum, confirmed; cricopharyngeal myotomy next</td></tr>
<tr><td></td><td></td><td>Dilated esophagus tapering to a <b>bird's beak</b></td><td>Achalasia: manometry next</td></tr>
</tbody>
<tbody>
<tr><td>Esophageal manometry</td><td>Confirms</td><td><b>Absent peristalsis</b>, LES fails to relax</td><td>Achalasia</td></tr>
<tr><td>Upper endoscopy with biopsy</td><td>Confirms</td><td><b>Malignant</b> tissue</td><td>Esophageal cancer; goes first only with alarm features and no neck finding</td></tr>
<tr><td>Videofluoroscopic swallow study</td><td>By branch</td><td>Trouble <b>initiating</b> the swallow, aspiration</td><td>Oropharyngeal neurologic dysphagia: speech therapy</td></tr>
<tr><td>Upper endoscopy or blind nasogastric tube</td><td>Skip</td><td>Can enter the pouch and <b>perforate</b> it</td><td>Image before instrumenting</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="dx" data-d1="Achalasia" data-d2="Esophageal squamous cell carcinoma" data-item-id="q_67450a69f8865270a927" data-item-version="1" data-item-status="ready" data-key-id="o_1e49fb18a4e0554fb9f3" data-d1-id="o_b6950bcabbb457a0b493" data-d2-id="o_ac65d67a2dc058cf86ac">74 yo M, months of dysphagia, regurgitates <b>undigested food</b> hours after meals, halitosis, gurgling in the neck when he swallows, weight stable &rarr; <b>Zenker diverticulum</b> &rarr; barium esophagram</li>
<li data-type="test" data-d1="Upper endoscopy" data-d2="Esophageal manometry" data-item-id="q_07613ec976ee52c5a710" data-item-version="2" data-item-status="ready" data-key-id="o_06e0fbe917dd5d4ab732" data-d1-id="o_90fa06c54eec5c72b0e9" data-d2-id="o_4311845e2c4e55f9891a" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">79 yo M with regurgitation of undigested food, halitosis and a gurgling neck &rarr; <b>Barium esophagram</b> &rarr; a blind scope or tube risks perforating the pouch</li>
<li data-type="avoid" data-d1="Barium esophagram" data-d2="Cricopharyngeal myotomy" data-item-id="q_899c61f983865b6b99c5" data-item-version="1" data-item-status="ready" data-key-id="o_e5a5cde519a95e459e9a" data-d1-id="o_98e8efb070595e2c8a14" data-d2-id="o_ffd7a145b8aa5d859662">81 yo M with suspected Zenker diverticulum and poor oral intake; the intervention to avoid &rarr; <b>Blind nasogastric tube placement</b> &rarr; the tube enters the pouch and perforates it</li>
<li data-type="next" data-d1="Proton pump inhibitor and dietary modification" data-d2="Esophagectomy" data-item-id="q_cbb89259f029559ba921" data-item-version="1" data-item-status="ready" data-key-id="o_a825298130e35e49b21f" data-d1-id="o_90f3950eee035e42b52a" data-d2-id="o_8a299feb10ad53fc87d6">72 yo M whose esophagram shows a posterior pharyngoesophageal outpouching above the cricopharyngeus &rarr; <b>Cricopharyngeal myotomy with or without diverticulectomy</b> &rarr; the pouch is the symptom, the non-relaxing muscle is the cause</li>
<li data-type="mech" data-d1="Esophageal perforation" data-d2="Squamous cell carcinoma of the pouch" data-item-id="q_c2086accc0d35444ab6b" data-item-version="1" data-item-status="ready" data-key-id="o_88b02f5e48275562954d" data-d1-id="o_8590bcd5c3af5dce96a2" data-d2-id="o_41ccf0b832155e26a228">76 yo M with known Zenker diverticulum, 3 days of fever, productive cough and a right lower lobe infiltrate &rarr; <b>Aspiration pneumonia</b> &rarr; pooled contents aspirate at night</li>
<li data-type="dx" data-d1="Zenker diverticulum" data-d2="Diffuse esophageal spasm" data-item-id="q_e47cccaa16775e0a8b5f" data-item-version="1" data-item-status="ready" data-key-id="o_3c3e266278d35f4cab38" data-d1-id="o_28c15ee519f25b9fa61a" data-d2-id="o_0197a0d4968b51c4a9a9">46 yo F, dysphagia to <b>solids and liquids from the outset</b>, regurgitation of undigested food, 5 kg weight loss, esophagram with a dilated esophagus tapering to a bird's beak &rarr; <b>Achalasia</b> &rarr; manometry, then pneumatic dilation or myotomy</li>
<li data-type="dx" data-d1="Zenker diverticulum" data-d2="Schatzki ring" data-item-id="q_9b5d01b7a5e3561c9f9b" data-item-version="1" data-item-status="ready" data-key-id="o_f85a2365282d5cbf8fb6" data-d1-id="o_777e826a49ca53bdba07" data-d2-id="o_8cd16591bc325b82b24f">63 yo M, 40 pack-years and daily alcohol, 3 months of progressive solid-food dysphagia now with liquids, 8 kg weight loss &rarr; <b>Esophageal squamous cell carcinoma</b> &rarr; endoscopy with biopsy</li>
</ol>
<div class="danger"><span class="lbl">Undigested regurgitation</span> Regurgitated <b>undigested</b> food never reached the stomach; a pouch or a non-emptying esophagus held it. With a <b>neck</b> finding it is a Zenker pouch; with dysphagia to <b>liquids from day one</b> it is achalasia. In both, the first study is the esophagram. Endoscopy comes first only with an alarm feature for cancer (weight loss, smoking, progressive solid dysphagia) and no neck finding.</div>
<div class="pearls"><span class="lbl">Pearls</span> Zenker is a false (pulsion) diverticulum: mucosa and submucosa herniate through the posterior wall between the inferior pharyngeal constrictor and the cricopharyngeus · the mechanism is <b>cricopharyngeal motor dysfunction</b> (diminished relaxation), not structural weakness alone · halitosis comes from food decaying in the pouch · the main complication is <b>aspiration pneumonia</b> · treatment is <b>cricopharyngeal myotomy</b>, with diverticulectomy for larger pouches</div>
<div class="pearls"><span class="lbl">Pairs with</span> Ask: is the regurgitated food undigested, and is the finding in the neck or in the chest?</div>
<div class="rule"><span class="lbl">Transferable rule</span> When the diagnosis implies a blind pouch or cavity the instrument cannot see, image it before instrumenting it: esophagram before endoscopy in Zenker, as with ultrasound before the needle in a hip effusion.</div>
<div class="traps"><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Upper endoscopy is ordered too early; a blind scope can perforate the pouch that the esophagram would have shown.</span></div><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Weight loss and age suggest cancer, but undigested regurgitation with a neck gurgle indicates a pouch, and the esophagram evaluates both.</span></div><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Manometry evaluates motility disorders such as achalasia, not a pharyngeal pouch.</span></div></div>
</div>
```

### `feeding-refusal`: Toddler Food Refusal

```html
<div class="brief" id="feeding-refusal" data-shelf="fm peds" data-nid="1482255679162" data-bp="gi behav">
<h4>Toddler Food Refusal</h4>
<p class="sub">Toddler who will not advance past purees &middot; Is he refusing a texture, a food group, or eating altogether — and is he atopic?</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 18 mo, stuck on pureed textures, eczema, weight fallen from the 25th to the 5th percentile &middot; <b>Labs</b> &mdash; swallow study normal &middot; <b>Q</b> &mdash; the most appropriate test; options spanned endoscopy with esophageal biopsy, tissue transglutaminase antibody and allergy skin testing</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>He is not anorexic and is not avoiding a food group; he refuses a <b>texture</b>. Children normally advance from purees to solids between 6 and 12 months, and failure to advance in a toddler suggests dysphagia. The <b>swallow study is normal</b>, so the problem is below the pharynx. Because <b>development is normal</b>, a behavioral or autism-spectrum feeding disorder is unlikely. The <b>stools are soft and daily with a benign abdomen</b>, which argues against celiac disease or an intraabdominal process. That leaves esophageal inflammation. His <b>eczema</b> supports eosinophilic esophagitis, since most patients are atopic. The diagnosis is histologic, so the test is <b>endoscopy with esophageal biopsy</b>.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Eosinophilic esophagitis</b> &mdash; endoscopy with esophageal biopsy showing <b>≥15 eosinophils per high-power field</b>, with alternative diagnoses such as achalasia and infection excluded &middot; <b>The texture milestone</b> &mdash; advancement from purees to solids normally occurs between <b>6 and 12 months</b>; failure to advance is itself the abnormal finding &middot; <b>What a normal swallow study buys</b> &mdash; it excludes oropharyngeal dysfunction and aspiration, moving the lesion below the pharynx</div>
<div class="pearls"><span class="lbl">Pertinent positives &amp; negatives</span> <b>Prefers purees, refuses all solid meat, fruit and vegetables</b> &mdash; a texture-based refusal, not a food-group avoidance; the toddler presentation of esophageal disease &middot; <b>History of eczema</b> &mdash; atopy, present in most patients with eosinophilic esophagitis &middot; <b>Weight from the 25th to the 5th percentile with height at the 30th</b> &mdash; a caloric deficit; weight crosses percentiles before height does &middot; <b>Normal swallow study</b> &mdash; oropharyngeal dysfunction and aspiration are excluded, so repeat swallow imaging adds nothing &middot; <b>Development otherwise normal</b> &mdash; argues against a developmental or behavioral feeding disorder &middot; <b>Daily soft stools, no diarrhea or vomiting, soft nondistended abdomen</b> &mdash; celiac disease typically brings diarrhea or constipation with pain and distension, and none is present &middot; <b>Moist mucous membranes, normal vital signs</b> &mdash; chronic and compensated, not acute; no resuscitation is needed &middot; <b>Refusal of every solid rather than of bread and pasta</b> &mdash; points to the esophagus rather than gluten</div>
<table data-mask="3">
<caption>The toddler who stops advancing his diet — the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th><th>Excluded here by</th></tr></thead>
<tbody>
<tr><td><b>Eosinophilic esophagitis</b></td><td>Th2 response to food antigen; comorbid atopy; age-shifting presentation</td><td><b>Failure to advance past purees in an atopic toddler</b>; ≥15 eosinophils per hpf on biopsy</td><td>— (the answer)</td></tr>
<tr><td>Celiac disease</td><td>Gluten-driven enteropathy; poor weight gain with malabsorption</td><td><b>Diarrhea or constipation with pain and distension</b>; avoidance of <i>gluten-rich</i> foods specifically</td><td>Soft daily stools, benign abdomen, refusal of all solids</td></tr>
<tr><td>Oropharyngeal dysphagia</td><td>Neuromuscular disease or incoordination; aspiration risk</td><td><b>Coughing and choking with feeds</b>; abnormal video swallow study</td><td>The swallow study is normal</td></tr>
<tr><td>Anatomic obstruction (stricture, ring, vascular ring ⚠︎)</td><td>Fixed narrowing; solids worse than liquids</td><td><b>Abrupt onset or a caustic/reflux history</b>; a lesion on esophagram or endoscopy</td><td>No such history; endoscopy would show it, which is why the scope is still the answer</td></tr>
<tr><td>Developmental or behavioral feeding disorder</td><td>Sensory aversion, autism spectrum, learned avoidance</td><td><b>Developmental delay or a normal endoscopy</b> with feeding therapy as the answer</td><td>Development is normal for age</td></tr>
<tr><td>Systemic causes of poor gain <i>(hyperthyroidism, intraabdominal mass)</i></td><td>Raised demand or anorexia from disease</td><td><b>Increased appetite with tachycardia and goiter</b>, or anorexia with a palpable mass</td><td>He refuses food and has a normal examination</td></tr>
</tbody></table>
<div class="danger"><span class="lbl">Management, in one line</span> Treatment: <b>dietary elimination is first-line</b>, with proton pump inhibitors and swallowed topical glucocorticoids as pharmacologic options and feeding therapy for the maladaptive eating that follows <i>(all in-context)</i>.</div>
<div class="pearls"><span class="lbl">Decision spine</span> <b>Is he refusing food, or is he not hungry?</b> &mdash; Refusing → a mechanical or inflammatory problem, not a metabolic one &middot; <b>What exactly does he refuse?</b> &mdash; Every solid, tolerates purees → a texture problem &middot; <b>Is the swallow normal?</b> &mdash; Yes → the lesion is below the pharynx &middot; <b>Is he atopic?</b> &mdash; Eczema → eosinophilic esophagitis &middot; <b>What establishes it?</b> &mdash; Endoscopy with esophageal biopsy; the diagnosis rests on the eosinophil count, not serology</div>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>Weight and height on the growth chart</td><td>First</td><td>Weight falls to the <b>5th</b> percentile, height holds</td><td>Caloric deficit: a real problem, not picky eating</td></tr>
<tr><td>Video swallow study</td><td>First</td><td><b>Normal</b></td><td>Lesion is below the pharynx; abnormal with choking points to oropharyngeal dysphagia</td></tr>
<tr><td>Tissue transglutaminase IgA with total IgA</td><td>By branch</td><td><b>Positive</b></td><td>Celiac disease, when diarrhea, distension or gluten-food avoidance is present</td></tr>
<tr><td>Endoscopy with esophageal biopsy</td><td>Confirms</td><td><b>15 or more</b> eosinophils per high-power field</td><td>Eosinophilic esophagitis; normal biopsies point to a behavioral feeding disorder</td></tr>
<tr><td>Allergy skin testing</td><td>Skip</td><td>Shows IgE <b>sensitization</b> only</td><td>Cannot diagnose eosinophilic esophagitis; guides the elimination diet afterward</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="test" data-d1="Tissue transglutaminase antibody" data-d2="Allergy skin testing" data-item-id="q_cdf5f4d7e34e533e8129" data-item-version="2" data-item-status="ready" data-key-id="o_b72db814ee975d2ebf62" data-d1-id="o_af61ca299d38562ebc3e" data-d2-id="o_7573bbc1bb185f1fa0f5" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">18 mo stuck on purees with eczema, weight from the 25th to the 5th percentile, and a normal swallow study &rarr; <b>Endoscopy with esophageal biopsy</b> &rarr; 15 or more eosinophils per high-power field is diagnostic</li>
<li data-type="next" data-d1="Swallowed topical glucocorticoid" data-d2="Systemic prednisone" data-item-id="q_45aa1d404d5e57fd83e6" data-item-version="1" data-item-status="ready" data-key-id="o_defe20d6cec55d8bbc9c" data-d1-id="o_ce5ec1f1becb5ff5ad9a" data-d2-id="o_5b93bd8838405208affa">2 yo with biopsy-confirmed eosinophilic esophagitis; first-line treatment &rarr; <b>Dietary elimination</b> &rarr; Pharmacologic therapy is the next tier</li>
<li data-type="next" data-d1="Intravenous glucagon and observation" data-d2="Barium swallow" data-item-id="q_678a1543b2ad5d308512" data-item-version="1" data-item-status="ready" data-key-id="o_eba6c76abd3659959967" data-d1-id="o_d344e22421cc5f008b67" data-d2-id="o_6242992475f05f0887c6">16 yo with known eosinophilic esophagitis, a meat bolus impacted for 3 hours, now drooling &rarr; <b>Urgent endoscopy</b> &rarr; Adolescent presentation of the same disease</li>
<li data-type="dx" data-d1="Gastroesophageal reflux disease" data-d2="Celiac disease" data-item-id="q_969b250c9a615c07a972" data-item-version="1" data-item-status="ready" data-key-id="o_67e4620513b5545db725" data-d1-id="o_a3093953f47b5251b83a" data-d2-id="o_b61326c7715452beb745">8 yo, atopic, months of abdominal pain and vomiting; esophageal biopsies show 25 eosinophils per high-power field &rarr; <b>Eosinophilic esophagitis</b> &rarr; The school-age presentation</li>
<li data-type="next" data-d1="Endoscopy with esophageal biopsy" data-d2="Sweat chloride testing" data-item-id="q_5e007475c2595f2c8886" data-item-version="1" data-item-status="ready" data-key-id="o_8cbbd92421cf5ee2858a" data-d1-id="o_a3d0c385a8c05f0fb18f" data-d2-id="o_1d822af8a1b359b6a8c2">3 yo with poor weight gain, chronic diarrhea, a distended abdomen, and avoidance of bread and pasta &rarr; <b>Tissue transglutaminase IgA with a total IgA level</b> &rarr; Celiac disease</li>
<li data-type="next" data-d1="Endoscopy with esophageal biopsy" data-d2="Tissue transglutaminase antibody" data-item-id="q_1cefd39eb3ac5803b67f" data-item-version="1" data-item-status="ready" data-key-id="o_728c210eb0d15270ba00" data-d1-id="o_3a12bc02984755118eff" data-d2-id="o_16f934e617c25048a649">14 mo with coughing and choking during feeds and two prior pneumonias &rarr; <b>Video swallow study</b> &rarr; Oropharyngeal dysfunction with aspiration</li>
<li data-type="avoid" data-d1="Endoscopy with esophageal biopsy" data-d2="Esophageal biopsy eosinophil count" data-item-id="q_d5221ff63735558bab1e" data-item-version="1" data-item-status="ready" data-key-id="o_3f739619f90c50d780f4" data-d1-id="o_c3b32550b22a58b0be3f" data-d2-id="o_68e4650f6ce45e67b8b8">Toddler with suspected eosinophilic esophagitis; which test will not establish the diagnosis &rarr; <b>Allergy skin testing</b> &rarr; It diagnoses IgE-mediated allergy rather than this</li>
<li data-type="next" data-d1="Repeat endoscopy in 3 months" data-d2="Empiric swallowed glucocorticoid" data-item-id="q_806fc38bb7d858cb9442" data-item-version="1" data-item-status="ready" data-key-id="o_ed3125a755e151209f70" data-d1-id="o_49488a23a3525e72a5fd" data-d2-id="o_8f4ce7f057c255d280f8">2 yo with poor weight gain, normal development, no atopy, a normal swallow study, and normal endoscopy with normal biopsies &rarr; <b>Feeding therapy for a behavioral feeding disorder</b> &rarr; The scope has excluded the organ</li>
<li data-type="mech" data-d1="IgE-mediated mast cell degranulation" data-d2="Autoimmune destruction of esophageal mucosa" data-item-id="q_67a7790b6f665c538c29" data-item-version="1" data-item-status="ready" data-key-id="o_11cff8dc39805824a79b" data-d1-id="o_63bf2170ff125fe2a30c" data-d2-id="o_285009373ee85764a7ae">The immunologic basis of eosinophilic esophagitis &rarr; <b>A Th2-mediated response to food antigen</b> &rarr; Comorbid atopy is the clinical correlate</li>
<li data-type="claim" data-d1="To confirm the eosinophil count" data-d2="To determine whether glucocorticoids are indicated" data-item-id="q_3e10faf6ed0352829fb7" data-item-version="2" data-item-status="ready" data-key-id="o_b778db4dfd665d0a854e" data-d1-id="o_7cce80b4d0d55637a934" data-d2-id="o_3dc6fa83b3ce5bdcb2bd" data-lead-in="Which of the following is the main reason allergy testing may still be performed?">Child with confirmed eosinophilic esophagitis &rarr; <b>To guide dietary elimination given frequent concomitant IgE sensitivities</b> &rarr; After the diagnosis, never instead of it</li>
</ol>
<div class="danger"><span class="lbl">Decoy note</span> "Has always been a picky eater" suggests a behavioral cause, but development is normal. Soft daily stools with no diarrhea or vomiting argue against celiac disease and gastroenteritis. The eczema, listed in the past medical history, is supporting evidence for eosinophilic esophagitis and is easy to overlook.</div>
<div class="pearls"><span class="lbl">Pearls</span> A toddler stuck on purees with eczema and falling weight likely has eosinophilic esophagitis; endoscopic biopsy showing fifteen or more eosinophils confirms it. &middot; The type of refusal localizes the problem: a <b>texture</b> refusal points to the esophagus, a <b>food-group</b> refusal to celiac disease or an IgE allergy, and a poor <b>appetite</b> with normal eating to systemic or metabolic disease. &middot; Presentation varies with age: toddlers refuse solids, school-age children have abdominal pain and vomiting, and adolescents have dysphagia and food impaction. &middot; Atopy accompanies most cases, so eczema, asthma, allergic rhinitis or a known food allergy in a child refusing food is a clue. &middot; The diagnosis rests on the biopsy eosinophil count, not a serology or a skin test; allergy testing guides the elimination diet only after biopsy confirms the diagnosis. &middot; Dietary elimination is first-line, with a proton pump inhibitor or a swallowed topical glucocorticoid as pharmacologic options, and feeding therapy for learned food avoidance.</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part II <b>Faltering Weight</b> covers the general approach to poor weight gain and reading the growth curve; this brief covers the child who refuses food rather than simply failing to grow. Ask: <i>is he refusing food, and if so, a texture or a food group?</i> Celiac disease appears here only as a distractor; its serology-and-biopsy workup is not covered on this page.</div>
<div class="rule"><span class="lbl">Transferable rule</span> In feeding problems, refusal of a texture, refusal of a food group, and loss of appetite point to different diseases; identify which pattern is present before choosing a test.</div>
<div class="traps"><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Tissue transglutaminase antibody &mdash; Celiac disease causes diarrhea or constipation with pain and distension, and children avoid <b>gluten-rich</b> foods, not every solid; this child's stools and abdomen are normal</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Abdominal ultrasonography &mdash; A mass causes <b>anorexia</b>, not a preference for purees, and the abdomen is soft, nontender and nondistended</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Thyroid function tests &mdash; Hyperthyroidism increases appetite and causes tachycardia and goiter; this child refuses food</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Allergy skin testing &mdash; It diagnoses IgE-mediated allergy, which presents acutely with urticaria and angioedema; even in confirmed disease it only guides the diet, and the priority is establishing the diagnosis</span></div></div>
</div>
```

### `peds-constipation`: Constipation in a Child

```html
<div class="brief" id="peds-constipation" data-shelf="fm peds" data-nid="1531920182274" data-bp="gi">
<h4>Constipation in a Child</h4>
<p class="sub">Exclude alarm signs, then start an oral laxative before any rectal treatment &middot; Is growth normal and the examination benign, and is there stool in the rectum?</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 3 yo M, hard painful stools since toilet training began, normal growth, nontender abdomen, anal fissure &middot; <b>Q</b> &mdash; the most appropriate next step; options spanned an oral osmotic laxative, a rectal enema and abdominal radiography</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Stools were <b>daily and soft until toilet training began</b>, and the pain came before the hardness worsened. This is the <b>withholding cycle</b>: a painful stool leads the child to hold, the rectum desiccates the retained stool, and the next stool hurts more. The <b>anal fissure</b> results from the cycle and worsens it. Growth on the 75th percentile, a nontender abdomen and a normal perineum mean no alarm signs, so treat rather than investigate. Give <b>an oral osmotic laxative</b> to make the next stool painless.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Alarm signs</b> &mdash; delayed passage of meconium, fever or vomiting, <b>ribbon stools</b>, poor growth, severe abdominal distension, and abnormal examination findings such as a <b>displaced anus or a tuft at the gluteal cleft</b> &middot; <b>Cow's-milk limit</b> &mdash; <b>under 24 oz per day</b>; this child's 24 oz is at the limit, not above it &middot; <b>Complications that are not alarm signs</b> &mdash; anal fissure, hemorrhoids, enuresis and urinary tract infections; each argues <i>for</i> the functional diagnosis rather than against it</div>
<div class="pearls"><span class="lbl">Pertinent positives &amp; negatives</span> <b>Onset coincides with toilet training</b> &mdash; the commonest trigger, with solid-food and cow's-milk introduction and school entry; points to a behavioral rather than anatomic cause &middot; <b>Previously daily soft stools</b> &mdash; normal baseline function excludes a congenital motility defect, which would have presented earlier &middot; <b>Cries and screams with defecation</b> &mdash; pain drives withholding and is what the laxative treats &middot; <b>Growth tracking at the 75th percentile</b> &mdash; no growth alarm sign; effectively excludes Hirschsprung disease, hypothyroidism and celiac disease &middot; <b>Anal fissure</b> &mdash; a complication of hard stools and the reason to avoid a rectal enema &middot; <b>Abdomen firm and mildly distended but nontender</b> &mdash; stool load without obstruction; severe distension or tenderness would be an alarm sign &middot; <b>24 oz of milk, refuses fruit</b> &mdash; diet contributes and should be modified, not eliminated &middot; <b>Urinates in the toilet without difficulty</b> &mdash; normal bladder function argues against a neurologic cause</div>
<table data-mask="3">
<caption>Constipation in a child — the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th><th>Excluded here by</th></tr></thead>
<tbody>
<tr><td><b>Functional constipation</b></td><td>Toddler at a transition — toilet training, school entry, cow's milk; painful stool leads to withholding, which hardens the next stool</td><td><b>Normal growth and examination</b>, onset tied to a transition, anal fissure as a complication</td><td>— (the answer)</td></tr>
<tr><td>Hirschsprung disease <span class="tag t-em">Can't miss</span></td><td>Aganglionic distal segment; usually declares in the neonatal period</td><td><b>Delayed meconium beyond 48 hours</b> ⚠︎, ribbon stools, distension, poor growth; <b>anal fissures are uncommon</b></td><td>Passed meconium normally, thriving, fissure present</td></tr>
<tr><td>Congenital hypothyroidism</td><td>Slowed transit with systemic features</td><td><b>Poor linear growth, prolonged jaundice, hypotonia, large fontanelle</b> ⚠︎</td><td>Height and weight both on the 75th percentile</td></tr>
<tr><td>Tethered cord or spinal dysraphism</td><td>Occult dysraphism impairing sacral outflow</td><td><b>Sacral dimple, hair tuft or displaced anus</b>, with urinary symptoms and lower-limb findings</td><td>Normal perineal examination; urinates without difficulty</td></tr>
<tr><td>Celiac disease</td><td>Gluten enteropathy; constipation is a recognised presentation ⚠︎</td><td><b>Falling weight percentile</b>, distension with irritability, iron deficiency</td><td>Growth tracking, well nourished</td></tr>
<tr><td>Excessive cow's-milk intake</td><td>Fat and protein without fiber; slow transit and satiety that crowds out fiber</td><td><b>Milk volume well above 24 oz per day</b>, often with iron deficiency</td><td>24 oz is within the recommended range</td></tr>
</tbody></table>
<table>
<caption>Classify first — constipation in a child</caption>
<thead><tr><th>Axis</th><th>The stem sentence that settles it</th><th>Consequence for management</th></tr></thead>
<tbody>
<tr><td>Any alarm sign?</td><td>"Height and weight have been tracking along the 75th percentiles… remainder of the examination is unremarkable"</td><td>No — treat rather than investigate; the film and the manometry both die here</td></tr>
<tr><td>Impacted or not?</td><td>"abdomen is firm, mildly distended, and <b>nontender</b>"; no stool ball described</td><td>Not impacted — maintenance therapy without a disimpaction step</td></tr>
<tr><td>Is the rectum safe to instrument?</td><td>"An anal fissure is present"</td><td>The rectal route causes further trauma; if disimpaction were needed, go oral</td></tr>
<tr><td>Is the diet the driver?</td><td>"drinks 24 oz of milk… eats vegetables, meats, and grains"</td><td>Within limits — modify fiber and water rather than withdraw milk</td></tr>
</tbody></table>
<div class="pearls"><span class="lbl">Tier fingerprint</span> done: nothing has been tried yet &middot; normal: growth, perineum, abdominal tenderness and urinary function &middot; bothered: the child cries with every stool, so treat today rather than counsel and wait.</div>
<table>
<caption>Management ladder — constipation in a child</caption>
<thead><tr><th>Tier</th><th>Intervention</th><th>Escalate when</th></tr></thead>
<tbody>
<tr><td>1</td><td><b>Oral osmotic laxative</b> such as polyethylene glycol, plus increased dietary fiber and water, cow's milk kept under 24 oz per day, and age-appropriate toileting guidance — sitting after meals with the feet supported ⚠︎</td><td>A stool ball on examination or overflow soiling means disimpaction is needed first</td></tr>
<tr><td>2</td><td><b>Disimpaction</b> — high-dose oral polyethylene glycol, or an enema; <b>enemas are limited when an anal fissure is present</b> because they cause further rectal trauma. Follow with long-term maintenance so the dilated rectum can return to normal size</td><td>Failure to clear, or vomiting and severe pain suggesting obstruction, earns an abdominal x-ray</td></tr>
<tr><td>3</td><td><b>Constipation persisting despite standard therapy</b> — anorectal manometry; suction rectal biopsy is the confirmatory test for Hirschsprung disease ⚠︎</td><td>Manometry abnormal or alarm signs emerging means paediatric gastroenterology and an anatomic workup</td></tr>
<tr><td>Maintenance</td><td>Continue the laxative for months rather than days ⚠︎ — the goal is a painless stool often enough that the child unlearns withholding</td><td>Relapse on weaning means resuming and re-addressing the behavioural side</td></tr>
</tbody></table>
<div class="danger"><span class="lbl">Numbers that gate &amp; exit ramps</span> cow's milk under 24 oz per day and the alarm-sign list are in-context; the 48-hour meconium threshold, the duration of maintenance therapy and toileting-posture advice are ⚠︎. &middot; delayed meconium with ribbon stools and poor growth → Hirschsprung disease, manometry then rectal biopsy ⚠︎ &middot; sacral dimple, hair tuft or a displaced anus → spinal imaging for occult dysraphism &middot; vomiting or severe distension with pain → abdominal x-ray, because severe impaction mimics obstruction &middot; overflow soiling in an older child → impaction with encopresis, so disimpact before maintenance and tell the parents the soiling is not deliberate &middot; milk intake well above 24 oz with pallor → reduce milk and check for iron deficiency ⚠︎.</div>
<div class="pearls"><span class="lbl">Decision spine</span> <b>Any alarm sign?</b> &mdash; Growth normal, examination benign, meconium normal → no, so do not investigate &middot; <b>Is there an impaction?</b> &mdash; Nontender abdomen with no stool ball → no, so no disimpaction &middot; <b>Is the rectum instrumentable?</b> &mdash; There is a fissure → no rectal route even if one were needed &middot; <b>Is the diet outside limits?</b> &mdash; 24 oz of milk is at the ceiling rather than over it → modify rather than withdraw &middot; <b>What breaks the cycle?</b> &mdash; Make the next stool painless → an oral osmotic laxative</div>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>History, growth chart and perineal examination</td><td>First</td><td><b>No</b> alarm sign: normal growth, meconium and perineum</td><td>Functional constipation: treat without testing</td></tr>
<tr><td>None: clinical diagnosis</td><td>Confirms</td><td><b>No test</b> needed with a benign screen</td><td>Tests are only for alarm signs, to exclude the mimics</td></tr>
<tr><td>TSH and tissue transglutaminase IgA</td><td>By branch</td><td><b>Abnormal</b>, with poor growth</td><td>Hypothyroidism or celiac disease</td></tr>
<tr><td>MRI of the spine</td><td>By branch</td><td><b>Tethered cord</b> or dysraphism</td><td>Sacral tuft, dimple or displaced anus, urinary symptoms</td></tr>
<tr><td>Anorectal manometry or contrast enema</td><td>By branch</td><td><b>Absent</b> rectoanal inhibitory reflex, or a transition zone</td><td>Hirschsprung features or failure of standard therapy: rectal biopsy next</td></tr>
<tr><td>Suction rectal biopsy</td><td>Confirms</td><td><b>Absent</b> ganglion cells</td><td>Hirschsprung disease</td></tr>
<tr><td>Abdominal radiograph</td><td>Skip</td><td>Stool on film does <b>not</b> change treatment</td><td>Only for severe impaction with pain and vomiting that mimics obstruction</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="next" data-d1="Administer a rectal enema" data-d2="Obtain an abdominal radiograph" data-item-id="q_8aa6e356852d590c9185" data-item-version="1" data-item-status="ready" data-key-id="o_2674268b5df452ecabbc" data-d1-id="o_e7b449c65d955fa1a857" data-d2-id="o_38dcdf417308588bb0b6">3 yo M with hard painful stools since toilet training began, normal growth, a nontender abdomen and an anal fissure &rarr; <b>Initiate an oral osmotic laxative</b> &rarr; Functional constipation</li>
<li data-type="next" data-d1="Maintenance laxative alone" data-d2="Anorectal manometry" data-item-id="q_7cba7b54b2635b80b06b" data-item-version="1" data-item-status="ready" data-key-id="o_3ecf010f7fa751b98b69" data-d1-id="o_1be38d2ea6b25a92861a" data-d2-id="o_c537202423ec52b19f28">6 yo M with involuntary soiling of his underwear and a palpable suprapubic stool mass, without an anal fissure &rarr; <b>Disimpaction followed by maintenance laxative therapy</b> &rarr; Impaction with overflow incontinence</li>
<li data-type="next" data-d1="Rectal enema" data-d2="Glycerin suppository" data-item-id="q_4c0c7d7991e7564896e2" data-item-version="1" data-item-status="ready" data-key-id="o_ab41536d44d757999492" data-d1-id="o_cb80ee4bb2ab55fa9c38" data-d2-id="o_45867813e16e5570b9a8">4 yo F with fecal impaction requiring disimpaction who has a painful anal fissure on examination &rarr; <b>High-dose oral polyethylene glycol</b> &rarr; Enemas cause further rectal trauma</li>
<li data-type="next" data-d1="Discontinue cow's milk entirely" data-d2="Obtain anorectal manometry" data-item-id="q_d10eebfa393e5311a792" data-item-version="1" data-item-status="ready" data-key-id="o_f75b91e281905b5e8d9c" data-d1-id="o_e4271303823a5e699735" data-d2-id="o_c24a363923925594a234">2 yo M with constipation and pallor who drinks 40 oz of cow's milk daily and eats little else &rarr; <b>Reduce cow's milk intake and start a laxative</b> &rarr; Milk volume above the recommended limit</li>
<li data-type="next" data-d1="Initiate an oral osmotic laxative" data-d2="Obtain an abdominal radiograph" data-item-id="q_9eb260eb1cdb50aba219" data-item-version="1" data-item-status="ready" data-key-id="o_38e529c274ce541dbdc0" data-d1-id="o_07f3b3a031dd575c88a5" data-d2-id="o_ef7b554939dd5ad29bde">3 yo F with constipation, daytime urinary incontinence and a tuft of hair over the sacrum &rarr; <b>Magnetic resonance imaging of the spine</b> &rarr; Occult spinal dysraphism</li>
<li data-type="next" data-d1="Increase the laxative dose and continue" data-d2="Rectal enema" data-item-id="q_207db426203a5fd4a6d6" data-item-version="1" data-item-status="ready" data-key-id="o_c1599a11ae7c57f9ad31" data-d1-id="o_8687e723319b5574b0d7" data-d2-id="o_56217c257e745688bf83">5 yo M whose constipation persists after 3 months of adequate laxative and dietary therapy, with normal growth and examination &rarr; <b>Anorectal manometry</b> &rarr; Refractory to standard therapy</li>
<li data-type="dx" data-d1="Functional constipation" data-d2="Congenital hypothyroidism" data-item-id="q_7afe798554085c5c9016" data-item-version="1" data-item-status="ready" data-key-id="o_175457eee6b1555dbae0" data-d1-id="o_bddbdaeacaae58efa03a" data-d2-id="o_cf3227694be655df8a1f">Newborn who first passed meconium at 60 hours, now with ribbon-like stools, abdominal distension and poor weight gain &rarr; <b>Hirschsprung disease</b> &rarr; Manometry, then rectal biopsy</li>
<li data-type="dx" data-d1="Hirschsprung disease" data-d2="Functional constipation" data-item-id="q_2ef7953bc86d5b64ba2b" data-item-version="1" data-item-status="ready" data-key-id="o_a197633490fa528d886b" data-d1-id="o_e33b883b0f3b51c39830" data-d2-id="o_4273aac741c25ca0933c">8-month-old with constipation, prolonged jaundice, hypotonia and a large anterior fontanelle &rarr; <b>Congenital hypothyroidism</b> &rarr; Check the TSH</li>
<li data-type="mech" data-d1="Aganglionosis of the distal rectum" data-d2="Reduced colonic smooth muscle contractility from cow's-milk protein" data-item-id="q_eae0ddb937ed5593b9d1" data-item-version="3" data-item-status="ready" data-key-id="o_f1bce2af0f85507f83c1" data-d1-id="o_0f83658e1eee5606b739" data-d2-id="o_db53066f968a5342b1d1">Why one painful bowel movement can produce weeks of worsening constipation in a toddler &rarr; <b>Withholding desiccates stool in the rectum</b>&rarr; so the next defecation hurts more, which reinforces withholding; The cycle is the disease</li>
<li data-type="avoid" data-d1="Initiating an oral osmotic laxative" data-d2="Increasing dietary fiber and water" data-item-id="q_0a43b19d7318509f8a4d" data-item-version="1" data-item-status="ready" data-key-id="o_a905529757575b368c51" data-d1-id="o_57179d78edd955769612" data-d2-id="o_84110467f1175ad0a3b9">3 yo M with functional constipation who drinks 24 oz of cow's milk daily; which management is inappropriate &rarr; <b>Discontinuing cow's milk entirely</b> &rarr; It removes calcium and vitamin D without benefit</li>
<li data-type="next" data-d1="Replace dairy with soy products" data-d2="Begin polyethylene glycol" data-item-id="q_b3119ed1dc6e5738b3fd" data-item-version="2" data-item-status="ready" data-key-id="o_65832f81d6985bad920f" data-d1-id="o_91e927a49f585baaae76" data-d2-id="o_efd4b07e83325f9d913d">15-month-old with constipation since infancy refractory to dietary changes, thin caliber stools, distended abdomen, explosive stool and gas on rectal exam &rarr; <b>Contrast enema</b> &rarr; Hirschsprung disease</li>
</ol>
<div class="danger"><span class="lbl">Decoy note</span> <b>Refusing to eat fruit</b> and the milk volume suggest a dietary cause, but the milk is <i>at</i> the limit, not above it, so diet is a contributor to adjust. Finding <b>a firm, mildly distended abdomen</b> is not an alarm sign; the alarm signs are <i>severe</i> distension and tenderness, and neither is present. The <b>anal fissure</b> is an expected complication of functional constipation, not evidence of another diagnosis; its only effect on management is to rule out the rectal route.</div>
<div class="pearls"><span class="lbl">Pearls</span> A growing child with painful hard stools and a normal examination gets an oral osmotic laxative, not a rectal procedure or imaging. &middot; Childhood constipation is a <b>behavioural cycle with a mechanical consequence</b>; the laxative makes stools painless so the child stops withholding, and it continues for months rather than days ⚠︎. &middot; The three common triggers are <b>solid food and cow's milk, toilet training, and school entry</b>; onset at one of them supports the diagnosis. &middot; An anal fissure is a <b>complication</b> of constipation, not a competing diagnosis, and is the reason to disimpact by mouth rather than by rectum. &middot; Hirschsprung disease presents with <b>delayed meconium and poor growth</b>, and fissures are uncommon in it; normal growth with a fissure indicates functional disease. &middot; <b>Growth is the alarm sign that does the most work</b>: a child tracking a percentile has essentially excluded hypothyroidism, celiac disease and Hirschsprung disease. &middot; Enuresis and urinary tract infections are complications of constipation, so in a child with both, treat the bowel first.</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part II <b>Fecal Impaction &amp; Overflow Diarrhea</b> is the adult counterpart of tier 2: there the rectal vault is full and an enema is first-line; here the vault is not full and the fissure rules out the rectal route. Part I <b>Infant Stool Complaints: Dyschezia, FPIAP &amp; Secondary Lactase Deficiency</b> covers infants, and Part II <b>Tethered Cord and Closed Spinal Dysraphism</b> covers the dysraphism the perineal examination screens for. Ask: is growth normal, and is there stool in the rectum?</div>
<div class="rule"><span class="lbl">Transferable rule</span> With no alarm signs and a normal examination, treat; investigate only when an alarm sign is present. A complication of the diagnosis supports it but can still change management, as an anal fissure rules out the rectal route.</div>
<div class="traps"><div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Discontinue milk: 24 oz is <b>within</b> the recommended 16 to 24 oz range; stopping it removes calcium and vitamin D with no benefit</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Obtain abdominal radiograph: The film is for <b>severe</b> impaction that mimics obstruction, with pain and vomiting; this abdomen is nontender and benign</span></div><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Administer rectal enema: There is no impaction to disimpact, and the <b>anal fissure</b> makes the rectal route actively harmful here</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Obtain anorectal manometry: Reserved for constipation that <b>persists despite standard therapy</b>; no therapy has been tried and no alarm sign is present</span></div></div>
</div>
```

### `bs-tef`: Tracheoesophageal Fistula with Esophageal Atresia

```html
<div class="brief bs" id="bs-tef" data-shelf="peds" data-nid="1539169473947 1578924962847" data-bp="newborn gi">
<h4>Tracheoesophageal Fistula with Esophageal Atresia</h4>
<p class="sub">Choking on the first feed · pass a tube before you order a picture</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 3 h old term boy born at home, coughs and vomits on his first breastfeed, formula mixed with saliva in his mouth, coarse breath sounds with retractions, soft systolic murmur at the upper left sternal border &middot; <b>Q</b> &mdash; the most appropriate next step; options spanned nasogastric tube placement, lateral neck radiography and echocardiography</div>
<div class="dp"><span class="lbl">The decision point</span>
<p><b>Formula mixed with saliva</b> means the milk filled a blind proximal pouch and overflowed without reaching the stomach. With choking on the <b>very first feed</b> and coarse lungs from aspiration, this is <b>esophageal atresia with a distal tracheoesophageal fistula</b>.</p>
<p>The first step is to <b>pass a nasogastric tube</b> at the bedside. It meets resistance at the pouch, and the film shows it coiled. The murmur, maternal drug history and absent prenatal care do not call for imaging or drug treatment first.</p>
</div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Type C</b> — proximal pouch with a distal fistula, about 85% of cases &middot; <b>Gas in the abdomen</b> — a distal fistula is present &middot; <b>Gasless abdomen</b> — pure atresia with no distal fistula &middot; <b>H-type</b> — no atresia, presenting months later with recurrent pneumonia</div>
<table>
<caption>Neonatal choking and vomiting — the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th></tr></thead>
<tbody>
<tr><td><b>EA with distal TEF</b></td><td>Choking on the first feed, copious frothy secretions, polyhydramnios in utero</td><td><b>Formula mixed with saliva</b>; tube will not pass</td></tr>
<tr><td>Congenital diaphragmatic hernia</td><td>Severe distress at delivery</td><td><b>Scaphoid abdomen</b>, bowel gas in the chest, shifted heart sounds</td></tr>
<tr><td>Congenital heart disease</td><td>Feeding difficulty with cyanosis</td><td><b>Cyanosis and diaphoresis with feeds</b>, no excess secretions</td></tr>
<tr><td>Epiglottitis</td><td>Febrile stridor with drooling</td><td><b>School-aged child</b>, never a newborn</td></tr>
<tr><td>Hypertrophic pyloric stenosis</td><td>Nonbilious projectile vomiting</td><td><b>Age 3 to 6 weeks</b>, hungry after vomiting, olive mass</td></tr>
<tr><td>Respiratory distress syndrome</td><td>Preterm surfactant deficiency</td><td><b>Ground-glass with air bronchograms</b>, low lung volumes</td></tr>
<tr><td>Neonatal abstinence syndrome</td><td>Maternal opioid use</td><td><b>Onset at or beyond 24 hours</b>, hypertonia and irritability</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>Nasogastric tube passage</td><td>First</td><td>Meets <b>resistance</b> at the pouch</td><td>Esophageal atresia likely: film with the tube in place</td></tr>
</tbody>
<tbody class="grp">
<tr><td>Chest and abdominal x-ray with the tube</td><td>Confirms</td><td>Tube <b>coiled</b> in the upper chest</td><td>Esophageal atresia</td></tr>
<tr><td></td><td></td><td><b>Gas</b> below the diaphragm</td><td>Distal fistula present (type C)</td></tr>
<tr><td></td><td></td><td><b>Gasless</b> abdomen</td><td>Pure atresia, no distal fistula</td></tr>
</tbody>
<tbody>
<tr><td>Echocardiogram and renal ultrasound</td><td>Next</td><td><b>VACTERL</b> anomalies</td><td>Screen after the diagnosis, before repair</td></tr>
<tr><td>Bronchoscopy or prone contrast esophagram</td><td>By branch</td><td><b>H-type</b> fistula</td><td>Tube passes; months of cough with feeds and recurrent pneumonia</td></tr>
<tr><td>Barium esophagram or endoscopy</td><td>Skip</td><td>Contrast can <b>aspirate</b> from the blind pouch</td><td>The coiled tube on film already confirms atresia</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="next" data-src="uworld" data-nid="1482203661732 1482203669616 1531933927642 1556997242950" data-d1="Lateral neck radiograph" data-d2="Echocardiogram" data-item-id="q_cc6bbef9bb48533c9ac4" data-item-version="1" data-item-status="ready" data-key-id="o_494a01a95b39558e8cf2" data-d1-id="o_330605bbdb2e57c7bfeb" data-d2-id="o_dc1b6c0910a85e9c9e04">3 h old term boy born at home, coughs and vomits on his first breastfeed, formula mixed with saliva in his mouth, coarse breath sounds with retractions, soft systolic murmur at the upper left sternal border &rarr; <b>Nasogastric tube placement</b> &rarr; Esophageal atresia with distal tracheoesophageal fistula</li>
<li data-type="next" data-src="authored" data-d1="Barium esophagram" data-d2="Flexible upper endoscopy" data-item-id="q_22db29be3a585f47b3d1" data-item-version="1" data-item-status="ready" data-key-id="o_6f1d65ff41c15579b872" data-d1-id="o_57a50e6b2ee655918846" data-d2-id="o_d9359cc619645523b639">2 h old term girl drooling frothy secretions who choked on her first feed; a nasogastric tube meets firm resistance and will not advance &rarr; <b>Chest x-ray with the tube in place</b> &rarr; A coiled tube confirms atresia; gas below the diaphragm means a distal fistula</li>
<li data-type="dx" data-src="authored" data-d1="Esophageal atresia with a distal fistula" data-d2="Duodenal atresia" data-item-id="q_bfea49b73852550e8341" data-item-version="1" data-item-status="ready" data-key-id="o_5647a7d16aec59ce81ca" data-d1-id="o_963e1cbb7a365cd48b55" data-d2-id="o_e00f401d147f5b4fa5bb">Term newborn girl, maternal polyhydramnios, drooling; the feeding tube coils in the upper chest on x-ray and the abdomen is completely gasless &rarr; <b>Esophageal atresia without a fistula</b> &rarr; No tracheal connection, so no air reaches the stomach</li>
<li data-type="dx" data-src="authored" data-d1="Gastroesophageal reflux disease" data-d2="Laryngomalacia" data-item-id="q_ce540f2e6f6f5b18b05d" data-item-version="1" data-item-status="ready" data-key-id="o_4126856d90f452c6b1c8" data-d1-id="o_bbd8f791ebb854969b81" data-d2-id="o_078c6faf411d5bce9807">8 mo old boy with three right upper lobe pneumonias and coughing and choking with liquid feeds since birth; a feeding tube passes easily into the stomach &rarr; <b>H-type tracheoesophageal fistula</b> &rarr; Bronchoscopy or prone contrast esophagram</li>
<li data-type="screen" data-src="authored" data-d1="TORCH titers" data-d2="Head ultrasound" data-item-id="q_7399db4494935cbb8f38" data-item-version="2" data-item-status="ready" data-key-id="o_c0950b66f182517e9ccc" data-d1-id="o_0fbab1850a20559abb25" data-d2-id="o_de68499dc7d457afbc24" data-lead-in="Which of the following is the most appropriate evaluation for associated anomalies?">Term newborn boy with esophageal atresia and a distal fistula confirmed on x-ray, before surgical repair &rarr; <b>Echocardiogram and renal ultrasound</b> &rarr; VACTERL association</li>
<li data-type="next" data-src="authored" data-d1="Immediate pyloromyotomy" data-d2="Thickened feeds and reflux precautions" data-item-id="q_67b52b60d4e5557a9151" data-item-version="1" data-item-status="ready" data-key-id="o_ca9c7a590bcb5a7f919b" data-d1-id="o_78ee988e405b5ad99cdc" data-d2-id="o_b43ae298a2275bb180a8">4 wk old boy with a week of nonbilious projectile vomiting, hungry after each episode, ultrasound showing a thickened elongated pylorus, low chloride and high bicarbonate &rarr; <b>IV fluids and electrolyte repletion</b> &rarr; Hypertrophic pyloric stenosis; pyloromyotomy once the alkalosis corrects</li>
<li data-type="next" data-src="authored" data-d1="Upper GI contrast series" data-d2="Emergency laparotomy" data-item-id="q_8f3af02e91b95e46b987" data-item-version="1" data-item-status="ready" data-key-id="o_9393b364d05b5544a772" data-d1-id="o_30e4e1a8943e51b686ff" data-d2-id="o_55f5e2bd8b0e5a42a0da">Newborn girl with upslanting palpebral fissures and a single palmar crease, maternal polyhydramnios, bilious vomiting on day 1, abdominal x-ray with a double bubble and no distal gas &rarr; <b>Nasogastric decompression and IV fluids</b> &rarr; Duodenal atresia; repair after stabilization and an echocardiogram</li>
<li data-type="dx" data-src="authored" data-d1="Transient tachypnea of the newborn" data-d2="Meconium aspiration syndrome" data-item-id="q_a94bc94df05658fb8694" data-item-version="1" data-item-status="ready" data-key-id="o_95c26258a09256538307" data-d1-id="o_bbdd61be8a7551369546" data-d2-id="o_0f189e76005c541f8ed8">30 wk preterm boy grunting and retracting at 1 h of life, x-ray with diffuse ground-glass opacities, air bronchograms and low lung volumes &rarr; <b>Respiratory distress syndrome</b> &rarr; CPAP, then surfactant if the oxygen requirement rises</li>
<li data-type="next" data-src="authored" data-d1="Oral morphine" data-d2="Naloxone" data-item-id="q_080d915d1e6e5dab870e" data-item-version="1" data-item-status="ready" data-key-id="o_5cd8c8aabc1451ceaffb" data-d1-id="o_c95db98e9c2f55ccac50" data-d2-id="o_edc525682ef65fe0b05c">36 h old girl, irritable and tremulous with a high-pitched cry, sneezing and feeding poorly; mother maintained on methadone &rarr; <b>Swaddling, low stimulation and rooming-in</b> &rarr; Neonatal abstinence syndrome; morphine only if nonpharmacologic care fails</li>
<li data-type="next" data-src="authored" data-d1="Small, frequent oral feeds held upright" data-d2="Intubation and positive-pressure ventilation" data-item-id="q_739ce4828c185fb3ae60" data-item-version="1" data-item-status="ready" data-key-id="o_020f8069df1256459a0b" data-d1-id="o_725f66a31c565cc087c9" data-d2-id="o_30d9bf66c9025bb7b03d">Term newborn boy with esophageal atresia and a distal fistula confirmed on x-ray, saturating 96% in room air, awaiting surgical repair &rarr; <b>NPO, head elevated, continuous pouch suction</b> &rarr; Keeps pooled saliva out of the lungs and gastric acid out of the fistula</li>
</ol>
<div class="danger"><span class="lbl">Age at presentation</span> Age at presentation narrows the differential. <b>Minutes to hours</b>: TEF/EA, choanal atresia, diaphragmatic hernia, respiratory distress syndrome, Potter sequence. <b>Beyond 24 hours</b>: neonatal abstinence, sepsis, ductal-dependent lesions as the PDA closes, bilious vomiting and malrotation. <b>3 to 6 weeks</b>: hypertrophic pyloric stenosis. <b>Months</b>: H-type fistula, laryngomalacia. Each wrong option here is a real disease that presents at a different age.</div>
<div class="pearls"><span class="lbl">Pearls</span> Polyhydramnios in utero, because the fetus cannot swallow amniotic fluid &middot; Diagnosis is made by passing the tube: resistance at roughly 9 to 11 cm, confirmed on film &middot; The abdominal gas pattern shows the anatomic type without endoscopy &middot; VACTERL screening after diagnosis: <b>echocardiogram and renal ultrasound</b> at minimum &middot; A soft systolic murmur on day one is usually a closing ductus, not structural disease</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part II <b>Posterior Urethral Valves and Potter Sequence</b> shares the mechanism in reverse: a fetus that cannot make urine has oligohydramnios and Potter sequence, and a fetus that cannot swallow has polyhydramnios and foregut or duodenal atresia. Part I <b>Cyanosis in the Newborn</b> covers cyanosis that worsens with feeding and improves with crying, which is choanal atresia, not a fistula. Part I <b>Multiple Anomalies in a Newborn</b> covers VACTERL alongside the syndromes it is mistaken for and what excludes each.</div>
<div class="rule"><span class="lbl">Transferable rule</span> When a newborn chokes or vomits with the first feed, first check whether a nasogastric tube reaches the stomach, before any imaging or drug. Imaging only confirms what the tube found. The other options are real diseases that present at other ages.</div>
<div class="traps">
<div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Epiglottitis is a febrile school-age disease; a 3-hour-old cannot have it.</span></div>
<div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Echocardiography is indicated for VACTERL screening, after the diagnosis, not before it.</span></div>
<div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Pyloric stenosis needs 3 to 6 weeks for the muscle to hypertrophy, and it gives projectile vomiting, not coughing with saliva-mixed formula at 3 hours.</span></div>
<div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Surfactant treats respiratory distress syndrome in the preterm lung; this is a term newborn whose retractions come from aspirated secretions, which surfactant does not fix.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">The maternal drug history points at neonatal abstinence syndrome, but withdrawal typically begins at 24 hours or later, never pools saliva or causes coughing with feeds, and is treated first without drugs.</span></div>
</div>
</div>
```
