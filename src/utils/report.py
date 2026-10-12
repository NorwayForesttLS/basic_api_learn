import datetime
from pathlib import Path
from models import PricingReport

BASE_DIR = Path(__file__).resolve().parent  # это папка src
PROJECT_ROOT = BASE_DIR.parent.parent              # это корень проекта api_lessons
target_dir = PROJECT_ROOT / "reports"

target_dir.mkdir(parents=True,exist_ok=True)


def save_report(report: PricingReport, coin: str):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"report {now_str}, coin {coin}.md"
    file_path = target_dir / file_name

    content = f"""# 🪙 Анализ {coin}
    **Дата:** {now_str}
    ## Рыночный анализ
    - **Тренд:** {report.analysis.trend.upper()}
    - **Текущая цена:** ${report.analysis.current_price}
    - **Поддержка:** ${report.analysis.support_level}
    - **Сопротивление:** ${report.analysis.resistance_level}
    ## Сигнал на сделку
    - **Направление:** {report.trade_levels.trade_enter_direction.upper()}
    - **Вход:** ${report.trade_levels.enter_price}
    - **Take-Profit:** ${report.trade_levels.take_profit}
    - **Stop-Loss:** ${report.trade_levels.stop_loss}
    ## Рекомендация
    > {report.recommendation.upper()}
    """

    with open(file_path,"w",encoding="utf-8") as file:
        file.write(content)




