#!/usr/bin/env python3
"""同步 dashboard 資料：即時價格、研究 frontmatter、目標價與研究品質狀態。"""
import json
import re
import datetime as dt
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
DATA = BASE / 'data.json'
LIVE = BASE / 'data' / 'live.json'
RESEARCH = BASE / 'research'
TODAY = dt.date.today()
STALE_DAYS = 30
FIELD_RE = re.compile(r'^(\w+):\s*["\']?(.+?)["\']?\s*$', re.M)
NUM_RE = re.compile(r'^[\d,.]+$')

def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return {}
    try:
        head = text.split('---', 2)[1]
    except IndexError:
        return {}
    fm = {}
    for key, val in FIELD_RE.findall(head):
        fm[key] = val.strip().strip('"\'')
    return fm

def parse_float(v):
    if v is None:
        return None
    s = str(v).strip().replace(',', '')
    if not NUM_RE.match(s):
        return None
    try:
        return float(s)
    except ValueError:
        return None

def parse_date(v):
    if not v:
        return None
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None

def maturity_status(maturity, verified):
    age = (TODAY - verified).days if verified else None
    if not verified:
        return '未驗證'
    if age is not None and age > STALE_DAYS:
        return '需重驗'
    if maturity is None:
        return '未分級'
    if maturity >= 90:
        return '深度'
    if maturity >= 80:
        return '可用'
    if maturity >= 60:
        return '草稿'
    return '淺層'

def target_status(target, dist):
    if not target:
        return '無目標'
    if dist is None:
        return '無報價'
    if dist >= 20:
        return '透支'
    if dist >= 0:
        return '已達標'
    if dist >= -10:
        return '接近'
    if dist <= -30:
        return '低估'
    return '未達標'

def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    live = json.loads(LIVE.read_text(encoding='utf-8')) if LIVE.exists() else {}
    prices = live.get('prices', {})
    research_map = {}
    for md in sorted(RESEARCH.glob('*_*.md')):
        name = md.name
        if name.startswith(('摘要_', '追蹤_')) or name.endswith('.html'):
            continue
        code = name.split('_', 1)[0]
        if not code.isdigit():
            continue
        fm = parse_frontmatter(md)
        target = parse_float(fm.get('target_base') or fm.get('target'))
        maturity = parse_float(fm.get('research_maturity'))
        verified = parse_date(fm.get('last_verified'))
        age = (TODAY - verified).days if verified else None
        research_map[code] = {
            'target': target,
            'researchTheme': fm.get('theme', ''),
            'lastVerified': fm.get('last_verified', ''),
            'sourcesAsOf': fm.get('sources_as_of', ''),
            'confidence': fm.get('confidence', ''),
            'researchMaturity': int(maturity) if maturity is not None else None,
            'researchAgeDays': age,
            'researchStatus': maturity_status(maturity, verified),
            'researchFile': f'research/{name}',
        }
    updated_prices = mapped_targets = mapped_research = 0
    for s in data.get('stocks', []):
        c = str(s.get('code', ''))
        p = prices.get(c)
        if p and p.get('price') is not None:
            s['price'] = p.get('price')
            s['pct'] = p.get('pct')
            s['vol'] = p.get('vol')
            updated_prices += 1
        r = research_map.get(c)
        if r:
            mapped_research += 1
            for k, v in r.items():
                if v not in (None, '') or k in ('researchMaturity', 'researchAgeDays'):
                    s[k] = v
            if r.get('target') is not None:
                s['target'] = r['target']
                mapped_targets += 1
                price = s.get('price')
                try:
                    s['targetDist'] = round((float(price) / float(r['target']) - 1) * 100, 1) if price else None
                except (TypeError, ValueError, ZeroDivisionError):
                    s['targetDist'] = None
            else:
                s.pop('target', None)
                s.pop('targetDist', None)
        else:
            s['researchStatus'] = s.get('researchStatus') or '無研究'
        s['targetStatus'] = target_status(s.get('target'), s.get('targetDist'))
    data['updated'] = dt.datetime.now().isoformat(timespec='seconds')
    status_counts = {}
    target_counts = {}
    for s in data.get('stocks', []):
        status_counts[s.get('researchStatus', '未知')] = status_counts.get(s.get('researchStatus', '未知'), 0) + 1
        target_counts[s.get('targetStatus', '未知')] = target_counts.get(s.get('targetStatus', '未知'), 0) + 1
    data['research_summary'] = {
        'stocks_total': len(data.get('stocks', [])),
        'research_files': len(research_map),
        'targets_mapped': mapped_targets,
        'stale_days': STALE_DAYS,
        'generated': data['updated'],
        'status_counts': status_counts,
        'target_status_counts': target_counts,
    }
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"prices updated: {updated_prices}; research mapped: {mapped_research}; targets mapped: {mapped_targets}")
    print('research status:', status_counts)
    print('target status:', target_counts)

if __name__ == '__main__':
    main()
