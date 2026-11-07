# TEXTBOOK_STYLE: how every visible line on Step2Haki is written

Decision: D-20261106-9 (supersedes the 2026-10-19 prose and label rules). Gate and READY checks: D-20261106-11.
Scope: every visible string on briefs and cards: titles, headers, captions, column heads, labels, key points, findings,
table cells, notes, timeline rows, pause points, hover cards and the per-choice reasons in practice items. Practice
stems also follow "Original stems" in STANDING_DIRECTIONS. Conversation replies are outside this file.

Enforcement:
- tools/spine/prose_lint.py: the gate's prose-lint check (no brief's count rises above tools/spine/prose_baseline.json)
  and prose-touched check (a brief whose text changed against the base has zero hits); ship.sh tightens the baseline.
- tools/spine/verify.py: a brief with prose hits is not READY, so ship.sh refuses it.
- The card below is copied into every builder's INSTRUCTIONS.md (tools/spine/build_lanes.py) and every reviewer's
  RULES.md (tools/spine/review_packet.py). This file is the only copy; edit it here.

<!-- card:start -->
## Writing card (read before writing or reviewing any line)

**Rule 0, the test.** Every line carries a clinical fact, a finding or an action. Remove words that serve cadence,
emphasis or persuasion. Connectives that carry logic ("because", "then", "after", "so that") count as information.
Classes 1 to 7 are examples of the test; a line that fails the test is out, listed or unlisted.

**1. Register.** Purpose: the reader scans, as in First Aid, AnKing or Pocket Medicine.
- Term first, then a colon, then the content. One fact per line; a list of parallel items under one label is one fact;
  at most one semicolon in a line.
- Arrows for cause and effect, one chain per line.
- Lists drop articles and "or"; keep "or" between mutually exclusive alternatives (two actions, either of two conditions).
- Keep the relation word when no heading says it: "Fluoxetine: also used for bulimia nervosa".
- Lines under a block heading (a bold line with nothing after it), row label, column head or hover title take their
  subject from it; a line that stands alone names its own; a label never repeats its heading.
- Violation: "Mirtazapine sedates and raises appetite and weight; it and bupropion cause no sexual dysfunction".
  Fix: "Mirtazapine: sedation, ↑ appetite, weight gain" and "Antidepressants without sexual dysfunction: bupropion, mirtazapine".
- Permitted near miss: "Onset: within days of an abrupt stop" under the heading "SNRI discontinuation syndrome".

**2. Cadence and persuasion devices.** Purpose: they add rhythm or a punchline and carry no information.
- Contrast: "X, not Y", "not X, but Y", "not just X", "not only X", "rather than", "instead of", "it isn't X, it's Y".
- Branch: "if not X, then Y", "otherwise", bare condition labels ("Declines restart:"); list the options in one line.
- Comma restatements ("paroxetine included", "paroxetine too"); trailing explainers (", which ...", ", making it ...",
  ", meaning ..."); intensifiers ("even", "really", "actually", "most of all", "above all", "only" or "just" as emphasis);
  reveal colons ("The key:", "The trap:", "The tell:"); rhythm pairs; slogan closers.
- Violation: "Not relapse, not influenza". Fix: "Discontinuation syndrome: can mimic depressive relapse or influenza".
- Permitted near misses: "unless contraindicated"; a purpose clause ("taper slowly so that symptoms resolve"); "only" as
  a fact ("the only FDA-approved drug for bulimia nervosa"); negative findings ("no seizures"); a real classification
  pair on separate lines (tertiary and secondary amines).

**3. Lines that lean on context.** Purpose: each line makes sense and is usable on its own.
- No fragments ("Worst: X", "Also: Y", "Some: X", "Maximum: X"); no vague back-references ("this", "less of both");
  an instruction names a concrete action, and a condition a concrete threshold.
- Violation: "Worst: amitriptyline". Fix: "Most anticholinergic TCA: amitriptyline".

