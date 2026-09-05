const REQUIRED = ['housing','connector','optics','laser','receiver','dsp','substrate','assembly'];
const state = { data:null, selected:'assembly', country:'', component:'assembly', tracked:false };
const $ = id => document.getElementById(id);
const escDate = value => value == null ? '—' : String(value);
function safeUrl(value){
  if (value == null || value === '') return '';
  try {
    const raw = String(value).trim();
    const u = new URL(raw, document.baseURI);
    if (!['http:','https:'].includes(u.protocol)) return '';
    return u.href;
  } catch { return ''; }
}
function text(el,value){ el.textContent = value == null ? '' : String(value); return el; }
function el(tag, cls, value){ const n=document.createElement(tag); if(cls)n.className=cls; if(value!==undefined)text(n,value); return n; }
function validData(d){ return d && Array.isArray(d.components) && Array.isArray(d.suppliers) && Array.isArray(d.sources) && REQUIRED.every(id=>d.components.some(c=>c.id===id)); }
function setState(message,error=false){ const n=$('load-state'); n.hidden=message==='資料已載入'; n.className='state'+(error?' error':''); text(n,message); }
function component(id){ return state.data?.components.find(c=>c.id===id); }
function supplier(id){ return state.data?.suppliers.find(s=>s.id===id); }
function sourceAnchor(id){ return `source-${encodeURIComponent(String(id))}`; }
function sourceLink(id){
  const source = state.data?.sources.find(s=>String(s.id)===String(id));
  const a=el('a','source-link',source?.short_title||source?.title||String(id));
  a.href=`#${sourceAnchor(id)}`;
  a.addEventListener('click',()=>{const details=document.querySelector('details.sources');if(details)details.open=true});
  a.title=source?.title||String(id);
  a.textContent=source?.short_title||source?.title||String(id);
  return a;
}
function sourceLinks(ids){
  const box=el('span','source-links');
  (Array.isArray(ids)?ids:[]).forEach((id,i)=>{if(i)box.append(document.createTextNode('、'));box.append(sourceLink(id))});
  return box;
}
function renderOptions(){
  const country=$('country-filter'), filter=$('component-filter');
  country.replaceChildren(el('option','', '全球')); country.firstElementChild.value='';
  filter.replaceChildren(el('option','', '全部零件')); filter.firstElementChild.value='';
  [...new Set(state.data.suppliers.map(s=>s.country).filter(Boolean))].sort((a,b)=>a.localeCompare(b)).forEach(c=>{const o=el('option','',c);o.value=c;country.append(o)});
  state.data.components.filter(c=>REQUIRED.includes(c.id)).forEach(c=>{const o=el('option','',c.title||c.id);o.value=c.id;filter.append(o)});
  country.value=state.country; filter.value=state.component;
}
function svgEl(tag){ return document.createElementNS('http://www.w3.org/2000/svg',tag); }
function iso(x,y,z){ return [70 + x + z * 0.52, 292 - y * 1.25 - z * 0.28]; }
function poly(pts, cls){
  const p=svgEl('path');
  p.setAttribute('d','M'+pts.map(([x,y])=>`${x.toFixed(1)} ${y.toFixed(1)}`).join('L')+'Z');
  p.setAttribute('class', cls);
  return p;
}
function boxFaces(x,y,z,w,h,d){
  const A=iso(x,y,z), B=iso(x+w,y,z), C=iso(x+w,y,z+d), D=iso(x,y,z+d);
  const E=iso(x,y+h,z), F=iso(x+w,y+h,z), G=iso(x+w,y+h,z+d), H=iso(x,y+h,z+d);
  return {top:[E,F,G,H], front:[A,B,F,E], side:[B,C,G,F], left:[A,D,H,E]};
}
function addBox(g, x,y,z,w,h,d, top, front, side){
  const f=boxFaces(x,y,z,w,h,d);
  g.append(poly(f.side, side), poly(f.front, front), poly(f.top, top));
  return f;
}
function partGroup(id){
  const g=svgEl('g');
  g.id=id; g.classList.add('part'); g.dataset.id=id;
  g.setAttribute('tabindex','0'); g.setAttribute('role','button');
  g.setAttribute('aria-label', component(id)?.title||id);
  g.setAttribute('aria-pressed', String(state.selected===id));
  g.addEventListener('click',()=>selectPart(id));
  g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectPart(id)}});
  return g;
}
function drawBackground(){
  const bg=$('bg-layer'); bg.replaceChildren();
  const floor=svgEl('ellipse');
  floor.setAttribute('cx','600'); floor.setAttribute('cy','328');
  floor.setAttribute('rx','430'); floor.setAttribute('ry','18');
  floor.setAttribute('class','shadow-plate'); bg.append(floor);
  const guide=svgEl('g'); guide.setAttribute('class','guide');
  const line=svgEl('path'); line.setAttribute('d','M50 338H1120'); guide.append(line); bg.append(guide);
  const left=svgEl('text'); left.setAttribute('x','70'); left.setAttribute('y','354'); left.setAttribute('class','end-label'); left.textContent='OPTICAL'; bg.append(left);
  const right=svgEl('text'); right.setAttribute('x','960'); right.setAttribute('y','354'); right.setAttribute('class','end-label'); right.textContent='ELECTRICAL'; bg.append(right);
}
function drawParts(){
  drawBackground();
  const layer=$('parts-layer'), calls=$('callouts');
  layer.replaceChildren(); calls.replaceChildren();
  const housing=partGroup('housing');
  addBox(housing, 48,0,6, 760,10, 92, 'metal-top','metal-front','metal-side');
  addBox(housing, 48,10,90, 760,28, 8, 'metal-top','metal-front','metal-side');
  addBox(housing, 48,10,6, 14,22, 84, 'metal-top','metal-front','metal-side');
  addBox(housing, 790,10,6, 18,16, 84, 'metal-top','metal-front','metal-side');
  [[70,4,18],[70,4,78],[780,4,18],[780,4,78]].forEach(([x,y,z])=>{
    const hole=svgEl('ellipse'); const p=iso(x,y,z);
    hole.setAttribute('cx',p[0]); hole.setAttribute('cy',p[1]); hole.setAttribute('rx','5'); hole.setAttribute('ry','3.2');
    hole.setAttribute('class','hole'); housing.append(hole);
  });
  const substrate=partGroup('substrate');
  addBox(substrate, 64,7,14, 722,3, 72, 'pcb-top','pcb-front','pcb-side');
  for(let i=0;i<14;i++){
    addBox(substrate, 786,7.4, 18+i*4.6, 46,1.1, 3.2, 'gold-face','gold-face','gold-face');
  }
  const traces=svgEl('g'); traces.setAttribute('class','trace'); traces.style.pointerEvents='none';
  [[180,10,50, 420,10,50],[180,10,70, 420,10,70],[520,10,40, 780,10,28],[520,10,78, 780,10,78]].forEach(([x1,y1,z1,x2,y2,z2])=>{
    const a=iso(x1,y1,z1), b=iso(x2,y2,z2);
    const p=svgEl('path'); p.setAttribute('d',`M${a[0]} ${a[1]}L${b[0]} ${b[1]}`); p.setAttribute('class','trace'); traces.append(p);
  });
  substrate.append(traces);
  const optics=partGroup('optics');
  addBox(optics, 118,10,28, 36,14, 44, 'can-top','can-front','can-side');
  const lens1=svgEl('ellipse'); const lp=iso(118,17,50);
  lens1.setAttribute('cx',lp[0]); lens1.setAttribute('cy',lp[1]); lens1.setAttribute('rx','10'); lens1.setAttribute('ry','16');
  lens1.setAttribute('class','lens'); optics.append(lens1);
  const laser=partGroup('laser');
  addBox(laser, 162,10,18, 100,22, 26, 'can-top','can-front','can-side');
  addBox(laser, 256,14,24, 18,12, 14, 'gold-face','gold-face','gold-face');
  const receiver=partGroup('receiver');
  addBox(receiver, 162,10,54, 100,22, 26, 'can-top','can-front','can-side');
  addBox(receiver, 256,14,60, 18,12, 14, 'gold-face','gold-face','gold-face');
  const dsp=partGroup('dsp');
  addBox(dsp, 430,10,30, 118,6, 40, 'chip-top','chip-front','metal-side');
  for(let i=0;i<11;i++){
    addBox(dsp, 436+i*10, 9.2, 28, 4, 1.4, 2, 'pin','pin','pin');
    addBox(dsp, 436+i*10, 9.2, 70, 4, 1.4, 2, 'pin','pin','pin');
  }
  const mark=svgEl('text'); const mp=iso(458,15,50);
  mark.setAttribute('x',mp[0]); mark.setAttribute('y',mp[1]); mark.setAttribute('class','part-label'); mark.setAttribute('font-size','9'); mark.textContent='DSP'; dsp.append(mark);
  const connector=partGroup('connector');
  const tab=svgEl('path');
  const t1=iso(6,22,36), t2=iso(6,22,62), t3=iso(-18,34,62), t4=iso(-18,34,36);
  tab.setAttribute('d',`M${t1[0]} ${t1[1]}L${t2[0]} ${t2[1]}L${t3[0]} ${t3[1]}L${t4[0]} ${t4[1]}Z`);
  tab.setAttribute('class','pull'); connector.append(tab);
  addBox(connector, 28,10,24, 78,16, 20, 'metal-top','metal-front','metal-side');
  addBox(connector, 28,10,58, 78,16, 20, 'metal-top','metal-front','metal-side');
  [[28,18,34],[28,18,68]].forEach(([x,y,z])=>{
    const hole=svgEl('ellipse'); const p=iso(x,y,z);
    hole.setAttribute('cx',p[0]); hole.setAttribute('cy',p[1]); hole.setAttribute('rx','7'); hole.setAttribute('ry','6');
    hole.setAttribute('class','ferrule'); connector.append(hole);
  });
  const assembly=partGroup('assembly');
  const outline=boxFaces(18,-6,-4, 830,40, 112);
  const dash=poly([...outline.top.slice(0,2), ...outline.side.slice(1,3), outline.left[1], outline.left[0]], 'assembly-box');
  dash.setAttribute('d', `M${iso(18,34,-4).join(' ')}L${iso(848,34,-4).join(' ')}L${iso(848,34,108).join(' ')}L${iso(18,34,108).join(' ')}Z`);
  assembly.append(dash);
  const bottom=svgEl('path');
  bottom.setAttribute('d', `M${iso(18,-6,-4).join(' ')}L${iso(848,-6,-4).join(' ')}L${iso(848,-6,108).join(' ')}L${iso(18,-6,108).join(' ')}Z`);
  bottom.setAttribute('class','assembly-box'); assembly.append(bottom);
  [housing, substrate, optics, laser, receiver, dsp, connector, assembly].forEach(g=>layer.append(g));
  const labels={
    housing:[iso(420,40,96)[0], iso(420,40,96)[1]-36, '外殼'],
    connector:[iso(-10,38,48)[0], iso(-10,38,48)[1]-18, '光口'],
    optics:[iso(130,28,50)[0], iso(130,28,50)[1]-42, '耦光'],
    laser:[iso(200,30,20)[0], iso(200,30,20)[1]-38, '雷射'],
    receiver:[iso(210,8,80)[0]+40, iso(210,8,80)[1]+48, '接收'],
    dsp:[iso(490,18,50)[0], iso(490,18,50)[1]-46, 'DSP'],
    substrate:[iso(360,6,14)[0], iso(360,6,14)[1]+52, 'PCB'],
    assembly:[iso(860,20,50)[0]+20, iso(860,20,50)[1]-10, '組裝']
  };
  const anchors={
    housing: iso(420,28,96),
    connector: iso(20,18,34),
    optics: iso(136,24,50),
    laser: iso(208,26,22),
    receiver: iso(208,10,78),
    dsp: iso(490,14,50),
    substrate: iso(400,8,18),
    assembly: iso(848,20,50)
  };
  REQUIRED.forEach((id,index)=>{
    const n=svgEl('g'); n.classList.add('callout');
    const [cx,cy,caption]=labels[id];
    const [ax,ay]=anchors[id];
    const line=svgEl('path'); line.setAttribute('d',`M${ax} ${ay}L${cx} ${cy}`); line.setAttribute('class','callout-line');
    const circle=svgEl('circle'); circle.setAttribute('cx',cx); circle.setAttribute('cy',cy); circle.setAttribute('r','13');
    circle.setAttribute('class','callout-num'); circle.dataset.id=id; circle.setAttribute('tabindex','0');
    circle.setAttribute('role','button'); circle.setAttribute('aria-label',`選擇${component(id)?.title||id}`);
    circle.setAttribute('aria-pressed', String(state.selected===id));
    const nt=svgEl('text'); nt.setAttribute('x',cx); nt.setAttribute('y',cy); nt.setAttribute('class','callout-num-text'); nt.textContent=index+1;
    const cap=svgEl('text'); cap.setAttribute('x', cx+16); cap.setAttribute('y', cy+4); cap.setAttribute('class','callout-caption'); cap.textContent=caption;
    circle.addEventListener('click',e=>{e.stopPropagation();selectPart(id)});
    circle.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectPart(id)}});
    n.append(line, circle, nt, cap); calls.append(n);
  });
}
function statusLabel(status){
  return {product_role:'產品角色確認', adjacent:'相鄰／延伸', gap:'本輪未確認'}[status] || status || '未標示';
}
function renderChain(id){
  const box=$('chain-content'); if(!box) return; box.replaceChildren();
  const c=component(id);
  box.append(el('div','detail-kicker', c?.title || id));
  box.append(el('h2','', `${c?.title||id}產業鏈`));
  const chains=Array.isArray(c?.chains)?c.chains:[];
  if(!chains.length){
    box.append(el('p','','這個零件還沒有分層產業鏈資料。'));
    return;
  }
  chains.forEach(ch=>{
    const branch=el('div','branch');
    branch.append(el('h3','', ch.title||'產業鏈'));
    if(ch.note) branch.append(el('p','branch-note', ch.note));
    const row=el('div','stages');
    (ch.stages||[]).forEach((st,i)=>{
      if(i) row.append(el('div','stage-arrow','→'));
      const stage=el('article','stage');
      stage.append(el('strong','', st.title||st.id));
      if(st.description) stage.append(el('p','', st.description));
      const cos=el('div','stage-cos');
      const firms=(st.supplier_ids||[]).map(supplier).filter(Boolean);
      const tw=firms.filter(s=>s.country==='台灣');
      const glob=firms.filter(s=>s.country!=='台灣');
      if(tw.length) cos.append(el('div','', '台股：'+tw.map(s=>`${s.name}${s.ticker?` ${s.ticker}`:''}`).join('、')));
      if(glob.length) cos.append(el('div','', '全球：'+glob.map(s=>s.name).join('、')));
      if(!firms.length) cos.append(el('div','', '公司未確認'));
      stage.append(cos);
      stage.append(el('span',`badge ${st.status||''}`, statusLabel(st.status)));
      row.append(stage);
    });
    branch.append(row);
    box.append(branch);
  });
}
function selectPart(id){
  if(!component(id)) return;
  state.selected=id; state.component=id;
  $('component-filter').value=id;
  document.querySelectorAll('.part').forEach(n=>{
    const on=n.id===id;
    n.classList.toggle('selected', on);
    n.classList.toggle('dim', id!=='assembly' && !on);
    n.setAttribute('aria-pressed', String(on));
  });
  document.querySelectorAll('.callout-num').forEach(n=>n.setAttribute('aria-pressed', String(n.dataset.id===id)));
  document.querySelectorAll('.component-button').forEach(n=>{
    const on=n.dataset.id===id; n.classList.toggle('active',on); n.setAttribute('aria-pressed', String(on));
  });
  renderSuppliers();
  renderChain(id);
  const c=component(id), box=$('detail-content'); box.replaceChildren();
  box.append(el('div','detail-kicker', String(c.signal||'訊號路徑')));
  box.append(el('h2','', c.title||id));
  box.append(el('p','', c.subtitle||c.role||''));
  const role=el('p',''); role.append(el('strong','角色：','角色：'), document.createTextNode(` ${c.role||'未提供'}`)); box.append(role);
  const chain=el('div','chain'); (c.chain||[]).forEach(v=>chain.append(el('span','',v))); box.append(chain);
  box.append(el('p','', c.architecture_note||'資料未提供架構備註。'));
  if(Array.isArray(c.source_ids)&&c.source_ids.length){
    const p=el('p','citation'); p.append(el('strong','引用來源：','引用來源：'), document.createTextNode(' '), sourceLinks(c.source_ids)); box.append(p);
  }
}
function renderButtons(){
  const box=$('component-buttons'); box.replaceChildren();
  state.data.components.filter(c=>REQUIRED.includes(c.id)).forEach(c=>{
    const b=el('button','component-button'); b.type='button'; b.dataset.id=c.id;
    b.setAttribute('aria-pressed', String(state.selected===c.id));
    b.append(el('strong','',c.title||c.id), el('small','',c.signal||'零件'));
    b.addEventListener('click',()=>selectPart(c.id)); box.append(b);
  });
}
function shareVerified(s){
  const m=s.market_share;
  return m&&m.status==='verified'&&typeof m.value==='number'&&m.value>=0&&m.value<=100&&m.denominator&&m.geography&&m.period&&Array.isArray(m.source_ids)&&m.source_ids.length;
}
function historicalEstimate(s){
  const m=s.market_share;
  return m&&m.status==='historical_estimate'&&typeof m.value==='number'&&m.period&&m.denominator&&m.source_ids?.length;
}
function renderSuppliers(){
  const box=$('supplier-grid'); box.replaceChildren(); const componentId=state.component;
  const list=state.data.suppliers.filter(s=>(!state.country||s.country===state.country)&&(!componentId||(s.component_ids||[]).includes(componentId))&&(!state.tracked||s.research_status==='tracked'));
  text($('supplier-count'), `${list.length} 家符合篩選`);
  if(!list.length){ box.append(el('div','empty','沒有符合條件的供應商。')); return; }
  list.forEach(s=>{
    const card=el('article','supplier-card');
    card.append(el('h3','', s.name||'未命名供應商'));
    const listed=s.ticker?(s.exchange?`${s.exchange}：${s.ticker}`:`${s.ticker}（未標示交易所）`):'私人／未上市';
    card.append(el('div','supplier-meta', `${s.country||'國家未提供'} · ${listed}`));
    const role=el('p','supplier-role'); role.append(el('strong','角色：','角色：'), document.createTextNode(` ${s.role||'未提供'}`)); card.append(role);
    const confidence=el('p','supplier-meta'); confidence.append(document.createTextNode(`證據狀態：${s.confidence||'未提供'}`)); card.append(confidence);
    const tags=el('div'); (s.component_ids||[]).map(id=>component(id)?.title||id).forEach(v=>tags.append(el('span','tag',v)));
    tags.append(el('span','tag', s.research_status==='tracked'?'已追蹤':'未追蹤')); card.append(tags);
    const share=el('div','share'), m=s.market_share, isHistorical=historicalEstimate(s);
    if(shareVerified(s)&&!isHistorical){
      const line=el('div','share-label'); line.append(el('span','',`市占 · ${m.geography}`), el('strong','',`${m.value}%`)); share.append(line);
      const bar=el('div','bar'), i=document.createElement('i'); i.style.width=`${m.value}%`; bar.append(i); share.append(bar);
      share.append(el('div','supplier-meta', `分母：${m.denominator} · ${m.period}`));
    } else {
      share.append(el('span','unconfirmed', isHistorical
        ? `歷史公司自估：約 ${m.value}% · ${m.period} · ${m.geography} · ${m.denominator}。${m.note||''}${componentId&&!(m.component_ids||[]).includes(componentId)?' 此為其他產品的歷史資料，本零件市占未確認。':''}`
        : '市占未確認（不以缺失資料推算）'));
    }
    if(m?.note&&!isHistorical){ share.append(el('p','share-note', m.note)); }
    if(Array.isArray(m?.source_ids)&&m.source_ids.length){
      const p=el('p','citation'); p.append(el('strong','市占來源：','市占來源：'), document.createTextNode(' '), sourceLinks(m.source_ids)); share.append(p);
    }
    card.append(share);
    if(Array.isArray(s.source_ids)&&s.source_ids.length){
      const p=el('p','citation'); p.append(el('strong','公司來源：','公司來源：'), document.createTextNode(' '), sourceLinks(s.source_ids)); card.append(p);
    }
    const url=s.research_url&&safeUrl(s.research_url);
    if(url){ const a=el('a','', s.research_status==='tracked'?'查看追蹤研究 ↗':'查看研究 ↗'); a.href=url; a.target='_blank'; a.rel='noopener noreferrer'; card.append(a); }
    box.append(card);
  });
}
function renderSources(){
  const box=$('sources-content'); box.replaceChildren();
  if(state.data.limitations?.length) box.append(el('p','muted', state.data.limitations.join(' ')));
  if(state.data.chain_notes?.length) box.append(el('p','muted', state.data.chain_notes.join(' ')));
  (state.data.sources||[]).forEach((s,i)=>{
    const row=el('div','source-row'); row.id=sourceAnchor(s.id??i+1);
    const heading=el('div','source-heading'); heading.append(el('strong','', `[${i+1}] ${s.id??'source-'+(i+1)} `));
    const url=safeUrl(s.url);
    if(url){ const a=el('a','', s.title||url); a.href=url; a.target='_blank'; a.rel='noopener noreferrer'; heading.append(a); }
    else heading.append(el('span','', s.title||'來源連結未提供'));
    row.append(heading);
    row.append(el('p','', `發布：${escDate(s.published)}　存取：${escDate(s.accessed)}${s.quote?`　「${s.quote}」`:''}`));
    box.append(row);
  });
}
function render(){
  renderOptions(); drawParts(); renderButtons(); selectPart(state.selected); renderSources();
  $('module-workspace').hidden=false; setState('資料已載入');
  $('data-status').textContent='已連線'; $('data-asof').textContent=`截至 ${escDate(state.data.as_of)}`;
}
async function load(){
  setState('正在載入光通模組資料…'); $('retry').hidden=true;
  $('supplier-grid').replaceChildren(); $('component-buttons').replaceChildren(); $('sources-content').replaceChildren();
  $('supplier-count').textContent='';
  try {
    const r=await fetch('./data/optical-module.json',{cache:'no-store'});
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const d=await r.json();
    if(!validData(d)) throw new Error('資料格式不完整');
    state.data=d; render();
  } catch(e) {
    $('module-workspace').hidden=true;
    setState(`無法載入資料：${e.message}。請確認 data/optical-module.json。`, true);
    $('data-status').textContent='載入失敗'; $('data-asof').textContent='來源未確認'; $('retry').hidden=false;
  }
}
$('country-filter').addEventListener('change',e=>{state.country=e.target.value;renderSuppliers()});
$('component-filter').addEventListener('change',e=>{
  if(e.target.value) selectPart(e.target.value);
  else { state.component=''; selectPart('assembly'); state.component=''; $('component-filter').value=''; renderSuppliers(); }
});
$('tracked-only').addEventListener('change',e=>{state.tracked=e.target.checked;renderSuppliers()});
$('retry').addEventListener('click', load);
$('theme-toggle').addEventListener('click',()=>{
  const root=document.documentElement;
  root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';
  try{localStorage.setItem('stocktw:theme', root.dataset.theme)}catch(e){}
});
load();
