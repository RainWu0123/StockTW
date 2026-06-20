#!/usr/bin/env python3
"""Patch footer history into render_dashboard.py as an extra endpoint."""

from pathlib import Path
p = Path("/home/ubuntu/investment/render_dashboard.py")
code = p.read_text(encoding="utf-8")
marker = "if __name__ == \"__main__\":\n    main()\n"
insert = '''def write_footer_history():
    base = Path("/home/ubuntu/investment")
    payload = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "items": [
            {"date":"2026-06-20","summary":"量化分數合併至 data.json；熱力圖（1週/1月）上線。"},
            {"date":"2026-06-20","summary":"量化 scoring engine 重建並產出 scores.json。"},
            {"date":"2026-06-19","summary":"重建 GitHub repo，只保留前端部署檔案，清除analysis docs。"},
        ],
    }
    (base/"footer_history.json").write_text(
        __import__("json").dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("[footer_history.json] written")

'''
if insert in code:
    raise SystemExit("already patched")
assert marker in code, "marker missing"
code = code.replace(marker, insert + marker)
p.write_text(code, encoding="utf-8")
print("patched render_dashboard.py")
