#!/usr/bin/env python3
"""批量抓取台股歷史收盤價，儲存為 research_data/{code}.json"""
import yfinance as yf, json, os, time

DATA_DIR = '/home/ubuntu/investment'
RD = f'{DATA_DIR}/research_data'

def guess_suffix(code):
    # 台股上市 4碼，上櫃也是 4碼，但部分老股有 3碼
    # 簡單 rule：code 開頭 6 通常是上櫃（傳产/金融），但這不準
    # yfinance 對台股通常 .TW 可行，不行再試 .TWO
    return '.TW'

codes = []
for fn in sorted(os.listdir(RD)):
    if fn.endswith('.md'):
        codes.append(fn.replace('.md', ''))

success = 0
fail = 0
for code in codes:
    path = f'{RD}/{code}.json'
    if os.path.exists(path):
        continue
    sfx = guess_suffix(code)
    ticker = code + sfx
    try:
        t = yf.Ticker(ticker)
        h = t.history(period='3mo')
        if not h.empty:
            closes = [round(x, 2) for x in h['Close'].tolist()]
            dates = [d.strftime('%m-%d') for d in h.index]
            obj = {'dates': dates, 'closes': closes, 'last': closes[-1]}
            with open(path, 'w') as f:
                json.dump(obj, f)
            success += 1
        else:
            fail += 1
    except Exception as e:
        fail += 1
    time.sleep(0.15)

print(f'Done. Success={success}, Fail={fail}')
print(f'Total charts: {len([f for f in os.listdir(RD) if f.endswith(".json")])}')
