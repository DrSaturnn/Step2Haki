# s150b independent S8 audit

Auditor: fresh independent Codex S8 agent. Date: 2026-10-23 EDT. Scope: the complete new pms-pmdd and parkinson briefs; only the authorized changes in somatic, psych-medical, mdd, bipolar-mania, ssri-effects, antipsych-effects and delirium. No subagents, web requests, content repairs, check changes or receipt changes were made by the auditor.

**Verdict: FAIL pending the four MED findings below.** There are no HIGH findings. This report describes the frozen r2 candidate before lead repairs; it does not grant presentation or ship approval.

Frozen page: `local/s150b/review/final-r2.html`; independent rebuild: `local/s150b/audit/final.html`. Both SHA-256: `8f3c09f90edcf766698531d147303f306af4fa7abb97fb7c5ddce8f2090f34ff`.

## Findings by severity

### MED A: regenerating supplemental facts makes six reviewed folders not READY

The required from-scratch sequence regenerated `facts_spec_s150b.json`, rebuilt the folder, checked quotes/cards, then ran full serial `verify_all.py`. SOMA, MED, N1, N4, APAE and N2 became MECHANICAL PASS, NOT READY: acc and flags facts dependencies are stale. The changed fields are only the supplemental facts' `population` metadata. PMS, PD and MDD reproduce their reviewed facts and remain READY. The rendered page is unchanged.

Evidence: `local/s150b/audit/mechanical.json`, `verify-all.log`, `initial-regeneration-differences.json`, and each affected folder's `facts_spec_s150b.json`, `facts_s150b.json`, `facts.json` and `verify_all.log`. The private pushed originals were compared with the regenerated rows. The exact affected fact IDs are preserved in the private JSON. This differs from the S7 record of nine READY and is a reproducibility defect, not a new clinical error.

Required answer: make each spec and generated fact metadata agree deliberately, regenerate twice to prove stability, then rerun full verification. Exact restoration of already-reviewed metadata can preserve current receipts when the dependencies match again. Any deliberately changed metadata needs fresh acc/flags review. Do not edit dependency hashes or checks to accept the mismatch.

### MED B: a new PMS/PMDD owner pointer is not actionable in bipolar-mania

The Pairs with block begins with raw `Part I` before its first owner label. The existing `pairs()` presentation function sets `items.bad` on that leading text and returns before it builds the owner rows. The newly added PMS/PMDD title therefore stays italic prose rather than becoming an owner button. The old leading text is inherited, but the new pointer is in this batch's scope.

Evidence: N1 `delta_s150b.json`; the frozen page's `pairs()` function; `local/s150b/s8/audit-display-final.png`, bipolar-mania component. Reproduce after page initialization: inspect the Pairs with block in `#bipolar-mania`; it lacks a `.qx-pairs` owner list and has no PMS/PMDD owner button. Adjacent MDD and SSRI owner components render correctly.

Required answer: repair this block's markup within the brief, preserving any necessary Part I context in a supported position. Verify the new owner button reaches pms-pmdd in a running page, then obtain normal read/display follow-up and any other dependencies reopened by the rendered change. The read/display roles passed a real new navigation failure.

### MED C: PD S148 adds an unsupported referral action

PD claim S148 combines diagnostic reconsideration with an explicit referral action. Its cited facts u29, u34 and u35 support clinical evaluation, alternate-diagnosis features and treatment response; they do not state the referral action. Searching the held Parkinson library article did not locate a referral recommendation. Clinical plausibility does not substitute for the required claim-level source support.

Evidence: PD `claim_map.json` S148 and `facts.json` u29/u34/u35; private `worksheet-private.txt`. The latest acc receipt is `parkinson_acc_r2.md`; it passes the final brief, while its explicit changed-line discussion does not answer this carried new-brief clause. This is an acc source-entailment miss, also relevant to flags review. Only one claim-meaning error was found, so the two-meaning-error trigger for a mandatory whole-claim expansion was not reached.

Required answer: remove the unsupported action or cite a held board-source passage that states it, then review the changed claim normally. Do not fetch a new source merely to defend an optional action.

### MED D: inherited card dispositions overstate child-statement coverage

The parent-card samples are largely taught correctly, and every explicit scope/conflict was inspected. Some inherited high-yield children are nevertheless marked covered by claim IDs that teach another part of their parent. Examples:

- PMS `1485037217772.882b8c9f79` inherits `covered:S082,S084`, which point to treatment and another-drug-trial statements rather than the child's comorbidity-risk statement. The body prompts screening, but that does not teach the stated increased-risk relationship.
- PD `1542317772683.d210e1bef3` inherits `covered:S047,S158`, which teach clinical recognition rather than the child's imaging/pathology comparisons. Those omitted comparisons are not taught elsewhere in the complete PD claim list.
- PD `1481857897457` points to S005/S019, which establish aggregate composition and distribution; they do not teach the card's primary-location contrast. That optional depth can receive an honest scope disposition instead.

