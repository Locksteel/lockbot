import os
import io
from random import choice

from localcmds import printLog

from discord.ext import commands
import google.generativeai as genai
from PIL import Image

class GeminiCog(commands.Cog, name='Gemini'):
    '''A group of commands accessing twitch.tv'''
    def __init__(self, bot):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        self.personalities = os.listdir('./personalities')
    
    async def getResponse(self, prompt, ctx: commands.Context, personality="default.txt", randPerson=False):
        '''Returns the Gemini-generated response from passed prompt'''
        username = ctx.author.name
        attachments = ctx.message.attachments
        
        attachFlag = attachments and "image" in attachments[0].content_type and attachments[0].size < 10000000
        
        intro = ""
        
        if randPerson:
            personality = choice(self.personalities)
        
        with open('personalities/' + personality, 'r') as file:
            intro = file.read().replace('\n', ' ')
            
        if attachFlag:
            intro += " You will also receive an image that the person you're talking to is giving you."
            
        intro += " Everything after this sentence is said by a person whose name is listed before their message.\n\n" + username + ": "
        exit = "\n\nLockBot: "
        fullPrompt = 0
        
        # if there is an attachment, it is an image, and it is smaller than 10 MB
        if attachFlag:
            buffIO = io.BytesIO(await attachments[0].read())
            buffIO.seek(0)
            
            image = Image.open(buffIO)
            
            fullPrompt = [intro + prompt + exit, image]
        else:
            fullPrompt = intro + prompt + exit
        
        response = self.model.generate_content(fullPrompt)
        return response.text
    
    @commands.hybrid_command(name='generate',
                             aliases=['gen', 'ai', 'gemini'],
                             brief='Sends AI-generated response to prompt'
                             )
    async def generate(self, ctx: commands.Context,
                   prompt:  str = commands.parameter(description='Prompt to pass to AI'),
                   random: bool = commands.parameter(description='True or false, respond as a random personality', default=False)
                   ):
        '''Sends the an AI-generated response to a prompt'''
        if not prompt:
            await ctx.send("Prompt is empty.")
        else:
            response = await self.getResponse(prompt, ctx, randPerson=random)
            await ctx.send(response)
            printLog(ctx)
        
        

async def setup(bot):
    await bot.add_cog(GeminiCog(bot))