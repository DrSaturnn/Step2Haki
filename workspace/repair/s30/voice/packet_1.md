# Voice packet 1 of 5 (s30, gi): liver-preg, masld, neonatal-bowel, bs-wilson

**Instructions.** Everything you need is in this packet. Do not open index.html, the skill files or other packets. Write your edits to `repair/s30/04_voice_1.json`, run `python3 tools/verify_edits.py repair/s30/04_voice_1.json scratch/s30_base.html --voice` from the workspace folder (Step2Haki/workspace) and loop until it prints PASS (add `--report` to read your own claim map). Then reply with the 3 to 5 line report the rules ask for, including any acronym you skipped.

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
### `liver-preg`: Liver Disease in Pregnancy

```html
<div class="brief" id="liver-preg" data-shelf="fm" data-bp="preg gi">
<h4>Liver Disease in Pregnancy</h4>
<p class="sub">Abnormal liver tests in pregnancy: check the trimester first</p>
<div class="dp"><span class="lbl">The decision point</span>
<p><b>Acute fatty liver of pregnancy, intrahepatic cholestasis, and preeclampsia/HELLP are all third-trimester diseases.</b> A patient at 14 weeks with elevated transaminases, obesity, and diabetes has metabolic liver disease unrelated to pregnancy.</p></div>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>AST, ALT, bilirubin and alkaline phosphatase</td><td>First</td><td>Alkaline phosphatase raised <b>alone</b>, all else normal</td><td>Placental isoenzyme: physiologic, reassure</td></tr>
<tr><td>Serum bile acids</td><td>Confirms</td><td><b>Raised</b> bile acids with itching of palms and soles</td><td>Intrahepatic cholestasis: ursodeoxycholic acid, deliver at 36 to 37 weeks</td></tr>
<tr><td>Blood pressure, urine protein, CBC with smear</td><td>Confirms</td><td><b>Schistocytes</b>, low platelets, raised LFTs, hypertension</td><td>HELLP syndrome: delivery</td></tr>
<tr><td>Glucose, PT/INR, ammonia and creatinine</td><td>By branch</td><td><b>Hypoglycemia</b> with coagulopathy and a rising creatinine</td><td>Acute fatty liver of pregnancy: emergent delivery</td></tr>
<tr><td>Hepatitis serologies and liver ultrasound</td><td>By branch</td><td>Raised ALT before 20 weeks, <b>echogenic</b> liver</td><td>Not pregnancy-specific: MASLD or viral hepatitis</td></tr>
<tr><td>Right upper quadrant ultrasound or bile acids</td><td>Skip</td><td>Adds nothing when AST, ALT and bilirubin are <b>normal</b></td><td>Isolated alkaline phosphatase in late pregnancy needs no workup</td></tr>
</tbody>
</table>
</div>
<div class="pearls"><span class="lbl">Mnemonic</span> <b>HELLP</b> &mdash; Hemolysis, Elevated Liver enzymes, Low Platelets</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="dx" data-d1="Acute fatty liver of pregnancy" data-d2="HELLP syndrome" data-item-id="q_e1ccff8f303e5636b6a5" data-item-version="1" data-item-status="ready" data-key-id="o_bb7d4e6e8d785d38891f" data-d1-id="o_a83720e1c0a255be80f2" data-d2-id="o_456ed239fbc55ae5b4da">26 yo F at 34 weeks with intense palmar pruritus, raised bile acids and no rash → <b>Intrahepatic cholestasis of pregnancy</b> → ursodeoxycholic acid</li>
<li data-type="dx" data-d1="Intrahepatic cholestasis of pregnancy" data-d2="Viral hepatitis" data-item-id="q_83f5141cfeae5d76af0a" data-item-version="1" data-item-status="ready" data-key-id="o_251ab3b4d82c5ffeac03" data-d1-id="o_2813d8259ef3557ab3e3" data-d2-id="o_c16bcf18ee31585a915a">26 yo F at 36 weeks with hypoglycemia, coagulopathy and raised transaminases → <b>Acute fatty liver of pregnancy</b> → urgent delivery</li>
<li data-type="dx" data-d1="Acute fatty liver of pregnancy" data-d2="Intrahepatic cholestasis of pregnancy" data-item-id="q_0e57849cad4252558d04" data-item-version="1" data-item-status="ready" data-key-id="o_a80515703ec85b8eabb3" data-d1-id="o_e2cf0d4cdbd65ee8b694" data-d2-id="o_ba7e1d134cc1568dbda4">26 yo F at 34 weeks with hypertension, hemolysis, high LFTs and platelets 68,000 → <b>HELLP syndrome</b> → delivery</li>
<li data-type="dx" data-d1="Acute fatty liver of pregnancy" data-d2="Viral hepatitis" data-item-id="q_3e9be3a0d32e541a9c68" data-item-version="1" data-item-status="ready" data-key-id="o_fc759daeceb75f9988e1" data-d1-id="o_bbc6008cb717568e94db" data-d2-id="o_4896fcacab47518fb3ce">26 yo F at 9 weeks with intractable vomiting, ketonuria and mildly raised transaminases → <b>Hyperemesis gravidarum</b></li>
<li data-type="dx" data-d1="HELLP syndrome" data-d2="Viral hepatitis" data-item-id="q_a8d68b30e3e85f3ab083" data-item-version="1" data-item-status="ready" data-key-id="o_7f250bfcf6765ea5b010" data-d1-id="o_e8fc88cedc645733a3c9" data-d2-id="o_65bcbddd02ae5b5093a3">26 yo F at 14 weeks, obese with diabetes and raised transaminases → <b>Metabolic dysfunction-associated steatotic liver disease &mdash; the third-trimester diseases do not fit at 14 weeks</b></li>
<li data-type="dx" data-d1="Cholestasis of pregnancy" data-d2="Biliary obstruction" data-item-id="q_fcddaf4001b1573b88cd" data-item-version="1" data-item-status="ready" data-key-id="o_d4e9f0e9d5ef55f79dcd" data-d1-id="o_a68125ff02f85df7b8f6" data-d2-id="o_ea7f18a6295a5b53b88c">26 yo F at 30 weeks with an isolated alkaline phosphatase twice normal, all else normal → <b>Placental alkaline phosphatase — physiologic</b> → reassurance</li>
<li data-type="next" data-src="authored" data-d1="Delivery at 40 weeks" data-d2="Immediate delivery" data-item-id="q_4f3bf9b16803b327984d" data-item-version="1" data-item-status="ready" data-key-id="o_e0df7c71fcbe9173f7cd" data-d1-id="o_fb310e46a9fee043e704" data-d2-id="o_9cd229813d123a8a91bf">26 yo F at 34 weeks with intractable palmar pruritus and raised bile acids, taking ursodeoxycholic acid &rarr; <b>Delivery at 36 to 37 weeks</b> &rarr; intrahepatic cholestasis carries stillbirth risk</li>
<li data-type="next" data-src="authored" data-d1="Ursodeoxycholic acid" data-d2="Magnesium sulfate and expectant management" data-item-id="q_23614287ba85d6b63f1c" data-item-version="1" data-item-status="ready" data-key-id="o_d6f9ae3170361147866a" data-d1-id="o_e03f0358ddfb1d422733" data-d2-id="o_78bd24c31e16b66205f5">29 yo F at 35 weeks with hypoglycemia, coagulopathy, raised ammonia and rising creatinine &rarr; <b>Emergent delivery</b> &rarr; acute fatty liver of pregnancy is treated by delivering</li>
<li data-type="next" data-src="authored" data-d1="Right upper quadrant ultrasound" data-d2="Serum bile acids" data-item-id="q_40767d0c5b70b9ce7b5a" data-item-version="1" data-item-status="ready" data-key-id="o_6ca214264e2fcc000548" data-d1-id="o_aa3b61ed91e393b8bd63" data-d2-id="o_8bbd5fb3ab0dc3e3abab">28 yo F at 32 weeks with alkaline phosphatase three times normal on routine labs; AST, ALT and bilirubin normal; no symptoms &rarr; <b>Reassurance</b> &rarr; the placenta makes alkaline phosphatase</li>
</ol>
<div class="danger"><span class="lbl">Alkaline phosphatase in pregnancy</span>
<b>Alkaline phosphatase is supposed to be elevated in pregnancy</b>: the placenta makes its own isoenzyme, and levels run 2–4× normal. <b>AST, ALT, and bilirubin do NOT rise physiologically</b>; any elevation is pathologic.</div>
<table data-mask="none"><caption>Liver labs in normal pregnancy</caption>
<thead><tr><th>Rises physiologically</th><th>Falls physiologically</th><th>Should stay normal</th></tr></thead>
<tbody>
<tr><td><b>Alkaline phosphatase</b> (placental), WBC (to ~15,000), ESR, fibrinogen and factors VII/VIII/X, total T4 and TBG, cholesterol, GFR</td><td>Hemoglobin (dilutional), platelets (mild gestational), <b>creatinine and BUN</b>, PaCO₂, TSH in the first trimester</td><td><b>AST, ALT, bilirubin</b></td></tr>
</tbody>
</table>
<table><caption>Liver disease in pregnancy — by trimester</caption>
<thead><tr><th>Condition</th><th>Timing</th><th>The tell</th><th>Management</th></tr></thead>
<tbody>
<tr><td>Hyperemesis gravidarum</td><td><b>1st</b></td><td>Vomiting, ketonuria, &gt;5% weight loss</td><td>Supportive</td></tr>
<tr><td>Intrahepatic cholestasis</td><td>2nd–<b>3rd</b></td><td><b>Pruritus of palms and soles, worse at night</b>; ↑bile acids, ↑bilirubin; <b>stillbirth risk</b></td><td>Ursodeoxycholic acid; deliver 36–37 wk</td></tr>
<tr><td>Preeclampsia / HELLP <span class="tag t-em">Emergency</span></td><td>&gt;20 wk</td><td>HTN + proteinuria; <b>Hemolysis, Elevated LFTs, Low Platelets</b>, RUQ pain, schistocytes</td><td>Delivery</td></tr>
<tr><td>Acute fatty liver <span class="tag t-em">Emergency</span></td><td><b>3rd</b></td><td><b>Hypoglycemia</b>, ↑ammonia, coagulopathy, ↑Cr, encephalopathy; <b>LCHAD deficiency</b> link</td><td><b>Emergent delivery</b></td></tr>
</tbody>
</table>
<div class="pearls"><span class="lbl">AFLP vs. HELLP</span> <b>Hypoglycemia + coagulopathy + high ammonia + renal failure = AFLP.</b> <b>Hemolysis + thrombocytopenia + more hypertension = HELLP.</b> Both are treated by delivering. Cholecystectomy in pregnancy is safest in the <b>second trimester</b>.</div>
<div class="rule"><span class="lbl">Transferable rule</span> Before diagnosing a pregnancy-specific liver disease, check that the gestational age fits it.</div>
<div class="traps"><span class="pill p-salient">Salient decoy</span></div>
</div>
```

