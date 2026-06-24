#!/usr/bin/env python3
"""
基本面選股系統 — 參考《別再看股價了》：
只看 ROE / 營收成長 / EPS成長 / PE，完全去掉價格噪聲。
"""
import json, os, math, time
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
    if v is None:
        return default
    try:
        n = float(v)
        return n if math.isfinite(n) else default
    except Exception:
        return default

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

def tiered_score_desc(value, tiers):
    for t in tiers:
        th = safe_num(t.get("threshold", 0))
        if t.get("threshold_type", "desc") == "default":
            return safe_num(t.get("score", 0), 0)
        if safe_num(value, -999) >= th:
            return safe_num(t.get("score", 0), 0)
    return 0.0

def tiered_score_asc(value, tiers):
    for t in tiers:
        th = safe_num(t.get("threshold", 0))
        if t.get("threshold_type", "default") == "default":
            return safe_num(t.get("score", 0), 0)
        if safe_num(value, 999) <= th:
            return safe_num(t.get("score", 0), 0)
    return 0.0

def score_roe(s):
    inst = safe_num(s.get("institutionPercentHeld"), None)
    if inst is not None and inst > 0:
        roe_est = (inst / 100.0) * 0.30
    else:
        roe_est = None
    roe = roe_est
    if roe is None or roe <= 0:
        try:
            import yfinance as yf
            tk = yf.Ticker(s.get("code", "") + ".TW")
            info = tk.info
            roe = safe_num(info.get("returnOnEquity"), None)
            if roe is None and hasattr(tk, "fast_info"):
                roe = safe_num(getattr(tk.fast_info, "roe", None), None)
            time.sleep(0.02)
        except Exception:
            roe = None
    if roe is None:
        return 0.0
    return clamp(tiered_score_desc(roe, rules.get("roe_tiers", [])))

def score_revenue_growth(s):
    rev = safe_num(s.get("revenueGrowth"), None)
    if rev is None:
        return 0.0
    return clamp(tiered_score_desc(rev, rules.get("revenue_growth_tiers", [])))

def score_earnings_growth(s):
    earn = safe_num(s.get("earningsGrowth"), None)
    if earn is None:
        return 0.0
    return clamp(tiered_score_desc(earn, rules.get("earnings_growth_tiers", [])))

def score_valuation(s):
    pe = safe_num(s.get("trailingPE"), None)
    if pe is None or pe <= 0:
        return 0.0
    return clamp(tiered_score_asc(pe, rules.get("valuation_tiers", [])))

results = []
for s in stocks:
    code = s.get("code", "")
    name = s.get("name", code)
    price = s.get("price")
    pct = s.get("pct")
    vol = s.get("vol", 0)
    note = s.get("note", "")

    dims = {
        "roe": score_roe(s),
        "revenueGrowth": score_revenue_growth(s),
        "earningsGrowth": score_earnings_growth(s),
        "valuation": score_valuation(s),
    }

    w = rules.get("weights", {})
    total = (
        dims["roe"] * w.get("roe", 0) / 100 +
        dims["revenueGrowth"] * w.get("revenueGrowth", 0) / 100 +
        dims["earningsGrowth"] * w.get("earningsGrowth", 0) / 100 +
        dims["valuation"] * w.get("valuation", 0) / 100
    )

    results.append({
        "code": code,
        "name": name,
        "price": price,
        "pct": pct,
        "vol": vol,
        "dimensions": {k: round(v, 2) for k, v in dims.items()},
        "score": round(total, 2),
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
    print('  ', r['rank'], r['code'], r['name'], 'score=', r['score'], 'dims=', r['dimensions'])
