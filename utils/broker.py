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

        # cap leverage
        self.leverage = 2

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
        self.sell_all_positions()

        # get updated BP (cap to leverage)
        self.account = self.api.get_account()
        buying_power = float(self.account.buying_power)
        buying_power = min(
            float(self.account.cash) * self.leverage,
            buying_power,
            self.account.daytrading_buying_power,
        )

        target_notional = buying_power / len(symbols)

        # enter all positions
        for symbol in symbols:
            try:
                quote = self.api.get_last_quote(symbol)
                qty = target_notional // quote.askprice

                if qty == 0:
                    print(f"{Fore.RED}WARNING: cannot buy 0 {symbol}{Style.RESET_ALL}")
                    continue

                self.api.submit_order(symbol, qty, "buy", "market", "day")
            except Exception as e:
                print(f"{Fore.RED}{symbol} order failed: {e}{Style.RESET_ALL}")

        # wait for orders to fill
        time.sleep(5)
        orders = self.api.list_orders()
        for order in orders:
            if order.qty != order.filled_qty:
                print(
                    f"{Fore.RED}WARNING: Order {order.symbol} ({order.status}) "
                    f"only filled {order.filled_qty} (target {order.qty}){Style.RESET_ALL}"
                )

    def sell_all_positions(self):
        positions = self.api.list_positions()
        for position in positions:
            side = "sell" if position.side == "long" else "buy"
            qty = abs(float(position.qty))
            self.api.submit_order(position.symbol, qty, side, "market", "day")

        # wait for orders to fill
        time.sleep(5)

    def await_market_open(self):
        print("waiting for market open")
        clock = self.api.get_clock()
        opening = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()

        while not clock.is_open:
            curr_time = clock.timestamp.replace(
                tzinfo=datetime.timezone.utc
            ).timestamp()
            time_to_open = (opening - curr_time) // 60

            print(f"{time_to_open} minutes until market open")
            time.sleep(300)
            clock = self.api.get_clock()

        print("market is open")

    def await_market_close(self):
        print("waiting for market close")
        clock = self.api.get_clock()
        close = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
        wait_mins = 5

        while clock.is_open:
            curr_time = clock.timestamp.replace(
                tzinfo=datetime.timezone.utc
            ).timestamp()
            time_to_close = (close - curr_time) // 60

            print(f"{time_to_close} minutes until market closes")
            time.sleep(wait_mins * 60)
            clock = self.api.get_clock()

        print("market is closed")
