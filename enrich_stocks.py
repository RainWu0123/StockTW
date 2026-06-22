#!/usr/bin/env python3
"""用 yfinance 對 data.json 補齊真實量化數據（非文字匹配）。"""
import json, time
import yfinance as yf

BASE = "/home/ubuntu/investment"
with open(f"{BASE}/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

fields = ["beta", "marketCap", "trailingPE", "revenueGrowth", "earningsGrowth",
          "institutionPercentHeld", "52WeekHigh", "52WeekLow", "averageVolume10days"]

for s in data["stocks"]:
    code = s["code"]
    ticker = None
    # 優先 .TW，失敗再試 .TWO
    for ext in [".TW", ".TWO"]:
        try:
            tk = yf.Ticker(code + ext)
            info = tk.fast_info
            # basic price/pct 若已老舊也順便刷新
            last = getattr(info, "last_price", None) or getattr(info, "regularMarketPrice", None)
            prev = getattr(info, "previous_close", None)
            if last and prev and prev != 0:
                s["price"] = round(last, 2)
                s["pct"] = round((last - prev) / prev * 100, 2)
            # 真實字段
            s["beta"] = getattr(info, "beta", None)
            s["marketCap"] = getattr(info, "market_cap", None)
            # 部分欄位在 info dict
            info_dict = tk.info if hasattr(tk, "info") else {}
            s["trailingPE"] = info_dict.get("trailingPE")
            s["revenueGrowth"] = info_dict.get("revenueGrowth")
            s["earningsGrowth"] = info_dict.get("earningsGrowth")
            s["institutionPercentHeld"] = info_dict.get("institutionPercentHeld")
            s["52WeekHigh"] = info_dict.get("fiftyTwoWeekHigh")
            s["52WeekLow"] = info_dict.get("fiftyTwoWeekLow")
            s["averageVolume10days"] = getattr(info, "ten_day_average_volume", None) or info_dict.get("averageVolume10days")
            ticker = code + ext
            break
        except Exception:
            continue
    if not ticker:
        print(f"[enrich] {code} FAILED")
        continue
    print(f"[enrich] {code} via {ticker}: beta={s.get('beta')}, pe={s.get('trailingPE')}, revg={s.get('revenueGrowth')}")
    time.sleep(0.05)

with open(f"{BASE}/data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("[enrich] done")
