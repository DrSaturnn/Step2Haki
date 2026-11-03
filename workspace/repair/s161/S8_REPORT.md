**s161 final report: Psych Pharmacology B3 (five class cards)**
SSRIs (pc-ssri), TCAs (pc-tca), Lithium and anticonvulsants (mood-anticonv, card in place, id and 9 items kept; was Anticonvulsant Mood Stabilizers), Cognitive agents (pc-cog), Other agents (pc-other). Bipolar Disorder gets one drawer label patch (target unchanged). Q4 "keep": SSRI Adverse Effects, Anticholinergic and Tricyclic Toxicity, Lithium Therapy and Dementia stay as the deep briefs the cards link to; no item moves out of them. After this ship 01 Antidepressants, 03 Mood and cognition and 06 Substance use and other are complete (14 of 18 cards); only 02 Antipsychotics stays greyed.

**1. Decisions needed**
None.

**2. Calls made under section 3** (reply with the reversal to undo any)
1. Owner calls (no live owner, so the card holds it with no drawer, s160 precedent): obesity drug choice (Other agents); tricyclic for neuropathic pain, migraine or tension headache prophylaxis, and low-dose doxepin for insomnia (TCAs). Narcolepsy: "modafinil is first line" (owner Sleep Problems names modafinil only; the second-line clause is left to it). Reverse: name the brief that should own it.
2. Lithium and anticonvulsants: one "How NBME framed it" block holding four NBME items (c01111 with data-nbme; 99c45f, d434f3, c85661 as framing and drawers). pc-benzo and adhd-meds already hold several items in that block, so this is the shipped pattern, not a new display. Reverse: "one NBME item per block".
3. Valproate range 50 to 125 mcg/mL (UWorld) over AnKing's 60 to 120 (conflict recorded in the facts).
4. Lamotrigine restart taught as the board rule (after any sudden stop, restart at the starting dose); the label's 5 half-lives are not shown and no "In practice:" hover was added (the item's 3-week gap gives the same answer under the label). Reverse: "add the lamotrigine label hover".
5. Lithium's mechanism in mania is taught as unknown (label). No new lithium item (it would duplicate Lithium Therapy's).
6. NBME items psych-cms8-99c45f, psych-cms-d434f3, psych-cms-3a30eb and psych-cms8-3b2f19 have no coverage.csv row (queue only), so no data-nbme attribute was added for them.
7. Cognitive agents: no danger rows (no board source tests a class reaction); the titration chart uses label times only (Aricept 4 to 6 weeks, Exelon at least 4 weeks per step and a restart after more than 3 missed days, memantine at least 1 week); anti-amyloid antibodies left out (MSD only); two unverified-mark lines kept and shown ("ECG if syncope", "caregiver observations"); bradycardia, heart block, syncope and the monitoring rows are primary-source content on a thin-coverage card.
8. Phentermine "contraindicated in cardiovascular disease, hypertension and heart failure" (AnKing); the label's "uncontrolled hypertension" list sits in an "In practice" hover.
9. Brand names left out where no current label was found by name: Razadyne, Namenda, Adipex, Elavil, Tofranil, Eskalith, Depakene.
10. TCAs: no timeline chart (overdose timing belongs to Anticholinergic and Tricyclic Toxicity, with no board hours; MAOI washouts to MAOIs).
11. SSRIs: the new agitation and akathisia seed line was not placed (no source opened). The SSRI Adverse Effects onset line ("may take up to 6 weeks", read by a reviewer as the outer limit) is a deep-brief fix, queued in OPEN_WORK, not made here.
12. Word totals over the soft cap are reported, nothing cut (STANDING "Layers, not totals").
13. pc-other preflight P3: the distractor "Space the two doses 12 hours apart" is named only in its item (carried; a distractor does not need a line on the card).
14. Tool changes: brief-build call budget 90 -> 100 and a per-brief budget in build_spec.json (from the s160 report); verify.py replay now undoes one replacement at a time in repeated passes, testing the hash after each (test_condpass 56 passed), which made pc-tca READY with no extra review after two replacements stacked on one span; bank_sync.py rewrites a shell bank from the builder's items (the pc-ssri bank had gone stale since chat 3).

