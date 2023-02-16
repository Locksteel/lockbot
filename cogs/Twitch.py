import os
import random

from commands import printLog

from discord.ext import commands

import requests

class TwitchCog(commands.Cog, name='Twitch'):
    '''A group of commands accessing twitch.tv'''
    def __init__(self, bot):
        self.bot = bot
        
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
    
    @commands.command(name='clip',
                      aliases=['twitchclip', 'c'],
                      brief='Sends random Twitch clip from user'
                      )
    async def clip(self, ctx,
                   username:   str = commands.parameter(description='Username of Twitch user to search'),
                   first:      int = commands.parameter(description='Number of top clips to access', default=100)
                   ):
        '''Sends the link to a random twitch.tv clip from passed user from a specified set of top clips'''
        
        if first > 100:                                     # if passed clip count is greater than max
            await ctx.send('Maximum clip search is 100.')   # send message
        else:                                               # else clip count is valid
            # get twitch api url by referencing getTwitchID function with passed username and first passed number of clips
            url = f'https://api.twitch.tv/helix/clips?first={first}&broadcaster_id={self.getTwitchID(username)}'
            response = requests.get(url, headers=self.head) # get api response from url
            data = response.json()                          # convert response to readable json
            clip = random.choice(data['data'])              # choose a random clip
            clipUrl = clip['url']                           # get clip's url
            await ctx.send(clipUrl)                         # send clip's url
            printLog(ctx)
        
    @commands.command(name='jerma',
                      aliases=['jerma985'],
                      brief='Sends random Twitch clip from Jerma985'
                      )
    async def jerma(self, ctx,
                    first: int = commands.parameter(default=100, description='Number of top clips to access')
                    ):
        '''Sends the link to a random Jerma985 twitch.tv clip from a specified set of top clips'''
        
        await self.clip(ctx, 'jerma985', first)   # reference clip command with jerma username parameter

async def setup(bot):
    await bot.add_cog(TwitchCog(bot))