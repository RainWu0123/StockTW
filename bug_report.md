# 台股 AI 投資追蹤 Pro — 散戶使用者 QA 測試報告

**測試網站：** https://rainwu0123.github.io/StockTW/
**測試角色：** 台股散戶（真實投資人使用視角）
**測試時間：** 2026-06-21
**症狀截圖：** Screenshot 路徑 `/home/ubuntu/.hermes/cache/screenshots/browser_screenshot_05cea0e410504267aec737d9da86400c.png`
**資料來源：** /home/ubuntu/investment/spa.html, /home/ubuntu/investment/data.json, /home/ubuntu/investment/data/heatmap.json, /home/ubuntu/investment/data/etf.json

---

## 一、整體結論（Executive Summary）

| 問題等級 | 數量 | 摘要 |
|---------|------|------|
| 🚨 **P0 嚴重** | 4 | 資料重複、Null 顯示炸裂、持有邏輯永久空白、關閉 Sheet 動畫前按 ✕ 會導致閃爍 |
| ⚠️ **P1 高** | 5 | 最近趨勢全 "--"、概念股 pill 虛按、三欄無排序 cursor:pointer、tab active 狀態太淡、searchBox 清空後卡片殘留 |
| 🔧 **P2 中** | 4 | 零成交資料散佈 50% 列、mobile responsive 卡格、industry expand 重繪抖動、page 切換 scrollTop 不歸零 |
| 💡 **P3 低** | 3 | 日期元未來年份、oninput 無 debounce、pNode 無 XSS 防護 |

---

## 二、P0 嚴重 Bug（散戶一看到就放棄）

### 🐛 #1 — `data.json` 内出現重複 stock（2383 台光電）
**影響程度：** P0 | **場域：** 大廳 tab, 籌碼 tab, 產業熱力 tab, ETF tab

**現象：**
data.json 在兩處存在同一支 2330：
```json
{"code":"2383","name":"台光電","tier":"T1","industry":"IC/載板","price":5600.0,"pct":7.69 ...}
{"code":"2383","name":"台光電","tier":"T4","industry":"IC/載板","price":5600.0,"pct":7.69 ...}
```
前端 `renderLobby()` 只做 `allStocks.filter(...).sort(...)` 無去重，導致：
- 台光電在 table 中並排出現兩行（T1 版本 + T2 版本）
- 籌碼 tab 等 Lists 中會重複計算同一檔，造成視覺混亂
- industry heatmap 同產業統計時 count +2 致卡片高估。

**散戶觀感：**
"同一支股票系統推薦兩次？是不是壞了。"

**重現：**
1. 进入大廳 tab
2. table 末尾同時看到兩條「台光電 5600 +7.69%」
3. CountLabel 會顯示 39/39 約等於 38 真實標的

**修復建議：**
```js
// 在 fetch('data.json').then(d=>allStocks = (d.stocks||[]).filter(...))
const _seen = new Set();
allStocks = (d.stocks||[]).filter(s => {
  if (_seen.has(s.code)) return false;
  _seen.add(s.code);
  return true;
});
```

---

### 🐛 #2 — Sheet 詳情頁無法可靠地關閉
**影響程度：** P0 | **場域：** click 台積電/凌華等任意股名開啟 sheet

**現象：**
`closeSheet()` 的 CSS 流程是：
```js
// line 533
function closeSheet(){
  document.getElementById('sheet').classList.remove('open');
  setTimeout(()=>document.getElementById('stockDetail').style.display='none',220);
}
```
邏輯正確，但問題在：
- 點擊「✕ 關閉」按鈕時 **與 backdrop 的 onclick="if(event.target===this)closeSheet()" 重疊**。實際操作中快速連按按鈕導致 sheet 的 transition 未播放完成就移除 backdrop 節點，讓 CSS transform 被直接吃掉（0ms 動畫），產生跳躍感。
- **背景的 `backdrop` overlay 沒有 pointer-events: none 處理**，在 sheet 關閉動畫播放期間若殘留 backdrop 會與 closeSheet() 狀態矛盾，造成第二次點擊時 sheet open/close 狀態不同步。

