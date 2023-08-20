import discord
from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
        guild = ctx.guild

        total_members = guild.member_count
        online_members = sum(
            member.status != discord.Status.offline for member in guild.members)

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)

        server_name = guild.name
        server_owner = guild.owner.display_name

        response = f"**Informações do Servidor**\n\n" \
            f"Nome: {server_name}\n" \
            f"Proprietário: {server_owner}\n" \
            f"Membros Totais: {total_members}\n" \
            f"Membros Online: {online_members}\n" \
            f"Canais de Texto: {text_channels}\n" \
            f"Canais de Voz: {voice_channels}"

        await ctx.send(response)


def setup(bot):
    bot.add_cog(Server(bot))
