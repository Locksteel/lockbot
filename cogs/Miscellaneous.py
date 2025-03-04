from localcmds import printLog

import discord
from discord.ext import commands

class MiscellaneousCog(commands.Cog, name='Miscellaneous'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        owenId = 263154005104918528
        serverId = 392520528935780353
        # print(f"Message sent by {message.author.id} in {message.guild.id}")
        if message.author.id != owenId or message.guild.id != serverId:
            return
        
        for attachment in message.attachments:
            # print(f"Message attachment {attachment.filename}")
            if attachment.filename == "gayboifarti.mp4":
                count = 0
                with open("serverData/gbf.txt", "r") as file:
                    count = int(file.read().strip())
                
                count += 1
                await message.channel.send(f"Owen has posted {attachment.filename} {count} times.")
                
                with open("serverData/gbf.txt", "w") as file:
                    file.write(str(count))
        
async def setup(bot):
    await bot.add_cog(MiscellaneousCog(bot))