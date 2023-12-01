
from nextpyp.client.jsonrpc import increment

def test_foo() -> None:
    assert increment(1) == 2
