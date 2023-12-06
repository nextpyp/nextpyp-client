
import pytest
import requests

import nextpyp.client.jsonrpc as jsonrpc

from typing import Any, Dict, Optional, cast


def test_request_endpoints() -> None:
    """check for invalid endpoints"""

    jsonrpc._request_body('/foo', [])
    jsonrpc._request_body('/foo/bar', [])

    with pytest.raises(Exception):
        jsonrpc._request_body('foo', [])
        jsonrpc._request_body('foo/bar', [])


def test_request_params() -> None:
    """check request params are encoded correctly"""

    r = jsonrpc._request_body('/foo', [])
    assert r['params'] == []

    r = jsonrpc._request_body('/foo', [1, 'bar'])
    assert r['params'] == [
        '1',
        '"bar"'
    ]


class MockResponse:

    def __init__(self, code: int) -> None:
        self.status_code: int = code
        self.reason: str = ''
        self.body: Optional[Dict[str, Any]] = None

    def mock(self) -> requests.Response:
        return cast(requests.Response, self)

    def json(self) -> Any:
        return self.body


def test_response_http_err() -> None:
    response = MockResponse(500)
    with pytest.raises(jsonrpc.HttpError) as ex_info:
        jsonrpc._handle_response(response.mock())
    assert ex_info.value.code == 500


def test_response_kvision_error() -> None:
    response = MockResponse(200)
    response.body = {
        'error': 'foo',
    }
    with pytest.raises(jsonrpc.RpcError) as ex_info:
        jsonrpc._handle_response(response.mock())
    assert ex_info.value.exception_type is None
    assert ex_info.value.args[0] == 'foo'


def test_response_kvision_error_type() -> None:
    response = MockResponse(200)
    response.body = {
        'error': 'foo',
        'exceptionType': 'err.type'
    }
    with pytest.raises(jsonrpc.RpcError) as ex_info:
        jsonrpc._handle_response(response.mock())
    assert ex_info.value.exception_type == 'err.type'
    assert ex_info.value.args[0] == 'foo'


def test_response_empty() -> None:
    response = MockResponse(200)
    response.body = {}
    result = jsonrpc._handle_response(response.mock())
    assert result is None


def test_response_str() -> None:
    response = MockResponse(200)
    response.body = {
        'result': '"foo"'
    }
    result = jsonrpc._handle_response(response.mock())
    assert result == 'foo'


def test_response_int() -> None:
    response = MockResponse(200)
    response.body = {
        'result': '5'
    }
    result = jsonrpc._handle_response(response.mock())
    assert result == 5


def test_response_list() -> None:
    response = MockResponse(200)
    response.body = {
        'result': '[5, "foo"]'
    }
    result = jsonrpc._handle_response(response.mock())
    assert result == [5, 'foo']


def test_response_dict() -> None:
    response = MockResponse(200)
    response.body = {
        'result': '{"key": "value"}'
    }
    result = jsonrpc._handle_response(response.mock())
    assert result == {
        'key': 'value'
    }
