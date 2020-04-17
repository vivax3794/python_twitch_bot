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
    followers_list = ctx.channel.followers
    ctx.reply(f"{channel.name} has {len(followers_list)} followers")
    # NOTE: there is a more efficent way to get this with the api that will be added latter.
    # TODO: remove note once the above mentioned is added

if __name__ == "__main__":
    bot.run()
