import json
import os
from iex import get_price_target


# load config
with open("config.json") as f:
    config = json.load(f)
    for key, value in config.items():
        os.environ[key] = value

price_taget = get_price_target('AAPL')
print(price_taget)
