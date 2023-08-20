import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        await self.load_extension('bot.cogs.general')
        await self.load_extension('bot.cogs.admin')
        await self.load_extension('bot.cogs.bot')
        await self.load_extension('bot.cogs.entertainment')
        await self.load_extension('bot.cogs.error_handler')
        await self.load_extension('bot.cogs.games')
        await self.load_extension('bot.cogs.gpt')
        await self.load_extension('bot.cogs.music')
        await self.load_extension('bot.cogs.server')
        await self.load_extension('bot.cogs.audio')
        print(f'We have logged in as {self.user}')
