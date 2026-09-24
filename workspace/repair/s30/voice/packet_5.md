# Voice packet 5 of 5 (s30, gi): fap, cyclic-vomiting, occult-gi-bleed, bs-galactosemia

**Instructions.** Everything you need is in this packet. Do not open index.html, the skill files or other packets. Write your edits to `repair/s30/04_voice_5.json`, run `python3 tools/verify_edits.py repair/s30/04_voice_5.json scratch/s30_base.html --voice` from the workspace folder (Step2Haki/workspace) and loop until it prints PASS (add `--report` to read your own claim map). Then reply with the 3 to 5 line report the rules ask for, including any acronym you skipped.

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
### `fap`: Familial Adenomatous Polyposis

```html
<div class="brief" id="fap" data-shelf="fm" data-bp="gi">
<h4>Familial Adenomatous Polyposis</h4>
<p class="sub">Known APC carrier: when to start screening and when to operate · APC, hundreds of adenomas, cancer by 40</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 12 yo M, asymptomatic, father has familial adenomatous polyposis &middot; <b>Labs</b> &mdash; APC testing positive &middot; <b>Q</b> &mdash; the most appropriate screening step; options spanned annual sigmoidoscopy or colonoscopy starting now, colonoscopy at age 40 and prophylactic colectomy now</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>An <b>APC</b> mutation (autosomal dominant) causes <b>hundreds to thousands</b> of adenomas and colon cancer in nearly <b>100% by age 40</b>. Screening is <b>annual sigmoidoscopy or colonoscopy from age 10–12</b> (puberty), not the first-degree-relative or average-risk schedule. A <b>prophylactic proctocolectomy</b> is planned for the teens to early 20s and is indicated <b>at any age</b> for bleeding, polyps over 1 cm, innumerable polyps, or high-grade dysplasia.</p>
<p>Colonoscopy at 40, or 10 years before the relative's cancer, is the schedule for sporadic family history and does not apply to a known APC carrier. After colectomy, continue <b>upper endoscopy</b> for duodenal and ampullary adenomas.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Familial adenomatous polyposis</b> — autosomal dominant APC mutation, hundreds to thousands of colonic adenomas, colon cancer in nearly 100% before age 40 · <b>Screening gate</b> — annual sigmoidoscopy or colonoscopy starting at puberty, age 10–12 · <b>Colectomy gate</b> — prophylactic proctocolectomy in the teens to early 20s, or at any age with GI bleeding, polyps over 1 cm, innumerable polyps, or high-grade dysplasia · <b>Upper tract</b> — upper endoscopy for duodenal and ampullary adenomas · <b>Gardner syndrome</b> — FAP plus osteomas and desmoid tumors · <b>Turcot syndrome</b> — FAP plus CNS tumors</div>
<table>
<caption>Management ladder — familial adenomatous polyposis</caption>
<thead><tr><th>Tier</th><th>Intervention</th><th>Escalate when</th></tr></thead>
<tbody>
<tr><td>0</td><td><b>APC genetic testing</b> of at-risk children of an affected parent</td><td>Mutation found, or testing unavailable → screen as affected</td></tr>
<tr><td>1</td><td><b>Annual sigmoidoscopy or colonoscopy from age 10–12</b></td><td>Polyposis develops → plan surgery; any colectomy trigger → operate now</td></tr>
<tr><td>2</td><td><b>Prophylactic proctocolectomy</b> (or colectomy with ileorectal anastomosis), usually teens to early 20s</td><td>Immediately, at any age: GI bleeding, polyps over 1 cm, innumerable polyps, high-grade dysplasia</td></tr>
<tr><td>3</td><td><b>Upper endoscopy</b> surveillance for duodenal and ampullary adenomas, continued after colectomy</td><td>Retained rectum after ileorectal anastomosis keeps its own endoscopic surveillance</td></tr>
</tbody>
</table>
<table>
<caption>Hereditary colon cancer syndromes — the differential</caption>
<thead><tr><th>Syndrome</th><th>Illness script</th><th>The NBME tell</th></tr></thead>
<tbody>
<tr><td><b>Familial adenomatous polyposis</b></td><td>APC, autosomal dominant; adenomas carpet the colon from adolescence</td><td><b>Hundreds of polyps</b>; scope from puberty, colectomy in the teens to 20s</td></tr>
<tr><td>Gardner syndrome</td><td>FAP variant</td><td>Polyposis plus <b>osteomas and desmoid tumors</b></td></tr>
<tr><td>Turcot syndrome</td><td>FAP variant</td><td>Polyposis plus <b>CNS tumors</b></td></tr>
<tr><td>Lynch syndrome (HNPCC)</td><td>Mismatch-repair mutation; few polyps, early right-sided cancer; endometrial and other cancers in the family</td><td><b>Early colon cancer with few polyps</b> and an endometrial cancer in the pedigree</td></tr>
<tr><td>Peutz-Jeghers syndrome</td><td>Hamartomatous polyps that intussuscept or bleed</td><td><b>Mucocutaneous pigmentation</b> of lips and buccal mucosa</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody class="grp">
<tr><td>APC testing, child of an affected parent</td><td>Screen</td><td><b>Positive</b> for the family mutation</td><td>Carrier: annual sigmoidoscopy or colonoscopy from age 10 to 12</td></tr>
<tr><td></td><td></td><td><b>Negative</b> for the known family mutation</td><td>Not a carrier: average-risk screening</td></tr>
</tbody>
<tbody class="grp">
<tr><td>Annual sigmoidoscopy or colonoscopy</td><td>Confirms</td><td><b>Hundreds</b> of adenomas</td><td>Polyposis: proctocolectomy planned for the teens to early 20s</td></tr>
<tr><td></td><td></td><td>Bleeding, polyps <b>over 1 cm</b>, innumerable polyps or high-grade dysplasia</td><td>Proctocolectomy now, at any age</td></tr>
</tbody>
<tbody>
<tr><td>Upper endoscopy</td><td>Next</td><td><b>Duodenal or ampullary</b> adenomas</td><td>Upper-tract surveillance continues after colectomy</td></tr>
<tr><td>Colonoscopy at 40 or annual FIT</td><td>Skip</td><td>Sporadic family-history <b>timing</b></td><td>Wrong pathway for an APC carrier</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="screen" data-d1="Colonoscopy at age 40" data-d2="Prophylactic colectomy now" data-item-id="q_bc8d39f8aa24524ba41b" data-item-version="1" data-item-status="ready" data-key-id="o_6b31c81ac1a954c9ac24" data-d1-id="o_097cb0567794530fba1f" data-d2-id="o_49cc0a56c7695509b536">12 yo M whose father has familial adenomatous polyposis; APC testing positive; asymptomatic &rarr; <b>Annual sigmoidoscopy or colonoscopy starting now</b> &rarr; the screening gate opens at puberty, age 10–12</li>
<li data-type="next" data-d1="Reassure and begin average-risk screening as an adult" data-d2="Annual fecal immunochemical testing" data-item-id="q_2d70179b757859ed83dd" data-item-version="1" data-item-status="ready" data-key-id="o_964a8bc82aba58a7ba12" data-d1-id="o_f8aefa98becc5ad4b23e" data-d2-id="o_5e79b68acf0155479679">10 yo F whose mother has FAP; the child has never been tested &rarr; <b>APC genetic testing</b> &rarr; a positive result starts annual endoscopic screening</li>
<li data-type="next" data-d1="Proctocolectomy now" data-d2="Repeat colonoscopy in 5 years" data-item-id="q_a6d9a08fb91858f79a06" data-item-version="1" data-item-status="ready" data-key-id="o_67e733cad016573496ba" data-d1-id="o_f092f66199a05cdb89e2" data-d2-id="o_15c0e9fddfee55cb98a6">14 yo M with FAP, colonoscopy shows a few small adenomas under 1 cm, no dysplasia, no bleeding &rarr; <b>Continue annual colonoscopy and plan colectomy for the late teens to early 20s</b> &rarr; no immediate trigger is present</li>
<li data-type="next" data-d1="Endoscopic polypectomy of the largest polyps" data-d2="Segmental colectomy of the involved region" data-item-id="q_da6ec107ad0c58e28fe2" data-item-version="1" data-item-status="ready" data-key-id="o_5cc8b4d30c725dc5aaaf" data-d1-id="o_871ce558ddcb5e34b0ff" data-d2-id="o_63c59e330fc05f2a92bc">17 yo F with FAP, colonoscopy shows <b>innumerable polyps</b>, several over 1 cm, one with <b>high-grade dysplasia</b> &rarr; <b>Total proctocolectomy</b> &rarr; a colectomy trigger is met at any age</li>
<li data-type="next" data-d1="Colonoscopy with polypectomy and iron supplementation" data-d2="Repeat colonoscopy in 1 year" data-item-id="q_a07dc81e540857c5a4d0" data-item-version="1" data-item-status="ready" data-key-id="o_f13c99901a115856af1e" data-d1-id="o_c0a241cbff3c505db856" data-d2-id="o_43fb184cd280507da90b">19 yo M with FAP under annual surveillance, now with <b>rectal bleeding</b> and iron deficiency &rarr; <b>Colectomy now</b> &rarr; bleeding is an any-age indication</li>
<li data-type="screen" data-d1="Annual abdominal CT for desmoid tumors" data-d2="No further surveillance is needed" data-item-id="q_31bc4ce1f2d9551a9a2b" data-item-version="1" data-item-status="ready" data-key-id="o_c3e1c364b29458ecb453" data-d1-id="o_dd6985c78293577ab17f" data-d2-id="o_a3d71154687c538c9285">23 yo F, total proctocolectomy for FAP 2 years ago, asymptomatic &rarr; <b>Upper endoscopy for duodenal and ampullary adenomas</b> &rarr; colectomy does not remove upper-tract risk</li>
<li data-type="dx" data-d1="Turcot syndrome" data-d2="Peutz-Jeghers syndrome" data-item-id="q_6af7a0f0681452519d15" data-item-version="1" data-item-status="ready" data-key-id="o_3ebe6cb7ab10503cbef2" data-d1-id="o_9e573397fbb7508288df" data-d2-id="o_37fdc4782ad853d88dee">28 yo M with hundreds of colonic adenomas, a <b>mandibular osteoma</b>, and a firm abdominal-wall <b>desmoid</b> tumor &rarr; <b>Gardner syndrome</b> &rarr; FAP pathway, same colectomy rules</li>
<li data-type="dx" data-d1="Familial adenomatous polyposis" data-d2="Peutz-Jeghers syndrome" data-item-id="q_7e8bb124480a52c983d2" data-item-version="1" data-item-status="ready" data-key-id="o_8d714a2fa8965bc5935c" data-d1-id="o_d403382fc7ca50b7a2f3" data-d2-id="o_fb6bf9b8406752eb81d1">36 yo F with right-sided colon cancer, <b>12 polyps</b> on colonoscopy, a mother with endometrial cancer at 45 and a brother with colon cancer at 42 &rarr; <b>Lynch syndrome</b> &rarr; mismatch-repair testing of the tumor</li>
</ol>
<div class="danger"><span class="lbl">Exceptions</span> These numbers apply to a <b>known APC carrier</b>. A first-degree relative with sporadic colon cancer follows a different schedule (earlier than average-risk screening, but not annual scoping from puberty), and a Lynch pedigree (few polyps, endometrial cancer in the family) follows a third. Any of <b>bleeding, polyps over 1 cm, innumerable polyps, or high-grade dysplasia</b> means colectomy now rather than in the teens to early 20s.</div>
<div class="pearls"><span class="lbl">Pearls</span> APC is autosomal dominant, so each child of an affected parent has a one-in-two risk and is tested rather than presumed · screening starts at puberty because adenomas appear in adolescence and cancer follows within decades · <b>Gardner</b> adds osteomas and desmoids, <b>Turcot</b> adds CNS tumors; both are managed as FAP · colectomy does not address duodenal and ampullary adenomas, which need upper endoscopy · Lynch has few polyps, a mismatch-repair mechanism and endometrial cancer in the pedigree</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Postmenopausal Bleeding</b> lists Lynch syndrome among the endometrial cancer risk factors; Lynch syndrome and its colorectal screening intervals are not covered on this page. Ask: how many polyps, and is there an APC mutation?</div>
<div class="rule"><span class="lbl">Transferable rule</span> Identify the hereditary syndrome first; start age, interval and operation all depend on it, and sporadic family-history numbers do not apply to a known carrier.</div>
<div class="traps"><div class="trapline"><span class="pill p-number">Wrong parameter</span><span class="trapwhy">Colonoscopy at 40 is the sporadic family-history schedule; an APC carrier is scoped annually from puberty.</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Polypectomy of the largest lesions is not enough once innumerable polyps or dysplasia indicate colectomy.</span></div><div class="trapline"><span class="pill p-uniform">Uniform-answer doubt</span><span class="trapwhy">Surveillance continues after colectomy because the duodenum and ampulla remain at risk.</span></div></div>
</div>
```

