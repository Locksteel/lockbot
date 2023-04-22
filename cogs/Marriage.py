from discord.ext import commands

class MarriageCog(commands.Cog, name='Marriage'):
    def __init__(self, bot):
        self.bot = bot
        
        
    
    

async def setup(bot):
    await bot.add_cog(MarriageCog(bot))