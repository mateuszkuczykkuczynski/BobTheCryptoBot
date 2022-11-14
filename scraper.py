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


def coin_supported_by_bot(coin):
    if coin in db.keys():
        return True
    else:
        return False


print(get_price('bitcoin'))


# Intents declaration
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'You have logged in as {client}')
    channel = discord.utils.find(lambda h: h.name == 'ogólny', client.get_all_channels())

    await client.get_channel(channel.id).send('BobTheBot is ready to use!')


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
        first_allpairs = allpairs[:len(allpairs)//2]
        second_allpairs = allpairs[len(allpairs) // 2:]
        await message.channel.send(first_allpairs)
        await message.channel.send(second_allpairs)

    if message.content.lower() == 'all_crypto':
        await message.channel.send(list(db.keys()))

BOT_TOKEN = 'DISCORD_TOKEN'
client.run(BOT_TOKEN)

