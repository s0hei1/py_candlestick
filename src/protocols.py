from typing import runtime_checkable, Protocol

from torch.utils.data import runtime_validation


@runtime_checkable
class RiskManagerProtocol(Protocol):
    def calculate_volume(self, *args, **kwargs) -> float: ...

class StrategyProtocol(Protocol):

    def trade_signal(self,*args, **kwargs) -> 'TradeSignal' | None:...