### `cyclic-vomiting`: Cyclic Vomiting Syndrome

```html
<div class="brief" id="cyclic-vomiting" data-shelf="peds" data-nid="1516474878334 1516475159634" data-bp="gi">
<h4>Cyclic Vomiting Syndrome</h4>
<p class="sub">Stereotyped episodes, well in between &middot; the pattern is the diagnosis</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 9-year-old girl, 8 months of nausea, vomiting and diffuse abdominal pain for several days each month; episodes begin early morning, recur <b>10&ndash;15 times daily for 2 days</b>, nonbloody and nonbilious; more frequent at the start of the school year; two admissions for intravenous hydration &middot; <b>Between episodes</b> &mdash; active, eating well, growth at the 25th percentile and unchanged &middot; <b>Exam</b> &mdash; well hydrated, <b>erosive maxillary caries</b>, soft nontender abdomen, normal neurologic examination &middot; <b>Q</b> &mdash; the most likely cause; options spanned bulimia, chronic pancreatitis, cyclic vomiting, factitious disorder imposed on another, reflux and inflammatory bowel disease</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Three features together make this cyclic vomiting syndrome: episodes that are <b>stereotyped</b>, <b>self-limited over 1 to 2 days</b>, and complete wellness between them with <b>normal growth</b>. Stress at the start of term is the trigger; most patients have a personal or family history of migraine. It is a diagnosis of exclusion, supported by wellness between episodes.</p>
<p>The erosive caries are <b>evidence that the vomiting is real and recurrent</b>, not evidence of purging; there is no bingeing, no restriction and no preoccupation with shape.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Stereotyped episodes</b> &mdash; the same acute nausea, abdominal pain, headache and vomiting each time &middot; <b>Duration</b> &mdash; self-limited over 1 to 2 days &middot; <b>Interval</b> &mdash; often regular, around 2 to 4 weeks, and asymptomatic between &middot; <b>Association</b> &mdash; personal or family history of migraine &middot; <b>Triggers</b> &mdash; infection or stress</div>
<table data-mask="last">
<caption>Recurrent vomiting in a child &mdash; the differential<span class="cap-sub">what happens between the episodes</span></caption>
<thead><tr><th>Diagnosis</th><th>Between episodes</th><th>Key discriminator</th><th>What to do</th></tr></thead>
<tbody>
<tr><td><b>Cyclic vomiting syndrome</b></td><td><b>Entirely well</b>, growing normally</td><td>Stereotyped, self-limited, regular intervals; migraine history</td><td>Rehydration and antiemetics; triptans may abort</td></tr>
<tr><td>Bulimia nervosa</td><td>Preoccupied with shape and weight</td><td><b>Bingeing with compensatory behaviour</b></td><td>Psychiatric assessment</td></tr>
<tr><td>Chronic pancreatitis</td><td>Poor growth, diarrhoea</td><td><b>Epigastric tenderness</b> on examination</td><td>Pancreatic imaging and enzyme studies</td></tr>
<tr><td>Inflammatory bowel disease</td><td>Weight loss, fever, ongoing symptoms</td><td><b>Diarrhoea with abdominal tenderness</b></td><td>Inflammatory markers and endoscopy</td></tr>
<tr><td>Gastroesophageal reflux</td><td>Ongoing low-grade symptoms</td><td><b>Regurgitation and substernal pain</b>, not episodic bursts</td><td>Trial of acid suppression</td></tr>
<tr><td>Factitious disorder imposed on another</td><td>Inconsistent history, symptoms unwitnessed</td><td>No objective corroboration of the illness</td><td>Careful documentation; child protection</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>Electrolytes, glucose and BUN during an episode</td><td>First</td><td>Dehydration changes <b>only</b></td><td>Rehydrate; tests are drawn during the episode to exclude urgent causes</td></tr>
<tr><td>Lipase, liver enzymes and urinalysis</td><td>By branch</td><td><b>Normal</b></td><td>Excludes pancreatitis, hepatobiliary and urinary causes</td></tr>
<tr><td>Upper GI contrast series</td><td>By branch</td><td><b>Malrotation</b> excluded</td><td>Required when vomiting is bilious or the pattern is atypical</td></tr>
<tr><td>Brain MRI</td><td>By branch</td><td><b>Mass</b> or hydrocephalus</td><td>Only with an abnormal neurologic examination</td></tr>
<tr><td>None: clinical diagnosis</td><td>Confirms</td><td>Stereotyped episodes, <b>well between</b>, normal growth</td><td>Cyclic vomiting syndrome; the tests only exclude mimics</td></tr>
<tr><td>Upper endoscopy</td><td>Skip</td><td>Adds <b>nothing</b> with normal growth and no alarm features</td><td>Reserve for weight loss, diarrhea or bleeding</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="dx" data-d1="Bulimia nervosa" data-d2="Factitious disorder imposed on another" data-src="uworld" data-item-id="q_1973afbf6f9ebf23ead0" data-item-version="1" data-item-status="ready" data-key-id="o_9159ebc8b357741a38f5" data-d1-id="o_eed0183280f294c28b94" data-d2-id="o_d71691d039603b32fef1">9 year old with 8 months of stereotyped vomiting episodes lasting 2 days, 10-15 times daily, entirely well between them, normal growth, erosive maxillary caries &rarr; <b>Cyclic vomiting syndrome</b> &rarr; A diagnosis of exclusion with predictable intervals</li>
<li data-type="mech" data-d1="Recent travel or food exposure" data-d2="A family history of peptic ulcer disease" data-src="uworld" data-item-id="q_7f71d5f727d4704c2a31" data-item-version="1" data-item-status="ready" data-key-id="o_a9aa0775d00ace526b2e" data-d1-id="o_c6ec6e3a3b4605b79c55" data-d2-id="o_972e5b0bc2fde58e2a52">The historical association that supports cyclic vomiting syndrome &rarr; <b>Personal or family history of migraine</b> &rarr; Triggers are often infection or stress</li>
<li data-type="next" data-d1="Upper endoscopy during the episode" data-d2="Psychiatric admission" data-src="uworld" data-item-id="q_8bbe05e746faebca3426" data-item-version="1" data-item-status="ready" data-key-id="o_689717a9d01f4c7d8135" data-d1-id="o_5780daea8639ff9678f1" data-d2-id="o_14c9d65e3d605e0224dd">Child with established cyclic vomiting syndrome presenting mid-episode, dehydrated &rarr; <b>Intravenous rehydration with an antiemetic</b> &rarr; Abortive triptans may shorten the episode</li>
<li data-type="dx" data-d1="Cyclic vomiting syndrome" data-d2="Gastroesophageal reflux disease" data-src="uworld" data-item-id="q_884ed6c3b6e5c3eaefc9" data-item-version="1" data-item-status="ready" data-key-id="o_06f00d26f0e3047e148f" data-d1-id="o_072d2e3b8ae43d1c76ca" data-d2-id="o_9f7a9fe469b5a3a4dfd7">Adolescent with self-induced vomiting after binge eating, preoccupied with body shape, normal weight &rarr; <b>Bulimia nervosa</b> &rarr; Bingeing and compensatory behaviour, not stereotyped episodes</li>
<li data-type="dx" data-d1="Cyclic vomiting syndrome" data-d2="Inflammatory bowel disease" data-src="uworld" data-item-id="q_5a5d257bed5b813be446" data-item-version="1" data-item-status="ready" data-key-id="o_94c052e9d99821c75abe" data-d1-id="o_2d38ac68e21f68ef9946" data-d2-id="o_c01bb3cd0b81517cc039">Child with recurrent abdominal pain, vomiting, diarrhoea, poor growth and epigastric tenderness &rarr; <b>Chronic pancreatitis</b> &rarr; Growth failure and tenderness, unlike the well-between-episodes pattern</li>
<li data-type="claim" data-d1="Proof of self-induced vomiting" data-d2="An independent nutritional deficiency" data-src="uworld" data-item-id="q_6ff125a4c6711d3ec1f0" data-item-version="1" data-item-status="ready" data-key-id="o_7a6745e64a3b0ec8afcc" data-d1-id="o_4aa1feecc06579358b5a" data-d2-id="o_96a863f742c7dd44b94a">What the erosive dental caries in a child with recurrent vomiting indicates &rarr; <b>Evidence that the vomiting is real and recurrent</b> &rarr; It supports the history rather than implying purging</li>
</ol>
<div class="danger"><span class="lbl">Gates</span> <b>Bilious vomiting, weight loss, fever or an abnormal neurologic examination</b> argues against cyclic vomiting and needs urgent evaluation &middot; <b>Growth must be normal</b> &mdash; faltering growth needs further evaluation &middot; Laboratory work and imaging are usually done <b>during</b> an acute episode to exclude the urgent causes, not between them &middot; Most children outgrow it during adolescence</div>
<div class="pearls"><span class="lbl">Pearls</span> <b>Symptom-free intervals</b> &mdash; episodes are regular and predictable, and the child is well between them &middot; Dental erosion shows recurrent acid exposure, not its cause &middot; Migraine history is the most useful historical clue &middot; As a diagnosis of exclusion, the workup targets dangerous mimics</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Headache in a Child: What Earns Imaging</b> covers migraine, which shares this condition's biology. Ask: how is the child between episodes?</div>
<div class="rule"><span class="lbl">Transferable rule</span> For episodic illness, ask how the patient is between episodes; the interval holds most of the diagnostic information.</div>
<div class="traps">
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Dental erosion suggests purging, but she has no bingeing, restriction or preoccupation with shape.</span></div>
<div class="trapline"><span class="pill p-unchecked">Unchecked attribute</span><span class="trapwhy">Normal growth is stated and excludes the chronic inflammatory and malabsorptive options.</span></div>
</div>
</div>
```

