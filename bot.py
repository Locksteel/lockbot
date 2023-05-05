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
intents.members = True

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
    
    # reset all pending flags to false
    for _, dirs, _ in os.walk('serverData'):
        for guildID in dirs:
            for _, _, files in os.walk('serverData/'+guildID):
                for userID in files:
                    with MarriageUser(int(userID[:-5]), guildID) as user:
                        user.setPending(False)
    
    print(f'{bot.user} has connected to Discord!')
    
@bot.event
async def on_guild_join(guild):
    addMarryFile(guild)

bot.run(token)  # run bot