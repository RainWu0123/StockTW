#!/usr/bin/env python3
"""
建立 Notion 投資追蹤筆記結構
Token: ntn_...（不印出）
"""
import requests
import json
import sys

NOTION_TOKEN = "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"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

BASE_URL = "https://api.notion.com/v1"

def api(method, endpoint, body=None):
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.request(method, url, headers=HEADERS, json=body, timeout=30)
    data = resp.json()
    if resp.status_code >= 400:
        print(f"ERROR {resp.status_code}: {data}", file=sys.stderr)
        sys.exit(1)
    return data

def create_page(parent_id, title, properties=None, children=None):
    body = {
        "parent": {"page_id": parent_id},
        "properties": properties or {
            "title": {"title": [{"text": {"content": title}}]}
        }
    }
    if children:
        body["children"] = children
    return api("POST", "pages", body)

def get_root_page():
    # 嘗試取得使用者的第一個 top-level page
    resp = api("GET", "search", {"filter": {"property": "object", "value": "page"}, "page_size": 1})
    results = resp.get("results", [])
    if results:
        return results[0]["id"]
    return None

# --- 結構定義 ---
THEMES = {
    "AI 基礎建設（被動元件/電源/散熱）": [
        ("國巨 (2327)", "T1", "被動元件龍頭，營收+47%，00981A/00991A核心持股，今日漲停創高1080元"),
        ("台達電 (2308)", "T1", "AI電源+液冷散熱雙主軸，首季營收創高+34%，HVDC提前量產"),
        ("奇鋐 (3017)", "T2", "液冷散熱台廠第一，訂單能見度到2029，外資升目標價3333"),
        ("凱美 (2375)", "T3", "AI電感/MLCC彈性最大，Q1 EPS+572%，今日漲停219元"),
    ],
    "AI 先進封裝（CoWoS/ABF/CPO）": [
        ("台光電 (2383)", "T1", "NVIDIA M9供應商，營收年增35%，ABF/PCB龍頭，今日5600強拉創高"),
        ("日月光投控 (3711)", "T2", "CoWoS產能溢訂單最大受惠，今日+3%創新高613元"),
        ("華通 (2313)", "T4", "AI載板+低軌衛星雙題材，今日-1.7%小拉，等255以下接"),
        ("光聖 (6442)", "T3", "CPO最純台廠，5月營收+116%，今日+6%創高1945元"),
        ("聯電 (2303)", "T2", "ADR三交易日狂漲25%，台股爆量29萬張接力，矽光子題材"),
        ("力成 (6239)", "T4", "儲存與周邊封裝測試，動能中等"),
    ],
    "AI 記憶體（DRAM/HBM）": [
        ("南亞科 (2408)", "T2", "營收年增582%，法人升買進目標490，今日459.5創高"),
        ("華邦電 (2344)", "T2", "營收+181%，毛利率破50%，今日漲停218.5元，法人狂買"),
    ],
    "AI 運算平台（IC設計/Edge AI）": [
        ("台積電 (2330)", "T1", "最大法人買超，CoWoS/2奈米確定性最高，今日2410小創高"),
        ("聯發科 (2454)", "T1", "AI ASIC營收翻倍至20億美元，今日4390高檔震盪"),
        ("凌華 (6166)", "T2", "營收+63%，今日漲停155.5元，Edge AI題材"),
        ("研華 (2395)", "T4", "Edge AI存股型，短線動能不足"),
        ("啟碁 (6285)", "T4", "網通+NB+低軌衛星，無明確AI爆發點"),
        ("創意 (3443)", "T4", "今日-4.24%拉回4860，高檔調整等止穩"),
    ],
    "地緣題材短打": [
        ("聯友金屬 (7610)", "T3", "鎢/APT/碳化鎢耗材，地緣政治題材，今日漲停2315元，最快進最快出"),
    ],
    "其他觀察": [
        ("大立光 (3008)", "T4", "鏡頭龍頭，營收確認佳但基期高，5195盤高"),
        ("漢唐 (2404)", "T4", "無塵室工程，今日-1.17%盤整，無明顯催化劑"),
        ("汎銓 (6830)", "T4", "AI測試探針題材，今日漲停564但成交僅783張流動性差"),
    ],
}

