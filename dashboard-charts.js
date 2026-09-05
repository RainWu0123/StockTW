// 圖表只使用已正規化且同日期的行情，不自行取價或寫入研究。
export const buckets = [
  { id:'down5', label:'< −5%', test:v=>v < -5, tone:'down' },
  { id:'down2', label:'−5～<−2%', test:v=>v >= -5 && v < -2, tone:'down' },
  { id:'down', label:'−2～<0%', test:v=>v >= -2 && v < 0, tone:'down' },
  { id:'flat', label:'0%', test:v=>v === 0, tone:'flat' },
  { id:'up', label:'>0～2%', test:v=>v > 0 && v <= 2, tone:'up' },
  { id:'up2', label:'>2～5%', test:v=>v > 2 && v <= 5, tone:'up' },
  { id:'up5', label:'> 5%', test:v=>v > 5, tone:'up' }
];
const $ = selector => document.querySelector(selector);
const pct = value => `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
const make = (tag, className, text) => {
  const el = document.createElement(tag);
  el.className = className || '';
  if (text !== undefined) el.textContent = String(text);
  return el;
};
const button = (className, label, callback) => {
  const el = make('button', className); el.type = 'button';
  el.setAttribute('aria-label', label); el.addEventListener('click', callback); return el;
};
const empty = text => make('p', 'chart-empty', text);
export const inBucket = (value, id) => Number.isFinite(value) && (buckets.find(b=>b.id === id)?.test(value) ?? false);

export function renderCharts({ base, selected, date, metric, expanded, range, industry, onStock, onRange, onIndustry }) {
  const sourceLabel = `行情檔 ${date || '日期未提供'} · data/live.json、data.json`;
  $('#chart-source').textContent = `${sourceLabel}。僅此日期樣本，排除不同日期、缺價格或缺漲跌；非即時行情、非全市場。`;
  $('#chart-count').textContent = `${selected.length} 檔 / 同日篩選樣本`;
  $('#chart-scope').textContent = `漲跌分布依搜尋、產業、ETF 與自選篩選；選取漲跌區間後，熱圖、產業圖與清單再連動。圖表固定採 1D，不是 1W／1M 走勢。`;
  const valueOf = stock => metric === 'gap' ? stock.gap : stock.currentPct;
  const eligible = selected.filter(s => Number.isFinite(valueOf(s)));
  const ordered = [...eligible].sort((a,b)=>Math.abs(valueOf(b))-Math.abs(valueOf(a)) || a.code.localeCompare(b.code));
  const limit = window.matchMedia('(max-width:700px)').matches ? 12 : 24;
  const visible = expanded ? ordered : ordered.slice(0,limit);
  $('#heatmap-title').textContent = metric === 'gap' ? '研究情境價差' : '個股漲跌熱圖';
  $('#heatmap-note').textContent = `${expanded ? '全部' : `絕對幅度前 ${limit} 檔`} · 顯示 ${visible.length} / ${eligible.length} 檔 · 每格等面積，不代表市值${metric === 'gap' ? '。紫色正價差、藍色負價差。Base ÷ 現價 − 1，目標為不同日期的舊研究情境，非預期報酬。' : '。紅漲綠跌，深色代表幅度較大。'}`;
  $('#heatmap-expand').textContent = expanded ? `收合至前 ${limit} 檔` : `展開全部 ${eligible.length} 檔`;
  $('#heatmap-expand').setAttribute('aria-expanded', String(expanded));
  $('#heatmap-expand').hidden = eligible.length <= limit;
  const scale = Math.max(1,...visible.map(s=>Math.abs(valueOf(s))));
  const heatmap = $('#heatmap');
  heatmap.replaceChildren(...visible.map(stock => {
    const value = valueOf(stock);
    const tone = value === 0 ? 'flat' : metric === 'gap' ? (value > 0 ? 'gap-plus' : 'gap-minus') : (value > 0 ? 'up' : 'down');
    const label = `${stock.code} ${stock.name}，${metric === 'gap' ? '情境價差' : '日漲跌'} ${pct(value)}，行情 ${date}，開啟詳細資料`;
    const tile = button(`heat-tile heat-${tone}`, label, () => onStock(stock));
    tile.dataset.code = stock.code;
    tile.style.setProperty('--intensity',`${Math.round(Math.abs(value)/scale*100)}%`);
    tile.append(make('span','heat-code',stock.code),make('strong','heat-name',stock.name),make('span','heat-value',pct(value)));
    const preview = () => {
      $('#chart-preview').textContent = `${stock.code} ${stock.name} · 現價 ${stock.currentPrice.toLocaleString('zh-TW')} 元 · ${metric === 'gap' ? '情境價差' : '日漲跌'} ${pct(value)} · ${stock.industry || '未分類'} · ${stock.priceSource} / ${date}`;
    };
    tile.addEventListener('pointerenter',preview); tile.addEventListener('focus',preview);
    return tile;
  }));
  if (!visible.length) heatmap.append(empty('此篩選範圍沒有可繪製資料，請調整條件。'));
  $('#chart-preview').textContent = visible.length ? '移到色塊或用 Tab 聚焦查看數字，點選開啟個股資料。' : '沒有符合條件的個股。';

  // 分布圖保留區間篩選前母體，讓使用者仍能切到其他區間。
  const counts = buckets.map(bucket => base.filter(s=>bucket.test(s.currentPct)).length);
  const maxCount = Math.max(1,...counts);
  $('#distribution-total').textContent = `${base.length} 檔`;
  $('#distribution').replaceChildren(...buckets.map((bucket,index) => {
    const count = counts[index], active = range === bucket.id;
    const column = button(`distribution-column ${bucket.tone}${active ? ' selected' : ''}`,`${bucket.label}：${count} 檔，${active ? '取消區間篩選' : '篩選此區間'}`,()=>onRange(active ? '' : bucket.id));
    column.dataset.bucket = bucket.id; column.dataset.count = String(count);
    column.setAttribute('aria-pressed',String(active));
    const plot = make('span','distribution-plot');
    const bar = make('span','distribution-bar'); bar.style.height = `${count/maxCount*100}%`;
    plot.append(bar);
    column.append(make('strong','distribution-count',count),plot,make('span','distribution-label',bucket.label));
    return column;
  }));
  $('#distribution-note').textContent = base.length ? `柱高代表檔數，共 ${base.length} 檔。點柱子交叉篩選，再點取消。` : '沒有同日期且有日漲跌的樣本。';

  const groups = new Map();
  selected.forEach(stock=>{
    if (!stock.industry) return;
    const group = groups.get(stock.industry) || []; group.push(stock); groups.set(stock.industry,group);
  });
  const sectors = [...groups].map(([name,stocks])=>({name,n:stocks.length,value:stocks.reduce((sum,s)=>sum+s.currentPct,0)/stocks.length}));
  const sorted = sectors.sort((a,b)=>Math.abs(b.value)-Math.abs(a.value) || a.name.localeCompare(b.name)).slice(0,6);
  const sectorMax = Math.max(1,...sorted.map(s=>Math.abs(s.value)));
  $('#sector-chart').replaceChildren(...sorted.map(sector=>{
    const row = button('sector-row',`${sector.name}，${sector.n} 檔，等權平均日漲跌 ${pct(sector.value)}，${industry === sector.name ? '取消產業篩選' : '篩選此產業'}`,()=>onIndustry(industry === sector.name ? '' : sector.name));
    row.dataset.industry = sector.name; row.dataset.value = sector.value;
    row.setAttribute('aria-pressed',String(industry === sector.name));
    row.append(make('span','sector-name',sector.name),make('small','sector-n',`${sector.n} 檔`));
    const track = make('span','sector-track');
    const bar = make('span',`sector-bar ${sector.value >= 0 ? 'positive' : 'negative'}`);
    bar.style.width = `${Math.abs(sector.value)/sectorMax*50}%`;
    track.append(bar);row.append(track,make('strong',sector.value > 0 ? 'up' : sector.value < 0 ? 'down' : 'na',pct(sector.value)));
    return row;
  }));
  if (!sorted.length) $('#sector-chart').append(empty('此篩選範圍沒有已分類的產業樣本。'));
  $('#sector-note').textContent = `按原快照產業欄位分組，等權平均日漲跌（%），絕對均幅前 6 組。排除 ${selected.filter(s=>!s.industry).length} 檔未分類；分類未重驗、非產業指數，單一樣本不代表產業。`;
}
