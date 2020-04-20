from typing import Callable, List, Dict
from . import twitch_bot

# used for type hinting
from .twitch_api import UserInfo, StreamInfo


class ChannelInfo:
    """
    Contains info about a channel.
    """
    def __init__(self, data: UserInfo):
        self.rank = data["broadcaster_type"]
        self.description = data["description"]


class Channel:
    """
    A twitch channel.
    """
    def __init__(
                self,
                channel_name: str,
                bot  # type: twitch_bot.TwitchBot
                ) -> None:
        self.name = channel_name
        self._bot = bot

    def send_message(self, message: str) -> None:
        """
        Send a message in the channel.
        """
        self._bot.send_message(self.name, message)

    @property
    def chatters(self) -> List[str]:
        return self._bot.api.chatters_no_roles(self.name)

    def chatters_with_roles(self) -> Dict[str, List[str]]:
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
    def followers(self) -> List[str]:
        """
        Who follows this channel.
        """
        followers: List[str] = []
        for connection in self._bot.api.following_info(to_name=self.name):
            followers.append(connection["from_name"])

        return followers

    @property
    def stream(self) -> "Stream":
        """
        The stream object representing this channel.
        """
        data = self._bot.api.stream_info(self.name)
        return Stream(data, self._bot)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Channel):
            raise NotImplementedError()

        return self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Channel(name={self.name})"


class Stream:
    """
    Like a channnel, but with more info on the stream.
    """
    def __init__(
            self,
            data: StreamInfo,
            bot  # type: twitch_bot.TwitchBot
            ) -> None:
        self.name = data["user_name"]
        self.game_id = int(data["game_id"])
        self.title = data["title"]
        self.views = data["viewer_count"]

        self._bot = bot

    @property
    def game(self) -> str:
        """
        The name of the currently playing game.
        """
        return self._bot.api.get_game(self.game_id)

    def __str__(self) -> str:
        return self.name


class User:
    """
    A twitch user.
    """
    def __init__(
            self,
            username: str,
            channel: Channel,
            twitch_bot  # type: twitch_bot.TwitchBot
            ) -> None:
        self.name = username
        self._channel = channel
        self._bot = twitch_bot

    @property
    def channel(self) -> Channel:
        """
        A channel reprisenting this users channel,

        If you wanted the channel this users object was made form use _channel
        """
        return Channel(self.name, self._bot)

    @property
    def role(self) -> str:
        """
        The highest role of the user.
        """
        chatters = self._bot.api.chatters(self._channel.name)
        for role, users in chatters.items():
            if self.name in users:
                role = role.rstrip("s")
                return role

        else:
            raise ValueError(
                    f"user {self.name} was not found in the chatters list."
                    )

    @property
    def following(self) -> List[str]:
        """
        Who this person is following.
        """
        following: List[str] = []
        for connection in self._bot.api.following_info(from_name=self.name):
            following.append(connection["to_name"])

        return following

    def is_following(self) -> bool:
        """
        Checks if the user is following the channel.

        Use this instead of checking if the username is in the followers.
        Since this asks twitch directly if they are following.
        """
        follow_info = self._bot.api.following_info(
                from_name=self.name,
                to_name=self._channel.name
            )
        # if they are following there will be 1 entry, that follow.
        return len(follow_info) == 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            raise NotImplementedError()

        return self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"User(name={self.name})"


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

    def __str__(self) -> str:
        return f"#{self.channel} {self.user}: {self.content}"

    def __repr__(self) -> str:
        return f"Message(channel={self.channel}, user={self.user})"


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

    def create_user(self, username: str) -> User:
        """
        Create a user as if their message came from the commands channel.
        """
        return User(username, self.channel, self.bot)


class Command:
    """
    A command it self
    """
    def __init__(self, func: Callable[[Context], None]):
        self.func = func

    def call(self, ctx: Context, arguments: List[str]) -> None:
        """
        Runs the command.
        """
        self.func(ctx, *arguments)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Command):
            raise NotImplementedError()

        return self.func == other.func

    def __repr__(self) -> str:
        return f"Command(func={self.func})"
