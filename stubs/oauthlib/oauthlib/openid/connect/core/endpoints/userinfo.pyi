"""
oauthlib.openid.connect.core.endpoints.userinfo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of userinfo endpoint.
"""

from collections.abc import Mapping
from logging import Logger

from oauthlib.common import Request, _HTTPMethod
from oauthlib.oauth2.rfc6749.endpoints.base import BaseEndpoint
from oauthlib.oauth2.rfc6749.request_validator import RequestValidator as OAuth2RequestValidator
from oauthlib.oauth2.rfc6749.tokens import BearerToken

log: Logger

class UserInfoEndpoint(BaseEndpoint):
    """Authorizes access to userinfo resource."""

    bearer: BearerToken
    request_validator: OAuth2RequestValidator
    def __init__(self, request_validator: OAuth2RequestValidator) -> None: ...
    def create_userinfo_response(
        self,
        uri: str,
        http_method: _HTTPMethod = "GET",
        body: str | dict[str, str] | list[tuple[str, str]] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> tuple[dict[str, str], str, int]:
        """Validate BearerToken and return userinfo from RequestValidator

        The UserInfo Endpoint MUST return a
        content-type header to indicate which format is being returned. The
        content-type of the HTTP response MUST be application/json if the
        response body is a text JSON object; the response body SHOULD be encoded
        using UTF-8.
        """

    def validate_userinfo_request(self, request: Request) -> None:
        """Ensure the request is valid.

        5.3.1.  UserInfo Request
        The Client sends the UserInfo Request using either HTTP GET or HTTP
        POST. The Access Token obtained from an OpenID Connect Authentication
        Request MUST be sent as a Bearer Token, per `Section 2`_ of OAuth 2.0
        Bearer Token Usage [RFC6750].

        It is RECOMMENDED that the request use the HTTP GET method and the
        Access Token be sent using the Authorization header field.

        The following is a non-normative example of a UserInfo Request:

        .. code-block:: http

            GET /userinfo HTTP/1.1
            Host: server.example.com
            Authorization: Bearer SlAV32hkKG

        5.3.3. UserInfo Error Response
        When an error condition occurs, the UserInfo Endpoint returns an Error
        Response as defined in `Section 3`_ of OAuth 2.0 Bearer Token Usage
        [RFC6750]. (HTTP errors unrelated to RFC 6750 are returned to the User
        Agent using the appropriate HTTP status code.)

        The following is a non-normative example of a UserInfo Error Response:

        .. code-block:: http

            HTTP/1.1 401 Unauthorized
            WWW-Authenticate: Bearer error="invalid_token",
                error_description="The Access Token expired"

        .. _`Section 2`: https://datatracker.ietf.org/doc/html/rfc6750#section-2
        .. _`Section 3`: https://datatracker.ietf.org/doc/html/rfc6750#section-3
        """
