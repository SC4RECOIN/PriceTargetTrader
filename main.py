import json
import os
import pandas as pd
from colorama import Fore, Style
from utils.iex import get_price_target, get_price
from utils.broker import AlpacaClient
from utils.storage import PandasStorage, PriceTargetRow
from datetime import datetime
from typing import List
from dataclasses import asdict


# load config
with open("config.json") as f:
    config = json.load(f)
    for key, value in config.items():
        os.environ[key] = str(value)

# stocks universe
stocks_df = pd.read_csv("s&p_500.csv")

alpaca_client = AlpacaClient()
storage = PandasStorage()
target_thresh = float(os.environ["PRICE_TARGET_THRES"])
max_hold = int(os.environ["MAX_HOLD"])

while True:
    # each loop will take a day
    alpaca_client.await_market_open()
    today = datetime.today().strftime("%Y-%m-%d")

    dtbp = alpaca_client.account.daytrading_buying_power
    if float(dtbp) < float(alpaca_client.account.buying_power) * 0.1:
        print(f"{Fore.RED}Insufficient DTBP (${dtbp}){Style.RESET_ALL}")
        alpaca_client.await_market_close(True)
        continue

    new_positions = []
    targets: List[PriceTargetRow] = []

    for idx, stock in enumerate(stocks_df["Symbol"]):
        try:
            pt = get_price_target(stock)
            price = get_price(stock)
            chg = pt.price_target_average / price - 1

            print(
                f"{idx:<5} {stock:<5} - {price:<8}"
                f"{Fore.GREEN if chg > target_thresh else Fore.WHITE}"
                f"target: {pt.price_target_average:<5} -> {chg * 100:.2f}%"
                f"{Style.RESET_ALL}"
            )

            # persist targets later
            targets.append(
                PriceTargetRow(date_fetched=today, current_price=price, **asdict(pt))
            )

            # add to positions if above thesh
            if chg > target_thresh:
                new_positions.append((stock, chg))

        except Exception as e:
            print(f"{Fore.RED}{stock} failed: {e}{Style.RESET_ALL}")

    # sort and limit to max
    new_positions.sort(key=lambda x: x[1], reverse=True)
    new_positions = [pos[0] for pos in new_positions[:max_hold]]

    # enter positions
    print(f"entering {len(new_positions)} new positions")
    alpaca_client.rebalance(new_positions)

    # persist price targets
    storage.insert_price_targets(targets)

    alpaca_client.await_market_close()
