from typing import List, Dict
import warnings

import requests

class ApiError(Exception):
    """
    A error happend with the api.
    """

class ResponseCodeError(ApiError):
    """
    The response code of a request was not excpected.
    """

class TwitchApi:
    """
    A wrapper around the twitch api.
    """
    def __init__(self, client_id: int, retry_limit: int=10):
        self.client_id = client_id
        self.retry_limit = retry_limit

        self.session = requests.session()
        headers = {
                "Client-ID": client_id
                }
        self.session.headers = headers

        if client_id is None:
            warnings.warn("Client id not given, all api functions except chatters will not be functional. this does NOT include the chat functions like sending message.")

    def _call_api(self, url: str, method: str="get"):
        """
        Calls the given url with the current session.
        """
        for retries_left in range(self.retry_limit, -1, -1):
            if method == "get":
                response = self.session.get(url)
            elif method == "post":
                response = self.session.get(url)
            else:
                raise ValueError(f"invalid method: {method}")

            if response.status_code == 429:
                # Rate limit error
                if retries_left == 0:
                    raise RatelimitError(f"Ratelimit retried reached ({self.retry_limit})")
                warnings.warn("twitch api ratelimit hit, sleeping for 5 seconds. reties left: {}")

            else:
                return response

    def chatters(self, channel: str) -> Dict[str, List[str]]:
        """
        The users in chat and their highest role.
        """
        url = f"http://tmi.twitch.tv/group/user/{channel}/chatters"
        # we dont use the session since this is not a offical twich api and it does not need the client-id
        response = requests.get(url)

        if response.status_code != 200:
            raise ResponseCodeError(f"Excpected a 200 response, but got {response.status_code}")

        return response.json()["chatters"]

    def chatters_no_roles(self, channel: str) -> List[str]:
        """
        Returns just a list of chatters, instead of divided into roles.
        """
        chatters_with_roles = self.chatters(channel)
        chatters: List[str] = []

        for users in chatters_with_roles.values():
            chatters.extend(users)

        return chatters