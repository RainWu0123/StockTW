#!/usr/bin/env python3
import requests
import time

NOTION_TOKEN=*** DERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
BASE_URL = "https://api.notion.com/v1"

def api(method, endpoint, body=None):
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"
    resp = requests.request(method, url, headers=HEADERS, json=body, timeout=30)
    if resp.status_code >= 400:
        print(f"ERROR {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        return None
    return resp.json()

def create(parent_id, title, children=None):
    body = {"parent": {"page_id": parent_id}, "properties": {"title": {"title": [{"text": {"content": title}}]}}}
    if children:
        body["children"] = children
    r = api("POST", "pages", body)
    print(f"  {'OK' if r else 'FAIL'}: {title}")
    return r

# 1) root
search = api("POST", "search", {"filter": {"property": "object", "value": "page"}, "page_size": 20})
results = search.get("results", []) if search else []
parent_id = next((p["id"] for p in results if p.get("parent", {}).get("type") == "workspace"), results[0]["id"])
root = create(parent_id, "台股 AI 投資追蹤", children=[
    {"type": "callout", "callout": {"icon": {"type": "emoji", "emoji": "🤖"}, "rich_text": [{"type": "text", "text": {"content": "本資料夾由 Hermes Agent 自動維護，每日 TWSE 收盤後自動更新。"}}]}},
    {"type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "每日選股邏輯摘要"}}]}},
    {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "營收確認型（T1）：持有 7-30 天"}}]}},
    {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "動能爆發型（T2）：持有 1-7 天"}}]}},
    {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "題材短打型（T3）：持有 1-3 天"}}]}},
    {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "觀察不追（T4）：等明確訊號"}}]}},
])
if not root:
    raise SystemExit(1)
time.sleep(0.4)

THEMES = {
    "AI 基礎建設（被動元件/電源/散熱）": [
        ("國巨 (2327)", "T1", "1080", "+9.76%"), ("台達電 (2308)", "T1", "2150", "-0.23%"),
        ("奇鋐 (3017)", "T2", "2400", "+1.48%"), ("凱美 (2375)", "T3", "219", "+9.77%"),
    ],
    "AI 先進封裝（CoWoS/ABF/CPO）": [
        ("台光電 (2383)", "T1", "5600", "+7.69%"), ("日月光投控 (3711)", "T2", "613", "+3.03%"),
        ("華通 (2313)", "T4", "259.5", "-1.70%"), ("光聖 (6442)", "T3", "1945", "+6.00%"),
        ("聯電 (2303)", "T2", "145.5", "+3.93%"), ("力成 (6239)", "T4", "363.5", "+5.36%"),
    ],
    "AI 記憶體（DRAM/HBM）": [
        ("南亞科 (2408)", "T2", "459.5", "+5.15%"), ("華邦電 (2344)", "T2", "218.5", "+9.80%"),
    ],
    "AI 運算平台（IC設計/Edge AI）": [
        ("台積電 (2330)", "T1", "2410", "+1.05%"), ("聯發科 (2454)", "T1", "4390", "-1.57%"),
        ("凌華 (6166)", "T2", "155.5", "+9.12%"), ("研華 (2395)", "T4", "494", "+1.12%"),
        ("啟碁 (6285)", "T4", "274", "+1.29%"), ("創意 (3443)", "T4", "4860", "-4.24%"),
    ],
    "地緣題材短打": [
        ("聯友金屬 (7610)", "T3", "2315", "+9.98%"),
    ],
    "其他觀察": [
        ("大立光 (3008)", "T4", "5195", "+0.97%"), ("漢唐 (2404)", "T4", "1265", "-1.17%"),
        ("汎銓 (6830)", "T4", "564", "+9.94%"),
    ],
}
LOGICS = {
    "國巨 (2327)": "被動元件龍頭，AI伺服器 MLCC/電阻需求爆發，5 月營收 +47%，00981A/00992A/00991A 三大冠軍 ETF 同步加碼",
    "台達電 (2308)": "AI 伺服器電源 + 液冷散熱雙主軸，2026 首季營收創高 +34%，伺服器電源占營收逾 20%",
    "奇鋐 (3017)": "液冷散熱台廠第一，Google/微軟/NVIDIA 訂單能見度到 2029，外資升評至 3333",
    "凱美 (2375)": "AI 電感/MLCC 彈性最大，Q1 EPS +572%，00981A 近期掃貨，體量小但動能強",
    "台光電 (2383)": "NVIDIA M9 供應商，ABF/PCB 雙引擎，2026 營收年增 35%+，外資看 2027 成長 39%",
    "日月光投控 (3711)": "CoWoS 產能溢訂單最大受惠，先進封裝占營收比重持續提升，今日 +3% 創新高",
    "華通 (2313)": "AI 載板 + 低軌衛星雙題材，法說會確認全年營收成長 25-30%，今日小拉等支撐",
    "光聖 (6442)": "CPO 最純台廠，5 月營收 +116%，外資買超最兇，波動大只適合短打",
    "聯電 (2303)": "布局美國產能 + imec 技術授權 + 矽光子，ADR 三交易日狂漲 25%，台股爆量接力",
    "力成 (6239)": "儲存與周邊封裝測試，動能中等，今日 +5.36% 創高",
    "南亞科 (2408)": "DRAM 超循環，營收年增 582%，外資升買進目標 490 元，今日 459.5 創高",
    "華邦電 (2344)": "AI 高效能記憶體需求爆發，5 月營收首度破 200 億年增 181%，毛利率破 50%",
    "台積電 (2330)": "最大法人買超，CoWoS/2 奈米確定性最高，所有冠軍 ETF 最大持股",
    "聯發科 (2454)": "AI ASIC 營收翻倍至 20 億美元，Momentum 最強，NPU 出貨量最高，今日高檔震盪",
    "凌華 (6166)": "Edge AI + 自動化，Q1 營收年增 29-30%，4 月 +63% 創新高，Edge AI 明年貢獻營收",
    "研華 (2395)": "Edge AI + 機器人存股型，營收 moderate 成長，短線動能不足",
    "啟碁 (6285)": "網通 + NB + 低軌衛星，無明確 AI 爆發點，271-281 區間震盪",
    "創意 (3443)": "IC 設計，今日 -4.24% 拉回 4860，高檔調整等止穩",
    "聯友金屬 (7610)": "鎢/APT/碳化鎢半導體耗材，地緣政治題材，最快進最快出",
    "大立光 (3008)": "鏡頭龍頭，營收確認佳但基期高，非最強動能主航道",
    "漢唐 (2404)": "無塵室工程，今日 -1.17%，無明顯催化劑",
    "汎銓 (6830)": "AI 芯片測試探針，今日漲停 564 但成交 783 張流動性差，等量能確認",
}
HOLD = {"T1":"營收確認型，持有 7-30 天（營收低於預期 10% 才賣）",
        "T2":"動能爆發型，持有 1-7 天（法人買超縮減或長上影線即出）",
        "T3":"題材短打型，持有 1-3 天（消息面鈍化即刻出）",
        "T4":"觀察不追"}

