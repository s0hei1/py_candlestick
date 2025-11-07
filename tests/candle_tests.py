import pytest
from py_candlestick.candle import Candle
from tests.fixtures import candle_dict,candle
import datetime as dt

def test_candle_from_dict_should_return_candle_object(candle_dict : dict):

    candle_ = Candle.from_dict(candle_dict)

    assert isinstance(candle_, Candle)
    assert candle_.open == candle_dict['open']
    assert candle_.close == candle_dict['close']
    assert candle_.high == candle_dict['high']
    assert candle_.low == candle_dict['low']
    assert candle_.timestamp == candle_dict['timestamp']
    assert candle_.volume == candle_dict['volume']

def test_candle_from_dict_should_not_accept_non_strings(candle_dict : dict):
    candle_dict[2] = 2

    pytest.raises(TypeError, Candle.from_dict, candle_dict)


def test_candle_from_dict_should_not_accept_non_required_column_names(candle_dict : dict):\

    assert all([c in ['open', 'high', 'low', 'close', 'timestamp','volume'] for c in candle_dict])


def test_candle_from_dict_should_not_accepts_non_number_values(candle_dict : dict):
    candle_dict['open'] = 'open'

    pytest.raises(TypeError, Candle.from_dict, candle_dict)


def test_candle_is_bearish():

    bearish_candle = Candle(
        timestamp=dt.datetime.now().timestamp(),
        open= 1.5,close = 1.2,high = 2.5,low = 0.5,volume=1000
    )

    assert bearish_candle.is_bearish()

def test_candle_is_bullish():

    bearish_candle = Candle(
        timestamp=dt.datetime.now().timestamp(),
        open= 1.2,close = 1.5,high = 2.5,low = 0.5,volume=1000
    )

    assert bearish_candle.is_bullish()

def test_candle_is_undecided():

    bearish_candle = Candle(
        timestamp=dt.datetime.now().timestamp(),
        open= 1.5,close = 1.5,high = 2.5,low = 0.5,volume=1000
    )

    assert bearish_candle.is_undecided()

def test_candle_range():

    high = 2.5
    low = 0.5
    _range = high - low

    bearish_candle = Candle(
        timestamp=dt.datetime.now().timestamp(),
        open= 1.5,close = 1.5,high = high,low = low,volume=1000
    )

    assert bearish_candle.range_() == _range

def test_candle_body_len():

    open = 2.0
    close = 1.5
    body_range = open - close

    bearish_candle = Candle(
        timestamp=dt.datetime.now().timestamp(),
        open= open,close = close,high = 2.5,low = 0.5,volume=1000
    )

    assert bearish_candle.candle_body_len() == body_range

def test_ground(candle):

    assert True





