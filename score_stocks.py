#!/usr/bin/env python3
"""Quantitative scoring engine.
Reads:
  data/snapshot_<date>.json  (from fetch_twse.py)
  data/scoring_rules.json    (quant weights + thresholds)
Writes:
  data/scores.json
"""
import json, os, glob
from datetime import datetime

BASE = "/home/ubuntu/investment"
RULE_PATH = os.path.join(BASE, "data", "scoring_rules.json")
SNAP_GLOB = os.path.join(BASE, "data", "snapshot_*.json")

with open(RULE_PATH, "r", encoding="utf-8") as f:
    rules = json.load(f)

paths = sorted(glob.glob(SNAP_GLOB))
if not paths:
    raise SystemExit("no snapshot found")
snap_path = paths[-1]
with open(snap_path, "r", encoding="utf-8") as f:
    snap = json.load(f)

weights = rules["weights"]
field_max = rules["field_max"]
thresholds = rules["thresholds"]
pct_cuts = rules.get("percentile_cutoffs")

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, float(v)))

def score_field(value, field):
    if value is None:
        return None
    mx = float(field_max.get(field, 1) or 1)
    return clamp(value / mx)

records = snap.get("stocks", [])
rows = []
for s in records:
    total = 0.0
    wsum = 0.0
    parts = {}
    for field, w in weights.items():
        v = s.get(field)
        sc = score_field(v, field)
        parts[field] = round(sc, 4) if sc is not None else None
        if sc is None:
            continue
        total += sc * float(w)
        wsum += float(w)
    score = round((total / wsum) * 100, 1) if wsum else 0.0
    rows.append({"code": s.get("code",""), "name": s.get("name",""),
                 "price": s.get("price"), "pct": s.get("pct"),
                 "vol": s.get("vol"), "score": score, "parts": parts})

rows.sort(key=lambda x: (-x["score"], x["code"]))
sorted_scores = [r["score"] for r in rows]

for r in rows:
    score = r["score"]
    tier = "T4"
    for t, thr in sorted(thresholds.items(), key=lambda kv: kv[1], reverse=True):
        if t == "T4":
            continue
        cutoff = thr
        if isinstance(pct_cuts, dict) and t in pct_cuts:
            pct = float(pct_cuts[t])
            if 0 < pct < 1:
                idx = int(len(sorted_scores) * pct)
                idx = max(0, min(idx, len(sorted_scores)-1))
                cutoff = sorted_scores[idx]
        if score >= cutoff:
            tier = t
            break
    r["tier"] = tier

out = {
    "date": snap.get("date", datetime.now().strftime("%Y-%m-%d")),
    "generated": datetime.now().isoformat(),
    "rules_version": rules.get("version", ""),
    "thresholds": thresholds,
    "percentile_cutoffs": pct_cuts,
    "stocks": rows,
}

out_path = os.path.join(BASE, "data", "scores.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"[score] {len(rows)} stocks -> {out_path}", flush=True)
