from redbot.core import commands
import discord
from datetime import datetime

class ReactQuote(commands.Cog):
    """Cog to store quotes by reacting with speech bubble"""

    def __init__(self, bot):
        self.bot = bot

    def _wrapQuote(self, msg):
        return msg

    def _buildQuote(self):
        embed = discord.Embed()
        quote = "Quoted text will be here\n- @Juni [(Jump)](https://discord.com/channels/898593470606889000/929701114641809438/963069688177360927)"
        embed.add_field(name="#1", value=quote, inline=False)
        time = datetime.now()
        footer = "<t:{time}>"
        embed.set_footer(text=footer)
        return embed

    @commands.command()
    async def quote(self, ctx: commands.Context):
        """Recall Random Quote"""
        # Your code will go here
        await ctx.send(embed=self._buildQuote())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        """On React"""
        if str(payload.emoji) == '💬':
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user = payload.member
            channel: discord.TextChannel = message.channel
            await channel.send("I'd quote that if I could...")
