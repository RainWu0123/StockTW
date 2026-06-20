#!/usr/bin/env python3
"""Render data.json + static dashboard.html from TWSE snapshot."""
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

def tier_meta(t):
    return {
        "T1": {"label": "T1 營收確認型", "cls": "tier-t1", "color": "#3ecf8e", "hold": "7-30天"},
        "T2": {"label": "T2 動能爆發型", "cls": "tier-t2", "color": "#4aa3ff", "hold": "1-7天"},
        "T3": {"label": "T3 題材短打型", "cls": "tier-t3", "color": "#f09030", "hold": "1-3天"},
        "T4": {"label": "T4 觀察/不追", "cls": "tier-t4", "color": "#7a8599", "hold": "--"},
    }.get(t, {})

NOTE = {
    "2327":"00981A/00992A/00991A 核心持股，今日漲停創高",
    "2308":"AI 電源+液冷雙主軸，盤整後還有空間",
    "2330":"CoWoS/2奈米確定性最高",
    "2383":"NVIDIA M9供應商，今日強拉+7.69%",
    "2454":"AI ASIC，今日-1.57%小拉，Momentum仍強",
    "2344":"DRAM超循環，營收+181%，法人狂買",
    "2408":"營收年增582%，外資目標490，今日創高",
    "3017":"液冷散熱台廠第一，訂單能見度到2029",
    "3711":"CoWoS溢最強，先進封裝占營收比持續提升",
    "6166":"Edge AI題材，今日漲停",
    "2303":"ADR 25%，爆量29萬張，矽光子題材",
    "6442":"CPO最純台廠，外資買超最兇",
    "2375":"AI電感/MLCC彈性最大，00981A掃貨",
    "7610":"地緣題材，最快進最快出",
    "2313":"AI載板+低軌衛星，等255以下",
    "2395":"Edge AI存股型，短線動能不足",
    "6285":"網通+NB+低軌，無明確AI爆發點",
    "3443":"高檔拉回，等止穩再說",
    "3008":"營收確認佳但基期高",
    "2404":"無明顯催化劑",
    "6830":"今日漲停但成交783張，流動性差",
    "6239":"動能中等，漲幅可能已被反映",
}

STYLE = """<style>
:root{--bg:#0c0f14;--panel:#141820;--panel2:#1a1f2b;--text:#d8dee8;--muted:#7a8599;--accent:#4aa3ff;--green:#3ecf8e;--red:#f0465a;--orange:#f09030;--warn:#c98dff;--border:#252a36}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans TC",sans-serif;line-height:1.55}
a{color:var(--accent)}
header{padding:18px 24px;border-bottom:1px solid var(--border);background:#11141c;position:sticky;top:0;z-index:10;backdrop-filter:blur(8px)}
header h1{font-size:18px;margin:0;font-weight:600}header .sub{color:var(--muted);font-size:12px;margin-top:6px}
.container{max-width:1300px;margin:0 auto;padding:18px 16px 40px}
.grid{display:grid;gap:14px}.grid-4{grid-template-columns:repeat(4,1fr)}@media(max-width:1100px){.grid-4{grid-template-columns:repeat(2,1fr)}}@media(max-width:720px){.grid-4{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px 16px}
.card h2{font-size:13px;color:var(--muted);margin:0 0 10px;text-transform:uppercase;letter-spacing:.6px}
.big{font-size:28px;font-weight:700;color:var(--text)}
.tier-tag{display:inline-block;font-size:11px;padding:3px 7px;border-radius:999px;font-weight:600;letter-spacing:.3px}
.tier-t1{background:#16302a;color:var(--green)}.tier-t2{background:#1a2430;color:var(--accent)}.tier-t3{background:#2f2316;color:var(--orange)}.tier-t4{background:#221a1a;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:6px}
th{color:var(--muted);font-weight:500;text-align:left;padding:7px 8px;border-bottom:1px solid var(--border);white-space:nowrap;cursor:pointer;user-select:none}
th:hover{color:var(--text)}td{padding:8px;border-bottom:1px solid #1b2130}tr:hover td{background:#161b25}
.up{color:var(--green)}.down{color:var(--red)}.float{color:var(--muted)}
.stock-list{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}@media(max-width:720px){.stock-list{grid-template-columns:1fr}}
.stock{background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:10px 12px}
.stock .name{font-weight:600;font-size:14px}.stock .meta{font-size:12px;color:var(--muted);margin-top:4px}.stock .price{font-size:18px;font-weight:700;margin-top:6px}.stock .note{font-size:12px;color:#9aa6b8;margin-top:6px}
.section{margin-top:20px}.section h2{font-size:15px;font-weight:600;margin:0 0 10px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.alert{padding:10px 12px;border-radius:8px;background:#1e1a22;border:1px solid #342840;color:#e3cbff;font-size:12px;margin-top:12px}
.bar-wrap{background:#1c2430;border-radius:999px;height:8px;overflow:hidden;margin-top:6px}.bar{height:100%;border-radius:999px}
.ctrl{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
.ctrl input{background:#11141c;color:var(--text);border:1px solid var(--border);border-radius:6px;padding:6px 10px;font-size:13px;min-width:160px}
.ctrl button{background:#1a1f2b;color:var(--text);border:1px solid var(--border);border-radius:6px;padding:6px 12px;cursor:pointer;font-size:13px}
.ctrl button:hover{border-color:var(--accent)}
.footer{color:var(--muted);font-size:12px;margin-top:18px}.footer a{color:#d8dee8;text-decoration:underline}
.kv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}@media(max-width:900px){.kv{grid-template-columns:repeat(2,1fr)}}
.kv div{background:#1a1f2b;border:1px solid var(--border);border-radius:8px;padding:10px 12px}.kv b{display:block;color:var(--muted);font-size:11px;font-weight:500}.kv span{font-size:14px;font-weight:600;display:block;margin-top:2px}
</style>"""

