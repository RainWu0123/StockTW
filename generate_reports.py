#!/usr/bin/env python3
"""Generate equity research reports for all tracked stocks."""
import json, os, time
from datetime import datetime

BASE = "/home/ubuntu/investment"
RESEARCH_DIR = os.path.join(BASE, "research")
os.makedirs(RESEARCH_DIR, exist_ok=True)

def load_data():
    p = os.path.join(BASE, "data.json")
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d.get("stocks", [])

REPORT_TMPL = """# {name} ({code}) 深度研究報告

**報告日期**: {date}
**研究員**: 法人研究員 SubAgent
**來源**: Hermes 自動化研究流程

---

## 1. 量化追蹤數據
| 指標 | 數值 |
|------|------|
| 收盤價 | {price} |
| 漲跌幅 | {pct}% |
| 成交張數 | {vol:,} |
| 分級 | {tier} |
| 量化評分 | {score} |
| ETF 追蹤標記 | {etf} |

## 2. 系統備註
{note}

## 3. 研究說明
本報告由 Hermes 法人研究員 SubAgent 自動產出。完整版（含營收能見度、法人買賣超、技術圖表、同業比較、目標價）將於下一版本全面上線。

---

*本報告僅供內部研究參考，不構成投資建議。*
"""

def gen(stocks):
    done = 0
    for s in stocks:
        code = s.get("code", "")
        name = s.get("name", code)
        if not code:
            continue
        safe_name = name.replace("/", "_").replace(" ", "_")
        fname = f"{code}_{safe_name}.md"
        path = os.path.join(RESEARCH_DIR, fname)
        if os.path.exists(path):
            continue
        body = REPORT_TMPL.format(
            name=name,
            code=code,
            date=datetime.now().strftime("%Y-%m-%d"),
            price=s.get("price", "--"),
            pct=s.get("pct", "--"),
            vol=s.get("vol", 0),
            tier=s.get("tier", "T4"),
            score=s.get("score", "--"),
            etf=", ".join(s.get("etf_tags", [])) or "無",
            note=s.get("note", "無系統備註"),
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        done += 1
        time.sleep(0.05)
    return done

if __name__ == "__main__":
    stocks = load_data()
    priority = [s for s in stocks if s.get("tier") in ("T1","T2")]
    others = [s for s in stocks if s.get("tier") not in ("T1","T2")]
    d1 = gen(priority)
    d2 = gen(others)
    print(f"[research] generated {d1+d2} reports ({d1} priority, {d2} others)")
