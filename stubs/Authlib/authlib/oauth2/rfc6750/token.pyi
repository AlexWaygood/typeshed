from collections.abc import Callable
from typing import Protocol

from authlib.oauth2.rfc6749 import ClientMixin

class _TokenGenerator(Protocol):
    def __call__(self, *, client: ClientMixin, grant_type: str, user, scope: str) -> str: ...

class BearerTokenGenerator:
    """Bearer token generator which can create the payload for token response
    by OAuth 2 server. A typical token response would be:

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json;charset=UTF-8
        Cache-Control: no-store
        Pragma: no-cache

        {
            "access_token":"mF_9.B5f-4.1JqM",
            "token_type":"Bearer",
            "expires_in":3600,
            "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA"
        }
    """

    DEFAULT_EXPIRES_IN: int
    GRANT_TYPES_EXPIRES_IN: dict[str, int]
    access_token_generator: _TokenGenerator
    refresh_token_generator: _TokenGenerator
    expires_generator: Callable[[ClientMixin, str], int]
    def __init__(
        self,
        access_token_generator: _TokenGenerator,
        refresh_token_generator: _TokenGenerator | None = None,
        expires_generator: Callable[[ClientMixin, str], int] | None = None,
    ) -> None: ...
    @staticmethod
    def get_allowed_scope(client: ClientMixin, scope: str) -> str: ...
    def generate(
        self,
        grant_type: str,
        client: ClientMixin,
        user=None,
        scope: str | None = None,
        expires_in: int | None = None,
        include_refresh_token: bool = True,
    ) -> dict[str, str | int]:
        """Generate a bearer token for OAuth 2.0 authorization token endpoint.

        :param client: the client that making the request.
        :param grant_type: current requested grant_type.
        :param user: current authorized user.
        :param expires_in: if provided, use this value as expires_in.
        :param scope: current requested scope.
        :param include_refresh_token: should refresh_token be included.
        :return: Token dict
        """

    def __call__(
        self,
        grant_type: str,
        client: ClientMixin,
        user=None,
        scope: str | None = None,
        expires_in: int | None = None,
        include_refresh_token: bool = True,
    ) -> dict[str, str | int]: ...
