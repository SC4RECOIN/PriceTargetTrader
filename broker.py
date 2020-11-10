import alpaca_trade_api as tradeapi
import time
import datetime
from typing import List


class AlpacaClient(object):
    def __init__(self):
        self.api = tradeapi.REST()
        self.account = self.api.get_account()
        self.positions = sorted([p.symbol for p in self.api.list_positions()])

        # close any open orders
        for order in self.api.list_orders(status="open"):
            self.api.cancel_order(order.id)

    def rebalance(self, symbols: List[str]) -> None:
        # check for any change
        symbols.sort()
        if symbols == self.positions:
            print("No change in positions")
            return

        # sell all positions to rebalance
        print("Closing all positions and rebalancing")
        positions = self.api.list_positions()
        for position in positions:
            side = 'sell' if position.side == 'long' else 'buy'
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
            self.api.submit_order(symbol, qty, "buy", "market", "day")

        # wait for orders to fill
        time.sleep(5)
        orders = self.api.list_orders()
        for order in orders:
            if order.qty != order.filled_qty:
                print(f"WARNING: Order {order.symbol} ({order.status}) "
                      f"only filled {order.filled_qty} (target {order.qty})")
        

    def await_market_open(self):
        print("waiting for market open")
        clock = self.api.get_clock()
        opening = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()

        while not clock.is_open:
            clock = self.api.get_clock()
            curr_time = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            time_to_open = (opening - curr_time) // 60

            print(f"{time_to_open} minutes til market open")
            time.sleep(300)

        print("market is open")