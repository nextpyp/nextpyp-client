
from __future__ import annotations

import json
from websockets.legacy.client import Connect, WebSocketClientProtocol

from types import TracebackType
from typing import Optional, Any, Type, TYPE_CHECKING, TypeVar, Generic, Callable, cast

if TYPE_CHECKING:
    from nextpyp.client import Client
    from nextpyp.client.gen import RealTimeS2C


C = TypeVar('C')


class RealtimeServiceUnexpectedBytes(Exception):

    def __init__(self) -> None:
        super(RealtimeServiceUnexpectedBytes, self).__init__("expected websocket server to send str, but got bytes instead")


class RealtimeServiceUnexpectedMessage(Exception):

    def __init__(self, type: Optional[str]) -> None:
        super(RealtimeServiceUnexpectedMessage, self).__init__(f"received unexpected message type from websocket: {type}")
        self.type = type


class RealtimeServiceError(Exception):

    def __init__(self, e: RealTimeS2C.Error) -> None:
        super(RealtimeServiceError, self).__init__(f'{e.name}: {e.msg}')
        self.e = e


class RealtimeServiceConnection:

    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        self.websocket = websocket

    async def _send(self, msg: Any) -> None:
        websocket = self.websocket
        if websocket is None:
            raise Exception('not connected')
        json_str = json.dumps(msg)
        await websocket.send(json_str)

    async def _recv(self) -> Any:

        websocket = self.websocket
        if websocket is None:
            raise Exception('not connected')

        # wait for the next message from the server
        recvd = await websocket.recv()

        # make sure we got a string frame
        if type(recvd) is bytes:
            raise RealtimeServiceUnexpectedBytes()
        recvd = cast(str, recvd)

        # try to interpret as JSON
        msg = json.loads(recvd)

        # look for error messages in the response
        from nextpyp.client.gen import RealTimeS2C
        if msg.get('type') == RealTimeS2C.Error.TYPE_ID:
            e = RealTimeS2C.Error.from_json(msg)
            raise RealtimeServiceError(e)

        # otherwise, return the received message
        return msg


class RealtimeService(Generic[C]):
    """
    An asyncio client for nextPYP realtime web services
    """

    def __init__(self, client: Client, endpoint: str, ctor: Callable[[WebSocketClientProtocol], C]) -> None:

        # the path should be absolute
        if not endpoint.startswith('/'):
            raise Exception(f'invalid endpoint, must be an absolute path: {endpoint}')

        self.client = client
        self._endpoint = endpoint
        self._connect: Optional[Connect] = None
        self._ctor = ctor

    async def __aenter__(self) -> C:

        if self._connect is not None:
            raise Exception('already connected')

        # init the connection, but don't connect to the server yet
        connect = self.client._connect_websocket(self._endpoint)
        self._connect = connect

        # connect to the server
        websocket = await connect.__aenter__()

        return self._ctor(websocket)

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None:
        connect = self._connect
        if connect is None:
            return
        self._connect = None
        await connect.__aexit__(exc_type, exc_value, traceback)
        pass