BODY_HEADER = """<header>
  <h1>🎯 台股 AI 投資追蹤 <span class="tier-tag tier-t1" style="margin-left:10px" id="headerDate">{date}</span></h1>
  <div class="sub">TWSE 即時快照 · 三軌配置 · 動態儀表板</div>
</header>
<div class="container">
  <div class="grid grid-4" id="summaryCards"><div class="card"><h2>載入中...</h2></div></div>
  <div class="alert">本頁由 Hermes 自動更新。支援點選欄位排序、關鍵字搜尋。<a href="research.html">🡒 個股研究報告</a></div>
  <div class="section">
    <h2>📊 TWSE 收盤快照</h2>
    <div class="card">
    <div class="ctrl">
      <input type="text" id="searchBox" placeholder="🔍 搜尋公司名稱或代號..." oninput="renderTable()">
      <button onclick="setSort('default')">預設</button>
      <button onclick="setSort('pct')">依漲跌幅</button>
      <button onclick="setSort('vol')">依成交量</button>
      <button onclick="setSort('price')">依股價</button>
      <span style="color:var(--muted);font-size:12px;align-self:center" id="countLabel"></span>
    </div>
    <div style="overflow:auto">
    <table id="snapshotTable">
    <thead><tr>
      <th onclick="setSort('code')">代號 ⇅</th>
      <th onclick="setSort('name')">公司 ⇅</th>
      <th onclick="setSort('price')">收盤價 ⇅</th>
      <th onclick="setSort('pct')">漲跌幅 ⇅</th>
      <th onclick="setSort('vol')">成交張數 ⇅</th>
      <th>持有邏輯</th>
      <th onclick="setSort('tier')">分級 ⇅</th>
    </tr></thead>
    <tbody id="snapshotBody"></tbody>
    </table></div></div></div>
  <div class="section"><h2>🏆 分級排名</h2><div class="grid grid-4" id="tierCards"></div></div>
  <div class="section"><h2>💼 最終投入配置（5 檔）</h2><div class="card">
  <table><thead><tr><th>優先</th><th>公司</th><th>部位</th><th>持有邏輯</th><th>可視化</th></tr></thead>
  <tbody id="allocBody"></tbody></table></div></div>
  <div class="section"><h2>📐 三軌配置摘要</h2><div class="grid grid-3" style="grid-template-columns:repeat(3,1fr)">
    <div class="card"><h2><span class="tier-tag tier-t1">A 軌</span>營收確認型 50%</h2><div id="aTrack"></div></div>
    <div class="card"><h2><span class="tier-tag tier-t2">B 軌</span>動能爆發型 30%</h2><div id="bTrack"></div></div>
    <div class="card"><h2><span class="tier-tag tier-t3">C 軌</span>地緣題材型 20%</h2><div id="cTrack"></div></div>
  </div></div>
  <div class="footer">資料來源：TWSE API · 更新時間：<span id="footerTime">--</span> · Hermes 投資追蹤系統<br><a href="research.html">🡒 個股深度研究報告</a></div>
</div>
<script>
let allStocks = [];
let currentSort = 'default';
let currentDir = 1;

function pctClass(p){{ if(p > 0) return 'up'; if(p < 0) return 'down'; return 'float'; }}
function fmt(n){{ if(n >= 10000) return (n/1000).toFixed(1) + 'K'; return n.toLocaleString(); }}
function tier_meta(t){{ return {{'T1':{{'cls':'tier-t1'}},'T2':{{'cls':'tier-t2'}},'T3':{{'cls':'tier-t3'}},'T4':{{'cls':'tier-t4'}}}}[t] || {{'cls':'tier-t4'}}; }}

function setSort(key){{
  if(currentSort === key) currentDir *= -1;
  else{{ currentSort = key; currentDir = 1; }}
  renderTable();
}}

function sortFn(a, b){{
  const k = currentSort;
  if(k === 'default'){{ return ({{'T1':1,'T2':2,'T3':3,'T4':4}}[a.tier]||4) - ({{'T1':1,'T2':2,'T3':3,'T4':4}}[b.tier]||4); }}
  let av = a[k], bv = b[k];
  if(k === 'pct' || k === 'price' || k === 'vol') return (av - bv) * currentDir;
  if(typeof av === 'string') av = av.toLowerCase();
  if(typeof bv === 'string') bv = bv.toLowerCase();
  if(av < bv) return -1 * currentDir;
  if(av > bv) return 1 * currentDir;
  return 0;
}}

function renderTable(){{
  const q = document.getElementById('searchBox').value.toLowerCase();
  let rows = allStocks.filter(s => s.name.toLowerCase().includes(q) || s.code.includes(q));
  rows.sort(sortFn);
  document.getElementById('snapshotBody').innerHTML = rows.map(s => '<tr><td>' + s.code + '</td><td><strong>' + s.name + '</strong><div style="font-size:11px;color:var(--muted);margin-top:2px">' + s.note + '</div></td><td style="font-weight:700">' + s.price + '</td><td class="' + pctClass(s.pct) + '">' + (s.pct > 0 ? '+' : '') + s.pct + '%</td><td>' + s.vol.toLocaleString() + '</td><td><span class="tier-tag ' + s.tier_cls + '">' + s.tier_label + '</span><div style="font-size:11px;color:var(--muted);margin-top:2px">持有 ' + s.hold + '</div></td><td><span class="tier-tag ' + s.tier_cls + '">' + s.tier + '</span></td></tr>').join('');
  document.getElementById('countLabel').textContent = rows.length + ' / ' + allStocks.length + ' 檔';
}}

function renderTierCards(){{
  const groups = {{}}; allStocks.forEach(s => {{ groups[s.tier] = groups[s.tier] || []; groups[s.tier].push(s); }});
  const titles = {{T1:'營收確認型 (7-30天)', T2:'動能爆發型 (1-7天)', T3:'題材短打型 (1-3天)', T4:'觀察 / 不追'}};
  document.getElementById('tierCards').innerHTML = Object.keys(groups).sort().map(t => '<div class="card"><h2><span class="tier-tag ' + tier_meta(t).cls + '" style="margin-right:6px">' + t + '</span>' + (titles[t]||t) + '</h2><div class="stock-list">' + groups[t].map(s => '<div class="stock"><div class="name">' + s.name + ' <span class="float">' + s.code + '</span></div><div class="meta">' + s.tier_label + '</div><div class="price ' + pctClass(s.pct) + '">' + s.price + ' <span style="font-size:13px">' + (s.pct > 0 ? '+' : '') + s.pct + '%</span></div><div class="note">' + s.note + '</div></div>').join('') + '</div></div>').join('');
}}

function renderSummary(){{
  const total = allStocks.length;
  const t1 = allStocks.filter(s=>s.tier==='T1').length;
  const t2 = allStocks.filter(s=>s.tier==='T2').length;
  const other = total - t1 - t2;
  document.getElementById('summaryCards').innerHTML = '<div class="card"><h2>標的總數</h2><div class="big">' + total + '</div></div><div class="card"><h2>T1 營收確認型</h2><div class="big">' + t1 + '</div></div><div class="card"><h2>T2 動能爆發型</h2><div class="big">' + t2 + '</div></div><div class="card"><h2>T3 / T4 觀察</h2><div class="big">' + other + '</div></div>';
}}

function renderAlloc(){{
  const allocs = [
    {{name:'國巨 2327',pct:25,logic:'被動元件龍頭，00981A核心'}},
    {{name:'奇鋐 3017',pct:20,logic:'液冷散熱台廠第一，訂單到2029'}},
    {{name:'華邦電 2344',pct:20,logic:'DRAM超循環，營收+181%'}},
    {{name:'南亞科 2408',pct:20,logic:'營收年增582%，外資目標490'}},
    {{name:'凱美 2375',pct:15,logic:'AI電感/MLCC，00981A近期掃貨'}},
  ];
  document.getElementById('allocBody').innerHTML = allocs.map(function(a,i){{
    return '<tr><td>' + (i+1) + '</td><td><strong>' + a.name + '</strong></td><td><strong>' + a.pct + '%</strong></td><td>' + a.logic + '</td><td><div class="bar-wrap"><div class="bar" style="width:' + a.pct + '%;background:var(--green)"></div></div></td></tr>';
  }}).join('');
}}

function renderTracks(){{
  var tracks = [
    {{id:'aTrack', codes:['2327','2308','2330','2383','2454'], label:'A 軌 營收確認型 50%'},
     id:'bTrack', codes:['2344','2408','3017','3711','6166','2303'], label:'B 軌 動能爆發型 30%'},
     id:'cTrack', codes:['6442','2375','7610'], label:'C 軌 地緣題材型 20%'}}];
  tracks.forEach(function(t){{
    var items = allStocks.filter(function(s){{ return t.codes.indexOf(s.code) >= 0; }});
    document.getElementById(t.id).innerHTML = items.map(function(s){{
      return '<div style="margin:4px 0;font-size:13px">' + s.name + ' <span class="float">' + s.code + '</span> <span style="float:right" class="' + pctClass(s.pct) + '">' + s.price + ' ' + (s.pct > 0 ? '+' : '') + s.pct + '%</span></div>';
    }}).join('') || '<div style="color:var(--muted);font-size:12px">--</div>';
  }});
}}

fetch('data.json')
  .then(function(r){{ return r.json(); }})
  .then(function(d){{
    document.getElementById('headerDate').textContent = d.date;
    document.getElementById('footerTime').textContent = d.updated;
    allStocks = d.stocks;
    renderSummary();
    renderTable();
    renderTierCards();
    renderAlloc();
    renderTracks();
  }})
  .catch(function(e){{
    document.querySelector('.container').insertAdjacentHTML('afterbegin', '<div class="alert" style="border-color:#f0465a;color:#fbb">讀取 data.json 失敗：' + e.message + '<br>請確認 GitHub Pages 已開啟，data.json 在根目錄。</div>');
  }});
</script>"""

