# Price Target Trader

Holds stocks with price targets above a set threshold. Rebalances everyday at market open.

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

The config will be loaded as env variables. The IEXCloud and Alpaca SDK will see these variables and use them. Update `config.json` with your keys and change the endpoints if you want to move from paper trading to live.

**Requires Python >= 3.7**
