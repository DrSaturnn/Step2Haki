# Changelog

Newest first. Each entry is the commit body written by tools/ship.sh.

## 2026-10-03 s69: merge batch 2: Wrist and Hand Pain and Numbness (scaphoid + cts + dequervain), Hip and Thigh Pain and Numbness (gtps + meralgia), Osteoporosis Screening and Treatment (osteoporosis + bs-dexa-highrisk); two audit rounds, 0 CRITICAL

```
Page: 212 briefs, 2117 items -> 208 briefs, 2110 items
Briefs REMOVED (4): cts, dequervain, meralgia, bs-dexa-highrisk
Briefs changed (3):
  - scaphoid (Wrist and Hand Pain and Numbness): 2 items added (q_17521eba78bcdfa1b8df, q_930ee52b2fc6abead7ba); items edited (q_00b06cea29d55a63a813, q_c477231dbf5e51b19a5e, q_235b617bfe7b59878451, q_ce28a15d91095602b63e, q_31393377f10253c3911e, q_da3d8ec8eb3b59b2b005, q_7efda076c41655479f31, q_b5188f20bc815957aa2b, q_98250ef442c150cdac2c, q_ae3a0b61449f581fb06c, q_feaa85f92e7a585ca84a, q_60378525225557a59eec, q_b09c11d6366f59a8a9a9, q_b4eb1443b5bb57e58c6e); versions bumped (q_00b06cea29d55a63a813 v1->v2, q_c477231dbf5e51b19a5e v2->v3, q_235b617bfe7b59878451 v1->v2, q_ce28a15d91095602b63e v1->v2, q_31393377f10253c3911e v1->v2, q_da3d8ec8eb3b59b2b005 v1->v2, q_7efda076c41655479f31 v1->v2, q_b5188f20bc815957aa2b v1->v2, q_98250ef442c150cdac2c v1->v2, q_ae3a0b61449f581fb06c v1->v2, q_feaa85f92e7a585ca84a v1->v2, q_60378525225557a59eec v1->v2, q_b09c11d6366f59a8a9a9 v1->v2, q_b4eb1443b5bb57e58c6e v1->v2); attrs set (brief data-bp,data-replaces; q_00b06cea29d55a63a813 data-lead-in,data-src; q_c477231dbf5e51b19a5e data-src; q_235b617bfe7b59878451 data-lead-in,data-src; q_ce28a15d91095602b63e data-lead-in,data-src; q_31393377f10253c3911e data-lead-in,data-src; q_da3d8ec8eb3b59b2b005 data-lead-in,data-src; q_7efda076c41655479f31 data-d1,data-d1-id,data-lead-in,data-src; q_b5188f20bc815957aa2b data-lead-in,data-src; q_98250ef442c150cdac2c data-lead-in,data-src; q_ae3a0b61449f581fb06c data-lead-in,data-src; q_feaa85f92e7a585ca84a data-lead-in,data-src; q_60378525225557a59eec data-lead-in,data-src; q_b09c11d6366f59a8a9a9 data-lead-in,data-src; q_b4eb1443b5bb57e58c6e data-lead-in,data-src); prose edited (+4705 chars)
  - gtps (Hip and Thigh Pain and Numbness): 2 items added (q_d0fb52f5786860c4fd9a, q_7f1e3221cf4b2f836d91); items edited (q_44001f1ef471c03117d7, q_2460bcc21c925357a433, q_0fafdd8de260501f98f0, q_0209b3c970df55b2b276, q_fae39303b47952eaacdd, q_7e828e8c4d4e5ac4b33b, q_78cd40d56320551289db, q_eeba8501aa2f54fdae1f, q_30cb97bbfe2453c4a04b, q_3001b36e0d3a5bb0b7b6, q_9f1b5e4c056d58778872, q_41a6b56a3b715cd694c3, q_f9c0419a0d4c547ab36c, q_aca55113683b5475bea7); versions bumped (q_44001f1ef471c03117d7 v1->v2, q_2460bcc21c925357a433 v2->v3, q_0fafdd8de260501f98f0 v1->v2, q_0209b3c970df55b2b276 v1->v2, q_fae39303b47952eaacdd v1->v2, q_7e828e8c4d4e5ac4b33b v1->v2, q_78cd40d56320551289db v1->v2, q_eeba8501aa2f54fdae1f v1->v2, q_30cb97bbfe2453c4a04b v1->v2, q_3001b36e0d3a5bb0b7b6 v1->v2, q_9f1b5e4c056d58778872 v1->v2, q_41a6b56a3b715cd694c3 v1->v2, q_f9c0419a0d4c547ab36c v1->v2, q_aca55113683b5475bea7 v1->v2); attrs set (brief data-bp,data-replaces; q_44001f1ef471c03117d7 data-lead-in; q_2460bcc21c925357a433 data-lead-in,data-src; q_0fafdd8de260501f98f0 data-d1,data-d1-id,data-lead-in,data-src; q_0209b3c970df55b2b276 data-lead-in,data-src; q_fae39303b47952eaacdd data-lead-in,data-src; q_7e828e8c4d4e5ac4b33b data-lead-in,data-src; q_78cd40d56320551289db data-lead-in,data-src; q_eeba8501aa2f54fdae1f data-lead-in,data-src; q_30cb97bbfe2453c4a04b data-lead-in,data-src; q_3001b36e0d3a5bb0b7b6 data-lead-in,data-src; q_9f1b5e4c056d58778872 data-lead-in,data-src; q_41a6b56a3b715cd694c3 data-lead-in,data-src; q_f9c0419a0d4c547ab36c data-lead-in,data-src; q_aca55113683b5475bea7 data-lead-in,data-src); ITEMS REMOVED (q_51678cf558d4534ab9ef); prose edited (+4003 chars)
  - osteoporosis (Osteoporosis Screening and Treatment): 2 items added (q_163bf1460c3bfdcc7fdb, q_4b54e273041093c2e843); items edited (q_c6114373cc3256e6bda1, q_9d537e5889785e8a9e13, q_09e7f6e15ab95cbd91c2, q_1032b6713b4050b79ac0, q_2953436ba09957738b08, q_774f59fb6fe759cf9e63, q_0263cf8d393f5319a3e7, q_63eb9b1c14fe59598997, q_ba420652bd9b571595cf); versions bumped (q_c6114373cc3256e6bda1 v2->v3, q_9d537e5889785e8a9e13 v3->v4, q_09e7f6e15ab95cbd91c2 v1->v2, q_1032b6713b4050b79ac0 v1->v2, q_2953436ba09957738b08 v1->v2, q_774f59fb6fe759cf9e63 v1->v2, q_0263cf8d393f5319a3e7 v1->v2, q_63eb9b1c14fe59598997 v1->v2, q_ba420652bd9b571595cf v1->v2); attrs set (brief data-replaces; q_c6114373cc3256e6bda1 data-lead-in,data-src; q_9d537e5889785e8a9e13 data-d1,data-d1-id,data-lead-in,data-src; q_09e7f6e15ab95cbd91c2 data-lead-in,data-src; q_1032b6713b4050b79ac0 data-lead-in,data-src; q_2953436ba09957738b08 data-lead-in,data-src; q_774f59fb6fe759cf9e63 data-d1,data-d1-id,data-lead-in,data-src; q_0263cf8d393f5319a3e7 data-lead-in,data-src; q_63eb9b1c14fe59598997 data-lead-in,data-src; q_ba420652bd9b571595cf data-d1,data-d1-id,data-lead-in,data-src); ITEMS REMOVED (q_49c3284cc3325ac68b0a, q_08cb900770515d90a6b5, q_9f3d98884472530aa877, q_1209661648d958659d7b, q_69d16408bcc95b419c60, q_dfd6593838d95aa99602); prose edited (+1057 chars)
Other page changes (nav, headers, scripts): -198 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 208 briefs, 2110 items, 6 scripts, 35 checks, base HEAD | allowlisted 27 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 208 | bankwraps 208 | mcq 2110 (axCheck 2110, reveal-only 0) | malformed 0 | crit gridded 180/181 | vignette gridded 117/117 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s68: s68: merge batch 1: Pyelonephritis (+ Naming the Organism; IDSA 2025 complicated-UTI definition, older male-sex rule flagged; 3 UWorld items archived and rewritten), Shoulder Pain (+ Biceps Tendinitis), Obstructive Lung Disease (COPD + Asthma vs. COPD; AAFP 2023: oxygen for resting hypoxemia only; NBME item moved to its framing block); lean style, two-line subtitles; each reviewed to 0 critical in 2 rounds

```
Page: 215 briefs, 2119 items -> 212 briefs, 2117 items
Briefs REMOVED (3): biceps, asthma-copd, bs-pyelo-organism
Briefs changed (5):
  - shoulder-rom (Shoulder Pain): items edited (q_fb1d66628e9e5dbe8804, q_d437d76a43fe5cc195f2, q_cf889d01eb9d5589b7ac, q_16ab9d19515c50b2bad3, q_485f9115660152fa90df, q_8ea463fa57525f9a88aa, q_b24432b9e91650af8cf0, q_d0b507b5222a5033807b, q_a10db1e08e775eaaa505, q_6bbbb94042b85378878a, q_1c3901f2318c5ec9ba9d, q_96955d7d66635dbc8531, q_afb41fb2eae851c1b242); versions bumped (q_fb1d66628e9e5dbe8804 v1->v2, q_d437d76a43fe5cc195f2 v1->v2, q_cf889d01eb9d5589b7ac v1->v2, q_16ab9d19515c50b2bad3 v1->v2, q_485f9115660152fa90df v1->v2, q_8ea463fa57525f9a88aa v1->v2, q_b24432b9e91650af8cf0 v1->v2, q_d0b507b5222a5033807b v1->v2, q_a10db1e08e775eaaa505 v1->v2, q_6bbbb94042b85378878a v1->v2, q_1c3901f2318c5ec9ba9d v1->v2, q_96955d7d66635dbc8531 v1->v2, q_afb41fb2eae851c1b242 v1->v2); attrs set (brief data-replaces; q_fb1d66628e9e5dbe8804 data-lead-in,data-src; q_d437d76a43fe5cc195f2 data-d1,data-d1-id,data-lead-in; q_cf889d01eb9d5589b7ac data-lead-in; q_16ab9d19515c50b2bad3 data-d2,data-d2-id,data-lead-in; q_485f9115660152fa90df data-d1,data-d1-id,data-lead-in; q_8ea463fa57525f9a88aa data-d1,data-d1-id,data-lead-in; q_b24432b9e91650af8cf0 data-d2,data-d2-id,data-lead-in; q_d0b507b5222a5033807b data-lead-in,data-src; q_a10db1e08e775eaaa505 data-lead-in,data-src; q_6bbbb94042b85378878a data-lead-in,data-src; q_1c3901f2318c5ec9ba9d data-lead-in,data-src; q_96955d7d66635dbc8531 data-lead-in,data-src; q_afb41fb2eae851c1b242 data-lead-in,data-src); prose edited (+1274 chars)
  - copd (Obstructive Lung Disease): items edited (q_8ae0956915f654db8cea, q_582f85d59e8652bfba7b, q_c61717d7d298572f8b18, q_b4d499d174735935bd84, q_d2014e221b4951e78f2d, q_2d2a0e782dde5770a9bf, q_e1d0b562a4195f5aa67d, q_a21c33a11152540783ed, q_4a4a1e8c0f775b17bc96, q_fc488cc379ca5efd9dac, q_fe770bee4e92526681d7, q_412751afcfdc52f6be00, q_a78a51dbde2c536088b6, q_75193c7374685f4793e9, q_cc7315e5e2a450bbacfc, q_62afba1e07c95c8bb96f); versions bumped (q_8ae0956915f654db8cea v1->v2, q_582f85d59e8652bfba7b v1->v2, q_c61717d7d298572f8b18 v1->v2, q_b4d499d174735935bd84 v1->v2, q_d2014e221b4951e78f2d v1->v2, q_2d2a0e782dde5770a9bf v1->v2, q_e1d0b562a4195f5aa67d v2->v3, q_a21c33a11152540783ed v1->v2, q_4a4a1e8c0f775b17bc96 v1->v2, q_fc488cc379ca5efd9dac v2->v3, q_fe770bee4e92526681d7 v1->v2, q_412751afcfdc52f6be00 v1->v2, q_a78a51dbde2c536088b6 v1->v2, q_75193c7374685f4793e9 v1->v2, q_cc7315e5e2a450bbacfc v2->v3, q_62afba1e07c95c8bb96f v1->v2); attrs set (brief data-replaces; q_8ae0956915f654db8cea data-lead-in,data-src; q_582f85d59e8652bfba7b data-d1,data-d1-id,data-d2,data-d2-id,data-lead-in,data-src; q_c61717d7d298572f8b18 data-lead-in,data-src; q_b4d499d174735935bd84 data-lead-in,data-src; q_d2014e221b4951e78f2d data-lead-in,data-src; q_2d2a0e782dde5770a9bf data-lead-in,data-src; q_e1d0b562a4195f5aa67d data-src; q_a21c33a11152540783ed data-lead-in,data-src; q_4a4a1e8c0f775b17bc96 data-lead-in,data-src; q_fc488cc379ca5efd9dac data-d2,data-d2-id,data-src; q_fe770bee4e92526681d7 data-lead-in,data-src; q_412751afcfdc52f6be00 data-lead-in,data-src; q_a78a51dbde2c536088b6 data-d2,data-d2-id,data-lead-in,data-src; q_75193c7374685f4793e9 data-lead-in,data-src; q_cc7315e5e2a450bbacfc data-src; q_62afba1e07c95c8bb96f data-lead-in); prose edited (+5824 chars)
  - abpa (When Antibiotics Fail in a Structural Lung): prose edited (+9 chars)
  - scd-dyspnea (Chronic Dyspnea in Sickle Cell Disease): prose edited (+9 chars)
  - pyelo (Pyelonephritis): 4 items added (q_e1f0e7693e4ac033fa19, q_275467832fd82bf2a6c4, q_d726b7ef5300f9ba5d26, q_bc0baad2e2586dc8d5f4); items edited (q_bf878ff6464c5ab3adea, q_60f2a706336a5684befd, q_a1dbfde2d57b58818137, q_38350d6bbf8e58b4b8cf, q_df64b280b82156628c5f, q_e7ad1e5c1b5a55d7a0ed, q_c498a30d3e6c595fbf8a, q_e0641cdada065ec5b18a, q_25f21cf7aa1a5e69905e, q_559afd68379b5e26ae48, q_0f943482beae53479119); versions bumped (q_bf878ff6464c5ab3adea v1->v2, q_60f2a706336a5684befd v1->v2, q_a1dbfde2d57b58818137 v1->v2, q_38350d6bbf8e58b4b8cf v1->v2, q_df64b280b82156628c5f v1->v2, q_e7ad1e5c1b5a55d7a0ed v1->v2, q_c498a30d3e6c595fbf8a v1->v2, q_e0641cdada065ec5b18a v1->v2, q_25f21cf7aa1a5e69905e v1->v2, q_559afd68379b5e26ae48 v1->v2, q_0f943482beae53479119 v1->v2); attrs set (brief data-replaces; q_bf878ff6464c5ab3adea data-lead-in,data-src; q_60f2a706336a5684befd data-d2,data-d2-id,data-lead-in,data-src; q_a1dbfde2d57b58818137 data-lead-in,data-src; q_38350d6bbf8e58b4b8cf data-lead-in,data-src; q_df64b280b82156628c5f data-lead-in,data-src; q_e7ad1e5c1b5a55d7a0ed data-d1,data-d1-id,data-d2,data-d2-id,data-lead-in,data-src; q_c498a30d3e6c595fbf8a data-lead-in,data-src; q_e0641cdada065ec5b18a data-lead-in,data-src; q_25f21cf7aa1a5e69905e data-lead-in,data-src; q_559afd68379b5e26ae48 data-d2,data-d2-id,data-lead-in,data-src; q_0f943482beae53479119 data-lead-in,data-src); ITEMS REMOVED (q_50b836e299425e419386, q_b6d14ad5f412538dbee6, q_43dfbe3878f05a598285, q_5b915fd039d45149af5e); prose edited (+4541 chars)