### `occult-gi-bleed`: Occult GI Bleeding in a Child

```html
<div class="brief" id="occult-gi-bleed" data-shelf="peds fm" data-nid="1482289546088 1482289549128 1535916392937 1537640546225" data-bp="gi">
<h4>Occult GI Bleeding in a Child</h4>
<p class="sub">Occult GI bleeding after a negative upper endoscopy and colonoscopy &middot; age decides the next study</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 10-year-old boy, 2 months of exertional fatigue and exercise intolerance; <b>no melena, hematochezia or abdominal pain</b>; no medications &middot; <b>Exam</b> &mdash; mucosal pallor, no lymphadenopathy, soft nontender abdomen, <b>stool positive for occult blood</b> &middot; <b>Labs</b> &mdash; hemoglobin 9.4, MCV 74, platelets 380,000, leukocytes 7,500; ESR and coagulation normal; <b>upper endoscopy and colonoscopy with biopsies unremarkable</b> &middot; <b>Q</b> &mdash; which study most likely reveals the diagnosis; options spanned CT angiography, fecal calprotectin, fecal DNA, technetium 99m pertechnetate scan and tissue transglutaminase antibodies</div>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 2 yo M, dark red formed stool in the diaper; eating and drinking well but more tired than usual; lives on a ranch with cattle and goats; afebrile, pale; abdomen soft, nondistended, nontender, no masses; no anal fissures or hemorrhoids; stool occult blood positive &middot; <b>Labs</b> &mdash; WBC 8,000, Hct 27%, platelets 320,000 &middot; <b>Q</b> &mdash; the study most likely to confirm the diagnosis; options spanned technetium-99m pertechnetate scan, abdominal CT, abdominal ultrasound, air contrast enema, bacterial stool culture, cow&#39;s milk elimination diet and upper endoscopy</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Iron deficiency anemia with a positive occult blood test and <b>no visible bleeding</b> is occult gastrointestinal bleeding. Both ends have been scoped and are clean, so the source is in the <b>small bowel</b>, which neither scope reaches. In a child the most common small-bowel bleeding lesion is a <b>Meckel diverticulum</b>, found by a <b>technetium 99m pertechnetate scan</b>, which images ectopic gastric mucosa rather than the bleeding.</p>
<p>An adult with the same negative workup gets <b>capsule endoscopy</b>, because adult small-bowel causes are angiodysplasia, neoplasia and ulcers.</p>
<p>A Meckel diverticulum can also bleed <b>visibly</b>. A toddler with <b>painless</b> dark red or maroon stool, pallor and a soft, <b>nontender</b> abdomen, without diarrhea, vomiting or fever, goes <b>straight to the pertechnetate scan</b> without endoscopy first. <b>Pain</b> suggests a complication or a different disease and changes the first test.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Occult GI bleeding</b> &mdash; positive fecal occult blood and/or iron deficiency anemia <b>without</b> visible bleeding &middot; <b>First step regardless of age</b> &mdash; upper endoscopy and colonoscopy &middot; <b>Child, source not found</b> &mdash; technetium 99m pertechnetate scan for Meckel &middot; <b>Adult, source not found</b> &mdash; capsule endoscopy, then CT or MR enterography &middot; <b>Meckel</b> &mdash; failed closure of the vitelline (omphalomesenteric) duct, the most common congenital GI anomaly, with ectopic gastric mucosa that ulcerates adjacent small bowel</div>
<table data-mask="last">
<caption>Occult GI bleeding in a child: what each study answers</caption>
<thead><tr><th>Study</th><th>What it detects</th><th>Who it is for</th><th>Why not here</th></tr></thead>
<tbody>
<tr><td><b>Tc 99m pertechnetate scan</b></td><td>Ectopic gastric mucosa</td><td><b>Child</b> with small-bowel bleeding</td><td>&mdash; (the answer)</td></tr>
<tr><td>Capsule endoscopy</td><td>Angiodysplasia, neoplasia, ulcers</td><td><b>Adult</b> with small-bowel bleeding</td><td>Right idea, wrong age branch</td></tr>
<tr><td>CT angiography</td><td>Brisk active bleeding</td><td>Hemodynamic instability with visible bleeding</td><td><b>Occult bleeding is too slow to see</b></td></tr>
<tr><td>Fecal calprotectin</td><td>Intestinal inflammation</td><td>Suspected inflammatory bowel disease</td><td>No pain, diarrhea or weight loss; scopes and biopsies clean</td></tr>
<tr><td>Tissue transglutaminase</td><td>Celiac disease</td><td>Malabsorptive iron deficiency</td><td><b>Celiac does not cause occult blood</b></td></tr>
<tr><td>Fecal DNA testing</td><td>Colorectal neoplasia</td><td>Average-risk adults over 45</td><td>Not a pediatric test</td></tr>
<tr><td>Upper endoscopy</td><td>Upper GI source</td><td><b>Hematemesis</b> or <b>black, sticky melena</b></td><td>Dark red or maroon stool without either is a lower source</td></tr>
<tr><td>Cow&#39;s milk elimination</td><td>Milk protein proctocolitis</td><td><b>Infant</b>, well, with blood-streaked stool</td><td>Resolves <b>by age 1</b>; a toddler is past the window</td></tr>
<tr><td>Abdominal ultrasound, then air enema</td><td>Intussusception</td><td>Child with <b>intermittent severe pain</b>, with or without bloody stool</td><td>The Meckel bleed is <b>painless</b></td></tr>
<tr><td>Bacterial stool culture</td><td>Bacterial colitis</td><td>Bloody <b>diarrhea</b> with crampy pain and fever</td><td>Formed stool, afebrile, no pain</td></tr>
<tr><td>Anal exam</td><td>Anal fissure</td><td>Bright red streaks on a hard stool, painful passage</td><td>Visible on exam; none here</td></tr>
<tr><td>Abdominal CT</td><td>Bowel and mass lesions</td><td>Abdominal trauma, abscess or tumor</td><td>Cannot reliably tell the diverticulum from other bowel loops</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>CBC and stool occult blood</td><td>First</td><td>Microcytic anemia, occult blood <b>positive</b></td><td>Occult GI bleeding</td></tr>
<tr><td>Upper endoscopy and colonoscopy</td><td>Next</td><td><b>Unremarkable</b>, biopsies clean</td><td>Source is in the small bowel</td></tr>
<tr><td>Technetium 99m pertechnetate scan</td><td>Confirms</td><td><b>Ectopic gastric mucosa</b></td><td>Meckel diverticulum, the child's small-bowel branch</td></tr>
<tr><td>Capsule endoscopy</td><td>By branch</td><td><b>Angiodysplasia</b>, neoplasia or ulcer</td><td>Adult branch; then CT or MR enterography</td></tr>
<tr><td>Tissue transglutaminase IgA</td><td>By branch</td><td><b>Positive</b>, with occult blood negative</td><td>Celiac disease: iron deficiency from malabsorption, not bleeding</td></tr>
<tr><td>CT angiography</td><td>Skip</td><td>Needs <b>brisk</b> active bleeding</td><td>Occult bleeding is too slow to show</td></tr>
<tr><td>Abdominal ultrasound</td><td>By branch</td><td><b>Target sign</b></td><td>Intussusception, when there is intermittent severe pain; air enema confirms and reduces it</td></tr>
<tr><td>Abdominal CT</td><td>Skip</td><td>Cannot separate the diverticulum from bowel loops</td><td>The pertechnetate scan answers the Meckel question</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="test" data-d1="Tissue transglutaminase antibodies" data-d2="CT angiography" data-src="uworld" data-item-id="q_2ee63804dd34cb933cbf" data-nid="1482289546088" data-item-version="2" data-item-status="ready" data-key-id="o_bafc7d0a1eb9f5df5230" data-d1-id="o_b36f572c37dc6339be73" data-d2-id="o_feb5b43f7b3f47a83a26" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">10 year old with 2 months of exertional fatigue, pallor, haemoglobin 9.4 with MCV 74, stool positive for occult blood; upper endoscopy and colonoscopy with biopsies are unremarkable &rarr; <b>Technetium 99m pertechnetate scan</b> &rarr; Meckel scan &mdash; it images ectopic gastric mucosa</li>
<li data-type="mech" data-d1="Venous congestion from a twisted mesentery" data-d2="Autoimmune villous atrophy" data-src="uworld" data-item-id="q_ea93d0e68589f7efae0e" data-item-version="1" data-item-status="ready" data-key-id="o_6657df31f3be277e7c84" data-d1-id="o_72a2419bd1221ed842e2" data-d2-id="o_f9a9b690c09efc3a38dd">How a Meckel diverticulum causes occult bleeding &rarr; <b>Ectopic gastric mucosa secreting acid</b> &rarr; Ulcerating adjacent small bowel</li>
<li data-type="next" data-d1="Technetium 99m pertechnetate scan" data-d2="Capsule endoscopy" data-src="uworld" data-item-id="q_4ebb2d84a9cdea8f120b" data-item-version="1" data-item-status="ready" data-key-id="o_4740e6d3cbd44067ab08" data-d1-id="o_00fc6455952bf9f9958b" data-d2-id="o_6174ddcb5c54b0f9fcff">Child with iron deficiency anaemia and a positive faecal occult blood test; the first step &rarr; <b>Upper endoscopy and colonoscopy</b> &rarr; Localise before reaching for small-bowel studies</li>
<li data-type="test" data-d1="Technetium 99m pertechnetate scan" data-d2="Faecal DNA testing" data-src="uworld" data-item-id="q_4be9f389933a59802b68" data-item-version="2" data-item-status="ready" data-key-id="o_19ed12128ce5e745f197" data-d1-id="o_ff3f73518ff3f75a0535" data-d2-id="o_c514a40bd63b7db51c94" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">Adult with occult gastrointestinal bleeding and a negative upper endoscopy and colonoscopy &rarr; <b>Capsule endoscopy</b> &rarr; Angiodysplasia, neoplasia and ulcers &mdash; the adult small-bowel causes</li>
<li data-type="dx" data-d1="Intussusception" data-d2="Milk protein proctocolitis" data-src="uworld" data-item-id="q_6547da545bf7230c1e2e" data-item-version="1" data-item-status="ready" data-key-id="o_deffb6c53ff6bec566d1" data-d1-id="o_4c040cb0e732a866f686" data-d2-id="o_28710da8bd7414f03d42">Child with painless hematochezia and no abdominal pain, age under 2 &rarr; <b>Meckel diverticulum</b> &rarr; Failed closure of the vitelline duct</li>
<li data-type="avoid" data-d1="Technetium 99m pertechnetate scan" data-d2="Capsule endoscopy" data-src="uworld" data-item-id="q_04376547aeb2ac228a0c" data-item-version="1" data-item-status="ready" data-key-id="o_a4b747ee51a6556ecf7d" data-d1-id="o_66dcea854ee94b82b597" data-d2-id="o_6fa023447593e21703b5">Child with slow occult blood loss and stable vital signs; which study is least likely to help &rarr; <b>CT angiography</b> &rarr; It needs brisk active bleeding to see anything</li>
<li data-type="dx" data-d1="Meckel diverticulum" data-d2="Inflammatory bowel disease" data-src="uworld" data-item-id="q_a7ed5a40912a683d78c2" data-item-version="1" data-item-status="ready" data-key-id="o_5aa862267699e29fe03e" data-d1-id="o_74cb039c306c8498a2e8" data-d2-id="o_0226cd55294eb81addf3">Child with microcytic anaemia, chronic diarrhoea and a negative faecal occult blood test &rarr; <b>Celiac disease</b> &rarr; Malabsorption, not blood loss &mdash; the occult blood is negative</li>
<li data-type="test" data-src="uworld" data-nid="1482289546088 1482289549128 1535916392937 1537640546225" data-d1="Cow&#x27;s milk elimination diet" data-d2="Upper endoscopy" data-item-id="q_3c3d26c6702192fc9f1b" data-item-version="1" data-item-status="ready" data-key-id="o_af4a5103ed3633ff7aa9" data-d1-id="o_3ad1e7d733a7fb778f6f" data-d2-id="o_9d25788f65f0ae8ec4aa" data-lead-in="Which of the following is most likely to confirm the diagnosis?">2-year-old boy with dark red, formed stool in his diaper; eating and drinking well but more tired than usual; lives on a ranch with cattle and goats; afebrile and pale; abdomen soft, nondistended and nontender without masses; no anal fissures or hemorrhoids; stool positive for occult blood; hematocrit 27%, leukocytes 8,000/mm3, platelets 320,000/mm3 &rarr; <b>Technetium 99m pertechnetate scan</b> &rarr; Meckel diverticulum: ectopic gastric mucosa takes up the tracer; painless small-bowel bleeding in a toddler, and dark red stool without hematemesis or melena is not an upper GI bleed</li>
<li data-type="next" data-src="authored" data-d1="Technetium 99m pertechnetate scan" data-d2="Bacterial stool culture" data-item-id="q_8d33d86d7fb7d316c020" data-item-version="1" data-item-status="ready" data-key-id="o_206ae95011c01edd930f" data-d1-id="o_41d7976a688c0c290346" data-d2-id="o_eb42267505431de944b6">10-week-old boy fed cow&#x27;s milk-based formula with several days of mucus and streaks of blood in otherwise soft stools; feeding well, gaining weight, afebrile and playful; mild eczema on the cheeks; abdomen soft and nontender; no anal fissure on exam &rarr; <b>Switch to an extensively hydrolyzed formula</b> &rarr; milk protein proctocolitis: a non-IgE reaction in infants; bleeding clears once cow&#x27;s milk protein is removed, and it resolves by age 1</li>
<li data-type="test" data-src="authored" data-d1="Technetium 99m pertechnetate scan" data-d2="Abdominal CT" data-item-id="q_0ad993ae16f11e7dcb84" data-item-version="1" data-item-status="ready" data-key-id="o_66cc396e9181368c1b0d" data-d1-id="o_97fa1c11e3fcc5d15853" data-d2-id="o_6eb2a55210124c5a68da" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">2-year-old boy with 12 hours of sudden episodes of severe crying with his legs drawn up, quiet and sleepy between episodes; vomited twice; one stool of dark red blood and mucus (currant jelly); afebrile; a sausage-shaped mass in the right upper quadrant &rarr; <b>Abdominal ultrasound</b> &rarr; intussusception: pain is the tell; target sign on ultrasound, then air enema to confirm and reduce; a Meckel diverticulum can be the lead point</li>
<li data-type="next" data-src="authored" data-d1="Oral iron and observation" data-d2="Proton pump inhibitor therapy" data-item-id="q_5c10a61871584228864a" data-item-version="1" data-item-status="ready" data-key-id="o_1597f41ea084fff54794" data-d1-id="o_77589ee3a6a3e63a3d89" data-d2-id="o_f7bf8b07c43bf1f7c302">3-year-old girl with two episodes of painless maroon stool over the past month; pale, hematocrit 28%, vital signs normal; abdomen soft and nontender; technetium-99m pertechnetate scan shows a focus of uptake in the right lower quadrant &rarr; <b>Surgical resection</b> &rarr; a symptomatic Meckel diverticulum is removed to stop the bleeding and prevent intussusception, diverticulitis and obstruction; iron treats the anemia, not the source</li>
</ol>
<div class="danger"><span class="lbl">Stool color and bleeding source</span> Stool color follows <b>transit time</b>, not only where the blood started. Dark red or maroon stool in a toddler is a <b>lower</b> source, usually the small bowel, because the blood passes quickly. The upper GI picture is <b>hematemesis</b> with <b>black, sticky melena</b>, and it is more common in adults. This child had neither, so upper endoscopy is not the first test.</div>
<div class="danger"><span class="lbl">Gates</span> <b>Visible bleeding with instability</b> &mdash; hematemesis, melena or hematochezia goes to CT angiography, not a Meckel scan &middot; <b>Scope first for occult bleeding</b> &mdash; small-bowel studies are for after a clean upper endoscopy and colonoscopy; a toddler with <b>visible, painless</b> dark red stool goes straight to the pertechnetate scan &middot; <b>Meckel is classically under 2</b> but presents into adolescence, so age does not exclude it &middot; Balloon-assisted enteroscopy is the fallback when the source stays hidden</div>
<div class="pearls"><span class="lbl">Pearls</span> The Meckel scan detects <b>gastric mucosa</b>, not blood, so it works when the lesion is not actively bleeding &middot; <b>Occult</b> bleeding is too slow for angiography &middot; Celiac gives iron deficiency <b>without</b> occult blood; the FOBT separates them &middot; Here, small bowel means the segment the two scopes cannot reach &middot; Painless hematochezia in a toddler is Meckel until proven otherwise &middot; <b>Rule of 2s</b>: often presents by age 2, usually under 2 inches long, within 2 feet of the ileocecal valve &middot; The bleed is <b>painless</b>; pain comes from complications: intussusception with the diverticulum as lead point, diverticulitis that mimics appendicitis, obstruction or perforation &middot; A symptomatic Meckel diverticulum is <b>surgically resected</b> to stop the bleeding and prevent those complications</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>The Distended Abdomen in a Newborn or Infant</b> covers the obstructed and acutely bleeding infant gut. Part I <b>Microcytic Anemia: Iron First</b> covers the iron-versus-thalassemia fork that precedes this workup. Ask: is the bleeding visible, and have both ends been scoped?</div>
<div class="rule"><span class="lbl">Transferable rule</span> When an algorithm branches on age, the same negative workup can send a child and an adult to different tests.</div>
<div class="traps">
<div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Capsule endoscopy is the adult small-bowel study; a child gets the pertechnetate scan.</span></div>
<div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Ordering a small-bowel study before upper endoscopy and colonoscopy are done.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Microcytic anemia in a child pulls toward celiac serology, which the positive FOBT excludes.</span></div>
<div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Milk elimination fits painless blood in an infant, but milk protein proctocolitis resolves by age 1; a 2-year-old is past it.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Ranch animals pull toward bacterial colitis, which needs bloody diarrhea, crampy pain and fever.</span></div>
<div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Endoscopy is right for hematemesis and black melena; dark red stool without either points below.</span></div>
</div>
</div>
```

