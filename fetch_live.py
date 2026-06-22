#!/usr/bin/env python3
"""TWSE 即時快照 → data/live.json（供前端即時刷新用）"""
import json, requests, time, os
from datetime import datetime

BASE = '/home/ubuntu/investment'
DATA_JSON = os.path.join(BASE, 'data.json')
OUT_PATH = os.path.join(BASE, 'data', 'live.json')

def fetch(symbols):
    chunk = "|".join(f"tse_{s}.tw" for s in symbols)
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={chunk}"
    r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
    r.raise_for_status()
    return r.json().get('msgArray', [])

def parse(data):
    out = []
    for d in data:
        try:
            code = d.get('c','')
            name = d.get('n','')
            price = float(d.get('z', d.get('o', 0)) or 0)
            ref = float(d.get('y', 0) or 0)
            pct = ((price - ref) / ref * 100) if ref else 0.0
            vol = int(d.get('v', 0) or 0)
            out.append({
                'code': code,
                'name': name,
                'price': round(price, 2),
                'pct': round(pct, 2),
                'vol': vol,
            })
        except Exception:
            continue
    return out

def main():
    # 讀取 data.json 完整名單
    with open(DATA_JSON, encoding='utf-8') as f:
        data = json.load(f)
    stocks = data.get('stocks', [])
    codes = [s['code'] for s in stocks]
    print(f'[fetch_live] total={len(codes)}', flush=True)

    results = {}
    for i in range(0, len(codes), 20):
        batch = codes[i:i+20]
        try:
            raw = fetch(batch)
            parsed = parse(raw)
            for r in parsed:
                results[r['code']] = r
        except Exception as e:
            print(f'  batch {i} err: {e}', flush=True)
        if i + 20 < len(codes):
            time.sleep(0.3)

    # 補上 TWSE API 沒回傳的（上櫃股 fallback）
    missing = [c for c in codes if c not in results]
    if missing:
        print(f'  fallback otc: {len(missing)}', flush=True)
        for i in range(0, len(missing), 20):
            batch = missing[i:i+20]
            try:
                ch = '|'.join(f'otc_{s}.tw' for s in batch)
                url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ch}'
                r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
                raw = r.json().get('msgArray', [])
                for item in parse(raw):
                    results[item['code']] = item
            except Exception as e:
                print(f'  otc batch {i} err: {e}', flush=True)
            time.sleep(0.3)

    live = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'updated': datetime.now().isoformat(),
        'prices': results,
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(live, f, ensure_ascii=False, indent=2)
    print(f'[done] -> {OUT_PATH} ({len(results)}/{len(codes)})', flush=True)

if __name__ == '__main__':
    main()
