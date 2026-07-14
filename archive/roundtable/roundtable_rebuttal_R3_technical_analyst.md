# Round 3 — 技術分析師 R3 修正式立場

**角色：** 技術分析師  
**辯論脈絡：**  
- Round 1 主張：1)籌碼面+價量結構雙軌數據集  2)強化月線/季線均線判讀  3)法人+族群事件驅動學習  
- Round 2 被籌碼分析師反駁（法人落後一期、事件episode邊界不清、稀疏reward、忽略資料品質），被風控專員補刀（處置股/全額交割會讓突破訊號失真、除權息造成假跳空、融資維持率被動賣壓）

---

## 格式

### 一、堅持不變

1. **價量結構仍是技術面最強的 predictive feature**  
   - 月線/季線均線的趨勢濾網、量價背離、突破回測，在台股仍具有高顯著性。多數行情的發動與結束，價量結構是最先發出的訊號，法人數據往往只是確認或落後。

2. **雙軌數據集（技術面 + 籌碼面）的架構方向不變**  
   - 技術面負責「何時發動」、籌碼面負責「發動的純度」。但承認 Round 1 將兩者混為單一 event-driven RL state space 是過度簡化。

3. **族群/板塊共振的判讀價值不變**  
   - 族群共振確實是多空轉折的強力指標，問題在於 Round 1 的單一股票 episode 設計無法捕捉這層結構，而非共振概念本身有誤。

---

### 二、根據反駁調整的

#### 1. 法人數據的「落後一期」問題 → 改為「lag-aware feature engineering」

- **接受反駁：** 三大法人日買賣超确实是 T+1 才生效，event-driven RL 若將法人數據直接作為 state feature 會引入 lookahead bias 或估算 noise。
- **調整方案：**
  - 法人數據不作為即時 state，而是作為 **「確認層特徵」**：在突破發生後 T+1 至 T+3 的 validation window 內，才嵌入法人動態數據（連買天數、動能加速度、板塊同步係數）。
  - 訓練時明確標註 `legal_person_lag = 1 trading_day`，避免 agent 誤學到法人數據與價格的即時因果關係。
  - 法人方向轉為 **「特徵確認器」**：若突破發生後法人未跟進（或反向賣超），即使技術面強勢，訊號權重主動降級。

#### 2. Event-Driven RL 的 episode 邊界不清 → 改為「多事件重疊狀態標註」

- **接受反駁：** 台股事件重疊且連續，單一事件的 episode boundary 會導致 reward 嚴重偏誤。
- **調整方案：**
  - 放棄 strict episode boundary，改採 **sliding-window multi-event state**。
  - 每個時間點標註同時作用的狀態向量：
    - `is_legal_person_consecutive`：法人連續買賣超（可疊加）
    - `is_sector_resonance`：族群融資/法人共振
    - `is_technical_breakout`：月線/季線突破
    - `is_margin_call_risk`：融資維持率壓力（與風控整合）
  - Reward 函數改為 **階層式 weighting**：基礎 reward 來自技術面，法人確認層提供 ±20% 的 reward adjustment，而非直接驅動 action。
  - 這樣 RL agent 學到的是「多事件融合下的部位調整」，而非「等單一事件 → 下單 → 平倉」的僵化 episode。

#### 3. 稀疏 reward + 過擬合歷史題材 → 改為「主題不變性 (theme-invariant) 特徵 + 少樣本正則化」

- **接受反駁：** 法人題材歷史樣本極少，直接訓練會過擬合當年族群節奏。
- **調整方案：**
  - 法人數據不再以「年度族群」為單位，而是抽象為 **「籌碼動能加速度」**、**「法人連續天數動能」** 等不隨主題變動的數學特徵。
  - 引入 **domain randomization**：訓練時隨機遮擋特定法人事件（模擬不同年份的主題差異），迫使模型學習更結構化的籌碼模式。
  - 與籌碼分析師協調：優先使用他建立的「法人籌碼時序標註資料集」作為 reinforcement signal，而非 raw 法人數據。

#### 4. 忽略上市櫃/興櫃資料品質差異 → 改為「市場分層 + 實收數據強制要求」

- **接受反駁：** 上市、上櫃、興櫃的法人披露規則、股權結構、散戶比例不同，混練會造成策略泛化失效。
- **調整方案：**
  - 數據集明確分為 `TWSE`、`TPEx`、`Emerging` 三層。
  - 模型架構採用 **market-type embedding**：訓練時先預測 market type，再進入對應的技術/籌碼特徵處理路徑。
  - 數據 pipeline 強制要求 **實收數據**（非盤中估算），並與籌碼分析師的数据集使用相同的 T+1 標註時間戳，避免 lookahead。

#### 5. 單一股票 episode 無法捕捉族群共振 → 改為「圖結構 RL (Graph-based RL)」

