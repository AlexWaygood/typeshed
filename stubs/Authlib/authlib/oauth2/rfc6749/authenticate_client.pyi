"""authlib.oauth2.rfc6749.authenticate_client.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Registry of client authentication methods, with 3 built-in methods:

1. client_secret_basic
2. client_secret_post
3. none

The "client_secret_basic" method is used a lot in examples of `RFC6749`_,
but the concept of naming are introduced in `RFC7591`_.

.. _`RFC6749`: https://tools.ietf.org/html/rfc6749
.. _`RFC7591`: https://tools.ietf.org/html/rfc7591
"""

from collections.abc import Callable, Collection

from authlib.oauth2 import OAuth2Request
from authlib.oauth2.rfc6749 import ClientMixin

__all__ = ["ClientAuthentication"]

class ClientAuthentication:
    query_client: Callable[[str], ClientMixin]
    def __init__(self, query_client: Callable[[str], ClientMixin]) -> None: ...
    def register(self, method: str, func: Callable[[Callable[[str], ClientMixin], OAuth2Request], ClientMixin]) -> None: ...
    def authenticate(self, request: OAuth2Request, methods: Collection[str], endpoint: str) -> ClientMixin: ...
    def __call__(self, request: OAuth2Request, methods: Collection[str], endpoint: str = "token") -> ClientMixin: ...
