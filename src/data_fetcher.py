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



