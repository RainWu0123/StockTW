# 四大科技巨頭的 AI CapEx 與估值重構：Microsoft、Amazon、Alphabet、Meta

**研究日期**：2026-08-19（台灣）  
**資料截止**：2026-08-19  
**來源文本**：KP@FOMOSoc《深入分析第60期：四大巨頭》使用者提供預覽  
**性質**：獨立續作與事實核對，不是付費原文重製  
**信心等級**：中  

> 結論：四家公司都在犧牲短期自由現金流購買 AI 產能，但不能因此一律視為毀滅價值。真正要比較的是「單位算力成本、模型控制、原生分發、變現形式」四條鏈能否把 CapEx 轉成增量營業利益。基準估值排序不是單看 PE，而是 Microsoft 用正常化 PE、Amazon 與 Alphabet 用 SOTP、Meta 用正常化 PE 並額外扣除折舊與 Reality Labs 風險。

## 先修正原文中最重要的事實邊界

原文關於 Alphabet Q2 CapEx 449億美元、FCF -59億美元，以及 Meta Q2 CapEx 310.8億美元、FCF 7.84億美元，均可由公司官方財報確認。[5][7]

Microsoft FY2026營收3318億美元、Azure全年營收突破1000億美元、Microsoft Cloud 2140億美元，以及OpenAI相關商業安排收入241億美元、期末應收帳款60億美元，也有公司財報與10-K支持。[1][2][3]

但「微軟已停止向OpenAI支付營收分潤」不能只靠預覽文字當成已確認事實。Microsoft與OpenAI在2026年2月的官方聯合聲明仍稱營收分享安排不變；4月27日雖宣布修訂協議，但公開可抓取頁面沒有足夠條款細節。因此本報告只採用10-K已揭露的241億美元收入與60億美元應收，不自行補完未公開合約條款。

---

# 第一章：Microsoft，不需要贏模型戰，但一定要贏成本與企業入口

Microsoft FY2026 Q4營收900億美元、營業利益406億美元；全年營收3318億美元、營業利益1552億美元。Azure Q4營收年增43%，全年Azure營收首次突破1000億美元；Microsoft 365 Copilot付費席次超過3000萬。[1][2]

## GPT不再獨家，反而降低單一供應商風險

Microsoft真正的護城河不是GPT本身，而是Windows、Microsoft 365、Teams、GitHub、Entra、Defender與Azure共同構成的企業工作入口。模型可以換，但企業身分、權限、資料與流程不會因另一模型便宜10%就整套搬走。

OpenAI可以向AWS或Oracle採購訓練算力，對Microsoft未必全是壞事：外部雲端替它承擔最重的前沿訓練CapEx，而Microsoft仍能靠Azure、企業分發、OpenAI商業收入與股權分享價值。但風險沒有消失。Microsoft FY2026來自OpenAI的商業安排收入241億美元，占總營收約7.3%；期末應收帳款60億美元，代表OpenAI仍是實質信用曝險。[3]

## CapEx品質判斷

Q4 CapEx為410億美元，約三分之二投入GPU、CPU等短壽命資產。管理層預期CY2026 CapEx約1750億美元，下一季超過500億美元；Azure需求仍高於可用產能。[2]

這表示短期毛利率壓力是真的，但並非沒有需求的盲目擴產。要盯的不是CapEx絕對值，而是Azure增量營收、Microsoft Cloud毛利率與每美元短壽命資產帶來多少增量營業利益。

## 自建估值

| 情境 | FY27調整後EPS | PE | 合理價 |
|---|---:|---:|---:|
| 空頭 | 18.7美元 | 22倍 | 411美元 |
| 基準 | 19.7美元 | 27倍 | 532美元 |
| 多頭 | 20.7美元 | 31倍 | 642美元 |

以2026年8月18日481.63美元計，基準上行約10%。[8]

**判斷**：HOLD／偏多。Microsoft不必擁有最強模型，但必須證明自研模型、Maia與路由能抵消折舊，並讓Copilot席次收入增速快於推理成本。

