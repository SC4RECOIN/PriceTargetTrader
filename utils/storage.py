from abc import ABC, abstractmethod
from colorama import Fore, Style
import pandas as pd
from typing import List
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class PriceTargetRow:
    symbol: str
    updated_date: datetime
    price_target_average: float
    price_target_high: float
    price_target_low: float
    number_of_analysts: int
    currency: str
    date_fetched: datetime
    current_price: float


class Storage(ABC):
    @abstractmethod
    def insert_price_targets(self, targets: List[PriceTargetRow]) -> None:
        pass


class NoStorage(Storage):
    def __init__(self):
        print(
            f"{Fore.RED}WARNING: creating empty storage class.\n"
            f"Implement `utils.Storage` to persist price targets{Style.RESET_ALL}"
        )

    def insert_price_targets(self, targets: List[PriceTargetRow]) -> None:
        pass


class PandasStorage(Storage):
    def __init__(self, save_path="price_targets.csv"):
        self.path = save_path
        self.df = pd.DataFrame()

        if os.path.exists(save_path):
            self.df = pd.read_csv(save_path)

    def insert_price_targets(self, targets: List[PriceTargetRow]) -> None:
        new = pd.DataFrame(targets)
        self.df = self.df.append(new)
        self.df.to_csv(self.path, index=False)