**3. Edit list per card** (S5 to S7 changes on the S3 build; new facts with quote, source, tier)

*SSRIs*
- Your ruling (chat 4): the adequate-trial row reads "At least 4 to 6 weeks at a therapeutic dose" (new fact uTrial, UWorld: "An adequate antidepressant trial is generally considered to be at least 4-6 weeks at a therapeutic dosage", board), bar 4 to 6 weeks, matching Major Depressive Disorder; AnKing's "6 weeks at full dose" is a hover. The new item q_b204614b (sertraline at 2 weeks: continue) follows the row in its key and distractor reasons; answer unchanged.
- Fluvoxamine and theophylline: "cut by a third" (a 2-fold error) -> "theophylline to a third of its dose, with levels" (new fact sxT1, fluvoxamine label 5.8: "its dose should be reduced to one-third of the usual daily maintenance dose and plasma concentrations of theophylline should be monitored", label).
- No board quote ranks the SSRIs, so the Key point and the citalopram and fluoxetine rows were reworded to the quotes: dose-dependent QT, avoided after a recent heart attack; the first-trimester heart-defect signal for paroxetine; fluoxetine's long half-life, so no taper. The item reason "the most in its class" removed.
- New adverse-effect line: an abrupt stop of a short half-life SSRI such as paroxetine brings flu-like, neurologic and psychiatric symptoms within days (facts ss01, ss03), with the SSRI Adverse Effects chip. Serotonin syndrome stays in the Interactions table.
- Owner line "Which antidepressant, and the next step after an adequate trial" (Major Depressive Disorder). Citalopram overdose note: "may be delayed: keep the heart monitored"; the Mechanism line's "isolated overdose is usually well tolerated, except with citalopram" now cites sx35.

*TCAs*
- "GABA-A antagonism: seizures" is its own line (the clomipramine hover moved with it).
- Recent heart attack row Why "Both labels warn about the acute recovery period" (a "contraindicated" Why would have repeated the masked "Do not use"); QT row Why "An abnormal result adds to the arrhythmia risk".
- The tca-tox chip moved to the Result cell.

*Lithium and anticonvulsants*
- Rows renamed "Carbamazepine in Asian ancestry" (the allele stays in the masked check) and "Confusion on valproate", note "Once confirmed: stop valproate and look for an underlying urea cycle disorder".
- Monitoring Why cells no longer name the masked test (valproate; carbamazepine before and during; oxcarbazepine "An adverse effect in about 2.5%"; topiramate "Its acid-base label warning"). "Faster valproate clearance" in the Result so the masked "Its level falls" has one referent; carbamazepine "Self-induction changes how the drug is handled early on".
- DRESS note "Eosinophilia is often present (lamotrigine label)"; speech dysfunction added to topiramate; "mild thyroid dysfunction" removed from a list; chips read "Lithium Therapy".
- Rejected: an "In practice" lamotrigine hover (call 4); "the question asks" -> "you are asked" (the NBME framing wording used 11 times on the page).

*Cognitive agents*
- Memantine titration: the cut-off fact m8 is now the whole label sentence ("The dose should be increased in 5 mg increments to 10 mg/day (5 mg twice daily), 15 mg/day (5 mg and 10 mg as separate doses), and 20 mg/day (10 mg twice daily).", label); Why "the dose rises in 5 mg steps to 20 mg a day". The old "to 10 mg a day" read as the target.
- Drawer line "Delirium from anticholinergic drugs"; the unverified mark dropped from the MSD-sourced row; Result and Why cells no longer name the masked rule or check.
- Owners confirmed: Parkinson disease dementia (Parkinson disease), physostigmine in tricyclic poisoning (tca-tox), organophosphate poisoning (Toxidromes).

*Other agents*
- Your ruling (chat 4): the masked heart-disease commit is back to "(phentermine, diethylpropion or benzphetamine)"; adding phentermine-topiramate had no packet quote on heart disease. "Narcolepsy daytime sleepiness: modafinil is first line".
- Subtitle "wake-promoting and weight-loss agents · modafinil · armodafinil · phentermine · phentermine-topiramate"; the obesity Uses line adds phentermine-topiramate (Qsymia label, qs1).
- "uncontrolled" out of the commit and the Monitoring check (it is the label's In practice wording, not the board's); modafinil's mechanism hedged ("thought to raise orexin and monoamine signaling"); Why cells "Alertness may not be fully restored" and "Rules out a contraindication it shares with phentermine alone".
- Rejected: "modafinil or armodafinil is first line" (the owner names modafinil only).

