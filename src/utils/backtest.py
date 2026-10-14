from indicators.rsi import rsi_calc,get_historical_prices
from models.models import Wallet

candles = get_historical_prices("ETHUSDT",interval="1h")

data = rsi_calc(candles)


def run_backtest(candles: list[dict]) -> Wallet:
    wallet = Wallet()
    in_position = False

    for i in range(1, len(candles)):
        prev_candle = candles[i - 1]
        curr_candle = candles[i]


        if not in_position:
            if prev_candle['rsi'] is not None and prev_candle["rsi"] <= 30 and curr_candle["rsi"] > 30:
                wallet.buy(curr_candle["Close"],amount_usdt=100.0)
                in_position = True

                print(f"КУПИЛИ по цене: {curr_candle["Close"]} (Баланс: ${round(wallet.balance,2)})")
        else:
            if curr_candle["rsi"] >= 50:
                wallet.sell(curr_candle["Close"])

                print(f"ПРОДАЛИ по цене: {curr_candle["Close"]} | (Баланс: {round(wallet.balance, 2)}%)")
                in_position = False
    return wallet

# Запускаем симуляцию на подготовленных данных:
wallet = run_backtest(data)

print(f"Всего сделок: {len(wallet.trades)}")
print(f"Список сделок (% прибыли): {wallet.trades}")
print(f"Финальный баланс: ${round(wallet.balance, 2)}")
print(f"Чистая прибыль: ${round(wallet.balance - 1000.0, 2)}")