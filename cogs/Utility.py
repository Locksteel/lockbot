from localcmds import printLog

from discord.ext import commands

class UtilityCog(commands.Cog, name='Utility'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='ping',
                             aliases=[],
                             brief='Sends a response message.',
                             hidden=True
                             )
    async def ping(self, ctx):
        '''Returns with a message reading "Pong!"'''
        await ctx.send('Pong!')
        printLog(ctx)
        
    @commands.hybrid_command(name='author',
                             aliases=[],
                             brief='Pings the author of command',
                             hidden=True
                             )
    async def author(self, ctx):
        '''Returns with a message pinging the author of the command'''
        await ctx.send(ctx.author.mention)
        
async def setup(bot):
    await bot.add_cog(UtilityCog(bot))