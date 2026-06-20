#!/usr/bin/env python3
"""Rebuild heatmap as industry-based, rebuild etf.json."""
import json
from collections import defaultdict
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
d = json.load(open(BASE / 'data.json', 'r', encoding='utf-8'))
stocks = d['stocks']

def guess_sector(name):
    if any(k in name for k in ['台積','聯電','聯發','日月光','台光','力積']): return 'IC/代工/封測'
    if any(k in name for k in ['國巨','凱美','信昌']): return '被動元件'
    if any(k in name for k in ['奇鋐','雙鴻','緯創','廣達','台達','金寶']): return 'AI/散熱/伺服器'
    if any(k in name for k in ['華邦','南亞']): return 'DRAM'
    if any(k in name for k in ['鴻海','研揚','金寶']): return 'ODM/EMS'
    if any(k in name for k in ['大立光']): return '光學'
    if any(k in name for k in ['啟','華']): return '網通'
    if any(k in name for k in ['漢唐','達']): return '設備'
    return '其他'

# 1) Industry heatmap (industry name + avg pct + count)
groups = defaultdict(list)
for s in stocks:
    groups[guess_sector(s['name'])].append(s)

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
with open(BASE / 'data' / 'heatmap.json', 'w', encoding='utf-8') as f:
    json.dump(heat, f, ensure_ascii=False, indent=2)
print(f'heatmap industries: {len(rows)}')

# 2) etf/peers/concepts
etf_map = {
    '0050': ['2330','2317','2454','2303','2881','2882','1303','2002','1301','2412'],
    '00981A': ['2330','2454','2303','3711','3038','6770','3443','6505','2382','3005'],
    '00991A': ['2330','2454','2345','3038','6770','3711','3443','3529','5269','2404'],
    '00988A': ['2330','2881','2317','2454','2882','2308','6505','1216','1101','2002']
}
concepts, peers = {}, {}
for s in stocks:
    c = s.get('concepts') or []
    if not c:
        n = s['name']
        if any(k in n for k in ['台積','聯電','聯發']): c.append('IC設計/製造')
        if any(k in n for k in ['國巨','凱美']): c.append('被動元件')
        if any(k in n for k in ['奇鋐','雙鴻','緯創','廣達','台達']): c.append('AI/散熱/伺服器')
        if any(k in n for k in ['華邦','南亞']): c.append('DRAM')
        if any(k in n for k in ['鴻海','研揚','金寶']): c.append('ODM/EMS')
        if s.get('in_ai_etf'): c.append('AI ETF')
    concepts[s['code']] = c
    ind = guess_sector(s['name'])
    peers[s['code']] = [x['code'] for x in stocks if guess_sector(x['name']) == ind and x['code'] != s['code']][:10]

with open(BASE / 'data' / 'etf.json', 'w', encoding='utf-8') as f:
    json.dump({'etfs': etf_map, 'concepts': concepts, 'peers': peers}, f, ensure_ascii=False, indent=2)
print('etf/peers built')
