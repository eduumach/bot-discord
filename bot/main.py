# main.py
import discord
from discord.ext import commands
from bot import Bot
from config import TOKEN
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = Bot(command_prefix='!', intents=intents)


def run():
    bot.run(TOKEN)
