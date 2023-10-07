from requests import get
from discord.ext import commands
import discord
import subprocess
import os


class Mine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mine_mods_start(self, ctx):
        await ctx.send('Iniciando o servidor mods...')
        caminho_da_pasta = '/home/edu/mine'
        comando = 'screen -dm -S minecraft ~/mines/mods/run.sh'

        os.system("screen -S minecraft -X quit")
        os.chdir(caminho_da_pasta)
        subprocess.run(comando, shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @commands.command()
    async def mine_atm_start(self, ctx):
        await ctx.send('Iniciando o servidor ATM...')
        caminho_da_pasta = '/home/edu/mine'
        comando = 'screen -dm -S minecraft ~/mines/atm/startserver.sh'

        os.system("screen -S minecraft -X quit")
        os.chdir(caminho_da_pasta)
        subprocess.run(comando, shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @commands.command()
    async def mine_ip(self, ctx):
        ip = get('https://api.ipify.org').content.decode('utf8')
        await ctx.send(f'O IP do servidor é: {ip}:25565')

    @commands.command()
    async def mine_stop(self, ctx):
        await ctx.send('Parando o servidor...')
        os.system("screen -S minecraft -X quit")

    @commands.command()
    async def ajuda_mine(self, ctx):
        embed = discord.Embed(title="Comandos do Servidor de Minecraft", description="Lista de comandos do servidor de Minecraft",
                              color=discord.Color.blue())
        embed.add_field(name="!mine_mods_start",
                        value="Inicia o servidor de mods", inline=False)
        embed.add_field(name="!mine_atm_start",
                        value="Inicia o servidor ATM", inline=False)
        embed.add_field(name="!mine_ip",
                        value="Mostra o IP do servidor", inline=False)
        # embed.add_field(name="!mine_stop", value="Para o servidor", inline=False)
        embed.add_field(name="!ajuda_mine",
                        value="Mostra essa mensagem", inline=False)
        await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Mine(bot))
