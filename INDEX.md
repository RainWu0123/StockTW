# 投資知識庫總索引（唯一入口）

**更新日期**：2026-07-14  
**根目錄**：`/home/ubuntu/investment/`  
**方法論（非研究本體）**：`/home/ubuntu/guides/`

之後引用股票／投資內容，**先讀本檔**，再跳到對應路徑。不要再從 home 根目錄或散落路徑猜。

---

## 1. 權威落點（Canonical）

| 類型 | 路徑 | 用途 | 命名 |
|------|------|------|------|
| **個股研究** | `research/{代碼}_{名稱}.md` | 深度研究唯一落點 | `2330_台積電.md` |
| **專題摘要** | `research/摘要_{主題}_{YYYYMMDD}.md` | 外部內容／宏觀／Podcast | `摘要_股癌EP678_20260711.md` |
| **儀表板數據** | `data/*.json` | live / scores / etf / heatmap | 腳本寫入 |
| **個股 JSON 頁** | `stock/{代碼}.json` | 建站用原始頁資料 | `2330.json` |
| **前端／部署** | `index.html`、`spa.html`、`deploy_pages.sh` | GitHub Pages | — |
| **方法論／模板** | `/home/ubuntu/guides/` | 報告模板、系統指南 | 非個股研究 |
| **歷史／散檔歸檔** | `archive/` | Discord 備份、圓桌、legacy 腳本 | 只讀為主 |
| **本索引** | `INDEX.md` | 引用地圖 | 本檔 |
| **Agent 規範** | `AGENTS.md` | 本 repo 工作規則 | 本 repo |

### 引用規則（給 agent / 製作人）

1. 個股：寫完整路徑  
   `research/2330_台積電.md` 或絕對路徑 `/home/ubuntu/investment/research/2330_台積電.md`
2. 專題：同樣用 `research/摘要_*.md`
3. 方法論：用 `/home/ubuntu/guides/...`，**不要**塞進 research/
4. 歷史 Discord 討論：`archive/discord/`
5. 圓桌紀錄：`archive/roundtable/`
6. 禁止再寫入：`/home/ubuntu/*.md` 根目錄、`.gemini/history/investment`、空的 `obsidian-wiki/台股研究`

---

## 2. 目錄樹（精簡）

```
/home/ubuntu/investment/
├── INDEX.md              ← 你在這
├── AGENTS.md             ← 工作規範
├── research/             ← 研究唯一落點（52 個股 + 9 專題）
├── data/                 ← 即時與評分 JSON
├── stock/                ← 67 檔個股 JSON
├── archive/
│   ├── discord/          ← 投資頻道全量備份 + 摘要
│   ├── roundtable/       ← 2026-06 多代理圓桌
│   ├── notes/            ← 籌碼 AI 等零散筆記
│   └── legacy-scripts/   ← 舊 tw-stock-dashboard 副本
├── meta/                 ← 元資料（可擴充）
├── *.py / deploy_pages.sh
└── index.html / spa.html / data.json / etf.json / market.json
```

旁系（**不搬、只標記**）：

| 路徑 | 狀態 | 說明 |
|------|------|------|
| `/home/ubuntu/guides/` | 正式 | 方法論；與 research 分離 |
| `/home/ubuntu/tw-stock-dashboard/` | legacy 殘留 | 原檔仍在；副本在 `archive/legacy-scripts/`；有 `MOVED.md` |
| `/home/ubuntu/obsidian-wiki/台股研究/` | 空 | 未使用，勿當落點 |
| `/home/ubuntu/.gemini/{history,tmp}/investment/` | 工具殘渣 | 停止使用 |
| `/home/ubuntu/.openclaw/workspace/tw-stock-multiagent/` | 另一系統 | OpenClaw 產物，非 Hermes 權威 |
| `~/.hermes/skills/taiwan-stock/`、`investment/`、`equity-research-analyst/` | Skills | 流程；產物仍寫 research/ |
| `~/.hermes/skill-bundles/stock-research.yaml` | Bundle | TSA + 劇本 + 回顧 + ERA |
| `~/.hermes/memory/roundtable-stock-*.md` | 記憶副本 | 內容已 copy 到 archive/roundtable/ |

