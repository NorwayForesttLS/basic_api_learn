from dataclasses import Field
from datetime import datetime
from pydantic import BaseModel
from typing import Optional,Literal
from typing_extensions import Annotated

class PricingRequest(BaseModel):
    coin: str | None
    timeframe: Literal["1h", "4h", "1d", "1w"]
    topic: str
    comments: Optional[list[str]] | None

class MarketAnalysis(BaseModel):
    current_price: float
    trend: Literal["bearish","bullish","sideways"]
    support_level: float
    resistance_level: float
    key_signal: list[str]

class PricingProjection(BaseModel):
    trade_enter_direction: Literal["long","short"]
    enter_price: float
    take_profit: float
    stop_loss: float
    projection_confidence: Literal["100%","75%","50%","25%","0%"]


class PricingReport(BaseModel):
    analysis: MarketAnalysis
    trade_levels: PricingProjection
    conclusion: list[str]
    risks: list[str]
    recommendation: Literal["hold","sell","buy"]



