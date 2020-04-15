from .socket_wrapper import SocketWrapper
from typing import List


class IrcProtocol:
    """
    Methods to interact with a irc server
    """
    def __init__(self):
        self._sock = SocketWrapper()
        self._data: List[str] = []

    def connect(self, server: str, port: int=667) -> None:
        """
        Connect to a irc server.

        If no port is given it will default to 6667.
        """
        self._sock.connect(server, port)

    def login(self, username: str, password: str) -> None:
        """
        Login to the irc server
        """
        self._sock.send(f"PASS {password}")
        self._sock.send(f"NICK {username}")

    def join_channel(self, channel: str) -> None:
        """
        Join the specified channel.
        """
        self._sock.send(f"JOIN #{channel}")

    def send_message(self, channel: str, message: str) -> None:
        """
        Sends a message in the specified channel.
        """
        self._sock.send(f"PRIVMSG #{channel} :{message}")

    def read(self) -> str:
        """
        Reads one line of info from the connected server.
        """
        if not self._data:
            new_data = self._sock.read().split("\n")
            self._data.extend(new_data)

        return self._data.pop(0)
