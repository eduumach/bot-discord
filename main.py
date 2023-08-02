import asyncio
import difflib
import json
import os
import random
import requests
import urllib.parse

import discord
import openai
import yt_dlp as youtube_dl
from discord.ext import commands
from dotenv import load_dotenv
from unidecode import unidecode

from arquivos import EDUARDO_MACHADO, EDUARDO_KESLER

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_KEY = os.environ['OPENAI_KEY']
XP_FILE = 'xp_data.json'
COINS_FILE = 'coins_data.json'
MAX_COINS = 9999
initial_coins_gain_rate = 0.5
coins_decrease_rate = 0.02

openai.api_key = OPENAI_KEY

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

levels = {}
coins = {}

youtube_dl.utils.bug_reports_message = lambda: ''

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
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}


def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)


def calculate_rates():
    total_coins = sum(coins.values())
    coins_gain_rate = initial_coins_gain_rate * (1 - total_coins / MAX_COINS)
    return coins_gain_rate


def get_richest_users():
    sorted_users = sorted(coins.items(), key=lambda x: x[1], reverse=True)
    return sorted_users


def get_exchange_rate():
    response = requests.get("https://api.frankfurter.app/latest?to=USD,BRL")
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["rates"]["BRL"]
        return exchange_rate
    else:
        return None


def calculate_scarcity_rate():
    total_coins = sum(coins.values())
    scarcity_rate = 1 - total_coins / MAX_COINS
    return scarcity_rate


def update_coins(user: discord.User, amount: int):
    user_id = str(user.id)
    if user_id not in coins:
        coins[user_id] = 0

    if coins[user_id] + amount <= MAX_COINS:
        coins[user_id] += amount
    else:
        coins[user_id] = MAX_COINS

    save_data(coins, COINS_FILE)


def load_user_data():
    global levels, coins
    levels = load_data(XP_FILE)
    coins = load_data(COINS_FILE)


def save_user_data():
    save_data(levels, XP_FILE)
    save_data(coins, COINS_FILE)


def openia_api(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": prompt}],
    )
    return response.choices[0].message.content


