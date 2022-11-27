from bot_bob import Client
from pycoingecko import CoinGeckoAPI
from sqlitedict import SqliteDict
# from threading import Timer

cg = CoinGeckoAPI()
db = SqliteDict("Crypto.database")


def get_price(coin):
    """Function get data from CoinGecko and store it in our 'db' and return coin price if it exists."""
    data = cg.get_coins_markets('usd')
    for i in range(len(data)):
        db[data[i]['id']] = data[i]['current_price']
    return get_price_helper_function(coin)


def get_price_helper_function(coin):
    if coin in db.keys():
        return db[coin]
    else:
        return None


def message_split(all_pairs):
    """Helper function to split data from db because of discord characters sending limit."""
    first_half = all_pairs[:len(all_pairs) // 2]
    second_half = all_pairs[len(all_pairs) // 2:]

    return first_half, second_half


def coin_supported_by_bot(coin):
    if coin in db.keys():
        return True
    else:
        return False


def trend(start_price, end_price, p_alerts):
    if start_price < end_price:
        return increase_alert(end_price, p_alerts)
    elif start_price == end_price:
        return []
    else:
        return decrease_alert(end_price, p_alerts)


def increase_alert(end_price, p_alerts):
    noti = []
    for price in p_alerts:
        if price <= end_price:
            noti.append(price)
        else:
            continue
    return noti


def decrease_alert(end_price, p_alerts):
    noti = []
    for price in reversed(p_alerts):
        if end_price <= price:
            noti.append(price)
        else:
            continue
    return noti


async def price_detector(coin, price_alerts):
    """
    Litte algorithm function that allows to send message based on price alerts provided by user.
    Function also updates data stored in db based on actual coin price.
    """
    actual_price = get_price(coin)
    if len(trend(db['hitPriceTarget'], actual_price, price_alerts)) != 0:
        if db['notification'] != trend(db['hitPriceTarget'], actual_price, price_alerts):
            # Increasing in value
            if db['hitPriceTarget'] < actual_price:
                for price_alert in list(set(increase_alert(actual_price, price_alerts)) - set(db['notification'])):
                    await Client.sendMessage(
                        f'The price of {coin} has just passed {price_alert} USD. The current price '
                        f'is: {actual_price} USD.')
            # Decreasing in value
            else:
                for price_alert in list(set(db['notification']) - set(decrease_alert(actual_price, price_alerts))):
                    await Client.sendMessage(
                        f'The price of {coin} has just fallen below {price_alert} USD. The current price '
                        f'is: {actual_price} USD.')
        # Update values when actual price of coin is smaller than actual htiPriceTarget value.
        if db['hitPriceTarget'] < actual_price:
            db['notification'] = increase_alert(actual_price, price_alerts)
            db['hitPriceTarget'] = max(increase_alert(actual_price, price_alerts))
        # Update values when actual price of coin is bigger than actual htiPriceTarget value.
        if db['hitPriceTarget'] > actual_price:
            db['notification'] = decrease_alert(actual_price, price_alerts)
            db['hitPriceTarget'] = min(decrease_alert(actual_price, price_alerts))
    else:
        db['hitPriceTarget'] = 0

    # Timer(5.0, await price_detector(coin, price_alerts)).start()
