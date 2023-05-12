from cogs.utils.MarriageUser import MarriageUser

import discord
from discord.ext import commands
import os

# TO DO:
# Add proper command permissions
# Make response reply to original command

class MarriageCog(commands.Cog, name='Marriage'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name='marry',
                             aliases=['propose', 'm'],
                             brief='Propose to another user'
                             )
    async def marry(self, ctx,
                    target: discord.Member = commands.parameter(description='User to propose to')
                    ):
        '''Sends a proposal to another user'''
        
        with MarriageUser(ctx.author.id, ctx.guild.id) as authorUser:
            if authorUser.get(target.id, ctx.guild.id).pending:
                await ctx.send("That user has pending request. Please wait to make another.")
            elif ctx.author.id == target.id:                            # if sender targeted themself
                await ctx.send("You can't marry yourself.")
            elif target.id in authorUser.partners:                      # if sender is already married to target
                await ctx.send("You are already married to that user.")
            elif target.bot:                                            # if target is a bot user
                if self.bot.user and target.id == self.bot.user.id:     # if target is this bot
                    await ctx.send("As attractive as I am, I'm already taken by the game. 🎮😎🖕")
                else:
                    await ctx.send("That is a bot you disgusting mechanophile.")
            else:                                                       # else target is valid
                msg = await ctx.send(f'{target.mention}, {ctx.author.mention} would like to marry you. Do you accept?')
                    
                await msg.add_reaction('❤️')
                await msg.add_reaction('💔')
                
                def check(reaction, user):
                    return user.id == target.id and \
                        reaction.message.channel.id == ctx.channel.id and \
                        str(reaction.emoji) in ['❤️', '💔']
                
                try:
                    authorUser.setOtherPending(target.id, True)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except TimeoutError:
                    await ctx.send('Proposal timed out.')
                else:
                    if str(reaction.emoji) == '❤️':
                        # marry success
                        authorUser.addPartner(target.id)
                        # with MarriageUser(ctx.author.id, ctx.guild.id) as u:
                        #     u.addPartner(target.id)
                        
                        await ctx.send(f'{ctx.author.mention} and {target.mention} are now married. Congratulations!')
                    elif str(reaction.emoji) == '💔':
                        # marry fail
                        await ctx.send(f'Unfortunately {target.mention} is not interested.')
                # remove reactions after command conclusion
                await msg.remove_reaction('❤️', self.bot.user)
                await msg.remove_reaction('💔', self.bot.user)
                
                authorUser.setOtherPending(target.id, False)    # reset pending flag
            
    @commands.hybrid_command(name='adopt',
                             aliases=['a'],
                             brief='Request to adopt a user'
                             )
    async def adopt(self, ctx,
                    target: discord.Member = commands.parameter(description='User to adopt')
                    ):
        '''Sends an adoption request to another user'''
        
        with MarriageUser(ctx.author.id, ctx.guild.id) as authorUser:
            if authorUser.get(target.id, ctx.guild.id).pending:
                await ctx.send("That user has pending request. Please wait to make another.")
            elif ctx.author.id == target.id:                            # if sender targeted themself
                await ctx.send("You can't adopt yourself.")
            elif target.id in authorUser.children:                      # if sender was already adopted by target
                await ctx.send("That user is already your child.")
            elif target.bot:                                            # if target is a bot user
                if self.bot.user and target.id == self.bot.user.id:     # if target is this bot
                    await ctx.send("I have a father, his name is <@262860459244388352>.")
                else:
                    await ctx.send("Bots have no feelings and cannot have parents.")
            else:                                                       # else target is valid
                msg = await ctx.send(f'{target.mention}, {ctx.author.mention} would like to adopt you. Do you accept?')
                
                await msg.add_reaction('❤️')
                await msg.add_reaction('💔')
                
                def check(reaction, user):
                    return user.id == target.id and \
                        reaction.message.channel.id == ctx.channel.id and \
                        str(reaction.emoji) in ['❤️', '💔']
                
                try:
                    authorUser.setOtherPending(target.id, True)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except TimeoutError:
                    await ctx.send('Adoption timed out.')
                else:
                    if str(reaction.emoji) == '❤️':
                        # adoption success
                        authorUser.addChild(target.id)
                        
                        await ctx.send(f'{ctx.author.mention} has adopted {target.mention}. Congratulations!')
                    elif str(reaction.emoji) == '💔':
                        # adoption fail
                        await ctx.send(f'Unfortunately {target.mention} is not interested.')
                # remove reactions after command conclusion
                await msg.remove_reaction('❤️', self.bot.user)
                await msg.remove_reaction('💔', self.bot.user)
                        
                authorUser.setOtherPending(target.id, False)    # reset pending flag
                
    @commands.hybrid_command(name='divorce',
                             aliases=['dv'],
                             brief='Divorces a user'
                             )
    async def divorce(self, ctx,
                      target: discord.Member = commands.parameter(description='User to divorce')
                      ):
        '''Divorces another user you are married to'''
        
        with MarriageUser(ctx.author.id, ctx.guild.id) as authorUser:
            if authorUser.pending:
                await ctx.send("You have a pending request. Please complete it to make another.")
            elif ctx.author.id == target.id:                              # if sender targeted themself
                await ctx.send("You can't divorce yourself.")
            elif target.id not in authorUser.partners:                  # if sender is not married to target
                await ctx.send("You are not married to that user.")
            else:                                                       # else target is valid
                msg = await ctx.send(f'Are you sure you would like to divorce {target.mention}?')
                
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                
                def check(reaction, user):
                    return user.id == ctx.author.id and \
                        reaction.message.channel.id == ctx.channel.id and \
                        str(reaction.emoji) in ['✅', '❌']
                        
                try:
                    authorUser.setPending(True)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except TimeoutError:
                    await ctx.send('Divorce timed out.')
                else:
                    if str(reaction.emoji) == '✅':
                        # divorce success
                        authorUser.removePartner(target.id)
                        
                        await ctx.send(f'Sorry {target.mention}, {ctx.author.mention} left you and took the kids.')
                    elif str(reaction.emoji) == '❌':
                        # divorce fail
                        await ctx.send('Divorce cancelled.')
                # remove reactions after command conclusion
                await msg.remove_reaction('✅', self.bot.user)
                await msg.remove_reaction('❌', self.bot.user)
                
                authorUser.setPending(False)    # reset pending flag
    
    @commands.hybrid_command(name='disown',
                             aliases=['do'],
                             brief='Disowns a child'
                             )
    async def disown(self, ctx,
                     target: discord.Member = commands.parameter(description='Child to disown')
                     ):
        '''Disowns one of your children'''
        
        with MarriageUser(ctx.author.id, ctx.guild.id) as authorUser:
            if authorUser.pending:
                await ctx.send("You have a pending request. Please complete it to make another.")
            elif ctx.author.id == target.id:                              # if sender targeted themself
                await ctx.send("You can't disown yourself.")
            elif target.id not in authorUser.children:                  # if target is not a child of sender
                await ctx.send("That user is not your child.")
            else:                                                       # else target is valid
                msg = await ctx.send(f'Are you sure you would like to disown your child {target.mention}?')
                
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                
                def check(reaction, user):
                    return user.id == ctx.author.id and \
                        reaction.message.channel.id == ctx.channel.id and \
                        str(reaction.emoji) in ['✅', '❌']
                        
                try:
                    authorUser.setPending(True)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except TimeoutError:
                    await ctx.send('Disown timed out.')
                else:
                    if str(reaction.emoji) == '✅':
                        # disown success
                        authorUser.removeChild(target.id)
                        
                        await ctx.send(f'Sorry {target.mention}, {ctx.author.mention} no longer cares about you.')
                    elif str(reaction.emoji) == '❌':
                        await ctx.send('Disown cancelled.')
                # remove reactions after command conclusion
                await msg.remove_reaction('✅', self.bot.user)
                await msg.remove_reaction('❌', self.bot.user)
                
                authorUser.setPending(False)    # reset pending flag
    
    @commands.hybrid_command(name='cps',
                             aliases=[],
                             brief='Disowns a parent'
                             )
    async def cps(self, ctx,
                  target: discord.Member = commands.parameter(description='Parent to disown')
                  ):
        '''Disowns one of your parents'''
        
        with MarriageUser(ctx.author.id, ctx.guild.id) as authorUser:
            if authorUser.pending:
                await ctx.send("You have a pending request. Please complete it to make another.")
            elif ctx.author.id == target.id:                              # if sender targeted themself
                await ctx.send("You can't disown yourself.")
            elif target.id not in authorUser.parents:                   # if target is not a child of sender
                await ctx.send("That user is not your parent.")
            else:
                msg = await ctx.send(f'Are you sure you would like to disown your parent {target.mention}')
                
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                
                def check(reaction, user):
                    return user.id == ctx.author.id and \
                        reaction.message.channel.id == ctx.channel.id and \
                        str(reaction.emoji) in ['✅', '❌']
                
                try:
                    authorUser.setPending(True)
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except TimeoutError:
                    await ctx.send('Disown timed out.')
                else:
                    if str(reaction.emoji) == '✅':
                        # disown success
                        authorUser.removeParent(target.id)
                        
                        await ctx.send(f'Sorry {target.mention}, you are no longer the boss of {ctx.author.mention}.')
                    elif str(reaction.emoji) == '❌':
                        await ctx.send('Disown cancelled.')
                # remove reactions after command conclusion
                await msg.remove_reaction('✅', self.bot.user)
                await msg.remove_reaction('❌', self.bot.user)
                
                authorUser.setPending(False)    # reset pending flag
                
    @commands.hybrid_command(name='family',
                             aliases=['f'],
                             brief='List a user\'s family'
                             )
    async def family(self, ctx,
                     target: discord.Member = commands.parameter(description='User to list family of', default=None)
                     ):
        '''Lists the family of you or a mentioned user'''
        
        if target is None: target = ctx.author
        
        with MarriageUser(target.id, ctx.guild.id) as user:
            print(user.id + ' fetched')
            if user.parents or user.children or user.partners:
                parentsStr = ''
                childrenStr = ''
                partnersStr = ''
                
                for parentID in user.parents:
                    parent = await ctx.guild.fetch_member(parentID)
                    parentsStr += str(parent.nick) + '\n'
                for childID in user.children:
                    print('made it to children loop')
                    child = await ctx.guild.fetch_member(childID)
                    childrenStr += str(child.nick) + '\n'
                for partnerID in user.partners:
                    partner = await ctx.guild.fetch_member(partnerID)
                    partnersStr += str(partner.nick) + '\n'
                    
                embed = discord.Embed(title=f'{target.nick}\'s Family')
                
                if parentsStr:  embed.add_field(name='Parents', value=parentsStr, inline=False)
                if childrenStr: embed.add_field(name='Children', value=childrenStr, inline=False)
                if partnersStr: embed.add_field(name='Partners', value=partnersStr, inline=False)
                
                await ctx.send(embed=embed)
            else:
                ctx.send('You have no family. 😞')
            

async def setup(bot):
    await bot.add_cog(MarriageCog(bot))