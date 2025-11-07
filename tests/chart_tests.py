from pathlib import Path

import numpy as np
import pandas as pd
from py_candlestick import Chart, ClassicFractalTimeFrames, DefaultSymbols, Candle
from tests.fixtures import candle_dict, candle, candles
import datetime as dt
from more_itertools import last, first

def test_chart_to_dataframe(candles):
    c = Chart(
        candles=candles,
        timeframe=ClassicFractalTimeFrames.H1,
        symbol=DefaultSymbols.AUDUSD
    )

    assert isinstance(c.to_dataframe(), pd.DataFrame)
    assert 'open' in c.to_dataframe().columns
    assert 'close' in c.to_dataframe().columns
    assert 'timestamp' in c.to_dataframe().columns


def test_chart_to_nd_array(candles):
    c = Chart(
        candles=candles,
        timeframe=ClassicFractalTimeFrames.H1,
        symbol=DefaultSymbols.AUDUSD
    )

    arr = c.to_ndarray()

    assert isinstance(arr, np.ndarray)
    assert len(arr) == len(candles)


def test_chart_update(candles):
    chart = Chart(
        candles=candles,
        timeframe=ClassicFractalTimeFrames.H1,
        symbol=DefaultSymbols.AUDUSD
    )

    _candle = Candle(
        timestamp=(dt.datetime.now() + dt.timedelta(days=1)).timestamp(),
        open=1.1,
        high=2.0,
        low=0.5,
        close=1,
        volume=10000,
    )
    new_candles = [_candle]

    chart.update_chart(new_candles)

    assert len(chart) == len(candles) + len(new_candles)
    assert last(chart.candles) == _candle
    assert first(chart.candles).timestamp < last(chart.candles).timestamp

def test_chart_from_df(candles):

    chart = Chart(
        candles=candles,
        timeframe=ClassicFractalTimeFrames.H1,
        symbol=DefaultSymbols.AUDUSD
    )

    df = chart.to_dataframe()

    _chart = Chart.from_pd_dataframe(df, symbol=chart.symbol, timeframe=chart.timeframe)

    assert len(_chart) == len(df)
    assert _chart == chart

def test_chart_from_csv():
    csv_file_path = Path(__file__).parent / 'external_data' / 'exam_df.csv'

    chart = Chart.from_csv(str(csv_file_path))

    assert isinstance(chart, Chart)
