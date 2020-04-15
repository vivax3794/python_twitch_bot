from PyTwitch import TwitchBot

from secret import TOKEN

BOT_NAME = "therealvivax"
CHANNEL = "vivax3794"

bot = TwitchBot()
bot.connect(BOT_NAME, TOKEN)

channel = bot.join_channel(TOKEN)

@bot.command("my-role")
def my_role(ctx):
    user = ctx.user
    ctx.reply(f"@{user.name} is a {user.role}")

if __name__ == "__main__":
    bot.run()
