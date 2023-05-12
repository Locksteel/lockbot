import os
import random

from discord.ext import commands

import requests

class SteamCog(commands.Cog, name='Steam'):
    '''A group of commands accessing Steam's storefront API'''
    def __init__(self, bot):
        self.bot = bot
        
    def getAppDetails(self, gameID, currency='us'):
        url = f'https://store.steampowered.com/api/appdetails?appids={gameID}&cc={currency}'
        response = requests.get(url)
        return response.json()
    
    @commands.hybrid_command(name='steamtitle',
                             aliases=[],
                             brief='Sends the title of a Steam game from ID',
                             hidden=True
                             )
    async def steamtitle(self, ctx, game_id):
        data = self.getAppDetails(game_id)[game_id]
        if data['success']:
            data = data['data']
            
            await ctx.send(data['name'])
        else:
            await ctx.send('Invalid Steam app ID.')
            
    @commands.hybrid_command(name='dealtext',
                             aliases=['steamdeal', 'deal', 'dt'],
                             brief='Sends formatted Steam deal text from ID',
                             hidden=True
                             )
    async def dealtext(self, ctx, game_id):
        data = self.getAppDetails(game_id)[game_id]
        if data['success']:
            data = data['data']
            
            name = data['name']
            discount = data['price_overview']['discount_percent']
            initial = data['price_overview']['initial_formatted']
            final = data['price_overview']['final_formatted']
            gameURL = f'https://store.steampowered.com/app/{game_id}'
            
            message = f'{name} is {discount}% off on Steam\n({initial}→{final})\n{gameURL}'
            await ctx.send(message)
        else:
            await ctx.send('Invalid Steam app ID.')
            

async def setup(bot):
    await bot.add_cog(SteamCog(bot))