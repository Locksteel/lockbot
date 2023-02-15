import os

import discord
from discord.ext import commands

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
    await client.load_extension("cogs.VoiceCog")
    
    print(f'{client.user} has connected to Discord!')

## Utility Commands
@client.command()
async def ping(ctx):
    '''Sends a response message.'''
    await ctx.send('Pong!')

client.run(token)   # run bot