### `masld`: MASLD / Metabolic Fatty Liver

```html
<div class="brief" id="masld" data-shelf="fm" data-bp="gi">
<h4>MASLD / Metabolic Fatty Liver</h4>
<p class="sub">Formerly NAFLD · a diagnosis of exclusion</p>
<div class="dp"><span class="lbl">The decision point</span>
<p>Metabolic syndrome (obesity, T2DM, hypertension, dyslipidemia) + transaminase elevation with <b>AST/ALT ratio &lt;1</b> + <b>hyperechoic liver</b> on ultrasound. Alcohol gives the opposite ratio: <b>AST:ALT ≥2</b> ("t-<b>oAST</b>").</p></div>
<ul class="plain">
<li>Most common chronic liver disease in the US; progression is <b>steatosis → MASH → fibrosis → cirrhosis → HCC</b>, and HCC can occur <i>without</i> cirrhosis</li>
<li><b>Exclude first:</b> alcohol, hepatitis B/C, hemochromatosis, Wilson disease, autoimmune hepatitis, α1-antitrypsin deficiency, and drugs (steroids, amiodarone, methotrexate, tamoxifen)</li>
<li><b>Stage fibrosis</b> with FIB-4 or transient elastography</li>
<li><b>Treatment:</b> 7–10% weight loss reverses steatohepatitis; bariatric surgery if BMI ≥35; GLP-1 agonists; resmetirom for MASH with fibrosis</li>
</ul>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>AST and ALT</td><td>First</td><td>ALT higher, AST:ALT <b>under 1</b></td><td>Metabolic; a ratio of 2 or more points to alcohol</td></tr>
<tr><td>Liver ultrasound</td><td>First</td><td><b>Hyperechoic</b> liver</td><td>Steatosis</td></tr>
<tr><td>Hepatitis B and C serology, iron studies, ceruloplasmin</td><td>Confirms</td><td>All <b>normal</b>, alcohol under the threshold</td><td>MASLD is a diagnosis of exclusion; also exclude autoimmune hepatitis, alpha-1 antitrypsin deficiency, drugs</td></tr>
<tr><td>FIB-4 score</td><td>Staging</td><td><b>High</b> score</td><td>Possible advanced fibrosis: elastography next</td></tr>
<tr><td>Transient elastography</td><td>Staging</td><td><b>Stiff</b> liver</td><td>Advanced fibrosis or cirrhosis: hepatology, HCC surveillance if cirrhotic</td></tr>
<tr><td>Liver biopsy in every patient</td><td>Skip</td><td>Invasive; <b>noninvasive</b> staging comes first</td><td>Reserved for an uncertain diagnosis or discordant staging</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="dx" data-d1="Alcohol-associated liver disease" data-d2="Chronic hepatitis C" data-item-id="q_00672fcf96b85d359dc8" data-item-version="1" data-item-status="ready" data-key-id="o_6aeab74bc2125e459c31" data-d1-id="o_5068512cd1bb5b2ea8bc" data-d2-id="o_3f5888aaf97059a0ae7e">48 yo M, BMI 34, type 2 diabetes, ALT 70, AST 45, hyperechoic liver → <b>MASLD</b></li>
<li data-type="dx" data-d1="MASLD" data-d2="Autoimmune hepatitis" data-item-id="q_214f0143b1975c59bff3" data-item-version="1" data-item-status="ready" data-key-id="o_5ab30ae067705040a82f" data-d1-id="o_0b350fe66d795f41aa13" data-d2-id="o_d3b254ec30ae5719a223">48 yo M with AST 180 and ALT 70 and a history of heavy drinking → <b>Alcohol-associated liver disease</b> → AST:ALT of 2 or more</li>
<li data-type="next" data-d1="Ursodeoxycholic acid" data-d2="A statin" data-item-id="q_061d44e9127d5db78459" data-item-version="1" data-item-status="ready" data-key-id="o_d731ab4972cf59b6900e" data-d1-id="o_91ad7a3d7dbd5e769303" data-d2-id="o_ef84c93619f15e859fc5">48 yo M with MASLD asking what most improves liver histology → <b>7 To 10% weight loss</b></li>
<li data-type="next" data-d1="Reassure and recheck in a year" data-d2="Liver biopsy in every patient" data-item-id="q_26e432f48bf954a6b498" data-item-version="1" data-item-status="ready" data-key-id="o_59906eb9bd8455fc9344" data-d1-id="o_a211f8b30b715d15ad61" data-d2-id="o_8773a2a458755b869366">48 yo M with MASLD and a high FIB-4 score → <b>Assess fibrosis with elastography</b></li>
<li data-type="claim" data-d1="Statins are contraindicated in fatty liver" data-d2="Withhold until the ALT normalizes" data-item-id="q_27b2e47562d45b9a8d57" data-item-version="1" data-item-status="ready" data-key-id="o_9119020c54ad5a278fb4" data-d1-id="o_a4c54fa44b745fb3948b" data-d2-id="o_0faddfe6eb915bc9acf3">48 yo M with MASLD and LDL 160 → <b>Statins are safe and indicated</b></li>
<li data-type="dx" data-d1="MASLD" data-d2="Hereditary hemochromatosis" data-item-id="q_c1178edc75ea5acfabf3" data-item-version="1" data-item-status="ready" data-key-id="o_7349610cbe625e40b3dd" data-d1-id="o_9a2d0de9e061526c9384" data-d2-id="o_8ed6f2f564aa547ca941">32 yo M with fatty liver, low ceruloplasmin and Kayser-Fleischer rings → <b>Wilson disease</b></li>
</ol>
<div class="pearls"><span class="lbl">Pearls</span> Significant alcohol intake threshold: &gt;21 drinks/week (men), &gt;14 (women) · gallstones in pregnancy are common (progesterone → gallbladder stasis) and usually <b>incidental</b> without wall thickening, fever, or pain · young patient with steatosis + tremor + <b>Kayser-Fleischer rings</b> → Wilson disease.</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part II <b>Wilson Disease: Copper in the Liver, Brain and Eye</b> covers the copper exclusion: is the patient under about 40, with a tremor, psychiatric change or Kayser-Fleischer rings, and is the ceruloplasmin low?</div>
</div>
```

