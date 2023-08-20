from discord.ext import commands


class ErrorHandlerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(
                "Você não tem permissão para usar este comando, mas se quiser ajudar a pagar, aceitamos doações em "
                "cookies! 🍪\nbitcoin:bc1qr5nkd9d2wxwam8f3ulagajn00zp856vyrrywdt")
        else:
            raise error


async def setup(bot):
    await bot.add_cog(ErrorHandlerCog(bot))
