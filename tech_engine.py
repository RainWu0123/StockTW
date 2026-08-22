#!/usr/bin/env python3
"""技術分析引擎：計算 MA/KD/RSI/MACD/布林通道/乖離率。
資料來源：TWSE 官方日K線（開高低收+成交量）。

用法：
  python3 tech_engine.py --fetch 2330 2454   # 抓取歷史資料
  python3 tech_engine.py --calc              # 計算所有指標
  python3 tech_engine.py --backtest          # 回測訊號勝率
"""
import json, math, urllib.request, time, sys, os
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path('/home/ubuntu/investment')
HIST_DIR = BASE / 'data' / 'hist'
HIST_DIR.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════
# 資料抓取：TWSE 日 K（每次一個月，需逐月抓）
# ══════════════════════════════════════════

def fetch_twse_daily(code: str, year: int, month: int) -> list:
    """抓 TWSE 單月日K。回傳 [{date, open, high, low, close, vol}]"""
    url = f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={year}{month:02d}01&stockNo={code}&response=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    d = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
    rows = []
    if d.get('stat') != 'OK':
        return rows
    for r in d.get('data', []):
        try:
            date_str = f'{int(r[0].split("/")[0])+1911}-{r[0].split("/")[1]}-{r[0].split("/")[2]}'
            o, h, l, c = (float(x.replace(',','')) for x in (r[3],r[4],r[5],r[6]))
            v = int(r[1].replace(',', ''))
            rows.append({'date': date_str, 'open': o, 'high': h, 'low': l, 'close': c, 'vol': v})
        except (ValueError, IndexError):
            continue
    return rows


def fetch_history(code: str, months_back: int = 12) -> list:
    """抓近 N 個月的日K資料，合併去重存檔。"""
    hist_file = HIST_DIR / f'{code}.json'
    existing = []
    if hist_file.exists():
        existing = json.loads(hist_file.read_text())
    seen_dates = {r['date'] for r in existing}

    now = datetime.now()
    new_rows = []
    for m in range(months_back):
        dt = now - timedelta(days=30 * m)
        y, mo = dt.year, dt.month
        rows = fetch_twse_daily(code, y, mo)
        time.sleep(0.5)  # rate limit
        for r in rows:
            if r['date'] not in seen_dates:
                new_rows.append(r)
                seen_dates.add(r['date'])

    all_rows = sorted(existing + new_rows, key=lambda x: x['date'])
    hist_file.write_text(json.dumps(all_rows, ensure_ascii=False))
    return all_rows


# ══════════════════════════════════════════
# 技術指標計算
# ══════════════════════════════════════════

def sma(closes: list, period: int) -> list:
    """簡單移動平均線"""
    result = []
    for i in range(len(closes)):
        if i < period - 1:
            result.append(None)
        else:
            result.append(sum(closes[i-period+1:i+1]) / period)
    return result


def ema(values: list, period: int) -> list:
    """指數移動平均"""
    k = 2 / (period + 1)
    result = [None] * len(values)
    if len(values) < period:
        return result
    result[period-1] = sum(values[:period]) / period
    for i in range(period, len(values)):
        result[i] = values[i] * k + result[i-1] * (1 - k)
    return result


def calc_rsi(closes: list, period: int = 14) -> list:
    """RSI 相對強弱指標"""
    result = [None] * len(closes)
    if len(closes) < period + 1:
        return result
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    if avg_loss == 0:
        result[period] = 100
    else:
        rs = avg_gain / avg_loss
        result[period] = 100 - 100 / (1 + rs)
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period-1) + gains[i]) / period
        avg_loss = (avg_loss * (period-1) + losses[i]) / period
        if avg_loss == 0:
            result[i+1] = 100
        else:
            rs = avg_gain / avg_loss
            result[i+1] = 100 - 100 / (1 + rs)
    return result


def calc_kd(highs: list, lows: list, closes: list, period: int = 9) -> tuple:
    """KD 隨機指標，回傳 (k_values, d_values)"""
    n = len(closes)
    k_vals = [None]*n
    d_vals = [None]*n
    raw_k = []
    for i in range(n):
        if i < period - 1:
            raw_k.append(50)
            continue
        hh = max(highs[i-period+1:i+1])
        ll = min(lows[i-period+1:i+1])
        if hh == ll:
            rsv = 50
        else:
            rsv = (closes[i] - ll) / (hh - ll) * 100
        prev_k = raw_k[-1]
        k = prev_k * 2/3 + rsv * 1/3
        raw_k.append(k)
        k_vals[i] = round(k, 2)
        # D 值 = K 值的 3 日 EMA，用 raw_k 追蹤避免 None
        if i >= period:
            d_vals[i] = round(raw_k[-2] * 2/3 + k * 1/3, 2)
        else:
            d_vals[i] = round(k, 2)
    return k_vals, d_vals


