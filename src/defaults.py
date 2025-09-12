from enum import Enum
from functools import lru_cache
import MetaTrader5 as mt5
from more_itertools import first
from src.symbol import Symbol
from src.time_frame import TimeFrame

class DefaultTimeFrames(Enum):
    M1 = TimeFrame(name="m1", included_m1=1)
    M5 = TimeFrame(name="m5", included_m1=5)
    M15 = TimeFrame(name="m15", included_m1=15)
    H1 = TimeFrame(name="h1", included_m1=60)
    H2 = TimeFrame(name="h2", included_m1=120)
    H4 = TimeFrame(name="h4", included_m1=240)
    H12 = TimeFrame(name="h12", included_m1=720)
    Daily = TimeFrame(name="daily", included_m1=1440)
    Weekly = TimeFrame(name="weekly", included_m1=10080)
    Monthly = TimeFrame(name="monthly", included_m1 = None)

    @classmethod
    def get_time_frame_by_mt5_value(cls, mt5_value: int) -> 'TimeFrameEnum | None':
        return first([i for i in DefaultTimeFrames if i.value.mt5_value == mt5_value], default=None)

    @classmethod
    def get_time_frame_by_name(self, name: str) -> 'TimeFrameEnum | None':
        return first([i for i in DefaultTimeFrames if i.value.name == name], default=None)

    @classmethod
    def get_time_frame_names(cls):
        return [i.value.name for i in cls]


class DefaultSymbols(Enum):
    eur_usd = Symbol("EUR","USD",0.0001,suffix="b")

    @classmethod
    def get_symbol_by_name(cls, symbol_name : str):
        return first((i.value for i in cls if i.value.symbol_name == symbol_name))

    @classmethod
    def get_symbols_name(cls):
        return [i.value.symbol_name for i in cls]