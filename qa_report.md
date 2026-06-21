# 台股少年股神 — QA 測試回報報告（Z 世代視角）

**測試網站：** https://rainwu0123.github.io/StockTW/  
**測試者角色：** Z 世代年輕投資人  
**測試日期：** 2026-06-21（相對網站日期 2026-06-20）  
**測試檔案：** spa.html / data.json / data/heatmap.json / data/etf.json

---

## 1. 總評Executive Summary

| 維度 | 得分（/10） | 評語 |
|------|------------|------|
| UI/UX 美感 | 6.5 | 深色主題成熟但過於單調，缺乏 Gen-Z 期待的視覺衝擊與微互動 |
| 動畫流暢度 | 5.0 | GSAP 有到位，但 sheet 開合與 tab 切換動畫不一致；部分動畫只作用於子元素 |
| 手機適配 | 3.0 | 無 RWD 選單、表格僅靠橫向捲動、文字密度過高 |
| 視覺衝擊力 | 5.5 | 色碼系統清楚，但卡片邊框過於 aggressive、同質化過高 |
| 功能正確性 | 6.5 | 核心功能可用，但存在 data bug、HTML 錯誤與 null 渲染問題 |

**綜合結論：** 這是一個「桌面端專業儀表板」雛形，離「Z 世代手機優先的投資社群 App」尚有大段距離。

---

## 2. UI/UX 美感瑕疵（Design Flaws）

### 2.1 色彩系統問題
- **台灣市場紅綠反轉未處理**：台灣股市習慣「紅漲綠跌」，目前使用「綠漲紅跌」（美股慣例）。對於在地年輕投資人而言，這會造成認知負荷。
- **全站紅色過量**：`--border: #252b3a` 明明偏向灰藍，但視覺上因為密集的 card border 與 table 邊框，畫面呈現大量紅色描邊感，容易讓使用者誤以為全站在錯誤狀態。
- **缺少品牌色 highlight**：`--accent: #5aa9ff` 使用範圍極小（幾乎只有連結），無法形成品牌記憶點。

### 2.2 字體與可讀性
- **表格行高過大**：每列行高 61px，資訊密度看似高，但實際文字只佔中間一小塊，上下留白過多。
- **複合標題重複渲染**：公司欄同時渲染 `<a>` 與後續 `<div>` note，導致同一支股票名稱在視覺上出現兩次（例如 台塑化 ETF成分股(0050)），浪費視線焦點。
- **null 直接輸出字串**：力旺 (3529) 的價格、漲跌幅直接渲染 `null` / `null%`，是非常「工程師視角」的錯誤。
- **缺少 loading 狀態**：`renderSummary()` 先寫入「載入中…」，但其他 tab 切換時沒有 skeleton / shimmer。

### 2.3 視覺層次
- **熱力圖三區塊無stated區分**：heatDay / heatWeek / heatMonth 外觀完全相同，使用者難以一眼辨識時間維度。
- **Detail Sheet 內容堆疊**：概念股、同產業、交易劇本三區塊樣式完全一樣，缺乏視覺呼吸空間。
- **footer 字體與內容不匹配**：寫著 "Skeuomorphic UI · 2026"，但 UI 實際上是扁平化深色模式。

---

## 3. 動畫流暢度問題（Animation & Jank）

### 3.1 動畫不一致
- **Tab 動畫僅跑一次**：`animateTabs()` 定義了但未在 init 時呼叫（或只在切換時未重播），實際切換 tab 時無過渡動畫。
- **Sheet 動畫分離**：`animateSheet()` 對 `#sheetBody` 做 GSAP，但 sheet container 的 open/close 卻是 CSS transition（`.sheet { transition: transform .22s ease; }`）。這造成容器滑入時內容 opacity 才剛開始，時間軸不同步。
- **Card stagger 過多**：`animateAll()` 對 `.card` 做 stagger 0.03s，若有 20 張卡片會拖累初始渲染。且 heatmap 的 industry-card 動畫另有獨立 stagger，兩者可能同時觸發導致掉幀。

### 3.2 Jank / 效能隱忧
- **renderLobby 使用 innerHTML**：每次搜尋或排序都暴力重建整張表格（39 行），雖有 `requestAnimationFrame` 緩衝，但 GSAP 的 `fromTo(rows[0]...)` 只對第一列動畫，其餘直接 `gsap.set`，動畫節奏不一致。
- **熱力圖重複渲染**：`renderHeat()` 把同一份 `industries` slice 三份寫入三個 container，DOM 節點數是需要的三倍，不利於散熱/效能。
- **缺少 `will-change` / `contain`**：`.industry-card` 與 `.sheet` 為動態元素，但未告知瀏覽器做渲染優化。

### 3.3 交互回饋不足
- **industry-card hover 動畫僵硬**：translateY(-2px) + shadow 同時變化，感覺像「浮起來」而非「彈性選取」。
- **tab :active 只有 translateY(1px)**：沒有縮放或 color flash，觸覺回饋太輕。

---

## 4. 手機適配問題（Mobile Responsiveness）

### 4.1 结构性問題
- **tab 列於小螢幕上會直接換行**：`flex-wrap: wrap` 在手機上把 6 個 tab 擠成兩行，佔掉寶貴的頂部空間，且沒有捲動/收合機制。
- **grid-4 在 640px 以下只變 1fr**：這是唯一針對手機的 media query。但 `.table-wrap` 的表格仍維持 10 欄，必須左右滑動查看，違反單手操作原則。
- **topbar sticky 雙重堆疊**：`.topbar`（66px 以下 sticky）+ `.tabs`（sticky top:66px），在手機瀏覽器網址列縮放時容易產生 2 + 66 = 巨大佔高。

