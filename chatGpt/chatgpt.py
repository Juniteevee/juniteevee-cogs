from redbot.core import commands
from redbot.core import Config
import re
import discord
from datetime import datetime
from revChatGPT.revChatGPT import Chatbot

class ChatGpt(commands.Cog):
    """Cog to enable chat powered by OpenAi Chat GPT"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testchat(self, ctx: commands.Context):
        """Test"""
        
        email = await self.bot.get_shared_api_tokens("openai", "email")
        password = await self.bot.get_shared_api_tokens("openai", "password")
        self.config =  {
            "email": email,
            "password": password, 
        }
        await ctx.send(f"email {self.config.email}, password {self.config.password}")

    