FOOTER = "</body>\n</html>"

def render_dashboard(date):
    raw = STYLE + "\n<title>台股 AI 投資追蹤 — " + date + "</title>\n</head>\n<body>\n" + BODY_HEADER.replace("{date}", date) + FOOTER
    out = os.path.join(BASE, "dashboard.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(raw)
    print(f"[dashboard.html] -> {out}", flush=True)

def main():
    run_fetch = os.environ.get("RUN_FETCH","1") == "1"
    if run_fetch:
        import subprocess, sys
        subprocess.run([sys.executable, os.path.join(BASE, "fetch_twse.py")], check=False)

    date, stocks = load_snapshot()
    if not stocks:
        print("[warn] no new snapshot found; keeping existing data.json if any.", flush=True)
    else:
        stocks_map = {s["code"]: s for s in stocks}
        out = []
        for code in sorted(stocks_map.keys()):
            s = stocks_map[code]
            t = tier_of(code)
            m = tier_meta(t)
            out.append({
                "code": s["code"],
                "name": s["name"],
                "price": s["price"],
                "pct": s["pct"],
                "vol": s["vol"],
                "tier": t,
                "tier_label": m.get("label", t),
                "tier_cls": m.get("cls", "tier-t4"),
                "tier_color": m.get("color", "#7a8599"),
                "hold": m.get("hold", "--"),
                "note": NOTE.get(s["code"], ""),
            })

        with open(os.path.join(BASE, "data.json"), "w", encoding="utf-8") as f:
            json.dump({"date": date, "updated": datetime.now().isoformat(), "stocks": out}, f, ensure_ascii=False, indent=2)
        print(f"[data.json] written {len(out)} stocks at {date}", flush=True)

    # Always publish SPA as public pages
    for name in ("index.html", "dashboard_latest.html"):
        dst = os.path.join(BASE, name)
        src = os.path.join(BASE, "spa.html")
        with open(src, "r", encoding="utf-8") as s:
            with open(dst, "w", encoding="utf-8") as d:
                d.write(s.read())
        print(f"[copy] {name}", flush=True)

if __name__ == "__main__":
    main()
