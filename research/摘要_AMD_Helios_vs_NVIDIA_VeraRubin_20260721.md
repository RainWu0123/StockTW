# 摘要：AMD Helios vs. NVIDIA Vera Rubin NVL72 機櫃對比（Andrew Lu 報告）

**來源**: Andrew Lu on global Semi/Techs（付費 Substack）  
**發布**: 2026-07-21  
**標題**: Time to compare AMD Helios vs. Nvidia Vera Rubin NVL72 rack  
**落盤日期**: 2026-07-21  
**取得來源**: 製作人 RainWu0123 轉貼（executive summary + 第 1 點完整；2–6 點為付費牆後內容，本檔僅能引用已知架構對比，不揣測未見細節）

---

## 一、事件背景（一手可核部分）

**今日（2026-07-21）Microsoft 宣布採購 AMD Helios 機櫃平台（GPU/CPU）**，整合進 Azure AI，提供三類雲服務：

| 服務 | VM 名稱 | 用途 |
|------|---------|------|
| 數據處理 | Azure HDv2 VMs | 高密度數據處理 |
| 半導體 EDA | Azure HXv2 VMs | 晶片電子設計自動化 |
| AI 推理 | ND MI455 v7 VMs | AI 推理服務 |

**先前已簽 AMD MI455/Helios 訂單的客戶**：
- **OpenAI**：6GW 算力（近零成本認股權證結構）
- **Meta**：6GW 算力（近零成本認股權證）
- **Oracle**：（先前已簽）
- **Microsoft**：（本次新增）

合計四大超大客戶已全數押注 AMD Helios。市場解讀為 AMD 在 AI 機櫃市場對 NVIDIA 的首次系統性挑戰。

---

## 二、Andrew Lu 的核心結論

**儘管 Helios 連拿下四大客戶，Andrew Lu 認為**：

> AMD 除了在開源軟體、開放互聯架構、整櫃 CPU 核心數及 HBM4 容量有 45–50% 優勢外，在**系統定價、總耗能、機櫃尺寸**仍處劣勢，**互聯技術也沒有明顯優勢**。

> AMD 要從 NVIDIA 搶下更多機櫃份額，可能需等到下一代能跟 **Rosa Feynman** 真正競爭的產品。

**白話**：客戶簽了，不等於產品真的贏；現世代 Helios 在性價比上對 Vera Rubin 仍是劣勢，規格贏但成本／能耗輸。

---

## 三、6 個關鍵差異（一覽）

付費牆僅開放第 1 點完整內容；2–6 點為標題層級，本檔如實呈現可見部分，**不揣測付費牆後細節**。

### ✅ 第 1 點：NVIDIA 在系統定價勝出（完整）

| 比較項目 | NVIDIA Vera Rubin NVL72 | AMD Helios |
|----------|-------------------------|------------|
| 互聯晶片 | 9 顆昂貴 **NVLink 6 Switch** | 6 套標準化**乙太網 Switch** |
| 背板 | 專利**銅纜背板** | OCP 開放架構＋乙太網網卡（Pensando Vulcano） |
| CPU | Vera CPU（溢價） | 18 顆 Venice CPU |
| HBM4 容量 | 較少 | **多出 50% 的 31TB HBM4** |
| 整櫃售價 | **350–400 萬美元** | **500–550 萬美元** |
| 價差 | — | 比 NVIDIA 貴 **35–45%** |
| 利潤率 | Gross Margin 極高 | 受 BOM 壓力 |

**Andrew Lu 的判斷**：

- AMD 硬體 BOM 本應有競爭力（標準化乙太網 vs. 專利 NVLink）。
- 但 Helios 堆疊比 Vera Rubin 多 50% 的 31TB HBM4 → BOM 反而高。
- 整櫃售價 **500–550 萬 vs. NVIDIA 350–400 萬** → 貴 35–45%。
- **除非 Helios 在算力能大幅降低 cost per token（每 token 成本），否則這價格毫無競爭力。**

**關鍵追問**：Helios 的競爭力假設取決於 **cost per token** 是否能抵銷 35–45% 的售價劣勢。Andrew Lu 沒在第 1 點結論中給肯定答覆，暗示**大概率無法抵銷**，這也是他整篇「定價劣勢」決定的支點。

### 第 2–6 點：付費牆後

| # | 標題可見 | 內容 | 狀態 |
|---|----------|------|------|
| 2 | 架構核心數差異 | 未見 | 付費 |
| 3 | HBM4 容量差異 | 第 1 點已透露 AMD 多 50%（31TB） | 部分 |
| 4 | 互聯技術差異 | 第 1 點已透露 NVLink 6 vs. 乙太網+Pensando | 部分 |
| 5 | 耗能及機櫃重量差異 | 未見，Andrew 結論已說「AMD 劣勢」 | 推測 |
| 6 | 軟體生態差異 | 未見，Andrew 結論已說「AMD 唯一優勢」 | 推測 |

