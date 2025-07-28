"""
oauthlib.oauth2.rfc6749
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming and providing OAuth 2.0 RFC6749.
"""

from _typeshed import Incomplete
from logging import Logger

from oauthlib.common import _HTTPMethod

from .base import BaseEndpoint

log: Logger

class AuthorizationEndpoint(BaseEndpoint):
    """Authorization endpoint - used by the client to obtain authorization
    from the resource owner via user-agent redirection.

    The authorization endpoint is used to interact with the resource
    owner and obtain an authorization grant.  The authorization server
    MUST first verify the identity of the resource owner.  The way in
    which the authorization server authenticates the resource owner (e.g.
    username and password login, session cookies) is beyond the scope of
    this specification.

    The endpoint URI MAY include an "application/x-www-form-urlencoded"
    formatted (per `Appendix B`_) query component,
    which MUST be retained when adding additional query parameters.  The
    endpoint URI MUST NOT include a fragment component::

        https://example.com/path?query=component             # OK
        https://example.com/path?query=component#fragment    # Not OK

    Since requests to the authorization endpoint result in user
    authentication and the transmission of clear-text credentials (in the
    HTTP response), the authorization server MUST require the use of TLS
    as described in Section 1.6 when sending requests to the
    authorization endpoint::

        # We will deny any request which URI schema is not with https

    The authorization server MUST support the use of the HTTP "GET"
    method [RFC2616] for the authorization endpoint, and MAY support the
    use of the "POST" method as well::

        # HTTP method is currently not enforced

    Parameters sent without a value MUST be treated as if they were
    omitted from the request.  The authorization server MUST ignore
    unrecognized request parameters.  Request and response parameters
    MUST NOT be included more than once::

        # Enforced through the design of oauthlib.common.Request

    .. _`Appendix B`: https://tools.ietf.org/html/rfc6749#appendix-B
    """

    def __init__(self, default_response_type: str, default_token_type: str, response_types: dict[str, Incomplete]) -> None: ...
    @property
    def response_types(self) -> dict[str, Incomplete]: ...
    @property
    def default_response_type(self) -> str: ...
    @property
    def default_response_type_handler(self): ...
    @property
    def default_token_type(self): ...
    def create_authorization_response(
        self,
        uri: str,
        http_method: _HTTPMethod = "GET",
        body: str | None = None,
        headers: dict[str, str] | None = None,
        scopes=None,
        credentials: dict[str, Incomplete] | None = None,
    ):
        """Extract response_type and route to the designated handler."""

    def validate_authorization_request(
        self, uri: str, http_method: _HTTPMethod = "GET", body: str | None = None, headers: dict[str, str] | None = None
    ):
        """Extract response_type and route to the designated handler."""
