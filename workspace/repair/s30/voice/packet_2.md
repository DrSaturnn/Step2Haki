# Voice packet 2 of 5 (s30, gi): cholestasis, infant-stool, bs-impaction, bs-fat-soluble-vitamins, bs-water-soluble-vitamins

**Instructions.** Everything you need is in this packet. Do not open index.html, the skill files or other packets. Write your edits to `repair/s30/04_voice_2.json`, run `python3 tools/verify_edits.py repair/s30/04_voice_2.json scratch/s30_base.html --voice` from the workspace folder (Step2Haki/workspace) and loop until it prints PASS (add `--report` to read your own claim map). Then reply with the 3 to 5 line report the rules ask for, including any acronym you skipped.

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

## Briefs (5): current HTML
### `cholestasis`: Cholestasis & the LFT Patterns

```html
<div class="brief" id="cholestasis" data-shelf="fm" data-bp="gi">
<h4>Cholestasis &amp; the LFT Patterns</h4>
<p class="sub">Classify → localize → then test for causes</p>
<div class="dp"><span class="lbl">The decision point</span>
<p>Classify the <b>pattern</b> before testing for causes. <b>Alk phos ↑↑ with normal AST/ALT and a direct hyperbilirubinemia</b> is cholestasis. Then order an <b>abdominal ultrasound</b> to answer one question: <b>are the ducts dilated?</b> Nondilated ducts (intrahepatic) lead to an antibody test; dilated ducts (extrahepatic) lead to cross-sectional imaging.</p>
<p>Step 1.5: confirm the alk phos is <b>hepatic</b> with a <b>GGT</b> (or 5′-nucleotidase); alkaline phosphatase also comes from <b>bone, placenta, and intestine</b>.</p></div>
<table data-mask="4"><caption>LFT patterns<span class='cap-sub'>hepatocellular vs cholestatic</span></caption>
<thead><tr><th>Pattern</th><th>Labs</th><th>Causes</th><th>Targeted tests</th><th>Confirms, then</th></tr></thead>
<tbody>
<tr><td><b>Hepatocellular</b></td><td><b>AST/ALT ↑↑</b>, alk phos normal or mild</td><td>Viral hepatitis, MASLD, alcohol (<b>AST:ALT ≥2</b>), autoimmune hepatitis, hemochromatosis, Wilson, α1-antitrypsin, drugs</td><td><b>ASMA / anti-LKM1</b>, iron studies, ceruloplasmin</td><td>Viral serologies first; <b>liver biopsy</b> when the cause stays unclear</td></tr>
<tr><td><b>Cholestatic</b></td><td><b>Alk phos ↑↑ + direct bilirubin ↑</b></td><td>PBC, PSC, choledocholithiasis, pancreatic head cancer, stricture, drugs, infiltrative disease</td><td><b>Ultrasound first</b>, then AMA or MRCP/CT</td><td>Normal ducts: AMA for PBC, biopsy if negative; dilated ducts: MRCP or CT, <b>ERCP</b> only to intervene</td></tr>
<tr><td><b>Isolated hyperbilirubinemia</b></td><td>Bilirubin ↑ alone</td><td><b>Indirect:</b> Gilbert, hemolysis, Crigler-Najjar · <b>Direct:</b> Dubin-Johnson, Rotor</td><td>Fractionate, smear, reticulocytes</td><td>Indirect, normal smear and reticulocytes, rises with fasting: <b>Gilbert</b>, no further testing</td></tr>
<tr><td>Alk phos ↑ with <b>normal GGT</b></td><td>—</td><td><b>Not liver at all</b> — bone (Paget, metastases, vitamin D deficiency, healing fracture, growing child) or placenta</td><td>Bone-specific workup</td><td><b>GGT</b> normal confirms a non-hepatic source; then calcium, phosphate, vitamin D and bone imaging</td></tr>
</tbody>
</table>
<h5>After the ultrasound</h5>
<ul class="plain">
<li><b>Ducts NOT dilated → intrahepatic</b> → <b>AMA</b> (antimitochondrial antibody) for PBC; MRCP and biopsy if suspicion persists</li>
<li><b>Ducts dilated → extrahepatic</b> → <b>MRCP</b> (biliary tree) or <b>CT</b> (pancreatic mass) → <b>ERCP only when intervention is needed</b></li>
</ul>
<table data-mask="none"><caption>Primary biliary cholangitis vs primary sclerosing cholangitis</caption>
<thead><tr><th></th><th>PBC</th><th>PSC</th></tr></thead>
<tbody>
<tr><td>Patient</td><td>Middle-aged <b>women</b></td><td>Young <b>men</b></td></tr>
<tr><td>Antibody</td><td><b>AMA</b></td><td><b>p-ANCA</b></td></tr>
<tr><td>Association</td><td>Sjögren, Hashimoto, RA, celiac</td><td><b>Ulcerative colitis (~70–80%)</b></td></tr>
<tr><td>Imaging / path</td><td>Small intrahepatic ducts; <b>florid duct lesion</b>, granulomas</td><td><b>"Beads on a string"</b> on MRCP; <b>onion-skin fibrosis</b></td></tr>
<tr><td>Clinical</td><td><b>Pruritus + fatigue</b>, xanthelasma, hyperlipidemia</td><td>Fatigue, jaundice; <b>↑ cholangiocarcinoma and colorectal cancer</b></td></tr>
<tr><td>Treatment</td><td><b>Ursodeoxycholic acid</b></td><td>No effective medical therapy → transplant</td></tr>
</tbody>
</table>
<h5>Scenario bank</h5>
<ol class="bank">
<li data-type="next" data-d1="ERCP first" data-d2="Repeat ultrasound in 3 months" data-item-id="q_0950bfff255e50f9aa43" data-item-version="1" data-item-status="ready" data-key-id="o_5c65913635d853e89742" data-d1-id="o_31629d185aeb5840b3e5" data-d2-id="o_aba5e26374ef5c04b18f">Ultrasound shows a <b>dilated CBD and a pancreatic head mass</b> → <b>CT abdomen</b> → pancreatic adenocarcinoma</li>
<li data-type="dx" data-d1="Primary sclerosing cholangitis" data-d2="Autoimmune hepatitis" data-item-id="q_2def7a94c1c8561f86e1" data-item-version="1" data-item-status="ready" data-key-id="o_a94414694b7658eeb579" data-d1-id="o_2375542f4dc6501e8304" data-d2-id="o_3d5999a345195005ad9c">Normal ducts + <b>AMA positive</b> in a woman with pruritus → <b>Primary biliary cholangitis</b> → ursodiol</li>
<li data-type="test" data-d1="ERCP" data-d2="Liver biopsy" data-item-id="q_10e9b3319d655586bdce" data-item-version="2" data-item-status="ready" data-key-id="o_ff03d09eb70555388840" data-d1-id="o_15d5c549f8fe51f69525" data-d2-id="o_fb0104bc26f65ce2983f" data-lead-in="Which of the following is the most appropriate diagnostic study to obtain at this time?">Young man with <b>ulcerative colitis</b> and a cholestatic pattern → <b>MRCP</b> &rarr; beads on a string → PSC</li>
<li data-type="dx" data-d1="Cholestatic liver injury" data-d2="Bile duct obstruction" data-item-id="q_08b946e4e4205f6cb045" data-item-version="2" data-item-status="ready" data-key-id="o_8c6a2d4b35965ea18d24" data-d1-id="o_ee24ae5505055bb5a637" data-d2-id="o_ad1b9e19c0ca53418dc5">Alk phos elevated with a <b>normal GGT</b> → <b>Bone source or pregnancy</b> &rarr;  not liver disease at all</li>
<li data-type="dx" data-d1="Acute cholecystitis" data-d2="Choledocholithiasis without cholangitis" data-item-id="q_9f5d29acb26253f79858" data-item-version="1" data-item-status="ready" data-key-id="o_487ef968bd0b5ecfbc40" data-d1-id="o_75a763fa7d5e5326a874" data-d2-id="o_68dbc483e9fb581e8b92"><b>Charcot triad</b> (fever + RUQ pain + jaundice) → Ascending cholangitis → <b>urgent ERCP</b></li>
<li data-type="dx" data-d1="Choledocholithiasis" data-d2="Primary biliary cholangitis" data-item-id="q_08de329f5e5a59dd851e" data-item-version="2" data-item-status="ready" data-key-id="o_7ac9bfc44688528c8834" data-d1-id="o_8a2af2f4a33b554eb239" data-d2-id="o_e5f4e737ef6b5a4fa3ad"><b>Painless jaundice + weight loss + palpable nontender gallbladder</b> (<b>Courvoisier sign</b>) → Pancreatic head malignancy &rarr;  not stones</li>
<li data-type="dx" data-d1="Crigler-Najjar type II" data-d2="Hemolysis" data-item-id="q_0be8ac71bebf5e328ace" data-item-version="1" data-item-status="ready" data-key-id="o_1318925ba5f55bd9bfb3" data-d1-id="o_74a68e3208b859b58e18" data-d2-id="o_f8359025be9e5e8aa474">Isolated <b>indirect</b> hyperbilirubinemia appearing with fasting or illness, all else normal → <b>Gilbert syndrome</b> → reassurance</li>
<li data-type="next" data-d1="Start ursodiol" data-d2="Liver biopsy" data-item-id="q_698a6d92f12459929956" data-item-version="1" data-item-status="ready" data-key-id="o_32840acb1d615ca78387" data-d1-id="o_7bef7476cfbd59a2ab79" data-d2-id="o_bc0cb3e469e95ecd95ae">Cholestatic pattern after <b>amoxicillin-clavulanate</b>, anabolic steroids, OCPs, or chlorpromazine → Stop the drug, then monitor</li>
<li data-type="dx" data-d1="Primary biliary cholangitis" data-d2="Lymphoma" data-item-id="q_888d45f50c345f178c35" data-item-version="1" data-item-status="ready" data-key-id="o_835582bec7aa580ca59f" data-d1-id="o_c4864611c36b56cd9d3d" data-d2-id="o_e918807e1bbf5718aec4">Cholestasis + hilar lymphadenopathy + hypercalcemia → <b>Sarcoidosis</b></li>
</ol>
<div class="danger"><span class="lbl">Why the distractors fail</span>
<b>ASMA and iron studies</b>: these test for autoimmune and metabolic liver disease, which cause hepatocellular injury, the <b>wrong pattern</b> here. <b>ERCP</b>: premature at this step; it is invasive, carries a risk of post-ERCP pancreatitis, and no lesion has yet been shown to need intervention. <b>Repeat LFTs in 3 months</b>: appropriate only when a reversible cause has been identified and removed; here the alk phos is 7× normal with no cause found.</div>
<div class="rule"><span class="lbl">Transferable rule</span> Use the LFT pattern as a <b>triage instrument</b> to choose tests. Tests are pattern-specific: an autoimmune hepatitis antibody looks for hepatocellular disease and does not belong in the workup of a cholestatic pattern.</div>
<div class="traps"><span class="pill p-seq">Sequencing trap</span></div>
</div>
```

