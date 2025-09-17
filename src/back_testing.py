from dataclasses import dataclass
from src import TimeFrame, Chart
from src.protocols import StrategyProtocol, RiskManagerProtocol


class StaticRiskManager:
    risk_percentage: float
    balance: float
    pip_value_per_lot : float

    def __init__(self, risk_percentage: float, balance: float , pip_value_per_lot):
        self.risk_percentage = risk_percentage
        self.balance = balance
        self.pip_value_per_lot = pip_value_per_lot

    def calculate_volume(self,stop_size : float) -> float:
        risk_amount = self.balance * (self.risk_percentage / 100)

        lot_size = risk_amount / (stop_size * self.pip_value_per_lot)

        return round(lot_size, 2)

@dataclass
class TradeSignal:
    order_type : int
    entry_price : float | None
    stop_loss : float | None
    take_profit : float | None

# class MultiTimeChart:
#     charts : dict[TimeFrame, Chart]

class Backtest:

    def __init__(self, strategy : StrategyProtocol, chart : Chart, risk_manager : RiskManagerProtocol):
        self.strategy = strategy
        self.chart = chart
        self.risk_manager = risk_manager

    def start_test(self):
        for i in self.chart:
            signal = self.strategy.trade_signal(i)




