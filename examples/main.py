from PyTwitch import TwitchBot

from secret import TOKEN

COGS = [
        "info"
        ]

bot = TwitchBot()
bot.connect("therealvivax", TOKEN)

channel = bot.join_channel("vivax3794")

for cog in COGS:
    bot.load_cog(f"cogs.{cog}")

if __name__ == "__main__":
    bot.run()
