#!/usr/bin/env python3
"""
回溯測試：用現有五維 STAR 算法，回溯過去 20 個交易日。
輸出：各級別勝率、平均報酬、級別跳躍次數。
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

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

stocks = data.get("stocks", [])
codes = [s["code"] for s in stocks if s.get("code")]
print(f"[backtest] {len(codes)} stocks")

# 拉 20 日日線（yfinance）
def fetch_history(code):
    tickers = [code + ".TW", code + ".TWO"]
    hist = None
    for tk in tickers:
        try:
            t = yf.Ticker(tk)
            h = t.history(period="1mo", interval="1d")
            if h is not None and not h.empty:
                hist = h
                break
        except Exception:
            continue
    return hist

records = {}
for code in codes:
    h = fetch_history(code)
    if h is None or h.empty:
        print(f"[backtest] {code} no history")
        continue
    rows = []
    for idx, r in h.iterrows():
        rows.append({
            "date": idx.strftime("%Y-%m-%d"),
            "open": float(r["Open"]) if not math.isnan(r["Open"]) else None,
            "high": float(r["High"]) if not math.isnan(r["High"]) else None,
            "low": float(r["Low"]) if not math.isnan(r["Low"]) else None,
            "close": float(r["Close"]) if not math.isnan(r["Close"]) else None,
            "volume": int(r["Volume"]) if not math.isnan(r["Volume"]) else 0,
        })
    records[code] = rows
    time.sleep(0.05)

print(f"[backtest] loaded history for {len(records)} codes")

# 載入 scoring rules
with open(os.path.join(BASE, "data", "scoring_rules.json"), "r", encoding="utf-8") as f:
    rules = json.load(f)

def safe_num(v, default=0.0):
    try:
        n = float(v)
        return n if math.isfinite(n) else default
    except Exception:
        return default

def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))

# 五維函數（與 score_stocks.py 同步）
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
    if pct > 5:
        score += 50
    elif pct > 3:
        score += 35
    elif pct > 1:
        score += 20
    elif pct > -1:
        score += 10
    else:
        score += 3
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

MIN_TURNOVER = rules.get("pre_filters", {}).get("min_turnover", 3000)

# 回溯主 loop
lookback = 20
summary = {
    "generated_at": datetime.now().isoformat(),
    "lookback_days": lookback,
    "rules_version": rules.get("version", ""),
    "daily": [],
    "stats": {}
}

all_dates = sorted({r["date"] for rows in records.values() for r in rows})
target_dates = all_dates[-lookback:] if len(all_dates) >= lookback else all_dates

tier_hits = {t: {"count": 0, "win": 0, "returns": []} for t in ["S1", "S2", "A", "B", "C", "D", "E"]}
tier_transitions = {code: [] for code in codes}

for date in target_dates:
    day_result = {"date": date, "stocks": []}
    for code in codes:
        rows = records.get(code, [])
        row = next((r for r in rows if r["date"] == date), None)
        if not row or not row.get("close"):
            continue
        # 找前一日收盤（計算 pct）
        prev_rows = [r for r in rows if r["date"] < date and r.get("close")]
        if prev_rows:
            prev = prev_rows[-1]["close"]
            pct = round((row["close"] - prev) / prev * 100, 2)
        else:
            pct = 0.0
        s = {
            "code": code,
            "name": next((x["name"] for x in stocks if x["code"] == code), code),
            "price": row["close"],
            "pct": pct,
            "vol": row.get("volume", 0) or 0,
        }
        # 補齊 yfinance 衍生字段（從 history 算）
        # 簡化：52WeekHigh/Low 不回溯，用當日快照近似（此處略）
        # fundamental fields 也用快照近似（略）
        dims = {
            "liquidity": score_liquidity(s),
            "momentum": score_momentum(s),
            "alpha": score_alpha(s),
            "fund_flow": score_fund_flow(s),
            "theme": score_theme(s),
            "fundamental": score_fundamental(s),
        }
        s1 = classify(dims, "S1")
        s2 = classify(dims, "S2")
        tier = "E"
        turnover_est = (safe_num(s["vol"], 0) * safe_num(s["price"], 0) * 1000) / 10000 if safe_num(s["price"], 0) > 0 else 0
        assigned = False
        if turnover_est < MIN_TURNOVER:
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
        entry = {
            "code": code,
            "name": s["name"],
            "price": round(row["close"], 2),
            "pct": pct,
            "tier": tier,
            "s1": s1,
            "s2": s2,
        }
        day_result["stocks"].append(entry)
        tier_hits[tier]["count"] += 1
        # 次日收益（若存在）
        next_rows = [r for r in rows if r["date"] > date and r.get("close")]
        if next_rows:
            nxt = next_rows[0]
            future_return = round((nxt["close"] - row["close"]) / row["close"] * 100, 2)
            if future_return > 0:
                tier_hits[tier]["win"] += 1
            tier_hits[tier]["returns"].append(future_return)
        # 記錄級別變化
        tier_transitions.setdefault(code, []).append({"date": date, "tier": tier})
    day_result["stocks"].sort(key=lambda x: -{"S1":5,"S2":4,"A":3,"B":2,"C":1,"D":0,"E":0}.get(x["tier"],0))
    summary["daily"].append(day_result)

# 統計
for t, v in tier_hits.items():
    cnt = v["count"]
    if cnt > 0:
        v["win_rate"] = round(v["win"] / cnt, 3)
        rets = v["returns"]
        if rets:
            v["avg_return"] = round(sum(rets) / len(rets), 3)
            v["max_drawdown"] = round(min(rets), 3) if rets else 0
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
