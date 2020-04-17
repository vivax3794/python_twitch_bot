from typing import Callable, List

from .utils import check_type

class ChannelInfo:
    """
    Contains info about a channel.
    """
    def __init__(self, data):
        self.rank = data["broadcaster_type"]
        self.description = data["description"]

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
    def chatters(self):
        return self._bot.api.chatters_no_roles(self.name)

    def chatters_with_roles(self):
        return self._bot.api.chatters(self.name)

    @property
    def info(self) -> ChannelInfo:
        """
        A class containing info about the channel.

        From the api.
        """
        data = self._bot.api.user_info(self.name)
        return ChannelInfo(data)

    @property
    def followers(self):
        """
        Who follows this channel.
        """
        followers = []
        for connection in self._bot.api.following_info(to_id=self.name):
            followers.append(connection["from_name"])

        return followers

    def __eq__(self, other) -> bool:
        return self.name == other.name

    @property
    def stream(self):
        """
        The stream object representing this channel.
        """
        data = self._bot.api.stream_info(self.name)
        return Stream(data, self._bot)

class Stream:
    """
    Like a channnel, but with more info on the stream.
    """
    def __init__(self, data, bot):
        self.name = data["user_name"]
        self.game_id = data["game_id"]
        self.title = data["title"]
        self.views = data["viewer_count"]

        self._bot = bot

    @property
    def game(self):
        """
        The name of the currently playing game.
        """
        return self._bot.api.get_game(self.game_id)


class User:
    """
    A twitch user.
    """
    def __init__(self, username: str, channel: Channel, twitch_bot):
        self.name = username
        self._channel = channel
        self._bot = twitch_bot

    @property
    def channel(self):
        """
        A channel reprisenting this users channel,

        If you wanted the channel this users object was made form use "_channel"
        """
        return Channel(self.name, self._bot)


    @property
    def role(self):
        """
        The highest role of the user.
        """
        chatters = self._bot.api.chatters(self._channel.name)
        for role, users in chatters.items():
            if self.name in users:
                role = role.rstrip("s")
                return role

        else:
            raise ValueError(f"user {self.name} was not found in the chatters list.")

    @property
    def following(self):
        """
        Who this person is following.
        """
        following  = []
        for connection in self._bot.api.following_info(from_name=self.name):
            following.append(connection["to_name"])

        return following

    def is_following(self):
        """
        Checks if the user is following the channel.

        Use this instead of checking if the username is in the channel followers.
        Since this ask twitch directly if they are following and not for all followers.
        """
        follow_info = self._bot.api.following_info(from_name=self.name, to_name=self._channel.name)

        return len(follow_info) == 1 # if they are following there will be 1 entry, that follow.

    def __eq__(self, other):
        return self.name == other.name


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

    def __eq__(self, other):
        return self.func == other.func
