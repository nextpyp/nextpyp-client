
import textwrap
import json

import requests  # https://requests.readthedocs.io/en/latest/

from typing import cast, List, Any, Dict, Optional

from nextpyp.client.credentials import Credentials


def call(url_base: str, endpoint: str, credentials: Optional[Credentials], params: List[Any]) -> Optional[Any]:

    # NOTE: jsonrpcclient can't parse responses from kvision correctly
    # probably because kvision isn't really following the spec,
    # so let's just implement kvision-flavored JSONRPC here instead of using a real library

    # endpoints must be absolute paths
    if not endpoint.startswith('/'):
        raise Exception(f'invalid endpoint, must be an absolute path: {endpoint}')

    # build the JSONRPC request
    request_body = _request_body(endpoint, params)

    # DEBUG
    # print(f'request = {request_body}')

    # build the headers, if any
    headers = {}
    if credentials is not None:
        headers['nextpyp-userid'] = credentials.userid
        headers['nextpyp-token'] = credentials.token

    # NOTE: all kvision endpoints seem to use POST, regardless of arguments
    response = requests.post(f'{url_base}{endpoint}', headers=headers, json=request_body)

    return _handle_response(response)


def _request_body(endpoint: str, params: List[Any]) -> Dict[str, Any]:

    # endpoints must be absolute paths
    if not endpoint.startswith('/'):
        raise Exception(f'invalid endpoint, must be an absolute path: {endpoint}')

    # build the JSONRPC request
    return {
        'id': 1,
        'method': endpoint,
        # kvision exepects each arg to be a json-encoded string
        'params': [json.dumps(p) for p in params]
    }


def _handle_response(response: requests.Response) -> Any:

    if response.status_code != 200:
        raise HttpError(response.reason, response.status_code)

    # try to parse the response as json
    response_body = response.json()

    # DEBUG
    # print(f'response = {response_body}')

    def response_get(key: str) -> Optional[Any]:
        nonlocal response_body
        try:
            return response_body[key]
        except KeyError:
            return None

    # handle any kvision error in the response
    error = response_get('error')
    if error is not None:
        raise RpcError(error, cast(Optional[str], response_get('exceptionType')))

    result = response_get('result')
    if result is None:
        return None

    # kvision sends the result as a JSON string, which must be parsed again
    return json.loads(result)


class HttpError(Exception):

    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.code = code

    def __str__(self) -> str:
        return textwrap.dedent(f'''
            Error from HTTP server:
              Code:  {self.code}
               Msg:  {self.args[0]}
        ''')


class RpcError(Exception):

    def __init__(self, message: str, exception_type: Optional[str]) -> None:
        super().__init__(message)
        self.exception_type = exception_type

    def __str__(self) -> str:
        return textwrap.dedent(f'''
            Error from NextPYP:
                 Type:  {self.exception_type}
              Message:  {self.args[0]}
        ''')
