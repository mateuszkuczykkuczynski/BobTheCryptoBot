import os
import discord
import scraper as sc
from dotenv import load_dotenv


class Client(discord.Client):

    # Intents declaration
    def __init__(self, token: str):
        self._token = token
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    def run(self, *args, **kwargs):
        super().run(self._token)

    @staticmethod
    async def sendMessage(message):
        await discord.utils.find(lambda h: h.name == 'ogólny', Client.get_all_channels()).send(message)

    async def on_ready(self):
        print(f'You have logged in as {self.user}')
        channel = discord.utils.find(lambda h: h.name == 'ogólny', self.get_all_channels())

        sc.db['hitPriceTarget'] = 0
        sc.db['notification'] = []

        await self.get_channel(channel.id).send('BobTheBot is ready to use!')
        await self.get_channel(channel.id).send('Send "i" on chat to get all instructions.')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower() == 'i':
            await message.channel.send('........Instruction........\nSend "check <coin name>" to get coin price, '
                                       'ex. check dogecoin'
                                       '\nSend "all" to get all supported coins with prices.'
                                       '\nSend "all_crypto" to get all supported coins names.'
                                       '\nSend "set <price or prices>" to set price alerts, ex. set 10000 10100 11000'
                                       '\nSend "start" to start tracking coin price, based on price alerts that you '
                                       'set before.')

        if message.content.startswith('hello'):
            await message.channel.send('hello crypto freak!')

        if message.content.startswith('check'):
            checked_coin = message.content.split(' ')[1]
            if checked_coin.lower() in sc.db.keys():
                exisiting_coin = sc.get_price(checked_coin)
                await message.channel.send(f"{exisiting_coin} $")
            else:
                await message.channel.send(f'{checked_coin} is not supported by bot')

        if message.content.lower() == 'all':
            allpairs = list(sc.db.items())
            await message.channel.send(sc.message_split(allpairs)[0])
            await message.channel.send(sc.message_split(allpairs)[1])

        if message.content.lower() == 'all_crypto':
            await message.channel.send(list(sc.db.keys()))

        if message.content.startswith('set'):
            list_from_message = message.content.split(' ')
            chosen_crypto = list_from_message[1]
            user_price_alerts = []

            for price in range(len(list_from_message) - 2):
                try:
                    user_price_alerts.append(int(list_from_message[2 + price]))
                except ValueError:
                    await message.channel.send(
                        f"Price in price alerts must be an integer. Value provided was {list_from_message[2 + price]}")

            if sc.coin_supported_by_bot(chosen_crypto):
                sc.db['selected coin'] = chosen_crypto
                sc.db['alerts provided'] = user_price_alerts
                await message.channel.send(
                    f"You have set price alerts at {sc.db['alerts provided']} for {sc.db['selected coin']}")
            else:
                await message.channel.send("Sorry, provided coin is not supported by Bob.")

        if message.content.startswith('start'):
            await message.channel.send(
                f"You started tracking price of {sc.db['selected coin']} at {sc.db['alerts provided']}")
            await sc.price_detector(sc.db['selected coin'], (sc.db['alerts provided']))


def main():
    load_dotenv()
    client = Client(os.getenv('BOT_TOKEN'))
    client.run()


if __name__ == '__main__':
    main()