### `infant-stool`: Infant Stool Complaints: Dyschezia, FPIAP & Secondary Lactase Deficiency

```html
<div class="brief" id="infant-stool" data-shelf="fm peds" data-nid="1473707579754" data-bp="gi">
<h4>Infant Stool Complaints: Dyschezia, FPIAP &amp; Secondary Lactase Deficiency</h4>
<p class="sub">Well-appearing infant with a stool complaint · reassure, eliminate, or work up</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 4 mo M, thriving, screams and strains for 10 minutes several times daily then passes a soft yellow stool, normal examination &middot; <b>Q</b> &mdash; the most appropriate next step; options spanned reassurance and parental education, a glycerin suppository and switching to an extensively hydrolyzed formula</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Three benign stool complaints present in a <b>thriving, well-appearing</b> infant or child with alarmed parents; the <b>stool</b> and the <b>timing</b> set the answer. Straining and screaming for minutes, then a <b>normal soft stool</b>, under 9 months, is <b>infant dyschezia</b> → reassurance only. <b>Painless blood-streaked stools</b> in a well infant under 6 months is <b>food protein-induced allergic proctocolitis</b> → eliminate cow's milk and soy from the maternal diet, or use an extensively hydrolyzed formula. Watery diarrhea and bloating <b>after dairy is reintroduced</b> following gastroenteritis is <b>secondary lactase deficiency</b> → temporary lactose avoidance, no workup.</p>
<p>Two mimics change the tier, and both are <b>ill-appearing</b>: <b>FPIES</b> (profuse vomiting and lethargy 1–4 h after the trigger, non-IgE) needs fluids, and <b>IgE-mediated</b> allergy (urticaria, wheeze, anaphylaxis within minutes) needs epinephrine. Parental distress is not a finding; a thriving infant does not need a formula change, a suppository, or a stool workup.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Infant dyschezia</b> — under 9 months, strains and cries for minutes, then passes a normal soft stool, thriving; hard stool means constipation instead · <b>Food protein-induced allergic proctocolitis</b> — well-appearing infant under 6 months, painless blood-streaked stools, insidious onset; non-IgE · <b>Food protein-induced enterocolitis syndrome</b> — under 12 months, profuse vomiting with diarrhea, dehydration and lethargy within hours (1–4 h) of the trigger, ill-appearing; non-IgE · <b>IgE-mediated food allergy</b> — urticaria, vomiting, wheeze, angioedema or hypotension within minutes (under 1 h), any age · <b>Osmotic diarrhea</b> — stops with fasting, raised stool osmotic gap, acidic stool pH</div>
<table>
<caption>The well-appearing infant with a stool complaint — the differential</caption>
<thead><tr><th>Diagnosis</th><th>Illness script</th><th>The NBME tell</th></tr></thead>
<tbody>
<tr><td><b>Infant dyschezia</b></td><td>Under 9 months; cannot coordinate a Valsalva with pelvic-floor relaxation; resolves spontaneously</td><td><b>Screams and strains, then a normal soft stool</b>; reassurance, nothing else</td></tr>
<tr><td>Functional constipation</td><td>Infrequent, hard or pellet stools, often at a diet transition</td><td><b>Hard stool</b> — the one word that converts dyschezia into constipation</td></tr>
<tr><td><b>FPIAP</b></td><td>Under 6 months, breastfed or formula-fed; cow's milk or soy protein; resolves by about 1 year</td><td><b>Painless blood streaks in a well infant</b>; eliminate cow's milk and soy, no scope</td></tr>
<tr><td>FPIES</td><td>Under 12 months; non-IgE; classic triggers include cow's milk and soy</td><td><b>Profuse vomiting, lethargy, dehydration 1–4 h after feeding</b>, ill-appearing; fluids, not epinephrine</td></tr>
<tr><td>IgE-mediated food allergy</td><td>Any age; minutes after exposure; may progress to anaphylaxis</td><td><b>Urticaria or wheeze within an hour</b>; epinephrine, strict avoidance, allergist</td></tr>
<tr><td>Secondary lactase deficiency</td><td>Brush-border lactase lost after gastroenteritis or with IBD; osmotic diarrhea</td><td><b>Diarrhea and bloating when dairy is reintroduced</b> after a resolving gastroenteritis; no fever, no vomiting</td></tr>
<tr><td>Necrotizing enterocolitis <span class="tag t-em">Can't miss</span> <span class="tag t-peds">Preemie</span></td><td>Preterm infant on enteral feeds; bacterial invasion of an ischemic bowel wall</td><td><b>Distension, bloody stools, pneumatosis intestinalis</b> in a preemie — never a well-infant diagnosis</td></tr>
</tbody>
</table>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="next" data-d1="Glycerin suppository before feeds" data-d2="Switch to an extensively hydrolyzed formula" data-item-id="q_36b6849a9020578882c7" data-item-version="1" data-item-status="ready" data-key-id="o_7b69d9bbf4ad5c41b548" data-d1-id="o_fcfc4ebfd4ef567f8732" data-d2-id="o_1d274e08dee6523ca054">4 mo M, thriving, screams and strains for 10 minutes several times a day, then passes a <b>soft yellow stool</b>, normal exam &rarr; <b>Reassurance and parental education</b> &rarr; infant dyschezia resolves by about 9 months</li>
<li data-type="dx" data-d1="Infant dyschezia" data-d2="Hirschsprung disease" data-item-id="q_23282d7028d859d1b784" data-item-version="1" data-item-status="ready" data-key-id="o_7bbbd5b2e89b55d4a48e" data-d1-id="o_0d941000a4cf50f987c4" data-d2-id="o_76a1ddfbe7555ef6a996">5 mo F, passed meconium on day 1, now <b>hard pellet stools</b> every 3 days with straining since starting solids, thriving &rarr; <b>Functional constipation</b> &rarr; dietary change, then an osmotic laxative</li>
<li data-type="next" data-d1="Switch to a soy-based formula" data-d2="Stool culture and observation" data-item-id="q_e98d63aee8e255ed9204" data-item-version="1" data-item-status="ready" data-key-id="o_9ea1d92405bb51579efe" data-d1-id="o_d8b6c8d5df005b039280" data-d2-id="o_ce6ebbcf813b5d78af66">6 wk F, exclusively breastfed, thriving, <b>blood-streaked soft stools</b> for a week, comfortable and well &rarr; <b>Eliminate cow's milk and soy from the maternal diet</b> &rarr; food protein-induced allergic proctocolitis</li>
<li data-type="next" data-d1="Soy-based formula" data-d2="Colonoscopy with biopsy" data-item-id="q_e5157c51f1c8578598b8" data-item-version="1" data-item-status="ready" data-key-id="o_b9014676497a53678d74" data-d1-id="o_1ef61b6ed4e150e1aed5" data-d2-id="o_ca1b693067bd5669bf5a">3 mo M on cow's milk formula, well-appearing, gaining weight, blood streaks and mucus in soft stools &rarr; <b>Extensively hydrolyzed formula</b> &rarr; soy cross-reacts, so it is not the substitute</li>
<li data-type="avoid" data-d1="Continue breastfeeding with maternal dairy and soy elimination" data-d2="Extensively hydrolyzed formula if maternal elimination fails" data-item-id="q_6cd50edeb7305d6db5b5" data-item-version="1" data-item-status="ready" data-key-id="o_c51baf8548e957aaa7cb" data-d1-id="o_f3f4199f536950ca8044" data-d2-id="o_c111f71c685a500d9b40">2 mo F, breastfed, with food protein-induced allergic proctocolitis; the recommendation to avoid &rarr; <b>Stop breastfeeding and start a soy-based formula</b> &rarr; soy protein triggers the same reaction and breastfeeding need not stop</li>
<li data-type="next" data-d1="Intramuscular epinephrine" data-d2="Skin-prick testing to cow's milk" data-item-id="q_20fd5271853554adbc60" data-item-version="1" data-item-status="ready" data-key-id="o_a44aa190c4d25d479581" data-d1-id="o_ddf8da1238dc52e0aea4" data-d2-id="o_3910bea0536c5a4cb2a5">7 mo M, 2 hours after his first cow's-milk formula, <b>repetitive profuse vomiting</b>, pale, limp and lethargic, no urticaria or wheeze &rarr; <b>Intravenous fluid resuscitation</b> &rarr; food protein-induced enterocolitis syndrome is non-IgE, so epinephrine does nothing</li>
<li data-type="next" data-d1="Oral antihistamine and observation" data-d2="Intravenous fluid bolus" data-item-id="q_ff5279d9b8e05457b87d" data-item-version="1" data-item-status="ready" data-key-id="o_ba48054e636f5310bc94" data-d1-id="o_80dfec59cd325f368104" data-d2-id="o_422c2ac6d9f55c768101">9 mo F, <b>hives and wheezing within 15 minutes</b> of her first scrambled egg &rarr; <b>Intramuscular epinephrine</b> &rarr; IgE-mediated food allergy, strict avoidance and allergist referral</li>
<li data-type="next" data-d1="Stool ova and parasite testing" data-d2="Empiric metronidazole" data-item-id="q_cd73bba1f005500086c8" data-item-version="1" data-item-status="ready" data-key-id="o_93451d67a0c1512bae30" data-d1-id="o_e4feda877bb95148a1e6" data-d2-id="o_aecfcdd63aac54dbbbc6">6 yo M, viral gastroenteritis 10 days ago that was improving, now <b>watery diarrhea and bloating since milk was reintroduced</b>, afebrile, no vomiting &rarr; <b>Temporary lactose avoidance, then reintroduce</b> &rarr; secondary lactase deficiency needs no workup</li>
<li data-type="mech" data-d1="Giardia lamblia infection" data-d2="Clostridioides difficile colitis" data-item-id="q_236e169370a25d0695a7" data-item-version="1" data-item-status="ready" data-key-id="o_34dc8f5766e95edb8dd6" data-d1-id="o_adc4de6712645548abdc" data-d2-id="o_74128121142a55b6bb89">5 yo F, diarrhea after a resolving gastroenteritis that <b>stops when she fasts</b>, acidic stool pH, raised stool osmotic gap &rarr; <b>Transient loss of brush-border lactase</b> &rarr; colonic bacteria ferment the unabsorbed lactose</li>
<li data-type="next" data-d1="Immediate exploratory laparotomy" data-d2="Continue breast milk feeds and observe" data-item-id="q_2c51038d3635532fa9f5" data-item-version="1" data-item-status="ready" data-key-id="o_8ead63eeccb0551e88a4" data-d1-id="o_14b069be35dc5826badd" data-d2-id="o_77b2cacb83de57118ad2">5-day-old born at 32 weeks, bilious and coffee-grounds emesis, distended tender abdomen, pneumatosis intestinalis on abdominal x-ray &rarr; <b>Blood cultures and empiric broad-spectrum antibiotics with bowel rest</b> &rarr; necrotizing enterocolitis</li>
</ol>
<div class="danger"><span class="lbl">Exceptions</span> The rule applies only to an infant who is <b>well-appearing and thriving</b>. Lethargy, dehydration, or profuse vomiting is FPIES; urticaria or wheeze is IgE-mediated allergy; a <b>preterm</b> infant with distension and bloody stools has necrotizing enterocolitis; a child with fever, vomiting, or weight loss after gastroenteritis does not fit secondary lactase deficiency and needs a workup. Formula changes, rectal stimulation, and laxatives are wrong for dyschezia; a laxative is right only when the stool is <b>hard</b>.</div>
<div class="pearls"><span class="lbl">Pearls</span> Dyschezia is a coordination failure: raised intra-abdominal pressure without pelvic-floor relaxation, and inadequate abdominal tone for an effective Valsalva · FPIAP is non-IgE and self-limited; the mother eliminates cow's milk <b>and</b> soy, and it resolves by about 1 year · FPIES is also non-IgE but ill-appearing: onset hours after the trigger, no urticaria, treated with fluids · Only IgE-mediated disease gets epinephrine · Secondary lactase deficiency is osmotic (stops with fasting, acidic stool, no fever); IBD also causes brush-border loss</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part II <b>Infant Feeding at Six Months</b> covers the age for starting cow's milk; this brief covers the stool effects of cow's-milk protein before that age. Part I <b>Bronchopulmonary Dysplasia</b> has the necrotizing enterocolitis item: bloody stool in an ill preemie is not proctocolitis. Ask: is the infant well-appearing, and is the stool soft? Part I <b>Constipation in a Child</b> covers the same complaint in toddlers, where the withholding cycle, not milk protein, is the cause.</div>
<div class="rule"><span class="lbl">Transferable rule</span> In a thriving child with worried parents, choose the tier from the stool, the timing after the trigger, and the child's appearance; reassure or eliminate the trigger before testing.</div>
<div class="traps"><div class="trapline"><span class="pill p-uniform">Uniform-answer doubt</span><span class="trapwhy">Reassurance feels like doing nothing, but for dyschezia every active option is a named wrong answer.</span></div><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Soy formula removes cow's milk, but soy protein cross-reacts.</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Epinephrine treats IgE-mediated food allergy; FPIES vomiting hours later is non-IgE and needs fluids.</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">A stool workup is the tier above dietary change in a well child whose diarrhea followed dairy.</span></div></div>
</div>
```

