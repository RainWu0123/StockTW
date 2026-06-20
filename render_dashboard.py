#!/usr/bin/env python3
"""讀取 TWSE snapshot JSON，重建 dashboard.html + research.html"""
import os, json, glob
from datetime import datetime

BASE = "/home/ubuntu/investment"

def latest_snapshot():
    paths = glob.glob(os.path.join(BASE, "data", "snapshot_*.json"))
    if not paths:
        return None
    return max(paths, key=os.path.getmtime)

def load_snapshot():
    p = latest_snapshot()
    if not p:
        return None, []
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d.get("date", ""), d.get("stocks", [])

def tier_of(code):
    TIER = {
        "2327":"T1","2308":"T1","2330":"T1","2383":"T1","2454":"T1",
        "2344":"T2","2408":"T2","3017":"T2","3711":"T2","6166":"T2","2303":"T2",
        "6442":"T3","2375":"T3","7610":"T3",
        "2313":"T4","2395":"T4","6285":"T4","3443":"T4","3008":"T4","2404":"T4","6830":"T4","6239":"T4",
    }
    return TIER.get(code, "T4")

def tier_class(t):
    return {"T1":"tier-t1","T2":"tier-t2","T3":"tier-t3","T4":"tier-t4"}.get(t,"tier-t4")

def color_pct(p):
    if p > 0: return f"<span class='up'>+{p}%</span>"
    if p < 0: return f"<span class='down'>{p}%</span>"
    return "<span class='float'>0.0%</span>"

