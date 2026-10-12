import json
from datetime import datetime
import time
from clients.binance_client import binance_client


keys = ["Open time","Open","High","Low","Close","Volume","Close time",
        "Quote asset volume"]


def get_daily_prices(symbol: str = "BTCUSDT") -> list[dict]:
    now = int(time.time() * 1000)
    day_ago_ms = now - (24 * 60 * 60 * 1000)

    klines = binance_client.get_klines(symbol=symbol,interval=binance_client.KLINE_INTERVAL_1HOUR,
                               startTime=day_ago_ms,endTime=now)

    prices_per_day= [dict(zip(keys,kline[:8])) for kline in klines]

    for candle in prices_per_day:
        open_time_sec = candle["Open time"] / 1000
        close_time_sec = candle["Close time"] / 1000

        candle["Open time"] = datetime.fromtimestamp(open_time_sec).strftime('%Y-%m-%d %H:%M:%S')
        candle["Close time"] = datetime.fromtimestamp(close_time_sec).strftime('%Y-%m-%d %H:%M:%S')
    return prices_per_day
#data model : print(json.dumps(get_daily_prices(),indent=2))



def levels_calc(candles: list[dict]):
    candles = candles
    all_highs = [float(c["High"]) for c in candles]
    day_high = max(all_highs)
    all_lows = [float(c["Low"]) for c in candles]
    day_low = min(all_lows)
    day_close = float(candles[-1]["Close"])

    p = round(((day_high + day_low + day_close) / 3),3)

    resistance_level = round(((2 * p) - day_low),3)
    support_level = round(((2 * p) - day_high),3)

    return {"p":p,"resistance_level":resistance_level,"support_level":support_level}