**紀律標註**：本檔不為第 2、5、6 點填空。製作人若要完整對比，需取得 Andrew Lu 付費訂閱。

---

## 四、與既有研究交叉

| Andrew Lu 報告 | 我們既有檔案 |
|----------------|--------------|
| Vera Rubin NVL72 LPDDR5X 容量砍 1/4（極端） | `摘要_存儲跳水多重利空_20260716.md` 已記（廣發 7/2 分析轉述，高不確定）|
| NVIDIA NVLink 6 Switch × 9 | 先前已記（晶片高利潤率核心） |
| 廣達 Vera Rubin 出貨動態 | `money.udn.com` cache 已記廣達月季營收雙新高受 VR 帶動 |
| 立隆電（2472）打入 Vera Rubin 平台 | `readmo.cmoney.tw` cache 已記，高階電源管理需求受惠 |
| 奇鋐（3017）VR 散熱案 | `tw.stock.yahoo.com` cache 已記，Q1 EPS 20.17 元、伺服器占 66.4% |
| HBM4 容量戰 | 與日前「記憶體 5 倍 P/E」討論接面：若 AMD 堆 31TB HBM4，對 HBM 需求量是利多 |

**台股供應鏈接面**（憑既有研究，非 Andrew Lu 本文明確提及）：
- **HBM4 多 50%** → SK 海力士／三星 HBM4 產能去化受惠；若 AMD 抓 HBM4 訂單，對**台積電 CoWoS 先進封裝**也是量能
- 廣達同時是 NVIDIA Vera Rubin 與 AMD Helios ODM 候選 → 雙邊押注，機櫃組裝受惠不論誰贏
- 散熱（奇鋐、雙鴻）受惠不論陣營，因功耗都是上升

---

## 五、對你研究的意義（推測層級）

**1. 「NVIDIA 獨霸」敘事裂縫確認**

- OpenAI／Meta 各 6GW ＋ Oracle ＋ Microsoft ＝ **四大超大客戶都簽 AMD Helios**
- 這是市場情緒面對 NVIDIA 壟斷的首次系統性挑戰
- **但 Andrew Lu 提醒**：簽約不等於規格贏，定價劣勢 35–45% 是硬傷

**2. NVIDIA 護城河的真實位置**

- **不是 GPU 本身**，是：**NVLink 生態＋銅纜背板＋CUDA 軟體＋利潤率**
- AMD 想用乙太網＋開放架構＋低價 CPU 打進來，但 HBM4 堆太多反而蓋過成本優勢
- 真正決戰在 cost per token，不是單價

**3. 對台股的接面**

- 不論 AMD Helios 或 NVIDIA Vera Rubin 誰出貨多，**台積電 CoWoS／HBM4 封裝都吃**
- 廣達雙邊押，**ODM 受惠不論陣營**
- 散熱族群（奇鋐、雙鴻）純看總功耗上升，**不論陣營**
- 真正的分叉：**NVIDIA 利潤率若因 AMD 競爭被拉低，台積電的定價權是否連動被砍？** 這才是長線觀察點。

**4. 對你「Forward P/E 5x」討論的延伸**

- 若 AMD 用 near-zero-cost warrant 簽下客戶，等於 **AMD 把 GPU 當贈品換 AI 雲端市場份額**
- NVIDIA 的因應若也是降價／增加綁定，會壓縮 NVIDIA GM → 影響 Forward E
- **這是第 1 層「5x P/E 市場不信 E」的具體傳導機制**：不是 E 自動下修，而是**競爭結構把 E 拉下來**
- 雲端巨頭用 AMD 來壓 NVIDIA 價格，NVIDIA 不降就掉份額，降了 GM 縮水 → Forward P/E 從 5x 變 6–7x

---

## 六、品質標註

| 項目 | 評估 |
|------|------|
| Microsoft 採購 Helios 宣布 | 一手可核（Microsoft 官方） |
| OpenAI／Meta 6GW 各 + 近零成本認股權證 | 轉述，量級可信但需 Andrew Lu 來源註記 |
| 整櫃售價 500–550 vs 350–400 萬美元 | Andrew Lu 估算，量級合理，未見 NVIDIA／AMD 官方確認 |
| AMD HBM4 多 50%／31TB | 規格數字，可信但未核官方 datasheet |
| NVLink 6 × 9 vs. 乙太網 Switch × 6 | 架構對比，邏輯合理 |
| 「Rosa Feynman 才能真正競爭」 | Andrew Lu 個人判斷，非事實 |
| 整體傾向 | 看多 NVIDIA 護城河，對 AMD 短期份額轉換持悲觀 |
| 付費牆限制 | 第 2–6 點未取得，本檔如實標註 |
