#!/usr/bin/env python3
"""Roundtable: UI/UX redesign critique."""
from pathlib import Path
import json

report = """# 介面 redesign 會議紀錄
## 角色：UI/UX 設計師、工程師、少年股神、投資大户、普通散户

### 主要批評
- 大廳：表格資訊密度過高，投資人快速決策時反而找不到重點。
- 量化分數不是萬能；對散戶來說「開催理由」和「防守點」更重要。
- 大單代理本科幻指數過高，容易被誤讀為主力進出。
- 漲停基因定義不清，需要明確計算方式，否則只是噪音。

### 具體修正建議
1. 大廳改為卡片式，突出：分級色塊、量化分數、近1日/1週漲跌幅、事件催化。
2. 信號區塊改名為「籌碼與動能」，去除「漲停基因」名詞，改為「強勢籌碼 + 量能異動」雙指標。
3. 新增快速操作列：「加入自選」「一鍵下單區」「防守點提醒」。
4. 深色模式維持，但提升可讀性：增加字級對比、表格懸浮Highlight。
5. 熱力圖從 S4 獨立出來，改為 S6 並加上 1日/1週/1月 Tab 切換（已有前端支援）。
"""
out = Path('/home/ubuntu/investment/ui_redesign_review.md')
out.write_text(report, encoding='utf-8')
print(out)
