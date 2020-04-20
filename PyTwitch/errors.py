class ApiError(Exception):
    """
    A error happend with the api.
    """


class ResponseCodeError(ApiError):
    """
    The response code of a request was not excpected.
    """


class NoClientId(ApiError):
    """
    Client id is needed for this request
    """
    def __init__(self) -> None:
        super().__init__("Client id is needed for this request")


class RatelimitError(ApiError):
    """
    Twitch rate limit reached.
    """


class StreamerNotLiveError(ApiError, ValueError):
    """
    The streamer is offline.
    """


class CommandNotFoundError(KeyError):
    """
    The command was not found.
    """
