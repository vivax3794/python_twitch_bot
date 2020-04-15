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
    def __init__(self, client_id: int):
        self.client_id = client_id
        self.session = requests.session()
        headers = {
                "Client-ID": client_id
                }
        self.session.headers = headers

        if client_id is None:
            warnings.warn("Client id not given, all api functions except chatters will not be functional. this does NOT include the chat functions like sending message.")

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
        chatters_with_roles = self.chatters(channel)
        chatters: List[str] = []

        for users in chatters_with_roles.values():
            chatters.extend(users)

        return chatters
