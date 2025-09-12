from dataclasses import dataclass
from typing import Sequence

from src import Symbol, Candle, TimeFrame


@dataclass
class Pattern:
    symbol : Symbol
    candles : Sequence[Candle]
    timestamp : TimeFrame

