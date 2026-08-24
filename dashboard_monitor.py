#!/usr/bin/env python3
"""Dashboard 週更 monitor：輸出狀態摘要供 cron change-detection 用。

輸出規則（watchdog 模式）：
- 狀態與上次相同 → 安靜（exit 0，無輸出）
- 有變化 → 印出 diff 摘要，觸發 agent 通知

狀態快照存 data/dashboard_state.json。
"""
import json
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
DATA = BASE / 'data.json'
STATE = BASE / 'data' / 'dashboard_state.json'

def snapshot():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    summary = data.get('research_summary', {})
    watch = []
    for s in data.get('stocks', []):
        if s.get('targetStatus') in ('透支', '已達標', '接近', '低估'):
            watch.append({
                'code': s['code'],
                'name': s['name'],
                'targetStatus': s.get('targetStatus'),
                'targetDist': s.get('targetDist'),
                'researchStatus': s.get('researchStatus'),
            })
    return {
        'status_counts': summary.get('status_counts', {}),
        'target_status_counts': summary.get('target_status_counts', {}),
        'watch_list': {w['code']: w for w in watch},
    }

def fmt_changes(old, new):
    lines = []

    def diff_counts(label, o, n):
        keys = set(o) | set(n)
        changed = [(k, o.get(k, 0), n.get(k, 0)) for k in sorted(keys) if o.get(k, 0) != n.get(k, 0)]
        for k, ov, nv in changed:
            sign = '+' if nv > ov else ''
            lines.append(f'- {label}「{k}」：{ov} → {nv}（{sign}{nv - ov}）')

    diff_counts('研究品質', old.get('status_counts', {}), new.get('status_counts', {}))
    diff_counts('目標狀態', old.get('target_status_counts', {}), new.get('target_status_counts', {}))

    ow, nw = old.get('watch_list', {}), new.get('watch_list', {})
    for code in sorted(set(ow) | set(nw)):
        o, n = ow.get(code), nw.get(code)
        if o and not n:
            lines.append(f'- 移出雷達：{code} {o["name"]}（原{o["targetStatus"]}）')
        elif n and not o:
            lines.append(f'- 新進雷達：{code} {n["name"]} → {n["targetStatus"]}（距離{n["targetDist"]:+.1f}%）')
        elif o and n and (o['targetStatus'] != n['targetStatus']):
            lines.append(f'- 狀態變化：{code} {n["name"]} {o["targetStatus"]} → {n["targetStatus"]}（距離{n["targetDist"]:+.1f}%）')
    return lines

def main():
    new = snapshot()
    if STATE.exists():
        old = json.loads(STATE.read_text(encoding='utf-8'))
        changes = fmt_changes(old, new)
        if not changes:
            print('')
            return
        print(f'# Dashboard 狀態變化偵測\n')
        print('\n'.join(changes[:40]))
        if len(changes) > 40:
            print(f'…（共 {len(changes)} 項變化）')
    else:
        print('# Dashboard 監控首次建立基準線')
        t = new.get('target_status_counts', {})
        r = new.get('status_counts', {})
        print(f"- 目標狀態：{t}")
        print(f"- 研究品質：{r}")
        print(f"- 交易雷達：{len(new.get('watch_list', {}))} 檔")
    STATE.write_text(json.dumps(new, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
