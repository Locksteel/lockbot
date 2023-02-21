from localcmds import printLog

from discord.ext import commands
from discord.voice_client import VoiceClient

class VoiceCog(commands.Cog, name='Voice'):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='join',
                      aliases=[],
                      brief='Joins voice channel'
                      )
    async def join(self, ctx):
        '''Joins the command user's current voice channel'''
        connected = ctx.author.voice
        if connected:                                                   # if user is connected to a voice channel
            await connected.channel.connect()                           # join that voice channel
            printLog(ctx)
        else:                                                           # else user is not connected to voice channel
            await ctx.send("You must be connected to a voice channel.") # send message
            
    @commands.command(name='leave',
                      aliases=[],
                      brief='Leaves voice channel'
                      )
    async def leave(self, ctx):
        '''Leaves the bot's current voice channel'''
        if ctx.voice_client:                                    # if bot is connected to voice channel
            await ctx.guild.voice_client.disconnect()           # disconnect from voice channel
            printLog(ctx)
        else:                                                   # else bot is not connected to voice channel
            await ctx.send("Bot is not in a voice channel.")    # send message
            
async def setup(bot):
    await bot.add_cog(VoiceCog(bot))