#!/usr/bin/env python3
"""重建 StockTW 靜態研究儀表板。輸出 spa.html 與 index.html。"""
import json
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
data = json.loads((BASE / 'data.json').read_text(encoding='utf-8'))
GITHUB_BASE = 'https://github.com/RainWu0123/StockTW/blob/main/'
STATUS_ORDER = {'透支':0,'已達標':1,'接近':2,'低估':3,'未達標':4,'無報價':5,'無目標':6}
RESEARCH_ORDER = {'需重驗':0,'未驗證':1,'淺層':2,'草稿':3,'未分級':4,'可用':5,'深度':6,'無研究':7}
stocks = sorted(data.get('stocks', []), key=lambda s: (
    STATUS_ORDER.get(s.get('targetStatus', '無目標'), 9),
    RESEARCH_ORDER.get(s.get('researchStatus', '無研究'), 9),
    s.get('targetDist') if s.get('targetDist') is not None else 999,
))

def esc(value):
    return str(value if value is not None else '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def fmt_num(value, digits=2):
    if value is None:
        return '—'
    try:
        f = float(value)
    except (TypeError, ValueError):
        return esc(value)
    if f.is_integer():
        return str(int(f))
    return f'{f:.{digits}f}'.rstrip('0').rstrip('.')

def pct_cell(value):
    if value is None:
        return '<span class="muted">—</span>'
    cls = 'up' if value >= 0 else 'down'
    return f'<span class="{cls}">{value:+.2f}%</span>'

def etf_badges(s):
    etf_tags = s.get('etf_tags') or []
    tags = []
    if s.get('etf0050') or '0050' in etf_tags: tags.append(('0050','e50'))
    if s.get('etf00981A') or '00981A' in etf_tags: tags.append(('00981A','e981'))
    if s.get('etf00991A') or '00991A' in etf_tags: tags.append(('00991A','e991'))
    if s.get('etf00988A') or '00988A' in etf_tags: tags.append(('00988A','e988'))
    return ''.join(f'<span class="etf {cls}">{label}</span>' for label, cls in tags) or '<span class="muted">—</span>'

def status_badge(status):
    cls = {'透支':'danger','已達標':'danger','接近':'warn','低估':'good','未達標':'neutral','無報價':'mutedb','無目標':'mutedb'}.get(status, 'neutral')
    label = {'透支':'🔴 透支','已達標':'🔴 已達標','接近':'🟡 接近','低估':'🟢 低估'}.get(status, status or '—')
    return f'<span class="badge {cls}">{esc(label)}</span>'

def research_badge(status):
    cls = {'深度':'good','可用':'good','草稿':'warn','淺層':'warn','需重驗':'danger','未驗證':'danger','無研究':'mutedb','未分級':'neutral'}.get(status, 'neutral')
    return f'<span class="badge {cls}">{esc(status or "—")}</span>'

def dist_text(s):
    if not s.get('target'):
        return '<span class="muted">—</span>'
    d = s.get('targetDist')
    if d is None:
        return '<span class="muted">無報價</span>'
    cls = 'up' if d >= 0 else 'down'
    return f'<b class="{cls}">{d:+.1f}%</b>'

def qt_cell(s, key, label):
    d = (s.get('qt') or {}).get(key) or {}
    if not d:
        return f'<td data-label="{label}"><span class="muted">—</span></td>'
    score = d.get('score')
    signal = d.get('signal', '')
    reasons = esc(' / '.join(d.get('reasons', [])[:2]))
    cls = 'up' if isinstance(score, (int, float)) and score >= 20 else ('down' if isinstance(score, (int, float)) and score <= -10 else '')
    clean_signal = signal.split(' ', 1)[-1] if ' ' in signal else signal
    return f'<td data-label="{label}" class="{cls}" title="{reasons}">{fmt_num(score,0)}<br><small>{esc(clean_signal)}</small></td>'

def row(s):
    code = esc(s.get('code', ''))
    name = esc(s.get('name', code))
    research_file = s.get('researchFile') or ''
    href = GITHUB_BASE + esc(research_file) if research_file else GITHUB_BASE
    theme = s.get('researchTheme') or '未標記'
    theme_main = theme.split('/')[0]
    target_status = s.get('targetStatus') or '無目標'
    research_status = s.get('researchStatus') or '無研究'
    maturity = s.get('researchMaturity')
    age = s.get('researchAgeDays')
    verified = s.get('lastVerified') or '—'
    maturity_age = fmt_num(maturity,0) + (('/' + str(age) + '天') if age is not None else '')
    search_blob = ' '.join([str(s.get(x,'')) for x in ['code','name','industry','researchTheme','targetStatus','researchStatus']]).lower()
    return f'''<tr data-theme="{esc(theme_main)}" data-target-status="{esc(target_status)}" data-research-status="{esc(research_status)}" data-search="{esc(search_blob)}">
<td data-label="代碼/名稱"><b>{code}</b> <a href="{href}" target="_blank" rel="noopener noreferrer">{name}</a></td>
<td data-label="現價">{fmt_num(s.get('price'))}</td>
<td data-label="漲跌">{pct_cell(s.get('pct'))}</td>
<td data-label="狀態">{status_badge(target_status)}<br><small>{dist_text(s)}</small></td>
<td data-label="Base目標價"><b>{fmt_num(s.get('target'))}</b></td>
<td data-label="研究">{research_badge(research_status)}<br><small>{esc(verified)}｜{maturity_age}</small></td>
<td data-label="主題"><span class="chip">{esc(theme)}</span></td>
<td data-label="ETF">{etf_badges(s)}</td>
{qt_cell(s, 'qt_short', '短線')}{qt_cell(s, 'qt_long', '長線')}
<td data-label="產業">{esc(s.get('industry') or '')}</td>
</tr>'''

summary = data.get('research_summary', {})
target_counts = summary.get('target_status_counts', {})
research_counts = summary.get('status_counts', {})
with_target = sum(1 for s in stocks if s.get('target'))
need_review = sum(1 for s in stocks if s.get('researchStatus') in {'需重驗','未驗證','淺層','草稿'})
watch_list = sum(1 for s in stocks if s.get('targetStatus') in {'透支','已達標','接近','低估'})
stat_cards = [('收錄個股',len(stocks),''),('有 Base 目標價',with_target,''),('交易雷達',watch_list,'warn'),('研究需處理',need_review,'danger'),('深度/可用研究',research_counts.get('深度',0)+research_counts.get('可用',0),'good')]
all_themes = {}
for s in stocks:
    t = (s.get('researchTheme') or '未標記').split('/')[0]
    all_themes[t] = all_themes.get(t, 0) + 1

def chip_buttons(items, attr):
    return ''.join(f'<button class="filter-chip" data-{attr}="{esc(k)}">{esc(k)} <span>{v}</span></button>' for k, v in items)

theme_chips = chip_buttons(sorted(all_themes.items(), key=lambda kv: -kv[1])[:28], 'theme')
target_chips = chip_buttons([(k, target_counts.get(k, 0)) for k in ['透支','已達標','接近','低估','未達標','無報價','無目標'] if target_counts.get(k, 0)], 'target')
research_chips = chip_buttons([(k, research_counts.get(k, 0)) for k in ['需重驗','未驗證','淺層','草稿','未分級','可用','深度','無研究'] if research_counts.get(k, 0)], 'research')
rows = '\n'.join(row(s) for s in stocks)
stats_html = ''.join(f'<div class="stat {cls}"><b>{num}</b><span>{label}</span></div>' for label, num, cls in stat_cards)

html = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>StockTW 台股研究決策雷達</title>
<style>
:root{{--bg:#0d1117;--card:#161b22;--card2:#1c2128;--border:#30363d;--ink:#e6edf3;--muted:#7d8590;--green:#3fb950;--red:#f85149;--accent:#58a6ff;--warn:#d29922;--blue:#79c0ff}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at top left,#172033 0,#0d1117 34rem);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC","Segoe UI",sans-serif;line-height:1.55;padding:24px}}
.wrap{{max-width:1480px;margin:0 auto}}h1{{font-size:1.75rem;margin:0 0 4px}}.sub{{color:var(--muted);margin:0 0 18px}}.panel{{background:rgba(22,27,34,.92);border:1px solid var(--border);border-radius:16px;padding:16px;margin-bottom:16px;box-shadow:0 10px 30px rgba(0,0,0,.18)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:12px}}.stat{{background:var(--card2);border:1px solid var(--border);border-radius:14px;padding:13px}}.stat b{{font-size:1.55rem;display:block}}.stat span{{color:var(--muted);font-size:.86rem}}.stat.good b{{color:var(--green)}}.stat.warn b{{color:var(--warn)}}.stat.danger b{{color:var(--red)}}
.controls{{display:grid;gap:10px}}.search{{width:100%;background:#0d1117;border:1px solid var(--border);border-radius:12px;color:var(--ink);padding:11px 13px;font-size:1rem}}.filter-row{{display:flex;gap:8px;overflow-x:auto;padding-bottom:2px;scrollbar-width:thin}}.filter-label{{flex:0 0 auto;color:var(--muted);font-size:.85rem;padding:6px 2px}}.filter-chip{{flex:0 0 auto;background:#21262d;border:1px solid var(--border);color:var(--ink);border-radius:999px;padding:6px 12px;cursor:pointer}}.filter-chip span{{color:var(--muted);margin-left:3px}}.filter-chip.on{{background:var(--accent);border-color:var(--accent);color:#07111f}}.filter-chip.on span{{color:#07111f}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:16px;overflow:auto}}table{{width:100%;border-collapse:collapse;font-size:.91rem;min-width:1320px}}th{{background:#1c2128;color:var(--muted);padding:10px 12px;text-align:left;position:sticky;top:0;white-space:nowrap;cursor:pointer;user-select:none;z-index:2}}td{{padding:10px 12px;border-top:1px solid var(--border);vertical-align:top}}tr:hover td{{background:#1b2430}}a{{color:var(--blue);text-decoration:none}}a:hover{{text-decoration:underline}}small{{color:var(--muted)}}.up{{color:var(--green)}}.down{{color:var(--red)}}.muted{{color:var(--muted)}}
.badge,.chip,.etf{{display:inline-block;border-radius:7px;padding:2px 8px;font-size:.78rem;border:1px solid var(--border);background:#21262d}}.badge.good{{color:var(--green);border-color:#285a35;background:#13251a}}.badge.warn{{color:var(--warn);border-color:#5b4318;background:#2a2111}}.badge.danger{{color:var(--red);border-color:#6a2a29;background:#2a1517}}.badge.neutral{{color:var(--blue)}}.badge.mutedb{{color:var(--muted)}}.chip{{font-size:.8rem}}.etf{{font-size:.67rem;margin-right:4px}}.e50{{background:#1f3a5f;color:#79b8ff;border-color:#2d4a6f}}.e981{{background:#3a2f1f;color:#e2b45a;border-color:#5a4a2d}}.e991{{background:#24361f;color:#8ddb8c;border-color:#36522f}}.e988{{background:#3b243f;color:#d2a8ff;border-color:#55395c}}
td[title]{{cursor:help}}footer{{color:var(--muted);font-size:.82rem;text-align:center;margin-top:18px}}.legend{{color:var(--muted);font-size:.86rem;margin-top:8px}}
@media(max-width:760px){{body{{padding:12px}}h1{{font-size:1.35rem}}.stats{{grid-template-columns:repeat(2,1fr)}}.panel{{padding:12px}}table{{font-size:.86rem;min-width:1180px}}th,td{{padding:9px 10px}}}}
</style></head><body><div class="wrap">
<h1>📊 StockTW 台股研究決策雷達</h1>
<p class="sub">更新時間：{esc(str(data.get('updated',''))[:19])} ｜ 來源：data.json + data/live.json + research frontmatter ｜ Base 目標價是研究模型情境，不是投資建議。</p>
<section class="panel"><div class="stats">{stats_html}</div><div class="controls">
<input id="q" class="search" placeholder="搜尋代碼、名稱、主題、產業、狀態…">
<div class="filter-row" id="targetFilters"><span class="filter-label">目標狀態</span>{target_chips}</div>
<div class="filter-row" id="researchFilters"><span class="filter-label">研究品質</span>{research_chips}</div>
<div class="filter-row" id="themeFilters"><span class="filter-label">主題</span>{theme_chips}</div>
<div class="legend">🔴 透支/已達標：不是買進訊號，是需要復盤或等待新 thesis 的警示。🟢 低估：只代表現價低於 Base 目標價 30% 以上，仍需確認賣出條件未觸發。</div>
</div></section>
<div class="card"><table id="tbl"><thead><tr><th>代碼/名稱</th><th>現價</th><th>漲跌</th><th>目標狀態</th><th>Base目標價</th><th>研究狀態</th><th>主題</th><th>ETF</th><th>短線</th><th>長線</th><th>產業</th></tr></thead><tbody>{rows}</tbody></table></div>
<footer>StockTW Research Dashboard ｜ 研究過期規則：last_verified 超過 {summary.get('stale_days',30)} 天列為需重驗 ｜ 資料筆數 {len(stocks)}</footer>
</div><script>
const state={{theme:null,target:null,research:null,q:''}};
function setActive(container, key, val, btn){{document.querySelectorAll('#'+container+' .filter-chip').forEach(b=>b.classList.remove('on'));if(state[key]===val){{state[key]=null;}}else{{state[key]=val;btn.classList.add('on');}}applyFilters();}}
function applyFilters(){{const q=state.q.trim().toLowerCase();document.querySelectorAll('#tbl tbody tr').forEach(tr=>{{const okTheme=!state.theme||tr.dataset.theme===state.theme;const okTarget=!state.target||tr.dataset.targetStatus===state.target;const okResearch=!state.research||tr.dataset.researchStatus===state.research;const okQ=!q||tr.dataset.search.includes(q);tr.style.display=(okTheme&&okTarget&&okResearch&&okQ)?'':'none';}});}}
document.querySelectorAll('#themeFilters .filter-chip').forEach(btn=>btn.addEventListener('click',()=>setActive('themeFilters','theme',btn.dataset.theme,btn)));
document.querySelectorAll('#targetFilters .filter-chip').forEach(btn=>btn.addEventListener('click',()=>setActive('targetFilters','target',btn.dataset.target,btn)));
document.querySelectorAll('#researchFilters .filter-chip').forEach(btn=>btn.addEventListener('click',()=>setActive('researchFilters','research',btn.dataset.research,btn)));
document.getElementById('q').addEventListener('input',e=>{{state.q=e.target.value;applyFilters();}});
document.querySelectorAll('th').forEach(th=>th.addEventListener('click',()=>{{const tb=document.querySelector('#tbl tbody'),idx=th.cellIndex,asc=!(th.dataset.asc==='1');th.dataset.asc=asc?'1':'0';[...tb.rows].sort((a,b)=>{{const tx=r=>r.cells[idx].innerText.replace('%','').replace(/[+🔴🟡🟢]/g,'').trim();const x=tx(a),y=tx(b),nx=parseFloat(x),ny=parseFloat(y);if(!isNaN(nx)&&!isNaN(ny))return asc?nx-ny:ny-nx;return asc?x.localeCompare(y,'zh-Hant'):y.localeCompare(x,'zh-Hant');}}).forEach(r=>tb.appendChild(r));}}));
</script></body></html>'''
for name in ['spa.html', 'index.html']:
    (BASE / name).write_text(html, encoding='utf-8')
print(f"dashboard rebuilt: {len(stocks)} rows; wrote spa.html and index.html")
