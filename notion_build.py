import requests, time
from pathlib import Path

token_path = Path('/home/ubuntu/.notion_token')
NT = token_path.read_text().strip()
H = {
    "Authorization": f"Bearer {NT}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
B = "https://api.notion.com/v1"

def api(m, e, b=None):
    url = f"{B}/{e.lstrip('/')}"
    r = requests.request(m, url, headers=H, json=b, timeout=30)
    if r.status_code >= 400:
        print(f"ERR {r.status_code}: {r.text[:180]}", flush=True)
        return None
    return r.json()

def mk(pid, title, ch=None):
    body = {"parent": {"page_id": pid}, "properties": {"title": {"title": [{"text": {"content": title}}]}}}
    if ch:
        body["children"] = ch
    r = api("POST", "pages", body)
    print(f"  {'OK' if r else 'FAIL'}: {title}", flush=True)
    return r

print("Searching workspace root...", flush=True)
s = api("POST", "search", {"filter": {"property": "object", "value": "page"}, "page_size": 20})
res = s.get("results", []) if s else []
pid = next((p["id"] for p in res if p.get("parent", {}).get("type") == "workspace"), res[0]["id"])

print("Creating root page...", flush=True)
root = mk(pid, "台股 AI 投資追蹤")
if not root:
    raise SystemExit(1)
time.sleep(0.3)

LOGI = {
    "國巨": "被動元件龍頭，AI伺服器 MLCC/電阻需求爆發，5月營收+47%，00981A/00992A/00991A同步加碼",
    "台達電": "AI伺服器電源+液冷散熱雙主軸，2026首季營收創高+34%，伺服器電源占營收逾20%",
    "奇鋐": "液冷散熱台廠第一，Google/微軟/NVIDIA訂單能見度到2029，外資升評至3333",
    "凱美": "AI電感/MLCC彈性最大，Q1 EPS+572%，00981A近期掃貨，體量小但動能強",
    "台光電": "NVIDIA M9供應商，ABF/PCB雙引擎，2026營收年增35%+，外資看2027成長39%",
    "日月光": "CoWoS產能溢訂單最大受惠，先進封裝占營收比重持續提升",
    "華通": "AI載板+低軌衛星雙題材，法說會確認全年營收成長25-30%",
    "光聖": "CPO最純台廠，5月營收+116%，外資買超最兇",
    "聯電": "布局美國產能+imec技術授權+矽光子，ADR三交易日狂漲25%",
    "力成": "儲存與周邊封裝測試，動能中等",
    "南亞科": "DRAM超循環，營收年增582%，外資升買進目標490元",
    "華邦電": "AI高效能記憶體需求爆發，5月營收首度破200億年增181%，毛利率破50%",
    "台積電": "最大法人買超，CoWoS/2奈米確定性最高，所有冠軍ETF最大持股",
    "聯發科": "AI ASIC營收翻倍至20億美元，Momentum最強，NPU出貨量最高",
    "凌華": "Edge AI+自動化，Q1營收年增29-30%，4月+63%創新高",
    "研華": "Edge AI+機器人存股型，營收moderate成長，短線動能不足",
    "啟碁": "網通+NB+低軌衛星，無明確AI爆發點",
    "創意": "IC設計，今日-4.24%拉回，高檔調整等止穩",
    "聯友金屬": "鎢/APT/碳化鎢半導體耗材，地緣政治題材，最快進最快出",
    "大立光": "鏡頭龍頭，營收確認佳但基期高，非最強動能主航道",
    "漢唐": "無塵室工程，今日-1.17%，無明顯催化劑",
    "汎銓": "AI芯片測試探針，今日漲停但成交783張流動性差",
}

THEMES = {
    "AI基礎建設": [("國巨","T1","1080","+9.76%"),("台達電","T1","2150","-0.23%"),("奇鋐","T2","2400","+1.48%"),("凱美","T3","219","+9.77%")],
    "AI先進封裝": [("台光電","T1","5600","+7.69%"),("日月光","T2","613","+3.03%"),("華通","T4","259.5","-1.70%"),("光聖","T3","1945","+6.00%"),("聯電","T2","145.5","+3.93%"),("力成","T4","363.5","+5.36%")],
    "AI記憶體": [("南亞科","T2","459.5","+5.15%"),("華邦電","T2","218.5","+9.80%")],
    "AI運算平台": [("台積電","T1","2410","+1.05%"),("聯發科","T1","4390","-1.57%"),("凌華","T2","155.5","+9.12%"),("研華","T4","494","+1.12%"),("啟碁","T4","274","+1.29%"),("創意","T4","4860","-4.24%")],
    "地緣短打": [("聯友金屬","T3","2315","+9.98%")],
    "其他觀察": [("大立光","T4","5195","+0.97%"),("漢唐","T4","1265","-1.17%"),("汎銓","T4","564","+9.94%")],
}

for theme, stocks in THEMES.items():
    print(f"\nTheme: {theme}", flush=True)
    p = mk(root["id"], theme)
    if not p:
        continue
    time.sleep(0.25)
    for name, tier, price, chg in stocks:
        children = [
            {"type": "callout", "callout": {"icon": {"type": "emoji", "emoji": "📋"}, "rich_text": [{"type": "text", "text": {"content": f"分級：{tier}"}}]}},
            {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "選股邏輯"}}]}},
            {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": LOGI.get(name, "待補")}}]}},
            {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "每日快照"}}]}},
            {"type": "callout", "callout": {"icon": {"type": "emoji", "emoji": "💰"}, "rich_text": [{"type": "text", "text": {"content": f"2026-06-18 收盤：{price}（{chg}）"}}]}},
            {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "每日追蹤記錄"}}]}},
            {"type": "table", "table": {"table_width": 4, "has_column_header": True, "children": [
                {"object": "block", "type": "table_row", "table_row": {"cells": [
                    [{"type": "text", "text": {"content": "日期"}}],
                    [{"type": "text", "text": {"content": "收盤價"}}],
                    [{"type": "text", "text": {"content": "漲跌幅"}}],
                    [{"type": "text", "text": {"content": "備註"}}],
                ]}},
                {"object": "block", "type": "table_row", "table_row": {"cells": [
                    [{"type": "text", "text": {"content": "2026-06-18"}}],
                    [{"type": "text", "text": {"content": price}}],
                    [{"type": "text", "text": {"content": chg}}],
                    [{"type": "text", "text": {"content": "初始建立"}}],
                ]}},
            ]}},
            {"type": "divider", "divider": {}},
        ]
        mk(p["id"], name, ch=children[:95])
        time.sleep(0.2)

print("\nDONE", flush=True)
