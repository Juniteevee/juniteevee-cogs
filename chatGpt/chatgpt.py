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
        config = await this.setCredentials(ctx)

        email = config.get("email")
        password = config.get("password")
        await ctx.send(f"email {email}, password {password}")

    async def setCredentials(self, ctx: commands.Context):
        openAiKeys = await self.bot.get_shared_api_tokens("openai")
        if openAiKeys.get("email") is None or openAiKeys.get("password") is None:
            return await ctx.send("The openai email and password keys have not been set.")
        config =  {
            "email": openAiKeys.get("email"),
            "password": openAiKeys.get("password"), 
        }
        return config


    