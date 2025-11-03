from dataclasses import dataclass
import datetime as dt
from numbers import Number


@dataclass(frozen= True)
class Candle:
    open : float
    high : float
    low : float
    close : float
    timestamp : float

    @property
    def date_time(self):
        return dt.datetime.fromtimestamp(self.timestamp, dt.UTC)

    def is_bearish(self) -> bool:
        return self.open > self.close

    def is_bullish(self) -> bool:
        return self.close > self.open

    def is_undecided(self) -> bool:
        return self.open == self.close

    def _range(self) -> float:
        return self.__len__()

    def candle_body_len(self) -> float:
        return abs(self.open - self.close)

    def to_tuple(self) -> tuple[float, float, float, float, float]:
        return (self.timestamp,self.open, self.high, self.low, self.close)

    def __str__(self):
        return f"datetime: {self.date_time} o: {self.open} h: {self.high} l: {self.low} c: {self.close} "

    def __repr__(self):
        return f'timestamp= {self.timestamp} open= {self.open} high= {self.high} low= {self.low} close= {self.close}\n'

    def __len__(self):
        return self.high - self.low

    def __hash__(self):
        return hash(self.to_tuple())

    def __eq__(self, other):
        return (self.open == other.open and
                self.high == other.high and
                self.low == other.low and
                self.close == other.close and
                self.timestamp == other.timestamp)

    def __dict__(self):
        return {'open': self.open, 'high': self.high, 'low': self.low, 'close': self.close}

    def as_dict(self):
        return self.__dict__()

    @classmethod
    def get_annotations(cls):
        return [i for i in Candle.__annotations__]

    @classmethod
    def from_dict(cls, _dict: dict[str, Number]):
        if not isinstance(_dict, dict):
            raise TypeError("Input must be a dictionary")

        required_keys = {'open', 'high', 'low', 'close', 'timestamp'}
        if set(_dict.keys()) != required_keys:
            raise TypeError(f"Dictionary must contain exactly these keys: {required_keys}")

        for key in ['open', 'high', 'low', 'close']:
            if not isinstance(_dict[key], (int, float)):
                raise TypeError(f"Value for '{key}' must be a number")

        return cls(**_dict)
