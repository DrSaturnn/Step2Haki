"""Deterministic ids for NEW items only. Existing ids are permanent and never regenerated.
Seed = brief | type | full key | full stem, so two items differ unless every part matches."""
import hashlib,re
def _n(s): return re.sub(r'\s+',' ',s).strip()
def item_id(brief,typ,key,stem): return 'q_'+hashlib.sha256(f"{brief}|{typ}|{_n(key)}|{_n(stem)}".encode()).hexdigest()[:20]
def option_id(item,slot,label): return 'o_'+hashlib.sha256(f"{item}|{slot}|{_n(label)}".encode()).hexdigest()[:20]
