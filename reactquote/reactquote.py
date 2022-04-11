from redbot.core import commands
from redbot.core import Config
from random import randrange
import discord
from datetime import datetime

class ReactQuote(commands.Cog):
    """Cog to store quotes by reacting with speech bubble"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=8368710483)
        default_guild = {
            "quotes": []
        }
        self.config.register_guild(**default_guild)

    async def _addQuote(self, msg:discord.Message):
        formattedMsg = {
            "channelId": msg.channel.id,
            "messageId": msg.id,
            "authorId": msg.author.id
        }
        guild_group = self.config.guild(msg.guild)
        quotes = await guild_group.quotes()
        if quotes.count(formattedMsg) > 0:
            return -1
        else:
            quotes.append(formattedMsg)
            await guild_group.quotes.set(quotes)
            return len(quotes)
    
    async def _removeQuote(self, guild: discord.Guild, n:int):
        guild_group = self.config.guild(guild)
        quotes = await guild_group.quotes()
        quotes.pop(n)
        await guild_group.quotes.set(quotes)

    def _buildQuote(self, message, num:int):
        quote = f"{message.content}\n[(Jump)]({message.jump_url})"
        timestamp = message.created_at
        embed = discord.Embed(timestamp=timestamp)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name=f"#{num}", value=quote, inline=False)
        return embed

    @commands.command()
    async def quote(self, ctx: commands.Context):
        """Recall Random Quote"""
        # Your code will go here
        quotes = await self.config.guild(ctx.guild).quotes()
        if quotes and len(quotes) > 0:
            num = randrange(len(quotes))
            message = await ctx.guild.get_channel(quotes[num]['channelId']).fetch_message(quotes[num]['messageId'])
            await ctx.send(embed=self._buildQuote(message, num+1))
        else:
            await ctx.send("No quotes added yet. Say something funny~ OwO")

    @commands.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def removeQuote(self, ctx: commands.Context, n:int):
        """Remove Quote"""
        await ctx.send(f"I Got {n}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        """On React"""
        if str(payload.emoji) == '💬':
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user = payload.member
            channel: discord.TextChannel = message.channel
            pos = await self._addQuote(message)
            if pos >= 0:
                await channel.send(f"New quote added by {user.display_name} #{pos}\n({message.jump_url})")
        else:
            return