def build_dashboard(date, stocks):
    rows = []
    for s in sorted(stocks, key=lambda x: x.get("code","")):
        t = tier_of(s["code"])
        rows.append(f"<tr><td>{s['code']}</td><td>{s['name']}</td><td>{s['price']}</td><td>{color_pct(s['pct'])}</td><td>{s['vol']:,}</td><td>{'─'}</td><td><span class='tier-tag {tier_class(t)}'>{t}</span></td></tr>")

    stocks_map = {s["code"]: s for s in stocks}
    def card(code, name, pct_ref):
        s = stocks_map.get(code)
        price = s["price"] if s else pct_ref
        pct = s["pct"] if s else 0
        chg = color_pct(pct) if s else ""
        return f"<div class='stock'><div class='name'>{name} <span class='float'>{code}</span></div><div class='price'>{price} {chg}</div></div>"

    t1_cards = "".join([
        card("2327","國巨","1080"), card("2308","台達電","2150"), card("2330","台積電","2410"),
        card("2383","台光電","5600"), card("2454","聯發科","4390"),
    ])
    t2_cards = "".join([
        card("2344","華邦電","218.5"), card("2408","南亞科","459.5"), card("3017","奇鋐","2400"),
        card("3711","日月光","613"), card("6166","凌華","155.5"), card("2303","聯電","145.5"),
    ])
    t3_cards = "".join([
        card("6442","光聖","1945"), card("2375","凱美","219"), card("7610","聯友金屬","2315"),
    ])
    t4_cards = "".join([
        card("2313","華通","259.5"), card("2395","研華","494"), card("6285","啟碁","274"),
        card("3443","創意","4860"), card("3008","大立光","5195"), card("2404","漢唐","1265"),
        card("6830","汎銓","564"), card("6239","力成","363.5"),
    ])

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>台股 AI 投資追蹤 — {date}</title>
<style>
:root{{--bg:#0c0f14;--panel:#141820;--panel2:#1a1f2b;--text:#d8dee8;--muted:#7a8599;--accent:#4aa3ff;--green:#3ecf8e;--red:#f0465a;--orange:#f09030;--warn:#c98dff;--border:#252a36}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans TC",sans-serif;line-height:1.55}}
a{{color:var(--accent)}}
header{{padding:18px 24px;border-bottom:1px solid var(--border);background:#11141c}}
header h1{{font-size:18px;margin:0;font-weight:600}}
header .sub{{color:var(--muted);font-size:12px;margin-top:6px}}
.container{{max-width:1300px;margin:0 auto;padding:18px 16px 40px}}
.grid{{display:grid;gap:14px}}.grid-4{{grid-template-columns:repeat(4,1fr)}}
@media(max-width:1100px){{.grid-4{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:720px){{.grid-4{{grid-template-columns:1fr}}}}
.card{{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px 16px}}
.card h2{{font-size:13px;color:var(--muted);margin:0 0 10px;text-transform:uppercase;letter-spacing:.6px}}
.big{{font-size:28px;font-weight:700;color:var(--text)}}
.tier-tag{{display:inline-block;font-size:11px;padding:3px 7px;border-radius:999px;font-weight:600;letter-spacing:.3px}}
.tier-t1{{background:#16302a;color:var(--green)}}.tier-t2{{background:#1a2430;color:var(--accent)}}.tier-t3{{background:#2f2316;color:var(--orange)}}.tier-t4{{background:#221a1a;color:var(--muted)}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:6px}}
th{{color:var(--muted);font-weight:500;text-align:left;padding:7px 8px;border-bottom:1px solid var(--border);white-space:nowrap}}
td{{padding:8px;border-bottom:1px solid #1b2130}}
tr:hover td{{background:#161b25}}
.up{{color:var(--green)}}.down{{color:var(--red)}}.float{{color:var(--muted)}}
.stock-list{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}
@media(max-width:720px){{.stock-list{{grid-template-columns:1fr}}}}
.stock{{background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:10px 12px}}
.stock .name{{font-weight:600;font-size:14px}}.stock .meta{{font-size:12px;color:var(--muted);margin-top:4px}}
.stock .price{{font-size:18px;font-weight:700;margin-top:6px}}.stock .note{{font-size:12px;color:#9aa6b8;margin-top:6px}}
.section{{margin-top:20px}}.section h2{{font-size:15px;font-weight:600;margin:0 0 10px}}
.footer{{color:var(--muted);font-size:12px;margin-top:18px}}
.alert{{padding:10px 12px;border-radius:8px;background:#1e1a22;border:1px solid #342840;color:#e3cbff;font-size:12px;margin-top:12px}}
</style>
</head>
<body>
<header>
  <h1>🎯 台股 AI 投資追蹤 <span class='tier-tag tier-t1' style='margin-left:10px'>{date}</span></h1>
  <div class='sub'>TWSE 即時快照 · 三軌配置 · 自動更新</div>
</header>
<div class='container'>
  <div class='grid grid-4'>
    <div class='card'><h2>標的總數</h2><div class='big'>{len(stocks)} <span class='tier-tag tier-t1'>22</span></div></div>
    <div class='card'><h2>T1 營收確認型</h2><div class='big'>5 <span class='tier-tag tier-t1'>25%</span></div></div>
    <div class='card'><h2>T2 動能爆發型</h2><div class='big'>7 <span class='tier-tag tier-t2'>30%</span></div></div>
    <div class='card'><h2>T3 / T4 觀察</h2><div class='big'>10 <span class='tier-tag tier-t4'>45%</span></div></div>
  </div>
  <div class='alert'>本頁由 Hermes 自動更新。資料日期：{date}。<a href='research.html'>🡒 個股研究報告</a></div>

  <div class='section'>
    <h2>📊 TWSE 收盤快照</h2>
    <div class='card' style='overflow:auto'>
    <table><thead><tr><th>代號</th><th>公司</th><th>收盤價</th><th>漲跌幅</th><th>成交張數</th><th>分級</th></tr></thead>
    <tbody>{''.join(rows)}</tbody></table></div></div>

  <div class='section'><h2>🏆 分級排名</h2>
  <div class='grid grid-4'>
    <div class='card'><h2><span class='tier-tag tier-t1'>T1</span> 營收確認型 (7-30天)</h2><div class='stock-list'>{t1_cards}</div></div>
    <div class='card'><h2><span class='tier-tag tier-t2'>T2</span> 動能爆發型 (1-7天)</h2><div class='stock-list'>{t2_cards}</div></div>
    <div class='card'><h2><span class='tier-tag tier-t3'>T3</span> 題材短打型 (1-3天)</h2><div class='stock-list'>{t3_cards}</div></div>
    <div class='card'><h2><span class='tier-tag tier-t4'>T4</span> 觀察 / 不追</h2><div class='stock-list'>{t4_cards}</div></div>
  </div></div>

  <div class='footer'>資料來源：TWSE API · 更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M')} · Hermes 投資追蹤系統</div>
</div>
</body>
</html>"""
    with open(os.path.join(BASE, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.join(BASE, "dashboard.html")

def main():
    date, stocks = load_snapshot()
    if not stocks:
        print("[warn] no snapshot found, run fetch_twse.py first", flush=True)
        sys.exit(1)
    p = build_dashboard(date, stocks)
    print(f"[rendered] -> {p}", flush=True)

if __name__ == "__main__":
    main()
