"""Advisory never-keyed report using the shared structural parser.

This is a diagnostic comparison, not a content-deletion rule.  Its historical
policy is intentionally fixed at the 59 aliases and three synonym groups used
by the supplied report so that the frozen input remains comparable (21
candidates, versus 27 from the old first-bold extraction).
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import axlib


ABBR = {
    "vsd": "ventricular septal defect", "asd": "atrial septal defect", "pda": "patent ductus arteriosus",
    "tof": "tetralogy of fallot", "tga": "transposition of the great arteries", "chd": "congenital heart disease",
    "avsd": "atrioventricular septal defect", "hcm": "hypertrophic cardiomyopathy", "pps": "peripheral pulmonic stenosis",
    "uti": "urinary tract infection", "vur": "vesicoureteral reflux", "puv": "posterior urethral valves",
    "aom": "acute otitis media", "ome": "otitis media with effusion", "urti": "upper respiratory infection",
    "uri": "upper respiratory infection", "cf": "cystic fibrosis", "gerd": "gastroesophageal reflux disease",
    "jia": "juvenile idiopathic arthritis", "sjia": "systemic juvenile idiopathic arthritis",
    "scfe": "slipped capital femoral epiphysis", "lcp": "legg calve perthes disease", "ddh": "developmental dysplasia of the hip",
    "arf": "acute rheumatic fever", "rmsf": "rocky mountain spotted fever", "ivh": "intraventricular hemorrhage",
    "nec": "necrotizing enterocolitis", "rds": "respiratory distress syndrome", "bpd": "bronchopulmonary dysplasia",
    "tef": "tracheoesophageal fistula", "cah": "congenital adrenal hyperplasia", "pcos": "polycystic ovary syndrome",
    "scid": "severe combined immunodeficiency", "cvid": "common variable immunodeficiency", "cgd": "chronic granulomatous disease",
    "itp": "immune thrombocytopenia", "tacо": "taco", "ida": "iron deficiency anemia", "aihа": "autoimmune hemolytic anemia",
    "e coli": "escherichia coli", "gbs": "group b streptococcus", "gas": "group a streptococcus",
    "mri": "magnetic resonance imaging", "ct": "computed tomography", "us": "ultrasound", "cbc": "complete blood count",
    "iih": "idiopathic intracranial hypertension", "nf1": "neurofibromatosis type 1", "ts": "tuberous sclerosis",
    "dmd": "duchenne muscular dystrophy", "sma": "spinal muscular atrophy", "cp": "cerebral palsy",
    "ivig": "intravenous immunoglobulin", "nsaid": "nonsteroidal anti inflammatory drug", "ppi": "proton pump inhibitor",
    "ocp": "combined oral contraceptive", "iud": "intrauterine device", "hsv": "herpes simplex virus", "cmv": "cytomegalovirus",
}

SYN = [
    ({"observation", "observation alone", "watchful waiting", "observation and reassurance",
      "reassurance and observation", "expectant management", "continued observation",
      "supportive care and observation"}, "OBSERVE"),
    ({"reassurance", "reassurance alone", "reassurance and follow up", "parental reassurance"}, "REASSURE"),
    ({"renal ultrasound", "renal and bladder ultrasound", "ultrasound of the kidneys and bladder",
      "kidney ultrasound", "renal bladder ultrasound"}, "RENAL-US"),
]

STRIP = re.compile(r"^(a|an|the)\s+|\s+(alone|only|now|first|immediately|empirically)$")


def canon(value: str | None) -> str:
    # ``ItemRecord.answer`` and HTMLParser attribute values are already
    # decoded once by axlib. Do not unescape again here.
    value = re.sub(r"<[^>]+>", "", value or "")
    value = value.lower().replace("&", "and")
    value = re.sub(r"[^a-z0-9 ]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    for _ in range(3):
        value = STRIP.sub("", value).strip()
    if value in ABBR:
        value = ABBR[value]
    for group, tag in SYN:
        if value in group:
            return tag
    return re.sub(r"\b(syndrome|disease|disorder)$", "", value).strip()


def report(source: str, threshold: int = 4) -> dict:
    document = axlib.parse_html(source)
    keyed: Counter[str] = Counter()
    distractors: Counter[str] = Counter()
    where: defaultdict[str, set[str]] = defaultdict(set)
    for item in document.items:
        answer = canon(item.answer)
        if answer:
            keyed[answer] += 1
        for field in ("data-d1", "data-d2"):
            value = canon(item.attr_map.get(field))
            if value:
                distractors[value] += 1
                where[value].add(item.brief_id)
    candidates = [
        {"value": key, "count": count, "brief_ids": sorted(where[key])}
        for key, count in distractors.most_common()
        if count >= threshold and keyed.get(key, 0) == 0
    ]
    return {
        "input_bytes": len(source.encode("utf-8")),
        "briefs": len(document.briefs),
        "items": len(document.items),
        "keyed_distinct": len(keyed),
        "distractor_distinct": len(distractors),
        "alias_count": len(ABBR),
        "synonym_group_count": len(SYN),
        "threshold": threshold,
        "candidates": candidates,
        "candidate_count": len(candidates),
        "policy": "historical alias-normalized advisory; never a deletion or zero-target rule",
        "parser_errors": document.errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--threshold", type=int, default=4)
    args = parser.parse_args(argv)
    result = report(args.input.read_text(encoding="utf-8"), args.threshold)
    print(f"INPUT: {args.input.resolve()}")
    print(f"KEYED distinct: {result['keyed_distinct']} | DISTRACTOR distinct: {result['distractor_distinct']}")
    print(f"alias set: {result['alias_count']} abbreviations + {result['synonym_group_count']} synonym groups (advisory)")
    print(f"never-keyed at >={args.threshold}x, alias-normalized: {result['candidate_count']}")
    for row in result["candidates"]:
        print(f"   {row['count']:2d}x  {row['value'][:46]:46s}  [{', '.join(row['brief_ids'][:3])}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
