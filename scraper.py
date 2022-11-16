from pycoingecko import CoinGeckoAPI
from sqlitedict import SqliteDict
import discord

cg = CoinGeckoAPI()
db = SqliteDict("Crypto.database")


def get_price(coin):
    data = cg.get_coins_markets('usd')
    for i in range(len(data)):
        db[data[i]['id']] = data[i]['current_price']
    if coin in db.keys():
        return db[coin]
    else:
        return None

def is_price_alert_int(prices_list):
    prices_list_2 = [i for i in prices_list if i.isdigit()]
    if prices_list == prices_list_2:
        return True
    else:
        return False


def coin_supported_by_bot(coin):
    if coin in db.keys():
        return True
    else:
        return False


def trend(start_price, end_price):
    if start_price > end_price:
        return decrease_alert(end_price)  # return min value of db['notification'
    elif start_price < end_price:
        return increase_alert(end_price)  # return max value of db['notification'
    else:
        return []  # if start_price == end_price


def increase_alert(end_price, price_alerts):
    noti = []
    for price in price_alerts:
        if end_price >= price:
            noti.append(price)
        else:
            continue
    return noti


def decrease_alert(end_price, price_alerts):
    noti = []
    for price in reversed(price_alerts):
        if end_price <= price:
            noti.append(price)
        else:
            continue
    return noti


def list_check(list1, list2):
    s1 = [list1[index] <= list1[index + 1] for index in range(len(list1) - 1)]
    s2 = [list2[index] <= list2[index + 1] for index in range(len(list1) - 1)]
    print(s1)
    print(s2)
    return all(s1) and all(s2)


async def price_detector(coin, price_alerts):
    actual_price = get_price(coin)

    if db['hitPriceTarget'] not in range(min(actual_price, db['hitPriceTarget']),
                                         max(actual_price, db['hitPriceTarget']) + 1) \
            and min(price_alerts) <= actual_price <= max(price_alerts):
        db['hitPriceTarget'] = 0
    else:
        # Check if there are price Target hits
        if len(trend(db['hitPriceTarget'], actual_price, price_alerts)) != 0:
            if db['notification'] != trend(db['hitPriceTarget'], actual_price, price_alerts):
                # Increasing in value
                if db['hitPriceTarget'] < actual_price:
                    if list_check(increase_alert(db['hitPriceTarget'], actual_price), db['notification']):
                        for price_alert in list(
                                set(increase_alert(db['hitPriceTarget'], actual_price)) - set(db['notification'])):
                            await sendMessage(
                                f'The price of {coin} has just passed {price_alert} USD. The current price is: {actual_price} USD.')
                    else:
                        for price_alert in list(
                                set(increase_alert(db['hitPriceTarget'], actual_price)) - set(db['notification'])):
                            await sendMessage(f'The price of {coin} has just passed {price_alert} USD. The current '
                                              f'price is: {actual_price} USD.')
                elif db['hitPriceTarget'] >= actual_price:
                    if list_check(decrease_alert(db['hitPriceTarget'], actual_price, price_alerts), db['notification']):
                        for price_alert in list(set(db['notification']) - set(
                                decrease_alert(db['hitPriceTarget'], actual_price, price_alerts))):
                            await sendMessage(
                                f'The price of {coin} has just fallen below {price_alert} USD. The current price is: {actual_price} USD.')
                    else:
                        for price_alert in list(set(db['notification']) - set(
                                decrease_alert(db['hitPriceTarget'], actual_price, price_alerts))):
                            await sendMessage(
                                f'The price of {coin} has just fallen below {price_alert} USD. The current price is: {actual_price} USD.')
                else:
                    pass
            if db['hitPriceTarget'] < actual_price:
                db['notification'] = increase_alert(db['hitPriceTarget'], actual_price)
                db['hitPriceTarget'] = max(increase_alert((db['hitPriceTarget']), actual_price))

            if db['hitPriceTarget'] > actual_price:
                db['notification'] = decrease_alert(db['hitPriceTarget'], actual_price, price_alerts)
                db['hitPriceTarget'] = min(decrease_alert((db['hitPriceTarget']), actual_price, price_alerts))
        else:
            db['hitPriceTarget'] = 0


# Intents declaration
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def sendMessage(message):
    await discord.utils.find(lambda h: h.name == 'ogólny', client.get_all_channels()).send(message)


@client.event
async def on_ready():
    print(f'You have logged in as {client}')
    channel = discord.utils.find(lambda h: h.name == 'ogólny', client.get_all_channels())

    await client.get_channel(channel.id).send('BobTheBot is ready to use!')

    db['hitPriceTarget'] = 0
    db['notification'] = []


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('hello')

    if message.content.lower() in db.keys():
        await message.channel.send(get_price(message.content.lower()))

    if coin_supported_by_bot(message.content.lower()):
        await message.channel.send(message.content.lower() + 'is supported by bot')
    else:
        await message.channel.send(message.content.lower() + 'is not supported by bot')

    if message.content.lower() == 'all':
        allpairs = list(db.items())
        first_allpairs = allpairs[:len(allpairs) // 2]
        second_allpairs = allpairs[len(allpairs) // 2:]
        await message.channel.send(first_allpairs)
        await message.channel.send(second_allpairs)

    if message.content.lower() == 'all_crypto':
        await message.channel.send(list(db.keys()))

    if message.content.startswith() == '$set':
        list_from_message = message.content.split(' ')
        chosen_crypto = list_from_message[1]
        user_price_alerts = []
        for price in range(len(list_from_message)):
            user_price_alerts.append(int(list_from_message[2 + price]))

        if coin_supported_by_bot(chosen_crypto) and is_price_alert_int(user_price_alerts):


BOT_TOKEN = 'DISCORD_TOKEN'
client.run(BOT_TOKEN)
