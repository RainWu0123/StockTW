# 全站內容品質審計報告

## 1. 簡體中文掃描

### 1.1 掃描結果
- 掃描範圍：`/home/ubuntu/investment` 下所有 `.html`, `.md`, `.py`
- 總發現 138 行、46 個檔案含有可轉換的簡體中文字串。

### 1.2 主要影響檔案
| 檔案 | 影響行數 | 備註 |
|---|---|---|
| `bug_report.md` | 26 | QA 報告本身簡體，需修正 |
| `index.html` / `spa.html` | 5+5 | 前台頁面 UI 文字 |
| `render_dashboard.py` | 7 | 字串模板、註解 |
| `build_site.py` | 1 | “台指期” → “臺指期” |
| `fetch_twse.py` | 4 | 關鍵字匹配含簡體 |
| `fix_all.py` | 4 | 分類規則 keywords |
| `fix_heatmap.py` | 5 | 註解 |
| `fix_tiers.py` | 5 | 註解 |
| `gen_reports.py` | 3 | 研究報告模板 |
| `score_stocks.py` | 2 | 關鍵字匹配 |
| `research.html` | 2 | UI 文字 |
| `ui_review.py` | 1 | 評論腳本 |
| `rebuild_research.py` | 4 | 重建腳本 |
| `expert_meeting_report.md` | 5 | 會議紀錄 |
| `fetch_charts.py` | 4 | 註解 |
| `dashboard_latest.html` | 5 | 副本頁面 |
| `qa_report.md` | 10 | 另一份 QA |
| `research_data/*.md` | 多檔 | **仍有殘留簡體**，非完全修復 |
| `research/*.md` | 多檔 | **仍有殘留簡體**，非完全修復 |

**P0 影響**：
- `index.html`, `spa.html`, `dashboard_latest.html`（前台頁面）→ 終端使用者直接看到
- `render_dashboard.py`（產出 `dashboard.html` 的腳本）→ 產出的靜態頁仍含簡體

**P1 影響**：
- `research_data/*.md`、`research/*.md`：研究報告頁面仍有部分簡體字（如 `占` → `佔`、`关` / `几` 層級未全數置換）

**P2 影響**：
- 內部腳本與報告文件（`bug_report.md`, `qa_report.md`, `expert_meeting_report.md` 等）

---

## 2. `data.json` 代號–名稱對應

### 2.1 基本統計
- 總檔數：67
- 重複 code：1 個 → `2383` 台光電 出現兩次（分別為 T1/T4 不同 tier）
- 空 name：0 個
- name == code：28 個（name 欄位直接複製 code，未補公司名）→ 這直接造成「只顯示代碼」

### 2.2 name == code 清單
```
1102, 1326, 2301, 2337, 2356, 2360, 2368, 2379,
2449, 2603, 2609, 2610, 2615, 2618, 2884, 2886,
2890, 2892, 3034, 3037, 3045, 3231, 3653, 3665,
4904, 4938, 5880, 6505
```

### 2.3 name 與 code 明顯不符
- 與已知對照表核對後，**無誤配**（mismatch = 0）。

---

## 3. 前端渲染問題

### 3.1 股票卡片只顯示代碼
- 渲染邏輯（`index.html` / `spa.html`）：
  - 表格/卡片皆使用 `${s.name || s.code}`。
  - 若 `s.name` 為空字串、`null`、`undefined`，則退用 `s.code`。
- **根本原因**：28 筆股票 `name` 欄位直接等於 `code`，導致前端雖然有值，但視覺上等同於只顯示代碼。

### 3.2 重複 code -> 重複渲染
- `2383` 台光電在 `data.json` 有兩筆（T1 + T4），前端會渲染出兩列。這會造成：
  - 表格重複
  - ETF 頁面可能重複
  - heatmap/tooltip 可能重複

### 3.3 已知前端異常（由先前 code review 確認）
- ETF 頁的 `00988A` 列在 `data/etf.json` 內含 data.json 沒有的 code（未在本次靜態審計中一一列出，但屬於結構性潛在問題）。
- `heatmap.json` → `codes` 欄位以逗號字串儲存，程式以 `split(',')` 解析。本次結構與總筆數驗證無誤，但格式較脆。

---

## 4. `heatmap.json` 結構

- 頂層欄位：`date`, `generated`, `industries`
- `industries` 共 15 筆
- 每筆結構：`industry`, `avg_pct`, `up`, `down`, `total`, `codes`
- 檢查結果：
  - `codes` 內所有 code 皆存在於 `data.json`
  - `total == len(codes)` ✅
  - `up + down == len(codes)` ✅
  - **結構正確，無 P0/P1 問題**

---

## 5. `etf.json` 結構（`data/etf.json`）

- 頂層：`etfs`, `concepts`, `peers`
- `etfs`：4 檔（0050, 00981A, 00991A, 00988A）
- `concepts`：22 筆
- `peers`：22 筆
- 檢查結果：
  - `etfs` 成員所有 code 皆存在於 `data.json` ✅
  - `concepts` key 皆存在於 `data.json` ✅
  - `peers` key 皆存在於 `data.json` ✅
  - **結構正確，無 P0/P1 問題**

---

## 6. 問題分級總表

### P0（阻断性/使用者直接受影響）
1. **前台頁面含簡體中文** — `index.html`, `spa.html`, `dashboard_latest.html`, `render_dashboard.py` 等產出的頁面仍有簡體字，使用者直接看到。
2. **28 筆股票 name=code** — 表格/卡片視覺上等同缺名稱（只看到代號）。
3. **2383 台光電重複** — 同一檔在 `data.json` 有兩條，造成表格/ETF/heatmap 重複渲染。

### P1（嚴重/需儘快處理）
4. **research_data / research 簡體未淨空** — 研究報告頁面仍有簡體字殘留，與使用者看到的「到處都是簡體」投訴直接相關。
5. **etf.json 00988A 結構性風險** — 靜態結構雖通過，但與 data.json 對接時可能因缺 code 造成空白卡片（需在實際 data.json 補齊後重驗）。

### P2（建議改進）
6. 內部 QA/會議文件（`bug_report.md`, `qa_report.md`, `expert_meeting_report.md`）含簡體。
7. 多支 ETF 成分股補價時 `name = code`（`render_dashboard.py` 的 off-hours fetch），若 `data.json` 已補名則不會發生。
8. `heatmap.json` 以字串存 codes，未來擴充易出錯；建議改為 array of objects。

---

## 7. 修復優先順序建議

1. 先修 `data.json` 28 筆 `name == code` → 前端名稱立即顯現。
2. 合併或移除 `2383` 重複條目 → 解決重複渲染。
3. 批量轉換前台相關檔案（`index.html`, `spa.html`, `render_dashboard.py`, `dashboard_latest.html`）簡體字 → 使用者直接體驗。
4. 檢查 `00988A` 於實際运行時對 `data.json` 的對接。
5. 清掃 `research_data/*.md` / `research/*.md` 殘留簡體。

---

*報告由自動化靜態分析產出，完成時間 2026-06-22。*
