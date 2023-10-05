from requests import get
from discord.ext import commands
import subprocess
import os


class Mine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mine_start(self, ctx):
        await ctx.send('Iniciando o servidor...')
        caminho_da_pasta = '/home/edu/mine'
        comando = 'screen -dm -S minecraft ~/mine/run.sh'

        os.chdir(caminho_da_pasta)
        subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    
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

    