---

## 3. research/ 現況清單（2026-07-14）

**書寫品質評分（決定改/不改）**：`research/摘要_研究品質評分_20260714.md`  
（48 檔八維打分；P0 必須先動，P3 可先引用）

### 3.1 專題摘要（含品質評分檔）

**股癌入口（消化完成 2026-07-14）**：
1. **Skill（女媧蒸餾 · 執行層）**：`gooaye-perspective`  
   - 路徑：`~/.hermes/skills/investment/gooaye-perspective/`  
   - 底稿：`references/research/01–06` + `FIDELITY.md`  
   - 上游方法：[nuwa-skill](https://github.com/alchaincyf/nuwa-skill)  
2. **AI 可解析**：`research/gooaye_digest.json`  
3. **人讀判斷**：`research/摘要_股癌消化筆記_20260714.md`  
4. 索引／編年：觀點庫、H1 全景、故事線

| 檔案 | 主題 |
|------|------|
| skill `gooaye-perspective` | **怎麼用股癌框架做事** |
| `gooaye_digest.json` | 機器可讀 theses／ticker_map |
| `摘要_股癌消化筆記_20260714.md` | 人讀消化 |
| `摘要_股癌2026觀點庫_20260714.md` | 6–7 月論點索引 |
| `摘要_股癌2026H1全景_20260714.md` | H1 全景分級 |
| `摘要_股癌故事線_2025Q4至2026H1_20260714.md` | 故事編年 |
| `摘要_股癌EP678_20260711.md` | 股癌 EP678 光通／Meta |
| `摘要_股癌EP677_20260708.md` | 股癌 EP677 槓桿／Semi-Analysis |
| `摘要_EP676_台股強勢族群_Meta_NeoCloud_20260704.md` | 股癌 EP676 / Meta NeoCloud |
| `摘要_股癌EP675_20260701.md` | 股癌 EP675 動能／IC 設計 |
| `摘要_股癌EP674_20260627.md` | 股癌 EP674 上半年／蘋果漲價 |
| `摘要_股癌EP673_20260624.md` | 股癌 EP673 電阻漲浪 |
| `摘要_股癌EP671_20260617.md` | 股癌 EP671 離散／功率 |
| `摘要_股癌EP670_20260613.md` | 股癌 EP670 SpaceX／估值 |
| `摘要_股癌EP669_20260610.md` | 股癌 EP669 信仰考 |
| `摘要_股癌EP6xx_*.md` | EP640–668 等 A/B 分集（見 H1 全景） |
| `摘要_KP49期_20260704.md` | KP 思考 49 期 |
| `摘要_KP55期_Datadog可觀測層_20260708.md` | KP55 / Datadog |
| `摘要_MMPaM_EP206_ETF狂潮_20260712.md` | M 平方 Podcast ETF 狂潮 |
| `摘要_SK海力士暴跌_KIS下調_LTA定價模式_20260713.md` | 海力士 / LTA 定價 |
| `摘要_早晨財經速解讀_20260709.md` | 早晨財經 |
| `摘要_記憶體定價與頂部確認_三星Q2案例_20260708.md` | 三星 Q2 / 記憶體頂部 |
| `摘要_研究品質評分_20260714.md` | 書寫品質評分 |

### 3.2 個股研究（52）

**2026-07-14 新增觀察池（12）**：緯穎、信驊、欣興、健策、英業達、緯創、旺宏、金像電、京元電子、光寶科、台化、禾伸堂。

| 代碼 | 檔案 | 備註 |
|------|------|------|
| 1101 | `1101_台泥.md` | |
| 1216 | `1216_統一.md` | |
| 1301 | `1301_台塑.md` | |
| 1303 | `1303_南亞.md` | |
| 1326 | `1326_台化.md` | **新** 0050／台塑系 |
| 2002 | `2002_中鋼.md` | |
| 2301 | `2301_光寶科.md` | **新** 電源對照 |
| 2303 | `2303_聯電.md` | 核實較完整 |
| 2308 | `2308_台達電.md` | AI 電源／散熱 |
| 2313 | `2313_華通.md` | |
| 2317 | `2317_鴻海.md` | |
| 2327 | `2327_國巨.md` | |
| 2330 | `2330_台積電.md` | 深度重寫 |
| 2337 | `2337_旺宏.md` | **新** 記憶體 |
| 2344 | `2344_華邦電.md` | 記憶體 cross-ref |
| 2345 | `2345_智邦.md` | 深度重寫 |
| 2356 | `2356_英業達.md` | **新** server 代工 |
| 2368 | `2368_金像電.md` | **新** 高階 PCB |
| 2375 | `2375_凱美.md` | |
| 2382 | `2382_廣達.md` | AI 鏈加深 |
| 2383 | `2383_台光電.md` | AI 鏈加深 |
| 2395 | `2395_研華.md` | |
| 2404 | `2404_漢唐.md` | |
| 2408 | `2408_南亞科.md` | 記憶體 cross-ref |
| 2412 | `2412_中華電.md` | |
| 2449 | `2449_京元電子.md` | **新** 測試 |
| 2454 | `2454_聯發科.md` | |
| 2881 | `2881_富邦金.md` | 深度重寫 |
| 2882 | `2882_國泰金.md` | |
| 3005 | `3005_神基.md` | 深度重寫 |
| 3008 | `3008_大立光.md` | |
| 3017 | `3017_奇鋐.md` | AI 鏈加深 |
| 3026 | `3026_禾伸堂.md` | **新** 00991A／被動 |
| 3037 | `3037_欣興.md` | **新** 載板 00991A |
| 3038 | `3038_全台.md` | |
| 3231 | `3231_緯創.md` | **新** server |
| 3443 | `3443_創意.md` | |
| 3529 | `3529_力旺.md` | |
| 3653 | `3653_健策.md` | **新** 散熱 |
| 3711 | `3711_日月光.md` | |
| 5269 | `5269_祥碩.md` | 6 月年減警示 |
| 5274 | `5274_信驊.md` | **新** BMC 00991A |
| 6166 | `6166_凌華.md` | |
| 6239 | `6239_力成.md` | |
| 6285 | `6285_啟碁.md` | |
| 6415 | `6415_矽力.md` | 核實更新 |
| 6442 | `6442_光聖.md` | |
| 6505 | `6505_台塑化.md` | |
| 6669 | `6669_緯穎.md` | **新** AI server 純度 |
| 6770 | `6770_力積電.md` | |
| 6830 | `6830_汎銓.md` | |
| 7610 | `7610_聯友金屬創.md` | 深度重寫 |

深度索引：`research/.research_index.json`（2026-07-14 重建，含新增 12 檔）。

### 3.3 儀表板資料

| 檔案 | 用途 |
|------|------|
| `data/live.json` | TWSE 即時／收盤補價 |
| `data/scores.json` | 評分排序 |
| `data/etf.json` / 根目錄 `etf.json` | ETF 追蹤 |
| `data/heatmap.json` | 熱力 |
| `data/scoring_rules.json` | 評分規則 |
| `data/backtest_20d.json` | 回測 |
| `stock/*.json`（67） | 個股建站頁 |
| 根 `data.json` / `market.json` | 前端讀取 |

---

## 4. archive/ 內容

| 子目錄 | 內容 | 引用時 |
|--------|------|--------|
| `archive/discord/` | `investment_channel_all.json`（全量）、`latest_100.json`、`investment_channel_summary.md` | 歷史討論／劇本追溯 |
| `archive/roundtable/` | expert_meeting、R2/R3 反駁、chip analyst、hermes memory 副本 | 2026-06 圓桌 |
| `archive/notes/` | `tw_stock_ai_suggestions.md`（籌碼訓練建議） | 系統設計靈感 |
| `archive/legacy-scripts/tw-stock-dashboard/` | briefing / decision / discord_send 舊腳本 | 勿當正式 pipeline |

### 2026-07-14 從 home 根目錄搬入

| 原路徑 | 新路徑 |
|--------|--------|
| `/home/ubuntu/investment_channel_*.json|md` | `archive/discord/` |
| `/home/ubuntu/round*.md`、`expert_meeting_report.md` | `archive/roundtable/` |
| `/home/ubuntu/tw_stock_ai_suggestions.md` | `archive/notes/` |
| （副本）`tw-stock-dashboard/*` | `archive/legacy-scripts/tw-stock-dashboard/` |

根目錄留下 stub 指標（`investment_channel_summary.md`、`tw_stock_ai_suggestions.md`、`tw-stock-dashboard/MOVED.md`），避免舊連結完全斷掉。

### 命名修正

- `research/EP676_...` → `research/摘要_EP676_台股強勢族群_Meta_NeoCloud_20260704.md`（對齊專題規範）

---

## 5. guides/ 中與投資相關

| 檔案 | 用途 |
|------|------|
| `research-report-template.md` | 個股研究表頭（last_verified / confidence） |
| `authoritative-references.md` | 權威來源列表（含本 knowledge base） |
| `harness-engineering-backtest-plan.md` | harness 回測計劃（系統，非個股） |

其餘 guides 多為 Hermes／coding 方法論，不是台股研究本體。

---

## 6. Skills／Cron 對口

| 能力 | Skill / Job | 寫入落點 |
|------|-------------|---------|
| 個股決策 | `taiwan-stock-analyst` | 讀 data/ + research/ |
| 長報告 | `equity-research-analyst` | `research/{代碼}_{名稱}.md` |
| 外部內容留檔 | `investment-research-archive` | `research/摘要_*.md` |
| 劇本檢核 | `investment-playbook-review` | 通常不另存；結論可回寫 research |
| 交易回顧 | `trade-review` | 依 skill |
| 儀表板 | `tw-stock-dashboard` | data/、stock/、deploy |
| 晨報／盤後 | `morning-briefing` / `eod-analysis` | 輸出可落 research 或 cron output |
| Bundle | `~/.hermes/skill-bundles/stock-research.yaml` | 同上 |

---

## 7. 之後新增內容 checklist

- [ ] 個股 → 只寫 `research/{代碼}_{名稱}.md`
- [ ] 專題／Podcast／新聞摘要 → 只寫 `research/摘要_{主題}_{YYYYMMDD}.md`
- [ ] 新檔表頭用 `guides/research-report-template.md`
- [ ] 繁體中文；來源 + 日期 + 信心
- [ ] 更新本 INDEX 的清單節（或至少 git commit 訊息標清檔名）
- [ ] 不要往 home 根、obsidian 空資料夾、gemini tmp 塞研究

---

## 8. 已知缺口

1. 多數個股仍是「營收＋劇本」合格線，未達法人完整八塊；watchlist 優先加深
2. 光通二線（上詮 3363、波若威 3163）、雙鴻 3324 等尚未建檔（非本次必須）
3. `investment-research-archive` 舊步驟若寫 `YYYY-MM-DD_主題.md` → 以本 INDEX + `摘要_` 規範為準
4. OpenClaw multiagent 與 Hermes investment 未合併（有意分離）

---

*整理 session：2026-07-14。目標：一處可引用、路徑可驗證、散檔可追溯。觀察池 2026-07-14 擴充至 52 檔。*
