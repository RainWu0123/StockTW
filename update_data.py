#!/usr/bin/env python3
"""即時更新 data.json 的價格欄位（避開 CORS）"""
import json, os, requests, time
from datetime import datetime

BASE = '/home/ubuntu/investment'

def fetch_live():
    # 讀現有 data.json
    dj = os.path.join(BASE, 'data.json')
    with open(dj, encoding='utf-8') as f:
        data = json.load(f)
    stocks = data.get('stocks', [])
    codes = [s['code'] for s in stocks]

    price_map = {}
    for i in range(0, len(codes), 20):
        batch = codes[i:i+20]
        ch = '|'.join(f'tse_{c}.tw' for c in batch)
        url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ch}'
        try:
            r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
            for item in r.json().get('msgArray', []):
                code = item.get('c', '')
                if not code:
                    continue
                z = item.get('z', item.get('o', 0))
                y = item.get('y', 0)
                v = item.get('v', 0)
                try:
                    price = float(z or 0)
                    ref = float(y or 0)
                    pct = ((price - ref) / ref * 100) if ref else 0.0
                    vol = int(v or 0)
                    price_map[code] = {'price': round(price, 2), 'pct': round(pct, 2), 'vol': vol}
                except:
                    pass
        except Exception as e:
            print(f'  batch {i} err: {e}')
        if i + 20 < len(codes):
            time.sleep(0.3)

    # 上櫃 fallback
    missing = [c for c in codes if c not in price_map]
    if missing:
        for i in range(0, len(missing), 20):
            batch = missing[i:i+20]
            ch = '|'.join(f'otc_{c}.tw' for c in batch)
            url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ch}'
            try:
                r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
                for item in r.json().get('msgArray', []):
                    code = item.get('c', '')
                    if not code:
                        continue
                    z = item.get('z', item.get('o', 0))
                    y = item.get('y', 0)
                    v = item.get('v', 0)
                    try:
                        price = float(z or 0)
                        ref = float(y or 0)
                        pct = ((price - ref) / ref * 100) if ref else 0.0
                        vol = int(v or 0)
                        price_map[code] = {'price': round(price, 2), 'pct': round(pct, 2), 'vol': vol}
                    except:
                        pass
            except Exception as e:
                print(f'  otc batch {i} err: {e}')
            time.sleep(0.3)

    # 更新 stocks
    updated = 0
    for s in stocks:
        c = s['code']
        if c in price_map:
            pm = price_map[c]
            s['price'] = pm['price']
            s['pct'] = pm['pct']
            s['vol'] = pm['vol']
            updated += 1

    data['date'] = datetime.now().strftime('%Y-%m-%d')
    data['updated'] = datetime.now().isoformat()

    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'[update_data] {datetime.now().strftime("%H:%M:%S")} updated {updated}/{len(stocks)}', flush=True)
    return updated

if __name__ == '__main__':
    fetch_live()
