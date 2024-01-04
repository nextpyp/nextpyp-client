
from typing import Optional, List, Any

from websockets.legacy.client import Connect

import nextpyp.client.jsonrpc as jsonrpc
from nextpyp.client.credentials import Credentials
from nextpyp.client.gen import Services, RealtimeServices


class Client:
    """
    The main class for the client.
    """

    def __init__(self, url_base: str, credentials: Optional[Credentials]) -> None:
        """
        Things here too.

        And even more.

        :param url_base: The url_base
        :param credentials: The credentials
        """

        self.url_base: str = url_base
        """
        The url base
        
        Use this to do the thing!
        """

        self.credentials = credentials
        """The credentials"""
        self.services: Services = Services(self)
        """The services"""
        self.realtime_services = RealtimeServices(self)
        """The realtime services"""

        # convert the base url to the websockets protocol
        url_parts = url_base.split(':')
        url_parts[0] = 'ws'
        self.ws_url_base = ':'.join(url_parts)

    def _call(self, endpoint: str, params: List[Any]) -> Optional[Any]:
        return jsonrpc.call(self.url_base, endpoint, self.credentials, params)

    def _connect_websocket(self, endpoint: str) -> Connect:

        # build the headers, if any
        headers = {}
        if self.credentials is not None:
            headers['nextpyp-userid'] = self.credentials.userid
            headers['nextpyp-token'] = self.credentials.token

        return Connect(f'{self.ws_url_base}{endpoint}', extra_headers=headers)
