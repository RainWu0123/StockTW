#!/usr/bin/env python3
"""
STAR 五維雙軌分級系統 v2
全部基於 yfinance API 真實數據，不再用 note 文字匹配。
"""
import json, os, math
from datetime import datetime

BASE = "/home/ubuntu/investment"
RULE = os.path.join(BASE, "data", "scoring_rules.json")
DATA_JSON = os.path.join(BASE, "data.json")
OUT_SCORES = os.path.join(BASE, "data", "scores.json")

with open(RULE, "r", encoding="utf-8") as f:
    rules = json.load(f)

with open(DATA_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

stocks = data.get("stocks", []) or []

# Safe helpers
def safe_num(v, default=0.0):
    try:
        n = float(v)
        return n if math.isfinite(n) else default
    except Exception:
        return default

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

# === 五維量化函數（全部讀 API 字段） ===

def score_liquidity(s):
    price = safe_num(s.get("price"), 0)
    vol = safe_num(s.get("vol", 0))
    turnover = (vol * price * 1000) / 10000 if price > 0 else 0
    t_score = min(turnover / 5000, 1.0) * 60
    pct = abs(safe_num(s.get("pct", 0)))
    spread_score = max(0, (5 - pct) / 5) * 40
    return clamp(t_score + spread_score)

def score_momentum(s):
    pct = safe_num(s.get("pct"), 0)
    rev = safe_num(s.get("revenueGrowth"), 0)
    score = 0.0
    score += min(abs(pct) / 3, 1.0) * 40
    score += min(max(rev, -1), 1) * 15 + 15
    price = safe_num(s.get("price"), 0)
    high = safe_num(s.get("52WeekHigh"), 0)
    low = safe_num(s.get("52WeekLow"), 0)
    if high > low and price > 0:
        pos = (price - low) / (high - low)
        score += pos * 30
    return clamp(score)

def score_alpha(s):
    pct = safe_num(s.get("pct"), 0)
    beta = safe_num(s.get("beta"), 1)
    score = 0.0
    if pct > 3:
        score += 50
    elif pct > 1:
        score += 35
    elif pct > -1:
        score += 20
    elif pct > -3:
        score += 10
    beta_dev = abs(beta - 1)
    score += max(0, (1 - min(beta_dev, 1))) * 50
    return clamp(score)

def score_fund_flow(s):
    inst = safe_num(s.get("institutionPercentHeld"), 50)
    vol = safe_num(s.get("vol"), 0)
    avg = safe_num(s.get("averageVolume10days"), 0)
    score = 0.0
    score += (inst / 100) * 50
    if avg > 0:
        ratio = vol / avg
        score += min(ratio, 2.0) / 2.0 * 50
    return clamp(score)

def score_theme(s):
    return 0.0

def score_fundamental(s):
    pe = safe_num(s.get("trailingPE"), 0)
    rev = safe_num(s.get("revenueGrowth"), 0)
    earn = safe_num(s.get("earningsGrowth"), 0)
    score = 0.0
    if pe > 0:
        score += max(0, (1 - min(pe / 50, 1))) * 30
    score += min(max(rev, -1), 1) * 17.5 + 17.5
    score += min(max(earn, -1), 1) * 17.5 + 17.5
    return clamp(score)

def classify_track(dims, track):
    w = rules["tracks"][track]["weights"]
    raw = (
        dims["liquidity"] * w.get("liquidity", 0) / 100 +
        dims["momentum"] * w.get("momentum", 0) / 100 +
        dims["alpha"] * w.get("alpha", 0) / 100 +
        dims["fund_flow"] * w.get("fund_flow", 0) / 100 +
        dims["theme"] * w.get("theme", 0) / 100 +
        dims["fundamental"] * w.get("fundamental", 0) / 100
    )
    return round(raw, 2)

# === Main ===
MIN_TURNOVER = rules.get("pre_filters", {}).get("min_turnover", 3000)

results = []
for s in stocks:
    code = s.get("code", "")
    name = s.get("name", code)
    price = s.get("price")
    pct = s.get("pct")
    vol = s.get("vol", 0)
    note = s.get("note", "")

    dims = {
        "liquidity": score_liquidity(s),
        "momentum": score_momentum(s),
        "alpha": score_alpha(s),
        "fund_flow": score_fund_flow(s),
        "theme": score_theme(s),
        "fundamental": score_fundamental(s),
    }

    s1_raw = classify_track(dims, "S1")
    s2_raw = classify_track(dims, "S2")

    track_rules = rules.get("tracks", {})
    tier = "E"
    tier_label = track_rules.get("E", {}).get("label", "前置過濾不合格")
    action = track_rules.get("E", {}).get("action", {})
    track_assigned = None

    turnover_est = (safe_num(vol, 0) * safe_num(price, 0) * 1000) / 10000 if safe_num(price, 0) > 0 else 0
    if turnover_est < MIN_TURNOVER:
        tier = "E"
        tier_label = "流動性不足"
        action = track_rules.get("E", {}).get("action", {})
        track_assigned = "E"
    else:
        assigned = False
        if s1_raw >= track_rules.get("S1", {}).get("min_score", 60) and not track_rules.get("S1", {}).get("macro_bound", False):
            tier = "S1"
            tier_label = track_rules["S1"]["label"]
            action = track_rules["S1"]["action"]
            track_assigned = "S1"
            assigned = True
        if not assigned and s2_raw >= track_rules.get("S2", {}).get("min_score", 55):
            tier = "S2"
            tier_label = track_rules["S2"]["label"]
            action = track_rules["S2"]["action"]
            track_assigned = "S2"
            assigned = True
        if not assigned:
            for t in ["A", "B"]:
                thr = track_rules.get(t, {}).get("min_score", 0)
                if t == "A" and s1_raw >= thr:
                    tier = "A"; tier_label = "觀察"; action = track_rules["A"]["action"]; track_assigned = "A"; break
                if t == "B" and s1_raw >= thr:
                    tier = "B"; tier_label = "觀望"; action = track_rules["B"]["action"]; track_assigned = "B"; break
            if not track_assigned:
                tier = "C"; tier_label = "不建議"; action = track_rules.get("C", {}).get("action", {})

    tier_cls_map = {"S1": "tier-t1", "S2": "tier-t2", "A": "tier-t3", "B": "tier-t4", "C": "tier-t4", "D": "tier-t4", "E": "tier-t4"}
    results.append({
        "code": code,
        "name": name,
        "price": price,
        "pct": pct,
        "vol": vol,
        "turnover": round(turnover_est, 0),
        "dimensions": {k: round(v, 2) for k, v in dims.items()},
        "s1_raw": s1_raw,
        "s2_raw": s2_raw,
        "tier": tier,
        "tier_label": tier_label,
        "tier_cls": tier_cls_map.get(tier, "tier-t4"),
        "action": action,
        "track_assigned": track_assigned,
        "note": note,
    })

results.sort(key=lambda x: (
    -{"S1":4,"S2":3,"A":2,"B":1,"C":0,"D":0,"E":0}.get(x["tier"],0),
    -(x["s1_raw"] if x["tier"] == "S1" else x["s2_raw"]),
    x["code"]
))

out = {
    "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
    "generated": datetime.now().isoformat(),
    "rules_version": rules.get("version", ""),
    "stocks": results,
}

with open(OUT_SCORES, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"[score] {len(results)} stocks -> {OUT_SCORES}")
dist = {t: sum(1 for r in results if r["tier"] == t) for t in ["S1","S2","A","B","C","D","E"]}
print("[score] Tier distribution:", dist)
for r in results[:10]:
    print('  ', r['code'], r['name'], r['tier'], 'S1=', r['s1_raw'], 'S2=', r['s2_raw'])