Other page changes (nav, headers, scripts): -147 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 212 briefs, 2117 items, 6 scripts, 35 checks, base HEAD | allowlisted 27 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 212 | bankwraps 212 | mcq 2117 (axCheck 2117, reveal-only 0) | malformed 0 | crit gridded 173/174 | vignette gridded 118/118 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s67: s67: merge pilot: Enuresis + Primary Monosymptomatic Enuresis: Management into one lean brief, Enuresis (bs-enuresis kept as an alias); bare title, two-line subtitle (scope line, italic question), each defined term on its own line; AAFP 2022 settles desmopressin as first-line beside the alarm and the 6-week alarm checkpoint; hyponatremic seizure gets hypertonic saline (MSD); 13 questions (2 duplicates merged, 1 wrong-age key replaced); independent review to 0 critical in 2 rounds

```
Page: 216 briefs, 2121 items -> 215 briefs, 2119 items
Briefs REMOVED (1): bs-enuresis
Briefs changed (1):
  - enuresis (Enuresis): 1 item added (q_ee4a95940f37e9b9b97a); items edited (q_88b136166b31572fa806, q_2d70c913ab9f5f8a9075, q_d7ab0f6d88c85fc8907e, q_aee72a7d300a55b18d1a, q_76838a88eef25aba9843, q_de4be37a858a5c59ab0c, q_9faa21c84e2e5a39ba66, q_11fc98144a285b0bbd08, q_c774c1e43c8e5995bb32, q_a457a60b9ced565ab9fe, q_051cc928257f5b15ae65, q_2510a432a4295a879318); versions bumped (q_88b136166b31572fa806 v1->v2, q_2d70c913ab9f5f8a9075 v1->v2, q_d7ab0f6d88c85fc8907e v1->v2, q_aee72a7d300a55b18d1a v1->v2, q_76838a88eef25aba9843 v1->v2, q_de4be37a858a5c59ab0c v1->v2, q_9faa21c84e2e5a39ba66 v1->v2, q_11fc98144a285b0bbd08 v2->v3, q_c774c1e43c8e5995bb32 v1->v2, q_a457a60b9ced565ab9fe v1->v2, q_051cc928257f5b15ae65 v1->v2, q_2510a432a4295a879318 v1->v2); attrs set (brief data-replaces; q_88b136166b31572fa806 data-lead-in,data-src; q_2d70c913ab9f5f8a9075 data-lead-in,data-src; q_d7ab0f6d88c85fc8907e data-lead-in,data-src; q_aee72a7d300a55b18d1a data-d2,data-d2-id,data-lead-in,data-src; q_76838a88eef25aba9843 data-lead-in,data-src; q_de4be37a858a5c59ab0c data-lead-in,data-src; q_9faa21c84e2e5a39ba66 data-lead-in,data-src; q_11fc98144a285b0bbd08 data-lead-in,data-src; q_c774c1e43c8e5995bb32 data-lead-in,data-src; q_a457a60b9ced565ab9fe data-lead-in,data-src; q_051cc928257f5b15ae65 data-lead-in,data-src; q_2510a432a4295a879318 data-lead-in,data-src); ITEMS REMOVED (q_df2e8851633e5c7d9b40); prose edited (+2834 chars)
Other page changes (nav, headers, scripts): -7 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 215 briefs, 2119 items, 6 scripts, 35 checks, base HEAD | allowlisted 27 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 215 | bankwraps 215 | mcq 2119 (axCheck 2119, reveal-only 0) | malformed 0 | crit gridded 165/166 | vignette gridded 120/120 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s66: s66: retitle 100 briefs to their broadest honest topic (Jonathan 2026-10-03: generalized titles); decision clauses moved to the subtitle line; Pairs with, wording-guide links and sidebar labels follow; merge heads retitled only where the head alone fits the new title; merges to follow cluster by cluster

```
Page: 216 briefs, 2121 items -> 216 briefs, 2121 items
Briefs changed (151):
  - backpain (Low Back Pain in an Adult): prose edited (+1 chars)
  - hippos (Hip Injury in an Adult): prose edited (-19 chars)
  - gtps (Hip and Thigh Pain in an Adult): prose edited (+1 chars)
  - oa-pharm (Osteoarthritis): prose edited (-16 chars)
  - septic-hip (Septic Arthritis and Transient Synovitis in a Child): prose edited (+32 chars)
  - limp (The Limping Child): prose edited (-114 chars)
  - sjia (Juvenile Idiopathic Arthritis): prose edited (-5 chars)
  - nursemaid (Arm Injury in a Young Child): prose edited (-43 chars)
  - scfe (Slipped Capital Femoral Epiphysis): prose edited (+8 chars)
  - myositis-ossificans (Muscle Contusion and Myositis Ossificans): prose edited (-7 chars)
  - growing-pains (Leg Pain in a Child): prose edited (-114 chars)
  - bone-tumors (Bone Lesions in a Child): prose edited (-136 chars)
  - scheuermann (Adolescent Kyphosis): prose edited (+8 chars)
  - bs-septic-adult (The Acute Hot Joint (adult)): prose edited (-9 chars)
  - bs-lbp-acute (Acute Low Back Pain with No Red Flags): prose edited (+2 chars)
  - bs-puncture-osteomyelitis (Foot Puncture Wounds and Osteomyelitis): prose edited (-78 chars)
  - bs-torticollis (Torticollis and Plagiocephaly in an Infant): prose edited (-39 chars)
  - bs-brachial-plexus (Brachial Plexus Injury at Birth): prose edited (-33 chars)
  - shoulder-rom (Shoulder Pain): prose edited (-26 chars)
  - growth (Developmental Milestones and Normal Growth): prose edited (+5 chars)
  - neonatal-maternal-labs (Maternal Carryover in Newborn Labs): prose edited (-20 chars)
  - aneuploidy (Aneuploidy: Reading the Newborn): prose edited (+2 chars)
  - malform-syndromes (Multiple Anomalies in a Newborn): prose edited (-1 chars)
  - bs-learning (School Difficulty in a Child): prose edited (+2 chars)
  - bs-nat-fracture (Suspected Child Abuse): prose edited (-65 chars)
  - bs-infant-feeding (Infant Feeding at Six Months): prose edited (-41 chars)
  - bs-tanner (Sexual Maturity Rating): prose edited (+5 chars)
  - bs-ftt (Faltering Weight): prose edited (+2 chars)
  - bs-preterm-followup (Follow-Up of the Preterm Infant): prose edited (-28 chars)
  - aq-infant-hypotonia (Hypotonia in an Infant): prose edited (-15 chars)
  - chf (Heart Failure): prose edited (-26 chars)
  - ascvd (Lipid Screening and Statin Therapy): prose edited (-13 chars)
  - angina (Stable Ischemic Heart Disease): prose edited (-18 chars)
  - secondary-htn (Secondary Hypertension): prose edited (-4 chars)
  - dvt (Venous Thromboembolism): prose edited (-6 chars)
  - ped-murmur (Heart Murmurs in a Child): prose edited (-6 chars)
  - cyanotic-chd (Cyanotic Congenital Heart Disease): prose edited (-6 chars)
  - right-murmurs (Right-Sided Murmurs: Pulmonic Stenosis & Tricuspid Regurgitation): prose edited (-6 chars)
  - htn-drugs (Hypertension in an Adult): prose edited (-14 chars)
  - newborn-cyanosis (Cyanosis in the Newborn): prose edited (-1 chars)
  - kawasaki (Kawasaki Disease): prose edited (-4 chars)
  - myocarditis (Heart Failure in a Child): prose edited (-4 chars)
  - del22q11 (22q11.2 Deletion Syndrome): prose edited (-3 chars)
  - bs-adolescent-bp (High Blood Pressure in a Child or Adolescent): prose edited (-17 chars)
  - copd (COPD): prose edited (-38 chars)
  - rhinitis (Rhinitis): prose edited (-9 chars)
  - sinopulm-structural (Recurrent Sinopulmonary Infection): prose edited (-3 chars)
  - hypoxemia-mech (Hypoxemia): prose edited (-14 chars)
  - scd-dyspnea (Chronic Dyspnea in Sickle Cell Disease): prose edited (-28 chars)
  - airway (Noisy Breathing in a Child): prose edited (-38 chars)
  - asthma (Asthma): prose edited (-25 chars)
  - bpd (Bronchopulmonary Dysplasia): prose edited (-54 chars)
  - bs-nrd (Neonatal Respiratory Distress): prose edited (-34 chars)
  - masld (Fatty Liver Disease): prose edited (-46 chars)
  - cholestasis (Abnormal Liver Tests): prose edited (-14 chars)
  - infant-stool (Stool Changes in a Well Infant): prose edited (-46 chars)
  - rlq-pain (Right Lower Quadrant Pain): prose edited (-19 chars)
  - peds-constipation (Constipation in a Child): prose edited (-66 chars)
  - cyclic-vomiting (Recurrent Vomiting in a Child): prose edited (+8 chars)
  - neonatal-jaundice (Jaundice in a Newborn): prose edited (-10 chars)
  - neonatal-bowel (The Distended Abdomen in a Newborn or Infant): prose edited (-47 chars)
  - occult-gi-bleed (GI Bleeding in a Child): prose edited (-19 chars)
  - bs-galactosemia (The Sick Jaundiced Neonate with a Positive Screen): prose edited (-14 chars)
  - bs-impaction (Constipation and Fecal Impaction in an Adult): prose edited (+5 chars)
  - bs-tef (Tracheoesophageal Fistula and Esophageal Atresia): prose edited (-21 chars)
  - bs-umbilical (Umbilical Findings in a Newborn): prose edited (-1 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): prose edited (-11 chars)
  - bs-water-soluble-vitamins (Water-Soluble Vitamin Deficiency): prose edited (-10 chars)
  - bs-wilson (Wilson Disease): prose edited (-67 chars)
  - pyelo (Pyelonephritis): prose edited (-29 chars)
  - bph (Benign Prostatic Hyperplasia and Urinary Retention): prose edited (+17 chars)
  - scrotum (Scrotal Pain and Masses): prose edited (-9 chars)
  - hypercalcemia (Hypercalcemia): prose edited (-24 chars)
  - vur (Vesicoureteral Reflux): prose edited (-28 chars)
  - peds-uti-recurrent (Urinary Tract Infection in a Child): prose edited (-29 chars)
  - enuresis (Enuresis): prose edited (-27 chars)
  - polyuria (Polyuria): prose edited (-34 chars)
  - peds-aki (Acute Kidney Injury in a Child): prose edited (+1 chars)
  - bs-puv (Posterior Urethral Valves): prose edited (-46 chars)
  - bs-incontinence (Urinary Incontinence): prose edited (-20 chars)
  - bs-enuresis (Primary Monosymptomatic Enuresis: Management): prose edited (-10 chars)
  - bs-nephritic (Acute Nephritic Syndrome in a Child): prose edited (+1 chars)
  - bs-abdominal-mass (Abdominal Mass in a Young Child): prose edited (-33 chars)
  - bs-distal-rta (Hypokalemia and Acid-Base Disorders in a Child): prose edited (-14 chars)
  - aq-puffy-eyes (Child with Puffy Eyes): prose edited (-21 chars)
  - thyroid (Thyroid Disease in an Adult): prose edited (-8 chars)
  - gynecomastia (Male Breast Enlargement): prose edited (-12 chars)
  - congenital-hypothyroid (Congenital Hypothyroidism): prose edited (-8 chars)
  - tumor-syndromes (Inherited Tumor Syndromes): prose edited (-3 chars)
  - homocystinuria (Tall Stature and Marfanoid Habitus): prose edited (-10 chars)
  - bs-short-stature (Short Stature and Growth Velocity): prose edited (-8 chars)
  - anemia-thrombocytopenia (Anemia with Thrombocytopenia): prose edited (+1 chars)
  - dipstick-mismatch (Dark Urine: Hemoglobin, Myoglobin or Blood): prose edited (-6 chars)
  - microcytic-anemia (Microcytic Anemia): prose edited (-15 chars)
  - factor-inhibitor (Hemophilia): prose edited (-12 chars)
  - transfusion (Transfusion Reactions): prose edited (-3 chars)
  - bs-leukemia (Acute Leukemia in a Child): prose edited (-131 chars)
  - bs-sickle-trait (Sickle Cell Disease and Trait): prose edited (-3 chars)
  - aq-bruising (Bruising and Purpura in a Child): prose edited (-42 chars)
  - ig-panel (Antibody Deficiencies): prose edited (-16 chars)
  - rmsf (Tick-Borne Illness): prose edited (-5 chars)
  - lymphadenitis (Lymphadenopathy): prose edited (-26 chars)
  - herpangina (Oral Lesions in a Child): prose edited (+4 chars)
  - cgd (Neutrophil Disorders: Number and Function): prose edited (+4 chars)
  - bs-pta (Deep Neck Infections): prose edited (-26 chars)
  - bs-torch (Congenital Infections (TORCH)): prose edited (-35 chars)
  - bs-fever-rash-arthralgia (Fever, Rash and Joint Pain: Name the Rash, Then Date the Exposure): prose edited (-37 chars)
  - bs-exanthems (Fever and Rash in a Child): prose edited (-38 chars)
  - bs-anaphylaxis (Anaphylaxis): prose edited (-61 chars)
  - bs-isolation (Isolation Precautions): prose edited (+5 chars)
  - bs-foodborne (Infectious Diarrhea): prose edited (-26 chars)
  - aq-infant-fever (Fever in an Infant): prose edited (+1 chars)
  - cluster (Primary Headache in an Adult): prose edited (-6 chars)
  - sellar-mass (Sellar and Suprasellar Masses): prose edited (-14 chars)
  - peds-headache-imaging (Headache in a Child: Imaging and Treatment): prose edited (-5 chars)
  - cholesteatoma (Cholesteatoma and Chronic Ear Drainage): prose edited (-6 chars)
  - cerebral-palsy (Cerebral Palsy): prose edited (-65 chars)
  - abrs-complications (Sinusitis and Its Complications): prose edited (-6 chars)
  - vpshunt (Hydrocephalus and Shunt Complications): prose edited (-4 chars)
  - tics (Tics and Tic Disorders): prose edited (-2 chars)
  - bs-tethered (Spinal Dysraphism): prose edited (-35 chars)
  - bs-reye (Encephalopathy and Cerebral Edema in a Child): prose edited (+3 chars)
  - bs-peds-stroke (Stroke in a Child or Adolescent): prose edited (-13 chars)
  - bs-imprinting (Imprinting Disorders: Angelman and Prader-Willi): prose edited (-18 chars)
  - bs-eyelid-lump (Eyelid Lumps and Swelling in a Child): prose edited (-6 chars)
  - bs-posterior-fossa (Posterior Fossa Localization): prose edited (-19 chars)
  - aq-child-headache (Headache in a School-Age Child): prose edited (+9 chars)
  - psoriasis (Scaly Rashes): prose edited (-21 chars)
  - cellulitis (Skin and Soft Tissue Infection): prose edited (-3 chars)
  - eczemaherp (Atopic Dermatitis): prose edited (-14 chars)
  - peds-alopecia (Hair Loss in a Child): prose edited (-21 chars)
  - preg-vax (Vaccines in Pregnancy): prose edited (-13 chars)
  - contraception (Contraception): prose edited (-11 chars)
  - teratogens (Teratogenic Exposures): prose edited (-20 chars)
  - bs-tdap-preg (Tdap in Pregnancy at 10 Weeks): prose edited (-13 chars)
  - bs-genital-ulcer (Genital Ulcers): prose edited (-20 chars)
  - smoking (Preventive Care: Ranking Interventions): prose edited (+6 chars)
  - preop (Preoperative Evaluation): prose edited (+0 chars)
  - elder (Elder Abuse): prose edited (-25 chars)
  - bs-adolescent-confid (Adolescent Confidentiality): prose edited (-25 chars)
  - bs-infant-vax (Vaccines at the Infant Visits): prose edited (-25 chars)
  - bs-adolescent-vax (Adolescent Vaccines): prose edited (-25 chars)
  - psychosis-duration (Psychosis): prose edited (-4 chars)
  - bipolar-mania (Bipolar Disorder): prose edited (-145 chars)
  - sz-psychosocial (Schizophrenia: Long-Term Care): prose edited (-33 chars)
  - delirium (Delirium): prose edited (-36 chars)
  - panic (Panic Disorder and Other Anxiety): prose edited (+3 chars)
  - ssri-effects (SSRI Adverse Effects): prose edited (-111 chars)
  - lithium-effects (Lithium Therapy): prose edited (-24 chars)
  - ipv (Intimate Partner Violence): prose edited (-58 chars)
  - gppd (Genito-Pelvic Pain/Penetration Disorder): prose edited (+15 chars)
