#!/usr/bin/env python3
"""更新 data.json 的價格與研究目標價（輕量版：不重跑評分，只同步最新收盤與 target/theme）。"""
import json, re, glob, datetime
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
data = json.loads((BASE/'data.json').read_text(encoding='utf-8'))
live = json.loads((BASE/'data'/'live.json').read_text(encoding='utf-8'))
prices = live.get('prices', {})

# 從 research frontmatter 抽 target_base / theme
research_map = {}
for f in glob.glob(str(BASE/'research'/'*_*.md')):
    name = Path(f).name
    if name.startswith(('摘要_','追蹤_')) or name.endswith('.html'): continue
    code = name.split('_')[0]
    if not code.isdigit(): continue
    text = open(f, encoding='utf-8').read()
    if not text.startswith('---'): continue
    head = text.split('---',2)[1]
    tb = re.search(r'target_base:\s*"?([\d.,]+)"?', head)
    th = re.search(r'theme:\s*"?([^"\n]+)"?', head)
    lv = re.search(r'last_verified:\s*"?([\d-]+)"?', head)
    if tb:
        research_map[code] = {
            'target': float(tb.group(1).replace(',','')),
            'theme': th.group(1) if th else '',
            'last_verified': lv.group(1) if lv else '',
            'file': name,
        }

updated_prices = 0
for s in data['stocks']:
    c = s['code']
    p = prices.get(c)
    if p and p.get('price'):
        s['price'] = p['price']; s['pct'] = p.get('pct'); s['vol'] = p.get('vol')
        updated_prices += 1
    r = research_map.get(c)
    if r:
        s['target'] = r['target']
        # 距離%
        try: s['targetDist'] = round((s['price']/r['target'] - 1)*100, 1)
        except: s['targetDist'] = None
        s['researchTheme'] = r['theme']
        s['researchFile'] = 'research/'+r['file']
        s['lastVerified'] = r['last_verified']

data['updated'] = datetime.datetime.now().isoformat()
(BASE/'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"prices updated: {updated_prices}; targets mapped: {len(research_map)}")
