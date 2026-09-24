# Voice packet 3 of 5 (s29, gi): liver-preg, fap, peds-constipation, bs-water-soluble-vitamins

**Instructions.** Everything you need is in this packet. Do not open index.html, the skill files or other packets. Write your edits to `repair/s29/04_voice_3.json`, run `python3 tools/verify_edits.py repair/s29/04_voice_3.json scratch/s29_base.html --voice` from the workspace folder (Step2Haki/workspace) and loop until it prints PASS. Then reply with the 3 to 5 line report the rules ask for.

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
- every `<b>` term (you may reword around it, not drop or rename it);
- standard clinical phrases such as "until proven otherwise";
- the "·" row separators and "`<b>Term</b> — definition`" structure where they already exist (that " — " is structural, the only em dash allowed);
- `.rule` starts with its existing label markup.

**Model (approved by Jonathan):**
- Before: The phone call is the decoy and the urine is the decider. Every option is on the newborn screen, so a positive screen eliminates nothing. What separates them is that this infant has conjugated hyperbilirubinemia, a large liver, and a non-glucose reducing sugar in the urine after ten days of milk feeds. That triad is galactose-1-phosphate accumulating in a GALT-deficient liver: classic galactosemia. The fever is not incidental. Galactosemia predisposes to Escherichia coli sepsis, and a febrile 10-day-old is septic until cultured — the sepsis workup runs in parallel with the metabolic answer, never after it.
- After: Conjugated hyperbilirubinemia, a large liver, and a non-glucose reducing sugar in the urine after ten days of milk feeds indicate classic galactosemia (GALT deficiency; galactose-1-phosphate accumulates in the liver). Galactosemia predisposes to Escherichia coli sepsis, so start the sepsis workup and antibiotics while stopping lactose.
- Subtitle before: The screen names the panel, the presentation names the disease · handoff · conjugated, big liver, reducing sugar
- Subtitle after: Sick neonate with a positive newborn screen · conjugated jaundice, hepatomegaly, urine reducing sugar

If a block is already plain, leave it. If you are unsure a rewrite keeps the meaning, leave it and list it.

**Output:** edits JSON (replace ops, anchors unique within the brief) and a report of 3 to 5 lines: blocks changed, blocks left, anything uncertain.

## Edit format (replace only)
One JSON file: `{"edits": [op, op, ...]}`, replace ops only, applied in order:

```json
{"op": "replace", "brief": "<brief id>", "find": "<verbatim snippet of the brief HTML>", "with": "<rewritten HTML>", "note": "why"}
```

- `find` is copied verbatim from the brief HTML below, entities included (`&amp;`, `&middot;`, `&gt;`, `&lt;`), and occurs exactly once inside that brief. Lengthen it with neighbouring text until it is unique.
- `find` must lie inside `.dp`, `.rule`, `.pearls`, `.danger`, `.traps` or the first segment of `p.sub` (before the first `·`). Never inside `.vignette`, a table, `.crit` or the question bank (`ol.bank`); the verifier rejects those.
- Keep every `<b>` term, every number and every `<span class="lbl">...</span>` label exactly; the only em dash allowed is the structural `<b>Term</b> — definition`.
- One op per block is easiest: `find` = the block's prose (not its opening `<div ...>` tag), `with` = the rewrite.

## Briefs (4): current HTML
### `liver-preg`: Liver Disease in Pregnancy

```html
<div class="brief" id="liver-preg" data-shelf="fm" data-bp="preg gi">
<h4>Liver Disease in Pregnancy</h4>
<p class="sub">Trimester decides everything</p>
<div class="dp"><span class="lbl">The decision point</span>
<p><b>Acute fatty liver of pregnancy, intrahepatic cholestasis, and preeclampsia/HELLP are all third-trimester diseases.</b> A patient at 14 weeks with elevated transaminases, obesity, and diabetes has a metabolic liver disease that has nothing to do with being pregnant.</p></div>
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
<div class="danger"><span class="lbl">The lab detail most people misread</span>
<b>Alkaline phosphatase is supposed to be elevated in pregnancy</b> — the placenta makes its own isoenzyme, and levels run 2–4× normal. But <b>AST, ALT, and bilirubin do NOT rise physiologically</b>. Elevation of those is always pathologic.</div>
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
<div class="rule"><span class="lbl">Transferable rule</span> Trimester is to obstetric stems what duration is to pediatric joint stems — check that the timing <i>permits</i> the pregnancy-specific disease before reaching for it.</div>
<div class="traps"><span class="pill p-salient">Salient decoy</span></div>
</div>
```

