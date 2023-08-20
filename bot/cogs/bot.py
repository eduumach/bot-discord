import discord
from discord.ext import commands


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        info_text = "Este é um bot Discord com várias funcionalidades interativas. " \
                    "Você pode ganhar moedas virtuais, subir de nível, realizar votações, " \
                    "ouvir piadas, completar frases com a IA da OpenAI e muito mais!"
        await ctx.send(info_text)

    @commands.command()
    async def ajuda(self, ctx):
        help_text = "Lista de comandos disponíveis:\n" \
                    "```\n"

        await ctx.send(help_text)


async def setup(bot):
    await bot.add_cog(Bot(bot))
