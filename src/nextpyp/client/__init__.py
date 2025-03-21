
from typing import Optional, List, Any

from websockets.legacy.client import Connect
import semver

import nextpyp.client.jsonrpc as jsonrpc
from nextpyp.client.credentials import Credentials
from nextpyp.client.gen import API_VERSION, Services, RealtimeServices


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

    .. rubric:: Version Compatibility

    The nextPYP publishes a `SemVer`_ version number to communicate compatibility information with clients.

    .. _SemVer: https://semver.org

    It's a good idea to check if your client version is compatible with the website API version
    before using it. This will help warn you if the website API has been updated with a breaking change,
    but the client hasn't been updated to match yet.

    .. code-block:: python

        client = Client('https://nextpyp.my.org')
        if not client.is_compatible():
            raise Exception("Client might not work anymore, time to update")

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
            Unauthenticated mode is only able to access a limited set of service functions.
            These service functions are marked as **Permission Needed:** ``none`` in the documentation.
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

        self.api_version: str = API_VERSION
        """
        The nextPYP API version this client was built against.
        """

        # setup the transport
        self._transport: NetworkTransport = NetworkTransport(url_base, credentials)

    def is_compatible(self) -> bool:
        """
        Asks the nextPYP website for its API version number and compares it to the version
        number built into this client. This client is compatible with the website if (and only if)
        the two major version numbers match and the client minor version is less than or equal to the server.

        In this case, compatibility means that every service supported by the client is also supported
        by the server.
        """

        # collect the version numbers
        local_api_version = semver.Version.parse(self.api_version)
        remote_api_version = semver.Version.parse(self.services.apps.versions().api_version)

        # two SemVer versions are compatible iff the major numbers match
        return local_api_version.major == remote_api_version.major \
            and local_api_version.minor <= remote_api_version.minor


class NetworkTransport:

    def __init__(self, url_base: str, credentials: Optional[Credentials]) -> None:

        self.url_base = url_base
        self.credentials = credentials

        # convert the base url to the websockets protocol
        url_parts = url_base.split(':')
        if url_parts[0] == 'http':
            url_parts[0] = 'ws'
        elif url_parts[0] == 'https':
            url_parts[0] = 'wss'
        else:
            raise Exception(f"unexpected url_base protocol \"{url_parts[0]}\", try one of ['http','https']")
        self.ws_url_base = ':'.join(url_parts)

    def call(self, endpoint: str, params: List[Any]) -> Optional[Any]:
        return jsonrpc.call(self.url_base, endpoint, self.credentials, params)

    def connect_websocket(self, endpoint: str) -> Connect:

        # build the headers, if any
        headers = {}
        if self.credentials is not None:
            headers['nextpyp-userid'] = self.credentials.userid
            headers['nextpyp-token'] = self.credentials.token

        return Connect(f'{self.ws_url_base}{endpoint}', extra_headers=headers)
