#!/usr/bin/env python3
"""Decision helper for buy/sell/position questions on Taiwan stocks.
Inputs: ticker, question context.
Outputs: YES / NO / HOLD plus rationale and explicit risk reasons.

Rules:
- NO hype. NO buy-it-because-news positive.
- If evidence is weak or mixed -> strict default is NO / HOLD.
- Always output risks and veto conditions.
"""
import json, re, sys
from datetime import datetime, timezone, timedelta

try:
    import yfinance as yf
except Exception as e:
    print(json.dumps({"ok": False, "error": f"yfinance import failed: {e}"}, ensure_ascii=False))
    raise SystemExit(1)

def now_tw():
    return datetime.now(timezone(timedelta(hours=8)))

# Hard filters: automatic NO or NO+HOLD situations
HARD_NO_PATTERNS = [
    r"designated security", r"全額交割", r"處置", r"cash delivery",
    r"重大訊息待公布", r"變更交易方法", r"停止買賣",
]
HARD_RISK_PATTERNS = [
    r"董監事質押", r"海外公司法"
]

def detect_flags(ticker: str):
    try:
        info = yf.Ticker(ticker).info
    except Exception:
        info = {}
    text = json.dumps(info, ensure_ascii=False)
    veto = []
    risk = []
    for p in HARD_NO_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            veto.append(p)
    for p in HARD_RISK_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            risk.append(p)
    vet = bool(veto)
    return {"veto": vet, "veto_reasons": veto, "risk_reasons": risk, "raw_note": info.get("shortName", "")}

def price_context(ticker: str):
    try:
        h = yf.Ticker(ticker).history(period="5mo", interval="1d")
        if h.empty:
            return {"ok": False}
        close = float(h["Close"].iloc[-1])
        high52 = float(h["High"].max())
        low52 = float(h["Low"].min())
        ma20 = float(h["Close"].rolling(20).mean().iloc[-1])
        ma60 = float(h["Close"].rolling(20).mean().iloc[-1]) if len(h) >= 60 else None
        vol = float(h["Volume"].iloc[-1])
        return {"ok": True, "close": close, "pct_from_52h": round((close - high52) / high52 * 100, 1), "pct_from_52l": round((close - low52) / low52 * 100, 1), "above_ma20": close > ma20, "ma20": round(ma20, 2), "ma60": round(ma60, 2) if ma60 is not None else None}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def decide(price, flags, question: str):
    # Default strict
    verdict = "NO"
    reasons = []
    if flags["veto"]:
        return "NO", [f"VETO: {r} exists" for r in flags["veto_reasons"]], ["wait for clean filter pass"]
    p = price
    if not p["ok"]:
        return "NO", ["price context unavailable"], ["retry later"]
    if p.get("ma60") and p["close"] < min(p.get("ma20", 1e18), p.get("ma60", 1e18)):
        verdict = "NO"
        reasons.append("price below key moving averages")
    elif p.get("above_ma20"):
        verdict = "HOLD"
        reasons.append("above MA20 but not confirmed")
    else:
        verdict = "HOLD"
        reasons.append("no confirmation")
    return verdict, reasons + [f"52w:{p['pct_from_52h']}%", f"risk flags:{flags['risk_reasons'] or 'none'}"], ["check institutional calendar", "do not size up before volatility drop"]

def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "2330.TW"
    question = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "可不可以買"
    flags = detect_flags(ticker)
    price = price_context(ticker)
    verdict, reasons, next_steps = decide(price, flags, question)
    out = {
        "ts": now_tw().isoformat(),
        "ticker": ticker,
        "question": question,
        "verdict": verdict,
        "reasons": reasons,
        "next_steps": next_steps,
        "flags": flags,
        "price": price,
    }
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
