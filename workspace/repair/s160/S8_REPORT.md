**s160 final report: Psych Pharmacology B2 (six class cards)**
Benzodiazepines, Other anxiety agents, ADHD (id adhd-meds kept), Sleep agents, Orexin antagonists, Substance use and cessation (id sud-meds kept). Anxiolytics and Sedative-Hypnotics retires into the four new cards (alias on Benzodiazepines); ADHD Medications and Medications for Substance Use Disorders become cards in place, items and bank ids kept. Drawer patches in Tics and Tic Disorders, Sleep Problems, Panic Disorder and Other Anxiety, Stages of Change and Other antidepressants. All 11 READY (verify_all: six cards, five drawer-patched briefs); gate PASS, 0 failures (3 stale temporary allowlist lines, removed at the ship); render PASS; squeeze 0; pointers 60 checked, 1 problem (the Tics Pairs-with row, open since s157, so present was run by hand). Presented as approval s160, page 31727475b3d6.

**1. Decisions needed**
None.

**2. Calls made under section 3** (reply with the reversal to undo any)
1. REM sleep behavior disorder: "Melatonin first; clonazepam if symptoms persist" (UWorld library: melatonin first-line, clonazepam if symptoms persist; AASM 2023 lists both, all conditional). MSD orders clonazepam first. The round 1 text ("such as ramelteon") was wrong and is gone. Reverse: "clonazepam first".
2. Pregabalin adverse effects "sedation, weight gain" rest on the AAFP 2022 GAD and panic review, not a label (no Lyrica label cached; no fetch spent). Its quote opens mid-sentence ("which appears effective..."); a requote naming pregabalin is facts-only and is left for after the ship, since it would restale two receipts. Reverse: "drop the pregabalin line".
3. Benzodiazepine withdrawal onset: short-acting 1 to 2 days is the taught time (UWorld library 12 hours sits in a hover); long-acting "about 2 days to a week" (board 2 days plus MSD). The rebound bar is drawn over the alprazolam dosing interval (no board time exists).
4. Owner calls: the ADHD drug-choice lines stay on the ADHD card (there is no ADHD diagnosis brief: a coverage gap, and viloxazine is not taught); opioid use disorder in pregnancy (methadone or buprenorphine over abstinence) and the tobacco efficacy order stay on Substance use and cessation (no live owner).
5. Label-only facts sit in hovers marked as such: the zolpidem and eszopiclone complex sleep behaviors boxed warning and the ramelteon and fluvoxamine bar ("No board question on it found yet"); the orexin antagonist liver nuance (In practice: the label bars only severe impairment); the disulfiram 14-day window; the varenicline row's note that the boxed warning was removed. The hover title "Label warning" on that row is kept although its boxed warning is gone; the hover says so.
6. Brand names left out where no current label exists: Librium, Halcion, Serax, Dalmane, Tranxene, BuSpar, Atarax, Vistaril, Sonata.
7. ADHD practice item (stem): "urine drug screen negative" -> "positive for amphetamine only", item version 2, id kept. The negative screen contradicted the item's own answer (acc round 1). Reverse: "restore the stem" (the item would fail accuracy again).
8. Other anxiety agents adds gabapentin and pregabalin (AnKing); pregabalin will also appear on the B3 card.
9. Unverified-mark (pc-uv) lines kept and shown as such: clorazepate (Benzodiazepines); three on Other anxiety agents, buspirone's delayed onset among them.
10. Optional LOWs not applied (both cross masked spans or change a negation, so they would need another review round): Other anxiety agents, moving the hydroxyzine pointer to the end of its line; Sleep agents, "no better choice" referent and the "In practice" hover colon.
11. Lisdexamfetamine's gut activation is taught from AnKing alone (board tier, no label line).
12. Sleep Problems' benzodiazepine "Watch for" text has no drawer, so none was pointed to Benzodiazepines.
13. Word totals over the soft cap are reported, nothing cut (STANDING "Layers, not totals").
14. Orexin antagonists: the builder's hover inside the class tag was removed (it would have been a new display pattern).
15. Tool fixes: vendor_scan judges briefs.json by the page limit; a one-brief verify judges only its own P1 hedge lines; verify V1 skips the class tag line; aasm.org on the fetch allowlist (still bot-blocked).

