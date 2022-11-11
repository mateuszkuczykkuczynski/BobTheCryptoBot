from pycoingecko import CoinGeckoAPI
from sqlitedict import SqliteDict

db = SqliteDict("Crypto.database")
cg = CoinGeckoAPI()


def get_price(currency):
    data = cg.get_coins_markets(currency)
    print(data[0]['id'])
    print(data[0]['current_price'])

