import discord
from discord.ext import commands
from bot.utils.aut import has_permission
from utils.openia import openia_api, openia_image
from bot.config import EDUARDO_MACHADO


class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permission()
    async def gpt3(self, ctx, *, prompt: str = None):
        if prompt is None:
            await ctx.channel.send('Você precisa me dar um prompt para eu completar.')
            return

        response_text = openia_api(prompt)

        for i in range(0, len(response_text), 2000):
            await ctx.channel.send(response_text[i:i + 2000])

    @commands.command()
    @has_permission()
    async def image(self, ctx, *, prompt: str = None):

        await ctx.send(openia_image(prompt))


def setup(bot):
    bot.add_cog(Gpt(bot))
