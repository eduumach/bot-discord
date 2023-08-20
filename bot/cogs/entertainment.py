import discord
from discord.ext import commands
import urllib3
from bot.utils.openia import openia_api
import random


class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        await ctx.send(openia_api('Cria uma piada'))

    @commands.command()
    async def gay(self, ctx):
        porcentagem = random.randint(0, 100)
        await ctx.channel.send(f'Você é {porcentagem}% gay!')

    @commands.command()
    async def xinga(self, ctx):
        await ctx.channel.send('Vai tomar no cu, seu filho da puta! @strogonoff01')

    @commands.command()
    async def kick(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            voice_channel = ctx.author.voice.channel
            members = voice_channel.members

            if len(members) > 1:
                member_to_kick = random.choice(members)
                await member_to_kick.move_to(None)
                await ctx.channel.send(f'{member_to_kick.mention} foi kickado da chamada.')
            else:
                await ctx.channel.send('Não há membros suficientes na chamada para usar o comando !kick.')

    @commands.command()
    async def vote(self, ctx, *, question: str):
        message = await ctx.send(f"**Votação:** {question}")
        await message.add_reaction('👍')  # Reação de "sim"
        await message.add_reaction('👎')  # Reação de "não"

    @commands.command()
    async def cumprimentar(self, ctx, member: discord.Member):
        if ctx.author.bot:
            return

        await ctx.send(f'Olá, {member.mention}! Como você está?')

    @commands.command()
    async def abraco(self, ctx, member: discord.Member):
        if not member:
            await ctx.send("Você precisa mencionar um usuário para dar um abraço!")
            return

        # pasta_abracos = 'abracos'
        # arquivos_abracos = os.listdir(pasta_abracos)
        # gif_abraco = random.choice(arquivos_abracos)

        # await ctx.send(f"{ctx.author.mention} deu um abraço em {member.mention}! 🤗",
        #             file=discord.File(os.path.join(pasta_abracos, gif_abraco)))

        await ctx.send(f"{ctx.author.mention} deu um abraço em {member.mention}! 🤗")

    @commands.command()
    async def elogio(self, ctx, user: discord.Member):
        elogio = openia_api("Crie um elogio curto")
        await ctx.send(f"{user.mention}, {elogio}")

    @commands.command()
    async def google(ctx, *, consulta):
        pesquisa = urllib3.parse.quote(consulta)
        url = f'https://www.google.com/search?q={pesquisa}'
        await ctx.send(f'Aqui estão os resultados da pesquisa para "{consulta}": {url}')


async def setup(bot):
    await bot.add_cog(Entertainment(bot))