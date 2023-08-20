import discord
from discord.ext import commands
from bot.bot import Bot
from bot.config import TOKEN


intents = discord.Intents.all()
bot = Bot(command_prefix='!', intents=intents)


def run():
    bot.run(TOKEN)
