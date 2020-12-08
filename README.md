# Price Target Trader ✨

Holds stocks with price targets above a set threshold. Rebalances weekly at market open.

## Schedule

The program will rebalance every Monday morning. This can be changed with `schedule.every().monday.at("09:15").do(rebalance_task)` in `main.py` (see [python scheduler](https://pypi.org/project/schedule/)). The rebalance function will wait for the market to open before entering positions the function can be run early to fetch price targets.

## Data Source

Price target data is being pulled from [IEXCloud](https://iexcloud.io/docs/api/#price-target).

```
GET /stock/{symbol}/price-target
```

```json
{
  "symbol": "AAPL",
  "updatedDate": "2019-01-30",
  "priceTargetAverage": 178.59,
  "priceTargetHigh": 245,
  "priceTargetLow": 140,
  "numberOfAnalysts": 34,
  "currency": "USD"
}
```

This request requires at least a launch account (\$20/month) with IEXCloud. Similar data can be found at [finnhub.io](https://finnhub.io/docs/api#price-target) for free, however, I found the IEXCloud data to be more up to date.

## Paper Trading

[Alpaca](https://alpaca.markets/) was chosen as the broker as they are easy to work with and you can open up a paper account without account verification.

### Test Results
2020-11-16 to ?
Benchmark: SPY 360.60

### Config

The config will be loaded as env variables. The IEXCloud and Alpaca SDK will see these variables and use them. Update `config.json` with your keys and change the endpoints if you want to move from paper trading to live. Also, set `PRICE_TARGET_THRES` (how far the average price target is from the current price) and `MAX_HOLD` (the maximum number of positions you can have) to your desired behaviour. The price targets will be sorted and the top n=MAX_HOLD will be taken. There can be less than MAX_HOLD if not enough stocks reach the desired threshold.

```json
{
  "IEX_TOKEN": "iex_key",
  "IEX_API": "https://cloud.iexapis.com/v1/",
  "APCA_API_BASE_URL": "https://paper-api.alpaca.markets",
  "APCA_API_KEY_ID": "alpaca_key",
  "APCA_API_SECRET_KEY": "alpaca_secret",
  "PRICE_TARGET_THRES": 0.1,
  "MAX_HOLD": 20
}
```

### Output

```
...
...
86    SBUX  - 100.82  target: 97.6  -> -3.19%
87    SNPS  - 238.435 target: 263.43 -> 10.48%
88    TMUS  - 132.535 target: 148.75 -> 12.23%
89    TTWO  - 184.86  target: 191.08 -> 3.36%
90    TSLA  - 627.56  target: 375.66 -> -40.14%
91    TXN   - 165.91  target: 158.11 -> -4.70%
92    TCOM  - 33.905  target: 34.1669248 -> 0.77%
93    ULTA  - 271.36  target: 284.42 -> 4.81%
94    VRSN  - 205.9   target: 240.58 -> 16.84%
95    VRSK  - 194.12  target: 206.53 -> 6.39%
96    VRTX  - 226.255 target: 288.44 -> 27.48%
97    WBA   - 41.86   target: 39.83 -> -4.85%
98    WDAY  - 227.405 target: 247.97 -> 9.04%
waiting for market open
market open
entering 10 new positions
Closing all positions and rebalancing
```

**Requires Python >= 3.7**
