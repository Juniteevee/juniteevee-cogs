from .chatgpt import ChatGpt

def setup(bot):
    bot.add_cog(ChatGpt(bot))