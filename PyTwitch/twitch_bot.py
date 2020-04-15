import traceback
from typing import Callable, List

from .irc_protocol import IrcProtocol

def check_type(name: str, value: any, should_be: any) -> None:
    """
    Check that the passed in value is the correct type, if not raise TypeError.
    """
    if not isinstance(value, should_be):
        raise TypeError(f"{name} must be type {should_be.__name__}, but got {type(value)}")

class Channel:
    """
    A twitch channel.
    """
    def __init__(self, channel_name: str, twitch_bot: "TwitchBot"):
        self.name = channel_name
        self._bot = twitch_bot

    def send_message(self, message: str):
        """
        Send a message in the channel.
        """
        check_type("message", message, str)
        self._bot.send_message(self.name, message)


class User:
    """
    A twitch user.
    """
    def __init__(self, username: str, twitch_bot: "TwitchBot"):
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
        check_type("message", message, str)
        self.channel.send_message(message)

# TODO: make Context
# TODO: make Command
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
    def __init__(self, func: Callable[[Context, str, ...], None]):
        self.func = func

    def call(self, ctx: Context, arguments: List[any]) -> None:
        """
        Runs the command.
        """
        self.func(ctx, *arguments)

class TwitchBot:
    def __init__(self, prefix: str="!"):
        self._irc = IrcProtocol()
        self.channels: List[Channel] = []
        self.commands = List[Command] = []

        check_type("prefix", prefix, str)
        self.prefix = prefix

    def connect(self, username: str, password: str) -> None:
        """
        Connect to twitch using username and password.
        """
        check_type("username", username, str)
        check_type("password", password, str)

        self._irc.connect("irc.twitch.tv", 6667)
        self._irc.login(username, password)

    def join_channel(self, channel: str) -> Channel:
        """
        Join a channel.

        return the channel object of the channel joined.
        """
        check_type("channel", channel, str)

        self._irc.join_channel(channel)
        channel = Channel(channel, self)
        self.channels.append(channel)

        return channel

    def send_message(self, channel_name: str, message: str) -> None:
        """
        Send message in a channel.

        If you have the channel object use it's send method instead.
        """
        check_type("channel_name", channel_name, str)
        check_type("message", message, str)

        self._irc.send_message(channel_name, message)

    def whisper(self, channel: str, username: str, message: str) -> None:
        """
        Whispers a user, if possible use a user object.
        """
        self.send_message(channel, f"/w {username} {message}")

    def read_message(self) -> Message:
        """
        Reads message from twitch
        """

        while True:
            data = self._irc.read()
            # print(data)
            if "PRIVMSG" in data:
                # This is a message, let's parse it!
                # messages are in this format:
                # :<user>!<user>@<user>.tmi.twitch.tv PRIVMSG #<channel> :This is a sample message

                data = data[1:]
                user = data.split("!")[0]
                channel = data.split("#")[1].split(":")[0]
                message = data.split(":")[1:]
                message = ":".join(message)

                channel = Channel(channel, self)
                user = User(user, self)
                return Message(user, channel, message)

    def run(self) -> None:
        """
        Run the bots main loop.
        """
        while True:
            message = self.read_message()

            try:
                self.event_message(message)
            except Exception as e:
                self.event_error(e)

    def process_message(self, message: Message) -> None:
        """
        Check if the message is a command.

        If it is a command, fetch the command object and construct a ctx.
        """
        if message.content.startswith(self.prefix):
            command_name, *arguments = message.content[len(self.prefix):].split(" ")
            command = self.commands.get(command_name)
            if command is None:
                raise ValueError(f"Command {command_name} not found")

            ctx = Context(message)
            command.call(ctx, arguments)

    def event_error(self, e):
        traceback.print_exc()

    def event_message(self, message: Message) -> None:
        print(f"{message.user.name}: {message.content}")
        self.process_message(message)
