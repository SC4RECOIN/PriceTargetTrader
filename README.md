# Price Target Trader
Hold stocks with price targets above a set threshold and sell when the fall below.

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
This request requires at least a launch account ($20/month) with IEXCloud. Similar data can be found at [finnhub.io](https://finnhub.io/docs/api#price-target) for free, however, I found the IEXCloud data to be more up to date.

## Paper Trading
[Alpaca](https://alpaca.markets/) was chosen as the broker as they are easy to work with and you can open up a paper account without account verification. 


__Requires Python > 3.7__