**估值交叉檢查**：若先從FY26調整後EPS 17.28美元扣除Q4一次性利益，再用FY27 EPS成長14%與30倍PE，合理價約582美元；本報告532美元採27倍PE，屬較保守版本。因此Microsoft基準合理帶應讀成 **532～582美元**，不是迷信單點。

**追蹤信號**：Azure成長是否維持40%以上、Cloud毛利率是否止跌、OpenAI應收帳款／收入比、非OpenAI RPO增速、Copilot付費席次與使用量。

---

# 第二章：Amazon，看整體PE會同時低估AWS、又高估零售

Amazon Q2營收2006億美元、年增20%；營業利益275億美元、年增43%。AWS營收422億美元、年增37%，營業利益166億美元，營益率約39.4%。廣告服務營收198億美元、年增26%。TTM營業現金流1614億美元，但FCF為-76億美元，主要因AI相關資產採購年增661億美元。[4]

## AWS才是估值核心，但廣告已成第二個高品質引擎

AWS占Q2營收約21%，卻貢獻約61%的營業利益。AWS年化營收已達1690億美元，AI與自研晶片業務年化收入都超過250億美元。[4]

Trainium的戰略不要求模型一定屬於Amazon。Amazon只要讓Anthropic、OpenAI與企業客戶願意使用Trainium，就能把自研晶片從成本工具變成對外收費商品。這是它與Google TPU相似的地方。

廣告則直接依附Amazon的交易意圖，具備高毛利與高可衡量ROI；Q2廣告成長26%，不應再藏在零售外殼裡一起給低倍數。[4]

## 為什麼用SOTP

- AWS：高成長、高毛利基礎設施平台。
- 廣告：高毛利交易意圖變現。
- 北美／國際零售：低毛利，但物流效率與第三方服務可改善。

把三者塞進單一PE，會因Anthropic一次性評價利益與零售薄利產生失真。Q2 EPS 5.75美元包含約534億美元非營業投資收益，不能直接年化。[4]

## 自建SOTP估值，廣告必須從零售殘值中扣除

| 情境 | AWS TTM收入倍數 | 廣告TTM收入倍數 | 零售及其他殘值收入倍數 | 投資資產折價 | 每股合理價 |
|---|---:|---:|---:|---:|---:|
| 空頭 | 6倍 | 5倍 | 0.8倍 | 帳面60% | 166美元 |
| 基準 | 8倍 | 7倍 | 1.1倍 | 帳面75% | 225美元 |
| 多頭 | 10倍 | 9倍 | 1.4倍 | 帳面90% | 284美元 |

這組估值使用官方TTM營收，並把廣告收入從非AWS殘值中扣除，避免重複計算。若改用未來12個月收入，合理價會往約285美元靠攏。因此Amazon合理帶為 **225～285美元**。以2026年8月18日259.45美元計，股價位於區間中段，沒有明顯安全邊際。[9]

**判斷**：HOLD。Amazon不是明顯泡沫，但目前也不是便宜；關鍵是AWS 37%成長能否維持，而不是Amazon整體PE看起來多少。

**追蹤信號**：AWS營收與營益率、Trainium外部收入、廣告增速、TTM FCF何時轉正、AI CapEx每瓦收入、零售營益率。

---

# 第三章：Alphabet，Gemini不必永遠第一，但不能落後到傷害搜尋意圖理解

Alphabet Q2營收1198億美元、年增24%；Google Services營收950億美元、營業利益395億美元；Google Cloud營收248億美元、年增82%，營業利益88億美元、營益率35.6%。Search & Other年增17%，YouTube Ads年增13%。Q2營業現金流391億美元、CapEx 449億美元，因此FCF為-59億美元；全年CapEx指引上修至1950～2050億美元。[5][6]

## Google需要Gemini變強嗎？需要，但不必每個榜單都第一

Gemini對Google有三個不同任務：

