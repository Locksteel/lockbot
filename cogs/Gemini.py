import os
from random import choice

from localcmds import printLog

from discord.ext import commands
import google.generativeai as genai

class GeminiCog(commands.Cog, name='Gemini'):
    '''A group of commands accessing twitch.tv'''
    def __init__(self, bot):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        self.personalities = os.listdir('./personalities')
    
    def getResponse(self, prompt, username, personality="chill.txt", randPerson=False):
        '''Returns the Gemini-generated response from passed prompt'''
        intro = ""
        
        if randPerson:
            personality = choice(self.personalities)
        
        with open('personalities/' + personality, 'r') as file:
            intro = file.read().replace('\n', ' ')
        intro += " Everything after this sentence is said by a person whose name is listed before their message.\n\n" + username + ": "
        exit = "\n\nLockBot: "
        
        response = self.model.generate_content(intro + prompt + exit)
        return response.text
    
    @commands.hybrid_command(name='generate',
                             aliases=['gen', 'ai', 'gemini'],
                             brief='Sends AI-generated response to prompt'
                             )
    async def generate(self, ctx,
                   prompt:  str = commands.parameter(description='Prompt to pass to AI'),
                   random: str = commands.parameter(description='True or false, respond as a random personality', default='false')
                   ):
        '''Sends the an AI-generated response to a prompt'''
        rand = False
        if random == "true":
            rand = True
        if not prompt:
            await ctx.send("Prompt is empty.")
        else:
            response = self.getResponse(prompt, ctx.author.name, randPerson=rand)
            await ctx.send(response)
            printLog(ctx)
        
        

async def setup(bot):
    await bot.add_cog(GeminiCog(bot))