### `fap`: Familial Adenomatous Polyposis

```html
<div class="brief" id="fap" data-shelf="fm" data-bp="gi">
<h4>Familial Adenomatous Polyposis</h4>
<p class="sub">Puberty starts the scope, the polyps set the colectomy · APC, hundreds of adenomas, cancer by 40</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 12 yo M, asymptomatic, father has familial adenomatous polyposis &middot; <b>Labs</b> &mdash; APC testing positive &middot; <b>Q</b> &mdash; the most appropriate screening step; options spanned annual sigmoidoscopy or colonoscopy starting now, colonoscopy at age 40 and prophylactic colectomy now</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>An <b>APC</b> mutation (autosomal dominant) means <b>hundreds to thousands</b> of adenomas and colon cancer in nearly <b>100% by age 40</b>. The exam scores two gates. First, screening: <b>annual sigmoidoscopy or colonoscopy from age 10–12</b> (puberty) — not the first-degree-relative rule, not average-risk screening. Second, the operation: <b>prophylactic proctocolectomy</b> is planned for the teens to early 20s, but is indicated <b>at any age</b> for bleeding, large (over 1 cm) or innumerable polyps, or high-grade dysplasia.</p>
<p>The miss is usually a parameter — the right rung with the wrong number (colonoscopy at 40, or at 10 years before the relative's cancer). Those are the rules for sporadic family history; a known APC carrier is a different pathway. The other tested move is the one after colectomy: <b>upper endoscopy</b> for duodenal and ampullary adenomas, which the colectomy does nothing about.</p></div>
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
<div class="danger"><span class="lbl">Where the rule breaks</span> The numbers here belong to a <b>known APC carrier</b>. A first-degree relative with sporadic colon cancer follows a different rule (earlier than average-risk screening, but not annual scoping from puberty), and a Lynch pedigree — few polyps, endometrial cancer in the family — follows a third. Match the pathway before you match the number. Colectomy timing is a plan, not a wait: any of <b>bleeding, polyps over 1 cm, innumerable polyps, or high-grade dysplasia</b> converts "teens to early 20s" into "now."</div>
<div class="pearls"><span class="lbl">Pearls</span> APC is autosomal dominant, so each child of an affected parent has a one-in-two risk and is tested rather than presumed · screening starts at puberty because adenomas appear in adolescence and cancer follows within decades · <b>Gardner</b> adds osteomas and desmoids, <b>Turcot</b> adds CNS tumors — both are FAP for management purposes · the colectomy fixes the colon and nothing else: duodenal and ampullary adenomas need their own endoscopy · Lynch is the polyp-poor counterpart with a mismatch-repair mechanism and an endometrial cancer in the pedigree</div>
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>Postmenopausal Bleeding</b> names Lynch syndrome among the endometrial cancer risk factors — the same pedigree seen from the gynecologic side. This brief wants a partner on <i>Lynch syndrome and colorectal cancer screening intervals</i> (not yet written). Store the discriminator as a question: how many polyps, and is there an APC mutation?</div>
<div class="rule"><span class="lbl">Transferable rule</span> Hereditary cancer questions are pathway questions — identify the syndrome first, because every number (start age, interval, operation) belongs to a pathway, and the sporadic family-history numbers are the planted wrong parameters.</div>
<div class="traps"><div class="trapline"><span class="pill p-number">Wrong parameter</span><span class="trapwhy">"Colonoscopy at 40" is the right intervention with the sporadic family-history number; an APC carrier is scoped annually from puberty.</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Polypectomy of the largest lesions is a rung below what innumerable polyps or dysplasia already licenses.</span></div><div class="trapline"><span class="pill p-uniform">Uniform-answer doubt</span><span class="trapwhy">"No further surveillance" after colectomy feels earned, but the duodenum was never operated on.</span></div></div>
</div>
```

