from iexfinance.stocks import Stock
from datetime import datetime
from dataclasses import dataclass
from typing import Union


@dataclass
class PriceTaget:
    symbol: str
    updated_date: datetime
    price_target_average: float
    price_target_high: float
    price_target_low: float
    number_of_analysts: int
    currency: str


def get_price_target(symbol: str) -> Union[PriceTaget, None]:
    try:
        stock = Stock(symbol)
        pt = stock.get_price_target()

        return PriceTaget(
            symbol=pt["symbol"],
            updated_date=datetime.strptime(pt["updatedDate"], "%Y-%m-%d"),
            price_target_average=pt["priceTargetAverage"],
            price_target_high=pt["priceTargetHigh"],
            price_target_low=pt["priceTargetLow"],
            number_of_analysts=pt["numberOfAnalysts"],
            currency=pt["currency"],
        )
    except:
        return None
