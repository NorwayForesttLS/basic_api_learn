import pandas as pd
import numpy as np
import json
from datetime import datetime
import time
from clients.binance_client import binance_client

keys = ["Open time","Open","High","Low","Close","Volume","Close time",
        "Quote asset volume"]

def get_historical_prices(symbol: str = "BTCUSDT",interval: str = "1h") -> list[dict]:

    klines = binance_client.get_klines(symbol=symbol,interval=interval,
                               limit=1000)

    prices_per_day = [dict(zip(keys, kline[:7])) for kline in klines]

    for candle in prices_per_day:
        open_time_sec = candle["Open time"] / 1000
        close_time_sec = candle["Close time"] / 1000
        candle["Open time"] = datetime.fromtimestamp(open_time_sec).strftime('%Y-%m-%d %H:%M:%S')
        candle["Close time"] = datetime.fromtimestamp(close_time_sec).strftime('%Y-%m-%d %H:%M:%S')
        candle["Open"] = float(candle["Open"])
        candle["High"] = float(candle["High"])
        candle["Low"] = float(candle["Low"])
        candle["Close"] = float(candle["Close"])
    return prices_per_day

def rsi_calc(candles: list[dict],period=14):
    deltas = []
    gains = []
    losses = []
    candles[0]['rsi'] = None
    for index in range(1,len(candles)):
        current_candle = candles[index]

        if index > 0:
            delta = candles[index]["Close"] - candles[index - 1]["Close"]
            deltas.append(delta)

            gain = delta if delta > 0 else 0
            loss = abs(delta) if delta < 0 else 0
            gains.append(gain)
            losses.append(loss)

            if len(gains) < 14:
                current_candle["rsi"] = None
            else:
                recent_gains = gains[-14:]
                recent_losses = losses[-14:]

                avg_gain = sum(recent_gains) / 14
                avg_loss = sum(recent_losses) / 14
                if avg_loss != 0:
                    rs = avg_gain / avg_loss
                    normalized_rs = 100 - (100 / (1 + rs))
                    current_candle['rsi'] = round(normalized_rs, 2)
                else:
                    current_candle['rsi'] = 100.0

    return candles

candles = get_historical_prices("ETHUSDT",interval="1h")
candles = rsi_calc(candles)

for c in candles:
    print(f"Время: {c['Close time']} | Цена: {c['Close']} | RSI: {c['rsi']}")

#print(rsi_calc(get_historical_prices()))#get_historical_prices(),indent=2)