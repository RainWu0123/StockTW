# Investment Workspace — AGENTS.md

## 專案概述
台股研究與儀表板系統。包含個股深度研究、即時數據、排名評分、GitHub Pages 發布。

## 先讀
- **總索引（引用地圖）**：`/home/ubuntu/investment/INDEX.md`
- **股癌校準（寫 AI／硬體／被動／功率／光通／記憶體個股前）**：
  - **Skill（優先）**：`gooaye-perspective`（`skill_view` 載入）
  - AI JSON：`research/gooaye_digest.json`
  - 人讀：`research/摘要_股癌消化筆記_20260714.md`
- 本檔：工作規範與 pipeline

## 目錄結構
- `INDEX.md` — 全庫引用入口（散落來源地圖 + research 清單）
- `research/` — 個股／專題深度研究，**唯一寫入落點**
  - 個股：`{代碼}_{名稱}.md`（例：`2330_台積電.md`）
  - 專題：`摘要_{主題}_{YYYYMMDD}.md`
- `data/` — JSON 資料檔（etf.json, live.json, scores.json, heatmap.json 等）
- `stock/` — 個股原始資料（每檔一個 JSON，代碼為檔名）
- `archive/` — 歷史／散檔歸檔（discord、roundtable、legacy、notes）；只讀為主
- `meta/` — 元資料預留
- `index.html` / `spa.html` — 儀表板前端
- `*.py` — 資料抓取、評分、建站腳本
- `deploy_pages.sh` — GitHub Pages 部署腳本

## 旁系路徑（勿當 research 落點）
- 方法論：`/home/ubuntu/guides/`（含 `research-report-template.md`）
- Skills：`~/.hermes/skills/taiwan-stock/`、`investment/`、`equity-research-analyst/`
- 停止使用：home 根目錄散 md、`.gemini/**/investment/`、空的 `obsidian-wiki/台股研究/`
- 另一系統：`.openclaw/workspace/tw-stock-multiagent/`（非 Hermes 權威）

## 規範
- **語言**：所有研究報告、註解、輸出統一使用**繁體中文**
- **研究檔名**：個股 `{代碼}_{名稱}.md`；專題 `摘要_{主題}_{YYYYMMDD}.md`；不用簡體
- **引用**：回覆與跨檔連結用相對 `research/...` 或絕對 `/home/ubuntu/investment/research/...`；新增後必要時更新 INDEX
- **數據來源**：TWSE API + 即時補價，必須附來源日期
- **評分系統**：ROE + 營收成長 + 盈餘成長 + 估值，輸出排序與分數
- **研究表頭**：新檔/重大更新用 `/home/ubuntu/guides/research-report-template.md`（含 `last_verified`、`confidence`、`sources_as_of`）
- **過期規則**：`last_verified` 超過 30 天仍被引用 → 重新驗證或降 confidence

## Dashboard Pipeline
1. `fetch_live.py` — 抓 TWSE 收盤價 → `data/live.json`
2. `score_stocks.py` — 跑評分 → `data/scores.json`
3. `build_site.py` — 建站 → 更新 stock/ 目錄 + index.html
4. `deploy_pages.sh` — git push 到 GitHub Pages

## Git 規範
- 遠端 `origin/main` 為權威來源
- 有 conflict 時：`git fetch origin && git reset --hard origin/main` 再 apply patch
