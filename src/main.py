from models import *
from clients.openai_client import *
from data_fetcher import get_daily_prices,levels_calc
from utils.report import save_report
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT = (BASE_DIR / "prompts" / "system_prompt.md").read_text(encoding="utf-8")




def get_pricing_report(request: PricingRequest) -> PricingReport:
    response = OPENAI_CLIENT.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=[
            {"role":"system","content":SYSTEM_PROMPT}, ## system prompt md ? import ?
            {"role": "user", "content": request.model_dump_json()}
        ],
        response_format=PricingReport
    )
    return response.choices[0].message.parsed



def main():
    target_coin = "ETHUSDT"
    print(f"Запуск анализа {target_coin}")
    candles = get_daily_prices(symbol=target_coin)

    levels = levels_calc(candles)

    request = PricingRequest(
        coin=target_coin,
        timeframe="1d",
        topic="Поиск среднесрочной сделки на основе 24ч свечей",
        comments=[
            f"Текущие свечи: {candles}. "
            f"Математические уровни: Pivot: ${levels['p']}, "
            f"Поддержка: ${levels['support_level']}, Сопротивление: ${levels['resistance_level']}. "
            "Используй эти уровни для обоснования точки входа с RR > 3.0 и опиши риски."
        ],
    )

    report: PricingReport = get_pricing_report(request)
    print("\n" + "=" * 50)
    print(f"🪙 Монета: {target_coin}")
    print(f"📈 Тренд: {report.analysis.trend.upper()}")
    print(f"💵 Текущая цена: ${report.analysis.current_price}")
    print(f"🛡 Поддержка: ${report.analysis.support_level} | Сопротивление: ${report.analysis.resistance_level}")
    print("-" * 50)
    print(f"🎯 Сделка: {report.trade_levels.trade_enter_direction.upper()}")
    print(f"   Вход: ${report.trade_levels.enter_price}")
    print(f"   Take-Profit: ${report.trade_levels.take_profit}")
    print(f"   Stop-Loss:   ${report.trade_levels.stop_loss}")
    print(f"   Уверенность: {report.trade_levels.projection_confidence}")
    print("-" * 50)
    print(f"💡 Рекомендация: {report.recommendation.upper()}")
    print(f"⚠️ Риски: {', '.join(report.risks)}")
    print("=" * 50)

    save_report(report,target_coin)


if __name__ == "__main__":
    main()