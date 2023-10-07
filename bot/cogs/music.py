import discord
from discord.ext import commands
import youtube_dl


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.queue = []
        self.play_next = self.bot.loop.create_task(self.play_music())

    def get_voice(self, ctx):
        if self.voice is None:
            self.voice = ctx.author.voice.channel.connect()
        elif self.voice.channel != ctx.author.voice.channel:
            raise commands.CommandError('Você precisa estar no mesmo canal de voz que o bot.')
        return self.voice

    async def play_music(self):
        while True:
            if self.queue:
                url = self.queue.pop(0)
                voice = self.voice or await self.queue[0].channel.connect()
                with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    voice.play(discord.FFmpegPCMAudio(info['url']))
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=info['title']))
                    while voice.is_playing():
                        await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

    @commands.command()
    async def join(self, ctx):
        self.voice = await self.get_voice(ctx)
        await ctx.send(f'Conectado ao canal de voz {self.voice.channel.name}.')

    @commands.command()
    async def leave(self, ctx):
        if self.voice is not None:
            await self.voice.disconnect()
            self.voice = None
            self.queue = []
            await self.bot.change_presence(activity=None)
            await ctx.send('Desconectado do canal de voz.')
        else:
            await ctx.send('Não estou conectado a nenhum canal de voz.')

    @commands.command()
    async def play(self, ctx, url):
        self.queue.append(await self.bot.fetch_channel(ctx.channel.id).fetch_message(ctx.message.id))
        await ctx.send(f'Adicionado à fila: {url}')

    @commands.command()
    async def skip(self, ctx):
        if self.voice is not None and self.voice.is_playing():
            self.voice.stop()
            await ctx.send('Música pulada.')
        else:
            await ctx.send('Não estou tocando nada no momento.')

    @commands.command()
    async def queue(self, ctx):
        if self.queue:
            queue_list = '\n'.join([f'{i+1}. {msg.content}' for i, msg in enumerate(self.queue)])
            await ctx.send(f'Fila de reprodução:\n{queue_list}')
        else:
            await ctx.send('A fila de reprodução está vazia.')


async def setup(bot):
    await bot.add_cog(Music(bot))