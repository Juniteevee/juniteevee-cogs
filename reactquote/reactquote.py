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
            "quotes": [],
            "reactQuotesSettings": {
                "outputChannel": None
            }
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
    
    async def _manualAddQuote(self, guild, author, message):
        formattedMsg = {
            "messageText": message,
            "authorId": author.id,
            "messageId": None
        }
        guild_group = self.config.guild(guild)
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

    async def _buildQuote(self, ctx:commands.Context, formattedMessage, num:int):
        if formattedMessage["messageId"] is not None:
            message = await ctx.guild.get_channel(formattedMessage['channelId']).fetch_message(formattedMessage['messageId'])
            quote = f"{message.content}\n[(Jump)]({message.jump_url})"
            timestamp = message.created_at
            author = message.author
        else:
            message = formattedMessage["messageText"]
            quote = f"{message}\n*Added Manually*"
            timestamp = ctx.message.created_at
            author = ctx.guild.get_member(formattedMessage["authorId"])
        embed = discord.Embed(timestamp=timestamp)
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        embed.add_field(name=f"#{num}", value=quote, inline=False)
        return embed
    
    def _oldBuildQuote(self, message, num:int):
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
        quotes = await self.config.guild(ctx.guild).quotes()
        numQuotes = len(quotes)
        if numQuotes > 0:
            if(query == ""):
                """case random"""
                num = randrange(len(quotes))
                embed = await self._buildQuote(ctx, quotes[num], num+1)
                await ctx.send(embed=embed)
            elif(re.search("^\d+$", query) is not None):
                """case id"""
                num = int(query)
                if num <= numQuotes:
                    embed = await self._buildQuote(ctx, quotes[num], num+1)
                    await ctx.send(embed=embed)
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
                        embed = await self._buildQuote(ctx, filteredQuotes[num], globalNum+1)
                        await ctx.send(embed=embed)
            else:
                """Testing case"""
                await ctx.send(f"{query} was not picked up. (This is for testing purposes)")

        else:
            await ctx.send("No quotes added yet.\nSay something funny~ OwO")

    @commands.guild_only()
    @commands.command()
    async def addquote(self, ctx: commands.Context, *, query: str):
        """Manually add quote. @ the speaker of quote to properly credit them"""
        if query is None or len(query) == 0:
            await ctx.send("No quote provided. What are you saying? OwO")
        else:
            quotes = await self.config.guild(ctx.guild).quotes()
            numQuotes = len(quotes)
            quote = f"{query}\n*Added Manually*)"
            timestamp = ctx.message.created_at
            embed = discord.Embed(timestamp=timestamp)
            if len(ctx.message.mentions) > 0:
                member: discord.Member = ctx.message.mentions[0]
                self._manualAddQuote(ctx.guild, member, quote)
                await ctx.send(f"New quote manually added by {ctx.author.display_name} as #{numQuotes}")
                guild_group = self.config.guild(ctx.guild)
                settings = await guild_group.reactQuotesSettings()
                if settings["outputChannel"] is not None:
                    logChan = ctx.guild.get_channel(settings["outputChannel"])
                    formattedMsg = {
                        "messageText": quote,
                        "authorId": member.id
                    }
                    embed = await self._buildQuote(ctx, formattedMsg, numQuotes)
                    await logChan.send(embed=embed)



    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command()
    async def removequote(self, ctx: commands.Context, quote_num:int):
        """Remove Quote"""
        await self._removeQuote(ctx.guild, quote_num-1)
        await ctx.send(f"Removed quote #{quote_num}.")

    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command()
    async def setquoteout(self, ctx: commands.Context):
        """Sets Channel to be output for new Quotes"""
        guild_group = self.config.guild(ctx.guild)
        settings = await guild_group.reactQuotesSettings()
        settings["outputChannel"] = ctx.channel.id
        await guild_group.reactQuotesSettings.set(settings)
        await ctx.send("New Quotes will print here.")

    
    @commands.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.command()
    async def allquotes(self, ctx: commands.Context):
        """Print all quotes"""
        quotes = await self.config.guild(ctx.guild).quotes()
        for index, quote in enumerate(quotes):
            embed = await self._buildQuote(ctx, quote, index+1)
            await ctx.send(embed=embed)


    
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
                guild_group = self.config.guild(message.guild)
                settings = await guild_group.reactQuotesSettings()
                if settings["outputChannel"] is not None:
                    logChan = message.guild.get_channel(settings["outputChannel"])
                    await logChan.send(embed=self._oldBuildQuote(message, pos))
        else:
            return