1. 在Search改善查詢理解、廣告相關性與新增查詢量。
2. 在Cloud成為企業AI與token消耗的產品引擎。
3. 在TPU上形成軟硬體閉環，降低每個token的履約成本。

因此，Gemini不必在所有benchmark擊敗GPT或Claude；但如果模型長期落後到使用者改變搜尋入口、企業不願在GCP部署、TPU無法吸引外部工作負載，才會真正傷害估值。

目前Q2數字反而證明變現已發生：Search成長17%、Cloud成長82%、Cloud backlog達5140億美元，近90% Fortune 100使用Gemini Enterprise。[5]

## TPU的價值比模型排行更耐久

TPU同時服務搜尋、YouTube推薦、Gemini與Cloud客戶。只要TPU能降低自有服務成本，便已創造價值；若再對外成為獨立系統銷售，才是額外選擇權。風險是專用ASIC對架構變化反應較慢，因此Google仍同時供應NVIDIA平台，避免單一路線鎖死。

## 自建SOTP估值與方法敏感度

| 方法 | 空頭 | 基準 | 多頭 | 說明 |
|---|---:|---:|---:|---|
| 分部收入倍數SOTP | 221美元 | 278美元 | 336美元 | 對Search給5～7倍、Cloud給8～12倍收入，另扣AI R&D並加入金融資產 |
| 分部營業利益SOTP | 300美元 | 397美元 | 525美元 | 對Services與Cloud正常化營業利益給20～35倍 |

收入倍數法對高毛利Search較保守，營業利益法則對Cloud高增長與Search韌性給較高價值。兩種方法差距很大，本身就是估值風險。Alphabet合理帶暫抓 **278～397美元**，中樞約340美元；以2026年8月18日344.20美元計，現價大致合理。[10]

**判斷**：HOLD。Google的風險不是Gemini某次跑分第二，而是AI查詢是否降低廣告密度、Cloud需求是否消化不了CapEx。

**追蹤信號**：Search查詢與廣告相關性、Cloud營益率、Cloud backlog轉收入速度、TPU外部營收、AI Mode單次回應成本、CapEx／增量營業利益。

---

# 第四章：Meta，低PE不是免費午餐，而是市場在賭折舊跑得比廣告快

Meta Q2營收608億美元、年增28%，但營業利益188億美元、年減8%，營益率由43%降至31%；EPS 6.18美元、年減13%。廣告曝光年增14%、單價年增12%，核心廣告機器仍強。Q2 CapEx 310.8億美元、FCF只剩7.84億美元，2026全年CapEx指引1300～1450億美元。[7]

## Meta的AI變現其實已經發生

廣告收入594億美元、年增27%；曝光與價格同時成長，代表AI推薦、排序與廣告工具仍在提高變現。這是Meta與模型公司的最大不同：它不需要向使用者收token費，只要AI讓內容更黏、廣告更準，收入就會上升。[7]

但成本曲線也在加速。Q2折舊攤銷64億美元、年增約46%；R&D達217億美元。Family of Apps營業利益234億美元，Reality Labs虧損46億美元。[7]

所以Meta低PE反映三個折價：

1. 折舊與AI人才成本增速高於廣告營收。
2. Reality Labs持續燒錢。
3. Meta沒有公共雲收入，龐大算力主要靠自身廣告與未來產品消化。

## 自建PE估值

| 情境 | 2027 EPS | PE | 合理價 |
|---|---:|---:|---:|
| 空頭 | 28美元 | 16倍 | 448美元 |
| 基準 | 34美元 | 19倍 | 646美元 |
| 多頭 | 40美元 | 23倍 | 920美元 |

以2026年8月18日543.67美元計，基準上行約19%。[11]

**判斷**：HOLD／高風險偏多。Meta不是因PE低就必然便宜；只有當廣告營收與FoA營業利益增速重新超過折舊、人事與Reality Labs虧損增速，低PE才會變成真正的估值錯配。

