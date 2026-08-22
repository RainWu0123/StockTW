#!/usr/bin/env python3
"""追蹤研究目標價達成率。

從 research/*.md 的 frontmatter 抽取 target_base / target_date（缺則標未確認），
比對 data/live.json 現價，輸出：
  1. research/.research_index.json 補上 target 欄位
  2. research/追蹤_目標價達成率_{YYYYMMDD}.md
用法：python3 track_predictions.py [--write-index]
"""
import json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path('/home/ubuntu/investment')
RES = ROOT / 'research'
LIVE = ROOT / 'data' / 'live.json'

def parse_frontmatter(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return {}
    try:
        block = text.split('---', 2)[1]
    except IndexError:
        return {}
    fm = {}
    for line in block.splitlines():
        m = re.match(r'^(\w+):\s*"?([^"#]+?)"?\s*$', line)
        if m:
            fm[m.group(1).strip()] = m.group(2).strip()
    return fm

def main():
    write_index = '--write-index' in sys.argv
    live = json.loads(LIVE.read_text())
    prices = live.get('prices', {})
    today = date.today().strftime('%Y-%m-%d')

    rows = []
    for md in sorted(RES.glob('*_*.md')):
        if md.name.startswith(('摘要_', '追蹤_')) or md.name.endswith('.html'):
            continue
        code = md.name.split('_')[0]
        if not code.isdigit():
            continue
        fm = parse_frontmatter(md)
        target = fm.get('target_base') or fm.get('target')
        lv = fm.get('last_verified', '')
        conf = fm.get('confidence', '')
        p = prices.get(code, {}).get('price')
        if not (target and re.match(r'^[\d.,]+$', target)):
            rows.append((code, md.stem.split('_', 1)[1], None, None, p, lv, conf))
            continue
        t = float(target.replace(',', ''))
        pct = round((p / t - 1) * 100, 1) if p else None
        # 達成判定：現價落在目標價 ±10% 內算「接近」
        status = ('已達標' if p and p >= t else
                  ('接近' if pct is not None and abs(pct) <= 10 else
                   ('落後' if pct is not None else '無報價')))
        rows.append((code, md.stem.split('_', 1)[1], t, status, p, lv, conf))

    tracked = [r for r in rows if r[2] is not None]
    hit = sum(1 for r in tracked if r[3] == '已達標')
    near = sum(1 for r in tracked if r[3] == '接近')

    lines = [
        f'# 目標價追蹤表 {today}',
        '',
        f'- 追蹤檔數：{len(rows)}；有明確 target_base：{len(tracked)}',
        f'- 已達標：{hit}；接近（±10%內）：{near}',
        '- 判定基準：現價 >= Base 目標價為已達標；距離 ±10% 內為接近。資料來源 data/live.json（收盤）。',
        '',
        '| 代碼 | 名稱 | Base目標價 | 現價 | 距離% | 判定 | last_verified | confidence |',
        '|---|---|---:|---:|---:|---|---|---|',
    ]
    for code, name, t, status, p, lv, conf in rows:
        t_s = f'{t:g}' if t else '未確認'
        pct_s = ''
        if t and p:
            pct_s = f'{round((p/t-1)*100,1):+g}%'
        elif t:
            pct_s = '—'
        lines.append(f'| {code} | {name} | {t_s} | {p if p else "—"} | {pct_s} | {status if t else "—"} | {lv or "—"} | {conf or "—"} |')

    out = RES / f'追蹤_目標價達成率_{date.today().strftime("%Y%m%d")}.md'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'written: {out}; tracked={len(tracked)}/{len(rows)}; hit={hit}; near={near}')

    if write_index:
        idx_path = RES / '.research_index.json'
        idx = json.loads(idx_path.read_text())
        by_code = {s['code']: s for s in idx['stocks']}
        for code, name, t, *_ in rows:
            if t and code in by_code:
                by_code[code]['target_base'] = t
                by_code[code]['tracked_at'] = today
        idx['stocks'] = list(by_code.values())
        idx['generated'] = today
        idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n')
        print(f'index updated with targets for {sum(1 for c,n,t,*_ in rows if t and c in by_code)} stocks')

if __name__ == '__main__':
    main()
