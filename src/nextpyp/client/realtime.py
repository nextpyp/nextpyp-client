
from __future__ import annotations

from websockets.legacy.client import Connect, WebSocketClientProtocol

from types import TracebackType
from typing import Optional, Any, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from nextpyp.client import Client


class RealtimeServiceConnection:

    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        self.websocket = websocket

    async def send(self, msg: Any) -> None:
        websocket = self.websocket
        if websocket is None:
            raise Exception('not connected')
        await websocket.send(msg)

    async def recv(self) -> Any:
        websocket = self.websocket
        if websocket is None:
            raise Exception('not connected')
        await websocket.recv()

    # TODO: implement type translation on send/recv


class RealtimeService:
    """
    An asyncio client for nextPYP realtime web services
    """

    def __init__(self, client: Client, endpoint: str) -> None:

        # the path should be absolute
        if not endpoint.startswith('/'):
            raise Exception(f'invalid endpoint, must be an absolute path: {endpoint}')

        self.client = client
        self.endpoint = endpoint
        self.connect: Optional[Connect] = None

    async def __aenter__(self) -> RealtimeServiceConnection:
        if self.connect is not None:
            raise Exception('already connected')
        connect = Connect(f'{self.client.ws_url_base}{self.endpoint}')
        self.connect = connect
        return RealtimeServiceConnection(await connect.__aenter__())

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        connect = self.connect
        if connect is None:
            return
        self.connect = None
        await connect.__aexit__(exc_type, exc_value, traceback)
        pass
