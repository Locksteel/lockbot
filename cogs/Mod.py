from localcmds import printLog

from discord.ext import commands
from discord import Member, HTTPException, Forbidden, NotFound

class ModCog(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name='purge',
                             aliases=['p'],
                             brief='Deletes a number of recent messages'
                             )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx,
                    count:  int = commands.parameter(description='Number of messages to remove'),
                    reason: str = commands.parameter(description='Reason for purge', default=None)
                    ):
        try:
            await ctx.channel.purge(limit=count+1, reason=reason)
        except Forbidden:
            await ctx.send('You do not have permission to purge messages in this channel.')
        except HTTPException:
            await ctx.send('Purge failed.')
        printLog(ctx)
        
    @commands.hybrid_command(name='kick',
                             aliases=['k'],
                             brief='Kicks a user',
                             )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx,
                   user:    Member = commands.parameter(description='User to kick'),
                   reason:  str = commands.parameter(description='Reason for kick', default=None)
                   ):
        try:
            await user.kick(reason=reason)
        except Forbidden:
            await ctx.send('You do not have permission to kick this user.')
        except HTTPException:
            await ctx.send('Kick failed.')
        printLog(ctx)
            
    @commands.hybrid_command(name='ban',
                             aliases=['b'],
                             brief='Bans a user',
                             )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx,
                  user:        Member = commands.parameter(description='User to ban'),
                  del_msg_secs:  int = commands.parameter(description='Number of seconds of messages from user to delete', default=None),
                  reason:      str = commands.parameter(description='Reason for ban', default=None)
                   ):
        try:
            await user.ban(delete_message_seconds=del_msg_secs, reason=reason)
        except NotFound:
            await ctx.send('User not found.')
        except Forbidden:
            await ctx.send('You do not have permission to ban this user.')
        except HTTPException:
            await ctx.send('Ban failed.')
        printLog(ctx)
        
    @commands.hybrid_command(name='unban',
                             aliases=['ub'],
                             brief='Unbans a user'
                             )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,
                    user:   Member = commands.parameter(description='User to unban'),
                    reason: str = commands.parameter(description='Reason for unban'), default=None
                    ):
        try:
            await user.unban(reason=reason)
        except NotFound:
            await ctx.send('User not found.')
        except Forbidden:
            await ctx.send('You do not have permission to unban this user.')
        except HTTPException:
            await ctx.send('Unban failed.')
        
async def setup(bot):
    await bot.add_cog(ModCog(bot))