#!/usr/bin/env python3
"""掃描 research/*.md，依結構完整度估初版 research_maturity 並回寫 frontmatter。

評分規則（0-100）：
- 基本長度（內文 >3000 字）：25 分；>1500 字：15 分
- 必備段落各 8 分：Driver Chain／一句話結論、Bear/Base/Bull 或情境估值、
  目標價段落、風險與賣出條件、同業比較、Sources 來源
- 有 [unverified] 標記每個 -5（上限 -20）
- 已有 research_maturity 的檔案不覆蓋（--force 可強制）

等級對應 update_dashboard_data.py：
90+ 深度、80+ 可用、60+ 草稿、<60 淺層。

用法：python3 estimate_maturity.py [--force] [--dry-run]
"""
import re
import sys
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
RES = BASE / 'research'

SECTIONS = [
    (re.compile(r'Driver Chain|驅動鏈|一句話結論', re.I), 'driver'),
    (re.compile(r'Bear.*Base.*Bull|情境估值|估值情境|多頭情境', re.I | re.S), 'bbb'),
    (re.compile(r'目標價|目標價與估值', re.I), 'target_sec'),
    (re.compile(r'賣出條件|降級條件|風險與可觀測', re.I), 'sell'),
    (re.compile(r'同業比較|同業財報|競爭比較', re.I), 'peers'),
    (re.compile(r'^##\s*Sources|^##\s*數據來源|來源：', re.I | re.M), 'sources'),
]

def score_text(text: str):
    body = text.split('---', 2)[-1] if text.startswith('---') else text
    chars = len(re.sub(r'\s', '', body))
    s = 0
    if chars > 3000:
        s += 25
    elif chars > 1500:
        s += 15
    for pat, _ in SECTIONS:
        if pat.search(text):
            s += 8
    unverified = len(re.findall(r'\[unverified\]', text, re.I))
    s -= min(20, unverified * 5)
    return max(0, min(100, s)), chars

def write_frontmatter(path: Path, maturity: int) -> bool:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return False
    parts = text.split('---', 2)
    head = parts[1]
    if re.search(r'^research_maturity:', head, re.M):
        return False
    line = f'research_maturity: "{maturity}"'
    new_head = head.rstrip('\n') + '\n' + line + '\n'
    path.write_text('---' + new_head + '---' + parts[2], encoding='utf-8')
    return True

def main():
    force = '--force' in sys.argv
    dry = '--dry-run' in sys.argv
    rows = []
    updated = skipped_existing = low = 0
    for md in sorted(RES.glob('*_*.md')):
        name = md.name
        if name.startswith(('摘要_', '追蹤_')) or name.endswith('.html'):
            continue
        code = name.split('_', 1)[0]
        if not code.isdigit():
            continue
        text = md.read_text(encoding='utf-8')
        has_fm = text.startswith('---')
        existing = re.search(r'^research_maturity:\s*"?(\d+)"?', text, re.M) if has_fm else None
        s, chars = score_text(text)
        if not has_fm:
            # 無 frontmatter 的舊檔：只記錄，不硬塞（需人工決定是否升級格式）
            rows.append((code, name, None, s, chars, '無frontmatter'))
            continue
        if existing and not force:
            skipped_existing += 1
            continue
        if s < 60:
            low += 1
        if not dry:
            write_frontmatter(md, s)
        updated += 1
        rows.append((code, name, int(existing.group(1)) if existing else None, s, chars, 'updated' if not dry else 'dry'))
    print(f'scored: {len(rows)}; updated: {updated}; kept-existing: {skipped_existing}; no-frontmatter: {sum(1 for r in rows if r[5]=="無frontmatter")}; below-60: {low}')
    for code, name, old, s, chars, tag in rows:
        print(f'{tag:>12} {code} {name[:24]:<26} old={old} new={s} chars={chars}')

if __name__ == '__main__':
    main()