- **接受反駁：** 單一股票的 event-driven RL 確實看不到板塊層級共振。
- **調整方案：**
  - 提升為 **sector-level graph representation**：每個股票節點連接其板塊中心股票，板塊共振指數作為額外 state feature。
  - Agent 在 graph 上執行部位配置：可以同时持有板塊內的多檔個股，reward 包含板塊級賺賠結構。
  - 這是 Round 1 主張的延伸，但從單一股票 episode 升級為 graph-based MDP，解決籌碼分析師指出的共振不可見問題。

---

### 三、新納入的風控 / 制度考量

#### 1. 制度冷卻層（Institutional Cooldown Filter）— 接受風控專員補刀

- **問題：** 處置股（10 分鐘撮合、流動性稀釋）、全額交割股（散戶撤離、技術訊號失真），會讓技術面的突破回測出現大量假訊號。
- **新作法：**
  - Data pipeline 必須先過濾：`is_designated_security = True`、`is_cash_delivery_required = True` 的股票，直接排除於訊號池之外。
  - 若非要保留（例如觀察研究用途），則在 reward 函數中加入 **處置期流動性懲罰**（liquidity penalty = 1 / 當日成交股數），模擬滑價與 Execution Risk。
  - 在 RL 模擬環境中，這類股票進入被處置狀態時，強制觸發 `trading_halted`，agent 無法再增減部位。

#### 2. 除權息價格修正規則

- **問題：** 除權息會造成人為缺口，技術面模型容易誤判為技術性跳空。
- **新作法：**
  - 所有價格特徵一律使用 **還原價**（adjusted close）。
  - 在 state space 中增加 `ex_dividend_flag`、`cash_dividend_amount`、`ex_rights_flag`、`rights_price` 四因子。
  - 模型學會識別「這是制度造成的人為缺口」而非「市場行為造成的大力出擊」。

#### 3. 融資維持率被動賣壓的懲罰機制

- **問題：** 融資維持率不足引發強制賣出，形成螺旋下跌，這是 max drawdown 的主要來源，技術面完全無法預判。
- **新作法：**
  - 損失函數新增 **margin-call flow penalty**：
    - 計算 `margin_call_pressure = f(maintenance_ratio, stock_price, margin_balance)`。
    - 當壓力高於臨界值時，即使 model 未要求賣出，也將被動賣出視為 execution cost，從 reward 中扣除。
  - 這迫使模型學會在融資余額創高、維持率逼近警戒線時，主動減碼或避開，而非等到螺旋下跌才反應。

#### 4. 「訊號可執行性」成為特徵篩選的前置條件

- **問題：** 技術分析師的均線/突破訊號建立在「本週可自由買賣」的假設上，但處置/額全交割讓這個假設不成立。
- **新作法：**
  - 建立 **signal executability check**：
    - 近 5 日平均成交股數 > threshold（避免成交極度萎縮）
    - 無處置或全額交割標記
    - 融資維持率未達邊緣警戒（margin_ratio > 130%）
  - 只有通過 executable check 的股票，才進入技術面訊號生成流程。
  - 這是風控專員說的：「強化月線/季線之前，先問『這檔票這週能讓我停損嗎？』」的制度化實踐。

#### 5. RL reward 設計：從 PnL 導向改為「Adjusted Liquidity PnL」

- **問題：** 純 PnL reward 會忽視制度性的 execution cost。
- **新作法：**
  - `reward = raw_pnl * liquidity_factor - execution_cost`
  - `liquidity_factor`：
    - 處置期 = 0.3（高滑價、低流動性）
    - 全額交割 = 0.5
    - 正常 = 1.0
  - 這樣 RL 不會被處置股的假突破訊號誘惑，因為即使預測正確，adjusted reward 也會極低。

---

## 總結

| 面向 | Round 1 原主張 | Round 3 修正式立場 |
|------|---------------|--------------------|
| 法人數據 | 直接作為 state feature | 改為 lag-aware 確認層，T+1 嵌入，提供 reward adjustment |
| Event-driven RL | 單一事件 episode | 放棄 strict episode，改用 sliding-window multi-event state；獎勵函數階層式加權 |
| 稀疏樣本 | 直接用法人題材 | 抽象為不變數學特徵 + domain randomization |
| 上市櫃差異 | 未提及 | Market-type embedding，市場分層訓練 |
| 板塊共振 | 主張但未實踐 | 升級為 sector-level graph-based RL |
| 制度風險（風控補刀） | 完全忽略 | 制度冷卻層 + 流動性過濾 + 還原價格 + margin-call penalty + signal executability check |

**與籌碼分析師的和解方向：**  
我的修正式立場已將法人數據從「即時驅動」降級為「確認層」，並改用他建議的「法人籌碼時序標註資料集」作為 reinforcement signal。未來可進一步協調：技術面突破事件由其籌碼特徵進行评分，雙方的數據集對齊 T+1 標註，合力構建 clean feature space。

**與風控專員的和解方向：**  
五項制度性風控（處置/全額交割/融資維持率/除權息/signal executability）將作為模型的前置門檻與損失函數懲罰項，技術訊號必須通過制度監控後才能觸發。
