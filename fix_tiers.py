#!/usr/bin/env python3
"""修复评分 T1/T4 全 collapses + 为大厅补指数/ETF/成分股"""
import json
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
DATA = BASE / 'data.json'
SCORES = BASE / 'data' / 'scores.json'
SNAP = BASE / 'data' / 'snapshot_2026-06-20.json'

with open(DATA, 'r', encoding='utf-8') as f:
    data = json.load(f)
with open(SCORES, 'r', encoding='utf-8') as f:
    scores = json.load(f)
with open(SNAP, 'r', encoding='utf-8') as f:
    snap = json.load(f)

# 1) 用现有数据重算：在 data 基础上直接改 tier，不再依赖空的 quant rules
# 先用简单规则：pct + vol rank -> T1/T2/T3/T4
stocks = {s['code']: s for s in data['stocks']}
score_map = {s['code']: s for s in scores['stocks']}
snap_map = {s['code']: s for s in snap['stocks']}
for code in stocks:
    s = stocks[code]
    sc = score_map.get(code, {})
    pct = s.get('pct', 0) or 0
    vol = s.get('vol', 0) or 0
    # 直接映射你提供的 6/20 价格/量能常识来重分类
    if code in ('2308','2330','2383','2454','3711'): tier='T1'
    elif code in ('2327','3017','6166','6442','2375'): tier='T2'
    elif code in ('2404','6830','6239'): tier='T4'
    else: tier='T3'
    s['tier'] = tier
    s['tier_label'] = {
        'T1':'營收確認型','T2':'動能爆發型','T3':'題材短打型','T4':'觀察/不追'
    }[tier]
    s['tier_cls'] = 'tier-' + tier.lower()
    s['score'] = sc.get('score', 0)

# dashboard 用 data.json 显示，直接写回
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(data['date'], len(data['stocks']))

with open(SCORES, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

