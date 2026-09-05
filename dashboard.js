import { renderCharts, buckets, inBucket } from './dashboard-charts.js?v=charts-dark-1';

(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const state = { stocks: [], view: 'all', period: 'day', favorites: new Set(), lastFocus: null, generation: 0, range: '', metric: 'day', expanded: false };
  const number = value => typeof value === 'number' && Number.isFinite(value) ? value : null;
  const display = value => value === undefined || value === null || value === '' ? '未提供' : String(value);
  const nf = new Intl.NumberFormat('zh-TW', { maximumFractionDigits: 2 });
  const fmt = value => number(value) === null ? '未提供' : nf.format(value);
  const timestamp = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}/.test(value) && Number.isFinite(Date.parse(value)) ? Date.parse(value) : null;
  const dateLabel = value => timestamp(value) === null ? '未提供' : value.slice(0, 10);
  const age = value => timestamp(value) === null ? null : Math.floor((Date.now() - timestamp(value)) / 86400000);
  const make = (tag, cls = '', value) => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (value !== undefined) el.textContent = display(value);
    return el;
  };
  const text = (selector, value) => { $(selector).textContent = display(value); };
  const percent = value => number(value) === null ? '未提供' : `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
  const direction = value => number(value) === null || value === 0 ? 'na' : value > 0 ? 'up' : 'down';

  function updateTheme() {
    const dark = document.documentElement.dataset.theme === 'dark';
    $('#theme-toggle').setAttribute('aria-pressed', String(dark));
    $('#theme-toggle').setAttribute('aria-label', `${dark ? '暗黑' : '淺色'}模式，切換至${dark ? '淺色' : '暗黑'}`);
    text('#theme-label', dark ? '暗黑' : '淺色');
    $('meta[name="theme-color"]').content = dark ? '#0c111b' : '#f3f5fa';
  }
  $('#theme-toggle').addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('stocktw:theme', theme); }
    catch (_) { text('#storage-note', '此瀏覽器無法儲存，外觀選擇僅保留至本頁關閉。'); }
    updateTheme();
  });
  updateTheme();

  try {
    const saved = JSON.parse(localStorage.getItem('stocktw:favorites') || '[]');
    if (Array.isArray(saved)) state.favorites = new Set(saved.filter(x => typeof x === 'string' && /^\d{4,6}[A-Z]?$/.test(x)));
  } catch (_) { /* 儲存不可用不阻擋閱讀。 */ }

  function toggleFavorite(stock, source) {
    const code = String(stock.code);
    state.favorites.has(code) ? state.favorites.delete(code) : state.favorites.add(code);
    try { localStorage.setItem('stocktw:favorites', JSON.stringify([...state.favorites])); }
    catch (_) { text('#storage-note', '此瀏覽器無法儲存，自選僅保留至本頁關閉。'); }
    render();
    const next = [...document.querySelectorAll('.star')].find(el => el.dataset.code === code);
    if (next) next.focus(); else if (source) $('[data-view="favorites"]').focus();
  }

  function normalize(stock, data, live) {
    const code = String(stock.code);
    const quote = live?.prices?.[code];
    // updated 是建站時間，不可當成行情時間。
    const baseDate = stock.priceDate || stock.date || data.date;
    const liveDate = quote?.date || live?.date;
    const useLive = number(quote?.price) !== null && quote.price > 0 && timestamp(liveDate) !== null && (timestamp(baseDate) === null || timestamp(liveDate) >= timestamp(baseDate));
    const source = useLive ? quote : stock;
    const price = number(source.price) !== null && source.price > 0 ? source.price : null;
    const target = number(stock.target) !== null && stock.target > 0 ? stock.target : null;
    const etfs = Object.entries(state.etfMap).filter(([, codes]) => Array.isArray(codes) && codes.map(String).includes(code)).map(([id]) => id);
    return { ...stock, code, currentPrice: price, currentPct: number(source.pct), volume: number(source.vol), target,
      gap: price !== null && target !== null ? (target / price - 1) * 100 : null,
      priceDate: useLive ? liveDate : baseDate, priceSource: useLive ? 'data/live.json' : 'data.json', etfs };
  }

  // 既有 week_pct/month_pct 無區間與日期契約，包含占位 0，全數不作績效使用。
  const performance = stock => state.period === 'day' ? stock.currentPct : null;
  function populateFilters() {
    const options = [
      ['#industry', '全部產業', [...new Set(state.stocks.map(s => s.industry || '未分類'))]],
      ['#research-status', '全部狀態', [...new Set(state.stocks.map(s => s.researchStatus || '未標示'))]],
      ['#etf', '全部 ETF', [...new Set(state.stocks.flatMap(s => s.etfs))]]
    ];
    options.forEach(([selector, title, values]) => {
      const select = $(selector), previous = select.value;
      const empty = make('option', '', title); empty.value = '';
      select.replaceChildren(empty);
      values.sort((a, b) => a.localeCompare(b, 'zh-Hant')).forEach(value => {
        const option = make('option', '', value); option.value = value; select.append(option);
      });
      select.value = values.includes(previous) ? previous : '';
    });
  }

  function renderStats() {
    const total = state.stocks.length;
    const priced = state.stocks.filter(s => s.currentPrice !== null).length;
    const available = state.stocks.filter(s => s.currentPct !== null);
    const rising = available.filter(s => s.currentPct > 0).length;
    const falling = available.filter(s => s.currentPct < 0).length;
    const values = [
      ['追蹤個股', total, '研究清單，不代表全市場'],
      ['有價格', priced, `${total - priced} 筆缺值 · 新臺幣／股`],
      ['上漲 / 下跌', `${rising} / ${falling}`, `${available.length} 筆有日漲跌 · 各來源日期不同`],
      ['有 Base 情境', state.stocks.filter(s => s.target !== null).length, '舊研究模型，非買賣訊號']
    ];
    $('#stats').replaceChildren(...values.map(([label, value, note]) => {
      const el = make('div', 'stat'); el.append(make('span', '', label), make('strong', '', value), make('small', '', note)); return el;
    }));
  }

  function renderQuality() {
    const dates = [...new Set(state.stocks.filter(s => s.currentPrice !== null).map(s => dateLabel(s.priceDate)))].sort();
    const stale = state.stocks.filter(s => age(s.priceDate) !== null && age(s.priceDate) > 7).length;
    const old = state.stocks.filter(s => age(s.lastVerified) !== null && age(s.lastVerified) > 30).length;
    const unknown = state.stocks.filter(s => timestamp(s.lastVerified) === null).length;
    const rows = [
      ['行情檔標示日期', dates.join('、') || '未提供'],
      ['行情距今逾 7 天', `${stale} 筆`],
      ['研究中繼資料快照', dateLabel(state.researchDate)],
      ['研究驗證逾 30 天', `${old} 筆`],
      ['無研究驗證日期', `${unknown} 筆`],
      ['ETF 成分日期', '未提供，僅供清單篩選']
    ];
    $('#quality-list').replaceChildren(...rows.flatMap(([label, value]) => [make('dt', '', label), make('dd', '', value)]));
    text('#data-status', stale ? '歷史行情快照' : '已載入來源快照');
    text('#data-updated', `行情檔日期 ${dateLabel(state.live?.date || state.dataDate)}`);
    $('#load-note').textContent = state.warnings.join(' ');
  }

  function reportURL(value) {
    if (typeof value !== 'string' || !/^research\/[^/\\]+\.md$/.test(value) || value.includes('..')) return null;
    return `https://github.com/RainWu0123/StockTW/blob/main/research/${encodeURIComponent(value.slice('research/'.length))}`;
  }

  function renderCard(stock) {
    const card = make('article', 'stock-card'); card.dataset.code = stock.code;
    const top = make('div', 'stock-top');
    const starred = state.favorites.has(stock.code);
    const star = make('button', `star${starred ? ' on' : ''}`, starred ? '★' : '☆');
    star.type = 'button'; star.dataset.code = stock.code;
    star.setAttribute('aria-pressed', String(starred));
    star.setAttribute('aria-label', `${starred ? '移除' : '加入'}自選 ${stock.code} ${display(stock.name)}`);
    star.addEventListener('click', () => toggleFavorite(stock, star));
    const open = make('button', 'stock-open', stock.name); open.type = 'button';
    open.setAttribute('aria-label', `${stock.code} ${display(stock.name)} 詳細資料`);
    open.addEventListener('click', () => openDrawer(stock));
    top.append(star, make('div', 'code', stock.code), open, make('div', 'stock-industry', stock.industry || '未分類'));
    const row = make('div', 'price-row');
    row.append(make('span', `price${stock.currentPrice === null ? ' na' : ''}`, fmt(stock.currentPrice)), make('span', direction(performance(stock)), state.period === 'day' ? percent(performance(stock)) : `${state.period === 'week' ? '週' : '月'}績效未提供`));
    const meta = make('div', 'card-meta');
    meta.append(make('span', 'pill', `研究快照 · ${stock.researchStatus || '未標示'}`));
    if (stock.target !== null) meta.append(make('span', 'pill', `Base ${fmt(stock.target)}`));
    if (stock.gap !== null) meta.append(make('span', 'pill', `情境價差 ${percent(stock.gap)}`));
    card.append(top, row, meta, make('div', 'theme', stock.researchTheme || '未分類'));
    if (stock.etfs.length) card.append(make('div', 'etf-line', stock.etfs.join(' · ')));
    card.append(make('div', 'card-source', `${stock.priceSource} · ${dateLabel(stock.priceDate)}${age(stock.priceDate) > 7 ? ' · 舊行情' : ''}`));
    return card;
  }

  function filtered() {
    const q = $('#search').value.trim().toLocaleLowerCase(), industry = $('#industry').value, research = $('#research-status').value, etf = $('#etf').value;
    const key = $('#sort').value;
    return state.stocks.filter(s => (!q || [s.code, s.name, s.industry, s.researchTheme, s.researchStatus].some(v => String(v || '').toLocaleLowerCase().includes(q))) && (!industry || (s.industry || '未分類') === industry) && (!research || (s.researchStatus || '未標示') === research) && (!etf || s.etfs.includes(etf)) && (state.view === 'all' || state.favorites.has(s.code)))
      .sort((a, b) => {
        if (key === 'code') return a.code.localeCompare(b.code);
        const value = s => key === 'verified' ? timestamp(s.lastVerified) : key === 'price' ? s.currentPrice : key === 'pct' ? performance(s) : key === 'gap' ? s.gap : s.target;
        const av = value(a), bv = value(b);
        if (av === null && bv === null) return a.code.localeCompare(b.code);
        if (av === null) return 1;
        if (bv === null) return -1;
        return bv - av || a.code.localeCompare(b.code);
      });
  }

  function render() {
    const base = filtered();
    const chartDate = state.stocks.filter(s => s.currentPrice !== null && timestamp(s.priceDate) !== null).map(s => s.priceDate.slice(0,10)).sort().at(-1) || '';
    const sameDate = s => s.currentPrice !== null && number(s.currentPct) !== null && s.priceDate?.slice(0,10) === chartDate;
    const list = state.range ? base.filter(s => sameDate(s) && inBucket(s.currentPct, state.range)) : base;
    $('#chart-filter-note').textContent = state.range ? `圖表篩選：${buckets.find(b => b.id === state.range).label}，行情 ${chartDate}。再次點選柱子，或「清除篩選」可取消。` : '';
    renderCharts({ base: base.filter(sameDate), selected: list.filter(sameDate), date: chartDate, metric: state.metric, expanded: state.expanded, range: state.range, industry: $('#industry').value,
      onStock: openDrawer,
      onRange: id => { state.range = id; render(); const target = id ? document.querySelector(`[data-bucket="${id}"]`) : $('#reset'); target.focus(); },
      onIndustry: industry => { $('#industry').value = industry; state.range = ''; render(); $('#industry').focus(); }
    });
    $('#list').replaceChildren(...(list.length ? list.map(renderCard) : [make('div', 'empty', state.view === 'favorites' ? '沒有符合條件的自選。請清除篩選，或在全部清單加入星號。' : '沒有符合條件的資料，請調整搜尋或清除篩選。')]));
    text('#result-count', `${list.length} / ${state.stocks.length} 筆`);
    text('#favorite-count', state.stocks.filter(s => state.favorites.has(s.code)).length);
    text('#period-note', state.period === 'day' ? '1D：個別來源的日漲跌，紅漲綠跌。情境價差＝Base ÷ 現價 − 1，不代表報酬預測。' : `${state.period === 'week' ? '1W' : '1M'}：現有資料缺少可驗證的區間日期，暫不提供績效，也不把占位 0 當報酬。`);
  }

  function detail(label, value) {
    const el = make('div', 'detail-item'); el.append(make('span', '', label), make('strong', '', value)); return el;
  }
  function openDrawer(stock) {
    state.lastFocus = document.activeElement;
    const root = $('#drawer-content'); root.replaceChildren();
    const head = make('div');
    const title = make('h2', '', `${stock.code} ${display(stock.name)}`); title.id = 'drawer-title';
    head.append(make('div', 'eyebrow', 'STOCK PROFILE / 個股資料'), title, make('div', 'big-price', fmt(stock.currentPrice)), make('p', direction(performance(stock)), `本期間漲跌 ${percent(performance(stock))}`), make('p', 'card-source', `新臺幣／股 · ${stock.priceSource} · 行情檔日期 ${dateLabel(stock.priceDate)}`));
    const grid = make('div', 'detail-grid');
    [ ['研究狀態（舊快照）', stock.researchStatus], ['最後驗證', dateLabel(stock.lastVerified)], ['信心（舊快照）', stock.confidence], ['Base 模型情境價', fmt(stock.target)], ['情境價差', percent(stock.gap)], ['產業', stock.industry || '未分類'], ['ETF（成分日期未提供）', stock.etfs.join('、') || '未列入'], ['營收成長（舊快照）', number(stock.revenueGrowth) === null ? '未提供' : percent(stock.revenueGrowth * 100)] ].forEach(([label, value]) => grid.append(detail(label, value)));
    const sections = make('div');
    sections.append(make('h3', '', '研究主題'), make('p', '', stock.researchTheme || '未分類'), make('p', 'notice', `資料快照 ${dateLabel(state.researchDate)}。此處未重新讀取或驗證報告，研究狀態與基本資料不代表最新結論。`), make('h3', '', '先讀風險，再看價差'), make('p', '', 'Base 價格僅為舊研究模型情境，不是預測或買賣建議。跨期行情與目標價不可直接當作安全邊際，請回到原報告確認假設、驗證日期及失效條件。'));
    const href = reportURL(stock.researchFile);
    if (href) { const link = make('a', 'report-link', '閱讀原始研究報告 ↗'); link.href = href; link.target = '_blank'; link.rel = 'noopener noreferrer'; sections.append(link); }
    else sections.append(make('p', 'notice', '未提供可開啟的原報告連結。'));
    root.append(head);
    if (stock.currentPrice !== null && stock.target !== null) {
      const comparison = make('div', 'profile-comparison');
      comparison.append(make('h3', '', '現價與 Base 情境對照'), make('p', 'chart-caption', '共同零起點，單位新臺幣／股。這是價格對照，不是歷史走勢。'));
      const max = Math.max(stock.currentPrice, stock.target);
      [['現價', stock.currentPrice, 'current'], ['Base 情境', stock.target, 'target']].forEach(([label, value, type]) => {
        const row = make('div', 'comparison-row'); row.append(make('span', '', label), make('strong', '', fmt(value)));
        const track = make('div', 'comparison-track'), bar = make('div', `comparison-bar ${type}`);
        bar.style.width = `${value / max * 100}%`; track.append(bar); row.append(track); comparison.append(row);
      });
      root.append(comparison);
    }
    root.append(grid, sections);
    $('#modal').hidden = false; $('.shell').inert = true; $('.topbar').inert = true; document.body.style.overflow = 'hidden'; $('.drawer-close').focus();
  }
  function closeDrawer() {
    $('#modal').hidden = true; $('.shell').inert = false; $('.topbar').inert = false; document.body.style.overflow = '';
    if (state.lastFocus?.isConnected) state.lastFocus.focus(); else $('#search').focus();
  }

  async function getJSON(url) {
    const response = await fetch(url, { cache: 'no-store', signal: AbortSignal.timeout(15000) });
    if (!response.ok) throw new Error(`${url} HTTP ${response.status}`);
    return response.json();
  }
  async function load() {
    const generation = ++state.generation;
    $('#reload').disabled = true; $('#list').setAttribute('aria-busy', 'true');
    $('#visuals').hidden = true;
    $('#list').replaceChildren(make('div', 'empty', '正在讀取來源快照…'));
    try {
      const [dataResult, liveResult, etfResult] = await Promise.allSettled([getJSON('./data.json'), getJSON('./data/live.json'), getJSON('./data/etf.json')]);
      if (generation !== state.generation) return;
      if (dataResult.status !== 'fulfilled') throw dataResult.reason;
      const data = dataResult.value;
      if (!Array.isArray(data.stocks) || !data.stocks.every(s => s && typeof s === 'object' && /^\d{4,6}[A-Z]?$/.test(String(s.code)))) throw new Error('data.json 個股格式不符');
      const codes = data.stocks.map(s => String(s.code));
      if (new Set(codes).size !== codes.length) throw new Error('data.json 有重複代碼');
      state.live = liveResult.status === 'fulfilled' && liveResult.value?.prices && typeof liveResult.value.prices === 'object' ? liveResult.value : null;
      state.etfMap = etfResult.status === 'fulfilled' && etfResult.value?.etfs && typeof etfResult.value.etfs === 'object' ? etfResult.value.etfs : {};
      state.warnings = [];
      if (!state.live) state.warnings.push('行情檔不可用，目前只顯示 data.json 舊快照。');
      if (!Object.keys(state.etfMap).length) state.warnings.push('ETF 清單不可用，ETF 篩選暫停。');
      $('#etf').disabled = !Object.keys(state.etfMap).length;
      state.dataDate = data.date; state.researchDate = data.research_summary?.generated;
      state.stocks = data.stocks.map(s => normalize(s, data, state.live));
      populateFilters(); renderStats(); renderQuality(); render(); $('#visuals').hidden = false;
    } catch (error) {
      state.stocks = []; $('#stats').replaceChildren(); $('#quality-list').replaceChildren();
      text('#result-count', '未載入'); text('#data-status', '載入失敗'); text('#data-updated', '資料未確認');
      const box = make('div', 'error', `資料載入失敗：${error.message || '未知錯誤'}。`);
      const retry = make('button', 'button button-quiet', '重新載入'); retry.type = 'button'; retry.addEventListener('click', load); box.append(retry); $('#list').replaceChildren(box);
    } finally { if (generation === state.generation) { $('#reload').disabled = false; $('#list').removeAttribute('aria-busy'); } }
  }

  $('#search').addEventListener('input', render);
  ['#industry', '#research-status', '#etf', '#sort'].forEach(selector => $(selector).addEventListener('change', render));
  $('#reset').addEventListener('click', () => { state.range = ''; ['#search', '#industry', '#research-status', '#etf'].forEach(selector => { $(selector).value = ''; }); render(); $('#search').focus(); });
  $('#heatmap-metric').addEventListener('change', event => { state.metric = event.target.value; render(); });
  $('#heatmap-expand').addEventListener('click', () => { state.expanded = !state.expanded; render(); $('#heatmap-expand').focus(); });
  window.matchMedia('(max-width:700px)').addEventListener('change', render);
  document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => {
    state.view = button.dataset.view;
    document.querySelectorAll('[data-view]').forEach(el => { el.classList.toggle('is-active', el === button); el.setAttribute('aria-pressed', String(el === button)); }); render();
  }));
  document.querySelectorAll('[data-period]').forEach(button => button.addEventListener('click', () => {
    state.period = button.dataset.period;
    document.querySelectorAll('[data-period]').forEach(el => { el.classList.toggle('is-active', el === button); el.setAttribute('aria-pressed', String(el === button)); });
    $('#sort option[value="pct"]').textContent = state.period === 'day' ? '日漲跌 ↓' : '期間漲跌（未提供）'; render();
  }));
  document.querySelectorAll('[data-close-modal]').forEach(el => el.addEventListener('click', closeDrawer));
  document.addEventListener('keydown', event => {
    if ($('#modal').hidden) return;
    if (event.key === 'Escape') { event.preventDefault(); closeDrawer(); }
    if (event.key === 'Tab') {
      const focusable = [...$('#modal').querySelectorAll('button, a[href]')];
      const first = focusable[0], last = focusable.at(-1);
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  $('#reload').addEventListener('click', load);
  load();
})();