Evidence: PMS/PD `cards.md`, `cards_disposition.json`, and cited `claim_map.json` IDs; the selected parent IDs and all explicit scope/conflict IDs are recorded in `local/s150b/audit/sample_manifest.json` and the private worksheet. Correct handling of the old age-cutoff conflicts, the progression-mechanism conflict, and the existing explicit scopes was confirmed.

Required answer: audit the remaining children in both new card lists. Give each untaught child a specific scope/conflict/owner disposition or point to claims that actually teach it. Optional molecular or imaging detail need not be added to the visible brief. Fresh acc review should verify the full corrected disposition set. This is a board-coverage bookkeeping miss by the acc role, not evidence that the visible bank keys are wrong.

### LOW carried, unchanged

The prior deferred MPTP terminology LOW is accurately disclosed. The term is identified by its board-keyed name and contaminant context; no unsupported chemical-name expansion or optional removal was applied. The native Stage heading is permitted by the existing rule. Neither is promoted to a new MED finding.

## From-scratch mechanical result

The lead was told before verification began and after all verification ended. No lead tracked edits occurred during the verification interval. Every folder was rebuilt. The new briefs used `facts_spec.json`; existing targeted folders used `facts_spec_s150b.json` and the shipped-baseline replay builder, not archived legacy builders. Full `verify_all.py --jobs 1 --log` ran, including each folder's render, source, tail, identity, preview gate, browser render, preflight, vendor and number checks. No `--fast` substitute was used.

| Brief | Verified facts | Relayed / failed | Full mechanical | READY after regeneration |
|---|---:|---:|---|---|
| pms-pmdd | 45 | 0 / 0 | pass | READY |
| parkinson | 84 | 0 / 0 | pass | READY |
| somatic | 75 | 0 / 0 | pass | stale acc/flags facts |
| psych-medical | 30 | 0 / 0 | pass | stale acc/flags facts |
| mdd | 70 | 0 / 0 | pass | READY |
| bipolar-mania | 36 | 0 / 0 | pass | stale acc/flags facts |
| ssri-effects | 48 | 0 / 0 | pass | stale acc/flags facts |
| antipsych-effects | 37 | 0 / 0 | pass | stale acc/flags facts |
| delirium | 25 | 0 / 0 | pass | stale acc/flags facts |

All 450 fact quotes verify with zero relayed or failed fragments. The final batch build and gate pass: 182 briefs, 2,197 items, 39 checks, zero failures. Full verify_all exits 1 because six folders are not READY, as it should.

Standalone card checks pass in seven folders. N4 and N2 have neither legacy `cards.md` nor `cards_disposition.json`; their standalone checks return 1 for missing inputs, while verify correctly treats the check as inapplicable. No new card work is claimed for those pointer-only scopes. Logs retain these initial returns rather than relabeling them passes. Baseline lint advisories remain disclosed; source-meaning samples independently checked the new numerical and hedge-bearing claims.

Initial public/private tracked trees were clean on wip/s150b. The State and lead reported the checkpoints pushed. Local HEAD and remote-tracking ref evidence is saved in `local/s150b/audit/ref-evidence.json`; no token or remote authentication material was read. The batch file records S1-S7, adjudications, role differences, exceptions and unresolved LOWs.

## Meaning, board evidence and bank

The independent initial spread selected 15 claim IDs per new brief, then added every digit-bearing clause, complete bank reasoning and targeted urgent/differential/workup/treatment claims. All 126 PMS and 186 PD claim texts were read for context, and their held fact sets were inspected. The reproducible spread is:

- PMS: S001, S010, S019, S028, S037, S046, S055, S063, S072, S081, S090, S099, S108, S117, S126.
- PD: S001, S014, S027, S041, S054, S067, S080, S093, S107, S120, S133, S146, S160, S173, S186.

All additional IDs, all numeric IDs and the chosen covered-card parents are in the private sample manifest. PMS had only six parent cards, so all six were checked. PD included at least ten covered parents plus every parent needed to inspect all explicit scopes/conflicts. S148 and the card-disposition findings above are the exceptions to otherwise supported meaning samples. No second clinical meaning error, changed numerical cutoff, dropped outcome-changing hedge or bank/body contradiction was found.

The complete new bank was read: six PMS and nine PD original items, all with key and two distractor reasons. New stems contain 31-36 words under a direct three-line stem count and fit the 30-40-word rule. Keys match the held board decisions; original stems are not copied question narratives. The diary-first source ownership and PD depression ownership agree with the held board ledger; no invented Parkinson attempt or NBME source was introduced. The nearest-neighbor choices use the brief's diagnostic or treatment contrasts.

All seven existing bank blocks match their shipped pre-batch baseline. New item IDs, versions and option identities match the S3 freeze, and no changed key or choice needs an unrecorded version bump. Raw bank equality and hashes are retained in `bank-evidence.json`. Targeted SOMA S087 and MED additions were read against their own held quotes, surrounding body and bank. The five other old scopes are owner/pointer changes; their source associations are supported apart from the rendering failure in N1.

## Display and consistency with Claude goldens

