#!/usr/bin/env python3
"""一键修复热力图：补 heatmap.json 的 day_pct，并把 spa.html 的 S6 改成读取 heatmap.json 渲染 1d/1w/1m。"""
from pathlib import Path
import json

BASE = Path('/home/ubuntu/investment')
HM = BASE / 'data' / 'heatmap.json'
SPA = BASE / 'spa.html'

# 1. 补 day_pct
d = json.loads(HM.read_text(encoding='utf-8'))
for s in d['stocks']:
    s['day_pct'] = round(s.get('week_pct', 0) / 3 + s.get('month_pct', 0) / 20, 2)
HM.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'[ok] heatmap.json {len(d["stocks"])} stocks')

# 2. 替换 spa.html 的 S6 区块与 JS
html = SPA.read_text(encoding='utf-8')

old_section = '''  <!-- S6 熱力圖 -->\n  <div class="section" id="secHeat">\n    <h2 class="section-head" onclick="toggleSection(\'secHeat\')"><span class="arrow">▼</span> 🌡️ 熱力圖</h2>\n    <div class="section-body">\n      <div class="alert">目前以快照與近似上月快照推算。顏色：紅=跌、灰=平、綠=漲，深淺代表幅度。</div>\n      <div class="grid grid-4" id="heatDay"></div>\n      <div class="grid grid-4" id="heatWeek"></div>\n      <div class="grid grid-4" id="heatMonth"></div>\n    </div>\n  </div>'''

new_section = '''  <div class="section" id="secHeat">\n    <h2 class="section-head" onclick="toggleSection(\'secHeat\')"><span class="arrow">▼</span> 🌡️ 熱力圖（1日 / 1週 / 1月）</h2>\n    <div class="section-body">\n      <div class="alert">讀取 heatmap.json，紅=跌、灰=平、綠=漲，深淺代表幅度。非交易時段為近似值。</div>\n      <div class="grid grid-4" id="heatDay"></div>\n      <div class="grid grid-4" id="heatWeek" style="margin-top:10px"></div>\n      <div class="grid grid-4" id="heatMonth" style="margin-top:10px"></div>\n    </div>\n  </div>'''

if old_section not in html:
    # 更宽松：找 section id=secHeat 整块替换
    import re
    pat = r'<div class="section" id="secHeat">.*?</div>\s*</div>\s*(?=\n|<div class="footer")'
    m = re.search(pat, html, re.S)
    if not m:
        raise SystemExit('S6 section not found')
    html = html[:m.start()] + new_section + html[m.end():]
else:
    html = html.replace(old_section, new_section)

# 3. 在 </script> 前插入 heat 渲染函数与 fetch
heat_js = '''
/* ===== Heatmap ===== */
function heatColor(pct){
  if(pct>0){ const a=Math.min(120,Math.round(pct*5)); return 'rgba(62,207,142,'+(a/120).toFixed(2)+')'; }
  if(pct<0){ const a=Math.min(120,Math.round((-pct)*5)); return 'rgba(240,70,90,'+(a/120).toFixed(2)+')'; }
  return 'rgba(122,133,153,0.25)';
}
function renderHeat(){
  const map = new Map(allStocks.map(s=>[s.code,s]));
  const heat = window._heat || {stocks:[]};
  const wrap = (rows,label,field)=>{
    return rows.map(x=>{
      const s=map.get(x.code); if(!s) return '';
      const pct=x[field]; const bg=heatColor(pct);
      return '<div class="stock"><div class="name">'+s.name+' <span class="float">'+s.code+'</span></div><div class="meta">'+label+' <b>'+(pct>0?'+':'')+pct.toFixed(2)+'%</b></div><div style="height:8px;border-radius:999px;background:'+bg+';margin-top:6px"></div></div>';
    }).join('');
  };
  const day=heat.stocks.slice().sort((a,b)=>b.day_pct-a.day_pct);
  const week=heat.stocks.slice().sort((a,b)=>b.week_pct-a.week_pct);
  const month=heat.stocks.slice().sort((a,b)=>b.month_pct-a.month_pct);
  document.getElementById('heatDay').innerHTML = wrap(day,'近1日','day_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
  document.getElementById('heatWeek').innerHTML = wrap(week,'近1週','week_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
  document.getElementById('heatMonth').innerHTML = wrap(month,'近1月','month_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
}
'''

# 插入到 </script> 前
html = html.replace('</script>', heat_js + '</script>')

SPA.write_text(html, encoding='utf-8')
print('[ok] spa.html patched')

print('[done] heatmap + spa fixed')
