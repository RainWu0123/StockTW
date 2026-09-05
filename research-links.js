/** 研究頁與互動頁共用的 deep link 規則；不含公司清單。 */
const CODE_OK = /^[A-Za-z0-9][A-Za-z0-9.-]{0,15}$/;

export function resolveComponentParam(search, allowed, fallback = 'assembly') {
  const list = Array.isArray(allowed) ? allowed : [];
  let id = '';
  try {
    const raw = String(search ?? '');
    const q = raw.startsWith('?') ? raw.slice(1) : raw;
    id = new URLSearchParams(q).get('component') || '';
  } catch {
    id = '';
  }
  return list.includes(id) ? id : fallback;
}

export function resolveCodeParam(search) {
  let code = '';
  try {
    const raw = String(search ?? '');
    const q = raw.startsWith('?') ? raw.slice(1) : raw;
    code = new URLSearchParams(q).get('code') || '';
  } catch {
    return '';
  }
  return CODE_OK.test(code) ? code : '';
}

export function tickerFromFilename(filename) {
  const base = String(filename || '').split('/').pop() || '';
  const stem = base.replace(/\.md$/i, '');
  const cut = stem.indexOf('_');
  return cut === -1 ? stem : stem.slice(0, cut);
}

export function fileForCode(code, files) {
  const wanted = String(code || '');
  if (!wanted) return '';
  const list = Array.isArray(files) ? files : [];
  const found = list.find((f) => {
    const name = String(f).split('/').pop();
    return name === wanted || name === `${wanted}.md` || tickerFromFilename(name) === wanted;
  });
  return found || '';
}

function safeMdName(raw) {
  let value = String(raw || '');
  try {
    value = decodeURIComponent(value);
  } catch {
    return '';
  }
  if (!value || value.includes('..') || value.includes('\\')) return '';
  const name = value.split('/').pop() || '';
  if (!name.toLowerCase().endsWith('.md') || name.includes('/') || name.startsWith('摘要_')) return '';
  return name;
}

export function parseResearchFilenames(html) {
  const names = [];
  for (const match of String(html || '').matchAll(/href="([^"]+\.md)"/gi)) {
    const name = safeMdName(match[1]);
    if (name) names.push(name);
  }
  return [...new Set(names)];
}

export function parseResearchFilenamesFromIndex(markdown) {
  const names = [];
  for (const match of String(markdown || '').matchAll(/research\/([^)\s\]`]+\.md)/g)) {
    const name = safeMdName(match[1]);
    if (name) names.push(name);
  }
  return [...new Set(names)];
}

export function parseResearchFilenamesFromUniverse(data) {
  const names = [];
  for (const stock of data?.stocks || []) {
    const name = safeMdName(stock.research_path);
    if (name) names.push(name);
  }
  return [...new Set(names)];
}

export function mergeResearchFiles(...lists) {
  const seen = new Set();
  const out = [];
  for (const list of lists) {
    for (const item of list || []) {
      const name = safeMdName(item);
      if (!name || seen.has(name)) continue;
      seen.add(name);
      out.push(name);
    }
  }
  return out;
}

export function localResearchHref(supplier, files) {
  const ticker = String(supplier?.ticker || '');
  if (!CODE_OK.test(ticker) || !fileForCode(ticker, files)) return '';
  return `research.html?code=${encodeURIComponent(ticker)}`;
}

export async function loadResearchFilenames(fetchImpl = fetch) {
  const chunks = [];
  try {
    const res = await fetchImpl('./INDEX.md', { cache: 'no-store' });
    if (res && res.ok) chunks.push(parseResearchFilenamesFromIndex(await res.text()));
  } catch { /* Pages 仍可靠後續來源 */ }
  try {
    const res = await fetchImpl('./meta/research_universe.json', { cache: 'no-store' });
    if (res && res.ok) chunks.push(parseResearchFilenamesFromUniverse(await res.json()));
  } catch { /* universe 缺失時只用 INDEX */ }
  return mergeResearchFiles(...chunks);
}

export function linksForTicker(ticker, datasets) {
  const code = String(ticker || '');
  if (!code) return [];
  const out = [];
  for (const ds of Array.isArray(datasets) ? datasets : []) {
    const matches = (ds.suppliers || []).filter((s) => String(s.ticker || '') === code);
    if (!matches.length) continue;
    const seen = new Set();
    const ids = [];
    for (const s of matches) {
      for (const id of s.component_ids || []) {
        if (!seen.has(id)) {
          seen.add(id);
          ids.push(id);
        }
      }
    }
    const titles = Object.fromEntries((ds.components || []).map((c) => [c.id, c.title || c.id]));
    const href = ds.href || '';
    out.push({
      page: ds.page,
      href,
      label: ds.label || ds.page,
      components: ids.map((id) => ({
        id,
        title: titles[id] || id,
        href: `${href}?component=${encodeURIComponent(id)}`,
      })),
    });
  }
  return out;
}
