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

def check_folder():
    if not os.path.exists("data/reactquote"):
        print("Creating data/reactquote folder...")
        os.makedirs("data/reactquote")


def check_file(self):
    quotes = {}

    f = "data/reactquote/reactquote.json"
    if not fileIO(f, "check"):
        print("Creating default reactquote's reactquote.json...")
        fileIO(f, "save", quotes)


def setup(bot):
    check_folder()
    check_file()
    n = ReactQuote(bot)
    bot.add_cog(n)