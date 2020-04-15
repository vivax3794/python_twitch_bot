from PyTwitch import TwitchBot

from secret import TOKEN

COGS = [
        "info"
        ]
BOT_NAME = "therealvivax"
CHANNEL = "vivax3794"

bot = TwitchBot()
bot.connect(BOT_NAME, TOKEN)

channel = bot.join_channel(TOKEN)

for cog in COGS:
    bot.load_cog(f"cogs.{cog}")

if __name__ == "__main__":
    bot.run()
