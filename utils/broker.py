import alpaca_trade_api as tradeapi
from colorama import Fore, Style
import time
import datetime
from typing import List


class AlpacaClient(object):
    def __init__(self):
        self.api = tradeapi.REST()
        self.account = self.api.get_account()
        self.positions = sorted([p.symbol for p in self.api.list_positions()])

        # close any open orders
        self.api.cancel_all_orders()

    def rebalance(self, symbols: List[str]) -> None:
        self.api.cancel_all_orders()

        # check for any change
        symbols.sort()
        if symbols == self.positions:
            print("No change in positions")
            return

        # sell all positions to rebalance
        print("Closing all positions and rebalancing")
        positions = self.api.list_positions()
        for position in positions:
            side = "sell" if position.side == "long" else "buy"
            qty = abs(float(position.qty))
            self.api.submit_order(position.symbol, qty, side, "market", "day")

        # wait for orders to fill
        time.sleep(5)

        # get updated BP
        self.account = self.api.get_account()
        buying_power = float(self.account.buying_power)

        target_notional = buying_power / len(symbols)

        # enter all positions
        for symbol in symbols:
            quote = self.api.get_last_quote(symbol)
            qty = target_notional // quote.askprice

            if qty == 0:
                print(f"{Fore.RED}WARNING: cannot buy 0 {symbol}{Style.RESET_ALL}")
                continue

            self.api.submit_order(symbol, qty, "buy", "market", "day")

        # wait for orders to fill
        time.sleep(5)
        orders = self.api.list_orders()
        for order in orders:
            if order.qty != order.filled_qty:
                print(
                    f"{Fore.RED}WARNING: Order {order.symbol} ({order.status}) "
                    f"only filled {order.filled_qty} (target {order.qty}){Style.RESET_ALL}"
                )

    def await_market_open(self):
        print("waiting for market open")
        clock = self.api.get_clock()
        opening = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()

        while not clock.is_open:
            clock = self.api.get_clock()
            curr_time = clock.timestamp.replace(
                tzinfo=datetime.timezone.utc
            ).timestamp()
            time_to_open = (opening - curr_time) // 60

            print(f"{time_to_open} minutes until market open")
            time.sleep(300)

        print("market is open")

    def await_market_close(self):
        print("waiting for market close")
        clock = self.api.get_clock()
        close = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()

        while clock.is_open:
            clock = self.api.get_clock()
            curr_time = clock.timestamp.replace(
                tzinfo=datetime.timezone.utc
            ).timestamp()
            time_to_open = (close - curr_time) // 60

            print(f"{time_to_open} minutes until market closes")
            time.sleep(300)

        print("market is closed")
