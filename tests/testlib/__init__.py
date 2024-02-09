
from types import TracebackType
from typing import cast, List, Optional, Any, Type, Union

import json
from websockets.legacy.client import Connect, WebSocketClientProtocol

from nextpyp.client import Client, NetworkTransport


class MockTransport:

    def __init__(self) -> None:
        self.last_params: Optional[List[Any]] = None
        self.next_response: Optional[Any] = None
        self._last_sent_message: Optional[Any] = None
        self._next_recv_message: Optional[str] = None

    def client(self) -> Client:
        client = Client('who cares', None)
        client._transport = cast(NetworkTransport, self)
        return client

    def call(self, _endpoint: str, params: List[Any]) -> Optional[Any]:
        self.last_params = params
        out = self.next_response
        self.next_response = None
        return out

    def connect_websocket(self, _endpoint: str) -> Connect:
        return MockWebsocketConnect(self).mock()

    def get_last_sent_message(self) -> Any:
        if self._last_sent_message is None:
            return None
        return json.loads(self._last_sent_message)

    def set_next_recv_message(self, j: Any) -> None:
        self._next_recv_message = json.dumps(j)


class MockWebsocketConnect:

    def __init__(self, transport: MockTransport):
        self.transport = transport

    def mock(self) -> Connect:
        return cast(Connect, self)

    async def __aenter__(self) -> WebSocketClientProtocol:
        return MockWebsocket(self.transport).mock()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        pass


class MockWebsocket:

    def __init__(self, transport: MockTransport):
        self.transport = transport

    def mock(self) -> WebSocketClientProtocol:
        return cast(WebSocketClientProtocol, self)

    async def send(self, msg: Union[str, bytes]) -> None:
        if type(msg) is bytes:
            raise Exception('sending bytes not allowed')
        self.transport._last_sent_message = msg

    async def recv(self) -> str:
        if self.transport._next_recv_message is None:
            raise Exception("set a next_recv_message")
        out = self.transport._next_recv_message
        self.transport._next_recv_message = None
        return out
