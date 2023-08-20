import discord
from discord.ext import commands
from unidecode import unidecode
import json
from utils.openia import openia_api
import asyncio
import difflib


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def handle_question(self, ctx, question_type):
        question_type_map = {
            "trivia": "pergunta",
            "charada": "pergunta",
            "riddle": "pergunta"
        }

        question_prompt = f'Cria uma pergunta de {question_type}, você me responde nesse formato: {{\n"pergunta": "string",\n"resposta": "string"\n}}'

        question_data = json.loads(openia_api(question_prompt))
        question_content = question_data.get(question_type_map[question_type])

        await ctx.send(f'{question_type.capitalize()}: {question_content}')

        def check_response(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            response = await self.bot.wait_for('message', check=check_response, timeout=30)

            user_answer = unidecode(response.content).lower().strip()
            correct_answer = unidecode(
                question_data["resposta"]).lower().strip()

            similarity_ratio = difflib.SequenceMatcher(
                None, user_answer, correct_answer).ratio()

            similarity_threshold = 0.8

            if similarity_ratio >= similarity_threshold:
                await ctx.send(f'Parabéns, você acertou a {question_type}!')
            else:
                await ctx.send(f'Infelizmente, você errou! A resposta correta era: {question_data["resposta"]}')
        except asyncio.TimeoutError:
            await ctx.send('Tempo esgotado! Você não respondeu a tempo.')

    @commands.command()
    async def trivia(self, ctx):
        await self.handle_question(ctx, "trivia")

    @commands.command()
    async def charada(self, ctx):
        await self.handle_question(ctx, "charada")

    @commands.command()
    async def riddle(self, ctx):
        await self.handle_question(ctx, "riddle")


def setup(bot):
    bot.add_cog(Games(bot))
