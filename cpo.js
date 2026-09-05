const REQUIRED = ['lid','asic','engine','fiber','els','substrate','foundry','assembly'];
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
function iso(x,y,z){ return [420 + (x-z) * Math.sqrt(3)/2, 30 + (x+z)*0.5 - y]; }
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
function isoLabel(g,x,y,z,t,dy=0){
  const [sx,sy]=iso(x,y,z);
  const n=svgEl('text');
  n.setAttribute('x',sx.toFixed(1)); n.setAttribute('y',(sy+dy).toFixed(1));
  n.setAttribute('class','part-label'); n.textContent=t; g.append(n);
}
function ribbon(g,a,b,c,d){
  const A=iso(...a), B=iso(...b), C=iso(...c), D=iso(...d);
  const p=svgEl('path');
  p.setAttribute('d',`M${A[0].toFixed(1)} ${A[1].toFixed(1)}C${B[0].toFixed(1)} ${B[1].toFixed(1)},${C[0].toFixed(1)} ${C[1].toFixed(1)},${D[0].toFixed(1)} ${D[1].toFixed(1)}`);
  p.setAttribute('class','fiber-ribbon'); g.append(p);
}
function drawBackground(){
  const bg=$('bg-layer'); bg.replaceChildren();
  const [cx,cy]=iso(330,0,170);
  const floor=svgEl('ellipse');
  Object.entries({cx, cy:cy+26, rx:200, ry:15, class:'shadow-plate'}).forEach(([k,v])=>floor.setAttribute(k,v));
  bg.append(floor);
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
function drawParts(){
  drawBackground();
  const layer=$('parts-layer'), calls=$('callouts');
  layer.replaceChildren(); calls.replaceChildren();
  const SX=210, SZ=50, SW=240, SD=240, SH=8;
  const AX=285, AZ=125, AW=90, AD=90, AH=16, AY=SH;
  const engines=[
    {x:268,y:SH,z:256,w:36,h:10,d:18,side:'n'},
    {x:356,y:SH,z:256,w:36,h:10,d:18,side:'n'},
    {x:226,y:SH,z:138,w:18,h:10,d:36,side:'w'},
    {x:226,y:SH,z:196,w:18,h:10,d:36,side:'w'},
    {x:416,y:SH,z:138,w:18,h:10,d:36,side:'e'},
    {x:416,y:SH,z:196,w:18,h:10,d:36,side:'e'},
    {x:268,y:SH,z:66,w:36,h:10,d:18,side:'s'},
    {x:356,y:SH,z:66,w:36,h:10,d:18,side:'s'}
  ];
  const substrate=partGroup('substrate');
  addBox(substrate, SX,0,SZ, SW,SH,SD, 'pcb-top','pcb-front','pcb-side');
  addBox(substrate, AX-2,7.2,AZ-2, AW+4,1.2,AD+4, 'gold-face','gold-face','gold-face');
  engines.forEach(e=>{
    const a=iso(AX+AW/2, 8.3, AZ+AD/2), b=iso(e.x+e.w/2, 8.3, e.z+e.d/2);
    const p=svgEl('path'); p.setAttribute('d',`M${a[0].toFixed(1)} ${a[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}`);
    p.setAttribute('class','trace'); substrate.append(p);
  });
  isoLabel(substrate, SX+18, 2, SZ+10, '共基板');
  const els=partGroup('els');
  addBox(els, 28,0,110, 86,22,58, 'els-top','els-front','els-side');
  isoLabel(els, 40, 24, 138, '外置 ELS');
  ribbon(els, [114,14,140], [150,16,140], [200,12,145], [226,14,156]);
  const engine=partGroup('engine');
  engines.forEach(e=>addBox(engine, e.x,e.y,e.z,e.w,e.h,e.d, 'engine-top','engine-front','engine-side'));
  isoLabel(engine, 360, 22, 270, '光引擎');
  const asic=partGroup('asic');
  addBox(asic, AX,AY,AZ, AW,AH,AD, 'asic-top','asic-front','asic-side');
  isoLabel(asic, AX+14, AY+AH+2, AZ+AD/2, 'Switch ASIC');
  const fiber=partGroup('fiber');
  engines.forEach(e=>{
    const fa=e.side==='s'?{x:e.x+8,y:e.y+2,z:e.z-10,w:20,h:6,d:10}
      :e.side==='n'?{x:e.x+8,y:e.y+2,z:e.z+e.d,w:20,h:6,d:10}
      :e.side==='w'?{x:e.x-10,y:e.y+2,z:e.z+8,w:10,h:6,d:20}
      :{x:e.x+e.w,y:e.y+2,z:e.z+8,w:10,h:6,d:20};
    addBox(fiber, fa.x,fa.y,fa.z,fa.w,fa.h,fa.d, 'can-top','can-front','can-side');
    const mx=fa.x+fa.w/2, my=fa.y+fa.h, mz=fa.z+fa.d/2;
    if(e.side==='s') ribbon(fiber,[mx,my,fa.z],[mx,my-6,fa.z-24],[mx-20,4,fa.z-48],[mx-70,18,fa.z-70]);
    else if(e.side==='n') ribbon(fiber,[mx,my,fa.z+fa.d],[mx+10,my+8,fa.z+fa.d+24],[mx+40,20,fa.z+fa.d+50],[mx+90,28,fa.z+fa.d+70]);
    else if(e.side==='w') ribbon(fiber,[fa.x,my,mz],[fa.x-24,my-4,mz-10],[fa.x-50,8,mz-20],[fa.x-80,16,mz-40]);
    else ribbon(fiber,[fa.x+fa.w,my,mz],[fa.x+fa.w+28,my+4,mz+8],[fa.x+fa.w+60,10,mz+16],[fa.x+fa.w+95,22,mz+28]);
  });
  isoLabel(fiber, 430, 8, 40, 'FA／光纖');
  const foundry=partGroup('foundry');
  foundry.append(poly(boxFaces(548,-4,78,118,36,88).top, 'inset-frame'));
  addBox(foundry, 562,0,92, 88,7,64, 'chip-top','chip-front','metal-side');
  addBox(foundry, 576,7,104, 58,11,40, 'asic-top','asic-front','asic-side');
  isoLabel(foundry, 554, 24, 88, '製程放大');
  isoLabel(foundry, 580, 4, 100, 'PIC', 20);
  isoLabel(foundry, 584, 20, 118, 'EIC', -10);
  const lid=partGroup('lid');
  addBox(lid, 236,161,150, 150,5,140, 'lid-ghost','lid-front','lid-side');
  isoLabel(lid, 250, 169, 180, '懸浮散熱蓋');
  const assembly=partGroup('assembly');
  assembly.append(
    poly([iso(198,34,38), iso(458,34,38), iso(458,34,298), iso(198,34,298)], 'assembly-box'),
    poly([iso(198,-5,38), iso(458,-5,38), iso(458,-5,298), iso(198,-5,298)], 'assembly-box')
  );
  [substrate, els, engine, asic, fiber, foundry, lid, assembly].forEach(g=>layer.append(g));
  const labels={
    lid:[iso(236,169,150)[0], iso(236,169,150)[1]-16],
    asic:[iso(AX+AW/2,AY+AH,AZ+AD/2)[0]+6, iso(AX+AW/2,AY+AH,AZ+AD/2)[1]-34],
    engine:[iso(434,22,214)[0]+22, iso(434,22,214)[1]-26],
    fiber:[iso(374,12,56)[0]+8, iso(374,12,56)[1]+34],
    els:[iso(28,24,110)[0]-4, iso(28,24,110)[1]-20],
    substrate:[iso(210,0,50)[0]-6, iso(210,0,50)[1]+30],
    foundry:[iso(640,28,140)[0]+18, iso(640,28,140)[1]-18],
    assembly:[iso(450,0,50)[0]+72, iso(450,0,50)[1]+34]
  };
  const anchors={
    lid:iso(310,163,220), asic:iso(AX+AW/2,AY+AH,AZ+AD/2), engine:iso(434,18,214),
    fiber:iso(374,12,56), els:iso(70,22,140), substrate:iso(250,0,60),
    foundry:iso(620,18,120), assembly:iso(440,8,70)
  };
  REQUIRED.forEach((id,i)=>{
    const g=svgEl('g'); g.classList.add('callout');
    const [x,y]=labels[id], [ax,ay]=anchors[id];
    const line=svgEl('path'); line.setAttribute('d',`M${ax.toFixed(1)} ${ay.toFixed(1)}L${x.toFixed(1)} ${y.toFixed(1)}`); line.setAttribute('class','callout-line');
    const c=svgEl('circle');
    Object.entries({cx:x,cy:y,r:13,tabindex:0,role:'button','aria-label':component(id).title,class:'callout-num'}).forEach(([k,v])=>c.setAttribute(k,v));
    c.dataset.id=id;
    c.addEventListener('click',()=>selectPart(id));
    c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectPart(id)}});
    const t=svgEl('text'); t.setAttribute('x',x); t.setAttribute('y',y); t.setAttribute('class','callout-num-text'); t.textContent=i+1;
    g.append(line,c,t); calls.append(g);
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
      stage.append(cos); if(st.source_ids?.length) stage.append(sourceLinks(st.source_ids));
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
  return m&&m.status==='historical_estimate'&&typeof m.value==='number'&&Number.isFinite(m.value)&&m.value>=0&&m.value<=100&&m.period&&m.denominator&&m.geography&&m.source_ids?.length;
}
function renderSuppliers(){
  const box=$('supplier-grid'); box.replaceChildren(); if(!state.data)return; const componentId=state.component;
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
    const share=el('div','share'), m=s.market_share;
    const applies=Array.isArray(m?.component_ids)&&m.component_ids.length>0&&(!componentId||m.component_ids.includes(componentId));
    const isHistorical=applies&&historicalEstimate(s);
    if(applies&&shareVerified(s)&&!isHistorical){
      const line=el('div','share-label'); line.append(el('span','',`市占 · ${m.geography}`), el('strong','',`${m.value}%`)); share.append(line);
      const bar=el('div','bar'), i=document.createElement('i'); i.style.width=`${m.value}%`; bar.append(i); share.append(bar);
      share.append(el('div','supplier-meta', `分母：${m.denominator} · ${m.period}`));
    } else {
      share.append(el('span','unconfirmed', isHistorical
        ? `歷史公司自估：約 ${m.value}% · ${m.period} · ${m.geography} · ${m.denominator}。${m.note||''}`
        : '市占未確認（不以缺失資料推算）'));
    }
    if(applies&&m?.note&&!isHistorical){ share.append(el('p','share-note', m.note)); }
    if(applies&&Array.isArray(m?.source_ids)&&m.source_ids.length){
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
  setState('正在載入CPO 資料…'); $('retry').hidden=true;
  $('supplier-grid').replaceChildren(); $('component-buttons').replaceChildren(); $('sources-content').replaceChildren();
  $('supplier-count').textContent='';
  try {
    const r=await fetch('./data/cpo.json',{cache:'no-store'});
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const d=await r.json();
    if(!validData(d)) throw new Error('資料格式不完整');
    state.data=d; render();
  } catch(e) {
    $('module-workspace').hidden=true;
    setState(`無法載入資料：${e.message}。請確認 data/cpo.json。`, true);
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
