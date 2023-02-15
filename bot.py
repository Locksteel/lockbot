import os

import discord
from discord.ext import commands
from discord.voice_client import VoiceClient

from cogs.TwitterCog import TwitterCog

import requests
import random

from dotenv import load_dotenv

load_dotenv()

# Discord API connection
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='~', intents=intents)

@client.event
async def on_ready():
    await client.load_extension("cogs.TwitterCog")
    await client.load_extension("cogs.TwitchCog")
    
    print(f'{client.user} has connected to Discord!')

    
# # Twitch API connection
# twitchAuthURL = 'https://id.twitch.tv/oauth2/token'
# twitchClientID = os.getenv('TWITCH_CLIENT_ID')
# twitchSecret = os.getenv('TWITCH_SECRET')

# twitchAutParams = {'client_id': twitchClientID,
#              'client_secret': twitchSecret,
#              'grant_type': 'client_credentials'}

# autCall = requests.post(url=twitchAuthURL, params=twitchAutParams)
# accessToken = autCall.json()['access_token']
# head = {'Client-ID': twitchClientID,
#         'Authorization': "Bearer " + accessToken}

# def getTwitchID(username):
#     '''Gets the Twitch user ID from a passed username'''
#     req = requests.get(f'https://api.twitch.tv/helix/users?login={username}', headers=head)
#     return req.json()['data'][0]['id']

# # Twitter API connection
# twitterClient = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

# def getTwitterID(username):
#     '''Gets the Twitter user ID from a passed username'''
#     user = twitterClient.get_user(username=username)    # use tweepy get_user to get user info from username
#     return user[0]['data']['id']                        # return user id

# YouTube API connection

    
### Commands

## Utility Commands
@client.command()
async def ping(ctx):
    '''Sends a response message.'''
    await ctx.send('Pong!')

# ## Twitch Commands
# @client.command()
# async def clip(ctx, user, first=100):
#     '''Sends the link to a random Twitch clip from passed user from a specified set of top clips (max/default 100)'''
#     # get twitch api url by referencing getTwitchID function with passed username and first passed number of clips
#     url = f'https://api.twitch.tv/helix/clips?first={first}&broadcaster_id={getTwitchID(user)}'
#     response = requests.get(url, headers=head)  # get api response from url
#     data = response.json()                      # convert response to readable json
#     clip = random.choice(data['data'])          # choose a random clip
#     clipUrl = clip['url']                       # get clip's url
#     await ctx.send(clipUrl)                     # send clip's url
    
# @client.command()
# async def jerma(ctx, first=100):
#     '''Sends the link to a random Jerma985 Twitch clip from a specified set of top clips (max/default 100)'''
#     await clip(ctx, 'jerma985', first)  # reference clip command with jerma username parameter

# ## Twitter Commands
# @client.command()
# async def tweet(ctx, user, first=100):
#     '''Sends the link to a random tweet from passed user from a specified set of recent tweets'''
#     tweets = twitterClient.get_users_tweets(    # get user tweets
#         id=getTwitterID(user),                  # from passed user
#         max_results=first,                      # find first passed number
#         exclude=['retweets', 'replies']         # only include original tweets
#         )
#     tweetID = random.choice(tweets[0])['id']                # choose a random tweet id from list
#     tweetURL = f'https://vxtwitter.com/x/status/{tweetID}'  # get tweet link from id
#     await ctx.send(tweetURL)                                # send tweet link
        
# @client.command()
# async def iantweet(ctx, first=100):
#     '''Sends the link to a random Ian tweet from a specified set of recent tweets (default 100, max 800)'''
#     await tweet(ctx, 'soxeberomon', first)  # reference tweet command with ian username parameter
    
## Voice Chat Commands
@client.command()
async def join(ctx):
    '''Joins the command user's current voice channel'''
    connected = ctx.author.voice
    if connected:                                                   # if user is connected to a voice channel
        await connected.channel.connect()                           # join that voice channel
    else:                                                           # else user is not connected to voice channel
        await ctx.send("You must be connected to a voice channel.") # send message
        
@client.command()
async def leave(ctx):
    '''Leaves the bot's current voice channel'''
    if ctx.voice_client:                                    # if bot is connected to voice channel
        await ctx.guild.voice_client.disconnect()           # disconnect from voice channel
    else:                                                   # else bot is not connected to voice channel
        await ctx.send("Bot is not in a voice channel.")    # send message

client.run(token)   # run bot