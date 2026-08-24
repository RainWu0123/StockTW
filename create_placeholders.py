#!/usr/bin/env python3
"""為 data.json 有、research/ 無檔的股票補建研究佔位檔（status: watch）。"""
import json
from pathlib import Path

ROOT = Path('/home/ubuntu/investment')
RES = ROOT / 'research'
data = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))
have = {p.name.split('_', 1)[0] for p in RES.glob('*_*.md') if p.name.split('_', 1)[0].isdigit()}
missing = [(s['code'], s['name']) for s in data['stocks'] if s['code'] not in have]
TEMPLATE = '''---
code: "{code}"
name: "{name}"
last_verified: ""
confidence: "低"
horizon: "12M"
status: "watch"
sources_as_of: ""
theme: "未分類"
target_base: ""
research_maturity: "10"
---

# {name} ({code}) 研究佔位檔

> 狀態：watch。本檔是儀表板覆蓋率佔位，不是研究。尚未做任何查證，無目標價、無情境估值。

## 為什麼存在

data.json 有這檔（價格追蹤用），但 research/ 尚無對應深度研究。補上正式研究前，決策雷達會把它列為「淺層」，避免誤當已驗證標的。

## 待辦（升級條件）

1. 查公司主業、營收結構、最新財報。
2. 判斷是否值得進入追蹤清單；不值得就從 data.json 移除。
3. 依 guides/research-report-template.md 重寫本檔。

*內部研究備忘，不構成投資建議。*
'''
created = 0
for code, name in missing:
    p = RES / f'{code}_{name}.md'
    if p.exists():
        continue
    p.write_text(TEMPLATE.format(code=code, name=name), encoding='utf-8')
    created += 1
    print('created', p.name)
print('total created:', created)
