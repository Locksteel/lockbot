import os
import random

from discord.ext import commands

import tweepy

class TwitterCog(commands.Cog, name='Twitter'):
    def __init__(self, bot):
        self.bot = bot
        
        self.twitterClient = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

    def getTwitterID(self, username):
        '''Gets the Twitter user ID from a passed username'''
        user = self.twitterClient.get_user(username=username)   # use tweepy get_user to get user info from username
        return user[0]['data']['id']                            # return user id
    
    @commands.command(name='tweet',
                      aliases=['gettweet', 't'],
                      brief='Sends random tweet from user'
                      )
    async def tweet(self, ctx,
                    user:  str = commands.parameter(description='Username of Twitter user to search'),
                    first: int = commands.parameter(description='Number of recent tweets to access', default=100)
                    ):
        '''Sends the link to a random tweet from passed user from a specified set of recent tweets'''
        
        if first > 100:                                     # if passed tweet count is greater than max
            await ctx.send('Maximum tweet search is 100.')  # send message
        else:                                               # else tweet count is valid
            tweets = self.twitterClient.get_users_tweets(   # get user tweets
                id=self.getTwitterID(user),                 # from passed user
                max_results=first,                      # find first passed number
                exclude=['retweets', 'replies']         # only include original tweets
                )
            tweetID = random.choice(tweets[0])['id']                # choose a random tweet id from list
            tweetURL = f'https://vxtwitter.com/x/status/{tweetID}'  # get tweet link from id
            await ctx.send(tweetURL)                                # send tweet link
            
    @commands.command(name='iantweet',
                      aliases=['it', 'ian'],
                      brief='Sends a random tweet from Ian'
                      )
    async def iantweet(self, ctx,
                       first:  int = commands.parameter(description='Number of recent tweets to access', default=100)
                       ):
        '''Sends the link to a random Ian tweet from a specified set of recent tweets (default 100, max 800)'''
        
        await self.tweet(ctx, 'soxeberomon', first)  # reference tweet command with ian username parameter

async def setup(bot):
    await bot.add_cog(TwitterCog(bot))