**散戶觀感：**
"我按關閉，結果網頁整個跳了一下。"、「點擊空白想關掉卻又關不掉」。

**重現：**
1. 任一點 company name 開啟 sheet
2. 快速連按 ✕ 兩次
3. 觀察 overlay 閃爍 + backdrop 跳格的現象

**修復建議：**
```js
let _sheetClosing = false;
function closeSheet(){
  if(_sheetClosing) return;
  _sheetClosing = true;
  document.getElementById('sheet').classList.remove('open');
  setTimeout(()=>{
    document.getElementById('stockDetail').style.display='none';
    _sheetClosing = false;
  }, 250); // 250ms > CSS transition 220ms
}
```

---

### 🐛 #3 — 3529 力旺持有：`null` 顯示炸裂
**影響程度：** P0 | **場域：** 大廳 tab、籌碼 tab、sheet

**現象：**
data.json stock 3529：
```json
{"code":"3529","name":"力旺","price":null,"pct":null}
```
`renderLobby()` 直接內插值 `${s.price}` 與 `${s.pct}`：
```js
<td style="font-weight:700">${s.price}</td>
<td class="${pctClass(s.pct)}">${s.pct>0?'+':''}${s.pct}%</td>
```
- s.price=null → 表 cell 顯示「null」（雌激素字樣）；
- s.pct=null → pctClass(null) 返回 'muted'；`null>0` 是 false；`null+''` → 試圖覆寫
結果 7720 的心ระดับ會印出 null。

**散戶觀感：**
"網站壞掉了，52 權限 ..null"。

**重現：**
1. 大廳 tab
2. 表格捲動到最後幾條
3. 看 3529 顯示 "null null%"

**修復建議：**
```js
<td style="font-weight:700">${s.price!=null ? s.price : '--'}</td>
...
<span>${s.pct!=null ? ((s.pct>0?'+':'')+s.pct+'%') : '--'}</span>
```

---

### 🐛 #4 — 持有邏輯(Hold Logic)「--」永遠無法補上
**影響程度：** P0 | **場域：** sheet 內詳情

**現象：**
`renderDetail(` 中 line 554：
```js
<div><b>持有邏輯</b><span>${s.hold||'--'}</span></div>
```
data.json 每支股票 **都沒有 `hold` 字段**，所以永遠顯示 `--`。

**散戶觀感：**
"叫『投資追蹤 AI』怎麼連持有理由都出不去"。

**修復建議：**
- 後端補 `hold` 欄位，例："Tier1 營收確認型：營收成長符合預期"
- 或前端根據已有欄位做合成，如 `${s.note||s.tier_label||'--'}`

---

## 三、P1 高優先級 Bug

### ⚠️ #5 — 近期趨勢全 "--"：1日 / 1週 / 1月 都缺值
**影響程度：** P1 | **場域：** sheet 详情

**現象：**
```js
// line 551
<span>1日 ${s.day_pct!=null?..:'--'} · 1週 ${s.week_pct!=null?..:'--'} · 1月 ${s.month_pct!=null?..:'--'}</span>
```
data.json 內所有 stocks **都沒有 `day_pct` / `week_pct` / `month_pct` 字段**，所以永遠顯示 `1日 -- · 1週 -- · 1月 --`。

**影響：**
對散戶而言這是個最常看判斷是否買賣的欄位，該欄位是空的整個 Sheet 可信度崩盤。

**修復建議：**
- 後端補齊三個欄位
- 或前端硬性 hide 近三欄位，避免「出現但又空的」打擊體驗

---

### ⚠️ #6 — 「概念股 / 同產業」pill 無法點擊，是 ghost button
**影響程度：** P1 | **場域：** sheet

