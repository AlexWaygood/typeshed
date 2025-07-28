"""
oauthlib.oauth2.rfc8628
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming and providing OAuth 2.0 Device Authorization RFC8628.
"""

from _typeshed import Incomplete
from collections.abc import Callable

from oauthlib.oauth2.rfc6749.clients.base import Client, _TokenPlacement

class DeviceClient(Client):
    """A public client utilizing the device authorization workflow.

    The client can request an access token using a device code and
    a public client id associated with the device code as defined
    in RFC8628.

    The device authorization grant type can be used to obtain both
    access tokens and refresh tokens and is intended to be used in
    a scenario where the device being authorized does not have a
    user interface that is suitable for performing authentication.
    """

    grant_type: str
    client_secret: str | None
    def __init__(
        self,
        client_id: str,
        *,
        client_secret: str | None = None,
        default_token_placement: _TokenPlacement = "auth_header",
        token_type: str = "Bearer",
        access_token: str | None = None,
        refresh_token: str | None = None,
        mac_key: str | bytes | bytearray | None = None,
        mac_algorithm: str | None = None,
        token: dict[str, Incomplete] | None = None,
        scope: str | set[object] | tuple[object] | list[object] | None = None,
        state: str | None = None,
        redirect_url: str | None = None,
        state_generator: Callable[[], str] = ...,
        code_verifier: str | None = None,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
        **kwargs,
    ) -> None: ...
    def prepare_request_uri(
        self, uri: str, scope: str | set[object] | tuple[object] | list[object] | None = None, **kwargs
    ) -> str: ...
    def prepare_request_body(
        self,
        device_code: str,
        body: str = "",
        scope: str | set[object] | tuple[object] | list[object] | None = None,
        include_client_id: bool = False,
        **kwargs,
    ) -> str:
        """Add device_code to request body

        The client makes a request to the token endpoint by adding the
        device_code as a parameter using the
        "application/x-www-form-urlencoded" format to the HTTP request
        body.

        :param body: Existing request body (URL encoded string) to embed parameters
                     into. This may contain extra parameters. Default ''.
        :param scope:   The scope of the access request as described by
                        `Section 3.3`_.

        :param include_client_id: `True` to send the `client_id` in the
                                  body of the upstream request. This is required
                                  if the client is not authenticating with the
                                  authorization server as described in
                                  `Section 3.2.1`_. False otherwise (default).
        :type include_client_id: Boolean

        :param kwargs:  Extra credentials to include in the token request.

        The prepared body will include all provided device_code as well as
        the ``grant_type`` parameter set to
        ``urn:ietf:params:oauth:grant-type:device_code``::

            >>> from oauthlib.oauth2 import DeviceClient
            >>> client = DeviceClient('your_id', 'your_code')
            >>> client.prepare_request_body(scope=['hello', 'world'])
            'grant_type=urn:ietf:params:oauth:grant-type:device_code&scope=hello+world'

        .. _`Section 3.2.1`: https://datatracker.ietf.org/doc/html/rfc6749#section-3.2.1
        .. _`Section 3.3`: https://datatracker.ietf.org/doc/html/rfc6749#section-3.3
        .. _`Section 3.4`: https://datatracker.ietf.org/doc/html/rfc8628#section-3.4
        """
