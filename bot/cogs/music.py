import discord
from discord.ext import commands
import asyncio
import yt_dlp as youtube_dl

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()
            await ctx.send(f'Conectado ao canal de voz: {voice_channel}')

    @commands.command()
    async def adicionar(self, ctx, url):
        if ctx.author.voice and ctx.author.voice.channel:
            if ctx.guild.id not in self.queue:
                self.queue[ctx.guild.id] = []

            self.queue[ctx.guild.id].append(url)
            await ctx.send(f'Added the song to the queue: {url}')
        else:
            await ctx.send("You must be in a voice channel to use this command!")

    @commands.command()
    async def play(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            if not ctx.guild.voice_client:
                await self.start_playback(ctx)
            else:
                await ctx.send("The bot is already playing music.")
        else:
            await ctx.send("You must be in a voice channel to use this command!")

    @commands.command()
    async def pular(self, ctx):
        if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
            ctx.guild.voice_client.stop()
            await self.play_next(ctx)
        else:
            await ctx.send("Nothing is currently playing!")

    @commands.command()
    async def parar(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
            self.queue[ctx.guild.id] = []
        else:
            await ctx.send("I am not connected to a voice channel!")

    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play command")

    async def play_next(self, ctx):
        if ctx.guild.id in self.queue and self.queue[ctx.guild.id]:
            url = self.queue[ctx.guild.id].pop(0)
            filename = await self.get_filename(url, loop=self.bot.loop)
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(
                filename), after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))

    async def start_playback(self, ctx):
        if not ctx.guild.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()

        await self.play_next(ctx)

    async def get_filename(self, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        return data['url']


def setup(bot):
    bot.add_cog(Music(bot))
