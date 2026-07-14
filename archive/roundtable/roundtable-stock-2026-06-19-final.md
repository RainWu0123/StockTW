# Roundtable: 股票 — 訓練專業台股分析AI 會議總結
- date: 2026-06-19
- type: stock
- topic: 怎樣訓練出一個專業台股分析AI
- participants: 技術分析師, 籌碼分析師, 風控專員

---

## 總結

### 共識
1. 法人籌碼是台股 AI 的核心資訊，但不能只用總量加總，必須拆三法人分層分析
2. 資料品質優先於模型複雜度：實收數據、T+1 標註、上市櫃分群、制度事件對齊是基本門檻
3. 損失函數不能只優化 Accuracy，必須納入 max drawdown penalty、margin-call flow penalty 與制度流動性懲罰
4. RL 訓練環境必須內建模擬台股制度（當沖、融資維持率、處置股、漲跌停、除權息調整）
5. 價量結構、法人籌碼、風控三位一體，缺一不可

### 異議（未解決）
1. Event-Driven RL 是否可行：技術分析師主張保留但降級為「確認層」，籌碼分析師認為根本不可行
2. 法人時序特徵的領先性是否穩定：三人同意動態判定，但具體演算法未定
3. 族群共振的建模方式：graph-based RL vs sliding-window multi-event，成本與效果權衡未知

### 行動方案（3 個月）
1. **W1-2：資料層**
   - 建立法人籌碼時序 pipeline（連續買超天數、動能加速度、板塊同步係數）
   - 建立制度事件 calendar（處置宣告、除權息、ETF 權重調整、期貨結算）
   - 實收數據清洗 protocol：借券去重、外資重複申報過濾、回溯修正標記
2. **W3-4：特徵層**
   - 價量特徵改用還原價 + 除權息 flag
   - 法人特徵分三層（外資/投信/自營商）而非總量
   - 建立制度冷卻過濾層：處置股/全額交割直接下修權重為 0
3. **W5-8：模型層**
   - Baseline：tech 指標 + 籌碼特徵，跑 backtest 觀察 signal lag
   - 損失函數：加入 max drawdown penalty + margin-call flow penalty + 制度事件空窗期禁令
   - RL 環境：smallest viable 台股模擬，至少建模 T+0 當沖、融資維持率、漲跌停
4. **W9-12：整合層**
   - 三層防線架構：籌碼資料層 → 價量結構層 → 風控熔斷層
   - 建立 signal executability check：訊號輸出前先檢查「這檔票這週能讓我停損嗎？」

### 未來的圓桌會議
- 下次主題建議：「RL 模擬環境 smallest viable scope 定義」
- 需要確認：backtest 平台選擇、資料來源取得方式、法規限制

---

## Meta
- total_rounds: 3
- personas: 技術分析師, 籌碼分析師, 風控專員
- files_created: 6
  - /home/ubuntu/.hermes/memory/roundtable-stock-2026-06-19.md
  - /home/ubuntu/round2_tech_analyst_challenge.md
  - /home/ubuntu/roundtable-rebuttal-chip-analyst-R2.md
  - /home/ubuntu/roundtable_r2_risk_gaps.md
  - /home/ubuntu/roundtable_rebuttal_R3_technical_analyst.md
  - /home/ubuntu/roundtable_rebuttal_R3_chip_analyst.md
  - /home/ubuntu/roundtable_rebuttal_R3_risk_analyst.md (bonus note: this file was referenced; actual filename: /home/ubuntu/round3_risk_analyst_rebuttal.md per delegate output)
- notes: 股票圓桌第一版完整跑完三輪辯論，從「各自立場」→「互相挑戰」→「修正式共識」
