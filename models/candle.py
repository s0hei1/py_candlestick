from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen= True)
class Candle:
    open : float
    high : float
    low : float
    close : float
    datetime : datetime