def stock_children(name, tier, price, chg):
    return [
        {"type": "callout", "callout": {"icon": {"type": "emoji", "emoji": "📋"}, "rich_text": [{"type": "text", "text": {"content": f"分級：{tier} | 持有條件：{HOLD.get(tier,'')}"}}]}},
        {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "選股邏輯"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": LOGICS.get(name, "待補")}}]}},
        {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "每日快照"}}]}},
        {"type": "callout", "callout": {"icon": {"type": "emoji", "emoji": "💰"}, "rich_text": [{"type": "text", "text": {"content": f"2026-06-18 收盤：{price}（{chg}）"}}]}},
        {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "每日追蹤記錄"}}]}},
        {"type": "table", "table": {"table_width": 4, "has_column_header": True, "children": [
            {"object": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "日期"}}], [{"type": "text", "text": {"content": "收盤價"}}], [{"type": "text", "text": {"content": "漲跌幅"}}], [{"type": "text", "text": {"content": "備註"}}], ]}},
            {"object": "table_row", "table_row": {"cells": [
                [{"type": "text", "text": {"content": "2026-06-18"}}], [{"type": "text", "text": {"content": price}}], [{"type": "text", "text": {"content": chg}}], [{"type": "text", "text": {"content": "初始建立"}}], ]}},
        ]}},
        {"type": "divider", "divider": {}},
        {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "資料來源：TWSE即時API + 00981A/00992A/00991A ETF公開持倉"}}]}},
    ]

for theme, stocks in THEMES.items():
    print(f"\nTheme: {theme}")
    t = create(root["id"], theme, children=[{"type": "callout", "callout": {"icon": {"type": "emoji", "emoji": "📊"}, "rich_text": [{"type": "text", "text": {"content": f"共追蹤 {len(stocks)} 檔個股"}}]}}])
    if not t:
        continue
    time.sleep(0.4)
    for name, tier, price, chg in stocks:
        display = name.split(" (")[0] + " (" + name.split("(")[1].rstrip(")") + ")"
        create(t["id"], display, children=stock_children(name, tier, price, chg))
        time.sleep(0.35)

print("\n=== Done ===")
