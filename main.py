import json
import os
import pandas as pd
from iex import get_price_target, get_price
from broker import AlpacaClient

# load config
with open("config.json") as f:
    config = json.load(f)
    for key, value in config.items():
        os.environ[key] = str(value)

# stocks universe
stocks_df = pd.read_csv("s&p_500.csv")

alpaca_client = AlpacaClient()
target_thresh = float(os.environ["PRICE_TARGET_THRES"])

while True:
    alpaca_client.await_market_open()

    new_positions = []
    for stock in stocks_df["Symbol"]:
        try:
            pt = get_price_target(stock)
            price = get_price(stock)
            chg = pt.price_target_average / price - 1

            if pt is not None and chg > target_thresh:
                new_positions.append(stock)
        except Exception as e:
            print(f"{stock} failed: {e}")

    # enter positions
    alpaca_client.rebalance(new_positions)
    alpaca_client.await_market_close()
