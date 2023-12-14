
from typing import cast, List, Optional, Any

from nextpyp.client import Client as RealClient
from nextpyp.client.gen import Services


class MockClient:

    def __init__(self) -> None:
        self.services=Services(self.mock())
        self.last_params: Optional[List[Any]] = None
        self.next_response: Optional[Any] = None

    def mock(self) -> RealClient:
        return cast(RealClient, self)

    def _call(self, endpoint: str, params: List[Any]) -> Optional[Any]:
        self.last_params = params
        if self.next_response is None:
            raise Exception("set a next_response")
        out = self.next_response
        self.next_response = None
        return out
