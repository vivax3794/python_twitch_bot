from .irc_protocol import IrcProtocol

from .utils import check_type
from .data_types import Channel, Message, User

class TwitchCore:
    def __init__(self):
        self._irc = IrcProtocol()
        self.channels: List[Channel] = []

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

    def send_message(self, channel_name: str, message: any) -> None:
        """
        Send message in a channel.

        If you have the channel object use it's send method instead.
        """
        message = str(message)
        check_type("channel_name", channel_name, str)

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
                channel = data.split("#")[1].split(":")[0][:-1]
                message = data.split(":")[1:]
                message = ":".join(message)

                channel = Channel(channel, self)
                user = User(user, self)
                return Message(user, channel, message)