### `bs-impaction`: Fecal Impaction & Overflow Diarrhea

```html
<div class="brief bs" id="bs-impaction" data-shelf="fm" data-bp="gi">
<h4>Fecal Impaction &amp; Overflow Diarrhea</h4>
<p class="sub">Firm stool on rectal exam confirms impaction</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 77 yo F, 5 days without a bowel movement, distended abdomen, high-pitched bowel sounds, empty rectal vault, prior laparotomy &middot; <b>Q</b> &mdash; the most likely diagnosis; options spanned adhesive small bowel obstruction, fecal impaction and sigmoid volvulus</div>
<div class="dp"><span class="lbl">The decision point</span>
<p><b>Rectal examination shows firm stool in the rectal vault.</b> This confirms fecal impaction and is <b>incompatible</b> with adhesive small bowel obstruction, which gives an <b>empty</b> rectum, a distended abdomen, and high-pitched or absent bowel sounds.</p>
<p>The last bowel movement, 5 days ago, was <b>loose stool</b>. Loose stool in a constipated patient is <b>overflow diarrhea</b>: liquid stool passing around a hard impaction. It is near-pathognomonic.</p></div>
<table><caption>Stem findings → options ruled out</caption>
<thead><tr><th>Option</th><th>The sentence that kills it</th></tr></thead>
<tbody>
<tr><td><b>Adhesions</b></td><td><b>Firm stool in the rectal vault</b> (SBO empties the rectum); soft, undistended abdomen</td></tr>
<tr><td>Colon cancer</td><td>"<b>Colonoscopy 3 years ago showed no abnormalities</b>"</td></tr>
<tr><td>Diverticulitis</td><td>No fever; <b>diffuse</b>, not focal LLQ, tenderness</td></tr>
<tr><td>Ischemic bowel</td><td>No hematochezia; no AF or atherosclerotic risk factors</td></tr>
<tr><td>Volvulus</td><td><b>Soft abdomen without distension</b>; no coffee-bean film</td></tr>
</tbody>
</table>
<div class="pearls"><span class="lbl">Details that change management</span> <b>Oxybutynin</b> is an anticholinergic that slows colonic transit and is the cause here, so treatment includes addressing it. The patient's <b>warm, dry skin</b> is an anticholinergic sign. Constipating drugs: <b>anticholinergics</b> (oxybutynin, TCAs, antihistamines, antipsychotics), <b>opioids</b>, verapamil, iron, calcium, aluminum antacids, ondansetron.</div>
<table><caption>Management ladder — fecal impaction</caption>
<thead><tr><th>Tier</th><th>Intervention</th><th>Escalate when</th></tr></thead>
<tbody>
<tr><td><b>1</b></td><td><b>Enema</b> <span class="ex">(in-context: first-line)</span></td><td>Fails to clear</td></tr>
<tr><td><b>2</b></td><td>Manual disimpaction</td><td>Enema unsuccessful</td></tr>
<tr><td><b>3</b></td><td><b>Treat the cause</b> — stop or reduce the oxybutynin; then maintenance PEG, fluids, mobility</td><td>Always, after clearing</td></tr>
</tbody>
</table>
<h5>Scenario bank</h5>
<ol class="bank">
<li data-type="dx" data-d1="Fecal impaction" data-d2="Sigmoid volvulus" data-item-id="q_3d6cc290365e594cb0a9" data-item-version="1" data-item-status="ready" data-key-id="o_6ec798d45ac2576ea553" data-d1-id="o_1733b647b4715950aff7" data-d2-id="o_9cbc717b454c5794b13c"><b>77 yo F</b>, 5 days without a BM, <b>empty rectal vault</b>, distended abdomen, high-pitched bowel sounds, prior laparotomy → <b>Adhesive small bowel obstruction</b> → NG decompression + imaging</li>
<li data-type="dx" data-d1="Adhesive small bowel obstruction" data-d2="Cecal volvulus" data-item-id="q_12806db5b70e51d1b482" data-item-version="1" data-item-status="ready" data-key-id="o_040927db6a6952b49035" data-d1-id="o_9b860e7e17e7591083fd" data-d2-id="o_69380b132ddb5fd4a364"><b>77 yo F</b>, sudden severe pain, <b>distended tympanitic abdomen</b>, <b>coffee-bean sign</b> → Sigmoid volvulus → endoscopic decompression</li>
<li data-type="dx" data-d1="Ischemic colitis" data-d2="Colon cancer" data-item-id="q_e4cf89bdbce15736b1f5" data-item-version="1" data-item-status="ready" data-key-id="o_5cfcbff22962593ebade" data-d1-id="o_d03284958f81512b9f55" data-d2-id="o_560a478c1ddc5181aba5"><b>68 yo M</b>, LLQ pain with <b>fever 38.5</b> and focal tenderness → Diverticulitis → CT</li>
<li data-type="dx" data-d1="Diverticulitis" data-d2="Infectious colitis" data-item-id="q_3b8b3f6f9c405793af51" data-item-version="1" data-item-status="ready" data-key-id="o_d446a4da6a645ec995a2" data-d1-id="o_463fcea6f46b5640a5f6" data-d2-id="o_08671d0f97ad5f11a43b"><b>72 yo F with atrial fibrillation</b>, crampy pain and <b>hematochezia</b> → Ischemic colitis</li>
<li data-type="dx" data-d1="Diverticular stricture" data-d2="Chronic functional constipation" data-item-id="q_15039bd9de4559cda90f" data-item-version="1" data-item-status="ready" data-key-id="o_1b77879582ee5467a48f" data-d1-id="o_bf3d05dc23e552ca81c5" data-d2-id="o_18728c6ff5325b379900"><b>60 yo M</b>, progressive constipation with <b>iron deficiency anemia and weight loss</b>, no recent colonoscopy → Colon cancer → colonoscopy</li>
<li data-type="next" data-d1="Add senna, continue oxybutynin" data-d2="Start lubiprostone" data-item-id="q_945acc9a1c2b568197f1" data-item-version="1" data-item-status="ready" data-key-id="o_ba44f1655d4b5935826a" data-d1-id="o_c8a7b7944c3d53f4ab6b" data-d2-id="o_8aa1c8c01a765f439469"><b>77 yo F</b>, impaction cleared by enema, still constipated → <b>Stop the oxybutynin</b>, start PEG</li>
<li data-type="next" data-d1="Increase the opioid and add senna" data-d2="Start PEG alone" data-item-id="q_56636eea25ad5450a890" data-item-version="1" data-item-status="ready" data-key-id="o_33dd494f0c7459df9113" data-d1-id="o_9fc9e1ec51075039a526" data-d2-id="o_c35e3b7c720951b6968c"><b>80 yo M on chronic opioids</b>, 6 days without a BM, hard stool in the vault → Disimpaction + <b>methylnaltrexone or naloxegol</b></li>
</ol>
<div class="danger"><span class="lbl">Exceptions</span>
Impaction can sit <b>distal to</b> a second lesion, such as a slow-growing tumor or partial obstruction. Here, a <b>normal colonoscopy 3 years ago</b> and no weight loss or anemia mean no further workup is needed. If any one of these is missing, relieve the impaction and also investigate.</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Constipation in a Child</b> covers the paediatric case, where the rectal vault is empty and an anal fissure rules out the rectal route that is first-line here.</div>
<div class="rule"><span class="lbl">Transferable rule</span> Change an answer only when a new detail makes the current choice <b>impossible</b>, not when another option merely becomes plausible, and check whether the stem contains a finding that excludes the new option. Here, firm stool in the rectal vault excludes small bowel obstruction.</div>
<div class="traps"><span class="pill p-salient">Salient decoy</span></div>
</div>
```

