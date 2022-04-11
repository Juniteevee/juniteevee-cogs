from redbot.core import commands
import discord
from datetime import datetime

class ReactQuote(commands.Cog):
    """Cog to store quotes by reacting with speech bubble"""

    def __init__(self, bot):
        self.bot = bot

    def _wrapQuote(self, msg):
        return msg

    def _buildQuote(self, message:discord.Message):
        
        quote = "Quoted text will be here\n- <@{message.author.display_name}> [(Jump)]({message.jump_url})"
        timestamp = datetime.now()
        embed = discord.Embed(timestamp=timestamp)
        embed.add_field(name="#1", value=quote, inline=False)
        return embed

    @commands.command()
    async def quote(self, ctx: commands.Context):
        """Recall Random Quote"""
        # Your code will go here
        await ctx.send(embed=self._buildQuote(ctx.message))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        """On React"""
        if str(payload.emoji) == '💬':
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user = payload.member
            channel: discord.TextChannel = message.channel
            await channel.send("I'd quote that if I could...")