### 4.2 觸控友善度
- **表格 row 高度 61px，但點擊連結文字卻極小**：連結無 padding / block display，手指很容易點錯。
- **產業卡片無 swipe/長按提示**：在手機上點擊展開容易與捲動衝突。

---

## 5. 視覺衝擊力問題（Visual Impact）

### 5.1 一致的弱點
- **缺乏 Gen-Z 語彙**：沒有 emoji 數據 storytelling、沒有護眼模式/霓虹選項、沒有使用者頭像或社群按讚/分享。
- **卡片太像**：所有 `.card` 外觀近乎相同，缺乏頁面層級區分。
- **缺少「Wow Moment」**：沒有啟動動畫、沒有即時刷新閃爍、沒有漲停紅綠燈特效。

### 5.2 可改進的亮點
- `.industry-bar-fill` 的漸層動畫潛力不錯，但目前只有 width 變化，沒有 shimmer 或 pulse。
- 分級色條（tier-row-t1 綠色左框）是很好的視覺錨點。

---

## 6. 功能與程式瑕疵（Functional / Code Bugs）

| # | 嚴重度 | 問題描述 | 位置 |
|---|--------|----------|------|
| B1 | **高** | 力旺 (3529) 價格/漲跌幅為 `null` 字串，直接呈現在 UI | data.json + renderLobby() pctClass(null) |
| B2 | **高** | 台光電 (2383) 在 data.json 出現兩次（line ~156 與 line ~191），可能重複渲染 | data.json |
| B3 | **高** | 熱力圖同一批產業被 render 三次（日/週/月），視覺上出現三組完全相同卡片 | renderHeat() |
| B4 | **中** | HTML class 屬性重疊（如 `class="big" ... class="${pctClass...}"`），後者被覆蓋，導致顏色樣式失效 | renderSignals / renderChip / renderEtf / renderDetail |
| B5 | **中** | `onclick="javascript:void(0)"` 語法錯誤 | renderLobby 連結 |
| B6 | **中** | `gsap.min.js` 以外部 CDN 連結但無本地 fallback；若離線則動畫全掛 | <head> |
| B7 | **中** | Detail sheet 的「同產業/概念股」peerCards 使用 slice(0,20)，但資料庫 peers 沒有上限設計，可能無故截斷 | renderDetail() |
| B8 | **低** | `guessSector()` 永遠回傳 '其他'，無意義 | renderDetail |
| B9 | **低** | 網站日期寫死 2026-06-20（未來日期），可能讓真時使用者困惑 | data.json |
| B10 | **低** | footer 標註 "Skeuomorphic UI" 但 design 完全不像 skeuomorphic | footer |

---

## 7. 跨頁體驗一致性檢查

| 頁面 | 有動畫 | 有回到頂部 | 卡片樣式統一 | 備註 |
|------|--------|------------|--------------|------|
| 大廳 Lobby | 初始有，重繪時無 | 無 | ✅ | 初始載入有 stagger |
| 信號 Signals | ✗ | ✗ | ✅ | 純 innerHTML，無過渡 |
| 籌碼 Chip | ✗ | ✗ | ✅ | 同 Signals |
| 產業熱力 Heat | ✗ | ✗ | ✅ | expand/collapse 有 GSAP |
| ETF | ✗ | ✗ | ✅ | 尚未載入時空白 |
| 資產 Portfolio | ✗ | ✗ | ✅ | localStorage 驅動 |

---

## 8. 行動測試建議（Mobile Emulation Notes）

以桌面視窗縮小模擬手機時觀察到：
1. **640px breakpoint 只改變 grid-4**，其餘未跟進 → 表格資料在手機上完全不可用。
2. **Tab 列高度超過 80px**，相對內容高度比率過高。
3. ** Detail sheet 寬度 `min(800px, 94vw)`**，在 375px 手機上仍佔 94vw → 部分左右 padding 被吃掉，內容貼邊。

---

## 9. 優先改善建議（Top Priority Fixes）

### A. 立即修復（Blocking）
1. 修復 `class` 屬性重疊導致顏色樣式失效（改成單一 class 拼接）。
2. 修復 `null` 渲染：price / pct 為 null 時顯示 `--`。
3. 合併 data.json 中重複的台光電 (2383)。
4. 熱力圖 render 三組時增加視覺維度標示（例如 plus 背景色不同），或改用 tab 切換。

### B. Z 世代痛點（Engagement）
1. 加入「每日戰報」與分享截圖功能（Gen-Z 愛曬圖）。
2. 熱力圖改為可互動的圓形 treemap 或 flame graph。
3. Tab 列改為底部 nav bar（手機拇指熱區）。
4. 大量加入 loading shimmer / skeleton。

### C. 動畫優化（Polish）
1. 統一 GSAP 與 CSS transition 時機。
2. renderLobby / renderSignals 於內容取代前先淡出（fade-out → replace → fade-in）。
3. `.industry-card` 加入 `will-change: transform, box-shadow`。

---

## 10. 附錄：檔案勘誤

**data.json**
- Line 191-200：刪除一個 2383 重複物件

**data/heatmap.json**
- 結構本身正確，但前端 `renderHeat` 三次 render 同一陣列 → 建議改為 tab or 滾動分段

**spa.html**
- Line 392-501：多處雙 `class` 屬性
- Line 401：`javascript:void(0)` 缺空白
- Line 579-581：stagger/GSAP 只處理第一列
- Line 533-536：`closeSheet` timeout 220ms 與 CSS transition .22s 不同步

---

*報告結束。如需實際重現畫面截圖或進一步乙太測試，請重新啟動 browser 服務。*
