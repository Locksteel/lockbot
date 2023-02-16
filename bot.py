import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

# Discord API connection
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_ready():
    for filename in os.listdir('./cogs'):                       # for each file in cogs folder
        if filename.endswith('.py'):                            # if file is a python file
            await bot.load_extension(f'cogs.{filename[:-3]}')   # load that file as a cog
    
    print(f'{bot.user} has connected to Discord!')

bot.run(token)  # run bot