The built page was compared with septic-hip, sjia, scfe and the limp hub. Phone script and study-mode images were inspected side by side with septic-hip in `comparison-phone.png` and `comparison-phone-study.png`; the combined final display image adds workup and treatment comparisons plus old owner regions. The current MED workup phone sheet was also inspected directly. The SOMA changed hover's wording was inspected in source; an opened-hover screenshot was not independently inspected. This limitation must remain explicit in follow-up display evidence.

The new disease briefs use the same eight-step order, three bottom-line entries with bold criteria, template-ordered script with exactly two Insights, First step result pairing, Targeted tests, diagnostic/next-step and Skip bands, clue table, pause point, treatment ladder with Raise, follow-up table, Practice, Pairs with and Transferable rule. There is no fabricated NBME block when no NBME source exists. PD's Stage label is an allowed native term. The targeted MED workup row follows the existing clue/points-to/next-step card grammar; no whole old hub was reauthored.

Both new scripts preserve visible retrieval prompts while masking answers. PD's second prompt is visibly clear in the stable comparison image, confirming the earlier tall-capture finding was an artifact. Workup/treatment columns become readable stacked phone cards like the golden. Owner cards are consistent in the inspected old regions except N1. Neither new script showed squeezed text or a new hover button glued to its preceding word.

PD puts additional system/pathology detail in the collapsed systems panel and medication depth in hovers; board decisions remain visible. The new explicit Insights questions differ from the older declarative golden Insight style, but conform to the current retrieval rule. This is an allowed pattern, not a defect. Row wording and label density otherwise fit the current golden style.

Canonical new-body counts reproduce 781 words / 126 claims for PMS and 989 / 186 for PD. A separate same-DOM extraction, including interface/label words and any panel text not excluded by that extractor, provides the following comparison. These are comparable exploratory counts, not the formal word-cap counts:

| Brief | Same-extractor words before bank | Claim map count |
|---|---:|---:|
| pms-pmdd | 976 | 126 |
| parkinson | 1328 | 186 |
| septic-hip | 1329 | 136 |
| sjia | 1624 | 167 |
| scfe | 1457 | 149 |
| limp | 1393 | not located |

PD is comparable to septic-hip in this broader extraction and thinner than sjia; PMS is shorter in keeping with its narrower decision set. No density defect is inferred. The frozen claim-count evidence and exact extraction limits are retained privately in `comparison-metrics.json`.

The S3 native audit limits remain in force: native desktop below-threshold counts were 34 light / 37 dark; legacy small labels and the SSRI study widget remain baseline advisories. They are not reported as zero. The lead's focused component checks and current computed contrast support the scoped display evidence; this auditor did not rerun the entire native pixel matrix. Full current approval captures are the lead's responsibility after all repairs. Initial S8 display is not an approval of the unrepaired page.

## Proposed additions to CODEX_LEAD section 7

These are recommendations for Jonathan, not approved rule changes. Keep each addition numbered when integrating it with the existing list.

1. **Freeze generated evidence, not manually saved products.** Before review freeze, regenerate every current spec twice and compare canonical outputs; use per-fact or a deliberate common population where needed. Case: six s150b supplemental specs changed fact metadata only when independently regenerated. Recommend adding.
2. **Check the action verb in a source sample.** A quote supporting a diagnosis or test does not automatically support an added referral, treatment escalation or follow-up action in the same sentence. Case: PD S148. Recommend adding.
3. **A covered parent is not blanket coverage of its children.** Check each inherited high-yield statement against the cited claim IDs; use explicit scope/conflict/owner entries when it differs from the parent decision. Case: PMS comorbidity and PD imaging/location children. Recommend adding.
4. **Run every new owner pointer in the actual page.** Even in an unchanged shared renderer, inspect the generated owner control and activate its destination in each amended Pairs with block. Case: inherited leading Part I prevented N1's new PMS pointer from rendering. Recommend adding.

## Calls, limits and required closeout

Actual spend: **35 counted evidence operations of the expanded 35-operation cap**. This counts the mandatory direct documentation opens separately, including one failed initial handoff-path attempt; direct helper-document reads separately; each consolidated scripted evidence worksheet as one read; each screenshot as one image operation; and each mechanical launch/poll and final report write. Machine-internal reads performed by required generation/verification are not counted as separate reviewer calls, per the lead's clarified budget. Coordination messages are separate from evidence operations. Reviewer tokens are unknown and were not estimated.

Private source material stays in ignored `local/s150b/audit/`; no vendor quotations or question text are included here. The first oversized consolidated worksheet was truncated in tool output; subsequent compact source, claim, bank, card and receipt extracts supplied the reviewed material. The auditor did not independently inspect every legacy claim or bank source, consistent with the targeted old-brief scope, and did not inspect an opened SOMA hover or rerun the full native pixel audit.

The lead must answer all four MED findings, retain the initial failed evidence, complete the reopened follow-up roles, provide any missing scoped hover display proof, rerun deterministic generation and full verification, and obtain an independent follow-up verdict before approval.py present. No presentation or ship authorization is implied by this report.
