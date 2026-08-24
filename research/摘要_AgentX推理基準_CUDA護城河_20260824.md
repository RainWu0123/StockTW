---
title: "摘要：AgentX / InferenceXv3 — CUDA 護城河在 agentic 推理下是否成立"
source_author: "Cam Quilici, Bryan Shan, Alec Ibarra 等（SemiAnalysis）"
source_name: "SemiAnalysis（付費牆）"
source_url: "https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat"
published_at: "2026-08-24"
archived_at: "2026-08-24"
sources_as_of: "2026-08-24"
relation_to_thesis: "new-angle"
bindings_to_reobtain: ["各模型 perf/$ 排名", "B200/B300/MI355X 相對表現", "Rubin 測試結果（尚未公布）", "AMD ATOM upstream 進度"]
verification_guardrail: "引用前確認 AgentX 更新文（數週內）與 Rubin 測試結果是否已出，AMD 是否已把 ATOM 優化 upstream 回 vLLM/SGLang；模型排名會隨上游 PR 快速變動。"
requires_thesis_review: false
related_symbols: [2330, 2317, 2382, 3231, 2356, 6669, 2344, 8299, 4979, 6274, 6442, 3163, 3081, 4971, 2345, 3017, 8210, 2308, 2360, 2449, 6830, 6223, 6187, 3037, 8046, 2368, 2383, 4958, 6269, 3661, 3443]
---

> 一句話：agentic 推理把 CUDA 護城河從「kernel 生態」升級成「分散式系統棧生態」；對 NVIDIA 供應鏈整體是確認性利多，但 AI 錢的分配排序改變：HBM、光互連、散熱電源加分，純 GPU 組裝故事被稀釋。

## 來源主張

1. **AgentX 是業界第一個以真實 agentic 工作負載為主的開源推理基準**。重放 393 個匿名化 Claude Code session（中位數輸入 142k tokens、44% 有 subagent、最長 1M context），在超過 2MW、上千顆晶片上跑（GB300 NVL72、GB200 NVL72、B300/B200、H200、MI355X、MI325X 等）。建置成本超過 300 萬美元，全開源。
2. **Agentic 工作負載是系統工程問題，不是單晶片問題**：多輪長上下文使 prefix 重用率趨近 100%（實測 95%+ KV cache hit rate）；瓶頸移到 HBM 容量（KV cache working set）、跨節點 KV 傳輸（NIXL/Mooncake/LMCache）、路由親和性（Dynamo、llm-d）、PD 分離與 context parallelism。
3. **CUDA 護城河仍成立，但形態改變**：
   - 晶片硬體差距不大：MI355X 在低吞吐段與 B200/B300 有來有往，HBM 甚至更多。
   - 軟體差距巨大且集中在 agentic 場景：AMD 的 DCP/PCP 未優化、KV offload 傳輸效率差（`hipMemcpyBatchAsync` 到 ROCm 7.14 才補）、RDMA 支援殘缺。
   - 護城河新形態是「分散式推理系統棧」：Dynamo router、NIXL、DCP/PCP、TRT-LLM boundary-aware tokenization，多為 NVIDIA Research 發明或主導。
4. **各模型實測分歧大**：DeepSeek V4 Pro 接近五五波；Kimi K3 上 MI355X ATOM 部分段贏 GB300 vLLM 但 ATOM 生產環境沒人用；MiniMax M3 與 Qwen3.5 NVIDIA 完勝；GLM 5.3 NVIDIA 成本效率好 5 倍。「就算 AMD 晶片免費送，用 NVIDIA 每 token 成本仍更低。」
5. **反直覺觀察**：GB200/GB300 rack-scale 在 M3 上反而輸單機 B200/B300，因 Dynamo router 工作量隨 live prefix 數量增長變成瓶頸。rack-scale 不是自動更強。
6. **電力是真約束**：perf/MW 是 frontier labs 的核心指標，「錢是社會建構、電力是物理現實」。

## 對追蹤股票庫的影響（分診結論）

