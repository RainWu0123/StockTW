#!/usr/bin/env python3
"""TWSE 即時快照 → /home/ubuntu/investment/data/snapshot_<date>.json (行情 + 量化衍生字段)"""
import json, requests, time, os, sys
from datetime import datetime

SYMBOLS = [
    ("2327","國巨"),("2408","南亞科"),("2344","華邦電"),("2303","聯電"),
    ("6166","凌華"),("7610","聯友金屬"),("6442","光聖"),("2375","凱美"),
    ("3017","奇鋐"),("3711","日月光"),("2454","聯發科"),("3443","創意"),
    ("3008","大立光"),("2308","台達電"),("2330","台積電"),("2313","華通"),
    ("2395","研華"),("6285","啟碁"),("6830","汎銓"),("6239","力成"),
    ("2404","漢唐"),("2383","台光電"),
]

AI_ETF_HOLDINGS = {"2327","2383","2344","2408","2308","2330","3017","3711","6166","6442","2375","2454","2303","7610"}

def fetch(symbols):
    chunk = ",".join(f"tse_{s}.tw" for s,_ in symbols)
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={chunk}"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
    r.raise_for_status()
    return r.json().get("msgArray", [])

def parse(data):
    out = []
    for d in data:
        try:
            code = d.get("c","")
            name = d.get("n","")
            price = float(d.get("z", d.get("o", 0)) or 0)
            chg = float(d.get("a", d.get("y", 0)) or 0)
            pct = ((price - chg) / chg * 100) if chg else 0.0
            vol = int(d.get("v",0))
            tx = int(d.get("t",0)) if d.get("t") else 0
            out.append({
                "code": code,
                "name": name,
                "price": round(price,2),
                "pct": round(pct,2),
                "vol": vol,
                "tx": tx,
            })
        except Exception:
            continue
    return out

def derive_quant(records):
    """From raw TWSE snap derive quantitative fields used by scoring_rules.json."""
    n = len(records) or 1
    avg_vol = sum(r["vol"] for r in records) / n
    avg_amt = sum(r["price"] * r["vol"] * 1000 for r in records) / n

    # 5-day placeholders (will be replaced once 7d price history is stored)
    for r in records:
        r["revenue_yoy"] = None     # placeholder
        r["foreign_net_days"] = 0   # placeholder
        r["dealer_net_days"] = 0   # placeholder
        r["dist_52w_high"] = 0     # placeholder
        r["vol_ratio_5d"] = r["vol"] / avg_vol if avg_vol else 1.0
        r["limit_up_flag"] = r["pct"] >= 9.5
        r["in_ai_etf"] = r["code"] in AI_ETF_HOLDINGS
        # theme_score 0-5: crude proxy by NAME substring
        score = 0
        n2 = r["name"]
        if any(k in n2 for k in ["台積","聯電","聯發","奇鋐","日月光","台達","台光","華通","大立光","創意"]): score += 1
        if any(k in n2 for k in ["散熱","光","電","網"]): score += 1
        if "DRAM" in n2 or "南亞" in n2 or "華邦" in n2: score += 1
        if any(k in n2 for k in ["鋼","金屬","鑫"]): score += 1
        if any(k in n2 for k in ["巨","凱美","力成"]): score += 1
        r["theme_score"] = min(score, 5)

def main():
    base = "/home/ubuntu/investment"
    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = os.path.join(base, "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"snapshot_{today}.json")

    print(f"[fetch] date={today} symbols={len(SYMBOLS)}", flush=True)
    raw = []
    for i in range(0, len(SYMBOLS), 5):
        chunk = SYMBOLS[i:i+5]
        try:
            raw.extend(fetch(chunk))
            time.sleep(0.3)
        except Exception as e:
            print(f"[warn] chunk fail: {e}", flush=True)

    records = parse(raw)
    derive_quant(records)

    snapshot = {
        "date": today,
        "updated": datetime.now().isoformat(),
        "stocks": records,
        "meta": {
            "fields": {"revenue_yoy":"待補","foreign_net_days":"待補","dealer_net_days":"待補","dist_52w_high":"待補"},
            "note": "量化评分暂缓字段：营收YoY、法人连续天数、52周距离、5日均量比（5日K缺失）。请先在 5-agent 会议上讨论7日历史补全方案。"
        }
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"[done] -> {out_path} ({len(records)} stocks)", flush=True)
    return out_path

if __name__ == "__main__":
    main()