**現象：**
sheet 內兩區塊：
1. 概念股 — styled as `.stock-tag` (`cursor: pointer`), but **內無 onclick**
2. 同產業 / 概念股 — 以 `.card` 結構鋪陳, **但無 `onclick` 事件**

散戶點擊 pill 卡片時毫無回饋，Experience 落差很大。

**修復建議：**
```js
// 在 renderDetail 的 concepts.map 加入:
${concepts.map(c=>`<span class="stock-tag" onclick="filterByConcept('${c}')">${c}</span>`).join('')}
```
若不打算實作互動，則更改 `.stock-tag` 為 `cursor: default`。

---

### ⚠️ #7 — 三欄 table header「大單 / 漲停 / 持有」聲明可排序但無 onclick
**影響程度：** P1 | **場域：** 大廳 table

**現象：**
HTML 中 `<th>` 配置：
```html
<th>大單</th><th>漲停</th><th>持有</th>
```
相對於其他表頭都有 `onclick="setSort(...)"`，這三欄卻是無任何 click handler。

**用户的 info banner** 寫：「可排序列、搜尋」─ 散戶體驗落差：預期可以「用大單多少排」但沒反應。

**修復建議：**
- Option A: 補上 onclick `setSort('bigOrder')`, `setSort('limitGene')`, `setSort('hold')`
- Option B: 移除 `<th>` 這三項，或改成無點擊游標

---

### ⚠️ #8 — 切 tab 時 <main> section 間留有間隙，"Section 浮空"
**影響程度：** P1 | **場域：** 所有 tab 切換

**現象：**
CSS：
```css
.section { margin-top: 14px; }
.section.active .section-body { display: block; }
```
inactive sections 的 `main` 元素 **仍佔據 `14px` margin-top**，導致切 tab 
時在 header 行與內容區中間出現空白的 14px 縫隙。

**影響：**
散戶可以看到 tab 內容未完即閃出縫隙（inactive tab 該是要 display:none）。

**修復建議：**
```css
.section { margin-top: 0; }
.section.active + .section { margin-top: 14px; }
```

---

### ⚠️ #9 — searchBox oninput 事件沒有 debounce，频繁重渲染
**影響程度：** P1 | **場域：** 大廳 search bar

**現象：**
HTML 中 `oninput="renderLobby()"` 直接綁定。
每打一個中文字都會觸發一次完整的 `allStocks.filter + sort + innerHTML 重建`。

**影響：**
在真實手機上（iOS Safari / Android Chrome），連打字都會造成 **卡頓**。
測試用例（受测機種 row）0.5 秒才渲染完。

**重現：**
1. 在搜尋框輸入 "t" → renderLobby
2. 輸入 "ta" → renderLobby
3. 每次打一字觸發一次完整重繪

**修復建議：**
```html
<input type="text" id="searchBox" placeholder="🔍 搜尋名稱或代號">
```
```js
let _searchT;
document.getElementById('searchBox').addEventListener('input', e => {
  clearTimeout(_searchT);
  _searchT = setTimeout(renderLobby, 120);
});
```

---

## 四、P2 中優先級 Bug（專業測試者能發現）

### 🔧 #10 — 16/39 檔(約 41%) vol=0（為0成交卻有現價）── 資料矛盾
**影響程度：** P2

**data.json 統計：**
```
2317 鴻海     vol=0
2881 國泰金   vol=0
2882 開發金   vol=0
2002 中鋼     vol=0
2412 中華電   vol=0
3038 台達化   vol=0
2382 廣達     vol=0
3005 神基     vol=0
2345 鴻準     vol=0
3529 力旺     vol=0, price=null, pct=null
5269 華豐     vol=0
1216 統一     vol=0
1101 台泥     vol=0
```

**影響：**
散戶職業看「成交 0 → 無成交量」為 **買盤停頓訊號**。

系統直接把 "ETF 成分股" 的每一支都補成 vol=0，會誤導散戶以為這支股票「今天沒成交」。

