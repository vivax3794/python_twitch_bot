import socket


class SocketWrapper:
    """
    A wrapper around the standard python socket.
    """

    def __init__(self) -> None:
        self._sock = socket.socket()

    def connect(self, addr: str, port: int) -> None:
        """
        Connect to a server
        """
        self._sock.connect((addr, port))

    def send(self, data: str) -> None:
        """
        Send data over the socket
        """
        encoded_data: bytes = (data + "\r\n").encode()
        self._sock.sendall(encoded_data)

    def read(self) -> str:
        """
        Read data from the socket
        """
        data = self._sock.recv(2048)
        return data.decode().replace("\r", "\n")
