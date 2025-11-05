from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Sequence, Any, Callable, TypeAlias, Iterable, List
import csv
from numpy._typing import NDArray
from src.series import Indicator, Series
from src.time_frame import TimeFrame
from src.symbol import Symbol
from src.candle import Candle
import pandas as pd
import numpy as np
from more_itertools import last

Candles : TypeAlias = Sequence[Candle]
OnChartUpdate: TypeAlias = Callable[[Candles], Any]
IndicatorCalculator = Callable[[Candles], Indicator]

def candles_to_series(candles : Sequence[Candle]) -> tuple[Series, ...]:
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
        Series(name = 'timestamp', values= np.array(timestamps)),
        Series(name = 'open', values= np.array(opens)),
        Series(name = 'high', values= np.array(highs)),
        Series(name = 'low', values= np.array(lows)),
        Series(name = 'close', values= np.array(closes)),
        Series(name = 'volume', values= np.array(volumes)),
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
                 ):
        self.candles = candles
        self.timeframe = timeframe
        self.on_chart_update = on_chart_update
        self.symbol = symbol
        self.indicators = []

    def add_indicator(self, indicator: Indicator):

        if len(indicator) != len([i for i in self.candles]):
            raise Exception("Length of indicator values must equal with Candles length")

        if hasattr(self, indicator.name):
            raise Exception(f"an indicator with name {indicator.name} is exists")

        setattr(self, indicator.name, indicator.values)

    def to_dataframe(self, include_timeframe : bool = False, include_symbol : bool = False) -> pd.DataFrame:
        series = list(candles_to_series(self.candles)) + self.indicators

        data = [s.values.ravel() for s in series]
        columns = [s.name for s in series]

        print(columns)
        print(len(data[0]))

        return pd.DataFrame(data)

        # df = pd.DataFrame(
        #     data=data,
        #     columns=columns
        # )

        # if include_symbol:
        #     df['symbol'] = self.timeframe.name
        #
        # if include_timeframe:
        #     df['timeframe'] = self.symbol.symbol_name
        #
        #
        # return df

    def to_ndarray(self,) -> np.ndarray:
        data = [candle.as_tuple for candle in self.candles]

        arr = np.array(data + self.indicators, dtype=float)

        return arr

    def update_chart(self, new_candles: Iterable[Candle]) -> None:

        if new_candles is None or new_candles == []:
            return None

        candles = list(self.candles)

        last_candle = last(candles)
        new_candles_for_add = [i for i in new_candles if i.date_time > last_candle.date_time]

        for candle in new_candles_for_add:
            candles.append(candle)

        self.candles = candles

        if self.on_chart_update is not None:
            self.on_chart_update(self.candles)

    @classmethod
    def from_pd_dataframe(cls, data_frame: pd.DataFrame) -> 'Chart':
        candles = []

        for i, row in data_frame.iterrows():
            candle = Candle(
                timestamp=row['timestamp'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
            )
            candles.append(candle)

        return cls(candles)

    @classmethod
    def from_csv(cls, file_path: str) -> Chart:
        candles = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                timestamp, open_, high, low, close = row

                candle = Candle(
                    open=float(open_),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    timestamp=int(timestamp)
                )
                candles.append(candle)
        return cls(candles)

    @classmethod
    def from_mt5_data(cls, data: NDArray[tuple], symbol: Symbol, timeframe: TimeFrame) -> Chart:
        return Chart(
            data=[Candle(
                timestamp=i[0],
                open=i[1],
                high=i[2],
                low=i[3],
                close=i[4]
            ) for i in data],
            timeframe=timeframe,
            symbol=symbol,
        )

    def __getitem__(self, input : str | slice):

        if isinstance(input, str):
            return self.asdict()[input]

        if isinstance(input, slice):
            return self.candles[slice]

    def __iter__(self):
        return iter(self.candles)

    def __len__(self):
        return len([i for i in self.candles])

    def __add__(self, other: Chart) -> Chart:
        self.update_chart(other.candles)
        return self
