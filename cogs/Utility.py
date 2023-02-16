from discord.ext import commands

class UtilityCog(commands.Cog, name='Utilities'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping',
                      aliases=[],
                      brief='Sends a response message.'
                      )
    async def ping(ctx):
        '''Returns with a message reading "Pong!"'''
        await ctx.send('Pong!')
        
async def setup(bot):
    await bot.add_cog(UtilityCog(bot))