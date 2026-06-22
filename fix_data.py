#!/usr/bin/env python3
"""修復 data.json：(1) 補齊 name==code 的缺漏名稱 (2) 去重複 code"""
import json, urllib.request, time

DATA_DIR = '/home/ubuntu/investment'
JSON_PATH = f'{DATA_DIR}/data.json'

with open(JSON_PATH) as f:
    data = json.load(f)

stocks = data.get('stocks', [])

# 1) 收集需要補名稱的
need_fix = []
for i, s in enumerate(stocks):
    c = s.get('code', '')
    n = s.get('name', '')
    if n == c and c:
        need_fix.append((i, c))

print(f'Need fix names: {len(need_fix)}')

BATCH = 20
fixed = 0
for i in range(0, len(need_fix), BATCH):
    batch_codes = [c for _, c in need_fix[i:i+BATCH]]
    ch = '|'.join(f'tse_{c}.tw' for c in batch_codes)
    url = f'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={ch}&json=1'
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        mapping = {}
        for m in d.get('msgArray', []):
            c = str(m.get('c', ''))
            n = m.get('n', '') or m.get('nf', '')
            if c and n:
                mapping[c] = n
        for idx, code in need_fix[i:i+BATCH]:
            if code in mapping:
                stocks[idx]['name'] = mapping[code]
                print(f'  {code} -> {mapping[code]}')
                fixed += 1
    except Exception as e:
        print(f'Batch {i} error:', e)
    if i + BATCH < len(need_fix):
        time.sleep(0.3)

print(f'Fixed {fixed}/{len(need_fix)} names')

# 2) 去重複：保留 2383 T1（score 較高），刪 T2
seen = {}
deduped = []
for s in stocks:
    c = s.get('code', '')
    if c == '2383':
        if c not in seen:
            seen[c] = s
            deduped.append(s)
        else:
            tier = s.get('tier','')
            print(f'  Deduped 2383 (tier={tier})')
    else:
        if c not in seen:
            seen[c] = True
            deduped.append(s)
        else:
            print(f'  Deduped {c}')

print(f'After dedup: {len(deduped)} stocks')
data['stocks'] = deduped

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('data.json saved')
