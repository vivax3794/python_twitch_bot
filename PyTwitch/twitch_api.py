from typing import List, Dict
from functools import lru_cache
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

class NoClientId(ApiError):
    """
    Client id is needed for this request
    """
    def __init__(self, *args, **kwargs):
        super().__init__("Clientt id is needed for this request", *args, **kwargs)

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

    def _pagination(self, url):
        """
        gets all the data from a url using the cursor value
        """
        cursor = ""
        data = []
        while cursor is not None:
            response = self._call_api(f"{url}&after={cursor}")
            json = response.json()

            cursor = json["pagination"].get("cursor")
            new_data = json["data"]
            data.extend(new_data)

        return data

    def user_info(self, username: str):
        """
        Get info on a twitch user.

        see: https://dev.twitch.tv/docs/api/reference#get-users
        """
        if self.client_id is None:
            raise NoClientId()

        url = f"https://api.twitch.tv/helix/users?login={username}"
        response = self._call_api(url)

        return response.json()["data"][0]

    @lru_cache()
    def get_user_id(self, username: str):
        user_data = self.user_info(username)
        return user_data["id"]

    def following_info(self, to_name, from_name):
        if to_name is not None:
            to_id = self.get_user_id(to_name)
        else:
            to_id = None

        if from_name is not None:
            from_id = self.get_user_id(from_name)
        else:
            from_id = None

        url = f"https://api.twitch.tv/helix/users/follows?to_id={to_id}&from_id={from_id}"
        followers = self._pagination(url)
        return followers

    # BUG: only works if they are live
    # look into how it can be done if they are offline
    def stream_info(self, streamer_name: str):
        """
        Information about a stream.
        """
        url = f"https://api.twitch.tv/helix/streams?user_login={streamer_name}"
        data = self._call_api(url).json()

        return data["data"][0]

    def get_game(self, game_id):
        url = f"https://api.twitch.tv/helix/games?id={game_id}"
        data = self._call_api(url).json()
        return data["data"][0]["name"]
