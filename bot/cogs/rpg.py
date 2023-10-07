import random
from discord.ext import commands


class Rpg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Formato inválido. Use o formato `!roll <n>d<m>`.')
            return

        if rolls > 100 or limit > 1000:
            await ctx.send('Não é possível rolar mais de 100 dados ou dados com mais de 1000 lados.')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)


async def setup(bot):
    await bot.add_cog(Rpg(bot))