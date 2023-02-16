from discord.ext import commands

def printLog(ctx):
    print(f'User "{ctx.author}" used command "{ctx.command}"')