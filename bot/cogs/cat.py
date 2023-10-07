import requests
from discord.ext import commands

class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        image_url = data[0]['url']
        await ctx.send(image_url)
        
async def setup(bot):
    await bot.add_cog(Cat(bot))