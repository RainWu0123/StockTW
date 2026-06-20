#!/usr/bin/env python3
"""Fix heatmap to industry-based, rebuild etf.json, verify data.json."""
import json
from collections import defaultdict
from pathlib import Path

BASE = Path('/home/ubuntu/investment')

# 1. Industry heatmap from data.json stock list
d = json.load(open(BASE / 'data.json', 'r', encoding='utf-8'))
stocks = d['stocks']

# industry mapping by name (since industry field is empty)
def guess_sector(name):
    if any(k in name for k in ['台積','聯電','聯發','日月光','台光','力積']): return 'IC/代工/封測'
    if any(k in name for k in ['國巨','凱美','信昌']): return '被動元件'
    if any(k in name for k in ['奇鋐','雙鴻','緯創','廣達','台達','金寶']): return 'AI/散熱/伺服器'
    if any(k in name for k in ['華邦','南亞']): return 'DRAM'
    if any(k in name for k in ['鴻海','研揚','寶','緯創']): return 'ODM/EMS'
    if any(k in name for k in ['大立光']): return '光學'
    if any(k in name for k in ['啟','華']): return '網通'
    if any(k in name for k in ['漢唐','達']): return '設備/散熱'
    return '其他'

groups = defaultdict(list)
for s in stocks:
    ind = s.get('industry') or guess_sector(s['name'])
    groups[ind].append(s)

rows = []
for ind, arr in groups.items():
    avg = sum((x.get('pct', 0) or 0) for x in arr) / len(arr)
    up = sum(1 for x in arr if (x.get('pct', 0) or 0) > 0)
    dn = sum(1 for x in arr if (x.get('pct', 0) or 0) < 0)
    rows.append({
        'industry': ind,
        'avg_pct': round(avg, 2),
        'up': up,
        'down': dn,
        'total': len(arr),
        'codes': ','.join(x['code'] for x in arr)
    })

rows.sort(key=lambda x: -x['avg_pct'])
heat = {'date': d['date'], 'generated': '2026-06-20', 'industries': rows}
json.dump(heat, open(BASE / 'data' / 'heatmap.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'heatmap: {len(rows)} industries')

# 2. etf.json with demo constituents (replace with real later)
etf_map = {
    '0050': ['2330', '2317', '2454', '2303', '2881', '2882', '1303', '2002', '1301', '2412'],
    '00981A': ['2330', '2454', '2303', '3711', '3038', '6770', '3443', '6505', '2382', '3005'],
    '00991A': ['2330', '2454', '2345', '3038', '6770', '3711', '3443', '3529', '5269', '2404'],
    '00988A': ['2330', '2881', '2317', '2454', '2882', '2308', '6505', '1216', '1101', '2002']
}
concepts = {}
peers = {}
for s in stocks:
    code = s['code']
    # concepts from name guess + AI ETF flag
    c = s.get('concepts') or []
    if not c:
        n = s['name']
        if any(k in n for k in ['台積','聯電','聯發']): c.append('IC設計/製造')
        if any(k in n for k in ['國巨','凱美']): c.append('被動元件')
        if any(k in n for k in ['奇鋐','雙鴻','緯創','廣達','台達']): c.append('AI/散熱/伺服器')
        if any(k in n for k in ['華邦','南亞']): c.append('DRAM')
        if any(k in n for k in ['鴻海','研揚','金寶']): c.append('ODM/EMS')
        if s.get('in_ai_etf'): c.append('AI ETF')
    concepts[code] = c
    # peers by industry
    ind = s.get('industry') or guess_sector(s['name'])
    peers[code] = [x['code'] for x in stocks if ind == (x.get('industry') or guess_sector(x['name'])) and x['code'] != code][:10]

json.dump({'etfs': etf_map, 'concepts': concepts, 'peers': peers},
          open(BASE / 'data' / 'etf.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('etf/peers built')

# 3. Verify data.json structure
print('tiers:', {t: sum(1 for s in stocks if s.get('tier') == t) for t in ['T1', 'T2', 'T3', 'T4']})
print('sample stock keys:', list(stocks[0].keys())[:15])