# --- 內容模板 ---
STOCK_TEMPLATE = """# {name} 追蹤報告

## 分級定位
**Tier**: {tier}
**追蹤日期**: 2026-06-19
**收盤價**: 待每日更新
**信心等級**: 高（TWSE即時數據驗證）

## 選股邏輯
{logic}

## 主要持有條件
- 持有時間: {hold_period}
- 加碼時機: 法人連續買超3天且營收低於預期幅度
- 減碼時機: 單日成交爆量+上影線 或 月營收低於預期15%

## 風險因子
- 營收波動幅度
- 法人籌碼變化
- 大盤系統性風險

## 每日追蹤記錄
> 格式: 日期 | 收盤價 | 漲跌幅 | 成交張數 | 備註

---
*本頁由 Hermes Agent 自動建立，資料來源: TWSE即時API + 00981A/00992A/00991A ETF持倉*
"""

HOLD_PERIODS = {
    "T1": "7-30天（營收確認型，只有營收低於預期10%才賣）",
    "T2": "1-7天（動能爆發型，法人買超縮減或長上影線即出）",
    "T3": "1-3天（題材短打型，消息面鈍化即刻出）",
    "T4": "觀察不追（等明確訊號）",
}

LOGICS = {
    "國巨 (2327)": "被動元件龍頭，AI伺服器MLCC/電阻需求爆發，5月營收+47%，00981A/00992A/00991A三大冠軍ETF同步加碼",
    "台達電 (2308)": "AI伺服器電源+液冷散熱雙主軸，2026首季營收創高+34%，伺服器電源占營收逾20%",
    "奇鋐 (3017)": "液冷散熱台廠第一，Google/微軟/NVIDIA訂單能見度到2029，外資升評至3333",
    "凱美 (2375)": "AI電感/MLCC彈性最大，Q1 EPS+572%，00981A近期掃貨，體量小但動能強",
    "台光電 (2383)": "NVIDIA M9供應商，ABF/PCB雙引擎，2026營收年增35%+，外資看2027成長39%",
    "日月光投控 (3711)": "CoWoS產能溢訂單最大受惠，先進封裝占營收比重持續提升",
    "華通 (2313)": "AI載板+低軌衛星雙題材，法說會確認全年營收成長25-30%，今日小拉等支撐",
    "光聖 (6442)": "CPO最純台廠，5月營收+116%，外資買超最兇，波動大只適合短打",
    "聯電 (2303)": "布局美國產能+imec技術授權+矽光子，ADR三交易日狂漲25%，台股接棒",
    "力成 (6239)": "儲存與周邊封裝測試，動能中等",
    "南亞科 (2408)": "DRAM超循環，營收年增582%，外資升買進目標490元，今日459.5創高",
    "華邦電 (2344)": "AI高效能記憶體需求爆發，5月營收首度破200億年增181%，毛利率破50%",
    "台積電 (2330)": "最大法人買超，CoWoS/2奈米確定性最高，所有冠軍ETF最大持股",
    "聯發科 (2454)": "AI ASIC營收翻倍至20億美元，Momentum最強，NPU出貨量最高",
    "凌華 (6166)": "Edge AI+自動化，Q1營收年增29-30%，4月+63%創新高，明年Edge AI貢獻",
    "研華 (2395)": "Edge AI+機器人存股型，營收 moderate 成長，短線動能不足",
    "啟碁 (6285)": "網通+NB+低軌衛星，無明確AI爆發點，271-281區間震盪",
    "創意 (3443)": "IC設計，今日-4.24%拉回，高檔調整等止穩",
    "聯友金屬 (7610)": "鎢/APT/碳化鎢半導體耗材，地緣政治題材，最快進最快出",
    "大立光 (3008)": "鏡頭龍頭，營收確認佳但基期高，非最強動能主航道",
    "漢唐 (2404)": "無塵室工程，今日-1.17%，無明顯催化劑",
    "汎銓 (6830)": "AI芯片測試探針，今日漲停564但成交783張流動性差，等量能確認",
}

# Auth header check
print("Testing Notion API...")
try:
    resp = requests.get(f"{BASE_URL}/users/me", headers=HEADERS, timeout=10)
    if resp.status_code == 200:
        user = resp.json()
        print(f"OK: {user.get('name', '?')} ({user.get('id', '?')})")
    else:
        print(f"Auth failed: {resp.status_code} {resp.text}", file=sys.stderr)
        sys.exit(1)
except Exception as e:
    print(f"Connection error: {e}", file=sys.stderr)
    sys.exit(1)
