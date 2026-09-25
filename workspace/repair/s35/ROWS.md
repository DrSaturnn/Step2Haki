# s35 rows for coverage.csv and misses.csv (assembler input)

From repair/s35/sort.md and repair/sources/s35_questions.md. Form: Pediatrics CMS (form number not given). same_as: none for all 12. miss_cause: unknown for every incorrect item (nothing reported). item_id is the item that should carry data-nbme; "TBD" means the backfill or new-brief file that creates it sets it (take the id from that file's verify/build output). data-nbme set_attr ops for all 12 go in the 90 file.

| Q | nbme_id | fingerprint | sort | brief | item_id | bp_system | task | result | time |
|---|---|---|---|---|---|---|---|---|---|
| 1 | peds-cms-d90531 | d90531cd5a | new angle | precocious-puberty | TBD | endo | dx | incorrect | 0:29 |
| 2 | peds-cms-723033 | 7230339994 | new angle | bs-puv | TBD | renal newborn | dx | correct | 1:25 |
| 3 | peds-cms-ce7f06 | ce7f06970e | new | bs-infant-vax (new brief, repair/s35/15_q3.json) | q_5e35f1b7a625a2f602f5 | gen | prevention | incorrect | 1:53 |
| 4 | peds-cms-0354fa | 0354fa6e7d | new | bs-distal-rta (proposed) | TBD | renal | dx | incorrect | 2:52 |
| 5 | peds-cms-c4694e | c4694e76b7 | covered | ped-murmur | q_fb94648142ed51749518 | cv | dx | correct | 1:28 |
| 6 | peds-cms-3d1862 | 3d1862ca4b | new angle | scfe | TBD | msk | mgmt | incorrect | 0:35 |
| 7 | peds-cms-0efcba | 0efcba16c3 | new angle | mycoplasma | TBD (carrier item) | resp | dx | correct | 0:52 |
| 8 | peds-cms-6821fe | 6821fe82bf | new angle | bs-abdominal-mass | TBD | renal multi | dx | incorrect | 0:27 |
| 9 | peds-cms-7a44ef | 7a44ef1140 | new | bs-eyelid-lump (proposed) | TBD | neuro | mgmt | incorrect | 0:41 |
| 10 | peds-cms-44f3d3 | 44f3d30e35 | new angle | asthma-copd | TBD | resp | dx | incorrect | 0:17 |
| 11 | peds-cms-252cd2 | 252cd2ab65 | covered | cgd | q_1f7b49f7314459b8b98f | immune | mechanism | incorrect | 0:46 |
| 12 | peds-cms-9fb189 | 9fb189ce6c | new angle | bs-exanthems | TBD | multi skin | prevention | incorrect | 0:10 |

Notes
- Q3: sort.md said "new angle" under bs-adolescent-vax; no brief title covers the infant schedule (dtap is contraindications only; bs-adolescent-vax is adolescent-titled), so it became a new brief. Record sort as new. The id above is deterministic (tools/idgen.py on the item's key and stem) and was confirmed by applying 15_q3.json to a scratch copy.
- Q5 and Q11: link only; their "How NBME framed it" lines are in repair/s35/00_links.json. The data-nbme set_attr ops (q_fb94648142ed51749518 = peds-cms-c4694e, q_1f7b49f7314459b8b98f = peds-cms-252cd2) go in the 90 file.
- Coverage note column suggestions: Q3 "Infant schedule; rotavirus age limits; NBME explanation dates zoster to 60 (now 50)". Q5 "Explanation describes valvar PS; stem is physiologic PPS". Q11 "Maternal uncle as X-linked cue; key written as a mechanism".
