import pytest
import random
import datetime as dt
from src import Candle

@pytest.fixture
def sample_df(df_size=200):
    timestamp = [
        int(
            (dt.datetime.now() - dt.timedelta(minutes=i)).timestamp()
        )
        for i in range(df_size, 0, -1)
    ]
    highs = [round(random.uniform(0.9, 1), 4) for _ in range(df_size)]
    lows = [round(random.uniform(0.5, 0.6), 4) for _ in range(df_size)]
    opens = [round(random.uniform(0.6, 0.9), 4) for _ in range(df_size)]
    closes = [round(random.uniform(0.6, 0.9), 4) for _ in range(df_size)]

@pytest.fixture
def candle_dict():

    return {
        "timestamp": dt.datetime.now().timestamp(),
        'open' : round(random.uniform(0.9, 1), 4),
        'close': round(random.uniform(0.9, 1), 4),
        'high' : round(random.uniform(0.9, 1), 4),
        'low' : round(random.uniform(0.9, 1), 4),
        'volume' : random.randint(1000,2000),
    }

@pytest.fixture
def candle(candle_dict):

    return Candle.from_dict(candle_dict)

@pytest.fixture
def candles(candle_dict):

    return [Candle.from_dict(candle_dict) for _ in range(10)]