### `bs-fat-soluble-vitamins`: Fat-Soluble Vitamin Deficiency and Toxicity

```html
<div class="brief bs" id="bs-fat-soluble-vitamins" data-shelf="fm peds" data-nid="1473995736635 1474670598330" data-bp="multi gi">
<h4>Fat-Soluble Vitamin Deficiency and Toxicity</h4>
<p class="sub">Nosebleeds and bruising in a teen with CF off his medications &middot; which vitamin does the sign name, and why is fat not being absorbed?</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 15 yo M with cystic fibrosis who has not been taking his prescribed medications; a week of congestion and low-grade fever, then several days of nosebleeds, today hard to stop; easy bruising for 2 months &middot; <b>Exam</b> &mdash; normal vital signs; active bleeding from the left naris; coarse breath sounds; no organomegaly; normal neurologic exam; scattered bruises on the extremities &middot; <b>Q</b> &mdash; the most likely cause of the bleeding; options spanned absent coagulation factor activation, increased coagulation factor consumption, increased platelet sequestration, reduced von Willebrand factor-cleaving protease activity and vitamin C malabsorption</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>Vitamins A, D, E and K need bile and pancreatic enzymes to be absorbed, so <b>any fat malabsorption</b> can deplete all four: <b>CF and other pancreatic insufficiency</b>, <b>cholestasis and biliary atresia</b>, <b>celiac disease and IBD</b>, and <b>gastric bypass</b> or short bowel. Name the deficiency by its sign: <b>night blindness and Bitot spots</b> (A), <b>rickets or osteomalacia</b> (D), <b>ataxia with loss of vibration and position sense plus hemolysis</b> (E), <b>bleeding with a long PT</b> (K). This teen with CF stopped his enzymes and vitamins; without vitamin K the liver cannot gamma-carboxylate (activate) factors II, VII, IX and X. Factor VII has the shortest half-life, so the <b>PT lengthens first</b> and the aPTT follows only when deficiency is severe; platelets stay normal.</p>
<p>The exception is <b>liver failure</b>, which also prolongs the PT but lowers <b>factor V</b>, a factor that does not need vitamin K. Scurvy also causes gum bleeding and bruising, but vitamin C is water soluble, so CF does not deplete it, and its coagulation studies are normal. Toxicity is a concern only for A and D.</p>
</div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Vitamin K deficiency pattern</b> &mdash; PT/INR prolonged first, aPTT normal or prolonged if severe, platelets normal, factor V normal &middot; <b>Liver failure pattern</b> &mdash; PT prolonged with a <b>low factor V</b> &middot; <b>Vitamin D status</b> (two threshold sets appear in questions; see the note below) &mdash; 25-hydroxyvitamin D <b>under 12 ng/mL</b> is deficiency and 12 to 20 insufficiency (IOM cutoffs), or <b>under 20</b> is deficiency and 20 to 30 insufficiency (Endocrine Society 2011 cutoffs, withdrawn in 2024)</div>
<table data-mask="4">
<caption>Fat-soluble vitamins and the bleeding mimics &mdash; the differential</caption>
<thead><tr><th>Diagnosis</th><th>Setting</th><th>Labs</th><th>The NBME tell</th></tr></thead>
<tbody>
<tr><td><b>Vitamin K deficiency</b></td><td>Fat malabsorption (CF, biliary atresia, celiac, IBD); broad-spectrum antibiotics; newborn without prophylaxis; poor intake</td><td><b>PT prolonged first</b>, aPTT if severe; platelets and factor V normal</td><td><b>Bruising, mucosal or GI bleeding</b> that corrects with vitamin K</td></tr>
<tr><td>Vitamin A deficiency</td><td>Fat malabsorption; poor intake in low-income regions</td><td>Clinical</td><td><b>Night blindness</b>, dry conjunctivae and cornea (xerophthalmia), <b>Bitot spots</b>, dry skin</td></tr>
<tr><td>Vitamin D deficiency</td><td>Fat malabsorption; breastfed infant without supplements; little sun, dark skin; vegan diet</td><td><b>25-OH vitamin D low</b>; phosphate low, alkaline phosphatase and PTH high</td><td>Children: <b>rickets</b> (bowed legs, widened wrists, rachitic rosary); adults: <b>osteomalacia</b> with bone pain and proximal weakness</td></tr>
<tr><td>Vitamin E deficiency</td><td>Cholestatic liver disease, CF, abetalipoproteinemia</td><td><b>Hemolytic</b> anemia</td><td><b>Ataxia with lost vibration and position sense</b>, peripheral neuropathy with hyporeflexia, myopathy; <b>mimics Friedreich ataxia</b></td></tr>
<tr><td>Liver failure</td><td>Cirrhosis or acute liver failure</td><td>PT prolonged, <b>factor V low</b>, albumin low</td><td>Stigmata of liver disease; the PT <b>does not correct</b> with vitamin K</td></tr>
<tr><td>Disseminated intravascular coagulation</td><td>Sepsis, trauma, malignancy</td><td><b>Platelets low</b>, PT and aPTT prolonged, fibrinogen low, D-dimer high</td><td>A <b>critically ill</b> patient oozing from lines; factors and platelets consumed together</td></tr>
<tr><td>Scurvy (vitamin C)</td><td>No fruits or vegetables: food-selective child, alcohol, severe malnutrition</td><td>Platelets, PT and aPTT <b>normal</b></td><td><b>Bleeding gums, perifollicular hemorrhages, corkscrew hairs</b></td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>PT/INR with platelet count</td><td>First</td><td><b>PT prolonged</b>, platelets normal</td><td>Vitamin K pathway (factor VII falls first); low platelets point to DIC, TTP or a big spleen</td></tr>
<tr><td>aPTT</td><td>Next</td><td>Normal, or <b>prolonged</b> when severe</td><td>Severity; both prolonged with low platelets and fibrinogen is DIC</td></tr>
<tr><td>Factor V activity</td><td>By branch</td><td><b>Normal</b> in vitamin K deficiency; <b>low</b> in liver failure</td><td>Separates vitamin K deficiency from hepatic synthetic failure</td></tr>
<tr><td>PT after vitamin K</td><td>Confirms</td><td>PT <b>corrects</b></td><td>Vitamin K deficiency; little change points to the liver</td></tr>
<tr><td>Serum 25-hydroxyvitamin D</td><td>By branch</td><td><b>Under 12 ng/mL</b> deficient, 12 to 20 insufficient; by the older Endocrine Society 2011 set, <b>under 20</b> deficient, 20 to 30 insufficient</td><td>Vitamin D deficiency with rickets or osteomalacia</td></tr>
<tr><td>Serum 1,25-dihydroxyvitamin D</td><td>Skip</td><td>Often <b>normal</b> in deficiency, because PTH drives its production</td><td>Misleading for deficiency; order it for hypercalcemia with suspected sarcoidosis or lymphoma</td></tr>
</tbody>
</table>
</div>
<div class="pearls"><span class="lbl">Vitamin D thresholds: current status (checked Sept 2026)</span> <b>In force:</b> the National Academies (IOM 2011) cutoffs, still used by the NIH Office of Dietary Supplements and matched by the 2016 Global Consensus on nutritional rickets: 25-hydroxyvitamin D <b>under 12 ng/mL (30 nmol/L)</b> is deficient, <b>12 to under 20</b> is inadequate, <b>20 or more</b> is adequate, and over 50 ng/mL carries risk of harm &middot; <b>Retired:</b> the Endocrine Society 2011 set (under 20 deficient, 21 to 29 insufficient, 30 to 100 sufficient). The Endocrine Society&#39;s 2024 guideline no longer endorses any cutoff or a target of 30, and advises <b>against routine testing</b> in healthy people &middot; <b>2024 empiric supplementation</b> above the daily allowance: ages 1 to 18, over 75, pregnancy and high-risk prediabetes; adults 19 to 74 take only the usual allowance (600 IU, 800 IU over 70) &middot; <b>Unchanged:</b> 400 IU daily for every infant in the first year, and treatment of symptomatic deficiency (rickets, osteomalacia) whatever the cutoff &middot; <b>On the exam:</b> older questions may use the 20 and 30 cutoffs; read the level against the symptoms, not against a single number</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="mech" data-src="uworld" data-nid="1473995736635 1474670598330" data-d1="Increased coagulation factor consumption" data-d2="Vitamin C malabsorption" data-item-id="q_44ce9acc258dd0603933" data-item-version="1" data-item-status="ready" data-key-id="o_9ac6a544193c6326249f" data-d1-id="o_8792fa0c6234d409848e" data-d2-id="o_9a4eb057f8fe622f0f76" data-lead-in="Which of the following is the most likely cause of this patient&#x27;s bleeding?">15 yo M with cystic fibrosis who has not been taking his prescribed medications; a week of nasal congestion and low-grade fever, then several days of nosebleeds that are now hard to stop; easy bruising for 2 months; normal vital signs; active bleeding from the left naris; coarse breath sounds; no organomegaly; normal neurologic exam; scattered bruises on the arms and legs &rarr; <b>Absent coagulation factor activation</b> &rarr; vitamin K deficiency from pancreatic insufficiency; the PT lengthens first; give vitamin K</li>
<li data-type="test" data-src="authored" data-d1="Factor VII activity" data-d2="Mixing study" data-item-id="q_0d9d197ce96a29cbe062" data-item-version="1" data-item-status="ready" data-key-id="o_69b5c0e9f43383b9ab51" data-d1-id="o_7a95e5a82a2474754712" data-d2-id="o_6d78e85e07a216a37c1a" data-lead-in="Which of the following laboratory studies best distinguishes vitamin K deficiency from hepatic synthetic failure in this patient?">62 yo M with alcohol-related cirrhosis admitted with pneumonia; 10 days of broad-spectrum antibiotics and little oral intake; new oozing from IV sites; INR 2.6, aPTT mildly prolonged, platelets 140,000 &rarr; <b>Factor V activity</b> &rarr; normal factor V points to vitamin K deficiency; low factor V points to hepatic synthetic failure</li>
<li data-type="next" data-src="authored" data-d1="Oral vitamin K with a repeat PT in 1 week" data-d2="Factor VIII concentrate" data-item-id="q_d260ba614f8b376b52b7" data-item-version="1" data-item-status="ready" data-key-id="o_836dedfc844f96bb87be" data-d1-id="o_5ee29034d75729b34027" data-d2-id="o_266074933ddc91cc4b90">4-week-old M born at home, exclusively breastfed, whose parents declined all newborn injections; oozing from the circumcision site and a large scalp bruise; well-appearing; platelets normal; PT markedly prolonged and aPTT prolonged &rarr; <b>Parenteral vitamin K</b> &rarr; vitamin K deficiency bleeding; add fresh frozen plasma for serious bleeding</li>
<li data-type="dx" data-src="authored" data-d1="Vitamin B12 deficiency" data-d2="Friedreich ataxia" data-item-id="q_afca5a6bc917caadc4ec" data-item-version="1" data-item-status="ready" data-key-id="o_3c5549467020c802d41f" data-d1-id="o_3fc30bff8dc6c638c80a" data-d2-id="o_24fb7be5ed6b2a2984d1">14 yo F with cystic fibrosis and poor adherence to pancreatic enzymes; 6 months of clumsiness and frequent falls; wide-based gait, positive Romberg sign, lost vibration and position sense in the feet, absent ankle reflexes; hemoglobin 10.1, MCV 88, reticulocytes elevated; echocardiogram normal &rarr; <b>Vitamin E deficiency</b> &rarr; dorsal column and cerebellar damage with hemolysis; replace vitamin E</li>
<li data-type="test" data-src="authored" data-d1="Serum 1,25-dihydroxyvitamin D" data-d2="Serum ionized calcium" data-item-id="q_f2bd6151932e23a717e6" data-item-version="1" data-item-status="ready" data-key-id="o_c52c401cb0769d894434" data-d1-id="o_b35c77194fcc2d293d55" data-d2-id="o_7cecd0d330bbb90d47be" data-lead-in="Which of the following laboratory studies is most likely to confirm the cause?">18 mo M, exclusively breastfed with no supplements, dark skin, rarely outdoors; late walking; bowed legs, widened wrists and beading along the costochondral junctions; calcium low-normal, phosphate low, alkaline phosphatase high &rarr; <b>Serum 25-hydroxyvitamin D</b> &rarr; nutritional rickets; vitamin D replacement</li>
<li data-type="next" data-src="authored" data-d1="Vitamin D 1,000 IU daily" data-d2="Calcitriol daily" data-item-id="q_4c902ebf73a699b6fab7" data-item-version="1" data-item-status="ready" data-key-id="o_3df2cfa962e682e8b95c" data-d1-id="o_8a630ca7bf2adb1192fd" data-d2-id="o_50e5fdfb780199ca2af7">74 yo F in a nursing home who rarely goes outside; 3 months of aching hips and thighs and trouble rising from a chair; tender bones; 25-hydroxyvitamin D 8 ng/mL; calcium normal; kidney function normal &rarr; <b>Vitamin D 50,000 IU weekly for 8 weeks</b> &rarr; osteomalacia from vitamin D deficiency; then 800 to 1,000 IU daily and recheck the level in 3 to 4 months</li>
<li data-type="mech" data-src="authored" data-d1="Excess vitamin D intake" data-d2="Obesity-related intracranial hypertension" data-item-id="q_6a602762b258ee5a7b37" data-item-version="1" data-item-status="ready" data-key-id="o_203416ef7827fd4767b2" data-d1-id="o_bf385c6fedc7325e7fd0" data-d2-id="o_9f88deb0084fbd481907" data-lead-in="Which of the following is the most likely cause of this patient&#x27;s findings?">23 yo F with a normal BMI who has taken several high-dose vitamin A supplements for acne for 4 months; daily headaches and blurred vision; bilateral papilledema; brain MRI normal; lumbar puncture opening pressure high with normal fluid &rarr; <b>Excess vitamin A intake</b> &rarr; pseudotumor cerebri from vitamin A toxicity; stop the supplements and check for pregnancy</li>
<li data-type="dx" data-src="authored" data-d1="Vitamin B12 deficiency" data-d2="Vitamin E deficiency" data-item-id="q_0cf7d03ba2445d63b0d3" data-item-version="1" data-item-status="ready" data-key-id="o_4e647e6f2b252e4bc11a" data-d1-id="o_34f64a92ac763d0aee28" data-d2-id="o_cfbdad19a2e69bae7272">47 yo F with a Roux-en-Y gastric bypass 6 years ago who stopped her supplements 2 years ago; 5 months of worsening unsteadiness and numb feet; hair has become thin and lighter in color; broad-based gait, positive Romberg sign, lost vibration and position sense in the feet, mild leg stiffness with brisk knee reflexes; hemoglobin 10.6 g/dL, MCV 93; serum B12 and methylmalonic acid normal &rarr; <b>Copper deficiency</b> &rarr; myelopathy that mimics subacute combined degeneration of B12 deficiency; replace copper and resume supplements</li>
<li data-type="mech" data-src="authored" data-d1="Impaired renal 1-alpha-hydroxylation of vitamin D" data-d2="Impaired hepatic 25-hydroxylation of vitamin D" data-item-id="q_5842ccc08d0168f188be" data-item-version="1" data-item-status="ready" data-key-id="o_a52bdb209accc8d3d60d" data-d1-id="o_e54533c9e26477153c42" data-d2-id="o_876310933bd152ac636c" data-lead-in="Which of the following is the most likely mechanism of this patient&#x27;s condition?">44 yo F with long-standing epilepsy controlled on phenytoin; walks outdoors daily and drinks milk; 4 months of aching hips and thighs and trouble climbing stairs; tender pelvic bones; calcium low-normal, phosphate low, alkaline phosphatase and PTH high, 25-hydroxyvitamin D 9 ng/mL; creatinine, albumin and liver enzymes normal &rarr; <b>Accelerated hepatic breakdown of vitamin D</b> &rarr; drug-induced vitamin D deficiency with osteomalacia; carbamazepine, isoniazid and rifampin do the same; replace vitamin D</li>
</ol>
<div class="danger"><span class="lbl">Management</span> <b>Vitamin K deficiency</b> &mdash; vitamin K, parenteral for severe coagulopathy; fresh frozen plasma as well for serious bleeding; in CF, restart pancreatic enzymes and fat-soluble vitamin supplements &middot; <b>Newborn</b> &mdash; one intramuscular dose of vitamin K at birth prevents vitamin K deficiency bleeding; breast milk is low in vitamin K &middot; <b>Vitamin D deficiency</b> &mdash; 50,000 IU weekly for 8 weeks, then 800 to 1,000 IU daily; recheck 25-OH vitamin D in 3 to 4 months, aiming for 20 ng/mL or more &middot; <b>Route</b> &mdash; oral replacement for poor intake; parenteral when malabsorption or bypass surgery prevents absorption</div>
<div class="pearls"><span class="lbl">Toxicity: only A and D</span> <b>Vitamin A</b>, from excess liver or supplements or from retinoids &mdash; <b>pseudotumor cerebri</b> (headache, papilledema, high opening pressure), bone pain and fractures, hepatomegaly, dry skin and alopecia, and <b>teratogenicity</b>, the reason retinoids such as isotretinoin need pregnancy testing and contraception &middot; <b>Vitamin D</b> &mdash; <b>hypercalcemia</b>, from massive supplement overdose or from <b>granulomatous disease such as sarcoidosis</b>, where macrophages make 1,25-dihydroxyvitamin D without PTH control</div>
<div class="pearls"><span class="lbl">Vitamin D: pathway and causes</span> Skin makes D3 from 7-dehydrocholesterol with UV light (diet adds D2 and D3) &rarr; <b>liver 25-hydroxylase</b> makes 25-OH D, the form measured &rarr; <b>kidney 1-alpha-hydroxylase</b>, driven by <b>PTH</b> and suppressed by high calcium, makes active 1,25-(OH)2 D, which raises intestinal calcium absorption (its main action) and renal calcium and phosphate reabsorption, mineralizes bone and suppresses PTH &middot; <b>Causes of deficiency</b> &mdash; poor intake (milk avoidance, lactose intolerance, unfortified vegan diet); malabsorption (Crohn disease, celiac disease, gastrectomy or bariatric surgery); little sun (high latitude, dark skin, indoor life, nursing home, night work); obesity and older age; <b>CKD and chronic liver disease</b>; <b>drugs that speed its breakdown</b>: phenytoin, carbamazepine, isoniazid, rifampin &middot; Most deficiency is silent or causes vague aches; it surfaces as low bone density, fracture or osteomalacia</div>
<div class="pearls"><span class="lbl">After gastric bypass</span> Several deficiencies overlap, so supplements and periodic levels are lifelong: <b>B12</b> (macrocytic anemia, neuropathy, cognitive change) &middot; <b>A</b> (night blindness), <b>D and calcium</b> (bone loss with <b>secondary hyperparathyroidism</b>), <b>K</b> (coagulopathy) &middot; <b>iron</b> (anemia; the duodenum is bypassed) &middot; <b>zinc</b> (alopecia, rash, night blindness) &middot; <b>copper</b> (ataxia, weakness and neuropathy that <b>mimic B12 deficiency</b>, with fragile, depigmented hair; check copper when B12 and methylmalonic acid are normal) &middot; <b>folate</b> (macrocytic anemia) &middot; <b>thiamine</b> (Wernicke, especially with <b>intractable vomiting</b>)</div>
<div class="pearls"><span class="lbl">Pearls</span> One malabsorption cause usually depletes several fat-soluble vitamins at once, so a CF or cholestatic patient with one deficiency needs all four checked or replaced &middot; Vitamin A supplementation is standard in <b>severe measles</b> and in regions where deficiency is endemic &middot; Ask about antibiotics: broad-spectrum courses cut gut bacterial production of vitamin K &middot; <b>Half-lives</b> &mdash; factor <b>VII shortest</b> (about 6 h), then IX, X and II (about 60 h); anticoagulant <b>protein C</b> is also short (about 8 h), so starting warfarin lowers protein C first and briefly makes blood <b>hypercoagulable</b>, the reason for heparin bridging and the cause of warfarin skin necrosis</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Recurrent Sinopulmonary Infection</b> covers the diagnosis of cystic fibrosis: is growth poor with greasy stools, and is the sweat chloride high? Part I <b>Hemophilia A Inhibitor</b> covers the bleeding-pattern-to-lab table: is the PT or the aPTT long, and are platelets normal? Part I <b>Night Blindness</b> covers vitamin A against retinitis pigmentosa: is the front of the eye normal? Part I <b>Hypercalcemia Workup</b> covers vitamin D excess and sarcoidosis: is the 25-OH or the 1,25-OH vitamin D high? Aquifer <b>Infant Feeding at Six Months</b> covers vitamin D 400 IU for breastfed infants. Part II <b>Exanthems in a Child</b> covers measles. Part II <b>Water-Soluble Vitamin Deficiency</b> covers scurvy: are the coagulation studies normal? Part I <b>Headache in a Child: What Earns Imaging</b> covers the papilledema workup, MRI with MR venography and then LP, and the other drugs that raise intracranial pressure; ask: is the papilledema bilateral with full visual fields?</div>
<div class="rule"><span class="lbl">Transferable rule</span> Name a fat-soluble deficiency by its sign (eye, bone, dorsal columns with hemolysis, or bleeding), then find why fat is not being absorbed; for bleeding with normal platelets, a long PT that corrects with vitamin K is vitamin K deficiency, and a low factor V moves it to the liver.</div>
<div class="traps"><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Increased coagulation factor consumption: the recent febrile illness suggests sepsis and DIC, but DIC needs a critically ill patient with low platelets, and his vital signs are normal.</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Increased platelet sequestration: CF liver disease can enlarge the spleen, but there is no organomegaly, and sequestration lowers platelets without lengthening the PT.</span></div><div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Reduced von Willebrand factor-cleaving protease activity: TTP is acute, with thrombocytopenia, hemolysis and neurologic signs; his neurologic exam is normal and the bleeding is slow.</span></div><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Vitamin C malabsorption: the right class, a vitamin, but the wrong member; vitamin C is water soluble, so pancreatic insufficiency does not deplete it, and scurvy leaves the PT normal.</span></div></div>
</div>
```