### `neonatal-bowel`: The Distended Abdomen in a Newborn or Infant

```html
<div class="brief" id="neonatal-bowel" data-shelf="peds" data-nid="1473707579754 1482959865798 1512666375038 1539170612657 1569107827657 1581257194958 1482886567135 1482886572434 1482886584577 1520188762940 1482959868268 1512666496684 1581520331589 1482959873096 1539170479420 1556448809081" data-bp="newborn gi">
<h4>The Distended Abdomen in a Newborn or Infant</h4>
<p class="sub">Bilious emesis, bloody stool &middot; the film tells you which one</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 7-day-old term F with <b>truncus arteriosus</b> in the NICU awaiting repair, poor feeding and abdominal distension; <b>T 35 C</b>, BP 60/30, pulse 180, respirations 65, saturation 82% &middot; <b>Exam</b> &mdash; lethargic and cyanotic, moderate distension, <b>absent bowel sounds</b>, <b>bright red blood in stool</b>; nasogastric tube returns bilious fluid &middot; <b>Imaging</b> &mdash; abdominal x-ray &middot; <b>Q</b> &mdash; the most likely diagnosis; options spanned NEC, malrotation with volvulus, intussusception, milk protein proctocolitis and C difficile colitis</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>The combination of <b>temperature instability</b>, <b>abdominal distension with bloody stools</b>, and <b>pneumatosis intestinalis</b> on the film indicates necrotizing enterocolitis. NEC is mainly a disease of prematurity, but this infant is term. In a term infant, <b>cyanotic congenital heart disease and hypotension reduce mesenteric oxygen delivery</b> and cause the same ischemic bowel injury.</p>
<p>The bilious return also fits volvulus, so rule it out deliberately. Volvulus gives <b>abrupt</b> vomiting in a previously well infant, with <b>proximal gas and a gasless distal abdomen</b>. NEC gives air <b>in the bowel wall</b> with gas still visible in the large bowel. Read the gas pattern first; if malrotation is still possible, only an upper GI series excludes it.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Pneumatosis intestinalis</b> &mdash; air within the bowel wall; highly specific for NEC, often with <b>portal venous gas</b> (branching lucencies over the liver) &middot; <b>Pneumoperitoneum</b> &mdash; free air under the diaphragm; means perforation and an operation &middot; <b>NEC risk factors</b> &mdash; <b>prematurity</b> (the most important), very low birth weight under 1.5 kg, enteral feeding (especially <b>formula</b>), prolonged antibiotics, and in term infants a hypoxic-ischemic insult such as cyanotic heart disease, hypotension or perinatal asphyxia &middot; <b>Volvulus film</b> &mdash; proximal gaseous distension with a gasless distal abdomen &middot; <b>Intussusception age</b> &mdash; 6 months to 3 years</div>
<table>
<caption>The distended abdomen in a newborn or infant: the differential<span class="cap-sub">timing, the stool, and the gas pattern</span></caption>
<thead><tr><th>Diagnosis</th><th>The picture</th><th>Key discriminator</th><th>What to do</th></tr></thead>
<tbody>
<tr><td><b>Necrotizing enterocolitis</b> <span class="tag t-em">Emergency</span></td><td>Preterm infant on enteral feeds; lethargy, apnea, <b>hypothermia</b> rather than fever, distension, feeding intolerance, bilious emesis, bloody stools (may be absent early); leukocytosis, metabolic acidosis</td><td><b>Pneumatosis intestinalis</b> with or without <b>portal venous gas</b>; gas still present distally</td><td>NPO, NG decompression, parenteral nutrition, broad-spectrum antibiotics now; surgery for perforation or worsening despite medical care</td></tr>
<tr><td><b>Malrotation with midgut volvulus</b> <span class="tag t-em">Emergency</span></td><td>Previously well, then abrupt bilious vomiting and pain; <b>any age</b>, most often the first month; older children can have intermittent pain and vomiting instead</td><td><b>Proximal gas, gasless distal abdomen</b>; upper GI series shows the <b>ligament of Treitz on the right</b> and a corkscrew or bird's-beak duodenum</td><td>Upper GI series if stable; emergency laparotomy if not; the operation is the <b>Ladd procedure</b></td></tr>
<tr><td>Duodenal atresia</td><td>Bilious vomiting in the first 1 to 2 days, polyhydramnios, trisomy 21; abdomen <b>not distended</b></td><td><b>Double bubble with no distal gas</b>, present from birth rather than abrupt</td><td>Stop feeds, NG decompression, echocardiogram, then surgical repair</td></tr>
<tr><td>Hirschsprung disease</td><td>No meconium by 48 hours, poor feeding, distension, bilious vomiting; <b>failed neural crest migration</b> leaves an aganglionic segment, usually <b>rectosigmoid</b>, that cannot relax and stays contracted; usually isolated, but associated with <b>Down syndrome</b></td><td><b>Normal meconium</b> once it passes; tight rectum with an explosive <b>squirt</b> of stool and gas on rectal exam; enema shows a rectosigmoid transition zone with dilated proximal colon; a newborn under 48 hours is not yet late</td><td>Contrast enema, then rectal suction biopsy (absent ganglion cells confirms); surgical <b>resection of the aganglionic segment</b></td></tr>
<tr><td>Meconium ileus</td><td>No meconium, distension, ± bilious vomiting; <b>thick, sticky meconium</b> obstructs the terminal ileum; <b>cystic fibrosis in about 90%</b></td><td><b>Dilated small bowel</b> with little colonic gas; contrast enema shows a <b>microcolon</b>; empty rectum, no squirt; not a Down syndrome association</td><td>Hyperosmolar contrast enema, which can also relieve it; surgery if it fails or for free air; <b>sweat chloride test</b></td></tr>
<tr><td>Intussusception</td><td>Colicky pain, currant-jelly stool, right upper quadrant mass</td><td><b>Age 6 months to 3 years</b>; target sign on ultrasound</td><td>Air-contrast enema</td></tr>
<tr><td>Milk protein-induced proctocolitis</td><td>Blood-streaked stools at 2 to 8 weeks</td><td><b>The infant is well</b> &mdash; thriving, undistended, normal vitals</td><td>Maternal dairy elimination or hydrolyzed formula</td></tr>
<tr><td><i>Clostridioides difficile</i> colitis</td><td>Distension with watery, sometimes bloody stool</td><td>Neonates are colonized but <b>lack the toxin receptors</b></td><td>Not a neonatal diagnosis</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody class="grp">
<tr><td>Abdominal radiograph</td><td>First</td><td><b>Pneumatosis intestinalis</b> with or without <b>portal venous gas</b>, distal gas present</td><td>NEC: NPO, decompression, broad-spectrum antibiotics</td></tr>
<tr><td></td><td></td><td>Proximal gas, <b>gasless</b> distal abdomen</td><td>Volvulus: upper GI series if stable, laparotomy if not</td></tr>
<tr><td></td><td></td><td><b>Double bubble</b>, no distal gas</td><td>Duodenal atresia: NG decompression and surgical repair</td></tr>
<tr><td></td><td></td><td>Diffusely <b>dilated loops</b>, distended abdomen, <b>no air in the rectum</b>, no free air</td><td>Distal obstruction: Hirschsprung disease or meconium ileus</td></tr>
<tr><td></td><td></td><td><b>Free air</b> under the diaphragm</td><td>Perforation: laparotomy</td></tr>
</tbody>
<tbody>
<tr><td>Echocardiogram</td><td>By branch</td><td>Duodenal atresia with <b>trisomy 21</b> features</td><td>About half of infants with Down syndrome have heart disease (VSD, ASD, AV canal); obtain before surgery, murmur or not</td></tr>
<tr><td>Karyotype</td><td>Confirms</td><td><b>Trisomy 21</b></td><td>Confirms Down syndrome but is not urgent and does not change the operation</td></tr>
<tr><td>Upper GI series after a diagnostic double bubble</td><td>Skip</td><td>Film already <b>diagnostic</b></td><td>Upper GI is for malrotation, which has distal gas</td></tr>
<tr><td>Contrast enema, then rectal suction biopsy</td><td>By branch</td><td><b>Transition zone</b>; absent ganglion cells</td><td>Hirschsprung disease: no meconium by 48 hours with distension</td></tr>
<tr><td>Contrast enema, then sweat chloride test</td><td>By branch</td><td><b>Microcolon</b> with inspissated meconium in the terminal ileum</td><td>Meconium ileus: a hyperosmolar enema can relieve it; about 90% have cystic fibrosis</td></tr>
<tr><td>CBC, blood gas and blood culture</td><td>By branch</td><td>Leukocytosis, <b>thrombocytopenia</b>, metabolic acidosis</td><td>NEC: the platelet fall tracks severity; a rising count is often the first sign of improvement</td></tr>
<tr><td>Upper GI contrast series</td><td>Confirms</td><td><b>Ligament of Treitz on the right</b>; corkscrew or bird's-beak duodenum</td><td>Malrotation with midgut volvulus: Ladd procedure; skip it and operate if the infant is unstable</td></tr>
<tr><td>Abdominal ultrasound</td><td>By branch</td><td><b>Target</b> sign</td><td>Intussusception at 6 months to 3 years: air-contrast enema</td></tr>
<tr><td>C difficile toxin testing</td><td>Skip</td><td>Neonates <b>lack</b> the toxin receptors</td><td>Not a neonatal diagnosis</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="dx" data-d1="Malrotation with midgut volvulus" data-d2="Milk protein-induced proctocolitis" data-src="uworld" data-item-id="q_b9679e912ef5b77332a3" data-item-version="1" data-item-status="ready" data-key-id="o_c26c584c6bd84036761d" data-d1-id="o_6793962ac0eb18cccf9d" data-d2-id="o_e3a1ba1f870682b10391">7 day old term F with truncus arteriosus awaiting repair, temperature 35 C, lethargy, distended abdomen with absent bowel sounds, bilious nasogastric return and bright red blood per rectum &rarr; <b>Necrotizing enterocolitis</b> &rarr; Cyanotic heart disease is a term-infant risk factor &mdash; mesenteric hypoperfusion</li>
<li data-type="test" data-d1="Proximal gas with a gasless distal abdomen" data-d2="Double bubble with no distal gas" data-src="uworld" data-item-id="q_66f2cab70c716e8d7b41" data-item-version="2" data-item-status="ready" data-key-id="o_a8459779edb4b3b1d999" data-d1-id="o_2ccb4ae730f3e6034d41" data-d2-id="o_db92a6a694974d6d2f13" data-lead-in="Which of the following findings on abdominal radiograph is most likely?">Preterm neonate on enteral feeds with abdominal distension and bloody stools &rarr; <b>Pneumatosis intestinalis</b> &rarr; Air within the bowel wall &mdash; specific for NEC; portal venous gas may accompany it</li>
<li data-type="next" data-d1="Upper gastrointestinal contrast series" data-d2="Immediate laparotomy" data-src="uworld" data-item-id="q_99429574aee90427366f" data-item-version="1" data-item-status="ready" data-key-id="o_300c258bd0cd4576eb4d" data-d1-id="o_b5dc245776e6fe4870e3" data-d2-id="o_acb433f9aca7ce3857ba">Neonate with pneumatosis, distension and bloody stools, hemodynamically stable &rarr; <b>Bowel rest, decompression and broad-spectrum antibiotics</b> &rarr; Antibiotics immediately &mdash; septic shock is the lethal endpoint</li>
<li data-type="next" data-d1="Continue antibiotics and repeat the film" data-d2="Air-contrast enema reduction" data-src="uworld" data-item-id="q_f272b0f9ca5bc10bb8b9" data-item-version="1" data-item-status="ready" data-key-id="o_728626c12f8c686d87c3" data-d1-id="o_f92dc086be3be0026c34" data-d2-id="o_782694a1205d7522b08d">Neonate with NEC whose film now shows free air beneath the diaphragm &rarr; <b>Laparotomy</b> &rarr; Pneumoperitoneum means perforation</li>
<li data-type="dx" data-d1="Necrotizing enterocolitis" data-d2="Duodenal atresia" data-src="uworld" data-item-id="q_46f7f9b34fc43ff20397" data-item-version="1" data-item-status="ready" data-key-id="o_1004be167e650b96740a" data-d1-id="o_ecb7d583abbac2f4075c" data-d2-id="o_858c1ca8a072dcf0d65f">3 day old, well until now, abrupt bilious vomiting, abdominal pain and shock; film shows proximal gas and a gasless distal abdomen &rarr; <b>Malrotation with midgut volvulus</b> &rarr; Abrupt, previously well, and the mesenteric root twists around the superior mesenteric artery</li>
<li data-type="test" data-d1="Air-contrast enema" data-d2="Abdominal ultrasonography" data-src="uworld" data-item-id="q_00d8edb1b8a926a390cf" data-item-version="2" data-item-status="ready" data-key-id="o_5dd6ad7b0fec91979f5a" data-d1-id="o_a63da1f813ff137f0f43" data-d2-id="o_64b984e5bf16c87f36a1" data-lead-in="Which of the following is most likely to confirm the diagnosis?">Stable infant with suspected malrotation &rarr; <b>Upper gastrointestinal contrast series</b> &rarr; Outlines the duodenojejunal junction and any corkscrew</li>
<li data-type="dx" data-d1="Midgut volvulus" data-d2="Hirschsprung disease" data-src="uworld" data-item-id="q_861520f8284d83797da3" data-item-version="1" data-item-status="ready" data-key-id="o_3451785c6f6dcd275229" data-d1-id="o_b8c004943c326cce3d23" data-d2-id="o_703cad75a5924b45e036">Newborn with bilious emesis from the first feeds, polyhydramnios in utero, trisomy 21 features, no distal gas on film &rarr; <b>Duodenal atresia</b> &rarr; Present from birth rather than abrupt &mdash; failure of recanalization</li>
<li data-type="dx" data-d1="Necrotizing enterocolitis" data-d2="Meckel diverticulum" data-src="uworld" data-item-id="q_5b8630c94ea7399496e3" data-item-version="1" data-item-status="ready" data-key-id="o_e1435f469be1a32cdf5d" data-d1-id="o_d71285ab6047ba37e274" data-d2-id="o_517eff63f6282c1fdf71">9 month old with intermittent colicky pain, currant-jelly stool and a right upper quadrant mass &rarr; <b>Intussusception</b> &rarr; Age 6 months to 3 years, target sign on ultrasound</li>
<li data-type="dx" data-d1="Necrotizing enterocolitis" data-d2="Anal fissure" data-src="uworld" data-item-id="q_84502b624963f20391d6" data-item-version="1" data-item-status="ready" data-key-id="o_538dd24a7f6ed79e0535" data-d1-id="o_77b09b26ad54f48c20b4" data-d2-id="o_b04c231a0bc92809b129">Thriving 5 week old, exclusively breast-fed, blood-streaked stools, no distension and normal vitals &rarr; <b>Milk protein-induced proctocolitis</b> &rarr; A well infant &mdash; the whole point is that nothing else is wrong</li>
<li data-type="avoid" data-d1="Necrotizing enterocolitis" data-d2="Malrotation with volvulus" data-src="uworld" data-item-id="q_e60fbc2c8c6fa76d0379" data-item-version="1" data-item-status="ready" data-key-id="o_ad1fff19f24729272053" data-d1-id="o_f17431bfead284f7b5a5" data-d2-id="o_f33bfb174aa020113dd4">Neonate with abdominal distension and bloody stools; which diagnosis should not be entertained &rarr; <b>Clostridioides difficile colitis</b> &rarr; Neonates are colonized but lack the toxin receptors</li>
<li data-type="next" data-src="uworld" data-nid="1482289468295 1580505819683" data-d1="Karyotype analysis" data-d2="Upper GI contrast series" data-item-id="q_0b7026f11d0cbb53c359" data-item-version="1" data-item-status="ready" data-key-id="o_122348a362a1e4ef5fbf" data-d1-id="o_121c25ec02db63b4fa07" data-d2-id="o_9c940570a4af479ae31f" data-lead-in="In addition to echocardiography, which of the following is the most appropriate next step in management?">10-hour-old term boy with bilious vomiting, born to a 39-year-old mother without prenatal care; voided once, no meconium yet; hypotonia, flat facies, upslanting palpebral fissures, protruding tongue, single transverse palmar creases and a sandal gap; abdomen soft and not distended; loud holosystolic murmur with a thrill at the left lower sternal border; nasogastric tube in place; film shows a double bubble with no distal gas &rarr; <b>Surgical repair</b> &rarr; Duodenal atresia in Down syndrome; the echocardiogram comes first because of the likely VSD</li>
<li data-type="test" data-src="authored" data-d1="Karyotype analysis" data-d2="Upper GI contrast series" data-item-id="q_741e0fb92e80a6238c53" data-item-version="1" data-item-status="ready" data-key-id="o_0895d0037a49cbd93265" data-d1-id="o_d1cd78e4e8095d6143c2" data-d2-id="o_e2b3bc41531262cc63ab" data-lead-in="Which of the following studies should be obtained before surgical repair?">1-day-old girl with trisomy 21 features and bilious vomiting since the first feed; film shows a double bubble with no distal gas; nasogastric decompression and IV fluids started; vital signs stable, no murmur heard &rarr; <b>Echocardiography</b> &rarr; About half of infants with Down syndrome have heart disease, often silent at birth</li>
<li data-type="dx" data-src="authored" data-d1="Duodenal atresia" data-d2="Meconium ileus" data-item-id="q_4fa6f1504b659b6a03d6" data-item-version="1" data-item-status="ready" data-key-id="o_31d83da41b1bbd0ee9ae" data-d1-id="o_3d965a483b9920ecde80" data-d2-id="o_a4c1e7b142e3367bb0c7">3-day-old term boy with trisomy 21 features, no meconium since birth, bilious vomiting and progressive abdominal distension; film shows diffusely dilated loops of bowel &rarr; <b>Hirschsprung disease</b> &rarr; Contrast enema, then rectal suction biopsy</li>
<li data-type="next" data-src="authored" data-d1="Contrast enema" data-d2="Rectal suction biopsy" data-item-id="q_bd75fbc2842475937a6a" data-item-version="1" data-item-status="ready" data-key-id="o_a62eb121fbd8fc1eff76" data-d1-id="o_972e85cec05decc9d557" data-d2-id="o_cfc5410d9e5722a47bf5">12-hour-old term girl who has not yet passed meconium; breastfeeding well, voided twice, no vomiting, soft nondistended abdomen, patent normally placed anus &rarr; <b>Observation</b> &rarr; Most term newborns pass meconium within 24 hours and none by 48 hours is delayed; a well, undistended 12-hour-old is not yet late</li>
<li data-type="mech" data-src="uworld" data-nid="1474670612056 1482959859744 1512667141201" data-d1="Early-onset Alzheimer disease" data-d2="Hypothyroidism" data-item-id="q_2cf684861e26f8b48049" data-item-version="1" data-item-status="ready" data-key-id="o_83d9383cc6771dba5815" data-d1-id="o_a9415d09eb639c9e085f" data-d2-id="o_f7cf302fa56d8cc7fec1" data-lead-in="This patient is at greatest risk of developing which of the following conditions?">52 hour old term girl delivered by cesarean for arrest of labor, voiding but has not passed stool, with a tense distended abdomen and no stool or gas on rectal exam; upright film shows many dilated small-bowel loops with little gas in the colon and rectum, and a decubitus film shows free air; at emergency laparotomy thick, sticky stool is evacuated from the ileum and the colon is diffusely narrow &rarr; <b>Chronic rhinosinusitis</b> &rarr; Meconium ileus from cystic fibrosis; nasal polyps and sinus opacification follow</li>
<li data-type="dx" data-src="authored" data-d1="Hirschsprung disease" data-d2="Malrotation with midgut volvulus" data-item-id="q_b45e93ed12880f3adb56" data-item-version="1" data-item-status="ready" data-key-id="o_a98209bd4d523456840b" data-d1-id="o_4f8d039fc1c0006ad510" data-d2-id="o_1e46e808c3931048c8e6">2 day old boy with no meconium since birth, progressive abdominal distension and bilious vomiting; rectal exam finds an empty rectum with no release of stool or gas; film shows dilated small-bowel loops; contrast enema shows a narrow microcolon with pellets of inspissated stool in the terminal ileum &rarr; <b>Meconium ileus</b> &rarr; Sweat chloride test for cystic fibrosis</li>
<li data-type="dx" data-src="authored" data-d1="Meconium ileus" data-d2="Necrotizing enterocolitis" data-item-id="q_0a7c8f2250fa7271beb4" data-item-version="1" data-item-status="ready" data-key-id="o_babf6f8e3eebc4d196dc" data-d1-id="o_dc4b11e83614ca03dada" data-d2-id="o_370809d75da6cfafbc3f">2 day old boy without dysmorphic features, no meconium yet, abdominal distension and bilious vomiting; rectal exam finds a tight anal canal and is followed by an explosive release of normal-appearing stool and gas &rarr; <b>Hirschsprung disease</b> &rarr; Contrast enema, then rectal suction biopsy</li>
<li data-type="next" data-src="authored" data-d1="Emergency laparotomy" data-d2="Rectal suction biopsy" data-item-id="q_b3f1f07cfa6c69b3cda9" data-item-version="1" data-item-status="ready" data-key-id="o_b97ffb5c424c1c912caf" data-d1-id="o_7452b013149a6dd26a04" data-d2-id="o_d2b99b902516f8e385c1">2 day old girl with distension and no meconium; contrast enema shows a microcolon with inspissated meconium in the terminal ileum; vital signs stable, no free air on film, no signs of peritonitis &rarr; <b>Hyperosmolar contrast enema</b> &rarr; Uncomplicated meconium ileus; sweat chloride test for cystic fibrosis</li>
<li data-type="mech" data-src="uworld" data-nid="1482886567135 1482886572434 1482886584577 1520188762940" data-d1="Intestinal obstruction from inspissated meconium" data-d2="Spinal cord dysfunction from abnormal neural tube closure" data-item-id="q_04cc8dab969e5a41b2f9" data-item-version="1" data-item-status="ready" data-key-id="o_9937988309c4504aab73" data-d1-id="o_2dd67b597f93c3b08305" data-d2-id="o_eb91c91888cbe1eed64d" data-lead-in="Which of the following is the most likely underlying mechanism of this patient&#x27;s condition?">2-day-old term girl born to a 38-year-old mother after a fentanyl epidural; feeding poorly, spit up her last feed, has not passed meconium; firm distended abdomen; shallow 2-mm sacral dimple with intact skin and no hair; rectal exam finds increased tone followed by a release of stool; normal strength and reflexes; abdominal film shows dilated bowel loops with no air in the rectum &rarr; <b>Failure of neural crest cell migration</b> &rarr; Hirschsprung disease; contrast enema, then rectal suction biopsy</li>
<li data-type="test" data-src="authored" data-d1="Anorectal manometry" data-d2="Sweat chloride test" data-item-id="q_12b1112df2736b47351f" data-item-version="1" data-item-status="ready" data-key-id="o_826de03e2a009422d78c" data-d1-id="o_b66777aada4ee54d1c25" data-d2-id="o_b43c332ec22e60eb2b52" data-lead-in="Which of the following is most likely to confirm the diagnosis?">4-day-old girl without dysmorphic features, no meconium since birth, poor feeding and a distended abdomen; rectal exam is followed by an explosive release of gas and normal-appearing stool; contrast enema shows a narrow rectosigmoid with dilated colon above it &rarr; <b>Rectal suction biopsy</b> &rarr; Absent ganglion cells confirm Hirschsprung disease; treatment is resection of the aganglionic segment</li>
<li data-type="test" data-src="uworld" data-nid="1482959865798 1482959868268 1512666496684 1539170612657 1569107827657 1581257194958 1581520331589" data-d1="Abdominal x-ray with air in the stomach and duodenum but no distal air" data-d2="Contrast enema with a narrow rectosigmoid and a dilated proximal colon" data-item-id="q_44131b0bc9eaa69fa316" data-item-version="1" data-item-status="ready" data-key-id="o_410b316049c9d493d4d7" data-d1-id="o_b924d2d75afe3de1a5aa" data-d2-id="o_309d5113361877c6c530" data-lead-in="Which of the following imaging findings would most likely be seen in this patient?">3-week-old boy in the NICU born at 28 weeks weighing 900 g, extubated to nasal cannula last week, on continuous nasogastric formula feeds and gaining weight, with small yellow seedy stools until none in the past 24 hours, now has 6 hours of nonbloody bilious vomiting; temperature 35.6 C, BP 75/45, pulse 165, respirations 70; lethargic, with a tense distended abdomen and hypoactive bowel sounds; leukocytosis and metabolic acidosis &rarr; <b>Abdominal x-ray with air in the bowel wall and portal veins</b> &rarr; Necrotizing enterocolitis; stop feeds, NG decompression and broad-spectrum antibiotics</li>
<li data-type="screen" data-src="authored" data-d1="Calorie-dense preterm infant formula" data-d2="Prophylactic broad-spectrum IV antibiotics" data-item-id="q_93efe70cf25380b27989" data-item-version="1" data-item-status="ready" data-key-id="o_929c389390a8176322f2" data-d1-id="o_05fccceff4fa0dcc7241" data-d2-id="o_76e7982002995eac3af2" data-lead-in="Which of the following is most likely to reduce this patient&#x27;s risk of necrotizing enterocolitis?">Girl born at 27 weeks weighing 950 g, now 4 days old, stable on room air in the NICU and about to start enteral feeds; her mother is expressing milk &rarr; <b>Exclusive feeding with breast milk</b> &rarr; The most effective measure against necrotizing enterocolitis</li>
<li data-type="dx" data-src="uworld" data-nid="1482959873096 1539170479420 1556448809081" data-d1="Necrotizing enterocolitis" data-d2="Pyloric stenosis" data-item-id="q_d6ae55f4494c28124dcd" data-item-version="1" data-item-status="ready" data-key-id="o_4caa0e8f4cfccd1b44a5" data-d1-id="o_0dad47d46f61f3287750" data-d2-id="o_dad0de450ee9495d7d70">7-month-old boy with 6 hours of persistent bilious vomiting, no fever, diarrhea or recent illness, last bowel movement 24 hours ago and no prior surgery; temperature 37 C, BP 70/50, pulse 180, respirations 65; moans with light palpation of a distended, hypertympanic abdomen with absent bowel sounds &rarr; <b>Intestinal malrotation with midgut volvulus</b> &rarr; Emergency laparotomy, Ladd procedure</li>
<li data-type="next" data-src="authored" data-d1="Upper gastrointestinal contrast series" data-d2="Nasogastric decompression and serial abdominal exams" data-item-id="q_94ad4ac0efdc3ba2f7cd" data-item-version="1" data-item-status="ready" data-key-id="o_5ce9b972723b4bf4721b" data-d1-id="o_7ad005cf6bc515a0d532" data-d2-id="o_b73d6b944314ef52cfe3">5-week-old term girl with 4 hours of bilious vomiting and inconsolable crying; after a 20 mL/kg saline bolus, pulse is 190, BP 55/30 and capillary refill 4 seconds; abdomen distended and diffusely tender; film shows a dilated stomach and duodenum with little distal gas &rarr; <b>Emergency laparotomy</b> &rarr; Unstable malrotation with midgut volvulus; Ladd procedure without waiting for contrast</li>
</ol>
<div class="danger"><span class="lbl">Exit ramps</span> <b>Free air</b> &mdash; stop investigating and operate &middot; <b>Unstable with bilious vomiting</b> &mdash; laparotomy without waiting for contrast &middot; <b>Term infant with NEC</b> &mdash; look for the perfusion insult: cyanotic heart disease, hypotension, sepsis &middot; <b>NEC worsening despite bowel rest and antibiotics</b>: surgery &middot; <b>Late NEC sequelae</b> &mdash; strictures and short-bowel syndrome &middot; Bilious emesis in <b>any infant</b>, at any age, is malrotation until an upper GI series excludes it</div>
<div class="danger"><span class="lbl">Decoy note: delayed meconium</span> <b>Maternal fentanyl epidural</b> &mdash; maternal opioids can slow the newborn bowel and delay meconium, but they do not raise rectal tone or cause an explosive release of stool on rectal exam &middot; <b>Mother aged 38</b> &mdash; advanced maternal age raises the risk of Down syndrome, which goes with Hirschsprung disease; most Hirschsprung disease is isolated, so a nondysmorphic infant still fits &middot; <b>Shallow sacral dimple with intact skin and no hair</b> &mdash; a normal finding; spina bifida occulta severe enough to cause a neurogenic bowel brings a <b>hair tuft</b> or <b>neurologic deficits</b>, and this exam has normal strength and reflexes &middot; <b>Tight rectum, then a release of normal stool</b> &mdash; the squirt sign; meconium ileus gives normal tone, no release, and inspissated meconium in the ileum</div>
<div class="pearls"><span class="lbl">Duodenal atresia in Down syndrome</span> <b>The order</b> — stop feeds, NG decompression and IV fluids, echocardiogram, then <b>surgical repair</b> &middot; <b>Why the echo</b> — about <b>half</b> of infants with Down syndrome have heart disease; a loud holosystolic murmur at the left lower sternal border is a VSD &middot; <b>No distension</b> — the block is proximal, so the rest of the abdomen stays flat; distension points to a distal obstruction &middot; <b>Meconium timing</b> — about 99% of healthy term newborns pass meconium <b>within 24 hours</b>, so a distended infant with none by then needs evaluation; <b>none by 48 hours</b> is delayed and raises Hirschsprung disease or meconium ileus; a well, undistended newborn a few hours old is not yet late &middot; <b>Pyloric stenosis</b> — <b>nonbilious</b> projectile vomiting at <b>3 to 6 weeks</b>, not bilious emesis on day 1</div>
<div class="pearls"><span class="lbl">Pearls</span> <b>Pneumatosis</b> &mdash; gas made by bacteria that have invaded the wall, which is why it is specific &middot; <b>Bilious</b> means the obstruction is distal to the ampulla; it locates the obstruction and is urgent until an upper GI series excludes malrotation &middot; NEC and volvulus both give a distended, bilious, unwell neonate; the gas pattern separates them &middot; A well infant with blood in the stool is almost never surgical; distension and instability suggest a surgical cause &middot; Prematurity is the commonest NEC risk factor, not a required one &middot; <b>Meconium ileus means cystic fibrosis</b> &mdash; nearly all patients with CF develop sinopulmonary disease, including <b>chronic rhinosinusitis with nasal polyps</b> (sinus opacification by age 1); hypothyroidism and early-onset Alzheimer disease belong to Down syndrome, which goes with Hirschsprung disease</div>
<div class="pearls"><span class="lbl">NEC severity and prevention</span> <b>Mild</b>: lethargy, temperature instability, apnea, feeding intolerance, bilious residuals, heme-positive stool; labs and film normal or mild dilation &middot; <b>Moderate</b>: adds absent bowel sounds, tenderness, abdominal wall erythema, thrombocytopenia, metabolic acidosis and pneumatosis &middot; <b>Severe</b>: adds hypotension, peritonitis, DIC and pneumoperitoneum &middot; <b>Platelets</b>: the fall tracks severity, and a rising count is often the first sign of improvement &middot; <b>Prevention</b>: exclusive <b>breast milk</b> is the most effective measure; <b>antenatal corticosteroids</b> for a mother likely to deliver preterm within 7 days also lower the risk, along with respiratory distress syndrome and intraventricular hemorrhage</div>
<div class="pearls"><span class="lbl">Malrotation beyond the newborn period</span> <b>Age</b>: most present in the first month, but volvulus can happen at any age, so a 7-month-old with bilious vomiting, tachycardia and a silent distended abdomen still has malrotation first &middot; <b>Older children</b>: intermittent abdominal pain and vomiting, sometimes failure to thrive &middot; <b>Late signs</b>: hematochezia, peritonitis and shock mean the bowel is already ischemic &middot; <b>Not NEC</b>: NEC is a disease of preterm infants in the first weeks on feeds &middot; <b>Not pyloric stenosis</b>: that vomiting is nonbilious and projectile at 3 to 6 weeks, in a well infant with an olive-shaped mass</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Infant Stool Complaints: Dyschezia, FPIAP &amp; Secondary Lactase Deficiency</b> covers the well infant with blood in the stool; this brief covers the sick one. Part II <b>Tracheoesophageal Fistula with Esophageal Atresia</b> covers obstruction above the pylorus. Ask: is the infant well, and what is the gas pattern?</div>
<div class="rule"><span class="lbl">Transferable rule</span> In a distended neonate, the stool and vital signs show severity and the <b>gas pattern</b> identifies the disease: air in the wall, air where bowel should be, or no air at all.</div>
<div class="traps">
<div class="trapline"><span class="pill p-unchecked">Unchecked attribute</span><span class="trapwhy">NEC filed under prematurity, so a term infant is ruled out without checking perfusion.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Bilious nasogastric return pulls toward volvulus before the film is read.</span></div>
<div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Right category of neonatal bowel emergency, wrong member of it.</span></div>
<div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Karyotype confirms trisomy 21, but it is not urgent and does not change the need for repair.</span></div>
<div class="trapline"><span class="pill p-uniform">Redundant workup</span><span class="trapwhy">An upper GI series adds nothing once the film shows a double bubble with no distal gas; it is for malrotation.</span></div>
<div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">No meconium sounds like Hirschsprung disease, but a 10-hour-old is not yet late and the abdomen is not distended.</span></div>
<div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Early-onset Alzheimer disease and hypothyroidism are real Down syndrome associations, but Down syndrome goes with Hirschsprung disease; thick meconium in the ileum with a microcolon is meconium ileus, which means cystic fibrosis and later sinus disease.</span></div>
<div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Inspissated meconium is the other cause of no meconium with distension, but it obstructs the ileum with a microcolon, normal rectal tone and no squirt; it is cystic fibrosis, not Hirschsprung disease.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">A shallow sacral dimple without a hair tuft is normal; spinal cord dysfunction would bring neurologic deficits, and strength and reflexes are normal.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">A maternal fentanyl epidural can cause neonatal ileus, but not increased rectal tone with an explosive release of stool.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Bilious vomiting pulls toward a proximal block, but air in the stomach and duodenum with no distal gas is duodenal atresia, which presents with the first feeds; an infant who has been passing yellow seedy stools on full feeds is not obstructed there.</span></div>
<div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">No stool for a day suggests Hirschsprung disease, but that shows no meconium by 48 hours or chronic constipation, not sudden hypothermia, acidosis and a tense abdomen in a 3-week-old preterm infant.</span></div>
<div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">NEC is the right category of sick distended bowel, but it belongs to preterm infants in their first weeks on feeds; a term 7-month-old with bilious vomiting has volvulus.</span></div>
<div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Pyloric stenosis causes vomiting in infancy, but it is nonbilious and projectile at 3 to 6 weeks; bilious vomiting in any infant is malrotation until proven otherwise.</span></div>
</div>
</div>
```

