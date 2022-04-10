from redbot.core import commands
import discord

class ReactQuote(commands.Cog):
    """Cog to store quotes by reacting with speech bubble"""

    def __init__(self, bot):
        self.bot = bot

    def _wrapQuote(self, msg):
        return msg

    @commands.command()
    async def reactquote(self, ctx: commands.Context):
        """TestCommand"""
        # Your code will go here
        await ctx.send("I can do stuff, really!")
        

    @commands.command()
    async def quote(self, ctx: commands.Context):
        """TestCommand"""
        # Your code will go here
        await ctx.send("I can do stuff, really!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        """On React"""
        if str(payload.emoji) == ':speech_ballon:':
            self.bot.say('speech')