### `bs-water-soluble-vitamins`: Water-Soluble Vitamin Deficiency

```html
<div class="brief bs" id="bs-water-soluble-vitamins" data-shelf="fm peds" data-bp="multi gi">
<h4>Water-Soluble Vitamin Deficiency</h4>
<p class="sub">Confusion and ataxia in heavy drinking, a sun-exposed rash, bleeding gums with normal clotting &middot; UWorld library &middot; which organs are involved, and what is the patient drinking, taking or not eating?</p>
<div class="dp"><span class="lbl">The decision point</span>
<p>The body stores little of the B vitamins or vitamin C (B12 is the exception), so deficiency follows <b>chronic alcohol use</b>, poor intake, malabsorption (bypass, short bowel, Crohn disease) or a <b>drug</b>. The <b>organ pattern</b> identifies the vitamin: <b>brain, eyes and gait, or the heart</b> is B1; <b>photosensitive dermatitis with diarrhea and dementia</b> is B3; <b>neuropathy on isoniazid</b> is B6; <b>megaloblastic anemia</b> is B9 or B12, and a <b>high methylmalonic acid with neurologic signs</b> separates B12; <b>bleeding gums and perifollicular hemorrhages with normal platelets, PT and aPTT</b> is C.</p>
<p>In a malnourished or alcohol-using patient, give <b>IV thiamine before or with glucose</b>, because a glucose load can precipitate or worsen Wernicke encephalopathy. Do not treat a megaloblastic anemia with <b>folate alone</b> until B12 is known: folate corrects the anemia but not the neurologic damage of B12 deficiency, so give both when the cause is unclear.</p>
</div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Serum B12</b> &mdash; under 200 pg/mL is deficient, over 300 is sufficient, 200 to 300 needs a methylmalonic acid level &middot; <b>Methylmalonic acid</b> &mdash; high in B12 deficiency, normal in folate deficiency &middot; <b>Homocysteine</b> &mdash; high in both, so it does not separate them &middot; <b>Megaloblastic anemia</b> &mdash; MCV over 100 with hypersegmented neutrophils</div>
<table data-mask="4">
<caption>Water-soluble vitamins &mdash; the organ pattern</caption>
<thead><tr><th>Vitamin</th><th>Who gets it</th><th>Labs and separating clue</th><th>The NBME tell</th></tr></thead>
<tbody>
<tr><td><b>B1 thiamine</b></td><td>Alcohol use (most common), malnutrition including <b>anorexia nervosa</b>, <b>hyperemesis gravidarum</b>, bariatric surgery with vomiting</td><td>Clinical; treat without waiting for a level</td><td><b>Wernicke</b>: confusion, ophthalmoplegia (<b>horizontal nystagmus, bilateral abducens palsy</b>), gait ataxia; <b>Korsakoff</b>: anterograde and retrograde amnesia with confabulation and <b>no insight</b>, older long-term memories relatively preserved; dry beriberi: symmetric sensorimotor neuropathy; wet beriberi: high-output heart failure with edema</td></tr>
<tr><td>B3 niacin</td><td>Alcohol use, anorexia, Crohn disease, Hartnup disease, carcinoid syndrome (tryptophan diverted to serotonin)</td><td>Clinical</td><td><b>Pellagra</b>: photosensitive dermatitis on the neck (Casal necklace), hands and face, with diarrhea and dementia</td></tr>
<tr><td>B6 pyridoxine</td><td><b>Isoniazid</b>, alcohol use</td><td>Microcytic (sideroblastic) anemia</td><td><b>Peripheral neuropathy</b>, cheilitis, stomatitis; seizures when severe</td></tr>
<tr><td>B9 folate</td><td>Alcohol use, pregnancy, hemolysis, poor intake; <b>folate antagonists</b>: methotrexate, trimethoprim, triamterene, phenytoin, valproate, carbamazepine</td><td>Megaloblastic; homocysteine high, <b>MMA normal</b></td><td>Megaloblastic anemia with a <b>normal neurologic exam</b>; <b>neural tube defects</b> in pregnancy</td></tr>
<tr><td>B12 cobalamin</td><td>Pernicious anemia, atrophic gastritis, vegan diet, metformin, PPIs, ileal resection or Crohn disease, fish tapeworm</td><td>Megaloblastic; homocysteine and <b>MMA both high</b></td><td><b>Neurologic disease</b>: lost vibration and position sense with spastic weakness (subacute combined degeneration of the dorsal columns and corticospinal tracts), neuropathy, dementia</td></tr>
<tr><td>C ascorbic acid</td><td>No fruits or vegetables: food-selective child (autism), alcohol use, severe malnutrition</td><td>Platelets, PT and aPTT <b>normal</b>; anemia</td><td><b>Swollen bleeding gums, perifollicular hemorrhages, corkscrew hairs</b>, poor wound healing; a limp from bleeding under the periosteum in children</td></tr>
</tbody>
</table>
<div class="tw">
<table data-mask="4"><caption>Diagnostic workup</caption>
<thead><tr><th>Test</th><th>Order</th><th>Result</th><th>What it points to</th></tr></thead>
<tbody>
<tr><td>CBC with MCV and smear</td><td>First</td><td>MCV <b>over 100</b>, hypersegmented neutrophils</td><td>Megaloblastic anemia: B12 or folate</td></tr>
<tr><td>Serum B12 and folate</td><td>Next</td><td>B12 <b>under 200</b> deficient; over 300 sufficient</td><td>Names the vitamin when the level is clear</td></tr>
<tr><td>Methylmalonic acid</td><td>By branch</td><td>B12 200 to 300 with <b>high MMA</b></td><td>B12 deficiency; a normal MMA with high homocysteine is folate</td></tr>
<tr><td>Intrinsic factor antibodies</td><td>Cause</td><td><b>Positive</b></td><td>Pernicious anemia; lifelong B12</td></tr>
<tr><td>Thiamine level before treating suspected Wernicke</td><td>Skip</td><td>Result is not back in time</td><td>Give IV thiamine on clinical suspicion</td></tr>
</tbody>
</table>
</div>
<h5 class="authored-hdr">Scenario bank</h5>
<ol class="bank authored">
<li data-type="next" data-src="authored" data-d1="Intravenous dextrose, then thiamine once glucose is normal" data-d2="Oral thiamine and a multivitamin at discharge" data-item-id="q_0eadfa04551ec5c46fda" data-item-version="1" data-item-status="ready" data-key-id="o_752a9489c538c21e83f5" data-d1-id="o_e8c5e7e6af0f16efcb0d" data-d2-id="o_ef1db967c641f5184a8e">52 yo M with heavy daily alcohol use brought in confused and unsteady; horizontal nystagmus and weak lateral gaze in both eyes; wide-based gait; fingerstick glucose 58 mg/dL &rarr; <b>Intravenous thiamine before or with dextrose</b> &rarr; Wernicke encephalopathy</li>
<li data-type="dx" data-src="authored" data-d1="Wernicke encephalopathy" data-d2="Hepatic encephalopathy" data-item-id="q_da619dfb00c0da19f4b8" data-item-version="1" data-item-status="ready" data-key-id="o_16f6600550b593cdc473" data-d1-id="o_74936245d373a1355478" data-d2-id="o_652cf5f15a93a90648b6">61 yo M with long-standing alcohol use disorder, treated for Wernicke encephalopathy 3 months ago; now alert and attentive with normal eye movements; cannot form new memories and gives detailed invented accounts of his recent days &rarr; <b>Korsakoff syndrome</b> &rarr; mammillary body damage from thiamine deficiency; often permanent</li>
<li data-type="dx" data-src="authored" data-d1="Porphyria cutanea tarda" data-d2="Thiamine deficiency" data-item-id="q_bf2099995e856c9de8f7" data-item-version="1" data-item-status="ready" data-key-id="o_ea324cba6f1c6d9ce2ab" data-d1-id="o_231abb9429c5ed5ae508" data-d2-id="o_bc2a5e67f8d3fd5b985b">47 yo M with alcohol use disorder; 2 months of watery diarrhea and worsening forgetfulness; a sharply bordered, scaly, darkened rash on the backs of the hands, the face and a band around the neck, all sun-exposed; no blisters &rarr; <b>Niacin deficiency</b> &rarr; pellagra: dermatitis, diarrhea, dementia</li>
<li data-type="next" data-src="authored" data-d1="Stop isoniazid and switch to rifampin" data-d2="Start gabapentin" data-item-id="q_73f9e909f9563f899da6" data-item-version="1" data-item-status="ready" data-key-id="o_da6ccc69b7a630c44a2b" data-d1-id="o_1797337b4b9b129dafc6" data-d2-id="o_534798a35ea58a267892">38 yo F taking isoniazid alone for latent tuberculosis for 3 months with no other supplement; 3 weeks of burning and tingling in both feet; decreased pinprick sensation in a stocking distribution; liver enzymes normal &rarr; <b>Add pyridoxine</b> &rarr; isoniazid-induced B6 deficiency neuropathy</li>
<li data-type="test" data-src="authored" data-d1="Serum homocysteine" data-d2="Intrinsic factor antibodies" data-item-id="q_2686a6b270e8d061a995" data-item-version="1" data-item-status="ready" data-key-id="o_113eeeaadb100202de6f" data-d1-id="o_f58710dc5a1d3dede42e" data-d2-id="o_695c982f4a60f1fe7a68" data-lead-in="Which of the following is the most appropriate next test?">67 yo F with type 2 diabetes on metformin; fatigue and mild numbness of the feet; hemoglobin 10.8, MCV 108, hypersegmented neutrophils; serum B12 240 pg/mL; folate normal &rarr; <b>Serum methylmalonic acid</b> &rarr; a high level confirms B12 deficiency</li>
<li data-type="next" data-src="authored" data-d1="Intramuscular vitamin B12" data-d2="Bone marrow biopsy" data-item-id="q_74d52121bbf45a313b82" data-item-version="1" data-item-status="ready" data-key-id="o_50f5eb88f4e47791143b" data-d1-id="o_cb1c32f8453aac055be9" data-d2-id="o_c558d4f6ba8af8ab783d">58 yo F with rheumatoid arthritis on weekly methotrexate who stopped taking her folic acid; fatigue; hemoglobin 9.9, MCV 112, hypersegmented neutrophils; serum B12 450 pg/mL; neurologic exam normal &rarr; <b>Resume folic acid</b> &rarr; folate deficiency from a dihydrofolate reductase inhibitor</li>
<li data-type="dx" data-src="authored" data-d1="Acute lymphoblastic leukemia" data-d2="Vitamin K deficiency" data-item-id="q_cce9bc019dfd2c97f4cc" data-item-version="1" data-item-status="ready" data-key-id="o_07e7ab32f7b23fc54996" data-d1-id="o_1de8b14d2a46011cb81b" data-d2-id="o_8cdd8581860923c60df4">6 yo M with autism who eats only white bread, crackers and cheese; 3 weeks of refusing to walk because of leg pain; swollen, bleeding gums; perifollicular hemorrhages and coiled hairs on the legs; hemoglobin 10.2, white cells and platelets normal, PT and aPTT normal &rarr; <b>Vitamin C deficiency</b> &rarr; scurvy from impaired collagen hydroxylation; oral vitamin C</li>
<li data-type="screen" data-src="authored" data-d1="Folic acid 0.4 mg daily starting before conception" data-d2="Folic acid 4 mg daily starting at the first prenatal visit" data-item-id="q_6f7072ac79fb1914531c" data-item-version="1" data-item-status="ready" data-key-id="o_13d81828a46988a4abe7" data-d1-id="o_2929c78e46bb48fa2355" data-d2-id="o_4cd1c8bd190eddb6402f">27 yo F planning a pregnancy whose first pregnancy was affected by anencephaly; healthy, takes no medications, eats a varied diet &rarr; <b>Folic acid 4 mg daily starting before conception</b> &rarr; high-risk dose after a prior neural tube defect</li>
<li data-type="dx" data-src="authored" data-d1="Osmotic demyelination syndrome" data-d2="Cerebral venous sinus thrombosis" data-item-id="q_4a7266c174aa84c02fd6" data-item-version="1" data-item-status="ready" data-key-id="o_14c417115906327ca4a6" data-d1-id="o_734fc904704f12edd1c4" data-d2-id="o_7fa947a8db0bd7f050be">24 yo F at 11 weeks&#x27; gestation with 4 weeks of vomiting that has kept down almost nothing, a 6 kg weight loss and two emergency visits for dextrose-containing IV fluids; now confused and unable to walk without help; horizontal nystagmus and weak lateral gaze in both eyes; blood pressure 104/66 mm Hg; no headache or papilledema; serum sodium 134 mEq/L, unchanged over the past week &rarr; <b>Wernicke encephalopathy</b> &rarr; thiamine deficiency from hyperemesis gravidarum; IV thiamine before further dextrose</li>
</ol>
<div class="danger"><span class="lbl">Management</span> <b>Thiamine</b> &mdash; IV, before or with any glucose, in Wernicke encephalopathy or any malnourished drinker &middot; <b>B12</b> &mdash; intramuscular or high-dose oral B12; with neurologic signs, never folate alone &middot; <b>Folate</b> &mdash; oral folic acid, with the B12 level known; folic acid alongside methotrexate &middot; <b>Pregnancy</b> &mdash; folic acid 0.4 mg daily for anyone who could become pregnant, 4 mg daily after a prior neural tube defect pregnancy, starting before conception &middot; <b>B6</b> &mdash; pyridoxine with isoniazid &middot; <b>Vitamin C</b> &mdash; oral vitamin C; symptoms improve within days to weeks &middot; <b>Route</b> &mdash; oral for poor intake; parenteral for malabsorption or bypass</div>
<div class="pearls"><span class="lbl">Mnemonics</span> <b>Pellagra, the 4 Ds</b> &mdash; dermatitis, diarrhea, dementia, death &middot; <b>Wernicke triad</b> &mdash; confusion, ophthalmoplegia, ataxia; often incomplete, so one or two features in a drinker is enough to treat; add anterograde amnesia with confabulation and it has become <b>Korsakoff</b> (mammillary bodies), which is often permanent</div>
<div class="pearls"><span class="lbl">Pearls</span> <b>B2 riboflavin</b> &mdash; angular cheilitis, stomatitis, glossitis, normocytic anemia &middot; <b>B5 pantothenic acid</b> &mdash; rare; distal paresthesias &middot; <b>B7 biotin</b> &mdash; rare; raw egg whites; alopecia and dermatitis &middot; Pellagra's rash is photosensitive like porphyria cutanea tarda, but PCT blisters on the backs of the hands and brings no diarrhea or dementia &middot; B12 neurologic signs can appear before the anemia &middot; Scurvy in a child who refuses to walk mimics leukemia or abuse; normal counts and normal coagulation studies with gum disease point to the diet</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>The Vegan Diet</b> covers B12 against folate in a plant diet: is there a fortified or animal source of B12? Part I <b>Marfanoid Habitus: Homocystinuria</b> covers inherited high homocysteine, treated with B6, folate and B12. Part I <b>Teratogenic Exposures</b> covers the folate-antagonist antiepileptics and neural tube defects. Part I <b>Tuberculosis</b> covers isoniazid with B6. Part II <b>Fat-Soluble Vitamin Deficiency and Toxicity</b> covers bleeding with a long PT: are the coagulation studies abnormal (K) or normal (C)?</div>
<div class="rule"><span class="lbl">Transferable rule</span> Read the organ pattern first (brain, eyes and heart; sun-exposed skin with diarrhea; neuropathy on a drug; megaloblastic blood; bleeding gums with normal clotting), then ask what the patient drinks, takes or does not eat; give thiamine before glucose, and settle B12 (with MMA when the level is 200 to 300) before giving folate alone.</div>
<div class="traps"><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Dextrose first in a confused, hypoglycemic drinker: the glucose is needed, but thiamine goes in before or with it.</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Homocysteine to separate B12 from folate: it is truly high in B12 deficiency, but it is high in folate deficiency too; only MMA separates them.</span></div><div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Folic acid for a megaloblastic anemia with numb feet: the blood improves, but the neurologic signs mark B12, and folate alone lets them progress.</span></div><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Vitamin K for bleeding gums and bruises: the right class, a vitamin, but scurvy leaves the PT normal, so vitamin C is the member.</span></div></div>
</div>
```
