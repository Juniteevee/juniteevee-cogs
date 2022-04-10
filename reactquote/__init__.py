from .reactquote import ReactQuote
from redbot.core.utils import fileIO
import os

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