Other page changes (nav, headers, scripts): +25 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2121 items, 6 scripts, 35 checks, base HEAD | allowlisted 28 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2121 (axCheck 2121, reveal-only 0) | malformed 0 | crit gridded 164/165 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s65: s65: clear PENDING live errors: four vignettes rebuilt from their briefs (sellar-mass, peds-headache-imaging, bs-reye, bs-impaction; marked partial); scleritis systemic steroids; HPV early-dose repeat; ACS 2020 co-testing and cytology still acceptable; cervical HIV start age 21 per HHS 2024/ASCCP with CDC STI 2021 conflict labelled; non-HIV immunosuppression start 21; cervical-gate rarity reorder; dipstick Pairs with (spherocytes, DAT); posterior fossa cerebellar wording; exam-meta removed (nephrotic spine, headache pearl, two spine labels); adolescent HPV schedule status after the March 2026 court stay

```
Page: 216 briefs, 2121 items -> 216 briefs, 2121 items
Briefs changed (14):
  - malform-syndromes (Multiple Anomalies in a Newborn): prose edited (-30 chars)
  - bs-impaction (Fecal Impaction & Overflow Diarrhea): prose edited (+197 chars)
  - polyuria (Polyuria: Water or Solute): prose edited (-37 chars)
  - nephrotic-child (Nephrotic Syndrome in a Child): prose edited (-38 chars)
  - dipstick-mismatch (Hemoglobinuria: the Dipstick-Microscopy Mismatch): prose edited (+74 chars)
  - redeye (The Red Eye): prose edited (+34 chars)
  - sellar-mass (Sellar and Suprasellar Masses): prose edited (+354 chars)
  - peds-headache-imaging (Headache in a Child: What Earns Imaging): prose edited (+208 chars)
  - bs-reye (Cerebral Edema in a Child — Reye Syndrome): prose edited (+197 chars)
  - bs-posterior-fossa (Posterior Fossa Localization): prose edited (-26 chars)
  - cervical (Cervical Cancer Screening): prose edited (+349 chars)
  - hpv (HPV Vaccination & Series Rules): prose edited (+64 chars)
  - bs-cervical-gate (Cervical Screening: the Age-21 Floor): prose edited (+238 chars)
  - bs-adolescent-vax (Adolescent Immunization and the Age Platform): prose edited (+297 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2121 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2121 (axCheck 2121, reveal-only 0) | malformed 0 | crit gridded 164/165 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s64: s64: Psych: intimate partner violence in the lean style (raise-it tile, every-patient step table, safety plan tile, who-decides and who-must-be-reported table, screening and complications); NBME Q2 moved to its framing block; older or disabled adult reporting kept separate from capacity; step2 bases follow their sources. Psych lean queue complete

```
Page: 216 briefs, 2122 items -> 216 briefs, 2121 items
Briefs changed (1):
  - ipv (Intimate Partner Violence in an Adult: Plan for Safety, Report by Who Is at Risk): items edited (q_08f59bcec2907d1fbe0c, q_40971ac6e38b6d8b7be4, q_18884f761899281f8379, q_ba5b7078420440fa2058, q_9ee31320c880ba278f9a, q_cf19c178e8d4247cf58c, q_94b8689396a90e9cf711, q_bf0703ef66d06d09b871, q_7ce401bb1677c0c9fbb8, q_ab5eb45b397655435f35, q_9afa95fc7fac80545924); versions bumped (q_08f59bcec2907d1fbe0c v1->v2, q_40971ac6e38b6d8b7be4 v1->v2, q_18884f761899281f8379 v1->v2, q_ba5b7078420440fa2058 v1->v2, q_9ee31320c880ba278f9a v1->v2, q_cf19c178e8d4247cf58c v1->v2, q_94b8689396a90e9cf711 v1->v2, q_bf0703ef66d06d09b871 v1->v2, q_7ce401bb1677c0c9fbb8 v1->v2, q_ab5eb45b397655435f35 v1->v2, q_9afa95fc7fac80545924 v1->v2); ITEMS REMOVED (q_8d70e905d154f5399e60); prose edited (-3785 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2121 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2121 (axCheck 2121, reveal-only 0) | malformed 0 | crit gridded 164/165 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s63: s63: Psych: genito-pelvic pain/penetration disorder in the lean style (criteria tile, examine-before-labeling workup path, what-else table, multimodal treatment, body-cause treatments); NBME Q7 moved to its framing block; one-or-more criterion A kept in the rule and the workup; GAD and SSD rows sourced; vulvodynia item decider fixed

```
Page: 216 briefs, 2123 items -> 216 briefs, 2122 items
Briefs changed (1):
  - gppd (Genito-Pelvic Pain/Penetration Disorder (Vaginismus): Exclude a Body Cause, Then Treat): items edited (q_b589ce7156cbdcaf0964, q_d42d568cc568fd7b9fd1, q_3a7d844ecc3c3b9fe886, q_0ee19d0739b94cb7627d, q_b0f0c334fd087638797e, q_5dd7c86366ecfd236b41, q_1c3de6f03e7f9fe8f0e9, q_d1aaef1d03d23fe24820); versions bumped (q_b589ce7156cbdcaf0964 v1->v2, q_d42d568cc568fd7b9fd1 v1->v2, q_3a7d844ecc3c3b9fe886 v1->v2, q_0ee19d0739b94cb7627d v1->v2, q_b0f0c334fd087638797e v1->v2, q_5dd7c86366ecfd236b41 v1->v2, q_1c3de6f03e7f9fe8f0e9 v1->v2, q_d1aaef1d03d23fe24820 v1->v2); attrs set (q_3a7d844ecc3c3b9fe886 data-d1,data-d1-id); ITEMS REMOVED (q_ef57823831290143bd7b); prose edited (-3526 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2122 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2122 (axCheck 2122, reveal-only 0) | malformed 0 | crit gridded 161/163 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 2
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s62: s62: Psych: schizophrenia on treatment in the lean style (danger first, find what changed before changing the drug, expressed emotion tile, match-the-added-treatment table with APA strengths, not-the-answer tile, relapse prevention); NBME Q4 moved to its framing block; step2 bases no longer cite Q4 for content it never mentions; ownership with psychosis-duration stated

```
Page: 216 briefs, 2124 items -> 216 briefs, 2123 items
Briefs changed (1):
  - sz-psychosocial (Schizophrenia on Treatment: Psychosocial Care and Relapse Prevention): items edited (q_4c64032d1e4c534c6782, q_acec20862df55cf9786a, q_9bbca9be1aa0ef0942ca, q_4eff7cc0f37692494f18, q_4f51374399c5e2faa634, q_7b50d623d43c9a53c94f, q_5e890413f13e8d4b5abf, q_c85b7eee3da384e60440, q_b50c3ec605ca3faf50ee, q_9fa041c8970b9d3b3fba, q_4a4edd58a7fdd308d09f); versions bumped (q_4c64032d1e4c534c6782 v1->v2, q_acec20862df55cf9786a v1->v2, q_9bbca9be1aa0ef0942ca v1->v2, q_4eff7cc0f37692494f18 v1->v2, q_4f51374399c5e2faa634 v1->v2, q_7b50d623d43c9a53c94f v1->v2, q_5e890413f13e8d4b5abf v1->v2, q_c85b7eee3da384e60440 v1->v2, q_b50c3ec605ca3faf50ee v1->v2, q_9fa041c8970b9d3b3fba v1->v2, q_4a4edd58a7fdd308d09f v1->v2); attrs set (q_9bbca9be1aa0ef0942ca data-d1,data-d1-id; q_9fa041c8970b9d3b3fba data-lead-in); ITEMS REMOVED (q_c1513f868f37ef34aea2); prose edited (-4114 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2123 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2123 (axCheck 2123, reveal-only 0) | malformed 0 | crit gridded 158/161 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 3
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s61: s61: Psych: lithium complications in the lean style (act-first dialysis criteria in toxicity, three-pair workup path, LMNOP, which-one table, toxicity ladder, By situation, monitoring); NBME Q5 moved to its framing block; earlier review fixes kept (TSH with free thyroxine, commonly above 1.5 mmol/L, little or no desmopressin response)

```
Page: 216 briefs, 2125 items -> 216 briefs, 2124 items
Briefs changed (1):
  - lithium-effects (The Patient on Lithium: Which Complication, and What to Do): items edited (q_fdf8caeb97e43a815d98, q_182e22e561f6fc45d39e, q_04b1d3c440a7cf52da0a, q_fa69616f74588eaa5d79, q_2ea25399ba45abf02320, q_75b281aa8cbc5a5548c3, q_aa507f9a6ddbea9e1a0c, q_cf8fe6d5b6f2483d69e4, q_d952defc13d2eb0f68b3, q_1b55329353193e01aefd, q_06efe9680e1f6779f32c); versions bumped (q_fdf8caeb97e43a815d98 v1->v2, q_182e22e561f6fc45d39e v1->v2, q_04b1d3c440a7cf52da0a v2->v3, q_fa69616f74588eaa5d79 v1->v2, q_2ea25399ba45abf02320 v1->v2, q_75b281aa8cbc5a5548c3 v1->v2, q_aa507f9a6ddbea9e1a0c v1->v2, q_cf8fe6d5b6f2483d69e4 v2->v3, q_d952defc13d2eb0f68b3 v2->v3, q_1b55329353193e01aefd v1->v2, q_06efe9680e1f6779f32c v1->v2); attrs set (q_fa69616f74588eaa5d79 data-lead-in; q_75b281aa8cbc5a5548c3 data-lead-in); ITEMS REMOVED (q_f68b5a29e435cf4c9058); prose edited (-5816 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2124 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2124 (axCheck 2124, reveal-only 0) | malformed 0 | crit gridded 155/159 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 4
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s60: s60: Psych: SSRI adverse effects in the lean style (Which effect tile, FINISH, timing chart for serotonin syndrome, NMS, discontinuation and relapse, two ladders, By situation, prevention); NBME Q9 moved to its framing block; NBME hedges kept (commonly, reasonable options, eg); Warner restart option and other-causes-ruled-out step restored; review N_reviews_v1 N4 flags fixed

```
Page: 216 briefs, 2126 items -> 216 briefs, 2125 items
Briefs changed (1):
  - ssri-effects (SSRI (Selective Serotonin Reuptake Inhibitor) Adverse Effects: Name the Effect, Then Take the Next Step): items edited (q_125f388e00badb74a592, q_4c6ee3a2ac28b5d544c1, q_1319671e8b2c93ba6852, q_46efe61956d880fb6584, q_82d710660ff3e8d5c763, q_d825fd2c09edb7908257, q_6f875a3df168eda248ea, q_5568d24b36134cb369b5, q_25d0479945c172a43d22, q_1459fc022ab109ac3695); versions bumped (q_125f388e00badb74a592 v1->v2, q_4c6ee3a2ac28b5d544c1 v1->v2, q_1319671e8b2c93ba6852 v1->v2, q_46efe61956d880fb6584 v1->v2, q_82d710660ff3e8d5c763 v1->v2, q_d825fd2c09edb7908257 v1->v2, q_6f875a3df168eda248ea v1->v2, q_5568d24b36134cb369b5 v1->v2, q_25d0479945c172a43d22 v1->v2, q_1459fc022ab109ac3695 v1->v2); attrs set (q_6f875a3df168eda248ea data-d2,data-d2-id); ITEMS REMOVED (q_bb27f32e9b44fcdc72d4); prose edited (-1370 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2125 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2125 (axCheck 2125, reveal-only 0) | malformed 0 | crit gridded 153/159 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 6
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s59: s59: Psych: panic disorder in the lean style (criteria tile with the STUDENTS FEAR mnemonic, mimic workup path, timing chart of six anxiety disorders by what the fear is about, ladder with benzodiazepine as a short-term bridge only, By situation, follow-up); NBME Q10 moved to its framing block; every panic item meets Criteria A and B; review N_reviews_v1 N5 flags fixed

```
Page: 216 briefs, 2127 items -> 216 briefs, 2126 items
Briefs changed (1):
  - panic (Panic Disorder and Its Mimics: Which Anxiety, and How to Treat): items edited (q_9cb0cb9bbe901f8d82c3, q_0a680a7675773ffea9d5, q_d38874735cc315f53712, q_9882ee4e5ed520e497ed, q_1c1f69ce1e98783124e0, q_2770350e3c6d0c9f10b1, q_e3955a2914959af65ee8, q_0a1dc4c6f646148e90f6, q_b6fe551a76fe31c35481, q_417bf3e7befaa83ad1f7, q_f02353ec90fe1c1d49c2, q_8f56600a122cbeb2b97c, q_a29e571adb123e184e79, q_ce5106b02de93c0f3359, q_25ccc4431464504f2c69); versions bumped (q_9cb0cb9bbe901f8d82c3 v1->v2, q_0a680a7675773ffea9d5 v1->v2, q_d38874735cc315f53712 v1->v2, q_9882ee4e5ed520e497ed v1->v2, q_1c1f69ce1e98783124e0 v1->v2, q_2770350e3c6d0c9f10b1 v1->v2, q_e3955a2914959af65ee8 v1->v2, q_0a1dc4c6f646148e90f6 v1->v2, q_b6fe551a76fe31c35481 v1->v2, q_417bf3e7befaa83ad1f7 v1->v2, q_f02353ec90fe1c1d49c2 v1->v2, q_8f56600a122cbeb2b97c v1->v2, q_a29e571adb123e184e79 v1->v2, q_ce5106b02de93c0f3359 v1->v2, q_25ccc4431464504f2c69 v1->v2); ITEMS REMOVED (q_153eea8de1097e9a3bd3); prose edited (-2386 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2126 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2126 (axCheck 2126, reveal-only 0) | malformed 0 | crit gridded 151/158 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 7
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-03 s58: s58: Psych: delirium in the lean style (DSM-5-TR criteria tile, workup path with ordered CT, lumbar puncture and EEG branches, delirium/dementia/psychosis timing chart, ladder, By situation, Beers and course); NBME Q1 moved to its framing block; schizophrenia item retired to psychosis-duration; Alzheimer item gets a Lewy body distractor; review N_reviews_v1 flags fixed

```
Page: 216 briefs, 2129 items -> 216 briefs, 2127 items
Briefs changed (1):
  - delirium (Delirium: Tell It From Dementia and Psychosis, Then Find the Cause): items edited (q_11cc3578ab34fb7ed536, q_6528f9dbc4a553760f7d, q_7470edf44986934e921d, q_7b50e870883dc73ce0f9, q_9a86fc1b1a583b1c9607, q_9a43cb8744b66244d55b, q_1a09df3a1294e55d5d0d, q_34902597b649d6f0115f, q_0dcaebb0bf5c8466d61c, q_6f2d95529c86c3afb033, q_d86091a6d35ed2c8142e, q_9f31bf83cd5cb26c6178); versions bumped (q_11cc3578ab34fb7ed536 v1->v2, q_6528f9dbc4a553760f7d v1->v2, q_7470edf44986934e921d v1->v2, q_7b50e870883dc73ce0f9 v1->v2, q_9a86fc1b1a583b1c9607 v1->v2, q_9a43cb8744b66244d55b v1->v2, q_1a09df3a1294e55d5d0d v1->v2, q_34902597b649d6f0115f v1->v2, q_0dcaebb0bf5c8466d61c v1->v2, q_6f2d95529c86c3afb033 v1->v2, q_d86091a6d35ed2c8142e v1->v2, q_9f31bf83cd5cb26c6178 v1->v2); attrs set (q_34902597b649d6f0115f data-d2,data-d2-id; q_6f2d95529c86c3afb033 data-d2,data-d2-id; q_9f31bf83cd5cb26c6178 data-d2,data-d2-id); ITEMS REMOVED (q_a15b28dce7109b16b9e7, q_53551c863e1c812b0657); prose edited (-4336 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2127 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2127 (axCheck 2127, reveal-only 0) | malformed 0 | crit gridded 149/157 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 8
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-02 s57: Peds MSK: fever, rash and joint pain in the lean style (C8 sexual-history rule and C9 rubella clues fixed); two UWorld stems archived and rewritten; DGI knee clue carried; now a topic brief

```
Page: 216 briefs, 2129 items -> 216 briefs, 2129 items
Briefs changed (4):
  - bs-fever-rash-arthralgia (Fever, Rash and Joint Pain: Name the Rash, Then Date the Exposure): 2 items added (q_b1dd657dad06115ba86e, q_b265dce83e38f49b9dfe); items edited (q_18edf7d26cb5a8ad3e18, q_605646b1eeada5322f53, q_2bdcffda772905c78f3f, q_5413d7739952fa996be1, q_d613f4e6257d5e73b9d2, q_d4e11448e7cb70ea988b); versions bumped (q_18edf7d26cb5a8ad3e18 v1->v2, q_605646b1eeada5322f53 v1->v2, q_2bdcffda772905c78f3f v1->v2, q_5413d7739952fa996be1 v1->v2, q_d613f4e6257d5e73b9d2 v1->v2, q_d4e11448e7cb70ea988b v1->v2); attrs set (brief class; q_18edf7d26cb5a8ad3e18 data-lead-in; q_605646b1eeada5322f53 data-lead-in; q_2bdcffda772905c78f3f data-lead-in; q_5413d7739952fa996be1 data-lead-in; q_d4e11448e7cb70ea988b data-lead-in); ITEMS REMOVED (q_336f9bcf10beebd35742, q_ea5c77c1f0c5c96dd1b4); prose edited (-748 chars)
  - bs-exanthems (Exanthems in a Child): prose edited (+14 chars)
  - bs-anaphylaxis (Anaphylaxis and Its Mimics): prose edited (+14 chars)
  - bs-genital-ulcer (Genital Ulcer: Painless or Painful): prose edited (+14 chars)
Other page changes (nav, headers, scripts): -11 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2129 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2129 (axCheck 2129, reveal-only 0) | malformed 0 | crit gridded 147/156 | vignette gridded 121/121 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-02 s56: Peds MSK: homocystinuria in the lean style as Marfanoid Habitus: Marfan or Homocystinuria? (C7 fixed: no shared skin hyperelasticity; joints usually stiff); pediatric stroke pointer

```
Page: 216 briefs, 2130 items -> 216 briefs, 2129 items
Briefs changed (3):
  - bs-water-soluble-vitamins (Water-Soluble Vitamin Deficiency): prose edited (+11 chars)
  - homocystinuria (Marfanoid Habitus: Marfan or Homocystinuria?): items edited (q_c64e62ecc8495b6c96dd, q_c98add1f86775b51a0ed, q_d1782896a6d5534bab5b, q_11fd51fa7c3852118b6a, q_3687b4682d3f5fad9719, q_be932522d631521e85f9); versions bumped (q_c64e62ecc8495b6c96dd v1->v2, q_c98add1f86775b51a0ed v1->v2, q_d1782896a6d5534bab5b v1->v2, q_11fd51fa7c3852118b6a v1->v2, q_3687b4682d3f5fad9719 v2->v3, q_be932522d631521e85f9 v1->v2); attrs set (q_c64e62ecc8495b6c96dd data-lead-in,data-src; q_c98add1f86775b51a0ed data-lead-in,data-src; q_d1782896a6d5534bab5b data-lead-in,data-src; q_11fd51fa7c3852118b6a data-lead-in,data-src; q_3687b4682d3f5fad9719 data-src; q_be932522d631521e85f9 data-lead-in,data-src); ITEMS REMOVED (q_e37d80e3578051e593a8); prose edited (-1589 chars)
  - bs-peds-stroke (Stroke in a Child or Adolescent): prose edited (+157 chars)
Other page changes (nav, headers, scripts): +11 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2129 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2129 (axCheck 2129, reveal-only 0) | malformed 0 | crit gridded 147/156 | vignette gridded 123/123 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-02 s55: Peds MSK: foot puncture infection (C5 fixed; NBME item to its framing block) and torticollis in the lean style; both now topic briefs; every workup path labelled Diagnostic workup with wider result labels

```
Page: 216 briefs, 2132 items -> 216 briefs, 2130 items
Briefs changed (16):
  - septic-hip (Septic Arthritis in a Child: Aspirate, or Treat and Recheck?): prose edited (+37 chars)
  - limp (The Limping Child: Sick or Well, Then Age and Time): prose edited (+179 chars)
  - sjia (Juvenile Idiopathic Arthritis: Count the Joints, Chart the Fever): prose edited (+37 chars)
  - nursemaid (Child Won't Use the Arm: Reduce or Image?): prose edited (+37 chars)
  - scfe (Slipped Capital Femoral Epiphysis: Keep Off It and Pin It): prose edited (+37 chars)
  - myositis-ossificans (Myositis Ossificans: Did the Pain Resolve and Come Back?): prose edited (+37 chars)
  - growing-pains (Bilateral Leg Pain in a Child: Is the Examination Normal?): prose edited (+37 chars)
  - bone-tumors (Bone Lesion in a Child: Where It Sits and What It Does Next): prose edited (+37 chars)
  - scheuermann (Adolescent Kyphosis: Does the Curve Correct?): prose edited (+37 chars)
  - bs-puncture-osteomyelitis (Foot Puncture Infection: Name the Organism from the Exposure and the Clock): 1 item added (q_de2e508dab3159711357); items edited (q_704d96de81771c775d10, q_7ce0ba2045a93f935d69, q_d5e0eba54097f71a83a0, q_9bee21d9322103ff15d3); versions bumped (q_704d96de81771c775d10 v1->v2, q_7ce0ba2045a93f935d69 v1->v2, q_d5e0eba54097f71a83a0 v1->v2, q_9bee21d9322103ff15d3 v1->v2); attrs set (brief class; q_9bee21d9322103ff15d3 data-lead-in); ITEMS REMOVED (q_a5490882ad76890a739b); prose edited (+2034 chars)
  - bs-torticollis (Infant Head Tilt and Flat Head: Which Way Does the Ear Point?): 1 item added (q_2785e273f637f0e7cd0b); items edited (q_69f93af9bf4857c7ab54, q_2ddf479cfa3b55f88f4a, q_dcee52bc4c4f56a092a9, q_aec0474cacb25d25a252, q_fa278e2e3e52501580b1, q_d667351ae9a15bde8a37, q_1877179a99655cb584b4); versions bumped (q_69f93af9bf4857c7ab54 v1->v2, q_2ddf479cfa3b55f88f4a v1->v2, q_dcee52bc4c4f56a092a9 v1->v2, q_aec0474cacb25d25a252 v1->v2, q_fa278e2e3e52501580b1 v2->v3, q_d667351ae9a15bde8a37 v1->v2, q_1877179a99655cb584b4 v1->v2); attrs set (brief class; q_69f93af9bf4857c7ab54 data-lead-in; q_2ddf479cfa3b55f88f4a data-lead-in; q_dcee52bc4c4f56a092a9 data-lead-in; q_aec0474cacb25d25a252 data-lead-in; q_d667351ae9a15bde8a37 data-lead-in; q_1877179a99655cb584b4 data-lead-in); ITEMS REMOVED (q_36648710cbec530aa34d, q_6180430f0cf75084baa3, q_e85ad792a91453aca090); prose edited (-1024 chars)
  - bs-brachial-plexus (Brachial Plexus Injury at Birth): prose edited (+56 chars)
  - vpshunt (VP Shunt Complications): prose edited (+12 chars)
  - bs-posterior-fossa (Posterior Fossa Localization): prose edited (+12 chars)
  - psychosis-duration (Psychosis in an Adult: Rule Out a Cause, Then Time It): prose edited (+37 chars)
  - bipolar-mania (Bipolar Disorder: Rule Out a Cause, Time the Episode, Then Treat): prose edited (+37 chars)
Other page changes (nav, headers, scripts): +296 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2130 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2130 (axCheck 2130, reveal-only 0) | malformed 0 | crit gridded 146/155 | vignette gridded 124/124 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-02 s54: Peds MSK: bone tumors and Scheuermann kyphosis in the lean style; UWorld-tagged items archived and rewritten; Cobb brace range and bracing key corrected

```
Page: 216 briefs, 2135 items -> 216 briefs, 2132 items
Briefs changed (4):
  - myositis-ossificans (Myositis Ossificans: Did the Pain Resolve and Come Back?): prose edited (+37 chars)
  - bone-tumors (Bone Lesion in a Child: Where It Sits and What It Does Next): 10 items added (q_4f042bb76dcdd1b23ac6, q_15014417bcb8589af99e, q_177d59f0f83da40a3d07, q_5a91f3a8e64b71d10b7f, q_72ed885bcd35d034d6c2, q_f3554e2a2f81c4a2b61b, q_0410f18c21d2947a00ab, q_b8cd77d47bf199b390aa, q_f605a4bdc0172cdea088, q_df659300dd80881cdaf5); items edited (q_cbf97128d38b21671ff4, q_ca9206a2686d8742b3e6, q_06d007897142e41778b7); versions bumped (q_cbf97128d38b21671ff4 v1->v2, q_ca9206a2686d8742b3e6 v1->v2, q_06d007897142e41778b7 v1->v2); attrs set (brief data-nid; q_ca9206a2686d8742b3e6 data-lead-in; q_06d007897142e41778b7 data-lead-in); ITEMS REMOVED (q_05f131195a1d499af5c5, q_fc8a4c70d96070f981bf, q_f82648b5c469af3ad795, q_25c66cd2a65e70d30df9, q_45d3b40a35c32e0e2625, q_a28e60156f3d374cfb79, q_6c42537840ac7172c554, q_9fafc21840a7c64ce3e7, q_947fbc4df7af067f7452, q_f8d69bd8b17167df6bf0, q_0bab8400fb112765766d, q_fd463ef7e471587d0b6f); prose edited (-4067 chars)
  - scheuermann (Adolescent Kyphosis: Does the Curve Correct?): 1 item added (q_23ffc45b0af9a32bb6c0); items edited (q_39e91d80297b5c47a073, q_89c1da7227f55645a440, q_34ce385549f65801b20e, q_835be697ea175939aede); versions bumped (q_39e91d80297b5c47a073 v1->v2, q_89c1da7227f55645a440 v1->v2, q_34ce385549f65801b20e v2->v3, q_835be697ea175939aede v1->v2); attrs set (q_39e91d80297b5c47a073 data-lead-in,data-src; q_89c1da7227f55645a440 data-lead-in,data-src; q_34ce385549f65801b20e data-d2,data-d2-id,data-src; q_835be697ea175939aede data-lead-in,data-src); ITEMS REMOVED (q_06441347dbbe55a598b0, q_b2761b2f13b45b98bf63); prose edited (-1275 chars)
  - bs-nat-fracture (Suspected Child Abuse: Fractures and the Next Step): prose edited (+24 chars)
Other page changes (nav, headers, scripts): +10 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2132 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2132 (axCheck 2132, reveal-only 0) | malformed 0 | crit gridded 145/154 | vignette gridded 126/126 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-02 s53: Peds MSK: septic arthritis Kocher ladder named as the Kocher criteria, 3 and 4 rows tinted, 99.6% and derivation cite restored

```
Page: 216 briefs, 2135 items -> 216 briefs, 2135 items
Briefs changed (1):
  - septic-hip (Septic Arthritis in a Child: Aspirate, or Treat and Recheck?): prose edited (+242 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2135 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2135 (axCheck 2135, reveal-only 0) | malformed 0 | crit gridded 143/152 | vignette gridded 128/128 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-02 s52: Peds MSK: growing pains and benign acute childhood myositis merged in the lean style; NBME item moved to its framing block; night-pain (C4) and normal-strength (C6) contradictions fixed

```
Page: 217 briefs, 2140 items -> 216 briefs, 2135 items
Briefs REMOVED (1): bs-acute-myositis
Briefs changed (4):
  - limp (The Limping Child: Sick or Well, Then Age and Time): prose edited (+30 chars)
  - growing-pains (Bilateral Leg Pain in a Child: Is the Examination Normal?): items edited (q_f075f176703357309252, q_f3dc1a58d1a45216880e, q_790ff3a627b65e83b421, q_bcc4863685195098a913, q_6140b09fbc6e5920933e, q_2be9b5858d8d5f0a9395, q_0a1e03e56a43beb4d4ea, q_eee554b97996ff32f98f, q_0dad14c5794f68ff48b6, q_ae7c9f939696360148fe, q_0cd4c5408d7826fced82, q_605ba04e7d17d27321bf, q_466ecbed11f7240a758a); versions bumped (q_f075f176703357309252 v1->v2, q_f3dc1a58d1a45216880e v1->v2, q_790ff3a627b65e83b421 v1->v2, q_bcc4863685195098a913 v1->v2, q_6140b09fbc6e5920933e v1->v2, q_2be9b5858d8d5f0a9395 v1->v2, q_0a1e03e56a43beb4d4ea v1->v2, q_eee554b97996ff32f98f v1->v2, q_0dad14c5794f68ff48b6 v1->v2, q_ae7c9f939696360148fe v1->v2, q_0cd4c5408d7826fced82 v1->v2, q_605ba04e7d17d27321bf v1->v2, q_466ecbed11f7240a758a v1->v2); attrs set (brief data-replaces; q_f075f176703357309252 data-lead-in,data-src; q_f3dc1a58d1a45216880e data-lead-in,data-src; q_790ff3a627b65e83b421 data-lead-in,data-src; q_bcc4863685195098a913 data-lead-in,data-src; q_6140b09fbc6e5920933e data-d2,data-d2-id,data-lead-in,data-src; q_2be9b5858d8d5f0a9395 data-lead-in,data-src; q_eee554b97996ff32f98f data-lead-in; q_0dad14c5794f68ff48b6 data-d1,data-d1-id,data-lead-in; q_0cd4c5408d7826fced82 data-lead-in; q_605ba04e7d17d27321bf data-lead-in; q_466ecbed11f7240a758a data-lead-in); ITEMS REMOVED (q_221ed46f62e95f1cb568, q_9b7f03f4b6c152c59c44, q_403fcdb90cff5998a96a, q_38c7e742eb905a3ea7c1); prose edited (+343 chars)
  - bone-tumors (Bone Tumors: Location, Film, Course): prose edited (+30 chars)
  - bs-leukemia (Pediatric Acute Lymphoblastic Leukemia): prose edited (+30 chars)
Other page changes (nav, headers, scripts): -78 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 216 briefs, 2135 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 216 | bankwraps 216 | mcq 2135 (axCheck 2135, reveal-only 0) | malformed 0 | crit gridded 143/152 | vignette gridded 128/128 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-02 s51: Peds MSK: myositis ossificans in the lean style; untagged UWorld stem archived with its clues carried

```
Page: 217 briefs, 2142 items -> 217 briefs, 2140 items
Briefs changed (2):
  - myositis-ossificans (Myositis Ossificans: Did the Pain Resolve and Come Back?): 1 item added (q_07ecd53e7f8003f1e0ee); items edited (q_178b5428ce1554dfa17d, q_8e6c3c2ffa8758a7910e, q_65ef142520e15e1ea279, q_c153950959465fdfad77, q_d1227a8f9f6d51288261, q_7d00ae33f0525f3b9f24, q_c1e9f75aa54256a592b7); versions bumped (q_178b5428ce1554dfa17d v1->v2, q_8e6c3c2ffa8758a7910e v1->v2, q_65ef142520e15e1ea279 v1->v2, q_c153950959465fdfad77 v1->v2, q_d1227a8f9f6d51288261 v1->v2, q_7d00ae33f0525f3b9f24 v1->v2, q_c1e9f75aa54256a592b7 v1->v2); attrs set (q_178b5428ce1554dfa17d data-lead-in,data-src; q_8e6c3c2ffa8758a7910e data-lead-in,data-src; q_65ef142520e15e1ea279 data-d2,data-d2-id,data-lead-in,data-src; q_c153950959465fdfad77 data-lead-in,data-src; q_d1227a8f9f6d51288261 data-d2,data-d2-id,data-lead-in,data-src; q_7d00ae33f0525f3b9f24 data-lead-in,data-src; q_c1e9f75aa54256a592b7 data-d1,data-d1-id,data-lead-in,data-src); ITEMS REMOVED (q_6d1f3fc9cc1e56b3bd79, q_ef711f1688d35b828e35, q_ef1afb160c6a53dabb70); prose edited (-3823 chars)
  - bone-tumors (Bone Tumors: Location, Film, Course): prose edited (+28 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 217 briefs, 2140 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 217 | bankwraps 217 | mcq 2140 (axCheck 2140, reveal-only 0) | malformed 0 | crit gridded 142/151 | vignette gridded 130/130 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s50: Peds MSK: Child Won't Use the Arm (nursemaid) in the lean style

```
Page: 217 briefs, 2141 items -> 217 briefs, 2142 items
Briefs changed (2):
  - nursemaid (Child Won't Use the Arm: Reduce or Image?): 2 items added (q_6439d0e8c27422ee6bc7, q_64b61b0020de46f9f1c4); items edited (q_24718170482e5e118f19, q_fb622f5f0dc05f8aa6c3, q_a187fb9da9815bdda106, q_2a3ffd6515f3560095ae, q_5ca49edd96a950829343); versions bumped (q_24718170482e5e118f19 v1->v2, q_fb622f5f0dc05f8aa6c3 v1->v2, q_a187fb9da9815bdda106 v1->v2, q_2a3ffd6515f3560095ae v1->v2, q_5ca49edd96a950829343 v1->v2); attrs set (q_24718170482e5e118f19 data-lead-in,data-src; q_fb622f5f0dc05f8aa6c3 data-lead-in,data-src; q_a187fb9da9815bdda106 data-d2,data-d2-id,data-lead-in,data-src; q_2a3ffd6515f3560095ae data-lead-in,data-src; q_5ca49edd96a950829343 data-d2,data-d2-id,data-lead-in,data-src); ITEMS REMOVED (q_010e5b2ce53f59ccad3c); prose edited (+4640 chars)
  - bs-brachial-plexus (Brachial Plexus Injury at Birth): prose edited (+24 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 217 briefs, 2142 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 217 | bankwraps 217 | mcq 2142 (axCheck 2142, reveal-only 0) | malformed 0 | crit gridded 141/150 | vignette gridded 131/131 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s49: Peds MSK: JIA in the lean style; marrow before steroids when two cell lines are low; ACR 2019 uveitis screening

```
Page: 217 briefs, 2143 items -> 217 briefs, 2141 items
Briefs changed (2):
  - sjia (Juvenile Idiopathic Arthritis: Count the Joints, Chart the Fever): 5 items added (q_0f7039a8128a160ee26f, q_5304b137e326cefcec33, q_bb45f716de4a588aa25f, q_ab91a933c728ee27ec93, q_94d37339abbed3d36af3); items edited (q_3ec85d8e49895dc4a6ef, q_c0cb38b7ae515422b0ce, q_74820586b4ee51eebb04, q_8df973d7f65e57c9b4b8, q_3811fdc226a16772e13e, q_263275a6169156bf83a0); versions bumped (q_3ec85d8e49895dc4a6ef v1->v2, q_c0cb38b7ae515422b0ce v1->v2, q_74820586b4ee51eebb04 v1->v2, q_8df973d7f65e57c9b4b8 v1->v2, q_3811fdc226a16772e13e v1->v2, q_263275a6169156bf83a0 v1->v2); attrs set (q_3ec85d8e49895dc4a6ef data-d2,data-d2-id,data-lead-in,data-src; q_c0cb38b7ae515422b0ce data-d1,data-d1-id,data-d2,data-d2-id,data-lead-in,data-src; q_74820586b4ee51eebb04 data-lead-in,data-src; q_8df973d7f65e57c9b4b8 data-lead-in,data-src; q_3811fdc226a16772e13e data-lead-in; q_263275a6169156bf83a0 data-lead-in); ITEMS REMOVED (q_ac99dd9b7ab65669bec0, q_0f7557200bb25f49a751, q_0fb09262014f533ba0e0, q_25275156dd3956f7b1f0, q_956f0e2bffc85690b987, q_dcc21109d541cdb738b2, q_814a1b11d69f739125b9); prose edited (+25 chars)
  - bs-leukemia (Pediatric Acute Lymphoblastic Leukemia): prose edited (+35 chars)
Other page changes (nav, headers, scripts): +0 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 217 briefs, 2141 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 217 | bankwraps 217 | mcq 2141 (axCheck 2141, reveal-only 0) | malformed 0 | crit gridded 139/148 | vignette gridded 131/131 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s48: Peds MSK: limping-child cluster in the lean style; septic-hip absorbs transient synovitis and its management brief; limp and scfe reauthored

```
Page: 219 briefs, 2161 items -> 217 briefs, 2143 items
Briefs REMOVED (2): synovitis, bs-synovitis-mgmt
Briefs changed (8):
  - septic-hip (Septic Arthritis in a Child: Aspirate, or Treat and Recheck?): 4 items added (q_704d82a8b57f71bfefe3, q_2a8d348cbfed5bfe7123, q_23dedfb4a0276563ad3f, q_be3b8b383d754716ae30); items edited (q_14fa267d79fe510e8c81, q_75e2d3b095515e83aa22, q_ed207f159bb65ba98286, q_5fc72e65e76553a39bcc, q_144c6f99900458208ce0, q_34e4d21df9525a569ddb, q_e7e5430c61105202b45d, q_90907b616bed5f629949, q_82f761dc6ed7518eae1b); versions bumped (q_14fa267d79fe510e8c81 v1->v2, q_75e2d3b095515e83aa22 v1->v2, q_ed207f159bb65ba98286 v1->v2, q_5fc72e65e76553a39bcc v1->v2, q_144c6f99900458208ce0 v2->v3, q_34e4d21df9525a569ddb v1->v2, q_e7e5430c61105202b45d v1->v2, q_90907b616bed5f629949 v1->v2, q_82f761dc6ed7518eae1b v1->v2); attrs set (brief data-nid,data-replaces; q_14fa267d79fe510e8c81 data-lead-in,data-src; q_75e2d3b095515e83aa22 data-lead-in,data-src; q_ed207f159bb65ba98286 data-d1,data-d1-id,data-d2,data-d2-id,data-lead-in,data-src; q_5fc72e65e76553a39bcc data-lead-in,data-src; q_144c6f99900458208ce0 data-src; q_34e4d21df9525a569ddb data-lead-in,data-src; q_e7e5430c61105202b45d data-lead-in,data-src; q_90907b616bed5f629949 data-lead-in,data-src; q_82f761dc6ed7518eae1b data-lead-in,data-src); ITEMS REMOVED (q_18e8c3eeafb65030ae6a, q_38058079f43656f9af6d, q_e4d5a5deb5c859c0842d, q_1c5c95ee8ec9588394f5, q_6317a30c6b5d530ca106); prose edited (+5300 chars)
  - limp (The Limping Child: Sick or Well, Then Age and Time): items edited (q_bdee86ce98775e1e9a3f, q_11abb36f6ad6ea3085a4, q_734cdaa7b585522dbb51, q_f4f48dfd36df5c08b6d9, q_879f0b60f4f452e09820, q_33b90401a72c5bbfba10, q_069c75f1bef557f7b1bb, q_c1f4667f9db45a88bc0d, q_18241f64b48e542aad5c); versions bumped (q_bdee86ce98775e1e9a3f v1->v2, q_11abb36f6ad6ea3085a4 v1->v2, q_734cdaa7b585522dbb51 v1->v2, q_f4f48dfd36df5c08b6d9 v1->v2, q_879f0b60f4f452e09820 v1->v2, q_33b90401a72c5bbfba10 v1->v2, q_069c75f1bef557f7b1bb v1->v2, q_c1f4667f9db45a88bc0d v2->v3, q_18241f64b48e542aad5c v1->v2); attrs set (q_bdee86ce98775e1e9a3f data-lead-in,data-src; q_11abb36f6ad6ea3085a4 data-d2,data-d2-id; q_734cdaa7b585522dbb51 data-lead-in,data-src; q_f4f48dfd36df5c08b6d9 data-lead-in,data-src; q_879f0b60f4f452e09820 data-lead-in,data-src; q_33b90401a72c5bbfba10 data-lead-in,data-src; q_069c75f1bef557f7b1bb data-lead-in,data-src; q_c1f4667f9db45a88bc0d data-src; q_18241f64b48e542aad5c data-lead-in,data-src); ITEMS REMOVED (q_9621c3ac5eac5a3ea86b, q_a73aa8bda21c559fa678, q_b599f8e62f2070a52991); prose edited (+6427 chars)
  - scfe (Slipped Capital Femoral Epiphysis: Keep Off It and Pin It): 1 item added (q_c4752c99840e5fc84b7a); items edited (q_e04e23db080c508f930f, q_1e0294ade15759f89757, q_0107df0993795069b36a, q_d8aec8c3755f53ca843b, q_619cbce0b95b55c6b403, q_7b247bb620b6c48be44d); versions bumped (q_e04e23db080c508f930f v1->v2, q_1e0294ade15759f89757 v1->v2, q_0107df0993795069b36a v1->v2, q_d8aec8c3755f53ca843b v1->v2, q_619cbce0b95b55c6b403 v1->v2, q_7b247bb620b6c48be44d v1->v2); attrs set (q_e04e23db080c508f930f data-d2,data-d2-id,data-lead-in,data-src; q_1e0294ade15759f89757 data-lead-in,data-src; q_0107df0993795069b36a data-lead-in,data-src; q_d8aec8c3755f53ca843b data-lead-in,data-src; q_619cbce0b95b55c6b403 data-lead-in,data-src; q_7b247bb620b6c48be44d data-d1,data-d1-id,data-lead-in); ITEMS REMOVED (q_d141b8e3707e553eb3f2, q_8979ec9d9d6a5894b815, q_854d7a42ba8559208887, q_8358e863b9a7587cb33d, q_9777dcb58c677902b75f); prose edited (+1279 chars)
  - myositis-ossificans (The Post-Traumatic Limb Mass): prose edited (+42 chars)
  - growing-pains (Benign Limb Pain in a Child): prose edited (+42 chars)
  - bs-septic-adult (The Acute Hot Joint (adult)): prose edited (-13 chars)
  - bs-puncture-osteomyelitis (Foot Puncture Wound Infection): prose edited (+33 chars)
  - bs-leukemia (Pediatric Acute Lymphoblastic Leukemia): prose edited (+18 chars)
Other page changes (nav, headers, scripts): +260 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 217 briefs, 2143 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 217 | bankwraps 217 | mcq 2143 (axCheck 2143, reveal-only 0) | malformed 0 | crit gridded 138/147 | vignette gridded 131/131 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s47: phones and tablets: Index is a frosted pill at the top left that hides while scrolling

```
Page: 219 briefs, 2161 items -> 219 briefs, 2161 items
Other page changes (nav, headers, scripts): +514 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2161 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2161 (axCheck 2161, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s46: timelines: every row carries its own scale under its bars, with a time arrow

```
Page: 219 briefs, 2161 items -> 219 briefs, 2161 items
Briefs changed (2):
  - psychosis-duration (Psychosis in an Adult: Rule Out a Cause, Then Time It): prose edited (+650 chars)
  - bipolar-mania (Bipolar Disorder: Rule Out a Cause, Time the Episode, Then Treat): prose edited (+738 chars)
Other page changes (nav, headers, scripts): +581 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2161 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2161 (axCheck 2161, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s45: phones and tablets: Index opens from a tap tab on the left edge; sidebar label Bipolar Disorder

```
Page: 219 briefs, 2161 items -> 219 briefs, 2161 items
Other page changes (nav, headers, scripts): +2297 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2161 items, 6 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2161 (axCheck 2161, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s44: BOARD-STYLE ONLY resets to off on every visit

```
Page: 219 briefs, 2161 items -> 219 briefs, 2161 items
Other page changes (nav, headers, scripts): -13 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2161 items, 5 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2161 (axCheck 2161, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s43: version label and update check: the page shows its build and offers a refresh when a newer one is live

```
Page: 219 briefs, 2161 items -> 219 briefs, 2161 items
Other page changes (nav, headers, scripts): +3298 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2161 items, 5 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2161 (axCheck 2161, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s42: psychosis and bipolar questions: 30 to 40 words in scannable lines; NBME blocks; adversarial audit fixes

```
Page: 219 briefs, 2163 items -> 219 briefs, 2161 items
Briefs changed (2):
  - psychosis-duration (Psychosis in an Adult: Rule Out a Cause, Then Time It): items edited (q_825dd34c39a6fefa51c5, q_7dfe8050588133fa1bce, q_b3db6c76ffbbc3d98f8c, q_84e5c9dd0796f8bbc02d, q_29765c80940704a6c8b7, q_d94a444dc335c58a8169, q_4f7e99d406dda2fff18d, q_5af4628002a964e1149f, q_733a1cffb70304fef48c); versions bumped (q_825dd34c39a6fefa51c5 v2->v3, q_7dfe8050588133fa1bce v1->v2, q_b3db6c76ffbbc3d98f8c v2->v3, q_84e5c9dd0796f8bbc02d v4->v5, q_29765c80940704a6c8b7 v2->v3, q_d94a444dc335c58a8169 v2->v3, q_4f7e99d406dda2fff18d v2->v3, q_5af4628002a964e1149f v1->v2, q_733a1cffb70304fef48c v2->v3); attrs set (q_b3db6c76ffbbc3d98f8c data-d2,data-d2-id; q_29765c80940704a6c8b7 data-key-id; q_d94a444dc335c58a8169 data-d2,data-d2-id; q_4f7e99d406dda2fff18d data-d2,data-d2-id; q_5af4628002a964e1149f data-d2,data-d2-id); ITEMS REMOVED (q_f0f5f514ad0d6cb6928d, q_88c6314e2d98a8d9bb01); prose edited (+1865 chars)
  - bipolar-mania (Bipolar Disorder: Rule Out a Cause, Time the Episode, Then Treat): items edited (q_642294f71730fdce3fb8, q_cd2d3326193e35c8ef02, q_50864e4faace903913cf, q_bad56dc6413aaac87c48, q_7dc58d2f1afc9954f4a2, q_875af1ee71c6f2502d97, q_662161d54e6b8e321eef, q_e14998f0caa852bf05de, q_0c3b63b494f28be9d776, q_27f9ad042d7a0119e0e3, q_293aa90f0e5f09f9f42f, q_83176e5864a0d4fdea0c, q_cc8ff30e23e43a1a0d5b); versions bumped (q_642294f71730fdce3fb8 v2->v3, q_cd2d3326193e35c8ef02 v2->v3, q_50864e4faace903913cf v2->v3, q_bad56dc6413aaac87c48 v2->v3, q_7dc58d2f1afc9954f4a2 v2->v3, q_875af1ee71c6f2502d97 v2->v3, q_662161d54e6b8e321eef v2->v3, q_e14998f0caa852bf05de v2->v3, q_0c3b63b494f28be9d776 v2->v3, q_27f9ad042d7a0119e0e3 v2->v3, q_293aa90f0e5f09f9f42f v2->v3, q_83176e5864a0d4fdea0c v2->v3, q_cc8ff30e23e43a1a0d5b v2->v3); attrs set (q_7dc58d2f1afc9954f4a2 data-d2,data-d2-id; q_83176e5864a0d4fdea0c data-d2,data-d2-id); prose edited (+377 chars)
Other page changes (nav, headers, scripts): +717 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2161 items, 4 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2161 (axCheck 2161, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s41: faster startup: word-count self-check runs only under the ship check

```
Page: 219 briefs, 2163 items -> 219 briefs, 2163 items
Other page changes (nav, headers, scripts): +306 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2163 items, 4 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2163 (axCheck 2163, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-10-01 s40: bipolar brief lean reauthor; NBME question blocks; mnemonic letter column

```
Page: 219 briefs, 2165 items -> 219 briefs, 2163 items
Briefs changed (1):
  - bipolar-mania (Bipolar Disorder: Rule Out a Cause, Time the Episode, Then Treat): items edited (q_642294f71730fdce3fb8, q_cd2d3326193e35c8ef02, q_50864e4faace903913cf, q_bad56dc6413aaac87c48, q_7dc58d2f1afc9954f4a2, q_875af1ee71c6f2502d97, q_662161d54e6b8e321eef, q_e14998f0caa852bf05de, q_0c3b63b494f28be9d776, q_27f9ad042d7a0119e0e3, q_293aa90f0e5f09f9f42f, q_83176e5864a0d4fdea0c, q_cc8ff30e23e43a1a0d5b); versions bumped (q_642294f71730fdce3fb8 v1->v2, q_cd2d3326193e35c8ef02 v1->v2, q_50864e4faace903913cf v1->v2, q_bad56dc6413aaac87c48 v1->v2, q_7dc58d2f1afc9954f4a2 v1->v2, q_875af1ee71c6f2502d97 v1->v2, q_662161d54e6b8e321eef v1->v2, q_e14998f0caa852bf05de v1->v2, q_0c3b63b494f28be9d776 v1->v2, q_27f9ad042d7a0119e0e3 v1->v2, q_293aa90f0e5f09f9f42f v1->v2, q_83176e5864a0d4fdea0c v1->v2, q_cc8ff30e23e43a1a0d5b v1->v2); ITEMS REMOVED (q_e20f782cdbb589ed02db, q_56071dee18c65a08d431); prose edited (-3704 chars)
Other page changes (nav, headers, scripts): +2319 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2163 items, 4 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2163 (axCheck 2163, reveal-only 0) | malformed 0 | crit gridded 133/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 9
  vendor: clean (56601 source shingles; page 0.027%)
```

## 2026-10-01 s39: psychosis brief v7.1: horizontal timelines, workup path, bottom line lists

```
Page: 219 briefs, 2165 items -> 219 briefs, 2165 items
Briefs changed (1):
  - psychosis-duration (Psychosis in an Adult: Rule Out a Cause, Then Time It): items edited (q_84e5c9dd0796f8bbc02d); versions bumped (q_84e5c9dd0796f8bbc02d v3->v4); prose edited (+4469 chars)
Other page changes (nav, headers, scripts): +18359 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2165 items, 4 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2165 (axCheck 2165, reveal-only 0) | malformed 0 | crit gridded 132/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 10
  vendor: clean (56601 source shingles; page 0.028%)
```

## 2026-09-29 s38: psychosis-duration reauthored lean (1,301 to 457 words before the bank; 11 of 16 questions kept, 5 retired to the ledger); gate: retired-items ledger; coverage notes without option text

```
Page: 219 briefs, 2170 items -> 219 briefs, 2165 items
Briefs changed (1):
  - psychosis-duration (Psychosis in an Adult: Rule Out a Cause, Then Time It): ITEMS REMOVED (q_ff7cd239aba8bc48494b, q_695074e8d5332d0ea095, q_72ee5fbedbdc1fefbe82, q_eba4e1309651d19e9c72, q_afb8a32a559bb96e09b0); prose edited (-9907 chars)
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2165 items, 4 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2165 (axCheck 2165, reveal-only 0) | malformed 0 | crit gridded 131/141 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 10
  vendor: clean (56601 source shingles; page 0.027%)
```

## 2026-09-29 s37: Psych goes live for review: psych shelf and section, Type C page setup, 9 psych briefs (1 reviewer-accepted, 2 revised awaiting re-review, 6 first drafts with open review findings); Kawasaki migrated to Type C

```
Page: 210 briefs, 2050 items -> 219 briefs, 2170 items
Briefs added (9):
  - psychosis-duration: Psychosis in an Adult: Exclude a Cause, Then Time It Against Mood (16 items)
  - bipolar-mania: Elevated or Irritable Mood: Mania, Hypomania, and What to Start or Stop (15 items)
  - sz-psychosocial: Schizophrenia on Treatment: Psychosocial Care and Relapse Prevention (12 items)
  - delirium: Delirium: Tell It From Dementia and Psychosis, Then Find the Cause (14 items)
  - panic: Panic Disorder and Its Mimics: Which Anxiety, and How to Treat (16 items)
  - ssri-effects: SSRI (Selective Serotonin Reuptake Inhibitor) Adverse Effects: Name the Effect, Then Take the Next Step (11 items)
  - lithium-effects: The Patient on Lithium: Which Complication, and What to Do (12 items)
  - ipv: Intimate Partner Violence in an Adult: Plan for Safety, Report by Who Is at Risk (12 items)
  - gppd: Genito-Pelvic Pain/Penetration Disorder (Vaginismus): Exclude a Body Cause, Then Treat (9 items)
Briefs changed (1):
  - kawasaki (Kawasaki Disease): 3 items added (q_04918d28cea78d6d6e3f, q_8cb1497234ec678c9c04, q_1f532fe33cf4a10989c4); items edited (q_5c5ebd26ef5fe11337d5, q_0042a68171af5dfcac32, q_b9ce689609a95206a0ec, q_3c83fb8f43705e428d06, q_12be6cdeb54f52f8a101, q_4b45441faba2500fa091, q_c99ce2a03174582f9a18, q_cc99efd4118359b5b9b9, q_495dfa71396b7036d94a, q_e96fadc94a8327131c75); versions bumped (q_5c5ebd26ef5fe11337d5 v1->v2, q_0042a68171af5dfcac32 v1->v2, q_b9ce689609a95206a0ec v1->v2, q_3c83fb8f43705e428d06 v1->v2, q_12be6cdeb54f52f8a101 v1->v2, q_4b45441faba2500fa091 v1->v2, q_c99ce2a03174582f9a18 v1->v2, q_cc99efd4118359b5b9b9 v1->v2, q_495dfa71396b7036d94a v1->v2, q_e96fadc94a8327131c75 v1->v2); attrs set (q_0042a68171af5dfcac32 data-lead-in,data-src; q_b9ce689609a95206a0ec data-lead-in,data-src; q_3c83fb8f43705e428d06 data-d1,data-lead-in,data-src; q_12be6cdeb54f52f8a101 data-lead-in,data-src; q_4b45441faba2500fa091 data-d2,data-d2-id,data-lead-in,data-src; q_c99ce2a03174582f9a18 data-lead-in,data-src; q_cc99efd4118359b5b9b9 data-d2,data-d2-id,data-lead-in,data-src; q_495dfa71396b7036d94a data-lead-in); prose edited (+8720 chars)
Other page changes (nav, headers, scripts): +10869 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 219 briefs, 2170 items, 4 scripts, 35 checks, base HEAD | allowlisted 29 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 219 | bankwraps 219 | mcq 2170 (axCheck 2170, reveal-only 0) | malformed 0 | crit gridded 130/142 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 12
  vendor: clean (56601 source shingles; page 0.030%)
```

## 2026-09-25 s35: NBME Peds batch: 12 questions; 3 new briefs (infant vaccines, distal RTA, eyelid lumps), 7 backfills, distractor-design lines, wording guide

```
Page: 207 briefs, 2019 items -> 210 briefs, 2050 items
Briefs added (3):
  - bs-distal-rta: Hypokalemia with Acidosis in a Child (6 items)
  - bs-eyelid-lump: Eyelid Lumps and Swelling in a Child (6 items)
  - bs-infant-vax: Vaccines at the Infant Visits (4 items)
Briefs changed (14):
  - scfe (Slipped Capital Femoral Epiphysis): 2 items added (q_9777dcb58c677902b75f, q_7b247bb620b6c48be44d); prose edited (+2099 chars)
  - bs-ftt (Faltering Weight): prose edited (+191 chars)
  - secondary-htn (Secondary Hypertension): prose edited (+123 chars)
  - ped-murmur (Innocent vs Pathologic Murmurs): attrs set (q_fb94648142ed51749518 data-nbme); prose edited (+377 chars)
  - asthma-copd (Asthma vs. COPD): 2 items added (q_ef221864398f38009057, q_62afba1e07c95c8bb96f); prose edited (+1893 chars)
  - mycoplasma (Pediatric Community-Acquired Pneumonia): 2 items added (q_3f80feff189643e5acb8, q_796b44ec19796e951653); prose edited (+1824 chars)
  - bs-puv (Posterior Urethral Valves and Potter Sequence): 3 items added (q_5754bf5b284e1769cd62, q_1381ab09fca86d44a63e, q_6136bdea9d7844504d8c); prose edited (+2837 chars)
  - bs-abdominal-mass (Abdominal Mass in a Young Child): 2 items added (q_bfc284022b65919965b9, q_42896c8b4bbc936c7b15); prose edited (+2679 chars)
  - precocious-puberty (Precocious Puberty): 2 items added (q_a2533eb69947cf65b1ad, q_4ff187b2c8440f379d9a); prose edited (+3234 chars)
  - cgd (Recurrent Abscesses and Granulomas): attrs set (q_1f7b49f7314459b8b98f data-nbme); prose edited (+331 chars)
  - bs-exanthems (Exanthems in a Child): 2 items added (q_23d551c586e63e046a7a, q_6e288e9ba1a8a754195a); prose edited (+2907 chars)
  - redeye (The Red Eye): prose edited (+244 chars)
  - abrs-complications (Sinusitis with Intracranial Extension): prose edited (+249 chars)
  - bs-adolescent-vax (Adolescent Immunization and the Age Platform): prose edited (+102 chars)
Other page changes (nav, headers, scripts): +4263 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 210 briefs, 2050 items, 4 scripts, 31 checks, base HEAD | allowlisted 12 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 210 | bankwraps 210 | mcq 2050 (axCheck 2050, reveal-only 0) | malformed 0 | crit gridded 125/126 | vignette gridded 132/132 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (50361 source shingles; page 0.031%)
```

## 2026-09-25 s34: NBME Peds batch: FAS, rickets alkaline phosphatase, ITP mechanism; factor-inhibitor cleanup

```
Page: 207 briefs, 2014 items -> 207 briefs, 2019 items
Briefs changed (4):
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): 2 items added (q_f1da4cfcf0b5965ee660, q_a6f735a57b23ad49910f); prose edited (+2349 chars)
  - factor-inhibitor (Hemophilia A Inhibitor): prose edited (-132 chars)
  - aq-bruising (Bruising and Purpura in a Child): 2 items added (q_ee5e56588e265abea6ad, q_179857279bfa2f2d0870); prose edited (+2511 chars)
  - teratogens (Teratogenic Exposures): 1 item added (q_25742c68c19ec216b8d0); prose edited (+2767 chars)
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 207 briefs, 2019 items, 4 scripts, 31 checks, base HEAD | allowlisted 12 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 207 | bankwraps 207 | mcq 2019 (axCheck 2019, reveal-only 0) | malformed 0 | crit gridded 123/124 | vignette gridded 129/129 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (44118 source shingles; page 0.031%)
```

## 2026-09-25 s33: Plain-voice pass on all remaining systems; trap lines use colons; Distractors label

```
Page: 207 briefs, 2014 items -> 207 briefs, 2014 items
Briefs changed (189):
  - pmr (Polymyalgia Rheumatica): prose edited (+203 chars)
  - biceps (Biceps Tendinitis): prose edited (+143 chars)
  - cts (Carpal Tunnel Syndrome): prose edited (-9 chars)
  - dequervain (De Quervain Tendinopathy): prose edited (+160 chars)
  - meralgia (Meralgia Paresthetica): prose edited (+141 chars)
  - scaphoid (Scaphoid Fracture): prose edited (+176 chars)
  - backpain (Low Back Pain: Red Flags): prose edited (+24 chars)
  - hippos (Hip Positioning: Fracture vs. Dislocation): prose edited (+113 chars)
  - gtps (Pain Around the Hip and Thigh): prose edited (+198 chars)
  - inflam-back (Inflammatory Back Pain & Spondyloarthritis): prose edited (+119 chars)
  - oa-pharm (Osteoarthritis Pharmacotherapy): prose edited (+294 chars)
  - septic-bursitis (Septic Bursitis): prose edited (+64 chars)
  - septic-hip (Septic Arthritis of the Hip): prose edited (+224 chars)
  - synovitis (Transient Synovitis Mirror twin): prose edited (-44 chars)
  - limp (The Limping Child — Master Table): prose edited (+190 chars)
  - sjia (Juvenile Idiopathic Arthritis): prose edited (+494 chars)
  - nursemaid (Nursemaid's Elbow): prose edited (+39 chars)
  - scfe (Slipped Capital Femoral Epiphysis): prose edited (-9 chars)
  - myositis-ossificans (The Post-Traumatic Limb Mass): prose edited (-337 chars)
  - growing-pains (Benign Limb Pain in a Child): prose edited (-398 chars)
  - bone-tumors (Bone Tumors: Location, Film, Course): prose edited (+79 chars)
  - scheuermann (Scheuermann Kyphosis): prose edited (-71 chars)
  - bs-septic-adult (The Acute Hot Joint (adult)): prose edited (-94 chars)
  - bs-lbp-acute (Acute Low Back Pain with No Red Flags): prose edited (+2 chars)
  - bs-synovitis-mgmt (Transient Synovitis: Management): prose edited (+197 chars)
  - bs-puncture-osteomyelitis (Foot Puncture Wound Infection): prose edited (-28 chars)
  - bs-acute-myositis (Benign Acute Childhood Myositis): prose edited (-32 chars)
  - bs-torticollis (Congenital Muscular Torticollis and Plagiocephaly): prose edited (-148 chars)
  - bs-brachial-plexus (Brachial Plexus Injury at Birth): prose edited (+20 chars)
  - shoulder-rom (Shoulder Pain: the Range-of-Motion Rule): prose edited (+198 chars)
  - growth (Growth & Developmental Milestones): prose edited (-57 chars)
  - neonatal-maternal-labs (Maternal Carryover in Newborn Labs): prose edited (+62 chars)
  - newborn-hormone (Maternal Hormone Effects in the Newborn): prose edited (-398 chars)
  - aneuploidy (Aneuploidy: Reading the Newborn): prose edited (-333 chars)
  - malform-syndromes (Multiple Anomalies in a Newborn): prose edited (-381 chars)
  - bs-learning (Specific Learning Disorder): prose edited (-82 chars)
  - bs-nat-fracture (Suspected Child Abuse: Fractures and the Next Step): prose edited (+115 chars)
  - bs-shock (Shock in Children): prose edited (-93 chars)
  - bs-infant-feeding (Infant Feeding at Six Months): prose edited (+44 chars)
  - bs-tanner (Sexual Maturity Rating): prose edited (-176 chars)
  - bs-ftt (Faltering Weight): prose edited (-97 chars)
  - bs-preterm-followup (Prematurity Follow-Up and Corrected Age): prose edited (+59 chars)
  - aq-infant-hypotonia (Hypotonia in an Infant): prose edited (+310 chars)
  - chf (Heart Failure: Reducing Hospitalization): prose edited (+291 chars)
  - ascvd (Statins & the 10-Year ASCVD Risk Assessment): prose edited (+545 chars)
  - angina (Anginal Equivalents & Stress Test Selection): prose edited (+314 chars)
  - ie-ppx (Infective Endocarditis Prophylaxis): prose edited (+191 chars)
  - secondary-htn (Secondary Hypertension): prose edited (+358 chars)
  - dvt (DVT & Pulmonary Embolism): prose edited (+218 chars)
  - ped-murmur (Innocent vs Pathologic Murmurs): prose edited (-194 chars)
  - cyanotic-chd (Cyanotic Congenital Heart Disease): prose edited (+410 chars)
  - right-murmurs (Right-Sided Murmurs: Pulmonic Stenosis & Tricuspid Regurgitation): prose edited (+156 chars)
  - htn-drugs (Hypertension: Workup & Drug Choice): prose edited (+209 chars)
  - newborn-cyanosis (Cyanosis in the Newborn): prose edited (-322 chars)
  - kawasaki (Kawasaki Disease): prose edited (+175 chars)
  - arf (Acute Rheumatic Fever): prose edited (+245 chars)
  - myocarditis (New Heart Failure in a Child): prose edited (-153 chars)
  - del22q11 (22q11.2 Deletion Syndrome): prose edited (-351 chars)
  - bs-murmur-map (Murmur Man and Post-ToF Pulmonic Regurgitation): prose edited (-62 chars)
  - bs-shunt-timing (Congenital Shunts and the Transitional Clock): prose edited (+54 chars)
  - bs-adolescent-bp (Confirming High Blood Pressure in an Adolescent): prose edited (+40 chars)
  - copd (COPD: Which Interventions Improve Survival): prose edited (+176 chars)
  - asthma-copd (Asthma vs. COPD): prose edited (+74 chars)
  - cough (Chronic Cough): prose edited (+154 chars)
  - pneumoconiosis (Occupational Lung Disease): prose edited (+42 chars)
  - rhinitis (Allergic Rhinitis): prose edited (+46 chars)
  - sinopulm-structural (Recurrent Sinopulmonary Infection): prose edited (+81 chars)
  - hypoxemia-mech (Mechanisms of Hypoxemia): prose edited (-52 chars)
  - abpa (When Antibiotics Fail in a Structural Lung): prose edited (-470 chars)
  - scd-dyspnea (Chronic Dyspnea in Sickle Cell Disease): prose edited (-519 chars)
  - airway (Pediatric Airway & Noisy Breathing): prose edited (-14 chars)
  - mycoplasma (Pediatric Community-Acquired Pneumonia): prose edited (+22 chars)
  - uri (Pediatric Upper Respiratory Infection): prose edited (+73 chars)
  - asthma (Asthma: Severity Classification): prose edited (+441 chars)
  - bpd (Bronchopulmonary Dysplasia): prose edited (+404 chars)
  - bs-nrd (Neonatal Respiratory Distress): prose edited (-90 chars)
  - cholestasis (Cholestasis & the LFT Patterns): prose edited (-13 chars)
  - neonatal-jaundice (Neonatal Jaundice): prose edited (-28 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): prose edited (-28 chars)
  - pyelo (Pyelonephritis: Route & Disposition): prose edited (+132 chars)
  - bph (BPH & Acute Urinary Retention): prose edited (+327 chars)
  - nephropathy (Diabetic Nephropathy Screening): prose edited (+184 chars)
  - hematuria (Hematuria): prose edited (+172 chars)
  - scrotum (Acute Scrotum & Scrotal Mass): prose edited (+377 chars)
  - hypercalcemia (Hypercalcemia Workup): prose edited (+152 chars)
  - vur (Vesicoureteral Reflux): prose edited (+62 chars)
  - peds-uti-recurrent (Recurrent Urinary Infection in a Child): prose edited (-580 chars)
  - enuresis (Nocturnal Enuresis): prose edited (+74 chars)
  - polyuria (Polyuria: Water or Solute): prose edited (-169 chars)
  - peds-aki (NSAID Prerenal AKI in a Child): prose edited (+621 chars)
  - nephrotic-child (Nephrotic Syndrome in a Child): prose edited (-111 chars)
  - bs-puv (Posterior Urethral Valves and Potter Sequence): prose edited (+204 chars)
  - bs-pyelo-organism (Pyelonephritis: Naming the Organism): prose edited (+78 chars)
  - bs-incontinence (Incontinence & the Postvoid Residual): prose edited (+153 chars)
  - bs-enuresis (Primary Monosymptomatic Enuresis: Management): prose edited (+121 chars)
  - bs-nephritic (Acute Nephritic Syndrome in a Child): prose edited (+388 chars)
  - bs-abdominal-mass (Abdominal Mass in a Young Child): prose edited (+25 chars)
  - bs-isolated-proteinuria (Incidental Proteinuria in a Well Child): prose edited (+3 chars)
  - aq-puffy-eyes (Child with Puffy Eyes): prose edited (+78 chars)
  - thyroid (Thyroid Mimics & Discriminators): prose edited (+358 chars)
  - levo (Levothyroxine Titration): prose edited (-208 chars)
  - gynecomastia (Gynecomastia vs. Male Breast Cancer): prose edited (+62 chars)
  - prolactin (Hyperprolactinemia): prose edited (+232 chars)
  - osteoporosis (Osteoporosis Screening): prose edited (+258 chars)
  - preg-thyroid (Levothyroxine in Pregnancy): prose edited (+231 chars)
  - congenital-hypothyroid (Congenital Hypothyroidism): prose edited (+63 chars)
  - tumor-syndromes (Inherited Tumor Syndromes): prose edited (+196 chars)
  - precocious-puberty (Precocious Puberty): prose edited (-824 chars)
  - homocystinuria (Marfanoid Habitus: Homocystinuria): prose edited (+17 chars)
  - bs-dexa-highrisk (DEXA: When Screening Starts Early): prose edited (+351 chars)
  - bs-dm-bundle (Diabetes: the Annual Care Bundle): prose edited (+203 chars)
  - bs-short-stature (Short Stature and Growth Velocity): prose edited (+189 chars)
  - anemia-thrombocytopenia (Anemia with Thrombocytopenia): prose edited (+116 chars)
  - drug-hemolysis (Drug-Induced Immune Hemolysis): prose edited (-371 chars)
  - dipstick-mismatch (Hemoglobinuria: the Dipstick-Microscopy Mismatch): prose edited (+4 chars)
  - microcytic-anemia (Microcytic Anemia: Iron First): prose edited (-52 chars)
  - factor-inhibitor (Hemophilia A Inhibitor): prose edited (+322 chars)
  - transfusion (Transfusion Reactions): prose edited (-246 chars)
  - bs-leukemia (Pediatric Acute Lymphoblastic Leukemia): prose edited (+144 chars)
  - bs-spherocytosis (Hereditary Spherocytosis): prose edited (+332 chars)
  - bs-sickle-trait (Sickle Cell Trait versus Disease): prose edited (-220 chars)
  - aq-bruising (Bruising and Purpura in a Child): prose edited (+10 chars)
  - tb (Tuberculosis): prose edited (+262 chars)
  - meningitis (Bacterial Meningitis): prose edited (+405 chars)
  - hiv-vax (Vaccines in HIV): prose edited (+202 chars)
  - dtap (DTaP: Contraindication vs. Precaution): prose edited (-36 chars)
  - cervicitis (Acute Cervicitis): prose edited (+197 chars)
  - ig-panel (The Immunoglobulin Panel): prose edited (+27 chars)
  - rmsf (Tick-Borne Fever and Rash): prose edited (-146 chars)
  - lymphadenitis (Enlarged Lymph Nodes: Reading the Pattern): prose edited (-191 chars)
  - herpangina (Oral Vesicles in a Child): prose edited (-185 chars)
  - cgd (Recurrent Abscesses and Granulomas): prose edited (-69 chars)
  - bs-pta (Peritonsillar Abscess and the Deep Neck Spaces): prose edited (-86 chars)
  - bs-torch (Congenital CMV and the TORCH Discriminations): prose edited (-328 chars)
  - bs-neonatal-sepsis (Neonatal Sepsis and Its Mimics): prose edited (+58 chars)
  - bs-fever-rash-arthralgia (Fever, Rash and Joint Pain in a Child or Adolescent): prose edited (+239 chars)
  - bs-exanthems (Exanthems in a Child): prose edited (+36 chars)
  - bs-anaphylaxis (Anaphylaxis and Its Mimics): prose edited (+182 chars)
  - bs-isolation (Isolation Precautions): prose edited (+440 chars)
  - bs-foodborne (Foodborne Diarrhea: Source and Organism): prose edited (-13 chars)
  - bs-febrile-infant (The Febrile Infant — Finding the Source): prose edited (-57 chars)
  - aq-infant-fever (Fever in an Infant): prose edited (+159 chars)
  - hearing (Hearing Loss & Otosclerosis): prose edited (+159 chars)
  - redeye (The Red Eye): prose edited (+23 chars)
  - cluster (Headache Types & Cluster Headache): prose edited (-13 chars)
  - sellar-mass (Sellar and Suprasellar Masses): prose edited (-104 chars)
  - peds-headache-imaging (Headache in a Child: What Earns Imaging): prose edited (-13 chars)
  - cholesteatoma (Cholesteatoma and Chronic Ear Drainage): prose edited (-869 chars)
  - febrile-seizure (Seizure with Fever in a Child): prose edited (-367 chars)
  - cerebral-palsy (Cerebral Palsy and the MRI Pattern): prose edited (-567 chars)
  - abrs-complications (Sinusitis with Intracranial Extension): prose edited (+102 chars)
  - vpshunt (VP Shunt Complications): prose edited (+237 chars)
  - retinitis-pigmentosa (Night Blindness): prose edited (-434 chars)
  - tics (Tics in a School-Age Child): prose edited (+117 chars)
  - bs-tethered (Tethered Cord and Closed Spinal Dysraphism): prose edited (-136 chars)
  - bs-reye (Cerebral Edema in a Child — Reye Syndrome): prose edited (-152 chars)
  - bs-peds-stroke (Stroke in a Child or Adolescent): prose edited (-27 chars)
  - bs-imprinting (Angelman Syndrome and Its Genetic Look-Alikes): prose edited (+23 chars)
  - bs-posterior-fossa (Posterior Fossa Localization): prose edited (-107 chars)
  - aq-child-headache (Headache in a School-Age Child): prose edited (+134 chars)
  - psoriasis (Scaly Rash & Psoriasis): prose edited (+191 chars)
  - cellulitis (Cellulitis & the Depth Ladder): prose edited (+121 chars)
  - footulcer (Diabetic Foot Ulcer): prose edited (+110 chars)
  - eczemaherp (Atopic Dermatitis Complications): prose edited (+368 chars)
  - peds-alopecia (Patchy Hair Loss in a Child): prose edited (-229 chars)
  - neonatal-rash (Benign Neonatal Rashes): prose edited (+201 chars)
  - diaper-dermatitis (Diaper Dermatitis): prose edited (-213 chars)
  - bs-scabies (Scabies): prose edited (+22 chars)
  - preg-vax (Vaccines & Timing in Pregnancy): prose edited (+66 chars)
  - cervical (Cervical Cancer Screening): prose edited (+539 chars)
  - pmb (Postmenopausal Bleeding): prose edited (+312 chars)
  - ectopic (Ectopic Pregnancy): prose edited (+146 chars)
  - hpv (HPV Vaccination & Series Rules): prose edited (+39 chars)
  - adolescent-aub (Adolescent Abnormal Uterine Bleeding): prose edited (-32 chars)
  - contraception (Contraception & DMPA): prose edited (+245 chars)
  - fibroids (Uterine Fibroids): prose edited (-141 chars)
  - teratogens (Teratogenic Exposures): prose edited (-146 chars)
  - primary-amenorrhea (Primary Amenorrhea): prose edited (-164 chars)
  - bs-cervical-gate (Cervical Screening: the Age-21 Floor): prose edited (+235 chars)
  - bs-tdap-preg (Tdap in Pregnancy at 10 Weeks): prose edited (-178 chars)
  - bs-genital-ulcer (Genital Ulcer: Painless or Painful): prose edited (+14 chars)
  - bs-pid (Pelvic Inflammatory Disease): prose edited (+73 chars)
  - smoking (Ranking Preventive Interventions): prose edited (+130 chars)
  - lipid-screen (Lipid Screening & Vaccine Eligibility by Condition): prose edited (+262 chars)
  - preop (Preoperative Thresholds): prose edited (+166 chars)
  - elder (Elder Abuse & Mandated Reporting): prose edited (+58 chars)
  - vegan (The Vegan Diet): prose edited (-9 chars)
  - bs-adolescent-confid (Adolescent Confidentiality): prose edited (-88 chars)
  - bs-adolescent-vax (Adolescent Immunization and the Age Platform): prose edited (+163 chars)
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 207 briefs, 2014 items, 4 scripts, 31 checks, base HEAD | allowlisted 12 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 207 | bankwraps 207 | mcq 2014 (axCheck 2014, reveal-only 0) | malformed 0 | crit gridded 123/124 | vignette gridded 129/129 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (42269 source shingles; page 0.031%)
```

## 2026-09-24 s32: Mobile sidebar replaces the bottom sheet; full-text search on phone and desktop; Board-style only toggle replaces NBME-tested

```
Page: 207 briefs, 2014 items -> 207 briefs, 2014 items
Other page changes (nav, headers, scripts): +21852 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 207 briefs, 2014 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 207 | bankwraps 207 | mcq 2014 (axCheck 2014, reveal-only 0) | malformed 0 | crit gridded 123/124 | vignette gridded 129/129 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (42269 source shingles; page 0.031%)
```

## 2026-09-24 s31: NBME Peds batch: 27 questions linked; 6 new briefs, 12 backfills, NBME wording guide

```
Page: 201 briefs, 1942 items -> 207 briefs, 2014 items
Briefs added (6):
  - bs-puncture-osteomyelitis: Foot Puncture Wound Infection (5 items)
  - bs-acute-myositis: Benign Acute Childhood Myositis (8 items)
  - bs-adolescent-bp: Confirming High Blood Pressure in an Adolescent (6 items)
  - bs-isolated-proteinuria: Incidental Proteinuria in a Well Child (7 items)
  - bs-imprinting: Angelman Syndrome and Its Genetic Look-Alikes (7 items)
  - bs-genital-ulcer: Genital Ulcer: Painless or Painful (8 items)
Briefs changed (26):
  - limp (The Limping Child — Master Table): 2 items added (q_b599f8e62f2070a52991, q_11abb36f6ad6ea3085a4); prose edited (+2317 chars)
  - growing-pains (Benign Limb Pain in a Child): prose edited (+110 chars)
  - growth (Growth & Developmental Milestones): 3 items added (q_907cd6543effc4c0dec6, q_d0c9d6f19c78dd1fed12, q_eca33fcf91f5726143e5); prose edited (+2008 chars)
  - newborn-hormone (Maternal Hormone Effects in the Newborn): prose edited (+77 chars)
  - aneuploidy (Aneuploidy: Reading the Newborn): prose edited (+142 chars)
  - cyanotic-chd (Cyanotic Congenital Heart Disease): 2 items added (q_1dafa1911a5a64278be2, q_dc06038895874469075d); prose edited (+1628 chars)
  - kawasaki (Kawasaki Disease): 3 items added (q_5c5ebd26ef5fe11337d5, q_495dfa71396b7036d94a, q_e96fadc94a8327131c75); prose edited (+2035 chars)
  - arf (Acute Rheumatic Fever): attrs set (q_163add7fdad553c2a5e2 data-nbme); prose edited (+284 chars)
  - neonatal-jaundice (Neonatal Jaundice): 2 items added (q_68047f53bb547e1428b5, q_ea850ed3646b8e8e5167); prose edited (+1701 chars)
  - bs-umbilical (Umbilical Findings in a Newborn): attrs set (q_7e472e5bd7e09a357f4d data-nbme); prose edited (+278 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): 3 items added (q_44a4c5430977368dd3fc, q_187ede1b74536a0c7f62, q_ca7906ad3ce2003c2e2e); prose edited (+1423 chars)
  - nephrotic-child (Nephrotic Syndrome in a Child): prose edited (+148 chars)
  - bs-nephritic (Acute Nephritic Syndrome in a Child): attrs set (q_aeb588e544ebeb4b9c39 data-nbme); prose edited (+389 chars)
  - bs-abdominal-mass (Abdominal Mass in a Young Child): 3 items added (q_d9b8dd343b4ca836c41d, q_aacccbc0cf7974df049d, q_9ba68702a02ebc4483c1); prose edited (+1565 chars)
  - tumor-syndromes (Inherited Tumor Syndromes): 3 items added (q_791ab466c5d3371ac2d4, q_a73027aea794cb20e60e, q_07869c908680b86b0b69); prose edited (+2388 chars)
  - bs-leukemia (Pediatric Acute Lymphoblastic Leukemia): attrs set (q_d5a219c1127f50cba341 data-nbme); prose edited (+296 chars)
  - cervicitis (Acute Cervicitis): 2 items added (q_424c322e1a1fb44f35a6, q_6037409dfb4feb0f247f); prose edited (+2056 chars)
  - ig-panel (The Immunoglobulin Panel): 3 items added (q_6f1f0484f7cc597f3a69, q_ef6b8e7ad853646f5cd4, q_4319327c01c3ba7a9234); prose edited (+2702 chars)
  - rmsf (Tick-Borne Fever and Rash): prose edited (+243 chars)
  - lymphadenitis (Enlarged Lymph Nodes: Reading the Pattern): attrs set (q_bbe63e88a23044cd7f3a data-nbme); prose edited (+260 chars)
  - bs-torch (Congenital CMV and the TORCH Discriminations): 3 items added (q_f04e1e07cd1dacf1c640, q_92c751f85de71a0bcb69, q_a3ec9f313a821c1030d1); prose edited (+2501 chars)
  - bs-fever-rash-arthralgia (Fever, Rash and Joint Pain in a Child or Adolescent): prose edited (+103 chars)
  - redeye (The Red Eye): attrs set (q_bfc2adf60a295d1a841a data-nbme); prose edited (+288 chars)
  - cerebral-palsy (Cerebral Palsy and the MRI Pattern): prose edited (+161 chars)
  - neonatal-rash (Benign Neonatal Rashes): attrs set (q_ee07b7cec8875310382c data-nbme); prose edited (+242 chars)
  - diaper-dermatitis (Diaper Dermatitis): 2 items added (q_02665e6eb263aaa1aecd, q_ccd48da198c8448a6e8f); prose edited (+1986 chars)
Other page changes (nav, headers, scripts): +3593 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 207 briefs, 2014 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 207 | bankwraps 207 | mcq 2014 (axCheck 2014, reveal-only 0) | malformed 0 | crit gridded 123/124 | vignette gridded 129/129 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (42269 source shingles; page 0.033%)
```

## 2026-09-24 s30: GI plain-voice round 2: shorter sentences, acronyms written out, claim-mapped for no drift

```
Page: 201 briefs, 1942 items -> 201 briefs, 1942 items
Briefs changed (21):
  - liver-preg (Liver Disease in Pregnancy): prose edited (+246 chars)
  - masld (MASLD / Metabolic Fatty Liver): prose edited (+149 chars)
  - cholestasis (Cholestasis & the LFT Patterns): prose edited (+209 chars)
  - zenker (Zenker Diverticulum): prose edited (+17 chars)
  - infant-stool (Infant Stool Complaints: Dyschezia, FPIAP & Secondary Lactase Deficiency): prose edited (+312 chars)
  - fap (Familial Adenomatous Polyposis): prose edited (+233 chars)
  - peutz-jeghers (Peutz-Jeghers Syndrome): prose edited (+74 chars)
  - feeding-refusal (Toddler Food Refusal): prose edited (-56 chars)
  - rlq-pain (Right Lower Quadrant Pain): prose edited (-73 chars)
  - peds-constipation (Constipation in a Child): prose edited (-194 chars)
  - cyclic-vomiting (Cyclic Vomiting Syndrome): prose edited (+3 chars)
  - neonatal-jaundice (Neonatal Jaundice): prose edited (+204 chars)
  - neonatal-bowel (The Distended Abdomen in a Newborn or Infant): prose edited (+366 chars)
  - occult-gi-bleed (Occult GI Bleeding in a Child): prose edited (+172 chars)
  - bs-galactosemia (The Sick Jaundiced Neonate with a Positive Screen): prose edited (+249 chars)
  - bs-impaction (Fecal Impaction & Overflow Diarrhea): prose edited (+31 chars)
  - bs-tef (Tracheoesophageal Fistula with Esophageal Atresia): prose edited (+192 chars)
  - bs-umbilical (Umbilical Findings in a Newborn): prose edited (+109 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): prose edited (+824 chars)
  - bs-water-soluble-vitamins (Water-Soluble Vitamin Deficiency): prose edited (+233 chars)
  - bs-wilson (Wilson Disease: Copper in the Liver, Brain and Eye): prose edited (+22 chars)
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 201 briefs, 1942 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 201 | bankwraps 201 | mcq 1942 (axCheck 1942, reveal-only 0) | malformed 0 | crit gridded 120/121 | vignette gridded 123/123 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (27616 source shingles; page 0.033%)
```

## 2026-09-24 s29: Badges follow NBME first; subtitles drop provenance; GI plain-voice pass (sample)

```
Page: 201 briefs, 1942 items -> 201 briefs, 1942 items
Briefs changed (99):
  - myositis-ossificans (The Post-Traumatic Limb Mass): prose edited (-17 chars)
  - growing-pains (Benign Limb Pain in a Child): prose edited (-17 chars)
  - bone-tumors (Bone Tumors: Location, Film, Course): prose edited (-16 chars)
  - bs-torticollis (Congenital Muscular Torticollis and Plagiocephaly): prose edited (-9 chars)
  - bs-brachial-plexus (Brachial Plexus Injury at Birth): prose edited (-9 chars)
  - shoulder-rom (Shoulder Pain: the Range-of-Motion Rule): prose edited (-16 chars)
  - neonatal-maternal-labs (Maternal Carryover in Newborn Labs): prose edited (-24 chars)
  - newborn-hormone (Maternal Hormone Effects in the Newborn): prose edited (-24 chars)
  - aneuploidy (Aneuploidy: Reading the Newborn): prose edited (-16 chars)
  - malform-syndromes (Multiple Anomalies in a Newborn): prose edited (-16 chars)
  - bs-learning (Specific Learning Disorder): prose edited (-9 chars)
  - bs-nat-fracture (Suspected Child Abuse: Fractures and the Next Step): prose edited (-16 chars)
  - bs-shock (Shock in Children): prose edited (-10 chars)
  - bs-infant-feeding (Infant Feeding at Six Months): prose edited (-10 chars)
  - bs-tanner (Sexual Maturity Rating): prose edited (-10 chars)
  - bs-ftt (Faltering Weight): prose edited (-10 chars)
  - bs-preterm-followup (Prematurity Follow-Up and Corrected Age): prose edited (-10 chars)
  - aq-infant-hypotonia (Hypotonia in an Infant): prose edited (-55 chars)
  - newborn-cyanosis (Cyanosis in the Newborn): prose edited (-24 chars)
  - myocarditis (New Heart Failure in a Child): prose edited (-16 chars)
  - del22q11 (22q11.2 Deletion Syndrome): prose edited (-16 chars)
  - bs-murmur-map (Murmur Man and Post-ToF Pulmonic Regurgitation): prose edited (-9 chars)
  - bs-shunt-timing (Congenital Shunts and the Transitional Clock): prose edited (-10 chars)
  - sinopulm-structural (Recurrent Sinopulmonary Infection): prose edited (-24 chars)
  - hypoxemia-mech (Mechanisms of Hypoxemia): prose edited (-24 chars)
  - abpa (When Antibiotics Fail in a Structural Lung): prose edited (-24 chars)
  - scd-dyspnea (Chronic Dyspnea in Sickle Cell Disease): prose edited (-24 chars)
  - bs-nrd (Neonatal Respiratory Distress): prose edited (-10 chars)
  - liver-preg (Liver Disease in Pregnancy): prose edited (-82 chars)
  - masld (MASLD / Metabolic Fatty Liver): prose edited (+2 chars)
  - cholestasis (Cholestasis & the LFT Patterns): prose edited (-55 chars)
  - zenker (Zenker Diverticulum): prose edited (-483 chars)
  - infant-stool (Infant Stool Complaints: Dyschezia, FPIAP & Secondary Lactase Deficiency): prose edited (-249 chars)
  - fap (Familial Adenomatous Polyposis): prose edited (-569 chars)
  - peutz-jeghers (Peutz-Jeghers Syndrome): prose edited (-424 chars)
  - feeding-refusal (Toddler Food Refusal): prose edited (-801 chars)
  - rlq-pain (Right Lower Quadrant Pain): prose edited (-746 chars)
  - peds-constipation (Constipation in a Child): prose edited (-1054 chars)
  - cyclic-vomiting (Cyclic Vomiting Syndrome): prose edited (-198 chars)
  - neonatal-jaundice (Neonatal Jaundice): prose edited (-293 chars)
  - neonatal-bowel (The Distended Abdomen in a Newborn or Infant): prose edited (-96 chars)
  - occult-gi-bleed (Occult GI Bleeding in a Child): prose edited (-227 chars)
  - bs-galactosemia (The Sick Jaundiced Neonate with a Positive Screen): prose edited (-345 chars)
  - bs-impaction (Fecal Impaction & Overflow Diarrhea): prose edited (-217 chars)
  - bs-tef (Tracheoesophageal Fistula with Esophageal Atresia): prose edited (-396 chars)
  - bs-umbilical (Umbilical Findings in a Newborn): prose edited (-70 chars)
  - bs-fat-soluble-vitamins (Fat-Soluble Vitamin Deficiency and Toxicity): prose edited (+0 chars)
  - bs-water-soluble-vitamins (Water-Soluble Vitamin Deficiency): prose edited (-8 chars)
  - bs-wilson (Wilson Disease: Copper in the Liver, Brain and Eye): prose edited (-14 chars)
  - vur (Vesicoureteral Reflux): prose edited (-24 chars)
  - peds-uti-recurrent (Recurrent Urinary Infection in a Child): prose edited (-24 chars)
  - polyuria (Polyuria: Water or Solute): prose edited (-16 chars)
  - nephrotic-child (Nephrotic Syndrome in a Child): prose edited (-24 chars)
  - bs-puv (Posterior Urethral Valves and Potter Sequence): prose edited (-10 chars)
  - bs-nephritic (Acute Nephritic Syndrome in a Child): prose edited (-16 chars)
  - bs-abdominal-mass (Abdominal Mass in a Young Child): prose edited (-16 chars)
  - aq-puffy-eyes (Child with Puffy Eyes): prose edited (-55 chars)
  - congenital-hypothyroid (Congenital Hypothyroidism): prose edited (-24 chars)
  - tumor-syndromes (Inherited Tumor Syndromes): prose edited (-24 chars)
  - precocious-puberty (Precocious Puberty): prose edited (-17 chars)
  - bs-short-stature (Short Stature and Growth Velocity): prose edited (-16 chars)
  - anemia-thrombocytopenia (Anemia with Thrombocytopenia): prose edited (-24 chars)
  - drug-hemolysis (Drug-Induced Immune Hemolysis): prose edited (-24 chars)
  - transfusion (Transfusion Reactions): prose edited (-24 chars)
  - bs-spherocytosis (Hereditary Spherocytosis): prose edited (-10 chars)
  - bs-sickle-trait (Sickle Cell Trait versus Disease): prose edited (-9 chars)
  - aq-bruising (Bruising and Purpura in a Child): prose edited (-55 chars)
  - ig-panel (The Immunoglobulin Panel): prose edited (-24 chars)
  - rmsf (Tick-Borne Fever and Rash): prose edited (-16 chars)
  - lymphadenitis (Enlarged Lymph Nodes: Reading the Pattern): prose edited (-16 chars)
  - herpangina (Oral Vesicles in a Child): prose edited (-16 chars)
  - cgd (Recurrent Abscesses and Granulomas): prose edited (-24 chars)
  - bs-pta (Peritonsillar Abscess and the Deep Neck Spaces): prose edited (-9 chars)
  - bs-torch (Congenital CMV and the TORCH Discriminations): prose edited (-9 chars)
  - bs-neonatal-sepsis (Neonatal Sepsis and Its Mimics): prose edited (-24 chars)
  - bs-fever-rash-arthralgia (Fever, Rash and Joint Pain in a Child or Adolescent): prose edited (-9 chars)
  - bs-exanthems (Exanthems in a Child): prose edited (-9 chars)
  - bs-anaphylaxis (Anaphylaxis and Its Mimics): prose edited (-16 chars)
  - bs-isolation (Isolation Precautions): prose edited (-16 chars)
  - bs-foodborne (Foodborne Diarrhea: Source and Organism): prose edited (-16 chars)
  - bs-febrile-infant (The Febrile Infant — Finding the Source): prose edited (-10 chars)
  - aq-infant-fever (Fever in an Infant): prose edited (-55 chars)
  - sellar-mass (Sellar and Suprasellar Masses): prose edited (-24 chars)
  - peds-headache-imaging (Headache in a Child: What Earns Imaging): prose edited (-24 chars)
  - cholesteatoma (Cholesteatoma and Chronic Ear Drainage): prose edited (-24 chars)
  - febrile-seizure (Seizure with Fever in a Child): prose edited (-24 chars)
  - cerebral-palsy (Cerebral Palsy and the MRI Pattern): prose edited (-24 chars)
  - retinitis-pigmentosa (Night Blindness): prose edited (-16 chars)
  - tics (Tics in a School-Age Child): prose edited (-16 chars)
  - bs-tethered (Tethered Cord and Closed Spinal Dysraphism): prose edited (-9 chars)
  - bs-peds-stroke (Stroke in a Child or Adolescent): prose edited (-16 chars)
  - bs-posterior-fossa (Posterior Fossa Localization): prose edited (-10 chars)
  - aq-child-headache (Headache in a School-Age Child): prose edited (-54 chars)
  - peds-alopecia (Patchy Hair Loss in a Child): prose edited (-24 chars)
  - diaper-dermatitis (Diaper Dermatitis): prose edited (-16 chars)
  - teratogens (Teratogenic Exposures): prose edited (-24 chars)
  - primary-amenorrhea (Primary Amenorrhea): prose edited (-24 chars)
  - bs-pid (Pelvic Inflammatory Disease): prose edited (-10 chars)
  - bs-adolescent-vax (Adolescent Immunization and the Age Platform): prose edited (-10 chars)
Other page changes (nav, headers, scripts): +1108 chars
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 201 briefs, 1942 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 201 | bankwraps 201 | mcq 1942 (axCheck 1942, reveal-only 0) | malformed 0 | crit gridded 120/121 | vignette gridded 123/123 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (27616 source shingles; page 0.033%)
```

## 2026-09-24 s28d: Workspace in Step2Haki: ship updates the site copy, writes a changelog, pushes with a token

```
Page: 201 briefs, 1942 items -> 201 briefs, 1942 items
Page content unchanged.
Site: discriminator-briefs-site/index.html updated (Vercel deploys on push)
Checks:
  gate: PASS 201 briefs, 1942 items, 4 scripts, 31 checks, base HEAD | allowlisted 16 | 0 failure(s)
  render: PASS jsdom 24.1.3 | briefs 201 | bankwraps 201 | mcq 1942 (axCheck 1942, reveal-only 0) | malformed 0 | crit gridded 120/121 | vignette gridded 123/123 | vignette masks 0 | dead anchors 0 | js errors 0 | allowlisted 1
  vendor: clean (27616 source shingles; page 0.033%)
```

