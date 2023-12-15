
from typing import Optional, List, Any

import nextpyp.client.jsonrpc as jsonrpc
from nextpyp.client.credentials import Credentials
from nextpyp.client.gen import Services, RealtimeServices


class Client:

    def __init__(self, url_base: str, credentials: Optional[Credentials]) -> None:
        self.url_base = url_base
        self.credentials = credentials
        self.services = Services(self)
        self.realtime_services = RealtimeServices(self)

        # convert the base url to the websockets protocol
        url_parts = url_base.split(':')
        url_parts[0] = 'ws'
        self.ws_url_base = ':'.join(url_parts)

    def _call(self, endpoint: str, params: List[Any]) -> Optional[Any]:
        return jsonrpc.call(self.url_base, endpoint, self.credentials, params)
