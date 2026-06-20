#!/usr/bin/env python3
"""TWSE 即時快照 → /home/ubuntu/investment/data/snapshot_<date>.json"""
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
            name = d.get("n","")
            price = float(d.get("z", d.get("o", 0)) or 0)
            # Use 'a' (previous close) for chg; fallback to yesterday price
            chg = float(d.get("a", d.get("y", 0)) or 0)
            if chg:
                pct = (price - chg) / chg * 100
            else:
                pct = 0.0
            out.append({
                "code": d.get("c",""),
                "name": name,
                "price": round(price,2),
                "pct": round(pct,2),
                "vol": int(d.get("v",0)),
            })
        except Exception:
            continue
    return out

def main():
    base = "/home/ubuntu/investment/data"
    os.makedirs(base, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    out_path = os.path.join(base, f"snapshot_{today}.json")

    print(f"[fetch] date={today} symbols={len(SYMBOLS)}", flush=True)
    data = []
    for i in range(0, len(SYMBOLS), 5):
        chunk = SYMBOLS[i:i+5]
        try:
            data.extend(fetch(chunk))
            time.sleep(0.3)
        except Exception as e:
            print(f"[warn] chunk fail: {e}", flush=True)

    parsed = parse(data)
    snapshot = {
        "date": today,
        "updated": datetime.now().isoformat(),
        "stocks": parsed,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"[done] -> {out_path} ({len(parsed)} stocks)", flush=True)
    return out_path

if __name__ == "__main__":
    main()
