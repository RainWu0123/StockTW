#!/usr/bin/env python3
"""
回溯測試：從 yfinance 拉 60 日日線，逐日重建 STAR 分數，
只使用當日可見的價格/量能數據。
"""
import json, time, math
from datetime import datetime, timedelta
import os

try:
    import yfinance as yf
except Exception as e:
    print("[backtest] yfinance import failed:", e)
    raise SystemExit(1)

BASE = "/home/ubuntu/investment"
DATA_PATH = os.path.join(BASE, "data.json")
OUT_PATH = os.path.join(BASE, "data", "backtest_20d.json")
RULES_PATH = os.path.join(BASE, "data", "scoring_rules.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
with open(RULES_PATH, "r", encoding="utf-8") as f:
    rules = json.load(f)

stocks = data.get("stocks", [])
codes = [s["code"] for s in stocks if s.get("code")]
print(f"[backtest] {len(codes)} stocks")

# 靜態字段
static_fields = {}
for s in stocks:
    static_fields[s["code"]] = {
        "name": s.get("name", s["code"]),
        "revenueGrowth": s.get("revenueGrowth"),
        "earningsGrowth": s.get("earningsGrowth"),
        "trailingPE": s.get("trailingPE"),
        "institutionPercentHeld": s.get("institutionPercentHeld"),
        "52WeekHigh": s.get("52WeekHigh"),
        "52WeekLow": s.get("52WeekLow"),
        "averageVolume10days": s.get("averageVolume10days"),
    }

def fetch_history(code):
    for tk in [code + ".TW", code + ".TWO"]:
        try:
            t = yf.Ticker(tk)
            h = t.history(period="3mo", interval="1d")
            if h is not None and not h.empty and len(h) >= 10:
                return h
        except Exception:
            continue
    return None

hist_map = {}
for code in codes:
    h = fetch_history(code)
    if h is not None and not h.empty:
        hist_map[code] = h
    time.sleep(0.03)

print(f"[backtest] loaded history for {len(hist_map)}/{len(codes)} codes")

def safe_num(v, default=0.0):
    try:
        n = float(v)
        return n if math.isfinite(n) else default
    except Exception:
        return default

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

def score_liquidity(price, vol, pct):
    turnover = (vol * price * 1000) / 10000 if price > 0 else 0
    t_score = min(turnover / 5000, 1.0) * 30
    if vol > 0 and pct > 3: attack = 70
    elif vol > 0 and pct > 1: attack = 55
    elif vol > 0 and pct > 0: attack = 40
    elif vol > 0 and pct > -2: attack = 20
    else: attack = 5
    return clamp(t_score + attack)

def score_momentum(price, vol, pct, rev_growth):
    score = 0.0
    score += min(abs(pct) / 3, 1.0) * 40
    rev = safe_num(rev_growth, 0)
    score += min(max(rev, -1), 1) * 15 + 15
    score += min(max(pct + 5, 0) / 10, 1.0) * 30
    return clamp(score)

def score_alpha(pct):
    score = 0.0
    if pct > 5: score += 50
    elif pct > 3: score += 35
    elif pct > 1: score += 20
    elif pct > -1: score += 10
    else: score += 3
    score += min(abs(pct) / 5, 1.0) * 30
    return clamp(score)

def score_fund_flow(vol, avg_vol, inst_hold):
    inst = safe_num(inst_hold, 50)
    score = (inst / 100) * 50
    if avg_vol and avg_vol > 0:
        ratio = vol / avg_vol
        score += min(ratio, 2.0) / 2.0 * 50
    return clamp(score)

def score_theme(code, name):
    return 0.0

def score_fundamental(pe, rev, earn):
    score = 0.0
    if pe and pe > 0:
        score += max(0, (1 - min(pe / 50, 1))) * 30
    r = safe_num(rev, 0)
    e = safe_num(earn, 0)
    score += min(max(r, -1), 1) * 17.5 + 17.5
    score += min(max(e, -1), 1) * 17.5 + 17.5
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

lookback = 100
summary = {
    "generated_at": datetime.now().isoformat(),
    "lookback_days": lookback,
    "rules_version": rules.get("version", ""),
    "daily": [],
    "stats": {}
}

tier_hits = {t: {"count": 0, "win": 0, "returns": [], "codes": []} for t in ["S1","S2","A","B","C","D","E"]}

for code in codes:
    h = hist_map.get(code)
    if h is None or len(h) < 10:
        continue
    dates = list(h.index[-lookback:])
    for i, idx in enumerate(dates):
        date_str = idx.strftime("%Y-%m-%d")
        row = h.loc[idx]
        close = float(row["Close"])
        vol = int(row["Volume"]) if not math.isnan(row["Volume"]) else 0
        if i > 0:
            prev_idx = dates[i - 1]
            prev_close = float(h.loc[prev_idx, "Close"])
            pct = round((close - prev_close) / prev_close * 100, 2) if prev_close else 0.0
        else:
            pct = 0.0

        sf = static_fields.get(code, {})
        dims = {
            "liquidity": score_liquidity(close, vol, pct),
            "momentum": score_momentum(close, vol, pct, sf.get("revenueGrowth")),
            "alpha": score_alpha(pct),
            "fund_flow": score_fund_flow(vol, sf.get("averageVolume10days"), sf.get("institutionPercentHeld")),
            "theme": score_theme(code, sf.get("name", "")),
            "fundamental": score_fundamental(sf.get("trailingPE"), sf.get("revenueGrowth"), sf.get("earningsGrowth")),
        }
        s1 = classify(dims, "S1")
        s2 = classify(dims, "S2")
        turnover_est = (vol * close * 1000) / 10000 if close > 0 else 0
        assigned = False
        tier = "E"
        if turnover_est < rules.get("pre_filters", {}).get("min_turnover", 3000):
            tier = "E"
        else:
            if s1 >= rules["tracks"]["S1"]["min_score"] and not rules["tracks"]["S1"].get("macro_bound", False):
                tier = "S1"; assigned = True
            if not assigned and s2 >= rules["tracks"]["S2"]["min_score"]:
                tier = "S2"; assigned = True
            if not assigned:
                if s1 >= rules["tracks"]["A"]["min_score"]:
                    tier = "A"; assigned = True
                elif s1 >= rules["tracks"]["B"]["min_score"]:
                    tier = "B"; assigned = True
                else:
                    tier = "C"
        tier_hits[tier]["count"] += 1
        tier_hits[tier]["codes"].append(code)

        if i + 1 < len(dates):
            nxt_close = float(h.loc[dates[i + 1], "Close"])
            future_ret = round((nxt_close - close) / close * 100, 2)
            if future_ret > 0:
                tier_hits[tier]["win"] += 1
            tier_hits[tier]["returns"].append(future_ret)

for t, v in tier_hits.items():
    cnt = v["count"]
    if cnt > 0:
        v["win_rate"] = round(v["win"] / cnt, 3)
        rets = v["returns"]
        if rets:
            v["avg_return"] = round(sum(rets) / len(rets), 3)
            v["max_drawdown"] = round(min(rets), 3)
        else:
            v["avg_return"] = 0
            v["max_drawdown"] = 0
    else:
        v["win_rate"] = 0
        v["avg_return"] = 0
        v["max_drawdown"] = 0

summary["stats"] = tier_hits
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"[backtest] saved to {OUT_PATH}")
print("[backtest] Stats:")
for t, v in tier_hits.items():
    print(f"  {t}: n={v['count']}, win={v['win_rate']:.2%}, avg_ret={v['avg_return']:.2f}%, max_dd={v['max_drawdown']:.2f}%")
