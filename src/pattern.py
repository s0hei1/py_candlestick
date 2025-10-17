from collections.abc import Iterable
from dataclasses import dataclass
from .symbol import Symbol
from .candle import Candle
from .time_frame import TimeFrame


@dataclass
class Pattern:
    symbol : Symbol
    candles : Iterable[Candle]
    timestamp : TimeFrame

