from dataclasses import Field
from datetime import datetime
from hashlib import new

from binance.ccxt.static_dependencies.starkware import crypto
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


class Wallet:
    def __init__ (self,balance=1000.0,fee_rate=0.001,entry_price = 0.0):
        self.balance = balance
        self.crypto = 0.0
        self.fee_rate = fee_rate
        self.trades = []
        self.entry_price = entry_price

    def buy(self,price: float,amount_usdt:float = 100.0):

        fee = amount_usdt * self.fee_rate
        self.balance = self.balance - (amount_usdt + fee)
        crypto_bought = amount_usdt / price
        self.crypto = self.crypto + crypto_bought
        self.entry_price = price


    def sell(self,price): ## price -- рыночная цена монеты на момент продажи
        revenue = self.crypto * price
        fee = revenue * self.fee_rate
        net_payout = revenue - fee
        self.balance = self.balance + net_payout

        profit_percent = ((price - self.entry_price) / self.entry_price) * 100
        self.trades.append(profit_percent)
        self.crypto = 0.0







