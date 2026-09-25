# s34 summary (NBME Pediatrics CMS, 3 questions: 2 incorrect, 1 correct)

Sorts: 3 new angle, 0 covered, 0 conflict, 0 new. Build order: 05_cleanup (factor-inhibitor: removed the leftover "47-minute doubt loop" miss-history sentence from s33), 10_bf_* (3 backfills), 90_nbme_links (data-nbme on the 3 new NBME items). No 00_links file (nothing was covered). The item marked * carries data-nbme.

| Q | nbme_id | sort | brief | added | item ids |
|---|---|---|---|---|---|
| 1 | peds-cms-8e3e76 | new angle | teratogens | FAS without an exposure history (all four 2016 revised IOM criteria: facial, growth, head size or brain, neurobehavioral); short versus upslanting fissures; framing block; 5 traplines; 1 item. | q_25742c68c19ec216b8d0* |
| 2 | peds-cms-acdeb0 | new angle | bs-fat-soluble-vitamins | Rickets lab pattern (alkaline phosphatase and PTH up, phosphate down, calcium low or normal; osteoblast source; PTH acts on the gut through 1,25-dihydroxyvitamin D); framing block; 4 traplines; 2 items. | q_f1da4cfcf0b5965ee660* q_a6f735a57b23ad49910f |
| 3 | peds-cms-b095ba | new angle | aq-bruising | Differential cell now names destruction; "Bleeding by mechanism" block (destruction, production, function; normal PT and aPTT against factor deficiency and DIC); framing block; 4 traplines (abuse line: bruise color cannot date a bruise); 2 items. | q_ee5e56588e265abea6ad* q_179857279bfa2f2d0870 |

NBME explanation errors not transferred: FAS as "the leading cause" of intellectual disability; Down syndrome fissures as "downturned"; magnesium as irrelevant to PTH and vitamin D physiology; PTH directly increasing intestinal calcium absorption; osteoclasts releasing alkaline phosphatase; prolonged bleeding time as a practical ITP test.

Facts checked: FAS diagnosis without confirmed exposure, 2 of 3 facial features, growth and head size at or below the 10th percentile (Hoyme 2016, as summarized in AAFP 2017, aafp.org/afp/2017/1015/p515). Alkaline phosphatase is an osteoblast product that rises early in nutritional rickets, with low calcium and phosphate and high PTH (PMC9931734). ITP: antibody-coated platelets cleared by splenic macrophages, plus impaired megakaryocyte production; count under 100,000 (PMC3410635). Bruise age cannot be judged from color (Maguire 2005 systematic review, PubMed 15665179). Bleeding time largely abandoned (LA AAP bleeding evaluation page).

Coverage: 3 rows in repair/nbme/coverage.csv and 3 in repair/nbme/misses.csv (miss_cause unknown for the two misses; nothing reported).

Checks: each edits file passed tools/verify_edits.py (90_ checked in the full build, since its targets are created by 10_). Full build into a scratch copy: build s34 OK 5 files, 16 ops; gate PASS (207 briefs, 2019 items, base HEAD); render PASS (malformed 0, js errors 0); vendor scan 0 flagged, page shares 0 shingles with s34_questions.md (page total 0.031%, longest run 18 words, both unchanged). Not committed, not shipped.
