from typing import Callable, List

from .utils import check_type

class Channel:
    """
    A twitch channel.
    """
    def __init__(self, channel_name: str, twitch_bot):
        self.name = channel_name
        self._bot = twitch_bot

    def send_message(self, message: str):
        """
        Send a message in the channel.
        """
        self._bot.send_message(self.name, message)


class User:
    """
    A twitch user.
    """
    def __init__(self, username: str, twitch_bot):
        self.name = username
        self._bot = twitch_bot


class Message:
    """
    A twith message.
    """
    def __init__(self, user: User, channel: Channel, message: str):
        self.user = user
        self.channel = channel
        self.content = message

    def reply(self, message: str) -> None:
        """
        Reply to the message.
        """
        self.channel.send_message(message)


class Context:
    """
    A command context, normally the first argument to a command.
    """
    def __init__(self, message: Message):
        self.message = message
        self.channel = message.channel
        self.user = message.user

    def reply(self, message: str) -> None:
        """
        Send a message in the same channel as the command was actiavted in.
        """
        self.message.reply(message)

class Command:
    """
    A command it self
    """
    def __init__(self, func: Callable[[Context, List[str]], None]):
        self.func = func

    def call(self, ctx: Context, arguments: List[any]) -> None:
        """
        Runs the command.
        """
        self.func(ctx, *arguments)
