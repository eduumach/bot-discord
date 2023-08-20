import asyncio
import os
import discord
from discord.ext import commands
from bot.config import AUDIO_PATH


class Audio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def audio(self, ctx, audio: str = None):
        if audio is None:
            await self.show_available_audio(ctx)
        elif not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("Você precisa estar em um canal de voz para usar esse comando.")
        else:
            await self.play_audio(ctx, audio)

    async def show_available_audio(self, ctx):
        audio_files = [file.rstrip('.mp3') for file in os.listdir(
            AUDIO_PATH) if file.endswith('.mp3')]

        audio_list = "\n".join(
            f"{index + 1}. {audio_name.capitalize()}" for index, audio_name in enumerate(audio_files))
        embed = discord.Embed(title="Lista de Áudios Disponíveis", description=audio_list,
                              color=discord.Color.blue())

        await ctx.channel.send(embed=embed)

    async def play_audio(self, ctx, audio):
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        audio = audio.lower()
        audio_file = f'{AUDIO_PATH}/{audio}.mp3'
        
        def after_play(error):
            if error:
                print(f"Error playing {audio}: {error}")
            else:
                print(f"Finished playing {audio}")
        
            asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop)

        ctx.guild.voice_client.play(discord.FFmpegPCMAudio(audio_file), after=after_play)


    @commands.command()
    async def adiciona_audio(self, ctx):
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                await self.save_audio(ctx, attachment)

    async def save_audio(self, ctx, attachment):
        if attachment.filename.endswith('.mp3'):
            if not os.path.exists(AUDIO_PATH):
                print(f"Creating directory {AUDIO_PATH}")
                os.makedirs(AUDIO_PATH)
            save_path = os.path.join(AUDIO_PATH, attachment.filename)
            await attachment.save(save_path)
            await ctx.send(f"Arquivo MP3 '{attachment.filename}' recebido e salvo!")


async def setup(bot):
    await bot.add_cog(Audio(bot))
