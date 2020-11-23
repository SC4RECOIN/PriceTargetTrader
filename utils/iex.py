from iexfinance.stocks import Stock
from datetime import datetime
from dataclasses import dataclass
from typing import Union


@dataclass
class PriceTarget:
    symbol: str
    updated_date: datetime
    price_target_average: float
    price_target_high: float
    price_target_low: float
    number_of_analysts: int
    currency: str


def get_price_target(symbol: str) -> Union[PriceTarget, None]:
    try:
        stock = Stock(symbol)
        pt = stock.get_price_target()

        # https://iexcloud.io/docs/api/#currency-conversion
        if pt["currency"] == "CNY":
            pt["currency"] = "USD"
            pt["priceTargetAverage"] = pt["priceTargetAverage"] * 0.15188
            pt["priceTargetHigh"] = pt["priceTargetHigh"] * 0.15188
            pt["priceTargetLow"] = pt["priceTargetLow"] * 0.15188

        return PriceTarget(
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


def get_price(symbol: str) -> float:
    stock = Stock(symbol)
    return stock.get_price()
