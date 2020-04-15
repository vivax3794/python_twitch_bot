from PyTwitch import TwitchBot

from secret import TOKEN


bot = TwitchBot()
bot.connect("therealvivax", TOKEN)

channel = bot.join_channel("vivax3794")


bot.run()