**估值交叉檢查**：若以2027營收2600億美元、38%標準化營益率、16%稅率與25.6億稀釋股計算，EPS約32.4美元；25倍PE對應約810美元。因CapEx仍是折舊的近5倍，本報告不直接採25倍作單點，而將Meta合理帶定為 **646～810美元**。

**追蹤信號**：廣告曝光×價格、FoA營業利益、折舊增速、CapEx／增量廣告營收、Reality Labs虧損、債務與現金差額、WhatsApp／企業AI的新收入。

---

# 四家公司放在同一張表，真正比較的是CapEx回收路徑

| 公司 | 矽 | 模型 | 分發 | 變現 | 基準合理帶 | 主要風險 |
|---|---|---|---|---|---:|---|
| Microsoft | Maia起步，仍偏NVIDIA | 多模型＋OpenAI＋自研 | 企業工作入口最強 | 席次＋用量 | 532～582美元 | Cloud毛利率、OpenAI信用曝險 |
| Amazon | Trainium／Graviton已商品化 | Bedrock多模型 | AWS＋電商 | 算力＋廣告＋零售 | 225～285美元 | FCF轉負、AI CapEx過度 |
| Alphabet | TPU最成熟 | Gemini全棧 | Search／YouTube／Android | 廣告＋Cloud | 278～397美元 | 搜尋被侵蝕、CapEx消化 |
| Meta | MTIA仍在追趕 | 自研＋外購 | 社交圖譜與內容流最強 | 廣告 | 646～810美元 | 折舊、人才、Reality Labs |

## 最終排序

### 風險調整後品質

1. **Microsoft**：企業入口與軟體訂閱最穩，模型可替換。
2. **Alphabet**：TPU、Gemini、Search、Cloud最完整，但現價已反映不少好消息。
3. **Amazon**：AWS與廣告強，但FCF壓力最大，現價落在合理帶中段。
4. **Meta**：廣告本業最直接受惠AI，估值有重估空間，但成本與折舊可見度最低。

### 估值上行空間

1. **Meta**：合理帶646～810美元，潛在重估最大，風險也最大。
2. **Microsoft**：合理帶532～582美元，風險調整後較均衡。
3. **Amazon**：225～285美元，現價約259美元，接近合理。
4. **Alphabet**：278～397美元，方法差異極大，現價約344美元落在中間。

## 真正的投資結論

- Microsoft失去GPT算力獨家不是核心問題，只要它仍掌握企業入口、商業分發與成本路由，模型多元化反而能提高議價權。
- Amazon不能因整體PE高就判定昂貴；AWS與廣告需要分拆估值，但目前價格已要求AWS高速成長延續。
- Google不需要Gemini永遠第一，卻需要它足夠強，才能守住Search、推動Cloud並讓TPU變成利潤中心。
- Meta的低PE是對折舊、AI人才、Reality Labs與缺乏公共雲收入的折價，不是免費便宜；若廣告增長重新快過成本曲線，才是四家裡彈性最大的重估標的。

## Sources

[1] https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast — Microsoft FY2026 Q4 results
[2] https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4 — Microsoft FY2026 Q4 earnings call
[3] https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm — Microsoft FY2026 10-K
[4] https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results/default.aspx — Amazon 2026 Q2 results
[5] https://abc.xyz/investor/events/event-details/2026/2026-Q2-Earnings-Call-2026-GgTAq7Is0z/default.aspx — Alphabet 2026 Q2 earnings call
[6] https://abc.xyz/investor/news/news-details/2026/Alphabet-Announces-Second-Quarter-2026-Results-2026-Y3uQ6H4ZJa/default.aspx — Alphabet 2026 Q2 results
[7] https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/default.aspx — Meta 2026 Q2 results
[8] https://exa.ai/library/markets/stock/MSFT
[9] https://exa.ai/library/markets/stock/AMZN
[10] https://exa.ai/library/markets/stock/GOOGL
[11] https://exa.ai/library/markets/stock/META