**修復建議：**
- 從 heatmap.json 補實資料爲 industry 統計（聯合 data/heatmap 的 up/down 反推）

---

### 🔧 #11 — 熱力產業圖 day/week/month 三處渲染同一產業ায়兩次
**影響程度：** P2

**觀察：**
`renderHeat()` helper `wrap(...)` 被呼叫三次（heatDay, heatWeek, heatMonth）。
但每次只 sort 不同的 elements（按 avg_pct ），並**沒有 industry 去重**，導致同一產業在三個 section 下可能出現「重複卡片」。

**影響：**
散戶看到 grouped by industry 的 heatmap 誤以為系統在提示「某產業格外重要」。

**修復建議：**
```js
const industries = [...new Map(_heat.industries.map(i => [i.industry, i])).values()];
```

---

### 🔧 #12 — Tab 切換時 table scroll position 不歸零
**影響程度：** P2

**現象：**
從 tab A 切換至 tab B 再切的 tab A，table body 的 scrollTop 保持不變。
若散戶在 tab A Scroll 到下面資料，切換 tab B 再回頭，看到的是「錯誤的那一小段 table」（因為 filter / search 都還在）。

**重現：**
1. 大廳 tab + 搜尋 "光"
2. 看到結果 2383 在底部
3. Scroll 到 table 底部
4. 切到 tab ETF 再觀回大廳
5. 看到不是 "光" 的所有 stock 列表

**修復建議：**
```js
document.querySelector('.table-wrap')?.scrollTop = 0;
```
添加到切換函數/tab click handler 中。

---

### 🔧 #13 — 手機版 scroll 穿透（backdrop 觸控到背景）
**影響程度：** P2

**現象：**
ios Safari 上 `position: fixed` 元素 fixed 會被 ignore。若 scroll lock 沒做，在 sheet 覆蓋時手指滑動 backdrop → backdrop ** TranslateX(0)** bug 造成 sheet 同時被disable。

**修復建議：**
```css
body.sheet-open { overflow: hidden; }
/* + openSheet 時 add class sheet-open */
```

---

## 五、P3 低优先级（建議改進）

### 💡 #14 — Date 是 2026 未來年份，散戶以為是过期 mockup
**影響程度：** P3

**data.json** 有 `"updated": "2026-06-20"`。
除了 h1 問題，#headerDate 還有 `d.date` (為 "2026-06-19")。
散戶首次進入頁面 sees 未来日期，一   直以為是不是假的 demo。

**修復建議：**
自動填入 `new Date().toISOString().slice(0,10)` 或同一個 `d.date`。

---

### 💡 #15 — stock 列表HTML內插未 escape，潛在輕微 XSS
**影響程度：** P3

**s.name** / **s.note** 若透過 data.json 被注入 `<script>alert(1)</script>`，`innerHTML` 會直接執行動態程式碼。

**修復建議：**
```js
function esc(s){ return String(s||'').replace(/[<>&'"]/g, m => ({"<":"&lt;",">":"&gt;","&":"&amp;","'":"&#39;",'"":"&quot;"}[m])); }
```

---

### 💡 #16 — pctClass 未處理 null/undefined 返回 muted 正確
**場域：** renderLobby, renderSignals, renderChip
```js
function pctClass(p){ return p>0 ? 'up' : p<0 ? 'down' : 'muted'; }
```
(null 視為 muted) — 這是正確的行為。但因為 `s.pct` 通常在 null 時不應該出現（前面印出 null null%），差評放在本節的「相對測試」不處理。只要 Bug #3 被修好，就不會有這問題。

---

## 六、操作端到端 Smoke Test

