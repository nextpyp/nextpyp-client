
from typing import Optional, List, Any

from websockets.legacy.client import Connect

import nextpyp.client.jsonrpc as jsonrpc
from nextpyp.client.credentials import Credentials
from nextpyp.client.gen import Services, RealtimeServices


class Client:
    """
    Client for the NextPYP website.

    A complete listing of what services are available what services are available can be found at:

    * :py:class:`.Services` for regular services
    * :py:class:`.RealtimeServices` for realtime services

    Examples
    --------

    Before the client can be fully used, your app must ask for permission from the NextPYP user.
    Start by requesting an app token by using the client in unauthenticated mode.

    .. code-block:: python

        from nextpyp.client import Client

        client = Client('https://nextpyp.my.org')
        token_data = client.services.apps.request_token(
            user_id='jeff',
            app_name='My App',
            app_permission_ids=['project_list']
        )
        print(f'token data: {token_data}')

    The above example will print output similar to the following.

    .. code-block:: text

        AppTokenRequestData[request_id='the-request-id', app_name='My App', permissions=[AppPermissionData[...]]]

    Once the token has been requested, the user (``jeff`` in this example) should approve the request
    on the website and copy the app token into your app. The app token is just a string, so it should
    be easy to handle.

    Once you have the app token, you can use the client in authenticated mode
    which allows access to the services on behalf of the user according to the assigned permissions.

    .. code-block:: python

        client = Client(
            url_base='https://nextpyp.my.org',
            credentials=Credentials(
                userid='jeff',
                token='the-app-token'
            )
        )
        projects = client.services.projects.list('jeff')

    """

    def __init__(self, url_base: str, credentials: Optional[Credentials]) -> None:
        """
        Create a new client that can connect to the website at the given URL

        Parameters
        ----------
        url_base
            The base of the URL for your NextPYP website.

            Only the scheme and authority parts of the URL should be included,
            but not any path part.

            For example: ``https://nextpyp.my.org``

            If a port is needed, include it with a colon: ``http://nextpyp.my.org:8080``

        credentials
            The credentials, if any, to be used with this client.

            Omit this parameter to use the client in unauthenticated mode.
            Unauthenticated mode is only able to access a limited set of services.

            TODO: document what these services are
        """

        self.url_base: str = url_base
        """The URL passed into ``__init__``"""

        self.credentials: Optional[Credentials] = credentials
        """The credentials, if any, passed into ``__init__``"""

        self.services: Services = Services(self)
        """
        All of the services available with this client.
        See the :py:class:`.Services` Class for a complete listing.
        """

        self.realtime_services: RealtimeServices = RealtimeServices(self)
        """
        All of the realtime services available with this client.
        See the :py:class:`.RealtimeServices` Class for a complete listing.
        """

        # convert the base url to the websockets protocol
        url_parts = url_base.split(':')
        url_parts[0] = 'ws'
        self.ws_url_base = ':'.join(url_parts)

    def _call(self, endpoint: str, params: List[Any]) -> Optional[Any]:
        return jsonrpc.call(self.url_base, endpoint, self.credentials, params)

    def _connect_websocket(self, endpoint: str) -> Connect:

        # build the headers, if any
        headers = {}
        if self.credentials is not None:
            headers['nextpyp-userid'] = self.credentials.userid
            headers['nextpyp-token'] = self.credentials.token

        return Connect(f'{self.ws_url_base}{endpoint}', extra_headers=headers)
