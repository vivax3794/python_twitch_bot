import random

def setup(bot):
    @bot.command()
    def dice(ctx):
        num = random.randint(0, 10)
        ctx.reply(num)
