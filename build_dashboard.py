#!/usr/bin/env python3
"""重建 index.html：現代化深色儀表板，含研究目標價、主題篩選、追蹤狀態。
資料來源 data.json（已由 update_dashboard_data.py 同步最新價格與研究欄位）。"""
import json
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
data = json.loads((BASE/'data.json').read_text(encoding='utf-8'))
stocks = sorted(data['stocks'], key=lambda s: s.get('targetDist') if s.get('targetDist') is not None else -999)

def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def dist_badge(s):
    d = s.get('targetDist')
    if not s.get('target'): return '<span class="muted">—</span>'
    if d is None: return '<span class="muted">無報價</span>'
    cls = 'up' if d >= 0 else 'down'
    icon = '🔴 已達標' if d >= 0 else ('🟡 接近' if abs(d) <= 10 else f'<b class="{cls}">{d:+.1f}%</b>')
    return icon

rows = []
themes_seen = {}
for s in stocks:
    theme = s.get('researchTheme','')
    if theme:
        key = theme.split('/')[0]
        themes_seen[key] = themes_seen.get(key,0)+1
    rows.append(f'''<tr>
<td><a href="https://tw.stock.yahoo.com/quote/{s['code']}.TW" target="_blank">{s['code']}</a><br><small>{esc(s['name'])}</small></td>
<td>{s.get('price','—')}</td>
<td class="{'up' if (s.get('pct') or 0)>=0 else 'down'}">{(s.get('pct') or 0):+.2f}%</td>
<td>{s.get('score','—')}</td>
<td><span class="chip">{esc(theme or '未標記')}</span></td>
<td><b>{s['target'] if s.get('target') else '—'}</b></td>
<td>{dist_badge(s)}</td>
<td>{esc((s.get('industry') or '')[:8])}</td>
</tr>''')

theme_chips = ''.join(
    f'<button class="tchip" onclick="filterTheme(this)" data-t="{esc(t)}">{esc(t)} <span>{n}</span></button>'
    for t,n in sorted(themes_seen.items(), key=lambda x:-x[1]))

counts = {'total':len(stocks),
          'with_target':sum(1 for s in stocks if s.get('target')),
          'hit':sum(1 for s in stocks if s.get('targetDist') is not None and s['targetDist']>=0),
          'near':sum(1 for s in stocks if s.get('targetDist') is not None and -10<=s['targetDist']<0)}

