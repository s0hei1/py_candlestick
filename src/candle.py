from dataclasses import dataclass, asdict, astuple
import datetime as dt
from numbers import Number

@dataclass(frozen= True,)
class Candle:
    timestamp : float
    open : float
    high : float
    low : float
    close : float
    volume : float

    @property
    def date_time(self):
        return dt.datetime.fromtimestamp(self.timestamp, dt.UTC)

    def is_bearish(self) -> bool:
        return self.open > self.close

    def is_bullish(self) -> bool:
        return self.close > self.open

    def is_undecided(self) -> bool:
        return self.open == self.close

    def range_(self) -> float:
        return self.__len__()

    def candle_body_len(self) -> float:
        return abs(self.open - self.close)

    def as_tuple(self) -> tuple[float, float, float, float, float,float]:
        return astuple(self)

    def as_dict(self) -> dict[str, float]:
        return asdict(self)

    def __len__(self):
        return self.high - self.low

    def __hash__(self):
        return hash(self.to_tuple())

    def __eq__(self, other):
        return (
                self.open == other.open and
                self.high == other.high and
                self.low == other.low and
                self.close == other.close
        )

    def __ne__(self, other):
        return not __eq__(self)

    @classmethod
    def get_annotations(cls):
        return [i for i in Candle.__annotations__]

    @classmethod
    def from_dict(cls, _dict: dict[str, Number]):
        if not isinstance(_dict, dict):
            raise TypeError("Input must be a dictionary")

        required_keys = {'open', 'high', 'low', 'close', 'timestamp','volume'}
        if set(_dict.keys()) != required_keys:
            raise TypeError(f"Dictionary must contain exactly these keys: {required_keys}")

        for key in ['open', 'high', 'low', 'close','volume']:
            if not isinstance(_dict[key], (int, float)):
                raise TypeError(f"Values for '{key}' must be a number")

        return cls(**_dict)
