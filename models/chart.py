from dataclasses import dataclass
from typing import Sequence
from typing import ForwardRef
from models.candle import Candle
import pandas as pd
import csv
from datetime import datetime



@dataclass
class Chart:
    candles : Sequence[Candle]
    time_frame : str | None = None
    _indicators : dict | None = None

    def __getitem__(self, item):
        return self.candles[item]

    def __iter__(self):
        return iter(self.candles)

    def add_indicator(self, indicator_name ,indicator):
        self._indicators[indicator_name] = indicator


    @classmethod
    def from_pd_dataframe(cls, data_frame : pd.DataFrame, time_frame : str) -> 'Chart':
        candles = []

        for i, row in data_frame.iterrows():
            candle = Candle(
                open= row['Open'],
                high= row['High'],
                low= row['Low'],
                close= row['Close'],
            )
            candles.append(candle)

        return cls(candles)

    @classmethod
    def from_csv(cls, file_path: str) -> 'Chart':
        candles = []
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                open_, high, low, close, dt_str = row

                candle = Candle(
                    open=float(open_),
                    high=float(high),
                    low=float(low),
                    close=float(close),
                    datetime=datetime.fromisoformat(dt_str)
                )
                candles.append(candle)
        return cls(candles)

    #
    # def _repr_html_(self):
    #     import pandas as pd
    #     df = pd.DataFrame([c.__dict__() for c in self.candles])
    #     return df._repr_html_()