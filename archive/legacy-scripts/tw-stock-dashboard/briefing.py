#!/usr/bin/env python3
"""TW stock daily briefing: price-volume + hard filter flags for a human decision.
Output: compact JSON. Strict: no hype.
"""
import json
from datetime import datetime, timezone, timedelta

try:
    import yfinance as yf
except Exception as e:
    print(json.dumps({"ok": False, "error": f"yfinance import failed: {e}"}, ensure_ascii=False))
    raise SystemExit(1)

def now_tw():
    return datetime.now(timezone(timedelta(hours=8)))

def rsi(series, window=14):
    import pandas as pd
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    avg_up = up.ewm(alpha=1/window, adjust=False).mean()
    avg_down = down.ewm(alpha=1/window, adjust=False).mean()
    return 100 - (100 / (1 + avg_up / avg_down))

def fetch(ticker):
    h = yf.Ticker(ticker).history(period="6mo", interval="1d")
    if h.empty:
        return {"ticker": ticker, "ok": False, "reason": "ohlcv empty"}
    ma20 = h["Close"].rolling(20).mean().iloc[-1]
    ma60 = h["Close"].rolling(60).mean().iloc[-1]
    last_rsi = float(rsi(h["Close"]).iloc[-1])
    close = float(h["Close"].iloc[-1])
    prev_close = float(h["Close"].shift(1).iloc[-1])
    return {
        "ticker": ticker,
        "close": close,
        "change_pct": round((close - prev_close) / prev_close * 100, 2),
        "volume_vs_20d": round(float(h["Volume"].iloc[-1]) / max(1e-9, float(h["Volume"].rolling(20).mean().iloc[-1])), 2),
        "ma20": round(float(ma20), 2),
        "ma60": round(float(ma60), 2),
        "rsi14": round(last_rsi, 1),
        "trend": "uptrend" if ma20 > ma60 else "downtrend" if ma20 < ma60 else "sideways",
    }

def quality_flags(ticker):
    try:
        info = yf.Ticker(ticker).fast_info or {}
    except Exception:
        info = {}
    flags = []
    if info.get("exchange") not in ["TAI", "TWO"]:
        flags.append("exchange:unknown")
    # policy: do NOT report yfinance estimates as real institutional holdings
    flags.append("institutional:not_real_time")
    return flags

def main():
    tickers = ["^TWII", "2330.TW", "2317.TW"]
    out = {"ts": now_tw().isoformat(), "source": "yfinance", "prices": [], "index_flags": {}, "rules": {}}
    for t in tickers:
        out["prices"].append(fetch(t))
        out["index_flags"][t] = quality_flags(t)
    out["rules"] = {
        "ex_dividend_count": 3,
        "designated_securities_count": 12,
        "futures_expiry": "3rd Wednesday of month",
        "cooling_filter": "designated/cash_delivery securities excluded by default",
        "holder_note": "major-holder data is T+1 and NOT real-time; do not infer intraday intent.",
    }
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
