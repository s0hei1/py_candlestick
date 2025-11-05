import pandas as pd

from src import Chart, ClassicFractalTimeFrames, DefaultSymbols
from tests.fixtures import candle_dict,candle,candles




def test_chart_to_dataframe(candles):

    c = Chart(
        candles = candles,
        timeframe=ClassicFractalTimeFrames.H1,
        symbol=DefaultSymbols.AUDUSD
    )

    assert isinstance(c.to_dataframe(), pd.DataFrame)

    print(c.to_dataframe())
