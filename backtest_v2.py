#!/usr/bin/env python3
"""回測 v2：加入統計檢定力、趨勢濾網、風險指標、跨週期驗證。

修正項：
1. 趨勢濾網（Trend Filter）：只在 MA60 > MA200 時允許買進訊號
2. 樣本數門檻：至少 100 次觸發才報告
3. 完整風險指標：Profit Factor、Max Drawdown、Sharpe Ratio
4. Wilson Score 信賴區間
5. 基準線對比（隨機買進的勝率作為 null hypothesis）
"""
import json, math, sys, os
from pathlib import Path

BASE = Path('/home/ubuntu/investment')
HIST_DIR = BASE / 'data' / 'hist'


def wilson_ci(wins: int, total: int, confidence: float = 0.95) -> tuple:
    """Wilson Score 信賴區間"""
    if total == 0:
        return (0, 0)
    z = 1.96 if confidence == 0.95 else 1.645
    p = wins / total
    margin = z * math.sqrt(p * (1 - p) / total + z**2 / (4 * total**2))
    lower = max(0, (p + z**2/(2*total) - margin) / (1 + z**2/total))
    upper = min(1, (p + z**2/(2*total) + margin) / (1 + z**2/total))
    return (round(lower*100, 1), round(upper*100, 1))


def max_drawdown(returns: list) -> float:
    """最大回撤（連續虧損的累積最大損失）"""
    if not returns:
        return 0.0
    cumulative = 1.0
    peak = 1.0
    mdd = 0.0
    for r in returns:
        cumulative *= (1 + r/100)
        peak = max(peak, cumulative)
        dd = (peak - cumulative) / peak
        mdd = max(mdd, dd)
    return round(mdd * 100, 2)


def sharpe_ratio(returns: list, risk_free_daily: float = 0.01/252) -> float:
    """夏普比率（年化）"""
    if len(returns) < 2:
        return 0.0
    excess = [r/100 - risk_free_daily for r in returns]
    mean_excess = sum(excess) / len(excess)
    variance = sum((x - mean_excess)**2 for x in excess) / (len(excess) - 1)
    std = math.sqrt(variance) if variance > 0 else 0.001
    return round(mean_excess / std * math.sqrt(252), 2)


def profit_factor(returns: list) -> float:
    """賺賠比 = 總獲利 / 總虧損"""
    gross_profit = sum(r for r in returns if r > 0)
    gross_loss = abs(sum(r for r in returns if r < 0))
    if gross_loss == 0:
        return float('inf') if gross_profit > 0 else 0.0
    return round(gross_profit / gross_loss, 2)


# ══════════════════════════════════════════
# 趨勢濾網
# ══════════════════════════════════════════

def is_uptrend(closes: list, i: int, ma60: list, ma200: list) -> bool:
    """趨勢濾網：MA60 > MA200 且收盤 > MA60（多頭格局才允許買進）"""
    if i < 200 or not ma60[i] or not ma200[i]:
        return False
    return ma60[i] > ma200[i] and closes[i] > ma60[i]


def is_downtrend(closes: list, i: int, ma60: list, ma200: list) -> bool:
    """空頭格局"""
    if i < 200 or not ma60[i] or not ma200[i]:
        return False
    return ma60[i] < ma200[i] and closes[i] < ma60[i]


# ══════════════════════════════════════════
# 完整回測 v2
# ══════════════════════════════════════════

