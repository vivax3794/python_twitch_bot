from PyTwitch import TwitchBot

from secret import TOKEN, CLIENT_ID
# client id can be gotten by making a application at: https://dev.twitch.tv/console/apps

BOT_NAME = "therealvivax"
CHANNEL = "vivax3794"

bot = TwitchBot()
bot.connect(BOT_NAME, TOKEN)

channel = bot.join_channel(CHANNEL)

@bot.command()
def followers(ctx):
    # this attribute uses the api
    followers_ammount = ctx.channel.num_followers
    ctx.reply(f"{channel.name} has {followers_ammount} followers")

if __name__ == "__main__":
    bot.run()
