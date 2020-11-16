import json
import os
from datetime import datetime
from typing import List
from dataclasses import asdict
import schedule
import time
import pandas as pd
from colorama import Fore, Style
from utils.iex import get_price_target, get_price
from utils.broker import AlpacaClient
from utils.storage import PandasStorage, PriceTargetRow


# load config
with open("config.json") as f:
    config = json.load(f)
    for key, value in config.items():
        os.environ[key] = str(value)

# stock universe
stocks_df = pd.read_csv("data/nas100.csv")
universe = stocks_df["Symbol"]

alpaca_client = AlpacaClient()
storage = PandasStorage()
target_thresh = float(os.environ["PRICE_TARGET_THRES"])
max_hold = int(os.environ["MAX_HOLD"])


def rebalance_task():
    print("rebalance triggered")
    today = datetime.today().strftime("%Y-%m-%d")

    new_positions = []
    targets: List[PriceTargetRow] = []

    for idx, stock in enumerate(universe):
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

    # enter positions once market opens
    alpaca_client.await_market_open()
    print(f"entering {len(new_positions)} new positions")
    alpaca_client.rebalance(new_positions)

    # persist price targets
    storage.insert_price_targets(targets)


# rebalance schedule (calc positions before market open)
schedule.every().monday.at("09:15").do(rebalance_task)

# run rebalance once a week
print("waiting for task trigger")
while True:
    schedule.run_pending()
    time.sleep(60)