async def handle_question(ctx, question_type):
    question_types = {
        "trivia": "pergunta",
        "charada": "pergunta",
        "riddle": "pergunta"
    }

    prompt = f'Cria uma pergunta de {question_type}, você me responde nesse formato: {{\n"pergunta": "string",\n"resposta": "string"\n}}'

    question_data = json.loads(openia_api(prompt))
    await ctx.send(f'{question_type.capitalize()}: {question_data[question_types[question_type]]}')

    def verificar_resposta(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        resposta = await bot.wait_for('message', check=verificar_resposta, timeout=30)

        resposta_mensagem = unidecode(resposta.content).lower().strip()
        resposta_certa = unidecode(question_data["resposta"]).lower().strip()

        similaridade = difflib.SequenceMatcher(None, resposta_mensagem, resposta_certa).ratio()

        limite_similaridade = 0.8

        if similaridade >= limite_similaridade:
            moedas = calculate_rates()
            update_coins(ctx.author, moedas)
            await ctx.send(f'Parabéns, você acertou a {question_type}! Você ganhou {moedas} coins!')
        else:
            await ctx.send(f'Infelizmente, você errou! A resposta correta era: {question_data["resposta"]}')
    except asyncio.TimeoutError:
        await ctx.send('Tempo esgotado! Você não respondeu a tempo.')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    load_user_data()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    if user_id not in levels:
        levels[user_id] = 0

    if user_id not in coins:
        coins[user_id] = 0

    xp_gain_rate = len(message.content) / 100

    if random.random() < 0.7:
        coins_gained = random.randint(1, 3) * calculate_rates()
        levels[user_id] += xp_gain_rate
        update_coins(message.author, coins_gained)

        if levels[user_id] % 10 == 0:
            await message.channel.send(
                f"{message.author.mention} subiu para o nível {levels[user_id] // 10}!")

        save_user_data()

    await bot.process_commands(message)


@bot.command()
async def joke(ctx):
    await ctx.send(openia_api('Cria uma piada'))


@bot.command()
async def level(ctx):
    if str(ctx.author.id) in levels:
        current_level = levels[str(ctx.author.id)] // 10
        await ctx.send(f"{ctx.author.mention}, você está no nível {current_level}!")
    else:
        await ctx.send(f"{ctx.author.mention}, você ainda não tem XP!")


@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    server_name = server.name
    member_count = server.member_count
    await ctx.send(f"Nome do servidor: {server_name}\nMembros: {member_count}")


@bot.command()
async def gay(ctx):
    porcentagem = random.randint(0, 100)
    await ctx.channel.send(f'Você é {porcentagem}% gay!')


@bot.command()
async def xinga(ctx):
    await ctx.channel.send('Vai tomar no cu, seu filho da puta! @strogonoff01')


@bot.command()
async def kick(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        members = voice_channel.members

        if ctx.author.id == EDUARDO_KESLER:
            member_to_kick = ctx.author
            await member_to_kick.move_to(None)
            await ctx.channel.send(f'{member_to_kick.mention} foi kickado da chamada. KKKKKKKKKKKKKKK')
        elif len(members) > 1:
            member_to_kick = random.choice(members)
            await member_to_kick.move_to(None)
            await ctx.channel.send(f'{member_to_kick.mention} foi kickado da chamada.')
        else:
            await ctx.channel.send('Não há membros suficientes na chamada para usar o comando !kick.')


@bot.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel

        voice_client = await voice_channel.connect()
        await ctx.send(f'Conectado ao canal de voz: {voice_channel}')


@bot.command()
async def leave(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Desconectado do canal de voz.')


@bot.command()
async def play(ctx, audio: str = None):
    if audio is None:
        audio_files = [file.rstrip('.mp3') for file in os.listdir('audios') if file.endswith('.mp3')]

        audio_list = "\n".join(
            f"{index + 1}. {audio_name.capitalize()}" for index, audio_name in enumerate(audio_files))
        embed = discord.Embed(title="Lista de Áudios Disponíveis", description=audio_list,
                              color=discord.Color.blue())

        await ctx.channel.send(embed=embed)
        return

    if ctx.guild.voice_client:
        if ctx.author.voice and ctx.author.voice.channel:
            audio = audio.lower()
            audio_file = f'audios/{audio}.mp3'

            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(audio_file), after=lambda e: print('done', e))


@bot.command()
async def gpt3(ctx, *, prompt: str = None):
    if ctx.author.id != EDUARDO_MACHADO:
        await ctx.channel.send('Você não tem permissão para usar esse comando. Ou quer ajudar a pagar a conta?')
        return

    if prompt is None:
        await ctx.channel.send('Você precisa me dar um prompt para eu completar.')
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": prompt}],
    )

    response_text = response.choices[0].message.content

    for i in range(0, len(response_text), 2000):
        await ctx.channel.send(response_text[i:i + 2000])


@bot.command()
async def coin(ctx):
    if str(ctx.author.id) in coins:
        total_coins = coins[str(ctx.author.id)]
        await ctx.send(f"{ctx.author.mention}, você possui {total_coins} moedas!")
    else:
        await ctx.send(f"{ctx.author.mention}, você ainda não possui moedas!")


@bot.command()
async def transfer(ctx, recipient: discord.Member, amount: float):
    if str(ctx.author.id) in coins and coins[str(ctx.author.id)] >= amount:
        if str(recipient.id) == str(ctx.author.id):
            await ctx.send("Você não pode transferir moedas para si mesmo!")
            return

        coins[str(ctx.author.id)] -= amount
        coins[str(recipient.id)] = coins.get(str(recipient.id), 0) + amount
        save_data(coins, COINS_FILE)
        await ctx.send(f"{ctx.author.mention}, você transferiu {amount} moedas para {recipient.mention}!")
    else:
        await ctx.send(f"{ctx.author.mention}, você não tem moedas suficientes para transferir {amount} moedas!")


@bot.command()
async def vote(ctx, *, question: str):
    message = await ctx.send(f"**Votação:** {question}")
    await message.add_reaction('👍')  # Reação de "sim"
    await message.add_reaction('👎')  # Reação de "não"


@bot.command()
async def aposta(ctx, quantidade: float):
    user_id = str(ctx.author.id)
    if user_id not in coins:
        coins[user_id] = 0

    if quantidade <= 0:
        await ctx.send("A aposta precisa ser maior que zero.")
        return

    if quantidade > coins[user_id]:
        await ctx.send("Você não tem moedas suficientes para fazer essa aposta.")
        return

    if random.random() < 0.25:
        coins_ganhas = quantidade
        coins[user_id] += coins_ganhas
        await ctx.send(f"{ctx.author.mention}, você ganhou {coins_ganhas} moedas na aposta!")
    else:
        coins_perdidas = quantidade
        coins[user_id] -= coins_perdidas
        await ctx.send(f"{ctx.author.mention}, você perdeu {coins_perdidas} moedas na aposta.")

    save_data(coins, COINS_FILE)


@bot.command()
async def ranking(ctx):
    richest_users = get_richest_users()
    rank_message = "Ranking dos Usuários Mais Ricos:\n"
    for i, (user_id, coins_amount) in enumerate(richest_users, start=1):
        user = bot.get_user(int(user_id))
        user_name = user.name if user else "Usuário Desconhecido"
        rank_message += f"{i}. {user_name}: {coins_amount} moedas\n"

    await ctx.send(rank_message)


@bot.command()
async def escassez(ctx):
    scarcity_rate = calculate_scarcity_rate()
    real_value = 1.0 / scarcity_rate  # Inverso da taxa de escassez
    exchange_rate = get_exchange_rate()

    if exchange_rate is not None:
        real_to_brl = real_value / exchange_rate
        await ctx.send(f"A relação da moeda fictícia com o real é de {real_to_brl} reais por moeda fictícia.")
    else:
        await ctx.send("Não foi possível obter a taxa de câmbio do dólar em relação ao real.")


@bot.command()
async def adivinhar_numero(ctx, aposta: float, numero: int):
    if aposta <= 0.0:
        await ctx.send("A aposta deve ser maior que zero.")
        return

    if coins[str(ctx.author.id)] < aposta:
        await ctx.send("Você não tem moedas suficientes para fazer essa aposta.")
        return

    coins[str(ctx.author.id)] -= aposta
    numero_aleatorio = random.randint(1, 100)
    if numero == numero_aleatorio:
        coins_gained = aposta * 5
        coins[str(ctx.author.id)] += coins_gained
        await ctx.send(f"Parabéns! Você acertou o número e ganhou {coins_gained} moedas.")
    else:
        await ctx.send(f"Que pena! O número era {numero_aleatorio}. Você perdeu sua aposta de {aposta} moedas.")

    save_data(coins, COINS_FILE)


@bot.command()
async def server(ctx):
    guild = ctx.guild

    total_members = guild.member_count
    online_members = sum(member.status != discord.Status.offline for member in guild.members)

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


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        if ctx.author.top_role > member.top_role:
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} foi banido do servidor.')
        else:
            await ctx.send('Você não tem permissão para banir esse usuário.')
    else:
        await ctx.send('Você não tem permissão para banir membros.')