**4. Sources and provenance.** Purpose: things do not speak, and sourcing lives in the claim map.
- No source narration: "on the Zoloft label", "the AnKing card gives", "as the board teaches", "higher in the Merck
  Manual", "analogy from the source". Sources, analogy labels and verification notes go in data attributes, the claim
  map and the batch report. The ⚠︎ mark stays.
- "In practice:" (a board answer that differs from a guideline) starts the first line under a clinical title.
- Violation: "On the Zoloft label, newborns exposed ... have needed prolonged hospital care". Fix: "Late third-trimester
  exposure → some newborns need prolonged hospitalization, respiratory support, tube feeding".

**5. Notation and names.** Purpose: readers may misparse uncommon notation.
- In a sentence, write an uncommon comparison in words: "less than double baseline" for "< 2-fold", "more than half".
- Permitted near misses: standard notation where readers expect it: criteria and tables ("≥ 30 mg/g", "> 38 °C"),
  lab values, doses ("40 mg/day"), space-limited cells; the symbols ↑ ↓ → and the · row separator.
- Abbreviations: spelled out at first use in each block (a tile or a table row; a hover belongs to the block of the
  line that opens it) unless on repair/efficiency/ABBREV.json; never an unexpanded abbreviation alone in a list.
- Generic drug names plain, bold only as a line's key term, never italic. A trade name only after the generic, in
  parentheses, in the trade-name style, and only with a current FDA label. Italics for organism names only.
- Mnemonic letters in bold inside hovers; mnemonics in a brief keep their mnemonic tile.

