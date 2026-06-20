#!/usr/bin/env python3
"""Rebuild snapshot_<date>.json from data.json + heatmap.json so scoring has real inputs."""
import json, os
from datetime import datetime
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
DATA = BASE / 'data.json'
HEAT = BASE / 'data' / 'heatmap.json'
TODAY = datetime.now().strftime('%Y-%m-%d')
OUT = BASE / 'data' / f'snapshot_{TODAY}.json'

data = json.loads(DATA.read_text(encoding='utf-8'))
heat = {s['code']: s for s in json.loads(HEAT.read_text(encoding='utf-8')).get('stocks', [])}

vols = [s.get('vol', 0) or 0 for s in data['stocks']]
avg_vol = sum(vols) / max(len(vols), 1)
n = len(data['stocks']) or 1

stocks = []
for s in data['stocks']:
    code = s['code']
    vol = s.get('vol') or 0
    price = s.get('price') or 0
    rec = {
        'code': code,
        'name': s.get('name', code),
        'price': price,
        'pct': s.get('pct') or 0.0,
        'vol': vol,
        'tx': 0,
        'vol_ratio_5d': vol / avg_vol if avg_vol else 1.0,
        'limit_up_flag': bool((s.get('pct') or 0) >= 9.5),
        'in_ai_etf': bool(s.get('in_ai_etf') or any(code in etf for etf in [['2327','2383','2344','2408','2308','3017','3711','6166','6442','2375','2454','2303']])),
        'theme_score': s.get('theme_score', 1),
        'revenue_yoy': None,
        'foreign_net_days': 0,
        'dealer_net_days': 0,
        'dist_52w_high': 0,
    }
    stocks.append(rec)

snap = {
    'date': TODAY,
    'updated': datetime.now().isoformat(),
    'stocks': stocks,
    'meta': {
        'fields': {
            'revenue_yoy': '待補',
            'foreign_net_days': '待補',
            'dealer_net_days': '待補',
            'dist_52w_high': '待補'
        },
        'note': 'snapshot rebuilt from data.json + heatmap.json for scoring stability.'
    }
}
OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'[rebuild] {len(stocks)} stocks -> {OUT}')
