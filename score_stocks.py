#!/usr/bin/env python3
"""Quantitative scoring engine for tracked stocks.

Reads:  data/snapshot_<date>.json  data/scoring_rules.json
Writes: data/scores_<date>.json
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

def clamp(v, lo=0, hi=1):
    return max(lo, min(hi, v))

def score_field(value, field):
    if value is None:
        return None
    mx = field_max.get(field, 1) or 1
    # linear clip 0..1, special bools handled via mx=1
    return clamp((value if isinstance(value,(int,float)) else 0) / mx)

rows = []
for s in snap.get("stocks", []):
    parts = {}
    total = 0.0
    wsum = 0.0
    for field, w in weights.items():
        v = s.get(field)
        sc = score_field(v, field)
        if sc is None:
            parts[field] = None
            continue
        parts[field] = round(sc, 4)
        total += sc * w
        wsum += w
    score = round((total / wsum) * 100, 1) if wsum else 0
    # tier from thresholds highest that passes
    tier = "T4"
    for t, thr in sorted(thresholds.items(), key=lambda kv: kv[1], reverse=True):
        if score >= thr and t != "T4":
            tier = t
            break
    rows.append({
        "code": s.get("code",""),
        "name": s.get("name",""),
        "price": s.get("price"),
        "pct": s.get("pct"),
        "vol": s.get("vol"),
        "score": score,
        "tier": tier,
        "parts": parts,
        "missing_fields": [f for f,v in parts.items() if v is None],
    })

rows.sort(key=lambda x: (-x["score"], x["code"]))
out = {
    "date": snap.get("date", datetime.now().strftime("%Y-%m-%d")),
    "generated": datetime.now().isoformat(),
    "rules_version": rules.get("version", ""),
    "thresholds": thresholds,
    "stocks": rows,
}
out_path = os.path.join(BASE, "data", "scores.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"[score] {len(rows)} stocks -> {out_path}", flush=True)