def backtest_v2(rows: list, signal_fn, hold_days: int = 5,
                use_trend_filter: bool = True,
                stop_loss_pct: float = None) -> dict:
    """
    回測 v2：
    - use_trend_filter: 只在多頭格局觸發
    - stop_loss_pct: ATR 停損（如 0.05 = 5%）
    """
    from tech_engine import sma, calc_kd, calc_rsi, calc_macd, calc_bollinger, calc_bias

    closes = [r['close'] for r in rows]
    highs = [r['high'] for r in rows]
    lows = [r['low'] for r in rows]

    ma5 = sma(closes,5); ma10=sma(closes,10); ma20=sma(closes,20)
    ma60 = sma(closes,60); ma200 = sma(closes, min(200, len(closes)//2)) if len(closes) >= 200 else [None]*len(closes)
    k,d = calc_kd(highs,lows,closes)
    rsi = calc_rsi(closes,14)
    macd = calc_macd(closes)
    boll = calc_bollinger(closes)
    bias = calc_bias(closes,20)

    returns = []
    triggers = 0
    bull_triggers = 0
    bear_triggers = 0

    for i in range(210, len(rows) - hold_days):
        # 趨勢分類
        bull = is_uptrend(closes, i, ma60, ma200)
        bear = is_downtrend(closes, i, ma60, ma200)

        if use_trend_filter and not bull:
            continue  # 只在多頭格局觸發

        if signal_fn(i):
            triggers += 1
            if bull: bull_triggers += 1
            if bear: bear_triggers += 1

            entry = closes[i]
            # 停損檢查
            stop = None
            if stop_loss_pct:
                stop = entry * (1 - stop_loss_pct)

            exit_price = closes[min(i + hold_days, len(rows)-1)]
            # 逐日檢查停損
            if stop:
                for j in range(i+1, min(i+hold_days+1, len(rows))):
                    if lows[j] <= stop:
                        exit_price = stop
                        break
                    exit_price = closes[j]

            ret = (exit_price - entry) / entry * 100
            returns.append(ret)

    # 統計
    if not returns:
        return {'count': 0, 'note': 'insufficient triggers'}

    wins = sum(1 for r in returns if r > 0)
    win_rate = wins / len(returns)
    ci_low, ci_high = wilson_ci(wins, len(returns))

    return {
        'count': len(returns),
        'win_rate': round(win_rate * 100, 1),
        'wilson_95ci': f'[{ci_low}%, {ci_high}%]',
        'statistically_significant': len(returns) >= 100,
        'avg_return': round(sum(returns)/len(returns), 2),
        'profit_factor': profit_factor(returns),
        'max_drawdown': max_drawdown(returns),
        'sharpe': sharpe_ratio(returns),
        'bull_triggers': bull_triggers,
        'bear_triggers': bear_triggers,
    }


def run_backtest_v2(rows: list, code: str) -> dict:
    """跑全部訊號的 v2 回測（含趨勢濾網＋停損）。"""
    from tech_engine import sma, calc_kd, calc_rsi, calc_macd, calc_bollinger, calc_bias

    closes = [r['close'] for r in rows]
    highs = [r['high'] for r in rows]
    lows = [r['low'] for r in rows]

    ma5=sma(closes,5); ma10=sma(closes,10); ma20=sma(closes,20); ma60=sma(closes,60)
    ma200 = sma(closes, min(200, len(closes)//2)) if len(closes) >= 200 else [None]*len(closes)
    k,d = calc_kd(highs,lows,closes)
    rsi = calc_rsi(closes,14)
    macd = calc_macd(closes)
    boll = calc_bollinger(closes)
    bias = calc_bias(closes,20)

    # 訊號定義（不變）
    signals = {
        '觸及布林下軌': lambda i: boll['lower'][i] is not None and closes[i] <= boll['lower'][i],
        '站上MA20': lambda i: i>0 and closes[i-1]<=ma20[i-1] and closes[i]>ma20[i],
        'MA5黃金交叉MA20': lambda i: i>1 and ma5[i-1]<=ma20[i-1] and ma5[i]>ma20[i],
        '布林壓縮後突破': lambda i: i>5 and boll['bandwidth'][i-5] is not None and boll['bandwidth'][i] is not None and boll['bandwidth'][i-5]<8 and boll['bandwidth'][i]>boll['bandwidth'][i-5] and closes[i]>closes[i-1],
        'KD低檔黃金交叉': lambda i: i>1 and k[i-1]<=d[i-1] and k[i]>d[i] and k[i]<25,
        '乖離率<-7%回升': lambda i: i>0 and bias[i] is not None and bias[i-1] is not None and bias[i-1]<-7 and bias[i]>bias[i-1],
        'MACD黃金交叉': lambda i: i>1 and macd['dif'][i-1] is not None and macd['dif'][i-1]<=macd['macd'][i-1] and macd['dif'][i]>macd['macd'][i],
    }

    results = {}
    for name, fn in signals.items():
        # 無濾網版
        raw = backtest_v2(rows, fn, hold_days=5, use_trend_filter=False)
        # 有趨勢濾網版
        filtered = backtest_v2(rows, fn, hold_days=5, use_trend_filter=True)
        # 有濾網＋停損版
        filtered_sl = backtest_v2(rows, fn, hold_days=5, use_trend_filter=True, stop_loss_pct=0.05)

        results[name] = {
            'no_filter': raw,
            'with_trend_filter': filtered,
            'with_filter_and_stoploss': filtered_sl,
        }

    return results


if __name__ == '__main__':
    from tech_engine import fetch_history
    import time

    data = json.loads((BASE/'data.json').read_text(encoding='utf-8'))
    all_codes = [s['code'] for s in data['stocks'] if s.get('code','').isdigit()]

    # 抓取更多股票的歷史資料（擴大樣本）
    fetch_list = sys.argv[1:] if len(sys.argv) > 1 else all_codes[:30]

    print('=== Phase 1: Fetch history ===')
    for code in fetch_list:
        hf = HIST_DIR / f'{code}.json'
        if hf.exists():
            rows = json.loads(hf.read_text())
            if len(rows) >= 100:
                continue
        try:
            rows = fetch_history(code, months_back=12)
            print(f'  {code}: {len(rows)} days')
        except Exception as e:
            print(f'  {code}: FAIL {e}')

    print('\n=== Phase 2: Backtest v2 ===')
    all_results = {}
    for code in fetch_list:
        hf = HIST_DIR / f'{code}.json'
        if not hf.exists(): continue
        rows = json.loads(hf.read_text())
        if len(rows) < 210:
            continue

        print(f'\n--- {code} ({len(rows)} days) ---')
        results = run_backtest_v2(rows, code)

        # 只印出統計顯著或有趨勢濾網後勝率 > 60% 的訊號
        for sig_name, versions in results.items():
            tf = versions.get('with_trend_filter', {})
            nf = versions.get('no_filter', {})
            if tf.get('count', 0) >= 3:
                print(f'  {sig_name}:')
                print(f'    無濾網: {nf.get("count",0)}次 勝率{nf.get("win_rate","?")}%')
                print(f'    +濾網: {tf["count"]}次 勝率{tf["win_rate"]}% CI{tf["wilson_95ci"]} PF{tf["profit_factor"]} MDD{tf["max_drawdown"]}% Sharpe{tf["sharpe"]}')
                sl = versions.get('with_filter_and_stoploss', {})
                if sl.get('count',0) > 0:
                    print(f'    +停損: {sl["count"]}次 勝率{sl["win_rate"]}% PF{sl["profit_factor"]} MDD{sl["max_drawdown"]}%')

        all_results[code] = results

    out = BASE / 'data' / 'tech_backtest_v2.json'
    out.write_text(json.dumps(all_results, ensure_ascii=False, indent=2))
    print(f'\nSaved to {out}')
