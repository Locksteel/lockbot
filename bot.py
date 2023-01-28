import os

import discord
from discord.ext import commands

import tweepy

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
    print(f'{client.user} has connected to Discord!')
    
# Twitch API connection
twitchAuthURL = 'https://id.twitch.tv/oauth2/token'
twitchClientID = os.getenv('TWITCH_CLIENT_ID')
twitchSecret = os.getenv('TWITCH_SECRET')

twitchAutParams = {'client_id': twitchClientID,
             'client_secret': twitchSecret,
             'grant_type': 'client_credentials'}

autCall = requests.post(url=twitchAuthURL, params=twitchAutParams)
accessToken = autCall.json()['access_token']
head = {'Client-ID': twitchClientID,
        'Authorization': "Bearer " + accessToken}

def getTwitchID(username):
    '''Gets the Twitch user ID from a passed username'''
    req = requests.get(f'https://api.twitch.tv/helix/users?login={username}', headers=head)
    return req.json()['data'][0]['id']

# Twitter API connection
twitterClient = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

def getTwitterID(username):
    '''Gets the Twitter user ID from a passed username'''
    user = twitterClient.get_user(username=username)
    return user[0]['data']['id']
    
# Commands
@client.command()
async def ping(ctx):
    '''Sends a response message.'''
    await ctx.send('Pong!')

@client.command()
async def clip(ctx, user, first=100):
    '''Sends the link to a random Twitch clip from passed user from a specified set of top clips (max/default 100)'''
    url = f'https://api.twitch.tv/helix/clips?first={first}&broadcaster_id={getTwitchID(user)}'
    response = requests.get(url, headers=head)
    data = response.json()
    clip = random.choice(data['data'])
    clipUrl = clip['url']
    await ctx.send(clipUrl)
    
@client.command()
async def jerma(ctx, first=100):
    '''Sends the link to a random Jerma985 Twitch clip from a specified set of top clips (max/default 100)'''
    await clip(ctx, 'jerma985', first)

@client.command()
async def tweet(ctx, user, first=100):
    '''Sends the link to a random tweet from passed user from a specified set of recent tweets'''
    tweets = twitterClient.get_users_tweets(id=getTwitterID(user), max_results=first, exclude=['retweets', 'replies'])
    tweetID = random.choice(tweets[0])['id']
    tweetURL = f'https://vxtwitter.com/x/status/{tweetID}'
    await ctx.send(tweetURL)
        
@client.command()
async def iantweet(ctx, first=100):
    '''Sends the link to a random Ian tweet from a specified set of recent tweets (default 100, max 800)'''
    await tweet(ctx, 'soxeberomon', first)

client.run(token)