**3. Edit list per brief** (S5 and S6 changes on the S3 build; new facts with quote, source, tier)

*Benzodiazepines*
- Long-acting withdrawal row "About 2 days to a week after the last dose", bar 2 to 7 days (UWorld library within 2 days, board; MSD, primary); the hover that repeated it dropped.
- Timeline label "Short- and intermediate-acting withdrawal (alprazolam, lorazepam)".
- Study mode: the masked older-adult drug list is no longer restated outside the Key point; the Mechanism line reads "Agents cleared by glucuronidation alone".
- Insomnia drawer -> Sleep agents; Where lines now name what the owner keeps ("Managing sedative or alcohol withdrawal once it starts", "Managing delirium").
- Three hedges restored.

*Other anxiety agents*
- New: "Pregabalin: sedation, weight gain" (AAFP 2022 review pa1, primary; see call 2).
- Buspirone hover: "Anxiety symptoms typically ease only once the dose reaches the upper range; taken on a schedule, not as a rescue dose".
- Interactions row result no longer states its masked rule; fragments after the pc-uv marks made whole sentences; a Benzodiazepines drawer on the buspirone comparison line.
- Rejected: "and falls" as unsourced (true for a sedating anticholinergic in an older adult; the line carries the pc-uv mark).

*ADHD*
- Stem edit (call 7); the danger row drops "a urine toxicology screen sorts them" (that card goes to Bipolar Disorder).
- Mania row: "An episodic course fits bipolar disorder better than chronic ADHD"; "New psychotic or manic symptoms are a label warning; in diagnosed bipolar disorder, a small risk of switching to mania".
- Monitoring Why cells rewritten so none names its masked check ("a baseline to compare against"; "Long-term use can affect a growing child"; "Boxed warning in youth; a rare serious label warning"; guanfacine and clonidine "Rebound after a stop").
- Flags fixes R2 to R9 applied (lost hedges and unquoted clauses).

*Sleep agents*
- RBD line (call 1): new fact r01, UWorld library "Melatonin is the first-line therapy; clonazepam may be used if symptoms persist" (board).
- Driving Why "Zolpidem label: next-day impairment if under 7 to 8 hours in bed"; the 5 mg zolpidem dose quoted from the label in the hover, not repeated.
- "Diphenhydramine is no better choice: heavy sedation for questionable benefit".
- The two label hovers: "Not tested on the boards" -> "No board question on it found yet" (no source shows the boards never test them).
- Flumazenil and the older-adult choice no longer named unmasked outside their own rows; Orexin antagonists drawer on the insomnia line; Sleep Problems chip kept on the RBD line (that brief teaches RBD).

*Orexin antagonists*
- Key point and Dependence: "No or low physical dependence" (k25, AnKing).
- Before-starting check "liver disease" (the label nuance stays in the Key point hover).
- New: "Suicidal ideation, dose-related (suvorexant label)" (b8, label).
- Narcolepsy commit back to class only; contraindication requoted as the full Quviviq sentence (dq1).
- "Each visit" -> "During treatment"; Where line "cognitive behavioral therapy first".

*Substance use and cessation*
- New: "Liver disease or opioid use: acamprosate preferred" (u10, UWorld, board); Key point naltrexone "avoid with liver disease, never with acute hepatitis or liver failure" (u03, k02 board; u12 label).
- Naltrexone start "7 to 10 opioid-free days" (vv1, label), bar 0 to 67 percent; the MSD "at least 7" dropped.
- Nicotine replacement: caution with serious angina or within 2 weeks of a myocardial infarction (w20, label).
- Disulfiram: In practice hover, reactions "up to 14 days after" (ds6, label).
- Buprenorphine: the whole label sentence naming methadone (sx2); "after methadone, precipitated withdrawal may be more likely".
- Chart Why "a long half-life keeps the agonist in the body"; the receptor-residence claim cut as unsourced.
- Where line "Which drug for alcohol or opioid use disorder" dropped (this card owns it); overdose pointer stays on Substance Intoxication and Withdrawal.

