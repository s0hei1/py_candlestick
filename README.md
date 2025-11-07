<img width="1280" height="640" alt="Untitled" src="https://github.com/user-attachments/assets/23226603-89aa-4819-a11b-1e902a5d2da4" />

# 📈 Candlestick Library

Candlestick is a high‑performance, strongly‑typed Python library for working with financial chart data — including candlesticks (OHLCV) and indicators. Designed with flexibility and performance in mind, it integrates seamlessly with Pandas, NumPy, and other data‑science tools.

Whether you're building backtesting engines, streaming chart visualizations, or performing market analysis, **Candlestick** provides a clean, structured, and reliable foundation for managing time‑series financial data.

---

## 🚀 Quick Start


```bash
pip install py_candlestick
```

```python
from py_candlestick import Chart, Candle

candles = [
    Candle(timestamp=1700000000, open=1.2, high=1.3, low=1.1, close=1.25, volume=1500),
    Candle(timestamp=1700000600, open=1.25, high=1.32, low=1.2, close=1.28, volume=2100),
]

chart = Chart(candles)
print(len(chart))               # number of candles
print(chart.to_dataframe())    # convert to Pandas DataFrame
```

---

## 🔥 Key Features

- ✅ Strongly‑typed `Candle` and `Chart` classes
- ✅ Fast NumPy‑backed data operations
- ✅ Easy conversion to/from Pandas DataFrames
- ✅ Built‑in indicator registration
- ✅ CSV and MT5 data import utilities
- ✅ Safe chart updates with sequencing and timestamp validation
- ✅ Convenient Python slicing & iteration

---

## 🕯️ Candle Class

Each candlestick is represented by the immutable `Candle` class:

```python
Candle(
    timestamp: float,
    open: float,
    high: float,
    low: float,
    close: float,
    volume: float
)
```

### Candle Highlights
- Immutable (`frozen=True`)
- Time‑aware with `date_time` property
- Helpers: `is_bullish()`, `is_bearish()`, `is_undecided()`
- Conversions: `as_dict()`, `as_tuple()`, `from_dict()`
- Length (`len(candle)`) equals high‑low range

Example:
```python
c = Candle(timestamp=1700000000, open=1.2, high=1.3, low=1.1, close=1.25, volume=1000)
print(c.is_bullish())  # True
print(c.range_())      # 0.2
```

---

## 📊 Chart Class

`Chart` stores a sequence of candles and optional computed indicators.

### Creating a Chart
```python
chart = Chart(candles)
```

### Converting to DataFrame
```python
df = chart.to_dataframe(include_timeframe=True, include_symbol=True)
```

### Adding Indicators
Indicators are expected to return an `Indicator` object with `name` and NumPy `values`.

```python
def sma_indicator(candles):
    closes = [c.close for c in candles]
    values = np.convolve(closes, np.ones(5)/5, mode='valid')
    return Indicator(name="sma5", values=values)

chart = Chart(candles, indicator_calculators=[sma_indicator])
```

### Chart Updating
`update_chart()` adds only *new* candles (based on timestamp).

```python
chart.update_chart(new_candles)
```

If an update handler is passed:
```python
def on_update(c):
    print("Chart updated!", len(c))

chart = Chart(candles, on_chart_update=on_update)
chart.update_chart(new_candles)
```

---

## 📥 Importing Market Data

### From CSV
```python
chart = Chart.from_csv("data.csv")
```
CSV must contain:
```
timestamp,open,high,low,close,volume
```

### From Pandas DataFrame
```python
chart = Chart.from_pd_dataframe(df)
```

### From MT5 Raw Data
```python
chart = Chart.from_mt5_data(mt5_array, symbol=my_symbol, timeframe=my_tf)
```

---

## 📦 NumPy Integration
Convert to a stacked matrix of series:
```python
arr = chart.to_ndarray()
```

Output shape:
```
(num_candles, num_features)
```
Where features = timestamp, open, high, low, close, volume, + indicators.

---

## 🧩 Slicing & Iteration
```python
first_10 = chart[:10]
last_candle = chart[-1]
for c in chart:
    print(c.close)
```

---

## 🤝 Contributing
Pull requests, issues, and improvements are welcome! The project is designed to be clean, readable, and extensible.

---

## 📄 License
MIT License.

