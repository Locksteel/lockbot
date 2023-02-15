import os
import random

import discord
from discord.ext import commands

import tweepy

class TwitterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.twitterClient = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    def getTwitterID(self, username):
        '''Gets the Twitter user ID from a passed username'''
        user = self.twitterClient.get_user(username=username)   # use tweepy get_user to get user info from username
        return user[0]['data']['id']                            # return user id
    
    @commands.command()
    async def tweet(self, ctx, user, first=100):
        '''Sends the link to a random tweet from passed user from a specified set of recent tweets'''
        tweets = self.twitterClient.get_users_tweets(    # get user tweets
            id=self.getTwitterID(user),                  # from passed user
            max_results=first,                      # find first passed number
            exclude=['retweets', 'replies']         # only include original tweets
            )
        tweetID = random.choice(tweets[0])['id']                # choose a random tweet id from list
        tweetURL = f'https://vxtwitter.com/x/status/{tweetID}'  # get tweet link from id
        await ctx.send(tweetURL)                                # send tweet link
            
    @commands.command()
    async def iantweet(self, ctx, first=100):
        '''Sends the link to a random Ian tweet from a specified set of recent tweets (default 100, max 800)'''
        await self.tweet(ctx, 'soxeberomon', first)  # reference tweet command with ian username parameter

async def setup(bot):
    await bot.add_cog(TwitterCog(bot))