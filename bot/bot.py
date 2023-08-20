import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_extension('cogs.general')
        self.load_extension('cogs.admin')
        self.load_extension('cogs.bot')
        self.load_extension('cogs.entertainment')
        self.load_extension('cogs.error_handler')
        self.load_extension('cogs.games')
        self.load_extension('cogs.general')
        self.load_extension('cogs.gpt')
        self.load_extension('cogs.music')
        self.load_extension('cogs.server')
        self.load_extension('cogs.audio')

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
