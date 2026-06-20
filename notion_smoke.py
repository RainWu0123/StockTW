#!/usr/bin/env python3
import requests
import sys
import time

NOTION_TOKEN="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"
HEADERS = {
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

print("Searching workspace root page...")
search = api("POST", "search", {"filter": {"property": "object", "value": "page"}, "page_size": 20})
results = search.get("results", []) if search else []
parent_id = None
for p in results:
    if p.get("parent", {}).get("type") == "workspace":
        parent_id = p["id"]
        print(f"Found workspace root page: {parent_id}")
        break
if not parent_id:
    parent_id = results[0]["id"]

print("\nCreate root page: 台股 AI 投資追蹤")
root = api("POST", "pages", {
    "parent": {"page_id": parent_id},
    "properties": {"title": {"title": [{"text": {"content": "台股 AI 投資追蹤"}}]}},
    "children": [
        {"type": "callout", "callout": {"icon": {"type": "emoji", "emoji": "🤖"}, "rich_text": [{"type": "text", "text": {"content": "本資料夾由 Hermes Agent 自動維護，每日 TWSE 收盤後自動更新。"}}]}},
        {"type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "每日選股邏輯摘要"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "營收確認型（T1）：持有 7-30 天"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "動能爆發型（T2）：持有 1-7 天"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "題材短打型（T3）：持有 1-3 天"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "觀察不追（T4）：等明確訊號"}}]}},
    ]
})
print("Root created" if root else "Root create failed")
if not root:
    sys.exit(1)
time.sleep(0.4)

print("\nCreate first theme page: AI 基礎建設（被動元件/電源/散熱）")
theme = api("POST", "pages", {
    "parent": {"page_id": root["id"]},
    "properties": {"title": {"title": [{"text": {"content": "AI 基礎建設（被動元件/電源/散熱）"}}]}},
    "children": [
        {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "主題頁建立測試"}}]}},
    ]
})
print("Theme created" if theme else "Theme create failed")
if not theme:
    sys.exit(1)
time.sleep(0.4)

print("\nCreate stock page: 國巨 (2327)")
stock = api("POST", "pages", {
    "parent": {"page_id": theme["id"]},
    "properties": {"title": {"title": [{"text": {"content": "國巨 (2327)"}}]}},
    "children": [
        {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "個股頁建立測試"}}]}},
    ]
})
print("Stock page created" if stock else "Stock page create failed")
if not stock:
    sys.exit(1)

print("\n=== Minimal passage OK ===")