html = '''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>StockTW 台股研究儀表板</title>
<style>
:root{--bg:#0d1117;--card:#161b22;--border:#30363d;--ink:#e6edf3;--muted:#7d8590;--green:#3fb950;--red:#f85149;--accent:#58a6ff;--warn:#d29922}
*{box-sizing:border-box;margin:0}body{background:var(--bg);color:var(--ink);font-family:-apple-system,"Noto Sans TC",sans-serif;line-height:1.6;padding:24px}
.wrap{max-width:1280px;margin:0 auto}
h1{font-size:1.6rem;margin-bottom:4px}.sub{color:var(--muted);margin-bottom:20px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:20px}
.stat{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px}
.stat b{font-size:1.5rem;display:block}.stat span{color:var(--muted);font-size:.85rem}
.tbar{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.tchip{background:var(--card);border:1px solid var(--border);color:var(--ink);border-radius:99px;padding:5px 14px;cursor:pointer;font-size:.88rem}
.tchip span{color:var(--muted);margin-left:4px}
.tchip.on{background:var(--accent);color:#000;border-color:var(--accent)}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:auto}
table{width:100%;border-collapse:collapse;font-size:.92rem;min-width:900px}
th{background:#1c2128;color:var(--muted);padding:10px 12px;text-align:left;position:sticky;top:0;cursor:pointer;user-select:none;white-space:nowrap}
td{padding:9px 12px;border-top:1px solid var(--border);vertical-align:top}
tr:hover td{background:#1c2128}
.up{color:var(--green)}.down{color:var(--red)}.muted{color:var(--muted)}
.chip{display:inline-block;background:#21262d;border:1px solid var(--border);border-radius:6px;padding:2px 8px;font-size:.8rem}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
footer{color:var(--muted);font-size:.82rem;margin-top:20px;text-align:center}
@media(max-width:720px){body{padding:12px}.stats{grid-template-columns:repeat(2,1fr)}}
</style></head><body><div class="wrap">
<h1>📊 StockTW 台股研究儀表板</h1>
<p class="sub">更新時間：UPDATED_AT ｜ 資料來源：官方財報＋TWSE 收盤｜目標價為本系統 Bear/Base/Bull 的 Base 情境（12 個月）</p>
<div class="stats">
<div class="stat"><b>COUNT_TOTAL</b><span>收錄個股</span></div>
<div class="stat"><b>COUNT_TARGET</b><span>有 Base 目標價</span></div>
<div class="stat"><b style="color:var(--red)">COUNT_HIT</b><span>已達標／透支</span></div>
<div class="stat"><b style="color:var(--warn)">COUNT_NEAR</b><span>接近 ±10%</span></div>
</div>
<div class="tbar" id="themes">THEME_CHIPS</div>
<div class="card"><table id="tbl">
<thead><tr><th data-k="code">代碼/名稱</th><th data-k="price">現價</th><th data-k="pct">漲跌</th><th data-k="score">評分</th><th>主題</th><th data-k="target">Base目標價</th><th data-k="targetDist">距離</th><th>產業</th></tr></thead>
<tbody>ROWS</tbody></table></div>
<footer>StockTW Research Dashboard ｜ 目標價不构成投資建議 ｜ 資料截止 DATA_CUTOFF</footer>
</div>
<script>
let curTheme=null;
function filterTheme(btn){
  const t=btn.dataset.t;
  document.querySelectorAll('.tchip').forEach(b=>b.classList.remove('on'));
  if(curTheme===t){curTheme=null}else{curTheme=t;btn.classList.add('on')}
  document.querySelectorAll('#tbl tbody tr').forEach(tr=>{
    const chip=tr.querySelector('.chip');
    tr.style.display=(curTheme===null||chip.textContent.trim().startsWith(curTheme))?'':'none';
  });
}
document.querySelectorAll('th[data-k]').forEach(th=>{
  th.addEventListener('click',()=>{
    const k=th.dataset.k, tb=document.querySelector('#tbl tbody');
    const asc=!(th.dataset.asc==='1');
    th.dataset.asc=asc?'1':'0';
    [...tb.rows].sort((a,b)=>{
      let x=a.cells[th.cellIndex].innerText.replace('%','').replace(/[+🔴🟡]/g,'').trim();
      let y=b.cells[th.cellIndex].innerText.replace('%','').replace(/[+🔴🟡]/g,'').trim();
      const nx=parseFloat(x),ny=parseFloat(y);
      if(!isNaN(nx)&&!isNaN(ny))return asc?nx-ny:ny-nx;
      return asc?x.localeCompare(y):y.localeCompare(x);
    }).forEach(r=>tb.appendChild(r));
  });
});
</script></body></html>'''

html = html.replace('UPDATED_AT', data['updated'][:16])
html = html.replace('DATA_CUTOFF', '2026-08-22')
html = html.replace('COUNT_TOTAL', str(counts['total']))
html = html.replace('COUNT_TARGET', str(counts['with_target']))
html = html.replace('COUNT_HIT', str(counts['hit']))
html = html.replace('COUNT_NEAR', str(counts['near']))
html = html.replace('THEME_CHIPS', theme_chips)
html = html.replace('ROWS', '\n'.join(rows))

(BASE/'index.html').write_text(html, encoding='utf-8')
print(f"index.html rebuilt: {len(rows)} rows, {len(themes_seen)} themes")
