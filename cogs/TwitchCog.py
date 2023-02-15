import os
import random

import discord
from discord.ext import commands

import requests

class TwitchCog(commands.Cog):
    def __init__(self, bot):
        self.authURL = 'https://id.twitch.tv/oauth2/token'
        self.clientID = os.getenv('TWITCH_CLIENT_ID')
        self.secret = os.getenv('TWITCH_SECRET')

        self.autParams = {'client_id': self.clientID,
                    'client_secret': self.secret,
                    'grant_type': 'client_credentials'}

        self.autCall = requests.post(url=self.authURL, params=self.autParams)
        self.accessToken = self.autCall.json()['access_token']
        self.head = {'Client-ID': self.clientID,
                'Authorization': "Bearer " + self.accessToken}
        
    def getTwitchID(self, username):
        '''Gets the Twitch user ID from a passed username'''
        req = requests.get(f'https://api.twitch.tv/helix/users?login={username}', headers=self.head)
        return req.json()['data'][0]['id']
    
    @commands.command()
    async def clip(self, ctx, user, first=100):
        '''Sends the link to a random Twitch clip from passed user from a specified set of top clips (max/default 100)'''
        # get twitch api url by referencing getTwitchID function with passed username and first passed number of clips
        url = f'https://api.twitch.tv/helix/clips?first={first}&broadcaster_id={self.getTwitchID(user)}'
        response = requests.get(url, headers=self.head) # get api response from url
        data = response.json()                          # convert response to readable json
        clip = random.choice(data['data'])              # choose a random clip
        clipUrl = clip['url']                           # get clip's url
        await ctx.send(clipUrl)                         # send clip's url
        
    @commands.command()
    async def jerma(self, ctx, first=100):
        '''Sends the link to a random Jerma985 Twitch clip from a specified set of top clips (max/default 100)'''
        await self.clip(ctx, 'jerma985', first)   # reference clip command with jerma username parameter

async def setup(bot):
    await bot.add_cog(TwitchCog(bot))