**6. Headers and hovers.** Purpose: a header names a clinical category; a hover adds one clear detail.
- Headers come from the header list in this file: clinical nouns, no verbs, questions, ordering notes ("most tempting
  first") or tails (", by result", ", from the last dose"). A header not on the list needs Jonathan's approval.
- Hover title: the full clinical term or category ("Other common adverse effects"). Body: one idea per line, about 12
  words or fewer per line, arrow lines indented, no paragraph blocks.
- Line targets: key point about 15 words, finding about 20, hover line about 12. Over target means split; never cut a fact.

**7. Process.** Purpose: a correction changes the system that produced the error.
- Fix every instance of a pattern in the brief, and report the count.
- Before a build receipt: `python3 tools/spine/prose_lint.py <page> --brief <id>` reaches zero hits; verify.py refuses
  READY otherwise.
- Meaning lock: a rewrite keeps every fact, number, hedge (may, usually, often, typically, some, can), condition, scope
  and name; the claim map carries old to new.
- A false positive goes in prose_lint.py's ALLOW list with a test, and becomes a permitted near miss here.
<!-- card:end -->

## Approved examples, key points and findings (Jonathan 2026-11-05: "these are all good changes and more so what i imagined"; revised after two independent audits the same day)

| # | Where | Live | Textbook | Note |
|---|---|---|---|---|
| P1 | SNRIs · Key point | Serotonin and norepinephrine reuptake blocked → dose-dependent hypertension, the most common adverse effect of serotonin-norepinephrine reuptake inhibitors (SNRIs); venlafaxine is typically avoided in hypertension | Serotonin-norepinephrine reuptake inhibitors (SNRIs): serotonin and norepinephrine reuptake blockade → dose-dependent ↑ blood pressure<br>Venlafaxine: typically avoided in hypertension | the most-common claim held for N9 |
| P2 | SNRIs · Key point | Abrupt stop, most of all with short half-life venlafaxine → flu-like discontinuation symptoms within days, without seizures; a slow taper prevents them | **SNRI discontinuation syndrome**<br>Onset: within days of an abrupt stop<br>Highest risk: venlafaxine (short half-life)<br>Symptoms: flu-like illness; no seizures<br>Prevention: slow taper |  |
| P3 | SNRIs · Key point | First line, with selective serotonin reuptake inhibitors (SSRIs), for generalized anxiety, panic, social anxiety and posttraumatic stress disorders; duloxetine also treats diabetic neuropathy and fibromyalgia | Selective serotonin reuptake inhibitors (SSRIs), SNRIs: first line for generalized anxiety disorder, panic disorder, social anxiety disorder, posttraumatic stress disorder<br>Duloxetine: also used for diabetic neuropathy, fibromyalgia |  |
| P4 | SNRIs · Danger row | Blood pressure up, more at higher doses; heart rate may rise too | ↑ blood pressure, greater at higher doses; heart rate may also rise |  |
| P5 | SNRIs · Danger row | Flu-like aches, dizziness, nausea, irritability or electric shock-like sensations within days of an abrupt stop | Symptoms: flu-like aches, nausea, dizziness, irritability, electric shock-like sensations<br>Onset: within days of an abrupt stop |  |
| P6 | SNRIs · Note | Symptoms after an abrupt stop are discontinuation, not relapse or influenza; a patient willing to restart venlafaxine restarts it, then tapers slowly, as the board teaches for paroxetine, another short half-life drug; a patient who will not restart venlafaxine: SSRI Adverse Effects. | Discontinuation syndrome: can mimic depressive relapse or influenza<br>Treatment: restart venlafaxine and taper slowly · [SSRI Adverse Effects] | the paroxetine analogy moves to the data label (N4) |
| P7 | Other antidepressants · Key point | Bupropion lowers the seizure threshold → avoid it with a seizure disorder, bulimia or anorexia, or an abrupt stop of alcohol, a benzodiazepine, a barbiturate or an antiepileptic | **Bupropion**<br>Adverse effect: ↓ seizure threshold<br>Avoid in: seizure disorder, bulimia nervosa, anorexia nervosa<br>Avoid during: abrupt withdrawal from alcohol, benzodiazepines, barbiturates, antiepileptics |  |
| P8 | Other antidepressants · Key point | Trazodone blocks alpha-1 receptors → priapism and orthostatic hypotension; an erection over 4 hours is a urologic emergency | Trazodone: alpha-1 blockade → priapism, orthostatic hypotension<br>Erection lasting over 4 hours: urologic emergency |  |
| P9 | Other antidepressants · Key point | Mirtazapine sedates and raises appetite and weight; it and bupropion cause no sexual dysfunction | Mirtazapine: sedation, ↑ appetite, weight gain<br>Antidepressants without sexual dysfunction: bupropion, mirtazapine | shared decision: option B adds "add or switch to either for SSRI sexual dysfunction" (stated in SSRI Adverse Effects) |
| P10 | SSRIs · Danger row | First-trimester exposure: under a 2-fold rise in cardiac malformations | First-trimester exposure: ↑ risk of cardiac malformations (less than double baseline) |  |
| P11 | SSRIs · Timeline | Shows: a few may grow agitated or anxious: lower the dose or switch SSRI | Agitation or anxiety in some patients: lower the dose or switch to another SSRI |  |
| P12 | SSRIs · Timeline | Shows: keep the dose while waiting | Continue the same dose while awaiting response |  |
| P13 | SSRIs · Timeline | Why: a change comes only after an adequate trial | Adequate trial required before a change in treatment |  |
| P14 | SSRIs · Interactions | A monoamine oxidase inhibitor (MAOI), or one stopped inside its washout · Never together | Monoamine oxidase inhibitor (MAOI), current or within the washout period · Contraindicated |  |
| P15 | SSRIs · Interactions | Tramadol, linezolid, a triptan, dextromethorphan, ondansetron or St John's wort · Serotonin syndrome · Watch for clonus and hyperreflexia; avoid St John's wort | Tramadol, linezolid, triptans, dextromethorphan, ondansetron, St John's wort<br>Serotonin syndrome<br>Monitor for clonus, hyperreflexia; avoid St John's wort |  |
| P16 | SSRIs · Interactions | Bleeding risk can rise, including GI · Counsel on bleeding; check the international normalized ratio (INR) on warfarin | ↑ bleeding risk, including GI bleeding<br>Counsel on bleeding<br>Warfarin: check the international normalized ratio (INR) |  |
| P17 | SSRIs · Hover | Any SSRI late in pregnancy, paroxetine included, can cause persistent pulmonary hypertension of the newborn. On the Zoloft label, newborns exposed to an SSRI late in the third trimester have needed prolonged hospital care, breathing support and tube feeding. | **Any SSRI in late pregnancy**<br>→ ↑ risk of persistent pulmonary hypertension of the newborn<br>**Late third-trimester exposure**<br>→ some newborns need prolonged hospitalization, respiratory support, tube feeding |  |
| P18 | SSRIs · Hover | The Zoloft label also lists diarrhea, tremor, indigestion, less appetite and sweating among the most common effects. | Other common adverse effects (sertraline): diarrhea, tremor, dyspepsia, ↓ appetite, sweating |  |
| P19 | SSRIs · Hover | Higher in the Merck Manual: sexual dysfunction above half of patients, most often trouble reaching orgasm. | In practice: sexual dysfunction in more than half of patients<br>Most common type: difficulty reaching orgasm |  |
| P20 | SSRIs · Hover | The Celexa label also avoids it with congenital long QT, a slow heart rate, low potassium or magnesium, uncompensated heart failure or another QT-prolonging drug, and checks electrolytes when they may run low. | **Citalopram QT precautions**<br>Avoid in: congenital long QT syndrome, bradycardia, hypokalemia, hypomagnesemia, uncompensated heart failure<br>Avoid with: other QT-prolonging drugs<br>Monitor: potassium, magnesium in patients at risk of low levels |  |
| P21 | SSRIs · Hover | The AnKing card gives 6 weeks at full dose before considering a change. | Full dose: 6 weeks before considering a change | the visible line says at least 4 to 6 weeks at a therapeutic dose; this hover gives the full-dose figure; owner to confirm both stay |
| P22 | SSRIs · Hover | On an SSRI, platelets take up less serotonin, and they rely on it to stop bleeding. | SSRI → ↓ platelet serotonin uptake<br>Platelets need serotonin for hemostasis |  |
| P23 | TCAs · Hover | Analogy from the source: the sodium-channel block resembles class IA antiarrhythmics such as quinidine. | Na⁺ channel blockade: similar to class IA antiarrhythmics such as quinidine |  |
| P24 | TCAs · Hover | Neuropathic pain: a tricyclic or a gabapentinoid comes first. Migraine prophylaxis: tricyclics are second line. Amitriptyline is the first-line preventive for chronic tension headache. Tricyclics also help diarrhea-predominant irritable bowel syndrome and fibromyalgia. | Neuropathic pain: first-line TCA or gabapentinoid<br>Migraine prophylaxis: second-line TCA<br>Chronic tension headache: first-line amitriptyline for prevention<br>TCAs: also used for diarrhea-predominant irritable bowel syndrome, fibromyalgia |  |
| P25 | TCAs · Hover | On the Anafranil label, seizure is the most significant risk of the drug. | Clomipramine: seizure is the most significant risk |  |

## Approved examples, lines with hovers (same review; the anchor term is in _italics_)

| # | Where | Live line and hover | Textbook line, anchor in _italics_, and hover |
|---|---|---|---|
| T1 | SSRIs · Mechanism | **Serotonin transporter** blocked → more serotonin in the synapse → longer postsynaptic stimulation [trigger "Receptors"]<br>Hover (Serotonin receptors): Type 1 receptors carry the antidepressant and anti-anxiety effect; type 2 receptors bring anxiety, insomnia and sexual dysfunction; type 3 receptors bring nausea and headache. Dopamine and norepinephrine are barely touched. | **Serotonin transporter** blockade → ↑ synaptic serotonin → prolonged _postsynaptic stimulation_<br>Hover (SSRI effects by serotonin (5-HT) receptor): 5-HT1: antidepressant, anxiolytic effect / 5-HT2: anxiety, insomnia, sexual dysfunction / 5-HT3: nausea, headache / Dopamine, norepinephrine reuptake: little effect |
| T2 | SSRIs · Uses | **Depression**, **obsessive-compulsive disorder**, **panic**, **generalized and social anxiety**, **premenstrual dysphoric disorder**; fluoxetine for bulimia nervosa [trigger "Also"]<br>Hover (Other uses): SSRIs also treat premature ejaculation and menopausal hot flashes (paroxetine, citalopram). | **Depression**, **obsessive-compulsive disorder**, **panic disorder**, **generalized anxiety disorder**, **social anxiety disorder**, **premenstrual dysphoric disorder**<br>**Fluoxetine**: also used for bulimia nervosa<br>Now a visible line: **Other uses**: premature ejaculation, menopausal hot flashes (paroxetine, citalopram) |
| T3 | SSRIs · Adverse effects | **Early**: nausea, headache, insomnia or sleepiness, anxiety, dizziness [trigger "Label"]<br>Hover (Sertraline label): The Zoloft label also lists diarrhea, tremor, indigestion, less appetite and sweating among the most common effects. | **_Early_**: nausea, headache, insomnia or somnolence, anxiety, dizziness<br>Hover (Other common adverse effects (sertraline)): Diarrhea, tremor, dyspepsia, ↓ appetite, sweating |
| T4 | SSRIs · Adverse effects | **Later**: sexual dysfunction in up to half, weight gain [trigger "In practice"]<br>Hover (In practice): Higher in the Merck Manual: sexual dysfunction above half of patients, most often trouble reaching orgasm. | **Later**: _sexual dysfunction_ (up to half of patients), weight gain<br>Hover (SSRI sexual dysfunction): In practice: sexual dysfunction in more than half of patients / Most common type: difficulty reaching orgasm |
| T5 | SSRIs · Adverse effects | **Hyponatremia**, often from the syndrome of inappropriate antidiuretic hormone secretion (SIADH), higher risk over 65 [trigger "Mnemonic"]<br>Hover (Drug causes of SIADH): "Can't Concentrate Serum Na+": carbamazepine, cyclophosphamide, SSRIs and nonsteroidal anti-inflammatory drugs (NSAIDs) can all cause SIADH. | **Hyponatremia**: often from _syndrome of inappropriate antidiuretic hormone secretion_ (SIADH); higher risk over age 65<br>Hover (Drug causes of SIADH): Mnemonic: **C**an't **C**oncentrate **S**erum **N**a⁺ / **C**arbamazepine, **C**yclophosphamide, **S**SRIs, **N**onsteroidal anti-inflammatory drugs (NSAIDs) |
| T6 | SSRIs · Danger row | **QT prolongation on citalopram**Dose-dependent; label maximum 40 mg a day, 20 mg over age 60 or with hepatic impairment [trigger "Label"]<br>Hover (Citalopram label): The Celexa label also avoids it with congenital long QT, a slow heart rate, low potassium or magnesium, uncompensated heart failure or another QT-prolonging drug, and checks electrolytes when they may run low. | **Citalopram**: dose-dependent _QT prolongation_<br>Maximum dose: 40 mg/day; 20 mg/day over age 60 or with hepatic impairment<br>Hover (Citalopram QT precautions): Avoid in: congenital long QT syndrome, bradycardia, hypokalemia, hypomagnesemia, uncompensated heart failure / Avoid with: other QT-prolonging drugs / Monitor: potassium, magnesium in patients at risk of low levels |
| T7 | SSRIs · Danger row | **First-trimester exposure: under a 2-fold rise in cardiac malformations****If** an SSRI is needed in pregnancy, **choose** sertraline or escitalopram over paroxetine. [trigger "Newborn"]<br>Hover (Newborn risk): Any SSRI late in pregnancy, paroxetine included, can cause persistent pulmonary hypertension of the newborn. On the Zoloft label, newborns exposed to an SSRI late in the third trimester have needed prolonged hospital care, breathing support and tube feeding. | **First-trimester exposure: ↑ risk of cardiac malformations (less than double baseline)**<br>**If** an SSRI is needed in _pregnancy_, **choose** sertraline or escitalopram over paroxetine.<br>Hover (Late-pregnancy exposure): **Any SSRI in late pregnancy** / → ↑ risk of persistent pulmonary hypertension of the newborn / **Late third-trimester exposure** / → some newborns need prolonged hospitalization, respiratory support, tube feeding |
| T8 | SSRIs · Timeline: "From the first dose" → "Time to response" | **Adequate trial**At least 4 to 6 weeks at a therapeutic doseWhy: a change comes only after an adequate trial [trigger "AnKing"]<br>Hover (AnKing card): The AnKing card gives 6 weeks at full dose before considering a change. | **Adequate trial**<br>At least 4 to 6 weeks at a _therapeutic dose_<br>Rationale: adequate trial required before a change in treatment<br>Hover (Adequate trial): Full dose: 6 weeks before considering a change |
| T9 | SSRIs · Interactions: "Interactions, by result" → "Drug interactions" | **Aspirin, a nonsteroidal anti-inflammatory drug (NSAID), warfarin or another anticoagulant**Bleeding risk can rise, including GICounsel on bleeding; check the international normalized ratio (INR) on warfarin [trigger "Why"]<br>Hover (Platelet serotonin): On an SSRI, platelets take up less serotonin, and they rely on it to stop bleeding. | **Aspirin, nonsteroidal anti-inflammatory drugs (NSAIDs), warfarin, other anticoagulants**<br>_↑ bleeding risk_, including GI bleeding<br>Counsel on bleeding<br>Warfarin: check the international normalized ratio (INR)<br>Hover (Mechanism of SSRI-associated bleeding): SSRI → ↓ platelet serotonin uptake / Platelets need serotonin for hemostasis |
| T10 | TCAs · Drugs | **Protriptyline**: secondary [trigger "Tertiary or secondary"]<br>Hover (The two amine groups): Tertiary amines lean toward serotonin reuptake block and are more anticholinergic and sedating. Secondary amines lean toward norepinephrine reuptake block and are less of both. | **Protriptyline**: _secondary_ amine<br>Hover (Tertiary and secondary amines): Tertiary amines: more serotonin reuptake blockade; more anticholinergic, more sedating / Secondary amines: more norepinephrine reuptake blockade; less anticholinergic, less sedating |
| T11 | TCAs · Mechanism | **Cardiac fast sodium channels** blocked → slower conduction → QRS widening, ventricular arrhythmia [trigger "Like class IA"]<br>Hover (Analogy): Analogy from the source: the sodium-channel block resembles class IA antiarrhythmics such as quinidine. | **_Cardiac fast Na⁺ channel_ blockade** → slower conduction → QRS widening, ventricular arrhythmia<br>Hover (Similarity to class IA antiarrhythmics): Na⁺ channel blockade: similar to class IA antiarrhythmics such as quinidine |
| T12 | TCAs · Uses | **Amitriptyline**, **nortriptyline** at low doses: **neuropathic pain**, postherpetic neuralgia, **migraine** prophylaxis [trigger "Order"]<br>Hover (Pain and headache): Neuropathic pain: a tricyclic or a gabapentinoid comes first. Migraine prophylaxis: tricyclics are second line. Amitriptyline is the first-line preventive for chronic tension headache. Tricyclics also help diarrhea-predominant irritable bowel syndrome and fibromyalgia. | **Amitriptyline**, **nortriptyline** at low doses: **_neuropathic pain_**, postherpetic neuralgia, **migraine** prophylaxis<br>Hover (Line of therapy for pain and headache): Neuropathic pain: first-line TCA or gabapentinoid / Migraine prophylaxis: second-line TCA / Chronic tension headache: first-line amitriptyline for prevention / TCAs: also used for diarrhea-predominant irritable bowel syndrome, fibromyalgia |
| T13 | TCAs · Uses | **Doxepin**: **insomnia**, from its histamine block [trigger "Label"]<br>Hover (Doxepin label): Silenor, low-dose doxepin, is labeled for insomnia with trouble staying asleep. | **Doxepin**: **_insomnia_**, from H1 blockade<br>Hover (Doxepin for insomnia): Low-dose doxepin (Silenor): approved for sleep-maintenance insomnia |
| T14 | TCAs · Adverse effects | **Anticholinergic**: dry mouth, blurry vision, constipation, urinary retention, fast pulse, confusion; worst with amitriptyline [trigger "More"]<br>Hover (Other effects): Tricyclics can also cause gastroparesis; respiratory depression and hyperpyrexia are listed too. | **Anticholinergic effects**: dry mouth, blurry vision, constipation, urinary retention, tachycardia, confusion<br>Most anticholinergic TCA: amitriptyline<br>Now a visible line: **Other TCA adverse effects**: gastroparesis, respiratory depression, hyperpyrexia |
| T15 | TCAs · Adverse effects | **GABA-A antagonism**: seizures [trigger "Clomipramine"]<br>Hover (Clomipramine label): On the Anafranil label, seizure is the most significant risk of the drug. | **GABA-A antagonism**: _seizures_<br>Hover (Seizure risk): Clomipramine: seizure is the most significant risk |

## Header list (the closed list for rule 6)

Status 2026-11-06: proposed by Claude 2026-11-05 from a scan of the live page (1,109 distinct headers and labels, 265
matching a non-textbook pattern). Jonathan: rows he did not change go into the pilot as written. Rows H13 to H16
(they rename the standing clue-table columns), H24 (card spec timeline tags) and H45 (new block headings) wait for his
call. CARD_SPEC's prescribed labels ("Combined with | Result | Rule", "Where the choice is made") change in the content
batch that renames them on the page, so the spec and the page change in one commit.

| # | Kind | Live | Uses | Proposed | Why |
|---|---|---|---|---|---|
| H1 | Caption | Clues that change the answer | 103 | Key findings | names the question, not the content |
| H2 | Caption | Look-alikes, most tempting first; and 57 other "…, most tempting first" | 78 | Differential diagnosis (or "Differential diagnosis of low back pain") | ordering note is a build rule; the order stays |
| H3 | Caption | Follow-up decisions | 43 | Follow-up |  |
| H4 | Caption | Act now | 24 | Emergencies | imperative |
| H5 | Caption | First treatment by situation | 16 | Initial treatment |  |
| H6 | Caption | Interactions, by result; Interactions | 19 | Drug interactions | N3 |
| H7 | Caption | Urgent findings; Red flags: act before the full history | 10 | Red flags |  |
| H8 | Caption | What sets the outcome; What raises the stakes; What makes it severe; What makes it dangerous | 9 | Prognosis or Severity, by content | figurative |
| H9 | Caption | History: what each answer points to; Examination: what each finding points to | 6 | History; Physical examination |  |
| H10 | Caption | Finalists; What sets it apart | 6 | Leading diagnoses; Distinguishing features |  |
| H11 | Caption | Which effect is it, most tempting first; Manage by effect | 6 | Differential of adverse effects; Management by adverse effect | question, imperative |
| H12 | Caption | …: start on the lowest rung not yet tried; Management ladder: … | 9 | Stepwise management: … | figurative; the ladder rule stays as a line under the header |
| H13 | Column head | Decides it | 115 | Distinguishing feature | standing table spec |
| H14 | Column head | Points to; What it points to | 146 | Interpretation | standing table spec; a verb is not a header |
| H15 | Column head | Next move; Next | 58 | Next step | standing table spec |
| H16 | Column head | Clue | 112 | Finding | standing table spec |
| H17 | Column head | Fingerprint; Illness script + buzzwords | 72 | Key features | figurative |
| H18 | Column head | Do | 74 | Management |  |
| H19 | Column head | The NBME tell; The tell; Tell | 32 | Classic finding | meta; "Key finding" would collide with H1 |
| H20 | Column head | Combined with · Result · Rule | 16 | Drug · Effect · Management | card spec; N3 |
| H21 | Column head | Excluded here by; Excluded by; Why less likely here | 15 | Findings against the diagnosis | stem-bound column, retired in the old template |
| H22 | Column head | Hook; The picture; The company it keeps; What kills it; Why it tempts; Why it loses; Legitimate claim | 8 | Rewrite per table | figurative or meta |
| H23 | Tile label | Transferable rule · Pairs with · The decision point | 371 | General rule · Related topics · Key decision | old template jargon |
| H24 | Timeline tag | Shows · Why | 14 | Findings or Action, by content · Rationale | card spec; "Expect" and "Why" are not nouns |
| H25 | Tile label | Decoy note; Decoys; Distractors; Common wrong answers | 49 | Common wrong answers | four names for one thing |
| H26 | Tile label | Decision spine; Exit ramps; Gates; Boundary conditions; Tier fingerprint; The hierarchy to bank | 22 | Remove or rewrite per content | internal workflow terms |
| H27 | Tile label | Where the choice is made | 18 | Drug choice by condition | card spec; lists the decisions made in disease briefs |
| H28 | Tile label | Papilledema forbids the tap; Occulta means hidden; Latency is a diagnostic variable; The vitals do most of the eliminating | 4 | Noun labels per content | slogans |
| H29 | Card timeline | From the first dose | 1 | Treatment response timeline | N3 |
| H30 | Card timeline | Toxicity and withdrawal, from the exposure or the last dose | 1 | Toxicity and withdrawal timeline |  |
| H31 | Card timeline | Washout and diet limits, from the last dose; Limits after the last dose | 2 | Washout periods and dietary restrictions |  |
| H32 | Card timeline | Movement effects and NMS, from a start or dose increase | 1 | Onset of extrapyramidal effects and neuroleptic malignant syndrome |  |
| H33 | Card timeline | When each reaction appears, from the start; After a dose or a stop: which effect, and when | 2 | Onset of adverse and withdrawal effects | question |
| H34 | Card timeline | Titration and restart limits, from the last dose change | 1 | Titration and restart limits |  |
| H35 | Card timeline | When each drug can start | 1 | Timing of initiation |  |
| H36 | Card timeline | Clozapine, from the first dose | 1 | Clozapine adverse effects timeline |  |
| H37 | Card timeline | Contraception on modafinil or armodafinil, from the last dose | 1 | Contraception with modafinil, armodafinil |  |
| H38 | Psych timeline | Time the psychosis | 1 | Psychotic disorders by duration | imperative |
| H39 | Psych timeline | Check it against mood episodes | 1 | Psychosis and mood episodes | imperative |
| H40 | Psych timeline | Time the episode; Name the disorder from its episodes | 2 | Episode duration; Mood disorders by episode | imperative |
| H41 | Psych timeline | Time it, then name the fear | 1 | Anxiety disorders by duration and focus of fear | imperative |
| H42 | Psych timeline | Time the confusion; Time alcohol withdrawal from the last drink | 2 | Confusion timeline; Alcohol withdrawal timeline | imperative |
| H43 | Workup tree | 1 Is TSH low or high, and is the gland making or leaking? and 14 other question titles | 15 | Plain test or topic name ("Thyroid function workup") | also breaks "workups are not question-led" (2026-10-07) |
| H44 | Section | Practice; Scenario bank | 200 | Practice | two names for one thing |
| H45 | Block heading | (new) SNRI discontinuation syndrome; Citalopram QT precautions; Bupropion; Any SSRI in late pregnancy | 0 | As written | new headings group lines under one subject (R1); they need your approval like any header |

## Open owner decisions (from the 2026-11-05 review)

- P1: whether hypertension is the most common SNRI adverse effect (held for a board-source check).
- P6: whether a link to another brief at the end of a line takes a label ("Related topics:").
- P9: option A ("Antidepressants without sexual dysfunction: bupropion, mirtazapine") or option B (A plus "add or switch
  to either for SSRI-induced sexual dysfunction", stated in SSRI Adverse Effects).
- P21: the live page gives "at least 4 to 6 weeks at a therapeutic dose" and, in the hover, "6 weeks at full dose".
- TCA hover: whether respiratory depression and hyperpyrexia stay listed as adverse effects or move to overdose.
- SSRI other uses: whether "(paroxetine, citalopram)" scopes hot flashes alone or both uses.
- Hover trigger style (N7): A, the term anchor, with short hovers made visible lines (F), or E, the whole line.
