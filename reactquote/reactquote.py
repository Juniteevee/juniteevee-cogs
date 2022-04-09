from redbot.core import commands

class ReactQuote(commands.Cog):
    """Cog to store quotes by reacting with speech bubble"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reactquote(self, ctx):
        """TestCommand"""
        # Your code will go here
        await ctx.send("I can do stuff, really!")