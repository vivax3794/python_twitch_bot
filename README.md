# PyTwitch

PyTwitch is a small Python library oriented at making [Twitch](https://twitch.tv) bots.

## Instalation

You can install the library by first cloning the repo:
```bash
git clone git@github.com:vivax3794/python_twitch_bot.git
```
<br>

and then `cd` into the cloned directory and install it using [pip]
```bash
pip install .
```
<br>

## Usage

```py
from PyTwitch import TwitchBot
from mytoken import TOKEN                   # this is oauth token you can get from https://dev.twitch.tv/docs/irc 


bot = TwitchBot()
bot.connect("therealvivax", TOKEN)          # connect the bot with twitch servers

channel = bot.join_channel("vivax3794")     # join your stream chat 


@bot.command()
def hello(ctx):
    ctx.reply("Hello World!")


if __name__ == "__main__":                  # finally, run the bot
    bot.run()
```
<br>

## Contributing

Pull requests are more than welcome, if you want to discuss something open up an issue and we can work it out together!
Before pushing something, please make sure your code is working as expected.
<br>

## License
[MIT](https://choosealicense.com/licenses/mit/)
