from redbot.core import commands
from redbot.core.utils import fileIO
from __main__ import send_cmd_help
import os
from random import choice as randchoice

class ReactQuote(commands.Cog):
    """Cog to store quotes by reacting with speech bubble"""

    def __init__(self, bot):
        self.bot = bot
        self.quotes = fileIO("data/quotes/quotes.json", "load")

    def _wrapQuote(self, msg):
        return msg

    @commands.command()
    async def reactquote(self, ctx):
        """TestCommand"""
        # Your code will go here
        await ctx.send("I can do stuff, really!")

    @commands.command()
    async def addquote(self, *message):
        """Manually Add Quote"""
        self.bot.say(message)