*Bipolar Disorder* (patch lane, 3 of 3 PASS): drawer label "Anticonvulsant Mood Stabilizers" -> "Lithium and anticonvulsants".

**4. Word count** (above the bank, hover text included)
SSRIs 890, TCAs 689, Lithium and anticonvulsants 1569 (over 1300; the 2100-word brief it replaces was over too: ten danger rows, the onset chart, interactions and monitoring tables, four NBME items), Cognitive agents 708, Other agents 565. Build counts without hovers 616, 557, 1326, 594, 442. Bipolar Disorder 1691 (over 1300, pre-existing; label only). Board-keyed, nothing cut (call 12).

**5. Reviews**
- Round 1 (9 reviewer agents plus 1 relaunch): accuracy 0 HIGH, 2 MED (fluvoxamine dose 2-fold error; "uncontrolled" in the phentermine commit), 9 LOW; read all five FAIL (19 MED, 27 LOW: study-mode Why cells naming masked checks, ownership lines); flags 1 HIGH (Other agents' masked commit), 3 MED (unquoted SSRI ranking, two on Cognitive agents), 14 LOW; patch lane 3 of 3 PASS. Rejections recorded with evidence in repair/s161/adj_r1.md.
- Round 2 (4 agents): 1 MED (memantine titration number), 15 LOW; 4 rejected.
- Round 3 (5 agents): 1 MED (the phentermine-topiramate commit, settled by your ruling), 4 LOW.
- Round 4 (3 agents, pc-ssri and pc-other): 0 findings. All six READY.
- Packet errors: none in content. Tool gaps: outline_flags.txt shows no quotes under each line, so flags reviewers grep facts.json and one lane ran out of calls (relaunched, PASS); RECEIPT_FORMAT.md is missing from the flags lane folders; the cards.md packet path. The stale pc-ssri shell bank was a lead tool error, not a reviewer one.
- Sonnet against Opus: Opus accuracy caught the fluvoxamine 2-fold dosing error (lead confirmed against the label) and the phentermine commit wording. Sonnet flags caught the HIGH, the SSRI ranking with no board quote, and in round 3 an unquoted name that Opus's own round 2 replacement had added. Sonnet read caught the memantine titration MED, which Opus accuracy passed in round 1, and all the study-mode leaks.

**6. Cost**
- Builders (Opus): 5 agents, 332 calls, 40.32M of 42M (6, 450 planned); no relaunch and no lead-finished lane (s160 had 2 and 4). Lanes: MOOD 10.66M, SSRI 9.54M, TCA 7.98M, COG 7.61M, OTHER 4.53M.
- Reviewers: 21 agents, 197 calls, 8.30M of 10M (acc Opus 7 agents 3.16M; read Sonnet 6, 2.10M; flags Sonnet 7, 2.91M; patch Sonnet 1, 0.13M). Agents ran 3 over the 18 planned, within the max_agents 26 you approved for round 4.
- Wave: 26 agents, 529 calls, 48.62M of 52M.
- Lead: chats 1 to 4 74.9M measured, chat 5 about 7M so far: about 82M of 100M. Start-up context 133.7k (baseline 130k; the s160 chat ran 179k). Batch total about 131M.
- Per card: about 9.7M agents (8.1M builder, 1.7M review) plus about 16M lead (s160: 9.6M plus 20M).
- Proposed B4 (s162: Atypical, Typical, Anticholinergic, Tardive dyskinesia agents; Q4 "keep" carries, so Antipsychotic Adverse Effects stays as the deep brief): builders 5 agents, 380 calls, 34M (95 calls a card up front, 1 spare); reviewers 18 agents, 200 calls, 8M; lead 80M. Wave 23 agents, 580 calls, 42M.

Reply "ship" to publish, or name what to change.