*Drawer patches* (one review lane, 15 of 15 PASS): Tics "ADHD Medications" -> "ADHD"; Sleep Problems' sedatives drawer -> Sleep agents; Panic alprazolam row and alcohol row -> Benzodiazepines; Stages of Change and Other antidepressants -> "Substance use and cessation".

**4. Word count** (above the bank, hover text included)
Benzodiazepines 828, Other anxiety agents 573, ADHD 938, Sleep agents 589, Orexin antagonists 440, Substance use and cessation 1026. All six pass the 420-word MAOI golden (the build counts without hovers were 643, 439, 717, 441, 310, 693); board-keyed, nothing cut (call 13). Patched briefs (drawer labels only): Tics 1654, Sleep Problems 2014, Panic 1937 (over 1300, pre-existing), Stages of Change 506, Other antidepressants 642.

**5. Reviews**
- Round 1 (7 agents): accuracy 1 HIGH (Sleep agents RBD drug), 4 MED, 8 LOW; read all six FAIL (study-mode Why cells and rows, ownership lines; 14 MED accepted); flags 4 MED, about 30 LOW (lost hedges, unquoted clauses); drawer patch lane 15 of 15 PASS. 28 items accepted, 5 rejected.
- Round 2 (6 agents): 0 HIGH, 3 MED (orexin liver check; orexin narcolepsy commit unmasked; ADHD guanfacine Why naming its check), LOWs; 25 items, 23 applied, 2 rejected.
- Round 3 (2 agents): 0 findings. Round 4 confirmation (3 agents): 0 HIGH or MED; 4 LOW replacements (2 applied, 2 reverted as optional). Round 5 (Sleep agents, 2 agents): 0 findings. All six READY.
- Packet errors: none in content. Two flags lanes ran out of calls before writing their receipt (the lead saved the handed-back text); the launch gate refused the role name "flags-review" (it is "flag-review").
- Sonnet against Opus: Opus accuracy caught all three clinical sourcing errors (RBD drug, naltrexone in liver disease, the self-contradicting ADHD stem), which Sonnet read and flags missed. Sonnet read caught the study-mode leaks and ownership lines (not the accuracy part's job). What Opus missed: its own round 1 replacement on the orexin narcolepsy commit put a masked answer back in view, and Sonnet read caught it in round 2.

**6. Cost**
- Builders (Opus): 8 agents, 485 calls, 47.60M of the 40M plan (cards from the large s157 briefs needed over 90 calls; four lanes finished by the lead).
- Reviewers: 20 agents, 212 calls, 9.88M (acc Opus 6 agents 3.24M; read Sonnet 7, 2.28M; flags Sonnet 6, 4.16M; patch Sonnet 1, 0.20M) against your 10M plus the 0.5M round 5 approval.
- Wave: 28 agents, 697 calls, 57.48M of 58.1M (all within the raised caps).
- Lead: 6 measured chat rows, 121.7M (chat 1 unmeasured) against the 90M figure: over by about 32M. Start-up context this chat 179k (37% above the 130k baseline: the State and batch file have grown). Batch total about 179M.
- Per card: about 9.6M agents (7.9M builder, 1.7M review) plus about 20M lead; the lead is two thirds of the cost, driven by six chats and the round-by-round reviews of LOW-only parts.
- Proposed B3 (s161, five cards incl. Lithium and anticonvulsants; needs your Q4 answer first): builders 6 agents, 450 calls, 42M (budget the large lanes at 100 calls up front instead of relaunching); reviewers 18 agents, 230 calls, 10M; lead 100M with LOW fixes applied only through reps.py replacements that replay, so no LOW-only edit stales a receipt and forces a confirmation round (rounds 4 and 5 here).

Reply "ship" to publish, or name what to change.
