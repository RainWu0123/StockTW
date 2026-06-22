#!/usr/bin/env python3
"""
STAR 五維雙轨分級系統 — 只輸出 raw score + rank，不再 assign tier。
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

def safe_num(v, default=0.0):
    try:
        n = float(v)
        return n if math.isfinite(n) else default
    except Exception:
        return default

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

def score_liquidity(s):
    price = safe_num(s.get("price"), 0)
    vol = safe_num(s.get("vol"), 0)
    turnover = (vol * price * 1000) / 10000 if price > 0 else 0
    t_score = min(turnover / 5000, 1.0) * 30
    pct = safe_num(s.get("pct"), 0)
    if vol > 0 and pct > 3:
        attack = 70
    elif vol > 0 and pct > 1:
        attack = 55
    elif vol > 0 and pct > 0:
        attack = 40
    elif vol > 0 and pct > -2:
        attack = 20
    else:
        attack = 5
    return clamp(t_score + attack)

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
    score = 0.0
    if pct > 5: score += 50
    elif pct > 3: score += 35
    elif pct > 1: score += 20
    elif pct > -1: score += 10
    else: score += 3
    score += min(abs(pct) / 5, 1.0) * 30
    return clamp(score)

def score_fund_flow(s):
    inst = safe_num(s.get("institutionPercentHeld"), 50)
    vol = safe_num(s.get("vol"), 0)
    avg = safe_num(s.get("averageVolume10days"), 0)
    score = (inst / 100) * 50
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

def classify(dims, track):
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

    s1_raw = classify(dims, "S1")
    s2_raw = classify(dims, "S2")

    results.append({
        "code": code,
        "name": name,
        "price": price,
        "pct": pct,
        "vol": vol,
        "dimensions": {k: round(v, 2) for k, v in dims.items()},
        "s1_raw": s1_raw,
        "s2_raw": s2_raw,
        "score": round(max(s1_raw, s2_raw), 2),
        "rank": 0,
        "note": note,
    })

results.sort(key=lambda x: (-x["score"], x["code"]))
for i, r in enumerate(results):
    r["rank"] = i + 1

out = {
    "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
    "generated": datetime.now().isoformat(),
    "rules_version": rules.get("version", ""),
    "stocks": results,
}

with open(OUT_SCORES, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"[score] {len(results)} stocks -> {OUT_SCORES}")
for r in results[:10]:
    print('  ', r['rank'], r['code'], r['name'], 'score=', r['score'], 'S1=', r['s1_raw'], 'S2=', r['s2_raw'])
