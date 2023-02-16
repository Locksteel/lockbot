from discord.ext import commands

class UtilityCog(commands.Cog, name='Utility'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping',
                      aliases=[],
                      brief='Sends a response message.',
                      hidden=True
                      )
    async def ping(self, ctx):
        '''Returns with a message reading "Pong!"'''
        await ctx.send('Pong!')
        
async def setup(bot):
    await bot.add_cog(UtilityCog(bot))