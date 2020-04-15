from PyTwitch import TwitchBot

from secret import TOKEN


bot = TwitchBot()
bot.connect("therealvivax", TOKEN)

channel = bot.join_channel("vivax3794")

@bot.command()
def hello(ctx):
    ctx.reply("Hello World!")

@bot.command("add")
def add_command(ctx, a, b):
    a, b = int(a), int(b)
    s = a + b
    ctx.reply(str(s))

@bot.command()
def project(ctx):
    ctx.reply(f"I am working on a twitch bot in python, github link: https://github.com/vivax3794/python_twitch_bot")


bot.run()
