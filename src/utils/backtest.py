from indicators.rsi import rsi_calc,get_historical_prices
from models.models import Wallet
from data_fetcher import levels_calc

candles = get_historical_prices("ETHUSDT",interval="1h")

data = rsi_calc(candles)


def run_backtest(candles: list[dict]) -> Wallet:
    wallet = Wallet()
    in_position = False

    stop_loss = 0.02
    stop_price = 0.0


    for i in range(24, len(candles)):
        prev_candle = candles[i - 1]
        curr_candle = candles[i]

        last_24_candles = candles[i - 24 : i]
        levels = levels_calc(last_24_candles)
        pivot = levels['p']


        if not in_position:
            rsi_signal = (prev_candle['rsi'] is not None and prev_candle["rsi"] <= 30 < curr_candle["rsi"])
            trend_filter = curr_candle["Close"] > pivot

            if rsi_signal:
                wallet.buy(curr_candle["Close"],amount_usdt=100.0)
                in_position = True

                stop_price = curr_candle["Close"] * (1-stop_loss)

                print(f"КУПИЛИ по цене: {curr_candle["Close"]} PIVOT {pivot} (Баланс: ${round(wallet.balance,2)})"
                      f"Stop price{stop_price} stop_loss {stop_loss}")
        else:
            if curr_candle["rsi"] >= 50:
                wallet.sell(curr_candle["Close"])
                in_position = False
                print(f"ВЫШЛИ В ПЛЮС (RSI >= 50): {curr_candle['Close']}")

            if curr_candle["Close"] <= stop_price:
                wallet.sell(curr_candle["Close"])
                in_position = False
                print(f"ВЫШЛИ ПО СТОПУ (-2%): {curr_candle['Close']}")

    return wallet

# Запускаем симуляцию на подготовленных данных:
wallet = run_backtest(data)

print(f"Всего сделок: {len(wallet.trades)}")
#print(f"Список сделок (% прибыли): {wallet.trades}")
print(f"Финальный баланс: ${round(wallet.balance, 2)}")
print(f"Чистая прибыль: ${round(wallet.balance - 1000.0, 2)}")