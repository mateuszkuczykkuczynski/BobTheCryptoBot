import asyncio
import discord
import discord.ext.test as dpytest
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


async def test_is_bot_connected():
    dpytest.configure(bot)
    await dpytest.message("hello")
    assert dpytest.verify().message().content("hello")

load_dotenv()
bot.run('TESTER_TOKEN')
asyncio.run(test_is_bot_connected())
