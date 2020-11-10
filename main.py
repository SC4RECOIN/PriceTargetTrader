import json
import os
from iex import get_price_target
from broker import AlpacaClient

# load config
with open("config.json") as f:
    config = json.load(f)
    for key, value in config.items():
        os.environ[key] = str(value)

alpaca_client = AlpacaClient()
target_thresh = float(os.environ['PRICE_TARGET_THRES'])
stock_universe = ['AAPL', 'NVDA', 'SNAP', 'SHOP']

while True:
    alpaca_client.await_market_open()

    new_positions = []
    for stock in stock_universe:
        price_target = get_price_target(stock)

        if price_target.price_target_average > target_thresh:
            new_positions.append(stock)

    # enter positions
    alpaca_client.rebalance(new_positions)
    alpaca_client.await_market_close()
