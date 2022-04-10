from .reactquote import ReactQuote

def setup(bot):
    bot.add_cog(ReactQuote(bot))