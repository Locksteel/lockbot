import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

from cogs.utils.MarriageUser import MarriageUser

load_dotenv()

# Discord API connection
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='~', intents=intents)

def addMarryFile(guild):
    path = "serverData/" + str(guild.id)
    try:
        os.makedirs(path)
        print("Making dir:" + path)
    except FileExistsError:
        print("Dir " + path + " exists")

@bot.event
async def on_ready():
    for filename in os.listdir('./cogs'):                       # for each file in cogs folder
        if filename.endswith('.py'):                            # if file is a python file
            await bot.load_extension(f'cogs.{filename[:-3]}')   # load that file as a cog
            
    for guild in bot.guilds:
        addMarryFile(guild)
        
    testuser = MarriageUser(123, 364196302822703105)
    testuser2 = MarriageUser(456, 364196302822703105)
    testuser.addPartner(456)
    print(testuser.partners)
    print(testuser2.partners)
    
    print(f'{bot.user} has connected to Discord!')
    
@bot.event
async def on_guild_join(guild):
    addMarryFile(guild)

bot.run(token)  # run bot