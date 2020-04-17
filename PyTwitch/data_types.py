from typing import Callable, List

from .utils import check_type

class ChannelInfo:
    """
    Contains info about a channel.
    """
    def __init__(self, data):
        self.rank = data["broadcaster_type"]
        self.description = data["description"]
        self.views = data["view_count"]

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

    @property
    def info(self) -> ChannelInfo:
        """
        A class containing info about the channel.

        From the api.
        """
        data = self._bot.api.user_info(self.name)
        return ChannelInfo(data)

class User:
    """
    A twitch user.
    """
    def __init__(self, username: str, channel: Channel, twitch_bot):
        self.name = username
        self.channel = channel
        self._bot = twitch_bot

    @property
    def role(self):
        """
        The highest role of the user.
        """
        chatters = self._bot.api.chatters(self.channel.name)
        for role, users in chatters.items():
            if self.name in users:
                role = role.rstrip("s")
                return role

        else:
            raise ValueError(f"user {self.name} was not found in the chatters list.")


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
        self.bot = message.channel._bot

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
