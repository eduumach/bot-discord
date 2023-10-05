from requests import get
from discord.ext import commands
import os


class Mine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mine_start(self, ctx):
        await ctx.send('Iniciando o servidor...')
        os.chdir('~/mine')
        os.system("screen -dm -S minecraft ~/mine/run.sh")
        
    
    @commands.command()
    async def mine_ip(self, ctx):
        ip = get('https://api.ipify.org').content.decode('utf8')
        await ctx.send(f'O IP do servidor é: {ip}:25565')
    
    
    @commands.command()
    async def mine_stop(self, ctx):
        await ctx.send('Parando o servidor...')
        os.system("screen -S minecraft -X quit")
    
    
    
async def setup(bot):
    await bot.add_cog(Mine(bot))

    