### `bs-wilson`: Wilson Disease: Copper in the Liver, Brain and Eye

```html
<div class="brief bs" id="bs-wilson" data-shelf="fm peds" data-nid="1486591023980 1584231759637" data-bp="gi neuro">
<h4>Wilson Disease: Copper in the Liver, Brain and Eye</h4>
<p class="sub">A teen with hepatitis, a tremor and brown corneal rings &middot; is the patient young, with brain, eye or red-cell findings, and is the ceruloplasmin low?</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; adolescent with liver disease (hepatitis, possibly progressing to cirrhosis) plus neuropsychiatric change: tremor, slurred speech and altered behavior &middot; <b>Exam</b> &mdash; Kayser-Fleischer rings at the corneal margin &middot; <b>Labs</b> &mdash; elevated transaminases &middot; <b>Q</b> &mdash; the most likely underlying mechanism of the disease</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Think of <b>Wilson disease</b> in any patient <b>under about 40</b> ⚠︎ with unexplained liver disease, and especially when the liver disease comes with <b>neuropsychiatric signs</b> (tremor, dysarthria, dystonia, depression, personality change, psychosis), <b>Kayser-Fleischer rings</b>, or a <b>Coombs-negative hemolytic anemia</b>. Screen with serum ceruloplasmin (<b>low</b>) and a slit-lamp exam; a <b>high 24-hour urine copper</b> confirms, and liver biopsy copper settles cases where the tests disagree.</p>
<p>The mechanism is autosomal recessive loss of the ATP7B hepatocyte transporter that loads copper onto ceruloplasmin and excretes the excess into bile, so copper builds up in the liver (hepatitis, cirrhosis, sometimes acute liver failure), then spills into the blood and deposits in the <b>basal ganglia</b>, the <b>cornea</b> and <b>red cells</b>. Ceruloplasmin is low because it is unstable without its copper. The exception is the patient with liver disease alone: Kayser-Fleischer rings are often absent, and ceruloplasmin can read normal because it rises with inflammation, so the urine copper or the biopsy decides.</p>
</div>
<div class="tw">
<table data-mask="3"><caption>Liver disease in a young patient: the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th><th>Why less likely here</th></tr></thead>
<tbody>
<tr><td><b>Wilson disease</b></td><td>Autosomal recessive; child, teen or young adult; hepatitis, cirrhosis or acute liver failure, with movement or psychiatric change</td><td><b>Kayser-Fleischer rings</b>, <b>low ceruloplasmin</b>, Coombs-negative hemolysis</td><td>The key: the only one that adds brain, eye and red-cell findings to the liver</td></tr>
<tr><td>Autoimmune hepatitis</td><td>Young woman, often with another autoimmune disease; acute or chronic hepatitis</td><td><b>ANA and anti-smooth muscle antibody</b> (anti-LKM1 in children), <b>high IgG</b></td><td>No neurologic signs or corneal rings; Wilson can mimic it, so check ceruloplasmin</td></tr>
<tr><td>Hereditary hemochromatosis</td><td>Autosomal recessive HFE; iron builds for decades, so middle-aged men and women after menopause</td><td><b>High transferrin saturation and ferritin</b>; diabetes, bronze skin, arthropathy, cardiomyopathy, hypogonadism</td><td>Too young; iron does not cause tremor or corneal rings</td></tr>
<tr><td>Alpha-1 antitrypsin deficiency</td><td>Misfolded protein retained in hepatocytes; neonatal cholestasis in infants, cirrhosis in adults, early basal emphysema</td><td><b>Low serum alpha-1 antitrypsin</b>; lung disease in a young smoker</td><td>Its second organ is the lung, not the brain or eye</td></tr>
<tr><td>Viral hepatitis</td><td>Most common cause; risk factors for hepatitis B or C, or an acute illness with hepatitis A</td><td><b>Positive serologies</b></td><td>No neuropsychiatric signs or corneal rings; hemolysis is not a feature</td></tr>
<tr><td>MASLD</td><td>Obesity, diabetes, dyslipidemia; mild ALT-predominant rise</td><td><b>Metabolic syndrome with a hyperechoic liver</b>; a diagnosis of exclusion</td><td>Nothing outside the liver</td></tr>
<tr><td>Antipsychotic-induced parkinsonism</td><td>Tremor, rigidity or dystonia after starting a dopamine blocker</td><td><b>Movement signs follow the drug</b>; liver tests normal</td><td>Does not explain the liver disease</td></tr>
</tbody>
</table>
</div>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>Liver tests (AST, ALT, bilirubin, INR)</td><td>First</td><td><b>Hepatocellular</b> rise, from mild to acute liver failure</td><td>Liver injury; the pattern alone does not name the cause</td></tr>
<tr><td>Hepatitis serologies, iron studies, ANA and anti-smooth muscle antibody, alpha-1 antitrypsin level</td><td>First</td><td><b>Normal</b></td><td>Excludes the common mimics</td></tr>
<tr><td>Serum ceruloplasmin</td><td>Screen</td><td><b>Low</b>, under 20 mg/dL ⚠︎</td><td>Wilson disease; a normal value does not exclude it in active hepatitis, because ceruloplasmin is an acute-phase reactant</td></tr>
<tr><td>Slit-lamp examination</td><td>Next</td><td><b>Kayser-Fleischer rings</b></td><td>Corneal copper; almost always present with neurologic disease, often absent with liver disease alone</td></tr>
<tr><td>24-hour urine copper</td><td>Confirms</td><td><b>High</b>, over 100 mcg per day ⚠︎</td><td>Copper overflow from an overloaded liver; also used to monitor chelation</td></tr>
<tr><td>Liver biopsy with copper measurement</td><td>By branch</td><td><b>High</b> hepatic copper</td><td>When ceruloplasmin, urine copper and the slit-lamp exam disagree</td></tr>
<tr><td>CBC, reticulocytes, direct Coombs test</td><td>Supports</td><td>Anemia, <b>high reticulocytes</b>, Coombs <b>negative</b></td><td>Copper damages red cells; with acute liver failure, fulminant Wilson disease</td></tr>
<tr><td>Brain MRI</td><td>Supports</td><td><b>Basal ganglia</b> signal change</td><td>Neurologic involvement; not needed for the diagnosis</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="mech" data-src="uworld" data-nid="1486591023980 1584231759637" data-d1="Increased intestinal iron absorption" data-d2="Hepatocyte retention of a misfolded protease inhibitor" data-item-id="q_6580de55e4754d641c36" data-item-version="1" data-item-status="ready" data-key-id="o_6c50cf92032f82fb88b0" data-d1-id="o_819146e704f9153f358c" data-d2-id="o_4f0d28cd3086faab21fc" data-lead-in="Which of the following is the most likely underlying mechanism of this patient&#x27;s disease?">16 yo M with several months of fatigue and mild jaundice, a new hand tremor, slurred speech and irritability with falling grades; elevated AST and ALT; golden-brown rings at the corneal margins on slit-lamp exam &rarr; <b>Defective copper transport in hepatocytes</b> &rarr; Wilson disease: ATP7B failure blocks biliary copper excretion and copper loading onto ceruloplasmin, so copper deposits in the liver, basal ganglia and cornea</li>
<li data-type="test" data-src="authored" data-d1="Liver biopsy with copper measurement" data-d2="MRI of the brain" data-item-id="q_e83055dbd74a4e8a4cb4" data-item-version="1" data-item-status="ready" data-key-id="o_c68f8817968b8090f8cb" data-d1-id="o_5efd8bf9e6128f411451" data-d2-id="o_f70b08f6666b9206f056" data-lead-in="Which of the following is the most appropriate next diagnostic study?">19 yo F with 3 months of fatigue and a fine hand tremor; ALT 240, AST 190, bilirubin normal; hepatitis B and C serologies negative; ferritin and transferrin saturation normal; ANA and anti-smooth muscle antibody negative; normal BMI and no alcohol use &rarr; <b>Serum ceruloplasmin</b> &rarr; screen for Wilson disease in a young patient with unexplained hepatitis and a tremor; slit-lamp exam and 24-hour urine copper follow</li>
<li data-type="dx" data-src="authored" data-d1="Wilson disease" data-d2="Acute hepatitis A" data-item-id="q_254acab9b2c63f62f420" data-item-version="1" data-item-status="ready" data-key-id="o_d38e94358911fa9010fc" data-d1-id="o_bc324dfbdd57cf96846f" data-d2-id="o_45f7689bf6f069006f78">17 yo F with Hashimoto thyroiditis and 6 weeks of fatigue, joint aches and jaundice; ALT 850, AST 700; serum IgG high; ANA and anti-smooth muscle antibody positive; ceruloplasmin normal; no Kayser-Fleischer rings; normal neurologic exam &rarr; <b>Autoimmune hepatitis</b> &rarr; corticosteroids, with azathioprine to spare steroids</li>
<li data-type="next" data-src="authored" data-d1="Oral zinc acetate" data-d2="Liver transplantation" data-item-id="q_064ca1f3bfd729615c11" data-item-version="1" data-item-status="ready" data-key-id="o_58c81238e24efe5995d8" data-d1-id="o_425a8924dcf65bb83473" data-d2-id="o_7d3fb6849a3e7c823f72">21 yo M with 1 year of hand tremor and dysarthria; compensated cirrhosis on imaging, INR 1.3, no ascites or encephalopathy; ceruloplasmin low, 24-hour urine copper high, Kayser-Fleischer rings on slit-lamp exam &rarr; <b>Oral penicillamine</b> &rarr; symptomatic Wilson disease: lifelong chelation (penicillamine or trientine), zinc later for maintenance</li>
<li data-type="next" data-src="authored" data-d1="Oral penicillamine" data-d2="Intravenous acetylcysteine" data-item-id="q_7b0a3f75d5c80bb84acf" data-item-version="1" data-item-status="ready" data-key-id="o_d2d7ffa1ea2e44ace105" data-d1-id="o_ae894f5bc0af80f7bb44" data-d2-id="o_d40a3b605f92ad5c75e2">18 yo F with 1 week of jaundice, now confused; INR 3.2; hemoglobin 7.8 with high reticulocytes and a negative direct Coombs test; Kayser-Fleischer rings on slit-lamp exam; no acetaminophen ingestion &rarr; <b>Urgent liver transplantation</b> &rarr; fulminant Wilson disease: acute liver failure with Coombs-negative hemolysis does not recover with chelation alone</li>
<li data-type="screen" data-src="authored" data-d1="Serum ferritin and transferrin saturation" data-d2="No testing unless symptoms develop" data-item-id="q_6a31210a63b37c249c0c" data-item-version="1" data-item-status="ready" data-key-id="o_a6d6a573de0de8bc4f9f" data-d1-id="o_0eb79e5178a4dd758dbb" data-d2-id="o_a6bfd5e602fb2194418c">14 yo M, asymptomatic, whose 17-year-old sister was just diagnosed with Wilson disease; normal growth and development; normal physical and neurologic exam &rarr; <b>Serum ceruloplasmin and liver tests</b> &rarr; siblings carry a 1 in 4 risk; add a slit-lamp exam and 24-hour urine copper, and treat presymptomatic disease with zinc</li>
<li data-type="avoid" data-src="authored" data-d1="Switching to zinc maintenance" data-d2="Continuing yearly urine copper checks" data-item-id="q_a85c6013e48264f3c470" data-item-version="1" data-item-status="ready" data-key-id="o_98039123c5d4e47183ac" data-d1-id="o_5c25c4b0a9b6dc89d357" data-d2-id="o_6afb5dd9dfdd78094eee">24 yo M with Wilson disease treated with penicillamine for 3 years; tremor resolved, liver tests now normal, urine copper at target; asks about coming off medication &rarr; <b>Stopping copper-lowering therapy</b> &rarr; treatment is lifelong; stopping can precipitate acute liver failure</li>
</ol>
<div class="danger"><span class="lbl">Management</span> <b>Symptomatic disease</b> &mdash; copper chelation with <b>penicillamine or trientine</b>, lifelong, with a low-copper diet (avoid shellfish, organ meats, nuts, chocolate and mushrooms) &middot; <b>Maintenance or presymptomatic disease</b> &mdash; <b>zinc</b>, which blocks intestinal copper absorption &middot; <b>Fulminant liver failure</b> &mdash; urgent <b>liver transplantation</b>, which corrects the liver defect &middot; <b>Family</b> &mdash; screen first-degree relatives, <b>siblings</b> above all (a 1 in 4 chance of disease, since it is autosomal recessive), with ceruloplasmin, liver tests and a slit-lamp exam &middot; <b>Never stop</b> &mdash; stopping therapy can precipitate acute liver failure</div>
<div class="pearls"><span class="lbl">Pearls</span> Psychiatric change or falling school performance can precede the liver findings, so a young patient with new psychiatric illness and abnormal liver tests needs a ceruloplasmin &middot; Acute liver failure with a Coombs-negative hemolytic anemia in a teen or young adult is fulminant Wilson disease, and it needs a transplant center, not chelation alone &middot; A presumed autoimmune hepatitis in a young patient should have ceruloplasmin checked before steroids &middot; Serum total copper is usually low; the urine copper is the number that is high</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>MASLD / Metabolic Fatty Liver</b> lists Wilson disease among the exclusions: is the patient under about 40, with tremor or Kayser-Fleischer rings, and is the ceruloplasmin low? Part I <b>Cholestasis &amp; the LFT Patterns</b> places Wilson in the hepatocellular pattern: are the transaminases, not the alkaline phosphatase, leading? Part II <b>Hereditary Spherocytosis</b> covers the other Coombs-negative hemolysis of the young: are there spherocytes and an affected parent, or liver disease with corneal rings? Part I <b>Tick-Borne Fever and Rash</b> holds the acute mimic: did confusion with transaminitis arrive over hours with fever and a rash, or over months with a tremor?</div>
<div class="rule"><span class="lbl">Transferable rule</span> When liver disease in a patient under about 40 comes with a finding outside the liver, ask which organ it is: brain, cornea or red cells point to copper, the lung to alpha-1 antitrypsin, and the pancreas, skin, joints and heart in an older patient to iron.</div>
<div class="traps"><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Increased intestinal iron absorption: the right class, an inherited metal overload of the liver, but the wrong metal; HFE hemochromatosis presents in middle age with diabetes, skin and joint findings, never tremor or corneal rings.</span></div><div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Hepatocyte retention of a misfolded protease inhibitor: alpha-1 antitrypsin deficiency is an inherited liver disease of the young, but its second organ is the lung; it does not explain neuropsychiatric signs or Kayser-Fleischer rings.</span></div></div>
</div>
```
