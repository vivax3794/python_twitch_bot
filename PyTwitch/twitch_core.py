from typing import List

from .irc_protocol import IrcProtocol

from .utils import check_type
from .data_types import Channel, Message, User


class TwitchCore:
    def __init__(self) -> None:
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

    def join_channel(self, channel_name: str) -> Channel:
        """
        Join a channel.

        return the channel object of the channel joined.
        """
        check_type("channel_name", channel_name, str)

        self._irc.join_channel(channel_name)
        channel = Channel(channel_name, self)  # type: ignore
        self.channels.append(channel)

        return channel

    def send_message(self, channel_name: str, message: str) -> None:
        """
        Send message in a channel.

        If you have the channel object use it's send method instead.
        """
        message = str(message)
        check_type("channel_name", channel_name, str)

        self._irc.send_message(channel_name, message)

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
                user_name = data.split("!")[0]
                channel_name = data.split("#")[1].split(":")[0][:-1]
                message_parts = data.split(":")[1:]
                message_content = ":".join(message_parts)

                channel = Channel(channel_name, self)  # type: ignore
                user = User(user_name, channel, self)  # type: ignore
                return Message(user, channel, message_content)
