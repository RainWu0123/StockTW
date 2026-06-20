import requests, time
NT = "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"
H = {"Authorization": f"Bearer {NT}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
B = "https://api.notion.com/v1"
def api(m, e, b=None):
 r = requests.request(m, f"{B}/{e.lstrip('/')}", headers=H, json=b, timeout=30)
 if r.status_code >= 400: print(f"ERR {r.status_code}: {r.text[:200]}", flush=True); return None
 return r.json()
# root page id from smoke test
root = "2f68a30f-8abf-80f0-8cb2-d7cd197cdd3f"
# create main folder under root
main = api("POST", "pages", {"parent": {"page_id": root}, "properties": {"title": {"title": [{"text": {"content": "台股 AI 投資追蹤"}}]}}})
if not main: raise SystemExit("main failed")
print("MAIN", main["id"])
time.sleep(0.3)
for i, (t, stocks) in enumerate([
    ("AI基礎建設", [("國巨", "T1", "1080", "+9.76%"), ("台達電", "T1", "2150", "-0.23%")]),
    ("AI先進封裝", [("台光電", "T1", "5600", "+7.69%"), ("日月光", "T2", "613", "+3.03%")]),
    ("AI記憶體", [("南亞科", "T2", "459.5", "+5.15%"), ("華邦電", "T2", "218.5", "+9.80%")]),
    ("AI運算平台", [("台積電", "T1", "2410", "+1.05%"), ("聯發科", "T1", "4390", "-1.57%")]),
    ("地緣短打", [("聯友金屬", "T3", "2315", "+9.98%")]),
    ("其他觀察", [("大立光", "T4", "5195", "+0.97%")]),
]):
  p = api("POST", "pages", {"parent": {"page_id": main["id"]}, "properties": {"title": {"title": [{"text": {"content": t}}]}}})
  if not p: continue
  print("THEME", t, p["id"])
  time.sleep(0.25)
  for (n, tier, price, chg) in stocks:
    s = api("POST", "pages", {"parent": {"page_id": p["id"]}, "properties": {"title": {"title": [{"text": {"content": n}}]}})
    print("  STOCK", n, s["id"] if s else "FAIL")
    time.sleep(0.2)
print("=== batch1 done ===")
