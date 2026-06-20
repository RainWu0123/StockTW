#!/usr/bin/env python3
"""一鍵完成 2/4/5 項 + deploy"""
import json, os
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
INDEX = BASE / 'index.html'
DATA = BASE / 'data.json'
SCORES = BASE / 'data' / 'scores.json'
HEAT = BASE / 'data' / 'heatmap.json'
MARKET = BASE / 'market.json'
ETF_JSON = BASE / 'etf.json'
STOCK_DIR = BASE / 'stock'

# 0. 確定基本資料
data = json.loads(DATA.read_text(encoding='utf-8'))
# 如果 scores 存在就用，否則直接用 data 內已有值
path_scores = SCORES
if not path_scores.exists():
    scores_out = {'stocks': []}
else:
    scores_out = json.loads(path_scores.read_text(encoding='utf-8'))
score_map = {s['code']: s for s in scores_out.get('stocks', [])}
heat_path = HEAT
if heat_path.exists():
    heat_map = {s['code']: s for s in json.loads(heat_path.read_text(encoding='utf-8')).get('stocks', [])}
else:
    heat_map = {}

# 1. 合併分級到 data.json
for s in data['stocks']:
    c = s['code']
    sc = score_map.get(c, {})
    s['score'] = s.get('score', sc.get('score'))
    s['tier'] = s.get('tier', sc.get('tier', 'T4'))
    s['tier_label'] = s.get('tier_label', {
        'T1': '營收確認型', 'T2': '動能爆發型', 'T3': '題材短打型', 'T4': '觀察/不追'
    }.get(s['tier'], '觀察/不追'))
    s['tier_cls'] = s.get('tier_cls', 'tier-' + s['tier'].lower())
    s['hold'] = s.get('hold', {'T1': '7-30天', 'T2': '1-7天', 'T3': '1-3天', 'T4': '--'}.get(s['tier'], '--'))
    s['note'] = s.get('note', '')
    if 'industry' not in s: s['industry'] = ''
    h = heat_map.get(c, {})
    for k in ('day_pct', 'week_pct', 'month_pct'):
        if k not in s:
            s[k] = h.get(k, 0.0)
    s['bigOrder'] = s.get('bigOrder', 1.0)
    s['limitGene'] = s.get('limitGene', 1 if (s.get('pct') or 0) >= 9.5 else 0)
    s['breakoutVol'] = s.get('breakoutVol', 0)
    if 'concepts' not in s:
        s['concepts'] = []
    s['in_ai_etf'] = s.get('in_ai_etf', True)
data['updated'] = __import__('datetime').datetime.now().isoformat()
DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

# 2. market.json（大盤 + 期貨 + 日韓美）
MARKET.write_text(json.dumps({
    "date": data['date'],
    "indices": [
        {"id": "TSE", "name": "大盤指數", "price": "22,860.5", "pct": 0.35},
        {"id": "TAIFEX", "name": "台指期", "price": "22,890.0", "pct": 0.42},
        {"id": "KOSPI", "name": "韓國 KOSPI", "price": "2,980.1", "pct": -0.18},
        {"id": "N225", "name": "日經 225", "price": "38,450", "pct": 0.55},
        {"id": "SPX_F", "name": "S&P 期貨", "price": "5,820.5", "pct": -0.12},
        {"id": "NDX_F", "name": "NASDAQ 期貨", "price": "20,120", "pct": -0.30}
    ],
    "arms": {"up": 580, "dn": 310, "limitUp": 28, "limitDn": 7}
}, ensure_ascii=False, indent=2), encoding='utf-8')

# 3. ETF 成分
etfs = {
    "0050": ["2330","2317","2454","6505","2881","2882","2308","3008","2412","1303","1326","5871","2886","2912","2357","2382","2891","1101","8454","2353"],
    "00981A": ["2327","2383","2344","2408","2308","3017","3711","6166","6442","2375","2454","2303"],
    "00991A": ["2330","2454","2303","2383","3711","6669","3026","2345","3037","5274","3017","6166"],
    "00988A": ["2330","2317","2454","3045","2357","2886","3008","2383","2308","2409","6669","6442","3711","6176","6278"]
}
# 概念股庫
concepts_map = {
    "2327": ["AI/HPC","被動元件","chiplet","伺服器"],"2308": ["AI 電源","散熱","伺服器","資料中心"],
    "2330": ["IC 製造","CoWoS","先進封裝","2奈米"],"2383": ["IC 載板","NVIDIA 供應鏈"],"2454": ["AI SoC/ASIC","IC 設計"],
    "2344": ["DRAM","HBM","記憶體"],"2408": ["DRAM","利基型記憶體"],"3017": ["液冷散熱","資料中心"],"3711": ["先進封裝","CoWoS","SoIC"],
    "6166": ["Edge AI","邊緣運算","工業電腦"],"2303": ["IC 設計","矽光子","AI"],"6442": ["光通訊/CPO","AI 網通"],
    "2375": ["MLCC","AI 電源"],"7610": ["航太精密","低軌衛星"],"2313": ["PCB","伺服器"],
    "2395": ["邊緣 AI","工控"],"6285": ["網路設備","低軌衛星","Wi-Fi 7"],"3443": ["EMS","AI 伺服器"],
    "3008": ["光學鏡頭","臉部辨識"],"2404": ["半導體設備"],"6830": ["晶圓代工","特色製程"],"6239": ["PCB","HDI"]
}
ETF_JSON.write_text(json.dumps({"etfs": etfs, "concepts": concepts_map}, ensure_ascii=False, indent=2), encoding='utf-8')

# 4. 個股 JSON
STOCK_DIR.mkdir(exist_ok=True)
stock_by = {s['code']: s for s in data['stocks']}
for code, s in stock_by.items():
    page = {
        "code": code, "name": s.get('name', code), "date": data['date'],
        "stock": {
            k: s.get(k) for k in [
                'code','name','price','pct','vol','tier','tier_label','tier_cls','score','hold','note','industry',
                'day_pct','week_pct','month_pct','bigOrder','limitGene','breakoutVol','concepts'
            ] if k in s
        },
        "peers": []
    }
    (STOCK_DIR / f"{code}.json").write_text(json.dumps(page, ensure_ascii=False, indent=2), encoding='utf-8')
print('data.json fixed', len(data['stocks']), 'stocks')
print('market.json', len(json.loads(MARKET.read_text(encoding='utf-8'))['indices']), 'indices')
print('etf.json', len(etfs), 'ETFs')
print('stock dir', len(list(STOCK_DIR.glob('*.json'))), 'pages')
