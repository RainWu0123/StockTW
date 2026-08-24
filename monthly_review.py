#!/usr/bin/env python3
"""月度研究復盤：從 research frontmatter + data.json 產出判斷覆盤報告。

輸出 research/追蹤_月度復盤_{YYYYMMDD}.md，內容：
1. 已達標/透支清單（含「已透支」警示）
2. 低估清單（現價低於 Base 30%+）
3. 研究健康度統計（過期、淺層、無目標價）
4. 需要人工決策的邊界案例

用法：python3 monthly_review.py [--open]   # --open 只列出，不寫檔
"""
import json
import re
import datetime as dt
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
DATA = BASE / 'data.json'
RES = BASE / 'research'
TODAY = dt.date.today()
STALE_DAYS = 30

def main():
    open_only = '--open' in sys.argv if (sys := __import__('sys')) else False
    data = json.loads(DATA.read_text(encoding='utf-8'))
    stocks = data.get('stocks', [])

    hit, over, low, near = [], [], [], []
    stale, shallow, no_target = [], [], []
    for s in stocks:
        row = {
            'code': s['code'], 'name': s['name'],
            'price': s.get('price'), 'target': s.get('target'),
            'dist': s.get('targetDist'), 'status': s.get('targetStatus'),
            'research': s.get('researchStatus'), 'maturity': s.get('researchMaturity'),
            'verified': s.get('lastVerified') or '—',
            'confidence': s.get('confidence', ''), 'file': s.get('researchFile', ''),
        }
        ts, rs = s.get('targetStatus'), s.get('researchStatus')
        if ts == '已達標':
            hit.append(row)
        elif ts == '透支':
            over.append(row)
        elif ts == '低估':
            low.append(row)
        elif ts == '接近':
            near.append(row)
        if rs == '需重驗':
            stale.append(row)
        if rs in ('淺層', '未驗證'):
            shallow.append(row)
        if not s.get('target'):
            no_target.append(row)

    def table(rows):
        head = '| 代碼 | 名稱 | 現價 | Base | 距離% | 研究 | maturity | last_verified |'
        sep = '|---|---|---:|---:|---:|---|---:|---|'
        lines = [head, sep]
        for r in sorted(rows, key=lambda x: x['dist'] if x['dist'] is not None else 999):
            lines.append(f"| {r['code']} | {r['name']} | {r['price'] or '—'} | {r['target'] or '—'} | "
                         f"{f'{r[chr(100)+chr(105)+chr(115)+chr(116)]:+g}' if r['dist'] is not None else '—'} | "
                         f"{r['research'] or '—'} | {r['maturity'] or '—'} | {r['verified']} |")
        return '\n'.join(lines)

    lines = [
        f'# 月度研究復盤 {TODAY.isoformat()}', '',
        f'> 自動產生自 data.json 與 research frontmatter。判定基準：現價 >= Base 為已達標；超過 Base 20% 為透支；低於 Base 30% 以上為低估。資料截止 {str(data.get("updated",""))[:10]}。', '',
        '## 一、已達標（現價 >= Base 目標價）', '',
        '**注意：已達標不等於該買。要問的是「漲的原因和 thesis 一致嗎？」不一致就是復盤重點。**', '',
        table(hit) if hit else '（無）', '',
        '## 二、已透支（現價超過 Base 20% 以上）', '',
        '**這些代表市場比我們的模型樂觀很多。選擇：上修 thesis（要有新證據）、維持並記錄分歧、或降級追蹤。**', '',
        table(over) if over else '（無）', '',
        '## 三、低估（現價低於 Base 30% 以上）', '',
        '**先檢查三件事再興奮：① thesis 是否還成立 ② 賣出條件是否已觸發沒更新 ③ 目標價是不是批量導入時的舊數字。**', '',
        table(low) if low else '（無）', '',
        '## 四、接近達標（±10%）', '',
        table(near) if near else '（無）', '',
        '## 五、研究健康度', '',
        f'- 需重驗（last_verified 超 {STALE_DAYS} 天）：{len(stale)} 檔',
        f'- 淺層／未驗證研究：{len(shallow)} 檔',
        f'- 無 Base 目標價：{len(no_target)} 檔', '',
    ]
    if stale:
        lines += ['### 需重驗清單', '', table(stale), '']
    if no_target:
        lines += ['### 無目標價清單', '', ', '.join(f"{r['code']} {r['name']}" for r in no_target), '']

    lines += [
        '## 六、本月的復盤問題（下次更新時逐項回答）', '',
        '- 哪些判斷對了？原因和預期一致嗎？',
        '- 哪些漲到了但原因是別的？（運氣不是能力）',
        '- 哪些沒漲但 thesis 沒壞？（耐心 vs 執著的分界）',
        '- 哪些該降級或移出追蹤？',
        '- 上個月列的待辦做了嗎？', '',
        '*內部研究備忘，不構成投資建議。*',
    ]

    report = '\n'.join(lines) + '\n'
    out = RES / f'追蹤_月度復盤_{TODAY.strftime("%Y%m%d")}.md'
    if open_only:
        print(report)
        return
    out.write_text(report, encoding='utf-8')
    print(f'written: {out}')
    print(f'hit={len(hit)} over={len(over)} low={len(low)} near={len(near)} stale={len(stale)} shallow={len(shallow)} no_target={len(no_target)}')

if __name__ == '__main__':
    main()
