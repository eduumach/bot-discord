from discord.ext import commands
from config import AUTHORIZED_USERS

def has_permission():
    def predicate(ctx):
        return ctx.author.id in AUTHORIZED_USERS
    return commands.check(predicate)