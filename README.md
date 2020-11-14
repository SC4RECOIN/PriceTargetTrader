# Price Target Trader ✨

Holds stocks with price targets above a set threshold. Rebalances everyday at market open.

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

**Requires Python >= 3.7**
