from redbot.core import commands
from redbot.core import Config
from random import randrange
import re
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

    @commands.guild_only()
    @commands.command()
    async def quote(self, ctx: commands.Context, *, query: str = ""):
        """
        Recall Quote

        'quote' returns random
        'quote 3' returns the #3 quote
        """
        # Your code will go here
        quotes = await self.config.guild(ctx.guild).quotes()
        numQuotes = len(quotes)
        if numQuotes > 0:
            if(query == ""):
                num = randrange(len(quotes))
                message = await ctx.guild.get_channel(quotes[num]['channelId']).fetch_message(quotes[num]['messageId'])
                await ctx.send(embed=self._buildQuote(message, num+1))
            elif(re.search("^\d+$", query) is not None):
                """case id"""
                num = int(query)
                if num <= numQuotes:
                    message = await ctx.guild.get_channel(quotes[num-1]['channelId']).fetch_message(quotes[num-1]['messageId'])
                    await ctx.send(embed=self._buildQuote(message, num))
                else:
                    await ctx.send(f"There are only {numQuotes} quotes")
            elif(len(ctx.message.mentions) > 0):
                """Case username"""
                member: discord.Member = ctx.message.mentions[0]
                if member is None:
                    await ctx.send(f"{query} not found.\nWho are you talking about? OwO")
                else:
                    filteredQuotes = []
                    for quote in quotes:
                        if quote["authorId"] == member.id:
                            filteredQuotes.append(quote)
                    if len(filteredQuotes) == 0:
                        await ctx.send(f"No quotes by {member.name} found.\nSay something funny~ OwO")
                    else:
                        num = randrange(len(filteredQuotes))
                        globalNum = quotes.index(filteredQuotes[num])
                        message = await ctx.guild.get_channel(filteredQuotes[num]['channelId']).fetch_message(filteredQuotes[num]['messageId'])
                        await ctx.send(embed=self._buildQuote(message, globalNum+1))
            else:
                """Testing case"""
                await ctx.send(f"{query} was not picked up. (This is for testing purposes)")

        else:
            await ctx.send("No quotes added yet.\nSay something funny~ OwO")

    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command()
    async def removequote(self, ctx: commands.Context, quote_num:int):
        """Remove Quote"""
        await self._removeQuote(ctx.guild, quote_num-1)
        await ctx.send(f"Removed quote #{quote_num}.")
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        """On React"""
        if str(payload.emoji) == '💬':
            message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            user = payload.member
            channel: discord.TextChannel = message.channel
            pos = await self._addQuote(message)
            if pos >= 0:
                await channel.send(f"New quote added by {user.display_name} as #{pos}\n({message.jump_url})")
        else:
            return
