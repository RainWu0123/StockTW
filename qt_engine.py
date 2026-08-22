#!/usr/bin/env python3
"""量化訊號引擎：短線動能 + 長線估值，分開計算、附理由。
寫入 data.json 的 qt_signal 欄位。"""
import json, datetime
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
data = json.loads((BASE/'data.json').read_text(encoding='utf-8'))

def calc_signals(s):
    """為單一股票計算短線與長線量化訊號，回傳 dict 附理由。"""
    result = {}
    price = s.get('price')
    if not price or not s.get('code','').isdigit():
        return None
    
    # === 短線動能（1~5 個交易日）===
    short_score = 0
    short_reasons = []
    
    # 日漲跌動能
    day = s.get('pct') or 0
    if day > 2:
        short_score += 20; short_reasons.append(f'日漲{day:+.1f}%強勢')
    elif day > 0.5:
        short_score += 10; short_reasons.append(f'日漲{day:+.1f}%偏多')
    elif day < -3:
        short_score -= 20; short_reasons.append(f'日跌{day:+.1f}%弱勢')
    elif day < -0.5:
        short_score -= 10; short_reasons.append(f'日跌{day:+.1f}%偏空')
    
    # 週動能
    wk = s.get('week_pct') or 0
    if abs(wk) > 0.01:  # 有資料才評分
        if wk > 5:
            short_score += 15; short_reasons.append(f'週漲{wk:.0f}%')
        elif wk > 1:
            short_score += 8; short_reasons.append(f'週漲{wk:.0f}%')
        elif wk < -5:
            short_score -= 15; short_reasons.append(f'週跌{wk:.0f}%')
    
    # 月動能（中期趨勢確認）
    mo = s.get('month_pct') or 0
    if abs(mo) > 0.01:
        if mo > 10:
            short_score += 10; short_reasons.append(f'月漲{mo:.0f}%趨勢向上')
        elif mo < -10:
            short_score -= 10; short_reasons.append(f'月跌{mo:.0f}%趨勢向下')
    
    # 成交量異常（爆量偵測）
    avg_vol = s.get('averageVolume10days')
    vol_today = s.get('vol')
    if avg_vol and vol_today and vol_today > avg_vol * 2:
        short_score += 10; short_reasons.append('爆量（2倍於均量）')
    
    # 52週高低點位置（距離高點越近動能越強但風險也高）
    hi = s.get('52WeekHigh')
    lo = s.get('52WeekLow')
    if hi and lo and hi > lo:
        pos = (price - lo) / (hi - lo)  # 0=低點 1=高點
        if pos > 0.9:
            short_score += 5; short_reasons.append(f'接近52W高點（位置{pos:.0%}）')
        elif pos < 0.15:
            short_score -= 5; short_reasons.append(f'接近52W低點（位置{pos:.0%}）')
    
    # === 長線估值（基本面+研究目標價）===
    long_score = 0
    long_reasons = []
    
    td = s.get('targetDist')
    if td is not None:
        if td <= -30:
            long_score += 30; long_reasons.append(f'現價低於目標{abs(td):.0f}%，安全邊際大')
        elif td <= -15:
            long_score += 20; long_reasons.append(f'低於目標{abs(td):.0f}%，有空間')
        elif td <= -5:
            long_score += 10; long_reasons.append(f'低於目標{abs(td):.0f}%')
        elif td >= 5:
            long_score -= 20; long_reasons.append(f'已超越目標{td:.0f}%，透支')
        elif td >= -5:
            pass  # 接近合理價，不加減分
    
    # 基本面維度
    dims = s.get('dimensions', {})
    fund = dims.get('fundamental', 0)
    if fund >= 70:
        long_score += 15; long_reasons.append(f'基本面分{fund:.0f}/100')
    elif fund >= 50:
        long_score += 8; long_reasons.append(f'基本面分{fund:.0f}/100')
    elif fund < 25:
        long_score -= 8; long_reasons.append(f'基本面偏弱({fund:.0f})')
    
    # 盈餘成長
    eg = s.get('earningsGrowth')
    if eg is not None:
        if eg > 0.5:
            long_score += 10; long_reasons.append(f'盈餘成長{eg*100:.0f}%')
        elif eg > 0.1:
            long_score += 5; long_reasons.append(f'盈餘成長{eg*100:.0f}%')
        elif eg < -0.2:
            long_score -= 5; long_reasons.append(f'盈餘衰退{eg*100:.0f}%')
    
    # 營收成長
    rg = s.get('revenueGrowth')
    if rg is not None:
        if rg > 0.3:
            long_score += 8; long_reasons.append(f'營收年增{rg*100:.0f}%')
        elif rg < -0.1:
            long_score -= 5; short_reasons.append(f'營收衰退{rg*100:.0f}%')
    
    # ETF 加分（被動買盤支撐）
    if s.get('etf0050'):
        long_score += 5; long_reasons.append('0050成分股（被動資金支撐）')
    if s.get('etf00981A'):
        long_score += 5; long_reasons.append('00981A成分股（主動基金布局）')
    
    # === 訊號等級 ===
    def grade(score):
        if score >= 40: return '🟢 強力買進'
        if score >= 20: return '🟢 買進'
        if score >= 10: return '🟡 偏多'
        if score >= -10: return '⚪ 中性'
        if score >= -20: return '🟠 偏空'
        return '🔴 賣出'
    
    result['qt_short'] = {
        'score': short_score,
        'signal': grade(short_score),
        'reasons': short_reasons,
    }
    result['qt_long'] = {
        'score': long_score,
        'signal': grade(long_score),
        'reasons': long_reasons,
    }
    # 綜合：短線權重40%、長線60%
    combined = round(short_score * 0.4 + long_score * 0.6, 1)
    result['qt_combined'] = {
        'score': combined,
        'signal': grade(combined),
        'note': '短線40%＋長線60%加權',
    }
    return result


count = 0
for s in data['stocks']:
    sig = calc_signals(s)
    if sig:
        s['qt'] = sig
        count += 1

(BASE/'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'quantitative signals computed for {count}/{len(data["stocks"])} stocks')

# 印出前幾檔範例驗證
for s in data['stocks'][:5]:
    q = s.get('qt')
    if q:
        print(f"{s['code']} {s['name']} | 短線:{q['qt_short']['score']}({q['qt_short']['signal']}) | "
              f"長線:{q['qt_long']['score']}({q['qt_long']['signal']}) | "
              f"綜合:{q['qt_combined']['score']}({q['qt_combined']['signal']})")