### `bs-galactosemia`: The Sick Jaundiced Neonate with a Positive Screen

```html
<div class="brief bs" id="bs-galactosemia" data-shelf="peds" data-nid="1474165315038 1484603517328 1516557603865 1539168087031 1539459932653" data-bp="newborn gi">
<h4>The Sick Jaundiced Neonate with a Positive Screen</h4>
<p class="sub">Sick neonate with a positive newborn screen · conjugated jaundice, hepatomegaly, urine reducing sugar</p>
<div class="vignette" data-recon="partial"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; neonate after ten days of milk feeds, now febrile with hepatomegaly; newborn screen reported positive by telephone &middot; <b>Labs</b> &mdash; conjugated hyperbilirubinemia; a non-glucose reducing substance in the urine &middot; <b>Q</b> &mdash; the most appropriate next step; options spanned stopping lactose-containing feeds, continuing feeds pending confirmatory testing, and admission for intravenous antibiotics</div>
<div class="dp"><span class="lbl">The decision point</span>
<p><b>Conjugated</b> hyperbilirubinemia, a <b>large liver</b>, and a <b>non-glucose reducing sugar in the urine</b> after ten days of milk feeds indicate <b>classic galactosemia</b> (GALT deficiency; galactose-1-phosphate accumulates in the liver). Galactosemia predisposes to <b>Escherichia coli sepsis</b>, so start the sepsis workup and antibiotics while stopping lactose.</p>
</div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Conjugated hyperbilirubinemia</b> — direct bilirubin above 1.0 mg/dL &#9888;, or above 20% of total; never physiologic and never breast-milk jaundice &middot; <b>Urine reducing substances</b> — positive with dipstick glucose negative means a non-glucose reducing sugar, so galactose or fructose; requires recent intake of that sugar to be positive &#9888; &middot; <b>Classic galactosemia</b> — galactose-1-phosphate uridyltransferase deficiency, confirmed by red cell GALT enzyme activity &#9888;, which reads falsely normal after transfusion</div>
<table>
<caption>The screen-positive neonate - the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th></tr></thead>
<tbody>
<tr><td><b>Classic galactosemia</b></td><td>Autosomal recessive GALT deficiency, symptoms within days of milk feeds</td><td><b>Conjugated jaundice with hepatomegaly and urine reducing substances</b> in a milk-fed neonate</td></tr>
<tr><td>Galactokinase deficiency</td><td>Autosomal recessive block one step earlier; galactose is diverted to galactitol</td><td><b>Cataracts in a well infant</b>; no liver disease, no sepsis</td></tr>
<tr><td>Congenital rubella syndrome</td><td>Fetal infection in a mother not immune to rubella</td><td><b>Cataracts with deafness and a PDA</b>, blueberry muffin rash; present at birth, not triggered by milk</td></tr>
<tr><td>Urea cycle disorder</td><td>Hyperammonemia in the first days of feeding</td><td><b>Very high ammonia</b> with lethargy and respiratory alkalosis; no jaundice, hepatomegaly or cataracts</td></tr>
<tr><td>Hereditary fructose intolerance</td><td>Aldolase B deficiency, identical hepatic picture with hypoglycemia</td><td><b>Onset with fruit, juice or sucrose</b> at weaning, months old rather than days; essential fructosuria is the benign cousin, a urinary sugar with no illness</td></tr>
<tr><td>Biliary atresia <span class="tag t-em">Can't miss</span></td><td>Obstructive cholestasis, Kasai before about 60 days</td><td><b>Direct hyperbilirubinemia in a well infant with acholic stools</b>, reducing substances negative</td></tr>
<tr><td>Maple syrup urine disease</td><td>Branched-chain ketoacid dehydrogenase deficiency, day 4 to 7 &#9888;</td><td><b>Encephalopathy without hepatomegaly or cholestasis</b>, sweet-smelling urine, ketosis</td></tr>
<tr><td>Cystic fibrosis</td><td>Screened by immunoreactive trypsinogen</td><td><b>Meconium ileus or quiet cholestasis</b>, not fever with vomiting and urinary sugar</td></tr>
<tr><td>Sickle cell or neonatal hyperthyroidism</td><td>Screen-positive with no hepatic picture</td><td><b>No cholestasis, no hepatomegaly, no urinary sugar</b>; sickle is silent at 10 days because of HbF</td></tr>
<tr><td>Glycogen storage disease type I</td><td>Hepatomegaly, fasting hypoglycemia, lactic acidosis, hypertriglyceridemia</td><td><b>Hypoglycemia within hours of fasting</b>; no galactose trigger, no cataracts</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>Total and direct bilirubin</td><td>First</td><td><b>Conjugated</b> fraction raised</td><td>Never physiologic: galactosemia, sepsis or biliary atresia</td></tr>
<tr><td>Urine reducing substances with dipstick glucose</td><td>Next</td><td>Reducing substance <b>positive</b>, glucose negative</td><td>Galactose or fructose: stop lactose now; falsely negative once feeds stop</td></tr>
<tr><td>Blood, urine and CSF cultures</td><td>By branch</td><td><b>E. coli</b> growth</td><td>Febrile neonate: antibiotics in parallel, not after</td></tr>
<tr><td>Red cell GALT enzyme activity</td><td>Confirms</td><td><b>Absent</b> or near-absent activity</td><td>Classic galactosemia; falsely normal after transfusion</td></tr>
<tr><td>Abdominal ultrasound and HIDA scan</td><td>By branch</td><td><b>No</b> excretion into the bowel</td><td>Well infant, acholic stools, reducing substances negative: biliary atresia</td></tr>
<tr><td>Serum galactose level or liver biopsy</td><td>Skip</td><td>Does <b>not</b> name the enzyme defect</td><td>Red cell GALT activity is the confirmatory test</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-src="handoff" data-type="next" data-d1="Continue breastfeeding until confirmatory testing returns" data-d2="Admit for intravenous antibiotics" data-item-id="q_295d462b4c705e3facf1" data-item-version="1" data-item-status="ready" data-key-id="o_bc5610205819520d958d" data-d1-id="o_96a7405144765fb5b86a" data-d2-id="o_b486571df8fd528b8642">3-day-old, asymptomatic, breastfeeding well, newborn screen positive for galactosemia &rarr; <b>Stop breastfeeding and start soy-based formula pending confirmation</b> &rarr; presumptive galactosemia</li>
<li data-src="authored" data-type="next" data-d1="Phototherapy and continue breastfeeding" data-d2="Liver transplant evaluation" data-item-id="q_9f0568882aea52bab399" data-item-version="1" data-item-status="ready" data-key-id="o_63916c6b4841567caee8" data-d1-id="o_ee88b83b83925ed4a910" data-d2-id="o_299f0876136b51db841e">8-day-old with jaundice, hepatomegaly, vomiting after breastfeeds and positive urine reducing substances &rarr; <b>Stop breast milk and start soy-based formula</b> &rarr; classic galactosemia</li>
<li data-src="authored" data-type="next" data-d1="Blood and urine cultures, then IV ceftriaxone" data-d2="Blood and urine cultures, then observe off antibiotics" data-item-id="q_3b3b3b16ecad50c28538" data-item-version="2" data-item-status="ready" data-key-id="o_fff2095859cf519f9a66" data-d1-id="o_14ccd055aa70500fb220" data-d2-id="o_700577e2c37959e7ac59">12-day-old with galactosemia on soy formula, temperature 38.8 C, lethargic &rarr; <b>Blood, urine and CSF cultures, then IV ampicillin and gentamicin</b> &rarr; Escherichia coli sepsis; every febrile neonate gets a lumbar puncture</li>
<li data-src="authored" data-type="test" data-d1="Serum galactose level" data-d2="Liver biopsy" data-item-id="q_66a38fc6f1645f498b16" data-item-version="2" data-item-status="ready" data-key-id="o_b6ded2ef9f9f51d19fe4" data-d1-id="o_d905a872be2a5fc8af1b" data-d2-id="o_1e15506241a65d738a54" data-lead-in="Which of the following is most likely to confirm the diagnosis?">10-day-old with jaundice, hepatomegaly, positive urine reducing substances and a newborn screen positive for galactosemia &rarr; <b>Red cell GALT enzyme activity</b> &rarr; classic galactosemia</li>
<li data-src="authored" data-type="mech" data-d1="Galactose-1-phosphate deposition in the lens" data-d2="Sorbitol accumulation" data-item-id="q_7fd63f20e52d5f7d8f86" data-item-version="1" data-item-status="ready" data-key-id="o_11026b00a0fe5406bd7e" data-d1-id="o_6dd1eda1ddf550338288" data-d2-id="o_0dadcf939c12504eaa61">3-week-old with galactosemia and bilateral cataracts on examination &rarr; <b>Galactitol accumulation via aldose reductase</b> &rarr; osmotic lens injury</li>
<li data-src="authored" data-type="dx" data-d1="Classic galactosemia" data-d2="Congenital rubella syndrome" data-item-id="q_09deb04a563656a8a30a" data-item-version="1" data-item-status="ready" data-key-id="o_d94b27df25f45df5a41f" data-d1-id="o_d29438102d0252419fd8" data-d2-id="o_394e3ab9279358a9bd36">6-week-old, well and growing, bilateral cataracts only, no hepatomegaly, positive urine reducing substances &rarr; <b>Galactokinase deficiency</b> &rarr; lactose-free diet</li>
<li data-src="authored" data-type="dx" data-d1="Classic galactosemia" data-d2="Glycogen storage disease type I" data-item-id="q_dd7f36b418b352b1abf0" data-item-version="1" data-item-status="ready" data-key-id="o_ac6ffc39cb3252f5bbd3" data-d1-id="o_e77caf3fc5b55b6d8e15" data-d2-id="o_b09a563966c8578b9320">9-month-old with vomiting, hypoglycemia, hepatomegaly and jaundice since juice and fruit were introduced, positive urine reducing substances &rarr; <b>Hereditary fructose intolerance</b> &rarr; remove fructose, sucrose and sorbitol</li>
<li data-src="authored" data-type="next" data-d1="Phototherapy" data-d2="Kasai portoenterostomy now" data-item-id="q_48eaa885ee67553eac6e" data-item-version="1" data-item-status="ready" data-key-id="o_eae8cb822707577996bb" data-d1-id="o_f47620666e5358ef8f38" data-d2-id="o_387afba2690b52648862">4-week-old, well and feeding well, direct bilirubin 5, acholic stools, urine reducing substances negative &rarr; <b>Abdominal ultrasound and HIDA scan</b> &rarr; biliary atresia, with Kasai before about 60 days</li>
<li data-src="authored" data-type="next" data-d1="Switch to soy-based formula" data-d2="Empiric antibiotics and observation" data-item-id="q_e4a690479dda54b594c8" data-item-version="1" data-item-status="ready" data-key-id="o_05bce670d02353db84e0" data-d1-id="o_c99920f7d31a5d9ab17d" data-d2-id="o_a7b550f3fd435d06963c">5-day-old with poor feeding, lethargy, seizures and urine that smells like maple syrup, newborn screen positive &rarr; <b>Protein-free feeds with intravenous dextrose</b> &rarr; maple syrup urine disease</li>
<li data-src="authored" data-type="avoid" data-d1="Soy-based formula" data-d2="Elemental lactose-free formula" data-item-id="q_ca8409261f4b50c7a726" data-item-version="1" data-item-status="ready" data-key-id="o_7f1087a915175981b746" data-d1-id="o_13f24a3a30b4596ea825" data-d2-id="o_ce4dd77cd52753758a3c">2-week-old with confirmed galactosemia whose parents ask what to feed &rarr; <b>Breast milk</b> &rarr; soy-based formula is the substitute</li>
<li data-type="dx" data-d1="Galactosemia" data-d2="Hereditary fructose intolerance" data-item-id="q_e7c9671a218657638e7a" data-item-version="1" data-item-status="ready" data-key-id="o_8b22f3f41fda533dbb7c" data-d1-id="o_6bd9f2df50d8522eb5c0" data-d2-id="o_42e0e840c4b751e6adae">3-month-old with massive hepatomegaly, fasting hypoglycemia after a 4-hour fast, lactic acidosis, hypertriglyceridemia, doll-like facies &rarr; <b>Glycogen storage disease type I</b> &rarr; frequent cornstarch feeds</li>
<li data-type="dx" data-d1="Glycogen storage disease type I" data-d2="Hereditary fructose intolerance" data-item-id="q_1a901ce6589a5e3e9bba" data-item-version="1" data-item-status="ready" data-key-id="o_a696e77da77b51a5abbf" data-d1-id="o_a070cda862b05f36bfce" data-d2-id="o_1649c43f3cbf5977acdc">10-day-old with vomiting after starting formula, jaundice, hepatomegaly, cataracts, urine positive for reducing substances &rarr; <b>Classic galactosemia</b> &rarr; eliminate galactose and lactose from diet</li>
<li data-type="mech" data-src="uworld" data-nid="1474165315038 1484603517328 1516557603865 1539168087031 1539459932653" data-d1="Maternal nonadherence to recommended vaccines" data-d2="Advanced maternal age at conception" data-item-id="q_8a7f604f6bbb7a70dfe4" data-item-version="1" data-item-status="ready" data-key-id="o_c0d7c7cff78da0d6fe57" data-d1-id="o_1f2717562b32e2292504" data-d2-id="o_be1d5ce6c64a9ca632a7" data-lead-in="Which of the following is the most likely underlying cause of this patient&#x27;s condition?">9-day-old girl, exclusively breastfed, with 3 days of vomiting and poor feeding; jaundiced, liver edge 4 cm below the costal margin, bilateral cataracts on red reflex exam; passed her newborn hearing screen, no murmur; blood culture grows Escherichia coli; her mother is 39 and declined most recommended vaccines &rarr; <b>Inability to metabolize galactose in breast milk</b> &rarr; classic galactosemia (GALT deficiency): stop breast milk and start soy formula without waiting for confirmation</li>
<li data-type="dx" data-src="authored" data-d1="Classic galactosemia" data-d2="Maple syrup urine disease" data-item-id="q_3d56f5bcb0b7bbc18243" data-item-version="1" data-item-status="ready" data-key-id="o_b4766e47e53458290141" data-d1-id="o_2a77f0612c43dd06bee8" data-d2-id="o_a8b942963131b779ee57">3-day-old boy, formula-fed, with increasing lethargy, vomiting and rapid breathing; no jaundice, no hepatomegaly, clear lenses; glucose normal; arterial pH 7.50 with low PCO2; plasma ammonia markedly elevated; urine reducing substances negative &rarr; <b>Urea cycle disorder</b> &rarr; hyperammonemia with respiratory alkalosis; stop protein and lower the ammonia</li>
<li data-type="claim" data-src="authored" data-d1="Normal development and fertility are expected if the diet is strict" data-d2="Progressive cirrhosis is expected even if the diet is strict" data-item-id="q_a1c8d07e176b4cce3dd8" data-item-version="1" data-item-status="ready" data-key-id="o_e2e31924d8c9f8a2b873" data-d1-id="o_504d47c2ff0fcde27124" data-d2-id="o_7504275a079dbf571c27" data-lead-in="Which of the following is most accurate about her long-term outcome?">Parents of a girl with classic galactosemia, found on newborn screening and fed soy formula since day 5, ask about her long-term outlook &rarr; <b>Speech and learning problems and ovarian insufficiency can occur despite the diet</b> &rarr; the diet reverses the acute liver, sepsis and cataract illness but does not prevent these late complications</li>
</ol>
<div class="pearls"><span class="lbl">Exam answer versus current evidence</span> The exam keys <b>60 days</b> as the Kasai window, and that is the number to pick. The evidence underneath it is not a cliff &mdash; native-liver survival falls continuously with age at operation, and a 2023 meta-analysis found operating at <b>30 days or earlier</b> still beat 31&ndash;60 days. Read 60 days as the keyed threshold, not as a deadline with room to spare.</div>
<div class="danger"><span class="lbl">Immediate management</span> <b>Stop all lactose and galactose immediately</b> — breast milk and standard formula give way to soy-based formula — <b>without waiting for confirmation</b>, because the injury is ongoing. In parallel, <b>send blood and urine cultures and start empiric neonatal antibiotics</b> &#9888; for Escherichia coli. Confirm afterwards with red cell GALT activity. A negative urine reducing substance test in an infant who has stopped feeding excludes nothing &#9888;, because the test needs recent galactose intake.</div>
<div class="pearls"><span class="lbl">Pearls</span> Classic galactosemia is GALT deficiency affecting liver, kidney, brain and lens with a predisposition to Escherichia coli sepsis &middot; The pathway: galactokinase (GALK) makes galactose-1-phosphate, and GALT converts it to UDP-galactose and glucose-1-phosphate. A <b>GALK</b> block leaves only galactitol, so <b>cataracts alone</b>; a <b>GALT</b> block traps toxic galactose-1-phosphate, so the <b>whole sick-neonate picture</b> &middot; Reducing substances positive with dipstick glucose negative means galactose or fructose, because glucose is itself a reducing sugar, so read both tests &middot; Cataracts in both galactose disorders come from galactitol via aldose reductase, the same enzyme that makes sorbitol in the diabetic lens &middot; Hereditary fructose intolerance is the diet-shifted twin with the same hepatic picture plus hypoglycemia, appearing at weaning &middot; Direct hyperbilirubinemia in a <b>well</b> infant with acholic stools is biliary atresia, and the Kasai clock runs to about 60 days &#9888; &middot; Even with an early, strict diet, children can have <b>cognitive deficits</b> and <b>speech problems</b> (verbal dyspraxia), and girls develop <b>primary ovarian insufficiency</b>; the diet reverses the acute illness but does not prevent these</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Cholestasis &amp; the LFT Patterns</b> covers the conjugated-versus-unconjugated approach in adults; this brief covers the neonate. Related conditions without their own brief: <b>hereditary fructose intolerance</b> (ask: did symptoms start with fruit or sucrose?) and <b>biliary atresia</b> (ask: is the infant sick or well, and are reducing substances present?). Part I <b>Congenital Hypothyroidism</b> is another positive newborn screen: there the TSH level and the neck locate the defect; here the enzyme deficiency and the organism do.</div>
<div class="rule"><span class="lbl">Transferable rule</span> A positive newborn screen never names the disease because every option is on the panel, so the bilirubin fraction, the liver and the urine do the naming, and a febrile neonate is cultured and treated for sepsis in parallel with the metabolic answer rather than after it.</div>
<div class="traps"><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Maple syrup urine disease is the right class of screen-flagged inborn error but has no hepatomegaly and carries ketoacids rather than a reducing sugar.</span></div><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">The positive screen sells cystic fibrosis, whose neonatal face is meconium ileus rather than fever with urinary sugar.</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Sickle cell causes jaundice, but unconjugated and not at 10 days, because fetal hemoglobin protects the neonate.</span></div></div>
</div>
```