@bot.command()
async def mute(ctx, member: discord.Member, mute_time: int):
    if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.mute_members:
        if not member.guild_permissions.administrator:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                return await ctx.send(
                    "A role 'Muted' não foi encontrada. Crie a role ou verifique se o nome está correto.")

            await member.add_roles(muted_role)
            await ctx.send(f"{member.mention} foi mutado por {mute_time} segundos.")

            await asyncio.sleep(mute_time)
            await member.remove_roles(muted_role)
            await ctx.send(f"{member.mention} não está mais mutado.")
        else:
            await ctx.send("Não é possível mutar um administrador.")
    else:
        await ctx.send("Você não tem permissão para usar esse comando.")


@bot.command()
async def limpar(ctx, quantidade: int):
    if ctx.message.author.guild_permissions.manage_messages:
        if quantidade <= 0 or quantidade > 100:
            await ctx.send('Por favor, especifique uma quantidade entre 1 e 100.')
        else:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=quantidade)
            await ctx.send(f'Foram excluídas {len(deleted)} mensagens.', delete_after=5)
    else:
        await ctx.send('Você não tem permissão para usar este comando.')


@bot.command()
async def google(ctx, *, consulta):
    pesquisa = urllib.parse.quote(consulta)
    url = f'https://www.google.com/search?q={pesquisa}'
    await ctx.send(f'Aqui estão os resultados da pesquisa para "{consulta}": {url}')


