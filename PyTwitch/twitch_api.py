from typing import List, Dict, Union, Optional  # , Mapping
from typing_extensions import TypedDict

from functools import lru_cache
import warnings

import requests

from .errors import NoClientId, RatelimitError, ResponseCodeError, StreamerNotLiveError

# types
UserInfo = TypedDict("UserInfo", {
    "id": str,
    "login": str,
    "display_name": str,
    "type": str,
    "broadcaster_type": str,
    "description": str,
    "profile_image_url": str,
    "offline_image_url": str,
    "view_count": str,
    "email": str
    })

FollowingInfo = TypedDict("FollowingInfo", {
    "from_id": str,
    "from_name": str,
    "to_id": str,
    "to_name": str,
    "followed_at": str
    })

StreamInfo = TypedDict("StreamInfo", {
    "id": str,
    "user_id": str,
    "user_name": str,
    "game_id": str,
    "type": str,
    "title": str,
    "viewer_count": int,
    "started_at": str,
    "language": str,
    "thumbnail_url": str
    })

JsonData = Dict[str, Union[str, int]]
ApiRespons = TypedDict("ApiRespons", {
    "pagination": Dict[str, str],
    "data": List[JsonData]
    })


class TwitchApi:
    """
    A wrapper around the twitch api.
    """
    def __init__(self, client_id: Optional[str], retry_limit: int = 10):
        self.client_id = client_id

        if retry_limit <= 0:
            raise ValueError("retry_limit must be positiv.")
        self.retry_limit = retry_limit

        self.session = requests.session()
        headers = {
                "Client-ID": str(client_id)
                }
        self.session.headers.update(headers)

    def _call_api(self, url: str, method: str = "get") -> ApiRespons:
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
                continue

            json: ApiRespons = response.json()
            return json
        raise ValueError(f"retry_limit is negativ (or 0), retry_limt={self.retry_limit}")

    def chatters(self, channel: str) -> Dict[str, List[str]]:
        """
        The users in chat and their highest role.
        """
        url = f"http://tmi.twitch.tv/group/user/{channel}/chatters"
        # we dont use the session since this is not a offical twich api and it does not need the client-id
        response = requests.get(url)

        if response.status_code != 200:
            raise ResponseCodeError(f"Excpected a 200 response, but got {response.status_code}")

        data: Dict[str, Dict[str, List[str]]] = response.json()
        return data["chatters"]

    def chatters_no_roles(self, channel: str) -> List[str]:
        """
        Returns just a list of chatters, instead of divided into roles.
        """
        chatters_with_roles = self.chatters(channel)
        chatters: List[str] = []

        for users in chatters_with_roles.values():
            chatters.extend(users)

        return chatters

    def _pagination(self, url: str) -> List[JsonData]:
        """
        gets all the data from a url using the cursor value
        """
        cursor: Optional[str] = ""
        data: List[JsonData] = []
        while cursor is not None:
            json = self._call_api(f"{url}&after={cursor}")

            cursor = json["pagination"].get("cursor", None)
            new_data = json["data"]
            data.extend(new_data)

        return data

    def user_info(self, username: str) -> UserInfo:
        """
        Get info on a twitch user.

        see: https://dev.twitch.tv/docs/api/reference#get-users
        """
        if self.client_id is None:
            raise NoClientId()

        url = f"https://api.twitch.tv/helix/users?login={username}"
        json = self._call_api(url)
        data: UserInfo = json["data"][0]  # type: ignore

        return data

    @lru_cache()
    def get_user_id(self, username: str) -> int:
        user_data = self.user_info(username)
        user_id = user_data["id"]
        return int(user_id)

    def following_info(self, to_name: Optional[str] = None, from_name: Optional[str] = None) -> List[FollowingInfo]:
        to_id: Optional[int]
        from_id: Optional[int]

        if to_name is not None:
            to_id = self.get_user_id(to_name)
        else:
            to_id = None

        if from_name is not None:
            from_id = self.get_user_id(from_name)
        else:
            from_id = None

        url = f"https://api.twitch.tv/helix/users/follows?to_id={to_id}&from_id={from_id}"
        followers: List[FollowingInfo] = self._pagination(url)  # type: ignore
        return followers

    # BUG: only works if they are live
    # look into how it can be done if they are offline
    def stream_info(self, streamer_name: str) -> StreamInfo:
        """
        Information about a stream.
        """
        url = f"https://api.twitch.tv/helix/streams?user_login={streamer_name}"
        data = self._call_api(url)
        if len(data["data"]) == 0:
            raise StreamerNotLiveError(f"The requested streamer {streamer_name} is not live, and we can not get their info.")
        stream_data: StreamInfo = data["data"][0]  # type: ignore

        return stream_data

    def get_game(self, game_id: int) -> str:
        """
        Get the name of a game from it's id.
        """
        url = f"https://api.twitch.tv/helix/games?id={game_id}"
        data = self._call_api(url)
        name: str = data["data"][0]["name"]  # type: ignore
        return name
