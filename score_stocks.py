#!/usr/bin/env python3
"""Quant scoring with safe fallback derived fields."""
import json, os, glob
from datetime import datetime

BASE = "/home/ubuntu/investment"
RULE = os.path.join(BASE, "data", "scoring_rules.json")
paths = sorted(glob.glob(os.path.join(BASE, "data", "snapshot_*.json")))
if not paths:
    raise SystemExit("no snapshot")
snap_path = paths[-1]
with open(RULE, "r", encoding="utf-8") as f:
    rules = json.load(f)
with open(snap_path, "r", encoding="utf-8") as f:
    snap = json.load(f)

weights = rules.get("weights", {})
field_max = rules.get("field_max", {})
thresholds = rules.get("thresholds", {})
pct_cuts = rules.get("percentile_cutoffs")


def clamp(v):
    return max(0.0, min(1.0, float(v)))


def sf(v, field):
    if v is None:
        return None
    return clamp(v / max(float(field_max.get(field, 1) or 1), 1e-9))


# robust helper
def safe_float(x):
    try:
        v = float(x)
        if v != v:  # NaN
            return None
        return v
    except Exception:
        return None


def derive(rec):
    score = 0.0
    n2 = (rec.get("name") or "")
    if any(k in n2 for k in ["台達", "散熱", "光", "電"]):
        score += 1
    if any(k in n2 for k in ["台積", "聯電", "聯發", "台光", "日月光"]):
        score += 1
    if any(k in n2 for k in ["華邦", "南亞", "DRAM", "凱美", "力成", "國巨"]):
        score += 1
    if any(k in n2 for k in ["創意", "大立光", "奇鋐"]):
        score += 1
    if any(k in n2 for k in ["凌華", "研華", "工業"]):
        score += 1
    rec["theme_score"] = min(5, int(score))
    rec["in_ai_etf"] = bool(rec.get("in_ai_etf"))
    rec["limit_up_flag"] = bool(rec.get("limit_up_flag"))
    rec["vol_ratio_5d"] = safe_float(rec.get("vol_ratio_5d")) or 1.0


records = snap.get("stocks", []) or []
for rec in records:
    derive(rec)

rows = []
for s in records:
    total = 0.0
    wsum = 0.0
    parts = {}
    for field, w in weights.items():
        rv = s.get(field, 0.0)
        sc = sf(rv, field) if rv is not None else None
        parts[field] = round(sc, 4) if sc is not None else None
        total += round((sc or 0.0) * float(w), 4)
        wsum += float(w)
    score = round((total / max(wsum, 1.0)) * 100, 1)
    rows.append(
        {
            "code": s.get("code", ""),
            "name": s.get("name", ""),
            "price": s.get("price"),
            "pct": s.get("pct"),
            "vol": s.get("vol"),
            "score": score,
            "parts": parts,
        }
    )

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
            p = float(pct_cuts[t])
            if 0 < p < 1:
                idx = int(len(sorted_scores) * p)
                cutoff = sorted_scores[max(0, min(idx, len(sorted_scores) - 1))]
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
