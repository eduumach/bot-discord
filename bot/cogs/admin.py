import asyncio
import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            if ctx.author.top_role > member.top_role:
                await member.ban(reason=reason)
                await ctx.send(f'{member.mention} foi banido do servidor.')
            else:
                await ctx.send('Você não tem permissão para banir esse usuário.')
        else:
            await ctx.send('Você não tem permissão para banir membros.')

    @commands.command()
    async def mute(self, ctx, member: discord.Member, mute_time: int):
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

    @commands.command()
    async def limpar(self, ctx, quantidade: int):
        if ctx.message.author.guild_permissions.manage_messages:
            if quantidade <= 0 or quantidade > 100:
                await ctx.send('Por favor, especifique uma quantidade entre 1 e 100.')
            else:
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=quantidade)
                await ctx.send(f'Foram excluídas {len(deleted)} mensagens.', delete_after=5)
        else:
            await ctx.send('Você não tem permissão para usar este comando.')


async def setup(bot):
    await bot.add_cog(Admin(bot))
