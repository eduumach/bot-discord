import discord
from discord.ext import commands


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        info_text = "Este é um bot Discord com várias funcionalidades interativas. " \
                    "Você pode ganhar moedas virtuais, subir de nível, realizar votações, " \
                    "ouvir piadas, completar frases com a IA da OpenAI e muito mais!"
        await ctx.send(info_text)

    @commands.command()
    async def ajuda(self, ctx):
        help_text = f"Lista de comandos real:\n\n `ban`: Bane um usuário do servidor.\n`limpar`: Limpa uma quantidade de mensagens do chat.\n`mute`: Muta um usuário do servidor.\n`adiciona_audio`: Adiciona um arquivo de áudio ao bot.\n`audio`: Toca um arquivo de áudio adicionado ao bot.\n`ajuda`: Mostra a lista de comandos.\n`info`: Mostra informações sobre o bot.\n`abraco`: Abraça um usuário.\n`cumprimentar`: Cumprimenta um usuário.\n`elogio`: Elogia um usuário.\n`gay`: Mostra a taxa de boiolagem de um usuário.\n`google`: Pesquisa algo no Google.\n`joke`: Conta uma piada.\n`kick`: Expulsa um aleatorio da call.\n`vote`: Inicia uma votação.\n`xinga`: Xinga um usuário.\n`charada`: Conta uma charada.\n`riddle`: Conta uma charada.\n`trivia`: Inicia um jogo de trivia.\n`ping`: Mostra o ping do bot.\n`gpt3`: Completa uma frase com a IA da OpenAI.\n`image`: Completa uma imagem com a IA da OpenAI.\n`adicionar`: Adiciona uma música à fila.\n`join`: Entra na call.\n`parar`: Para de tocar música.\n`pause`: Pausa a música.\n`play`: Toca a música.\n`pular`: Pula a música.\n`resume`: Continua a música.\n`server`: Mostra informações sobre o servidor.\n"
        print('foi')
        await ctx.send(help_text)

        await ctx.send(help_text)


async def setup(bot):
    await bot.add_cog(Bot(bot))