### `peds-constipation`: Constipation in a Child

```html
<div class="brief" id="peds-constipation" data-shelf="fm peds" data-nid="1531920182274" data-bp="gi">
<h4>Constipation in a Child</h4>
<p class="sub">clear the alarm signs, then soften before you instrument &middot; Is growth normal and the examination benign, and is there stool in the rectum?</p>
<div class="vignette"><span class="lbl">Source vignette</span> <b>Pt</b> &mdash; 3 yo M, hard painful stools since toilet training began, normal growth, nontender abdomen, anal fissure &middot; <b>Q</b> &mdash; the most appropriate next step; options spanned an oral osmotic laxative, a rectal enema and abdominal radiography</div>
<div class="dp"><span class="lbl">The decision point</span>
<p>The stem hands you the mechanism in its chronology: stools were <b>daily and soft until toilet training began</b>, and the pain came before the hardness got worse. That is the <b>withholding cycle</b> — one painful stool teaches the child to hold, holding lets the rectum desiccate the next stool, and the next one hurts more. The <b>anal fissure</b> is the cycle's signature and its accelerant. Everything the examination <i>doesn't</i> show is doing equal work: growth on the 75th percentile with a nontender abdomen and a normal perineum clears the alarm-sign screen, which is what licenses treating rather than investigating. The move is the one that breaks the cycle at its only modifiable point — <b>an oral osmotic laxative</b> to make the next stool painless.</p></div>
<div class="crit"><span class="lbl">Defining criteria</span> <b>Alarm signs</b> &mdash; delayed passage of meconium, fever or vomiting, <b>ribbon stools</b>, poor growth, severe abdominal distension, and abnormal examination findings such as a <b>displaced anus or a tuft at the gluteal cleft</b> &middot; <b>Cow's-milk limit</b> &mdash; <b>under 24 oz per day</b>; this child's 24 oz is at the limit, not above it &middot; <b>Complications that are not alarm signs</b> &mdash; anal fissure, hemorrhoids, enuresis and urinary tract infections; each argues <i>for</i> the functional diagnosis rather than against it</div>
<div class="pearls"><span class="lbl">Pertinent positives &amp; negatives</span> <b>Onset coincides with toilet training</b> &mdash; the commonest trigger, alongside solid-food and cow's-milk introduction and school entry; it dates the problem to a behavior rather than an anatomy &middot; <b>Previously daily soft stools</b> &mdash; normal baseline function excludes a congenital motility defect, which would have declared earlier &middot; <b>Cries and screams with defecation</b> &mdash; pain is the engine of withholding, and it is the symptom the laxative is aimed at &middot; <b>Growth tracking at the 75th percentile</b> &mdash; clears the growth alarm sign and effectively removes Hirschsprung disease, hypothyroidism and celiac disease &middot; <b>Anal fissure</b> &mdash; a complication of hard stools, and the reason a rectal enema is the wrong instrument here &middot; <b>Abdomen firm and mildly distended but nontender</b> &mdash; stool load without obstruction; severe distension would be the alarm sign, and this is not it &middot; <b>24 oz of milk, refuses fruit</b> &mdash; the diet is a contributor to modify, not a cause to eliminate &middot; <b>Urinates in the toilet without difficulty</b> &mdash; the problem is stool-specific, which argues against a neurologic cause affecting both</div>
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
<div class="pearls"><span class="lbl">Tier fingerprint</span> done — nothing has been tried, so no failure has been earned &middot; normal — growth, perineum, abdominal tenderness and urinary function, all of them eliminations &middot; bothered — the child cries with every stool, which licenses treating today rather than counselling and waiting.</div>
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
<div class="pearls"><span class="lbl">Decision spine</span> <b>Any alarm sign?</b> &mdash; Growth normal, examination benign, meconium normal → no, so the investigation options are dead &middot; <b>Is there an impaction?</b> &mdash; Nontender abdomen with no stool ball → no, so disimpaction is not the tier being tested &middot; <b>Is the rectum instrumentable?</b> &mdash; There is a fissure → no rectal route even if one were needed &middot; <b>Is the diet outside limits?</b> &mdash; 24 oz of milk is at the ceiling rather than over it → modify rather than withdraw &middot; <b>What breaks the cycle?</b> &mdash; Make the next stool painless → an oral osmotic laxative</div>
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
<div class="danger"><span class="lbl">Decoy note</span> Two details invite over-reading in opposite directions. <b>Refusing to eat fruit</b> and the milk volume together read like a dietary indictment, but the stem quietly places the milk <i>at</i> the limit rather than above it, so the diet is a contributor to adjust rather than the answer. And <b>a firm, mildly distended abdomen</b> sounds ominous until you notice the two qualifiers the alarm-sign list actually uses: <i>severe</i> distension, and tenderness. Neither is here. The <b>anal fissure</b> is the most misread finding of all — it is not evidence of an alternative diagnosis, it is the expected complication of the diagnosis you already have, and its only management consequence is to close the rectal route.</div>
<div class="pearls"><span class="lbl">Pearls</span> A growing child with painful hard stools and a normal examination gets an oral osmotic laxative, not a rectal procedure or an image. &middot; Constipation in children is a <b>behavioural cycle with a mechanical consequence</b>; the laxative exists to make the next stool painless so the child stops holding, which is why it runs for months rather than days ⚠︎. &middot; The three transitions that generate it are <b>solid food and cow's milk, toilet training, and school entry</b> — a stem that names one is telling you the diagnosis. &middot; An anal fissure is a <b>complication</b> of constipation rather than a competing diagnosis, and it is the reason to disimpact by mouth rather than by rectum. &middot; Hirschsprung disease declares with <b>delayed meconium and poor growth</b>, and fissures are uncommon in it; normal growth with a fissure is functional disease. &middot; <b>Growth is the alarm sign that does the most work</b> — a child tracking a percentile has essentially excluded hypothyroidism, celiac disease and Hirschsprung disease before you order anything. &middot; Enuresis and urinary tract infections are complications of constipation, so a wet child with hard stools gets the bowel treated first.</div>
<div class="pearls"><span class="lbl">Pairs with</span> Verified: Part II <b>Fecal Impaction &amp; Overflow Diarrhea</b> is the adult mirror of this brief's tier 2 — there the rectal vault is full and the enema is first-line, while here the vault is not and the fissure closes that route. Part I <b>Infant Stool Complaints: Dyschezia, FPIAP &amp; Secondary Lactase Deficiency</b> owns the infant end of the same complaint, and Part II <b>Tethered Cord and Closed Spinal Dysraphism</b> owns the exit ramp this brief's perineal examination is screening for. Store the discriminator as a question: is growth normal, and is there stool in the rectum?</div>
<div class="rule"><span class="lbl">Transferable rule</span> When a common condition has a benign screening profile, the examination's normals are the permission to treat, and the alarm-sign list is the only thing that converts treatment into investigation. A complication of the diagnosis is evidence for it rather than against it — but it can still change which instrument you are allowed to use. --- <i>Batch 5, brief 01 · 2026-09-10.</i></div>
<div class="traps"><div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Discontinue milk &mdash; 24 oz is <b>within</b> the recommended 16 to 24 oz range; withdrawal costs calcium and vitamin D and buys nothing</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Obtain abdominal radiograph &mdash; The film is for <b>severe</b> impaction that mimics obstruction, with pain and vomiting; this abdomen is nontender and benign</span></div><div class="trapline"><span class="pill p-salient">Salient decoy</span><span class="trapwhy">Administer rectal enema &mdash; There is no impaction to disimpact, and the <b>anal fissure</b> makes the rectal route actively harmful here</span></div><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Obtain anorectal manometry &mdash; Reserved for constipation that <b>persists despite standard therapy</b>; no therapy has been tried and no alarm sign is present</span></div></div>
</div>
```