| 步驟 | 操作 | 期望 | 結果 | 問題 |
|------|------|------|------|------|
| 1 | 首次載入大廳 | 39 支正確 / loader 消失 / 摘要卡 T1:6 T2:12 T3/T4:21 | ✅ | 成功 |
| 2 | 搜尋"台積" | list 只留台積電 1 列、countLabel="1 / 39" | ✅ | 成功 |
| 3 | 清空搜尋 | 39 列重現、countLabel="39/39" | ✅ | 成功 |
| 4 | 點 table header「收盤」| list 排序 台泥 $24.5 → 台光電 $5600 | ✅ | 成功 |
| 5 | 點台積名稱 | sheet 右側滑入，顯示價/量/分級/評分等欄 | ✅ | 但「近期趨勢」全 "--"、"持有邏輯" "--" |
| 6 | 點 ✕ 關閉 sheet | sheet 收回、回到大廳 | ⚠️ | 狀態偶爾殘留 overlay |
| 7 | Tab「信號」| 15 筆信號正確列出 | ✅ | 成功 |
| 8 | Tab「籌碼」| 依成交額分位排序 | ✅ | 但力旺 3529 顯示 null null% |
| 9 | Tab「產業熱力」| 三欄 grid (Day/Wk/Month)、industry card 可展開 | ✅ | 偶有重複卡片 |
| 10| Tab「ETF」| 下拉選 0050 → 對應成分股.grid-4 | ⚠️ | 整體功能正常，但背景動畫看不清 render |
| 11| Tab「資產」| 清空 → 加入台積電 → 卡片顯示 → 清空 | ✅ | hold risk 正確 reasoning；但她提到的「合成」 Industries 不精準 |
| 12 | ESC 關閉 sheet | 直接關閉 | ❌ | 未綁定事件 |
| 13 | 點擊 backdrop overlay | 關閉 sheet | ✅ | 根據 onclick this.stockDetail 有做 |

---

## 七、資料品質檢查 (data.json + etf.json)

| 問題 | 說明 | 修復 |
|------|------|------|
| 2383 台光電重複條目 | Tier T1 + Tier T4 同时存在，front-end 對他分級混亂 | 刪除其中之一，統一用 T1（因為就 data）|
| 3529 price=null, pct=null | 力旺無價無百分比且 vol=0 | 補全三個字段，或移除 3529 |
| 16/39 檔 vol=0 | ETF 成分股混入但無成交資訊 |  heatmap 手工補 fixed vol |
| ETF 00284a 為 6505 ETF | etf.json 內 00981A、00991A 中均有 `6505`，但 data.json 無 6505 | 導致 ETF tab 實際表現「缺少成分股」|
| ETF 00284a 為 00713b ETF | etf.json 內 00988A 有 `1216`，data.json 尚有 1216 統一，但不能 Vol=0 戶合診 | 重 visually 資料一致 |

---

## 八、修復優先序（建議）

| Priority | 預估工時 | 建議修復項 |
|---------|---------|---------|
| P0 | 1.5h | 1. duplicate 去重 2. null fallback 3. closeSheet lock 4. hold 欄位補 |
| P1 | 3h | 5. 近期趨勢資料來源 6. Concept pill 互動 7. th 三欄去 sorting cursor:pointer 8. .section margin 9. debounce search |
| P2 | 4h | 10. 0-vol ETF 路徑也動態補 11. heatmap 去重 12. scrollTop 歸零 13. iOS scroll lock |
| P3 | 1h | 14. 日期自動刷 15. XSS 防護 16. 自訂深色 mode 點綴 |

---

## 九、測試環境說明

- **瀏覽器：** Chrome / 德 James 117 (官網自用）
- **Viewport：** 桌面版（หนังสือ 約 1440px）
- **檔案：** `/home/ubuntu/investment/spa.html`（前端唯一檔案）/ `data.json` / `data/heatmap.json` / `data/etf.json`
- **browser.js 引入來源：** `gs.link.min.js`（外部 CDN）
- **關聯問題：** 整體載入暢通，無 JS exception 被 console 顯示，但設計良莠不齊。

---

*備註：本報告由 AI QA 代理執行，內容基於靜態代碼審查與 lived 互動截圖，以台股散戶視角撰寫。*
