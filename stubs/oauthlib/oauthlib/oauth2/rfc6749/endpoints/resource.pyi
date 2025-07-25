"""
oauthlib.oauth2.rfc6749
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming and providing OAuth 2.0 RFC6749.
"""

from _typeshed import Incomplete
from logging import Logger

from oauthlib.common import Request, _HTTPMethod

from .base import BaseEndpoint

log: Logger

class ResourceEndpoint(BaseEndpoint):
    """Authorizes access to protected resources.

    The client accesses protected resources by presenting the access
    token to the resource server.  The resource server MUST validate the
    access token and ensure that it has not expired and that its scope
    covers the requested resource.  The methods used by the resource
    server to validate the access token (as well as any error responses)
    are beyond the scope of this specification but generally involve an
    interaction or coordination between the resource server and the
    authorization server::

        # For most cases, returning a 403 should suffice.

    The method in which the client utilizes the access token to
    authenticate with the resource server depends on the type of access
    token issued by the authorization server.  Typically, it involves
    using the HTTP "Authorization" request header field [RFC2617] with an
    authentication scheme defined by the specification of the access
    token type used, such as [RFC6750]::

        # Access tokens may also be provided in query and body
        https://example.com/protected?access_token=kjfch2345sdf   # Query
        access_token=sdf23409df   # Body
    """

    def __init__(self, default_token: str, token_types: dict[str, Incomplete]) -> None: ...
    @property
    def default_token(self) -> str: ...
    @property
    def default_token_type_handler(self): ...
    @property
    def tokens(self) -> dict[str, Incomplete]: ...
    def verify_request(
        self,
        uri: str,
        http_method: _HTTPMethod = "GET",
        body: str | None = None,
        headers: dict[str, str] | None = None,
        scopes=None,
    ) -> tuple[bool, Request]:
        """Validate client, code etc, return body + headers"""

    def find_token_type(self, request: Request):
        """Token type identification.

        RFC 6749 does not provide a method for easily differentiating between
        different token types during protected resource access. We estimate
        the most likely token type (if any) by asking each known token type
        to give an estimation based on the request.
        """
