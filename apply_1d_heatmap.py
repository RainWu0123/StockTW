
from pathlib import Path
import re

p = Path('/home/ubuntu/investment/spa.html')
s = p.read_text(encoding='utf-8')

old_section = '''  <!-- S6 熱力圖 -->
  <div class="section" id="secHeat">
    <h2 class="section-head" onclick="toggleSection('secHeat')"><span class="arrow">▼</span> 🌡️ 熱力圖（1週 / 1月）</h2>
    <div class="section-body">
      <div class="alert">目前以快照推算近 1 週、近 1 月漲跌幅近似值，非交易時段會以假資料呈現。顏色：紅=跌、灰=平、綠=漲，深淺代表幅度。</div>
      <div class="grid grid-4" id="heatWeek"></div>
      <div class="grid grid-4" id="heatMonth" style="margin-top:12px"></div>
    </div>
  </div>'''
new_section = '''  <!-- S6 熱力圖 -->
  <div class="section" id="secHeat">
    <h2 class="section-head" onclick="toggleSection('secHeat')"><span class="arrow">▼</span> 🌡️ 熱力圖（1日 / 1週 / 1月）</h2>
    <div class="section-body">
      <div class="alert">目前以快照推算近 1 日、近 1 週、近 1 月漲跌幅近似值，非交易時段會以假資料呈現。顏色：紅=跌、灰=平、綠=漲，深淺代表幅度。</div>
      <div class="grid grid-4" id="heatDay"></div>
      <div class="grid grid-4" id="heatWeek" style="margin-top:12px"></div>
      <div class="grid grid-4" id="heatMonth" style="margin-top:12px"></div>
    </div>
  </div>'''
if old_section not in s:
    raise SystemExit('section block not found')
s = s.replace(old_section, new_section)

old_fn = '''/* ===== Heatmap ===== */
function heatColor(pct){
  if(pct > 0){
    const a = Math.min(120, Math.round(pct * 5));
    return 'rgba(62,207,142,' + (a/120).toFixed(2) + ')'; // green
  }
  if(pct < 0){
    const a = Math.min(120, Math.round((-pct) * 5));
    return 'rgba(240,70,90,' + (a/120).toFixed(2) + ')';  // red
  }
  return 'rgba(122,133,153,0.25)';
}
function renderHeat(){
  const map = new Map(allStocks.map(s=>[s.code, s]));
  const heat = window._heat || {stocks:[]};
  const byCode = {};
  heat.stocks.forEach(function(x){ byCode[x.code]=x; });
  const wrap = function(rows, label, field){
    return rows.map(function(x){
      const s = map.get(x.code);
      if(!s) return '';
      const pct = x[field];
      const bg = heatColor(pct);
      return '<div class="stock"><div class="name">'+s.name+' <span class="float">'+s.code+'</span></div><div class="meta">'+label+' <b>'+(pct>0?'+':'')+pct.toFixed(2)+'%</b></div><div style="height:8px;border-radius:999px;background:'+bg+';margin-top:6px"></div></div>';
    }).join('');
  };
  const week = heat.stocks.slice().sort((a,b)=>b.week_pct-a.week_pct);
  const month = heat.stocks.slice().sort((a,b)=>b.month_pct-a.month_pct);
  document.getElementById('heatWeek').innerHTML = wrap(week, '近1週', 'week_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
  document.getElementById('heatMonth').innerHTML = wrap(month, '近1月', 'month_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
}'''
new_fn = '''/* ===== Heatmap ===== */
function heatColor(pct){
  if(pct > 0){
    const a = Math.min(120, Math.round(pct * 5));
    return 'rgba(62,207,142,' + (a/120).toFixed(2) + ')'; // green
  }
  if(pct < 0){
    const a = Math.min(120, Math.round((-pct) * 5));
    return 'rgba(240,70,90,' + (a/120).toFixed(2) + ')';  // red
  }
  return 'rgba(122,133,153,0.25)';
}
function renderHeat(){
  const map = new Map(allStocks.map(s=>[s.code, s]));
  const heat = window._heat || {stocks:[]};
  const byCode = {};
  heat.stocks.forEach(function(x){ byCode[x.code]=x; });
  const wrap = function(rows, label, field){
    return rows.map(function(x){
      const s = map.get(x.code);
      if(!s) return '';
      const pct = x[field];
      const bg = heatColor(pct);
      return '<div class="stock"><div class="name">'+s.name+' <span class="float">'+s.code+'</span></div><div class="meta">'+label+' <b>'+(pct>0?'+':'')+pct.toFixed(2)+'%</b></div><div style="height:8px;border-radius:999px;background:'+bg+';margin-top:6px"></div></div>';
    }).join('');
  };
  const day = heat.stocks.slice().sort((a,b)=>b.day_pct-a.day_pct);
  const week = heat.stocks.slice().sort((a,b)=>b.week_pct-a.week_pct);
  const month = heat.stocks.slice().sort((a,b)=>b.month_pct-a.month_pct);
  document.getElementById('heatDay').innerHTML = wrap(day, '近1日', 'day_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
  document.getElementById('heatWeek').innerHTML = wrap(week, '近1週', 'week_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
  document.getElementById('heatMonth').innerHTML = wrap(month, '近1月', 'month_pct') || '<div class="alert" style="border-color:#252a36;color:var(--muted)">暫無heat data</div>';
}'''
if old_fn not in s:
    raise SystemExit('heat render fn not found')
s = s.replace(old_fn, new_fn)
p.write_text(s, encoding='utf-8')
print('patched spa.html with 1d heatmap')
