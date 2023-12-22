
from types import TracebackType
from typing import cast, List, Optional, Any, Type, Union

import json
from websockets.legacy.client import Connect, WebSocketClientProtocol

from nextpyp.client import Client as RealClient
from nextpyp.client.gen import Services, RealtimeServices


class MockClient:

    def __init__(self) -> None:
        self.services = Services(self.mock())
        self.realtime_services = RealtimeServices(self.mock())
        self.last_params: Optional[List[Any]] = None
        self.next_response: Optional[Any] = None
        self._last_sent_message: Optional[Any] = None
        self._next_recv_message: Optional[str] = None

    def mock(self) -> RealClient:
        return cast(RealClient, self)

    def _call(self, _endpoint: str, params: List[Any]) -> Optional[Any]:
        self.last_params = params
        if self.next_response is None:
            raise Exception("set a next_response")
        out = self.next_response
        self.next_response = None
        return out

    def _connect_websocket(self, _endpoint: str) -> Connect:
        return MockWebsocketConnect(self).mock()

    def last_sent_message(self) -> Any:
        if self._last_sent_message is None:
            return None
        return json.loads(self._last_sent_message)

    def next_recv_message(self, j: Any) -> None:
        self._next_recv_message = json.dumps(j)


class MockWebsocketConnect:

    def __init__(self, client: MockClient):
        self.client = client

    def mock(self) -> Connect:
        return cast(Connect, self)

    async def __aenter__(self) -> WebSocketClientProtocol:
        return MockWebsocket(self.client).mock()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        pass


class MockWebsocket:

    def __init__(self, client: MockClient):
        self.client = client

    def mock(self) -> WebSocketClientProtocol:
        return cast(WebSocketClientProtocol, self)

    async def send(self, msg: Union[str, bytes]) -> None:
        if type(msg) is bytes:
            raise Exception('sending bytes not allowed')
        self.client._last_sent_message = msg

    async def recv(self) -> str:
        if self.client._next_recv_message is None:
            raise Exception("set a next_recv_message")
        out = self.client._next_recv_message
        self.client._next_recv_message = None
        return out