**總判斷：非利空。對 NVIDIA 供應鏈整體確認性利多，但改變「哪些環節吃得到 AI 錢」的排序。信心等級：中高（方向明確，個股彈性未量化）。**

| 環節 | 受惠股票 | 方向 | 邏輯 |
|---|---|---|---|
| HBM / KV cache 分層儲存 | 2344 華邦電、8299 群聯 | 加分最多 | B300 TCO 優勢主要來自 HBM 多 50%；KV offload 到 DRAM 已標配、NVMe 在路上 |
| 光互連 / 網通 | 2345 智邦、6274 台燿、6442 光聖、3163 波若威、3081 聯亞、4971 IET-KY、4979 華星光 | 加分 | PD 分離、wide-EP 加劇東西向流量；與華星光研究 CW Laser/800G ZR 邏輯同源 |
| rack-scale 組裝 | 2317 鴻海、2382 廣達、3231 緯創、6669 緯穎 | 正面但打折 | NVL72 出貨邏輯強化，但 rack-scale 滲透可能比市場線性外推慢（router 瓶頸） |
| 散熱 / 電源 | 3017 奇鋐、8210 勤誠、2308 台達電 | 加分 | perf/MW 約束下推理密度與 rack 功耗持續上升 |
| 測試 / 驗證 | 2360 致茂、2449 京元電子、6830 汎銓、6223 旺矽、6187 萬潤 | 慢變數加分 | 軟體棧正確性（silently wrong output）成為新測試需求 |
| ABF / CCL | 3037 欣興、8046 南電、2368 金像電、2383 台光電、4958 臻鼎、6269 台郡 | 中性正面 | GB300/B300 平台放量邏輯不變 |
| ASIC 線 | 3661 世芯、3443 創意 | 雙向風險 | TPU 年內加入測試：TPU 數字好是題材加持，Rubin 壓制則壓縮 ASIC 敘事 |
| 金融／電信／航運／傳產 | 2880-2892、3045、4904、2603/2615/2610/2618 等 | 無直接影響 | 間接：資金續留科技股時，2885/2890 證券獲利邏輯續成立 |

### 操作 takeaway

1. **換框架看 AI 硬體股**：瓶頸從 FLOPs 移到 HBM 容量、記憶體頻寬、互連頻寬與軟體棧。選股權重往 HBM、光互連、散熱電源傾斜，純 GPU 組裝故事彈性下降。
2. **盯兩個事件**：Rubin 測試結果（本月稍晚加入基準）；AgentX 更新文（幾週內，看 AMD 是否把 ATOM 優化 upstream 回 vLLM/SGLang——那是 AMD 鏈有無 second half 故事的真訊號）。
3. **風險監控點**：推理效率改善速度極快（70+ 上游 PR、數個月 double-digit 吞吐提升）。目前支持 Jevons 反論（更省→更多人用→總量更大），但若效率曲線明顯快過用量增長，市場會質疑硬體 capex 永永續性，屆時高估值 AI 硬體股會一起殺。現在不需動作，列入監控。

## 對既有研究的關係

- **new-angle**：為 AI 供應鏈研究提供新的評估維度——「agentic 負載下的系統棧地位」，可作為 HBM／光互連／散熱檔的 Driver Chain 增補依據。
- 與 `摘要_AI_Infra效率革命_GPU利用率_硅谷101_20260731.md`、`research/4979_華星光.md` 的光互連邏輯同源互補。
- 不觸發任何正式 thesis 重寫；`requires_thesis_review: false`。

## 待查證與下一步

- [ ] Rubin InferenceX 測試結果（來源承諾本月內）
- [ ] AgentX 更新文：AMD ATOM 是否 upstream 回 vLLM/SGLang
- [ ] MI455X UALoE72 與 TPU 加入基準後的排名變化
- [ ] 若要量化個股彈性，需另行驗證各公司實際 NVL72/HBM 出貨佔比（本素材不含）

原文全文存檔：`~/.hermes/cache/web/newsletter.semianalysis.com-ef7c166428.md`