def calc_macd(closes: list, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """MACD 指標，回傳 {'dif':[], 'macd':[], 'osc':[]}"""
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    dif = []
    for i in range(len(closes)):
        if ema_fast[i] is not None and ema_slow[i] is not None:
            dif.append(ema_fast[i] - ema_slow[i])
        else:
            dif.append(None)
    # 對 DIF 做 EMA 得到 MACD 線（信號線）
    valid_dif = [x if x is not None else 0 for x in dif]
    macd_line = ema(valid_dif, signal)
    osc = []
    for i in range(len(closes)):
        if dif[i] is not None and macd_line[i] is not None:
            osc.append(round(dif[i] - macd_line[i], 4))
        else:
            osc.append(None)
    return {
        'dif': [round(x,4) if x else None for x in dif],
        'macd': [round(x,4) if x else None for x in macd_line],
        'osc': osc,
    }


def calc_bollinger(closes: list, period: int = 20, num_std: float = 2.0) -> dict:
    """布林通道，回傳 {'upper':[], 'middle':[], 'lower':[], 'bandwidth':[]}"""
    mid = sma(closes, period)
    upper = [None]*len(closes)
    lower = [None]*len(closes)
    bw = [None]*len(closes)
    for i in range(period-1, len(closes)):
        window = closes[i-period+1:i+1]
        mean = sum(window) / period
        variance = sum((x-mean)**2 for x in window) / period
        std = math.sqrt(variance)
        upper[i] = round(mean + num_std*std, 2)
        lower[i] = round(mean - num_std*std, 2)
        if mid[i]:
            width = upper[i] - lower[i]
            bw[i] = round(width / mid[i] * 100, 2) if mid[i] > 0 else None
    return {'upper':upper,'middle':mid,'lower':lower,'bandwidth':bw}


def calc_bias(closes: list, period: int = 20) -> list:
    """乖離率 BIAS"""
    ma = sma(closes, period)
    return [round((closes[i]-ma[i])/ma[i]*100, 2) if ma[i] and ma[i]>0 else None
            for i in range(len(closes))]


def compute_all(rows: list) -> dict:
    """對完整 OHLCV 資料計算所有指標，回傳最新一天的快照＋近期趨勢。"""
    if len(rows) < 60:
        return {}
    dates = [r['date'] for r in rows]
    opens = [r['open'] for r in rows]
    highs = [r['high'] for r in rows]
    lows = [r['low'] for r in rows]
    closes = [r['close'] for r in rows]
    vols = [r['vol'] for r in rows]

    ma5 = sma(closes,5); ma10=sma(closes,10); ma20=sma(closes,20)
    ma60 = sma(closes,60); ma240 = sma(closes, min(240,len(closes)//2)) if len(closes)>=120 else [None]*len(closes)
    k,d = calc_kd(highs,lows,closes)
    rsi14 = calc_rsi(closes,14)
    macd = calc_macd(closes)
    boll = calc_bollinger(closes)
    bias20 = calc_bias(closes,20)

    last = -1
    latest_close = closes[last]

    def safe(arr): return arr[last] if arr and last < len(arr) else None

    snapshot = {
        'date': dates[last],
        'close': latest_close,
        # 均線系統
        'ma5': safe(ma5),'ma10':safe(ma10),'ma20':safe(ma20),
        'ma60': safe(ma60),
        'ma_bullish': (ma5[last] and ma10[last] and ma20[last] and
                       ma5[last]>ma10[last]>ma20[last]),  # 多頭排列
        'ma_bearish': (ma5[last] and ma10[last] and ma20[last] and
                       ma5[last]<ma10[last]<ma20[last]),  # 空頭排列
        'above_ma20': bool(ma20[last] and latest_close > ma20[last]),
        'above_ma60': bool(ma60[last] and latest_close > ma60[last]),
        # KD
        'kd_k': safe(k), 'kd_d': safe(d),
        'kd_golden_cross': bool(
            k[last] and d[last] and k[last-1] and d[last-1] and
            k[last-1] <= d[last-1] and k[last] > d[last]),  # 黃金交叉
        'kd_death_cross': bool(
            k[last] and d[last] and k[last-1] and d[last-1] and
            k[last-1] >= d[last-1] and k[last] < d[last]),
        'kd_overbought': bool(safe(k) and safe(k)>80),
        'kd_oversold': bool(safe(k) and safe(k)<20),
        # RSI
        'rsi14': safe(rsi14),
        'rsi_overbought': bool(safe(rsi14) and safe(rsi14)>70),
        'rsi_oversold': bool(safe(rsi14) and safe(rsi14)<30),
        # MACD
        'macd_dif': macd['dif'][last], 'macd_signal': macd['macd'][last],
        'macd_osc': macd['osc'][last],
        'macd_golden': bool(
            macd['dif'][last] and macd['macd'][last] and
            macd['dif'][last-1] is not None and
            macd['dif'][last-1] <= macd['macd'][last-1] and
            macd['dif'][last] > macd['macd'][last]),
        'macd_death': bool(
            macd['dif'][last] and macd['macd'][last] and
            macd['dif'][last-1] is not None and
            macd['dif'][last-1] >= macd['macd'][last-1] and
            macd['dif'][last] < macd['macd'][last]),
        'macd_above_zero': bool(macd['dif'][last] and macd['dif'][last]>0),
        # 布林通道
        'boll_upper': boll['upper'][last],'boll_lower': boll['lower'][last],
        'boll_middle': safe(boll['middle']),
        'boll_bandwidth': boll['bandwidth'][last],
        'price_at_upper': bool(boll['upper'][last] and latest_close>=boll['upper'][last]*0.98),
        'price_at_lower': bool(boll['lower'][last] and latest_close<=boll['lower'][last]*1.02),
        'boll_squeeze': bool(boll['bandwidth'][last] and boll['bandwidth'][last]<8),
        # 乖離率
        'bias20': bias20[last],
        # 成交量
        'vol_ratio': round(vols[last]/ (sum(vols[-11:-1])/10), 2) if sum(vols[-11:-1])>0 and len(vols)>=11 else None,
    }

    # 近期交叉偵測（過去5天內有沒有發生黃金/死亡交叉）
    recent_signals = []
    for i in range(max(1,len(closes)-5), len(closes)):
        if i < 1: continue
        # MA 黃金/死亡交叉
        if ma5[i] and ma20[i] and ma5[i-1] and ma20[i-1]:
            if ma5[i-1]<=ma20[i-1] and ma5[i]>ma20[i]:
                recent_signals.append(f'MA5上穿MA20({dates[i]})')
            if ma5[i-1]>=ma20[i-1] and ma5[i]<ma20[i]:
                recent_signals.append(f'MA5下穿MA20({dates[i]})')
        # KD 交叉
        if i<len(k) and k[i] and d[i] and k[i-1] is not None and d[i-1] is not None:
            if k[i-1]<=d[i-1] and k[i]>d[i] and k[i]<40:
                recent_signals.append(f'KD低檔黃金交叉({dates[i]})')
            if k[i-1]>=d[i-1] and k[i]<d[i] and k[i]>70:
                recent_signals.append(f'KD高檔死亡交叉({dates[i]})')
        # MACD 交叉
        if i<len(macd['dif']) and macd['dif'][i] and macd['macd'][i] and macd['dif'][i-1] is not None:
            if macd['dif'][i-1]<=macd['macd'][i-1] and macd['dif'][i]>macd['macd'][i]:
                recent_signals.append(f'MACD黃金交叉({dates[i]})')
            if macd['dif'][i-1]>=macd['macd'][i-1] and macd['dif'][i]<macd['macd'][i]:
                recent_signals.append(f'MACD死亡交叉({dates[i]})')

    snapshot['recent_signals'] = recent_signals
    return snapshot


# ══════════════════════════════════════════
# 回測框架：驗證各訊號的勝率與平均報酬
# ══════════════════════════════════════════

def backtest_signal(rows: list, signal_fn, hold_days: int = 5, lookforward: int = 5) -> dict:
    """
    回測某個訊號函數的歷史表現。
    signal_fn(i, rows) -> True/False（第 i 天是否觸發買進訊號）
    回測邏輯：觸發後持有 hold_days 天的報酬率。
    """
    closes = [r['close'] for r in rows]
    triggers = []
    returns = []

    for i in range(60, len(rows) - lookforward):
        if signal_fn(i, rows):
            entry = closes[i]
            exit_price = closes[min(i+hold_days, len(rows)-1)]
            ret = (exit_price - entry) / entry * 100
            returns.append(ret)
            triggers.append(i)

    if not returns:
        return {'count':0}
    wins = sum(1 for r in returns if r>0)
    return {
        'count': len(returns),
        'win_rate': round(wins/len(returns)*100, 1),
        'avg_return': round(sum(returns)/len(returns), 2),
        'max_return': round(max(returns), 2),
        'min_return': round(min(returns), 2),
    }


def run_backtests(rows: list) -> dict:
    """跑全部訊號的回測。"""
    closes=[r['close'] for r in rows]
    highs=[r['high'] for r in rows]; lows=[r['low'] for r in rows]

    # 預計算指標
    ma5=sma(closes,5); ma10=sma(closes,10); ma20=sma(closes,20); ma60=sma(closes,60)
    k,d=calc_kd(highs,lows,closes)
    rsi=calc_rsi(closes,14)
    macd=calc_macd(closes)
    boll=calc_bollinger(closes)
    bias=calc_bias(closes,20)

    signals={
      'MA5黃金交叉MA20': lambda i,r: i>1 and ma5[i-1]<=ma20[i-1] and ma5[i]>ma20[i],
      'MA5跌破MA20': lambda i,r: i>1 and ma5[i-1]>=ma20[i-1] and ma5[i]<ma20[i],
      '站上MA20': lambda i,r: i>0 and closes[i-1]<=ma20[i-1] and closes[i]>ma20[i],
      'KD低檔黃金交叉(<25)': lambda i,r: i>1 and k[i-1]<=d[i-1] and k[i]>d[i] and k[i]<25,
      'KD高檔死亡交叉(>75)': lambda i,r: i>1 and k[i-1]>=d[i-1] and k[i]<d[i] and k[i]>75,
      'RSI<30超賣': lambda i,r: i>0 and rsi[i] is not None and rsi[i]<30,
      'RSI>70超買': lambda i,r: i>0 and rsi[i] is not None and rsi[i]>70,
      'MACD黃金交叉': lambda i,r: i>1 and macd['dif'][i-1]<=macd['macd'][i-1] and macd['dif'][i]>macd['macd'][i],
      'MACD死亡交叉': lambda i,r: i>1 and macd['dif'][i-1]>=macd['macd'][i-1] and macd['dif'][i]<macd['macd'][i],
      '觸及布林下軌': lambda i,r: i>0 and boll['lower'][i] is not None and closes[i]<=boll['lower'][i],
      '觸及布林上軌': lambda i,r: i>0 and boll['upper'][i] is not None and closes[i]>=boll['upper'][i],
      '布林通道壓縮(<8%)': lambda i,r: i>0 and boll['bandwidth'][i] is not None and boll['bandwidth'][i]<8,
      '乖離率<-7%': lambda i,r: bias[i] is not None and bias[i]<-7,
      '乖離率>+7%': lambda i,r: bias[i] is not None and bias[i]>7,
      '多頭排列(MA5>10>20)': lambda i,r: i>0 and ma5[i] and ma10[i] and ma20[i] and ma5[i]>ma10[i]>ma20[i] and not(ma5[i-1]>ma10[i-1]>ma20[i-1] if ma5[i-1] and ma10[i-1] and ma20[i-1] else False),
    }

    results={}
    for name,fn in signals.items():
        r5=backtest_signal(rows,fn,hold_days=5)
        r10=backtest_signal(rows,fn,hold_days=10)
        results[name]={'hold_5d':r5,'hold_10d':r10}
    return results


# ══════════════════════════════════════════
# 主程式
# ══════════════════════════════════════════

if __name__=='__main__':
    data=json.loads((BASE/'data.json').read_text(encoding='utf-8'))
    codes=[s['code'] for s in data['stocks'] if s.get('code','').isdigit()]

    mode=sys.argv[1] if len(sys.argv)>1 else '--calc'

    if mode=='--fetch':
        target_codes=sys.argv[2:] if len(sys.argv)>2 else codes[:20]  # 分批
        for code in target_codes:
            print(f'Fetching {code}...',end=' ')
            try:
                rows=fetch_history(code,months_back=12)
                print(f'{len(rows)} days')
            except Exception as e:
                print(f'FAIL {e}')
        print('Done. Next run: python3 tech_engine.py --calc')

    elif mode=='--calc':
        results={}
        for code in codes:
            hf=HIST_DIR/f'{code}.json'
            if not hf.exists(): continue
            rows=json.loads(hf.read_text())
            snap=compute_all(rows)
            if snap:
                results[code]=snap
        out=BASE/'data'/'tech_signals.json'
        out.write_text(json.dumps(results,ensure_ascii=False,indent=2))
        print(f'Tech signals written: {len(results)} stocks -> {out}')

    elif mode=='--backtest':
        # 對前幾檔大權值股跑回測驗證
        test_codes=sys.argv[2:] if len(sys.argv)>2 else ['2330','2454','2308','2317','2881']
        all_results={}
        for code in test_codes:
            hf=HIST_DIR/f'{code}.json'
            if not hf.exists():
                print(f'{code}: no history, fetching...')
                fetch_history(code,12)
            rows=json.loads(hf.read_text())
            print(f'\n=== {code} 回測（{len(rows)}天）===')
            bt=run_backtests(rows)
            for sig_name,res in sorted(bt.items()):
                if res.get('count',0)>=3:
                    h5=res['hold_5d']
                    print(f'  {sig_name}: 觸發{res["count"]}次 | 5天勝率{h5["win_rate"]}% | 平均報酬{h5["avg_return"]}%')
            all_results[code]=bt
        out=BASE/'data'/'tech_backtest.json'
        out.write_text(json.dumps(all_results,ensure_ascii=False,indent=2))
        print(f'\nBacktest results saved to {out}')
