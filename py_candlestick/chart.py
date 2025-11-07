from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Sequence, Any, Callable, TypeAlias, Iterable, List
import csv
from numpy._typing import NDArray
from py_candlestick.series import Indicator, Series
from py_candlestick.time_frame import TimeFrame
from py_candlestick.symbol import Symbol
from py_candlestick.candle import Candle
import pandas as pd
import numpy as np
from more_itertools import last
import warnings

Candles: TypeAlias = List[Candle]
OnChartUpdate: TypeAlias = Callable[[Candles], Any]
IndicatorCalculator = Callable[[Candles], Indicator]


def candles_to_series(candles: Sequence[Candle]) -> tuple[Series, ...]:
    timestamps = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []

    for candle in candles:
        timestamps.append(candle.timestamp)
        opens.append(candle.open)
        highs.append(candle.high)
        lows.append(candle.low)
        closes.append(candle.close)
        volumes.append(candle.volume)

    return (
        Series(name='timestamp', values=np.array(timestamps)),
        Series(name='open', values=np.array(opens)),
        Series(name='high', values=np.array(highs)),
        Series(name='low', values=np.array(lows)),
        Series(name='close', values=np.array(closes)),
        Series(name='volume', values=np.array(volumes)),
    )


@dataclass(init=False)
class Chart:
    candles: Candles
    indicators: list[Indicator]
    timeframe: TimeFrame | None = None
    symbol: Symbol | None = None
    on_chart_update: OnChartUpdate | None = None

    def __init__(self,
                 candles: Candles,
                 timeframe: TimeFrame | None = None,
                 on_chart_update: OnChartUpdate | None = None,
                 symbol: Symbol | None = None,
                 indicator_calculators: list[IndicatorCalculator] | None = None
                 ):
        self.candles = candles
        self.timeframe = timeframe
        self.on_chart_update = on_chart_update
        self.symbol = symbol
        if indicator_calculators is not None:
            self.indicators = [clc(candles) for clc in indicator_calculators]
        else:
            self.indicators = []

    def add_indicator(self, indicator: Indicator):

        if len(indicator) != len([i for i in self.candles]):
            raise Exception("Length of indicator values must equal with Candles length")

        if hasattr(self, indicator.name):
            raise Exception(f"an indicator with name {indicator.name} is exists")

        setattr(self, indicator.name, indicator.values)

    def to_dataframe(self, include_timeframe: bool = False, include_symbol: bool = False) -> pd.DataFrame:
        series = list(candles_to_series(self.candles)) + self.indicators
        data = np.column_stack([s.values for s in series])
        columns = [s.name for s in series]

        df = pd.DataFrame(
            data=data,
            columns=columns
        )

        if self.timeframe is not None and include_timeframe:
            df['timeframe'] = self.timeframe.name
        elif self.timeframe is None and include_timeframe:
            warnings.warn("the object time frame is none !")

        if self.symbol is not None and include_symbol:
            df['symbol'] = self.symbol.symbol_name
        elif self.symbol is None and include_symbol:
            warnings.warn("the object symbol is none !")

        return df

    def to_ndarray(self, ) -> np.ndarray:
        series = list(candles_to_series(self.candles)) + self.indicators
        return np.column_stack([s.values for s in series])

    def update_chart(self, new_candles: Sequence[Candle]) -> None:
        if not isinstance(new_candles, Sequence):
            raise TypeError("new_candles must be a Sequence")

        if new_candles is None or new_candles == []:
            return None

        candles = list(self.candles)

        last_candle = last(candles)
        new_candles_for_add = [i for i in new_candles if i.date_time > last_candle.date_time]

        if new_candles_for_add == []:
            return None

        new_candles_for_add.sort(key=lambda x: x.timestamp)
        self.candles = self.candles + new_candles_for_add

        self.candles = candles

        if self.on_chart_update is not None:
            self.on_chart_update(self.candles)

    @classmethod
    def from_pd_dataframe(cls,
                          data_frame: pd.DataFrame,
                          timeframe: TimeFrame | None = None,
                          symbol: Symbol | None = None,
                          ) -> Chart:
        candles = []

        for i, row in data_frame.iterrows():
            candle = Candle(
                timestamp=row['timestamp'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume'],
            )
            candles.append(candle)

        return cls(candles, timeframe= timeframe,symbol= symbol)

    @classmethod
    def from_csv(cls, file_path: str,
                 timeframe: TimeFrame | None = None,
                 symbol: Symbol | None = None,
                 ) -> Chart:
        candles = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                timestamp, open_, high, low, close, volume = row

                candle = Candle(
                    open=float(open_),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    timestamp=float(timestamp),
                    volume=float(volume)
                )
                candles.append(candle)
        return cls(candles = candles,timeframe = timeframe, symbol = symbol )

    @classmethod
    def from_mt5_data(cls, data: NDArray[tuple], symbol: Symbol, timeframe: TimeFrame) -> Chart:
        return Chart(
            candles=[Candle(
                timestamp=i[0],
                open=i[1],
                high=i[2],
                low=i[3],
                close=i[4],
                volume=i[5]
            ) for i in data],
            timeframe=timeframe,
            symbol=symbol,
        )

    def __getitem__(self, input: str | slice):
        return self.candles.__getitem__(input)

    def __iter__(self):
        return iter(self.candles)

    def __len__(self):
        return len([i for i in self.candles])

    def __add__(self, other: Chart) -> Chart:
        self.update_chart(other.candles)
        return self