@bot.command()
async def trivia(ctx):
    await handle_question(ctx, "trivia")


@bot.command()
async def charada(ctx):
    await handle_question(ctx, "charada")


@bot.command()
async def riddle(ctx):
    await handle_question(ctx, "riddle")


@bot.command()
async def cumprimentar(ctx, member: discord.Member):
    if ctx.author.bot:
        return

    await ctx.send(f'Olá, {member.mention}! Como você está?')


@bot.command()
async def abraco(ctx, member: discord.Member):
    if not member:
        await ctx.send("Você precisa mencionar um usuário para dar um abraço!")
        return

    pasta_abracos = 'abracos'
    arquivos_abracos = os.listdir(pasta_abracos)
    gif_abraco = random.choice(arquivos_abracos)

    await ctx.send(f"{ctx.author.mention} deu um abraço em {member.mention}! 🤗",
                   file=discord.File(os.path.join(pasta_abracos, gif_abraco)))


@bot.command()
async def elogio(ctx, user: discord.Member):
    elogio = openia_api("Crie um elogio curto")
    await ctx.send(f"{user.mention}, {elogio}")


@bot.command()
async def reproduzir_url(ctx, url):
    if ctx.guild.voice_client:
        if ctx.author.voice and ctx.author.voice.channel:
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(filename), after=lambda e: print('done', e))


@bot.command()
async def info(ctx):
    info_text = "Este é um bot Discord com várias funcionalidades interativas. " \
                "Você pode ganhar moedas virtuais, subir de nível, realizar votações, " \
                "ouvir piadas, completar frases com a IA da OpenAI e muito mais!"
    await ctx.send(info_text)


@bot.command()
async def ajuda(ctx):
    help_text = "Lista de comandos disponíveis:\n" \
                "`!coin`: Mostra a quantidade de moedas virtuais que você possui.\n" \
                "`!vote pergunta`: Inicie uma votação com reações de 'sim' e 'não'.\n" \
                "`!info`: Exibe informações sobre o bot.\n" \
                "`!level`: Mostra o seu nível baseado na quantidade de mensagens enviadas.\n" \
                "`!joke`: Receba uma piada ou curiosidade aleatória.\n" \
                "`!gpt3 frase`: Completa a frase usando a IA da OpenAI.\n" \
                "`!play`: Toca um áudio.\n" \
                "`!join`: Entra no canal de voz.\n" \
                "`!leave`: Sai do canal de voz.\n" \
                "`!kick`: Kicka um membro aleatório do canal de voz.\n" \
                "`!transfer @usuario quantidade`: Transfere moedas para outro membro.\n" \
                "`!aposta quantidade`: Aposte moedas e ganhe mais moedas.\n" \
                "`!ranking`: Exibe o ranking dos usuários mais ricos.\n" \
                "`!escassez`: Exibe a relação da moeda fictícia com o dólar e com o real.\n" \
                "`!adivinhar_numero aposta numero`: Tente adivinhar um número de 1 a 100.\n" \
                "`!server`: Exibe informações sobre o servidor.\n" \
                "`!ban @usuario`: Bane um usuário do servidor.\n" \
                "`!mute @usuario tempo`: Muta um usuário por um determinado tempo.\n" \
                "`!limpar quantidade`: Limpa uma quantidade de mensagens do chat.\n" \
                "`!google consulta`: Pesquisa no Google.\n" \
                "`!trivia`: Inicia um jogo de perguntas e respostas.\n" \
                "`!charada`: Inicia um jogo de charadas.\n" \
                "`!riddle`: Inicia um jogo de enigmas.\n" \
                "`!cumprimentar @usuario`: Cumprimenta um usuário.\n" \
                "`!abraco @usuario`: Dá um abraço em um usuário.\n" \
                "`!elogio @usuario`: Elogia um usuário.\n" \
                "`!reproduzir_url url`: Reproduz uma música a partir de uma URL.\n" \
                "`!ajuda`: Exibe esta mensagem de ajuda."

    await ctx.send(help_text)


bot.run(TOKEN)