### `bs-water-soluble-vitamins`: Water-Soluble Vitamin Deficiency

```html
<div class="brief bs" id="bs-water-soluble-vitamins" data-shelf="fm peds" data-bp="multi gi">
<h4>Water-Soluble Vitamin Deficiency</h4>
<p class="sub">Confusion and ataxia in heavy drinking, a sun-exposed rash, bleeding gums with normal clotting &middot; UWorld library &middot; which organs are involved, and what is the patient drinking, taking or not eating?</p>
<div class="dp"><span class="lbl">The decision point</span>
<p>The body stores little of the B vitamins or vitamin C (B12 is the exception), so deficiency follows <b>chronic alcohol use</b>, poor intake, malabsorption (bypass, short bowel, Crohn disease) or a <b>drug</b>. The <b>organ pattern</b> names the vitamin: <b>brain, eyes and gait, or the heart</b> is B1; <b>photosensitive dermatitis with diarrhea and dementia</b> is B3; <b>neuropathy on isoniazid</b> is B6; <b>megaloblastic anemia</b> is B9 or B12, and a <b>high methylmalonic acid with neurologic signs</b> separates B12; <b>bleeding gums and perifollicular hemorrhages with normal platelets, PT and aPTT</b> is C.</p>
<p>Two orders matter. In a malnourished or alcohol-using patient, give <b>IV thiamine before or with glucose</b>, because a glucose load can precipitate or worsen Wernicke encephalopathy. And do not treat a megaloblastic anemia with <b>folate alone</b> until B12 is known: folate corrects the anemia but not the neurologic damage of B12 deficiency, so give both when the cause is unclear.</p>
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
<div class="pearls"><span class="lbl">Pairs with</span> Part I <b>The Vegan Diet</b> owns B12 against folate in a plant diet: is there a fortified or animal source of B12? Part I <b>Marfanoid Habitus: Homocystinuria</b> owns inherited high homocysteine, treated with B6, folate and B12. Part I <b>Teratogenic Exposures</b> owns the folate-antagonist antiepileptics and neural tube defects. Part I <b>Tuberculosis</b> owns isoniazid with B6. Part II <b>Fat-Soluble Vitamin Deficiency and Toxicity</b> owns bleeding with a long PT: are the coagulation studies abnormal (K) or normal (C)?</div>
<div class="rule"><span class="lbl">Transferable rule</span> Read the organ pattern first (brain, eyes and heart; sun-exposed skin with diarrhea; neuropathy on a drug; megaloblastic blood; bleeding gums with normal clotting), then ask what the patient drinks, takes or does not eat; give thiamine before glucose, and settle B12 (with MMA when the level is 200 to 300) before giving folate alone.</div>
<div class="traps"><div class="trapline"><span class="pill p-seq">Sequencing trap</span><span class="trapwhy">Dextrose first in a confused, hypoglycemic drinker: the glucose is needed, but thiamine goes in before or with it.</span></div><div class="trapline"><span class="pill p-slot">True-fact-wrong-slot</span><span class="trapwhy">Homocysteine to separate B12 from folate: it is truly high in B12 deficiency, but it is high in folate deficiency too; only MMA separates them.</span></div><div class="trapline"><span class="pill p-attr">Unchecked attribute</span><span class="trapwhy">Folic acid for a megaloblastic anemia with numb feet: the blood improves, but the neurologic signs mark B12, and folate alone lets them progress.</span></div><div class="trapline"><span class="pill p-class">Class-vs-member</span><span class="trapwhy">Vitamin K for bleeding gums and bruises: the right class, a vitamin, but scurvy leaves the PT normal, so vitamin C is the member.</span></div></div>
</div>
```
