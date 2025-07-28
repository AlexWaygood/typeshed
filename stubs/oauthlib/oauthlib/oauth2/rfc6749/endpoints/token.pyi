"""
oauthlib.oauth2.rfc6749
~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for consuming and providing OAuth 2.0 RFC6749.
"""

from _typeshed import Incomplete
from logging import Logger
from typing import Literal

from oauthlib.common import Request, _HTTPMethod

from .base import BaseEndpoint

log: Logger

class TokenEndpoint(BaseEndpoint):
    """Token issuing endpoint.

    The token endpoint is used by the client to obtain an access token by
    presenting its authorization grant or refresh token.  The token
    endpoint is used with every authorization grant except for the
    implicit grant type (since an access token is issued directly).

    The means through which the client obtains the location of the token
    endpoint are beyond the scope of this specification, but the location
    is typically provided in the service documentation.

    The endpoint URI MAY include an "application/x-www-form-urlencoded"
    formatted (per `Appendix B`_) query component,
    which MUST be retained when adding additional query parameters.  The
    endpoint URI MUST NOT include a fragment component::

        https://example.com/path?query=component             # OK
        https://example.com/path?query=component#fragment    # Not OK

    Since requests to the token endpoint result in the transmission of
    clear-text credentials (in the HTTP request and response), the
    authorization server MUST require the use of TLS as described in
    Section 1.6 when sending requests to the token endpoint::

        # We will deny any request which URI schema is not with https

    The client MUST use the HTTP "POST" method when making access token
    requests::

        # HTTP method is currently not enforced

    Parameters sent without a value MUST be treated as if they were
    omitted from the request.  The authorization server MUST ignore
    unrecognized request parameters.  Request and response parameters
    MUST NOT be included more than once::

        # Delegated to each grant type.

    .. _`Appendix B`: https://tools.ietf.org/html/rfc6749#appendix-B
    """

    valid_request_methods: tuple[Literal["POST"]]
    def __init__(self, default_grant_type: str, default_token_type: str, grant_types: dict[str, Incomplete]) -> None: ...
    @property
    def grant_types(self) -> dict[str, Incomplete]: ...
    @property
    def default_grant_type(self) -> str: ...
    @property
    def default_grant_type_handler(self): ...
    @property
    def default_token_type(self) -> str: ...
    def create_token_response(
        self,
        uri: str,
        http_method: _HTTPMethod = "POST",
        body: str | None = None,
        headers: dict[str, str] | None = None,
        credentials=None,
        grant_type_for_scope=None,
        claims=None,
    ):
        """Extract grant_type and route to the designated handler."""

    def validate_token_request(self, request: Request) -> None: ...
