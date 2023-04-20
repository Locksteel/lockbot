from localcmds import printLog

from discord.ext import commands
from discord import Member, HTTPException, Forbidden, NotFound

import wikipedia

class WikiCog(commands.Cog, name='Wikipedia'):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
        
async def setup(bot):
    await bot.add_cog(WikiCog(bot))