
from __future__ import annotations

import json
from websockets.legacy.client import Connect, WebSocketClientProtocol

from types import TracebackType
from typing import Optional, Any, Type, TYPE_CHECKING, TypeVar, Generic, Callable, cast

if TYPE_CHECKING:
    from nextpyp.client import Client


C = TypeVar('C')


class RealtimeServiceUnexpectedBytes(Exception):

    def __init__(self) -> None:
        super(RealtimeServiceUnexpectedBytes, self).__init__("expected websocket server to send str, but got bytes instead")


class RealtimeServiceUnexpectedMessage(Exception):

    def __init__(self, type: str) -> None:
        super(RealtimeServiceUnexpectedMessage, self).__init__(f"websocket sent unexpected message type: {type}")
        self.type = type


class RealtimeServiceError(Exception):

    def __init__(self, name: Optional[str], msg: Optional[str]) -> None:
        super(RealtimeServiceError, self).__init__(f'{name}: {msg}')
        self.name = name
        self.msg = msg


class RealtimeServiceConnection:

    def __init__(self, websocket: WebSocketClientProtocol) -> None:
        self.websocket = websocket

    async def _send(self, msg: Any) -> None:
        websocket = self.websocket
        if websocket is None:
            raise Exception('not connected')
        await websocket.send(msg)

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

        # look for error messages in the response
        if recvd.startswith('{"type":"edu.duke.bartesaghi.micromon.services.RealTimeS2C.Error"'):
            msg = json.loads(recvd)
            try:
                err_name = cast(str, msg['name'])
            except KeyError:
                err_name = None
            try:
                err_msg = cast(str, msg['msg'])
            except KeyError:
                err_msg = None
            raise RealtimeServiceError(err_name, err_msg)

        # otherwise, return the received message
        return recvd


class RealtimeService(Generic[C]):
    """
    An asyncio client for nextPYP realtime web services
    """

    def __init__(self, client: Client, endpoint: str, ctor: Callable[[WebSocketClientProtocol], C]) -> None:

        # the path should be absolute
        if not endpoint.startswith('/'):
            raise Exception(f'invalid endpoint, must be an absolute path: {endpoint}')

        self.client = client
        self.endpoint = endpoint
        self.connect: Optional[Connect] = None
        self.ctor = ctor

    async def __aenter__(self) -> C:

        if self.connect is not None:
            raise Exception('already connected')

        # build the headers, if any
        headers = {}
        if self.client.credentials is not None:
            headers['nextpyp-userid'] = self.client.credentials.userid
            headers['nextpyp-token'] = self.client.credentials.token

        # init the connection, but don't connect to the server yet
        connect = Connect(f'{self.client.ws_url_base}{self.endpoint}', extra_headers=headers)
        self.connect = connect

        # connect to the server
        websocket = await connect.__aenter__()

        return self.ctor(websocket)

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
