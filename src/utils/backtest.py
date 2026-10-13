from indicators.rsi import rsi_calc,get_historical_prices

candles = get_historical_prices("ETHUSDT",interval="1h")

data = rsi_calc(candles)


def run_backtest(candles: list[dict]):
    in_position = False
    trade_size = 100
    crypto_amount = 0.0
    initial_balance = 1000.0
    balance = initial_balance
    trades = []

    for i in range(1, len(candles)):
        prev_candle = candles[i - 1]
        curr_candle = candles[i]
        if not in_position:
            if prev_candle['rsi'] is not None and prev_candle["rsi"] <= 30 and curr_candle["rsi"] > 30:
                buy_price = curr_candle["Close"]
                crypto_amount = trade_size / buy_price
                in_position = True
                print(f"КУПИЛИ по цене: {buy_price} (RSI: {curr_candle['rsi']})")
        else:
            if curr_candle["rsi"] >= 50:
                sell_price = curr_candle["Close"]
                payout = crypto_amount * sell_price
                profit_usd = payout - trade_size
                balance = balance + profit_usd

                profit = ((sell_price - buy_price) / buy_price * 100)
                trades.append(profit)

                print(f"ПРОДАЛИ по цене: {sell_price} (Прибыль: {round(profit, 2)}%)")
                in_position = False
    return trades,balance

# Запускаем симуляцию на подготовленных данных:
my_trades,final_balance = run_backtest(data)

print(f"Всего сделок: {len(my_trades)}")
print(f"Список сделок (% прибыли): {my_trades}")
print(f"Финальный баланс: ${round(final_balance, 2)}")
print(f"Чистая прибыль: ${round(final_balance - 1000.0, 2)}")